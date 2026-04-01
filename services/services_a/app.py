from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/")
def home():
    if random.random() < 0.3:
        return {"status": "ERROR: database connection failed"}
    return {"status": "OK"}