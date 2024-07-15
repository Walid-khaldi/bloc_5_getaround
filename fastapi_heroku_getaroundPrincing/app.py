import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Union
from fastapi import FastAPI
from joblib import load

# API Description
description = """You can use this API to estimate the rental price of a car."""

# Tags Metadata
tags_metadata = [
    {"name": "Sample rows", "description": "Simple endpoints to try out!"},
    {"name": "Search model", "description": "Search data for a type of car model"},
    {"name": "Machine Learning", "description": "Prediction Endpoint."}
]

# Create FastAPI app
app = FastAPI(
    title="Getaround Pricing Predictor API",
    description=description,
    version="0.1",
    openapi_tags=tags_metadata
)

@app.get("/", tags=["Sample cars"])
async def load_sample_cars():
    cars = pd.read_csv("get_around_pricing_project.csv", index_col=0)
    car = cars.sample(5)
    return car.to_dict("index")

@app.get("/Search_model_key/{model_key}", tags=["Search model"])
async def search_model_key(model_key: object):
    cars = pd.read_csv("get_around_pricing_project.csv", index_col=0)
    rental_model = cars[cars["model_key"] == model_key]
    return rental_model.to_dict("index")

class PredictionFeatures(BaseModel):
    model_key: str
    mileage: Union[int, float]
    engine_power: Union[int, float]
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool

@app.post("/predict", tags=["Machine Learning"])
async def predict_post(predictionFeatures: PredictionFeatures):
    data = pd.DataFrame(dict(predictionFeatures), index=[0])
    loaded_model = load('model_xg.joblib')
    prediction = loaded_model.predict(data)
    response = {"predictions": prediction.tolist()[0]}
    return response

@app.get("/predict", tags=["Machine Learning"])
async def predict_get(
    model_key: str,
    mileage: Union[int, float],
    engine_power: Union[int, float],
    fuel: str,
    paint_color: str,
    car_type: str,
    private_parking_available: bool,
    has_gps: bool,
    has_air_conditioning: bool,
    automatic_car: bool,
    has_getaround_connect: bool,
    has_speed_regulator: bool,
    winter_tires: bool
):
    data = pd.DataFrame([{
        "model_key": model_key,
        "mileage": mileage,
        "engine_power": engine_power,
        "fuel": fuel,
        "paint_color": paint_color,
        "car_type": car_type,
        "private_parking_available": private_parking_available,
        "has_gps": has_gps,
        "has_air_conditioning": has_air_conditioning,
        "automatic_car": automatic_car,
        "has_getaround_connect": has_getaround_connect,
        "has_speed_regulator": has_speed_regulator,
        "winter_tires": winter_tires
    }])
    loaded_model = load('model_xg.joblib')
    prediction = loaded_model.predict(data)
    response = {"predictions": prediction.tolist()[0]}
    return response

if _name_ == "_main_":
    uvicorn.run(app, host="0.0.0.0", port=4000, debug=True,reload=True)