from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from enum import Enum
from carbon_calculator import calculate_total_footprint
from database import engine, get_db
from sqlalchemy.orm import Session
from models import User, Footprint, Base
from typing import List
from datetime import datetime
from pydantic import EmailStr, Field


Base.metadata.create_all(bind=engine)

app = FastAPI(title="CarbonLens API")

# ---------- CORS (IMPORTANT FOR FRONTEND) ----------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- ENUMS ----------

class TransportMode(str, Enum):
    petrol = "petrol"
    diesel = "diesel"
    public_transport = "public_transport"


class DietType(str, Enum):
    veg = "veg"
    mixed = "mixed"
    non_veg = "non_veg"


# ---------- AUTH MODELS ----------

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    id: int
    name: str
    email: str


# ---------- FOOTPRINT REQUEST ----------

class FootprintRequest(BaseModel):
    name: str
    email: str

    electricity_kwh: float = Field(..., ge=0)
    transport_mode: TransportMode
    transport_km: float = Field(..., ge=0)
    diet_type: DietType
    meals_per_month: float = Field(..., ge=0)
    waste_kg: float = Field(..., ge=0)


# ---------- FOOTPRINT RESPONSE ----------

class FootprintResponse(BaseModel):
    electricity: float
    transport: float
    food: float
    waste: float
    total: float


# ---------- HISTORY MODEL ----------

class FootprintHistoryItem(BaseModel):
    id: int
    electricity: float
    transport: float
    food: float
    waste: float
    total: float
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- ANALYTICS MODEL ----------

class UserAnalytics(BaseModel):
    total_records: int
    average_footprint: float
    highest_footprint: float
    lowest_footprint: float
    latest_footprint: float
    trend: str


# ---------- RECOMMENDATION MODEL ----------

class RecommendationResponse(BaseModel):
    dominant_category: str
    recommendations: List[str]


# ---------- RECOMMENDATION LOGIC ----------

def generate_recommendations(footprint: Footprint):

    categories = {
        "electricity": footprint.electricity,
        "transport": footprint.transport,
        "food": footprint.food,
        "waste": footprint.waste
    }

    dominant_category = max(categories, key=categories.get)

    recommendations = []

    if dominant_category == "electricity":
        recommendations.extend([
            "Switch to LED lighting.",
            "Use energy-efficient appliances.",
            "Turn off devices when not in use.",
            "Consider installing solar panels."
        ])

    elif dominant_category == "transport":
        recommendations.extend([
            "Use public transport more frequently.",
            "Consider carpooling.",
            "Switch to electric or hybrid vehicles.",
            "Reduce unnecessary travel."
        ])

    elif dominant_category == "food":
        recommendations.extend([
            "Reduce red meat consumption.",
            "Adopt more plant-based meals.",
            "Buy locally sourced food.",
            "Avoid food waste."
        ])

    elif dominant_category == "waste":
        recommendations.extend([
            "Start composting organic waste.",
            "Recycle properly.",
            "Reduce single-use plastics.",
            "Practice mindful consumption."
        ])

    return dominant_category, recommendations


# ---------- AUTH ENDPOINTS ----------

@app.post("/register", response_model=AuthResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == request.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=request.name,
        email=request.email,
        password=request.password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == request.email).first()

    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return user


# ---------- CARBON CALCULATION ----------

@app.post("/calculate", response_model=FootprintResponse)
def calculate(request: FootprintRequest, db: Session = Depends(get_db)):

    data = request.dict()

    data["transport_mode"] = data["transport_mode"].value
    data["diet_type"] = data["diet_type"].value

    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = calculate_total_footprint(data)

    footprint = Footprint(
        user_id=user.id,
        electricity=result["electricity"],
        transport=result["transport"],
        food=result["food"],
        waste=result["waste"],
        total=result["total"],
    )

    db.add(footprint)
    db.commit()

    return result


# ---------- HISTORY ----------

@app.get("/users/{email}/footprints", response_model=List[FootprintHistoryItem])
def get_user_footprints(email: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    footprints = (
        db.query(Footprint)
        .filter(Footprint.user_id == user.id)
        .order_by(Footprint.created_at.desc())
        .all()
    )

    return footprints


# ---------- ANALYTICS ----------

@app.get("/users/{email}/analytics", response_model=UserAnalytics)
def get_user_analytics(email: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    footprints = (
        db.query(Footprint)
        .filter(Footprint.user_id == user.id)
        .order_by(Footprint.created_at.asc())
        .all()
    )

    if not footprints:
        raise HTTPException(status_code=404, detail="No footprint records found")

    totals = [f.total for f in footprints]

    total_records = len(totals)
    average = sum(totals) / total_records
    highest = max(totals)
    lowest = min(totals)
    latest = totals[-1]

    trend = "insufficient data"
    if total_records >= 2:
        if totals[-1] > totals[-2]:
            trend = "increasing"
        elif totals[-1] < totals[-2]:
            trend = "decreasing"
        else:
            trend = "stable"

    return {
        "total_records": total_records,
        "average_footprint": round(average, 2),
        "highest_footprint": highest,
        "lowest_footprint": lowest,
        "latest_footprint": latest,
        "trend": trend
    }


# ---------- RECOMMENDATIONS ----------

@app.get("/users/{email}/recommendations", response_model=RecommendationResponse)
def get_recommendations(email: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    latest_footprint = (
        db.query(Footprint)
        .filter(Footprint.user_id == user.id)
        .order_by(Footprint.created_at.desc())
        .first()
    )

    if not latest_footprint:
        raise HTTPException(status_code=404, detail="No footprint records found")

    dominant_category, recommendations = generate_recommendations(latest_footprint)

    return {
        "dominant_category": dominant_category,
        "recommendations": recommendations
    }


# ---------- ROOT ----------

@app.get("/")
def root():
    return {"message": "CarbonLens API is running"}