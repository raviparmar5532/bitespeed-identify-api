from fastapi import FastAPI, Depends, HTTPException
from database import Base, engine
import schemas, services, database, models
from APIExceptions import APIException
from sqlalchemy.orm import Session
import asyncio
import threading
from uuid import uuid4 as uuid

# Initialize FastAPI app
app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Initialize the queue
identify_queue = asyncio.Queue()

# Dictionary to store results of tasks
task_results = {}

# Lock to ensure only one function runs at a time
function_lock = asyncio.Lock()

# Flag to check if the function is already running
is_worker_running = False

# Worker function for processing the queue
async def worker():
    global is_worker_running
    is_worker_running = True
    print(f"Looking in the queue : {identify_queue}")
    while True:
        # Wait for a task to appear in the queue
        task_id, task = await identify_queue.get()

        if task is None:
            # End the worker when a 'None' task is received (for graceful shutdown)
            break
        
        # Extract payload and db session from the task
        payload, db = task

        try:
            # Process the task
            result = await services.identify_service(payload.email, payload.phoneNumber, db)

            # Store the result in task_results
            task_results[task_id] = result
        except APIException as e:
            task_results[task_id] = None
            raise e
        # Mark the task as done
        finally:
            identify_queue.task_done()

    print("Queue completed")
    is_worker_running = False

# Define the API endpoint for identifying
@app.post("/identify", response_model=schemas.IdentifyResponse)
async def identify(payload: schemas.IdentifyRequest, db: Session = Depends(database.get_db)):
    if not payload.email and not payload.phoneNumber:
        raise HTTPException(status_code=400, detail="At least email or phoneNumber is required")

    # Create a unique task ID
    task_id = str(uuid())  # You can use any method to create a unique task ID

    # Immediately enqueue the task with the task_id
    print(f"Adding in queue : {task_id} {payload}")
    await identify_queue.put((task_id, (payload, db)))
    print(f"Addded : {identify_queue}")

    global is_worker_running
    if not is_worker_running:
        print("Starting worker")
        asyncio.create_task(worker())

    # Wait for the worker to finish processing the task
    while task_id not in task_results:
        await asyncio.sleep(0.1)  # Check for result every 100ms

    # Once the task is done, return the result
    result = task_results[task_id]
    if not result:
        raise HTTPException(status_code=500, detail="Check the logs")
    return result

@app.get("/get")
def get_db_state(db: Session = Depends(database.get_db)):
    return list(db.query(models.Contact).all())