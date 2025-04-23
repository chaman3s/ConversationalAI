from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow Gradio to call this server 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific URL if deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest(BaseModel):
    message: str
    history: list[list[str]]

# Basic AI logic for testing (reverses message)
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_message = request.message
    ai_response = f"🤖 FastAPI says: {user_message[::-1]}"
    updated_history = request.history + [[user_message, ai_response]]
    return {"response": ai_response, "history": updated_history}