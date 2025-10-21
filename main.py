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
