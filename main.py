# main.py
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/get_name")
def get_name(name: str = Query(...)):
    return {"name": name}
