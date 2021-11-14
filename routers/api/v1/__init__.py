import fastapi
import os
import pymongo
import models
import time
import aiohttp
import dotenv
from motor import motor_asyncio as motor

dotenv.load_dotenv()
sess = aiohttp.ClientSession()
router = fastapi.APIRouter(prefix="/api/v1")
clients = []
allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{};:'#~\\/,.-_=+!\"£$%^*() "
try:
    uri = f"mongodb+srv://{os.environ['MONGODB_USERNAME']}:{os.environ['MONGODB_PASSWORD']}@catboyluster.pgjoe.mongodb.net/users?retryWrites=true&w=majority"
    grecaptcha_secret = os.environ['RECAPTCHA_SECRET_KEY']
except KeyError:
    print("Please set MONGODB_PASSWORD, MONGODB_USERNAME and RECAPTCHA_SECRET_KEY.")
    exit(1)

db = motor.AsyncIOMotorClient(uri)


@router.get("/thoughts", response_class=fastapi.responses.JSONResponse)
async def get_thoughts():
    cursor = db.thoughtfloat.thoughts.find().sort('last_upd', pymongo.DESCENDING)
    dc = []
    async for document in cursor:
        dc.append(document.get("data"))
    if dc:
        return fastapi.responses.JSONResponse(dc)
    else:
        return fastapi.responses.JSONResponse([], status_code=204)


@router.post("/thoughts")
async def make_thought(thought: models.NewThought):
    if len(thought.content) == 0:
        raise fastapi.exceptions.HTTPException(status_code=400, detail="No content.")
    if len(thought.content) > 240:
        raise fastapi.exceptions.HTTPException(status_code=400, detail="Content exceeds 240 characters.")
    for char in thought.content:
        if char not in allowed_chars:
            raise fastapi.exceptions.HTTPException(status_code=400, detail="Content contains invalid characters.")
    async with sess.post(f'https://www.google.com/recaptcha/api/siteverify?secret={grecaptcha_secret}&response={thought.recaptcha_token}') as response:
        if not (await response.json()).get("success"):
            raise fastapi.exceptions.HTTPException(status_code=401, detail="reCAPTCHA verification failed.")
    thought_pre = dict(thought)
    thought_pre['creation_date'] = (t := time.time())
    thought_pre['last_updated'] = t
    await db.thoughtfloat.thoughts.insert_one({"data": thought_pre})
