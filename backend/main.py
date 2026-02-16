from fastapi import FastAPI
from pydantic import BaseModel
from carbon_calculator import calculate_total_footprint

app = FastAPI()

@app.get("/")
def root():
    return {"message": "CarbonLens API is running"}


class FootprintRequest(BaseModel):
    electricity_kwh: float
    transport_mode: str
    transport_km: float
    diet_type: str
    meals_per_month: float
    waste_kg: float


@app.post("/calculate")
def calculate(request: FootprintRequest):
    result = calculate_total_footprint(request.dict())
    return result
