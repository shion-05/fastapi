# main.py
from fastapi import FastAPI, Query, File, UploadFile, BackgroundTasks, Request
import user, item
import asyncio
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

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

#CSVファイルや画像などのファイルの受取
#from fastapi import FastAPI, File, UploadFile
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    # file.fileに実体が入ってくる
    data = file.file.read()  # 読み出すとポインタが末尾になる点に注意（再利用するならseek(0)が必要）
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(data)
    }

#ルーティングをまとめる
app.include_router(user.router)
app.include_router(item.router, prefix="/items", tags=["items"])

#非同期処理
@app.get("/async_demo")
async def async_demo():
    # 10回出力
    for i in range(1, 11):
        print(f"{datetime.now()}, {i}: 即時出力")

    # ”delayed_line”を実行予約
    asyncio.create_task(delayed_line())

    # すぐにレスポンスを返す
    return {"message": f"{datetime.now()}, すぐレスポンスを返すよ"}

async def delayed_line():
    await asyncio.sleep(5) #この間に”async_demo”が実行
    print(f"{datetime.now()}, 5秒後に出力されるよ")

#BackgroundTasks
@app.get("/bg_task")
async def bg_task(bg: BackgroundTasks):
    bg.add_task(time_sleep)
    return {"message": "すぐレスポンスを返すよ"}

def time_sleep():
    import time
    time.sleep(5)             # ここは同スレッド実行のため重い処理は避ける
    print("5秒後に出力されるよ")

#リクエスト前後に処理を挿入する この部分は全ての処理の前後に実行される
@app.middleware("http")
async def simple_middleware(request: Request, call_next):
    # リクエスト前の処理 
    print(f"リクエスト開始: {request.url.path}")

    # call_next(request) は「次の処理（=実際のエンドポイント）」を呼び出す
    response = await call_next(request)

    # レスポンス後の処理
    print("レスポンス完了")

    return response

@app.get("/menu")
def menu():
    return {"message": "menuです"}

#CORSの設定
# 許可するオリジン（フロントエンドのURL）
origins = [
    "http://localhost:3000",  # ローカルのReact/Vue開発環境
    "https://example.com",    # 本番環境のフロントエンド
]

# CORSMiddleware の追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # 許可するオリジン
    allow_credentials=True,           # Cookieや認証情報を含めるか
    allow_methods=["*"],              # 許可するHTTPメソッド（GET, POSTなど）
    allow_headers=["*"],              # 許可するHTTPヘッダー
)

@app.get("/menu")
def menu():
    return {"message": "menuです"}

#リクエスト（JSON）のバリデーションチェック
class Profile(BaseModel):
    name1: str
    name2: str = Field(..., min_length=5, max_length=20, description="5文字以上20文字以下")
    age: int = Field(..., gt=0, description="0より大きい整数")

@app.post("/get_profile")
def get_profile(profile: Profile):
    return {"json": profile.model_dump()}