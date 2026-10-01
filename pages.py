from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.models import User
from app.security import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})


@router.get("/home-planner", response_class=HTMLResponse)
def home_planner(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("home_planner.html", {"request": request, "user": user})


@router.get("/party-planner", response_class=HTMLResponse)
def party_planner(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("party_planner.html", {"request": request, "user": user})


@router.get("/jewelry-planner", response_class=HTMLResponse)
def jewelry_planner(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("jewelry_planner.html", {"request": request, "user": user})


@router.get("/history", response_class=HTMLResponse)
def history_page(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("history.html", {"request": request, "user": user})
