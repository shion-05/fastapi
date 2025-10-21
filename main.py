# main.py
from fastapi import FastAPI, Query

app = FastAPI()

#Hello, World! を返すエンドポイント定義
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

#クエリパラメータの取得（必須）
@app.get("/get_name")
def get_name(name: str = Query(...)): #...で「必須」
    return {"name": name}

#クエリパラメータの取得（任意）
@app.get("/get_age")
def get_age(age: int = Query(None)):#Noneで「任意」
    return {"age": age}

#クエリパラメータの取得（混合）
@app.get("/get_profile")
def get_profile(name: str = Query(...), age: int = Query(None)):
    return {"name": name, "age": age}