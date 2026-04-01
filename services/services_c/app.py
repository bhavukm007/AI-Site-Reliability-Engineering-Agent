from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/")
def home():
    if random.random() < 0.3:
        return {"status": "CRITICAL: service crashed"}
    return {"status": "OK"}