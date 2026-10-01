import io
import json
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from PIL import Image, UnidentifiedImageError
from app.database import get_db
from app.models import RecommendationHistory, User
from app.schemas import HomeRequest, PartyRequest, JewelryRequest
from app.security import get_current_user
from app.services.recommender import engine
from app.config import get_settings

router = APIRouter()


def save_history(db: Session, user_id: int, planner: str, request_data: dict, result):
    history = RecommendationHistory(
        user_id=user_id,
        planner=planner,
        request_json=json.dumps(request_data),
        response_json=result.model_dump_json(),
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


@router.post("/generate-home")
def generate_home(
    data: HomeRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = engine.home(data)
    history = save_history(db, user.id, "home", data.model_dump(), result)
    return {"history_id": history.id, "result": result.model_dump()}


@router.post("/generate-party")
def generate_party(
    data: PartyRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = engine.party(data)
    history = save_history(db, user.id, "party", data.model_dump(), result)
    return {"history_id": history.id, "result": result.model_dump()}


@router.post("/generate-jewelry")
async def generate_jewelry(
    budget: float,
    occasion: str,
    style: str,
    metal: str = "any",
    outfit_notes: str = "",
    outfit_image: UploadFile | None = File(default=None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = JewelryRequest(
        budget=budget,
        occasion=occasion,
        style=style,
        metal=metal,
        outfit_notes=outfit_notes,
    )

    image = None
    if outfit_image is not None:
        settings = get_settings()
        if outfit_image.content_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise HTTPException(status_code=400, detail="Only JPG, PNG, and WEBP images are supported")
        raw = await outfit_image.read()
        if len(raw) > settings.max_image_size_mb * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Image is too large")
        try:
            image = Image.open(io.BytesIO(raw)).convert("RGB")
        except UnidentifiedImageError as exc:
            raise HTTPException(status_code=400, detail="Invalid image file") from exc

    result = engine.jewelry(data, image=image)
    request_data = data.model_dump()
    request_data["image_uploaded"] = image is not None
    history = save_history(db, user.id, "jewelry", request_data, result)
    return {"history_id": history.id, "result": result.model_dump()}


@router.get("/recommendations-details/{history_id}")
def recommendation_details(
    history_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    history = db.get(RecommendationHistory, history_id)
    if not history or history.user_id != user.id:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return {
        "history_id": history.id,
        "planner": history.planner,
        "created_at": history.created_at.isoformat(),
        "result": json.loads(history.response_json),
    }


@router.get("/history")
def history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = (
        db.query(RecommendationHistory)
        .filter(RecommendationHistory.user_id == user.id)
        .order_by(RecommendationHistory.created_at.desc())
        .all()
    )
    return [
        {
            "id": row.id,
            "planner": row.planner,
            "created_at": row.created_at.isoformat(),
            "result": json.loads(row.response_json),
        }
        for row in rows
    ]
