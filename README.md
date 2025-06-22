## 📌 Implementation Overview

To maintain consistency and accuracy across concurrent API calls involving database reads and writes, this API adopts an **asynchronous architecture** using a **queue-based system**.

- Incoming API requests are added to a **queue**.
- A **worker** process listens for new entries in the queue.
- The worker processes the requests one-by-one, performs the required database operations, and prepares the API responses.
- The worker is **resource-efficient**: it activates only when there are requests in the queue and stops when the queue is empty.

## 🚀 Technology Stack

- **Python 3.11**
- **FastAPI** — for rapid, modern API development
- **MySQL** — Relational Database
- **SQLAlchemy ORM** — Database interaction
- **SQLite** — Alternative lightweight DB for quick testing (used in `sqlite-for-deployment` branch)

## ⚙️ Installation

### 1️⃣ Using MySQL (Recommended for Production)

- Install **MySQL** using [official documentation](https://dev.mysql.com/doc/).
- Configure the following environment variables as per your setup:

```bash
DB_USER=<your_mysql_user>
DB_PASSWORD=<your_mysql_password>
DB_HOST=<your_mysql_host>
DB_PORT=<your_mysql_port>
DB_NAME=<your_database_name>
```

- These configurations are used in `database.py`.

- Clone the repository and run:

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

### 2️⃣ Using SQLite (For Quick Testing)

- Switch to the `sqlite-for-deployment` branch:

```bash
git checkout sqlite-for-deployment
```

- Run:

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

- No environment variables or additional database setup required.

## 🧪 Testing Guidelines

- When using the deployed API, the first request might take a few seconds to respond as the server wakes up.
- After the first response, subsequent API calls should respond within **~2 seconds**.

## 📚 API Endpoints

### ➤ Identify Contact

**POST** `/identify`

#### Request Body:

```json
{
  "email": "optional_email@example.com",
  "phoneNumber": "optional_numeric_string"
}
```

#### Response Body:

```json
{
  "contact": {
    "primaryContatctId": number,
    "emails": [ "primary_email", "secondary_email", ... ],
    "phoneNumbers": [ "primary_phone", "secondary_phone", ... ],
    "secondaryContactIds": [ number, ... ]
  }
}
```

> 📝 **Note**: Returns an error message string with 4XX code in case of request errors.

---

### ➤ Reset Database

**DELETE** `/reset`

#### Response Body:

```text
"Database Truncated"
```

## 🌐 Deployed API Base URL

```
https://bitespeed-identify-api-9sja.onrender.com
```

---

## ✍️ Author

Developed by [Ravi Parmar] — [raviparmar5532@gmail.com]
