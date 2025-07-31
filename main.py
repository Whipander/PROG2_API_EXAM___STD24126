import base64
from typing import List
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

app = FastAPI()
#1
@app.get("/ping")
def get_ping():
    return Response(content = "pong", status_code=200)
#BONUS
@app.get("/ping/auth")
def get_auth(request: Request):
    required_value = "admin:123456"
    required_value_bytes = required_value.encode("utf-8")
    encoded_required_value = base64.b64encode(required_value_bytes)
    encoded_request_value_str = encoded_required_value.decode("utf-8")
    request_value = request.headers.get("Authorization").split(" ")[1]

    if encoded_request_value_str != request_value:
        return JSONResponse(status_code=403, content={"message": "ressource forbidden"})
    return Response(status_code=200, content="pong" )
#2
@app.get("/home")
def get_home():
    with open ("home.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return Response(content=html_content, status_code=200)


#4
class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime

posts_store: List[Post] = []

def serialize_post():
    serialized_post = []
    for post in posts_store:
        post.creation_datetime = str(post.creation_datetime)
        serialized_post.append(post.dict())
    return serialized_post
@app.post("/posts")
def create_post(posts_to_add : List[Post]):
    for post in posts_to_add:
        posts_store.append(post)
    return JSONResponse(content={"posts": serialize_post()}, status_code=201)

#5
@app.get("/posts")
def get_posts():
    return JSONResponse(content={"posts":serialize_post()}, status_code=200)
#6
@app.put("/posts")
def update_post(posts_to_update : List[Post]):
    for post in posts_to_update:
        is_found = False
        for index, old_post in enumerate(posts_store):
            if old_post.title == post.title:
                posts_store[index] = post
            is_found = True
            break
        if not is_found:
            posts_store.append(post)
    return JSONResponse(content={"posts": serialize_post()}, status_code=200)
#3
@app.get("/{full_path:path}")
def catch_all():
    with open("404.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")
