from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from enum import Enum
from carbon_calculator import calculate_total_footprint
from database import engine, get_db
from sqlalchemy.orm import Session
from models import User, Footprint, Base
from typing import List
from datetime import datetime

Base.metadata.create_all(bind=engine)
app = FastAPI(title="CarbonLens API")

# ---------- ENUMS & MODELS ----------
class TransportMode(str, Enum):
    petrol = "petrol"
    diesel = "diesel"
    public_transport = "public_transport"

class DietType(str, Enum):
    veg = "veg"
    mixed = "mixed"
    non_veg = "non_veg"

# ---------- REQUEST MODEL ----------
class FootprintRequest(BaseModel):
    name: str
    email: str

    electricity_kwh: float = Field(..., ge=0)
    transport_mode: TransportMode
    transport_km: float = Field(..., ge=0)
    diet_type: DietType
    meals_per_month: float = Field(..., ge=0)
    waste_kg: float = Field(..., ge=0)

# ---------- RESPONSE MODEL ----------
class FootprintResponse(BaseModel):
    electricity: float
    transport: float
    food: float
    waste: float
    total: float

# history endpoint response model
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

# analytics endpoint response model
class UserAnalytics(BaseModel):
    total_records: int
    average_footprint: float
    highest_footprint: float
    lowest_footprint: float
    latest_footprint: float
    trend: str

# Recommendation Response Model
class RecommendationResponse(BaseModel):
    dominant_category: str
    recommendations: List[str]

#helper function to determine dominant category and generate recommendations
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

# ---------- ENDPOINT ----------
@app.post("/calculate", response_model=FootprintResponse)
def calculate(request: FootprintRequest, db: Session = Depends(get_db)):

    try:
        data = request.dict()

        # Convert enums to strings
        data["transport_mode"] = data["transport_mode"].value
        data["diet_type"] = data["diet_type"].value


        user = db.query(User).filter(User.email == request.email).first()

        if not user:
            user = User(name=request.name, email=request.email)
            db.add(user)
            db.commit()
            db.refresh(user)

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

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
def root():
    return {"message": "CarbonLens API is running 🚀"}

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

@app.get("/users/{email}/analytics", response_model=UserAnalytics)
def get_user_analytics(email: str, db: Session = Depends(get_db)):

    # 1️⃣ Find user
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2️⃣ Get all footprints sorted by date
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

    # 3️⃣ Determine trend
    if total_records < 2:
        trend = "insufficient data"
    else:
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

@app.get("/users/{email}/recommendations", response_model=RecommendationResponse)
def get_recommendations(email: str, db: Session = Depends(get_db)):

    # 1️⃣ Find user
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2️⃣ Get latest footprint
    latest_footprint = (
        db.query(Footprint)
        .filter(Footprint.user_id == user.id)
        .order_by(Footprint.created_at.desc())
        .first()
    )

    if not latest_footprint:
        raise HTTPException(status_code=404, detail="No footprint records found")

    # 3️⃣ Generate recommendations
    dominant_category, recommendations = generate_recommendations(latest_footprint)

    return {
        "dominant_category": dominant_category,
        "recommendations": recommendations
    }
