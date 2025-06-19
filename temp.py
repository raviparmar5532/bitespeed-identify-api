from random import randrange
import json
import time
import requests

def get_random_alphabet():
    return chr(ord('a') + randrange(0, 26))

def get_random_number():
    return str(randrange(1, 10))

lst = [{
    "email": "e",
    "phoneNumber": "7"
},
{
    "email": "d",
    "phoneNumber": "6"
},
{
    "email": "y",
    "phoneNumber": "6"
},
{
    "email": "q",
    "phoneNumber": "6"
},
{
    "email": "h",
    "phoneNumber": "4"
},
{
    "email": "x",
    "phoneNumber": "6"
},
{
    "email": "t",
    "phoneNumber": "2"
},
{
    "email": "q",
    "phoneNumber": "2"
},
{
    "email": "w",
    "phoneNumber": "3"
},
{
    "email": "d",
    "phoneNumber": "7"
},
{
    "email": "m",
    "phoneNumber": "9"
},
{
    "email": "e",
    "phoneNumber": "3"
},
{
    "email": "x",
    "phoneNumber": "2"
},
{
    "email": "h",
    "phoneNumber": "8"
},
{
    "email": "q",
    "phoneNumber": "9"
},
{
    "email": "t",
    "phoneNumber": "3"
},
{
    "email": "f",
    "phoneNumber": "7"
},
{
    "email": "g",
    "phoneNumber": "4"
},
{
    "email": "e",
    "phoneNumber": "5"
},
{
    "email": "i",
    "phoneNumber": "3"
},
{
    "email": "u",
    "phoneNumber": "3"
},
{
    "email": "c",
    "phoneNumber": "5"
},
{
    "email": "p",
    "phoneNumber": "9"
},
{
    "email": "w",
    "phoneNumber": "9"
},
{
    "email": "h",
    "phoneNumber": "6"
},
{
    "email": "g",
    "phoneNumber": "1"
}]

for req in lst:
    req = json.dumps(req)
    response = requests.post("http://127.0.0.1:8000/identify", data=req)
    print(f"Request : {req}")
    if response.status_code == 500:
        break
    print(f"Response : {json.dumps(response.json(), indent=4)}")
    time.sleep(0.5)
else:
    print("run again")


# for _ in range(1000):
#     time.sleep(0.1)
#     email = get_random_alphabet()
#     phone = get_random_number()
#     body = json.dumps({
#         "email" : email,
#         "phoneNumber" : phone
#     }, indent=4)
#     response = requests.post("http://127.0.0.1:8000/identify", data=body)
#     print(f"Request : {body}")
#     if response.status_code == 500:
#         break
#     print(f"Response : {json.dumps(response.json(), indent=4)}")

