from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from enum import Enum
from carbon_calculator import calculate_total_footprint
from database import engine
from models import Base
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User, Footprint


Base.metadata.create_all(bind=engine)


app = FastAPI(title="CarbonLens API")


# ---------- ENUMS ----------

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
    return {"message": "CarbonLens API is running"}


