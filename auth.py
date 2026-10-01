from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import LoginRequest, RegisterRequest
from app.security import create_access_token, get_current_user, hash_password, verify_password

router = APIRouter()


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.scalar(select(User).where(User.email == data.email.lower()))
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(email=data.email.lower(), password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Registration successful", "user_id": user.id}


@router.post("/login")
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == data.email.lower()))
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user.id)
    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=60 * 24 * 60,
    )
    return {"message": "Login successful", "user": {"id": user.id, "email": user.email}}


@router.post("/token")
def token(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    return login(data, response, db)


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}


@router.get("/session-info")
def session_info(user: User = Depends(get_current_user)):
    return {"authenticated": True, "user_id": user.id, "email": user.email}


@router.get("/session-data")
def session_data(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from app.models import RecommendationHistory
    count = db.query(RecommendationHistory).filter(RecommendationHistory.user_id == user.id).count()
    return {"user_id": user.id, "email": user.email, "recommendation_count": count}
