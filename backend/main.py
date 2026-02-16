from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from carbon_calculator import calculate_total_footprint

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
    electricity_kwh: float
    transport_mode: TransportMode
    transport_km: float
    diet_type: DietType
    meals_per_month: float
    waste_kg: float


# ---------- RESPONSE MODEL ----------

class FootprintResponse(BaseModel):
    electricity: float
    transport: float
    food: float
    waste: float
    total: float


# ---------- ENDPOINT ----------

@app.post("/calculate", response_model=FootprintResponse)
def calculate(request: FootprintRequest):
    try:
        data = request.dict()

# Convert enums to strings
        data["transport_mode"] = data["transport_mode"].value
        data["diet_type"] = data["diet_type"].value

        result = calculate_total_footprint(data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
def root():
    return {"message": "CarbonLens API is running"}


