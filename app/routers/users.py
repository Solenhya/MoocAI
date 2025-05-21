from fastapi import APIRouter, Request , Depends , Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_303_SEE_OTHER
from ..dependencies import require_roles_any
from ..userManagements import auth,userAccess
from pathlib import Path
router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent  # points to /app
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/login")
async def PageLogin(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})

@router.post("/login")
async def connect(request:Request,form_data: OAuth2PasswordRequestForm=Depends()):
    try:
        auth_value =await auth.login_for_access_token(form_data)
    except ValueError as e:
        return templates.TemplateResponse("error.html",{"request":request})
    response = RedirectResponse(url="/secret", status_code=HTTP_303_SEE_OTHER)
    response.set_cookie(key="token", value=auth_value["access_token"])
    return response

@router.get("/sign_up")
async def inscription(request:Request):
    return templates.TemplateResponse("signUp.html",{"request":request})

@router.post("/createUser")
async def CreateUser(request: Request,userName:str = Form(...),userPassword:str = Form(...)):
    user = userAccess.get_user(userName)
    if user:
        raise HTTPException(status_code=409, detail="L'utilisateur existe deja")
    
    userAccess.sign_user(userName,userPassword)
    response = RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)
    return response

@router.get("/disconnect")
async def disconnect(request:Request,userData=Depends(require_roles_any(["admin","guest"]))):
    """Supprime le cookie de tokens
    Devrait etre post mais les <a> sont cancer avec le besoin de faire un form pour envoyer en post
    """
    response = RedirectResponse(url="/login",status_code=HTTP_303_SEE_OTHER)
    response.delete_cookie(key="token")
    return response

@router.get("/secret")
async def foundSecret(user_data=Depends(auth.get_current_user)):
    return {"message": f"Hello {user_data}, you have access to protected data."}