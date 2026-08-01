from fastapi import FastAPI,Request,Form,UploadFile,File,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,RedirectResponse,StreamingResponse,JSONResponse
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from agent_test import agent
from database import Check_user_password,add_user
from dotenv import load_dotenv
from filename import check_file
from pathlib import Path
import os

load_dotenv()
app = FastAPI()
template=Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["SECRET_KEY"],
    # https_only=True,
    same_site="lax",
    max_age=3600
)

@app.get("/")
def redirect(request:Request):
    return RedirectResponse(url="/register",status_code=303)

@app.get("/chat", response_class=HTMLResponse)
def home(request:Request):
    try:
        request.session["email"]
        return template.TemplateResponse(request,"index.html")
    except Exception as e:
        print("email not found")
        return RedirectResponse(url="/login",status_code=303)
    
@app.post("/chat")
async def chat(request: Request,message: str= Form(...),file: UploadFile | None = File(None)):
    try:
        email=request.session.get("email","")
        if email == "":
            raise HTTPException(status_code=401, detail="Not authenticated")
        filename=""
        if file:
            ALLOWED_EXTENIONS=[".pdf",".csv",".png",".jpg",".jpeg"]
            if Path(file.filename).suffix.lower() in ALLOWED_EXTENIONS:
                filename= check_file(file)
            else:
                return {"answer":"File extention not allowed"}
        return StreamingResponse(
            agent(email, message, filename),
            media_type="text/plain"
        )
    except KeyError:
        return {"error":"internal error"}

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return template.TemplateResponse(request, "login.html")

@app.post("/login")
async def login(
    request:Request,
    email: str = Form(...),
    password: str = Form(...)
):
    
    if Check_user_password(email,password):
        request.session["email"]=email
        return RedirectResponse(url="/chat",status_code=303)
         
    else:
        return RedirectResponse(url="/login-error",status_code=303)
    
@app.get("/login-error",response_class=HTMLResponse)
def error(request:Request):
    return template.TemplateResponse(request,"login-fail.html")

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return template.TemplateResponse(
        request,
        "register.html"
    )
@app.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    signal=add_user(username,email,password)
    if signal==None:
        return RedirectResponse(
            url="/login",
            status_code=303
        )
    else:
        return template.TemplateResponse(request,"register.html",{"error":"This email has already an account."})
    