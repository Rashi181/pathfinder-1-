from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = {} #user profile storage

messages = {} #message storage

class AskRequest(BaseModel):
    user_id: str
    message: str

@app.post("/ask")
def ask(request: AskRequest):
    user_id = request.user_id
    message = request.message

    if user_id not in users:
        users[user_id] = {"gpa": None, "interests": [], "strengths": [], "goals": []}

    if user_id not in messages:
        messages[user_id] = []

    messages[user_id].append({"role": "user", "content": message})

    response = "Thanks for your message!" #hardcoded for now

    messages[user_id].append({"role": "assistant", "content": response})

    return {"response": response}

@app.get("/messages/{user_id}")
def get_messages(user_id: str):
    if user_id not in messages:
        return {"messages": []}
    
    return {"messages": messages[user_id]}