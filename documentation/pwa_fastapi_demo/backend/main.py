from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Autoriser la PWA à communiquer avec le backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Petite mémoire interne pour la démo
messages = []

@app.get("/api/messages")
def get_messages():
    return messages

@app.post("/api/messages")
def add_message(msg: dict):
    messages.append(msg)
    return {"status": "ok", "received": msg}
