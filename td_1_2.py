from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

app = FastAPI()


@app.get("/hello")
def read_hello(request: Request, name: str = "Non défini", is_teacher: bool = False):
    accept_headers = request.headers.get("Accept")
    if accept_headers != "text/plain":
        return JSONResponse({"message": "Unsupported Media Type"}, status_code=400)
    if name != "Non défini":
        if is_teacher:
            return JSONResponse(content=f"Hello Teacher {name}", status_code=200)
        if not is_teacher:
            return JSONResponse(content=f"Hello {name}", status_code=200)
    if is_teacher is not None and name == "Non défini":
        if is_teacher:
            return JSONResponse(content=f"Hello Teacher {name}", status_code=200)
        else:
            return JSONResponse(content="Hello World", status_code=200)
    return None


class WelcomeRequest(BaseModel):
    name: str


@app.post("/welcome")
def welcome_user(request: WelcomeRequest):
    return {f"Bienvenue {request.name}"}


class SecretPayload(BaseModel):
    secret_code: int


@app.put("/top-secret")
def put_secret(request: Request, body: SecretPayload):
    authorization_secret = request.headers.get("Authorization")
    if len(str(body.secret_code)) != 4:
        return JSONResponse(content=f"Le code {body.secret_code} n'est pas un code à 4 chiffres")

    if authorization_secret is None or authorization_secret != "my-secret-key":
        return JSONResponse(content=f"La valeur fournie : {authorization_secret} ; n'est pas la valeur attendue.",
                            status_code=403)
    else:
        return JSONResponse("Accès autorisé", status_code=200)

#-------------------------------------------------------------------------------------------------------------------