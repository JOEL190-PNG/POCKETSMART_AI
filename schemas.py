from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


PlannerType = Literal["home", "party", "jewelry"]


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class HomeItem(BaseModel):
    category: str
    item: str
    quantity: int = Field(ge=1, le=100)
    max_budget: float = Field(gt=0)


class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=100_000_000)
    rooms: list[str] = Field(min_length=1, max_length=10)
    style: str = Field(default="modern", min_length=1, max_length=100)
    items: list[HomeItem] = Field(min_length=1, max_length=50)
    location: str = Field(default="India", max_length=100)


class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=100_000_000)
    guests: int = Field(gt=0, le=100_000)
    event_type: str = Field(min_length=2, max_length=100)
    venue: str = Field(min_length=2, max_length=200)
    city: str = Field(default="Chennai", max_length=100)
    preferences: str = Field(default="", max_length=1000)


class JewelryRequest(BaseModel):
    budget: float = Field(gt=0, le=100_000_000)
    occasion: str = Field(min_length=2, max_length=100)
    style: str = Field(min_length=2, max_length=100)
    metal: str = Field(default="any", max_length=50)
    outfit_notes: str = Field(default="", max_length=1000)


class Recommendation(BaseModel):
    title: str
    category: str
    platform: str
    estimated_price: float = Field(ge=0)
    quantity: int = Field(default=1, ge=1)
    reason: str
    search_url: str


class RecommendationResponse(BaseModel):
    planner: PlannerType
    summary: str
    budget: float
    estimated_total: float = Field(ge=0)
    remaining_budget: float = Field(ge=0)
    allocations: dict[str, float]
    recommendations: list[Recommendation] = Field(min_length=1)
    notes: list[str] = Field(default_factory=list)


class HistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    planner: str
    created_at: str
    result: RecommendationResponse
