from fastapi import FastAPI, Form
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Define Pydantic schema
class HealthData(BaseModel):
    Gender: str = Field(..., description="Gender", example="Male", enum=["Male", "Female"])
    Occupation: str = Field(..., description="Occupation", example="Software Engineer",
                            enum=["Software Engineer", "Doctor", "Sales Representative", "Teacher",
                                  "Nurse", "Engineer", "Accountant", "Scientist", "Lawyer",
                                  "Salesperson", "Manager"])
    Sleep_Duration: float = Field(..., description="Sleep Duration in hours", example=7.2)
    QualityOfSleep: str = Field(..., description="Quality of Sleep", example="Quality of Sleep")
    Stress_Level: int = Field(..., description="Stress Level (1-10)", ge=1, le=10)
    BMI_Category: str = Field(..., description="BMI Category",
                              enum=["Overweight", "Normal", "Obese", "Normal Weight"])
    Systolic: Optional[int] = Field(None, description="Systolic Blood Pressure", example=120)
    Diastolic: Optional[int] = Field(None, description="Diastolic Blood Pressure", example=80)
    Heart_Rate: int = Field(..., description="Heart Rate", example=1234)
    Daily_Steps: int = Field(..., description="Daily Steps", example=123)

# Endpoint to render form using Jinja2
@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API endpoint to accept JSON data
@app.post("/submit/")
async def submit_data(data: HealthData):
    return data.dict()
