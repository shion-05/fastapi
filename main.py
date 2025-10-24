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

#URLパラメータの場合
@app.get('/get_name2/{name2}/myname')
def get_name2(name2: str):
    return {"name": name2}

#まとめ
@app.get("/get_profile/{name2}/myname")
def get_profile(
    name2: str,                               # パスパラメータは非デフォルトを先にする（name2が非デフォルト）
    name: str = Query(...),                   # 必須クエリ
    age: int | None = Query(None)             # 任意クエリ
):
    return {"name": name, "name2": name2, "age": age}