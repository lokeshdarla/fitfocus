from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import Optional
import pandas as pd
from app.model import DecisionTreeModel
from app.preprocessing import Preprocessor
from app.db import save_data_to_db, fetch_data_from_db
from sklearn.model_selection import train_test_split
import joblib

app = FastAPI()

# Set up templates for HTML responses
templates = Jinja2Templates(directory="app/templates")

# Define the input data model
class HealthData(BaseModel):
    Gender: str
    Age: int
    Occupation: str
    Sleep_Duration: float
    QualityOfSleep: int
    PhysicalActivityLevel: int
    StressLevel: int
    BMICategory: str
    BloodPressure: str  # Blood Pressure as 'Systolic/Diastolic'
    HeartRate: int
    DailySteps: int  # Optional to store the prediction

@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API endpoint to accept form data
@app.post("/submit/")
async def submit_data(
    request:Request,
    Gender: str = Form(...),
    Age: int = Form(...),
    Occupation: str = Form(...),
    Sleep_Duration: float = Form(...),
    QualityOfSleep: int = Form(...),
    PhysicalActivityLevel: int = Form(...),
    StressLevel: int = Form(...),
    BMI_Category: str = Form(...),
    BloodPressure: str = Form(...),
    HeartRate: int = Form(...),
    DailySteps: int = Form(...),
):
    health_data = HealthData(
        Gender=Gender,
        Age=Age,
        Occupation=Occupation,
        Sleep_Duration=Sleep_Duration,
        QualityOfSleep=QualityOfSleep,
        PhysicalActivityLevel=PhysicalActivityLevel,
        StressLevel=StressLevel,
        BMICategory=BMI_Category,
        BloodPressure=BloodPressure,
        HeartRate=HeartRate,
        DailySteps=DailySteps
    )
    
    # Preprocess the data
    preprocessor = Preprocessor()
    preprocessed_data = preprocessor.transform(pd.DataFrame([health_data.dict()]))

    
    MODEL_PATH="/Users/lokeshnagasaidarla/Developer/webdev/sleep-health-cardio-prediction/models/dt_model.pkl"

    # Make prediction
    model = DecisionTreeModel()
    print(preprocessed_data)
    model.load_model(MODEL_PATH)
    print("before prediction")
    print(preprocessed_data)
    prediction = model.predict(preprocessed_data)
    print("After prediction")

    # Add prediction to the data before saving
    data_dict = health_data.dict()
    data_dict['SleepDisorder'] = prediction[0]  # Add predicted value to the raw data

    print(prediction[0])
    # Save the raw data to the database
    save_data_to_db(data_dict)

    # Retrain the model with the new data
    # all_data = fetch_data_from_db()  # Fetch all data from the database
    # df = all_data.rename(columns={
    #     'person_id': 'PersonId',
    #     'gender': 'Gender',
    #     'age': 'Age',
    #     'occupation': 'Occupation',
    #     'sleep_duration': 'SleepDuration',
    #     'quality_of_sleep': 'QualityOfSleep',
    #     'physical_activity_level': 'PhysicalActivityLevel',
    #     'stress_level': 'StressLevel',
    #     'bmi_category': 'BMICategory',
    #     'blood_pressure': 'BloodPressure',
    #     'heart_rate': 'HeartRate',
    #     'daily_steps': 'DailySteps',
    #     'sleep_disorder': 'SleepDisorder'
    # })
    # df = df.drop(columns=['SleepDisorder', 'PersonId'])
    # all_data_preprocessed_data=preprocessor.transform(df)  # Remove the target and ID column
    # y = all_data['sleep_disorder'].fillna('No Disorder')
    

    # # # Retrain the model
    # model.train(all_data_preprocessed_data, y)
    # model.save_model(MODEL_PATH)

    return templates.TemplateResponse("result.html", {"request": request, "data": data_dict})
