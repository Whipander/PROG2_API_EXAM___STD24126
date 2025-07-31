from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse, Response

app = FastAPI()
#1
app.get("/ping")
def get_ping():
    return Response(content = "pong", status_code=200)

