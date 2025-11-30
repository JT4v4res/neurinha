from fastapi import FastAPI
import uuid
from utils.db_handlers.pg_handler import create_session, get_all_sessions


app = FastAPI()


@app.post("/sessions")
def create_new_session():
    result = create_session(uuid.uuid4())
    return {"response": result}


@app.get("/sessions")
def get_sessions():
    result = get_all_sessions()
    return {"response": result}
