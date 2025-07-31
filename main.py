from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse, Response

app = FastAPI()
#1
@app.get("/ping")
def get_ping():
    return Response(content = "pong", status_code=200)

#2
@app.get("/home")
def get_home():
    with open ("home.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return Response(content=html_content, status_code=200)