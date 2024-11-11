import sqlite3
import pandas as pd
from typing import Dict

# Function to save data into the database
def save_data_to_db(data: Dict):
    conn = sqlite3.connect('sleep_data.db')
    cursor = conn.cursor()

    # Create table if it does not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS sleep_data (
        person_id INTEGER PRIMARY KEY AUTOINCREMENT,
        gender TEXT,
        age INTEGER,
        occupation TEXT,
        sleep_duration REAL,
        quality_of_sleep INTEGER,
        physical_activity_level INTEGER,
        stress_level INTEGER,
        bmi_category TEXT,
        blood_pressure TEXT,
        heart_rate INTEGER,
        daily_steps INTEGER,
        sleep_disorder TEXT
    )''')

    # Insert new data
    cursor.execute('''INSERT INTO sleep_data (gender, age, occupation, sleep_duration, quality_of_sleep, 
        physical_activity_level, stress_level, bmi_category, blood_pressure, heart_rate, daily_steps, sleep_disorder) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        data['Gender'],
        data['Age'],
        data['Occupation'],
        data['Sleep_Duration'],
        data['QualityOfSleep'],
        data['PhysicalActivityLevel'],
        data['StressLevel'],
        data['BMICategory'],
        data['BloodPressure'],  # Keeping blood pressure as a string (Systolic/Diastolic)
        data['HeartRate'],
        data['DailySteps'],
        data['SleepDisorder']  # Sleep disorder prediction value
    ))

    conn.commit()
    conn.close()

# Function to fetch data from DB
def fetch_data_from_db() -> pd.DataFrame:
    conn = sqlite3.connect('sleep_data.db')
    df = pd.read_sql_query("SELECT * FROM sleep_data", conn)
    conn.close()
    return df

# Function to read data from CSV and insert into DB
def save_csv_to_db(csv_file_path: str):
    # Read CSV into DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        # Convert row to dictionary
        data = row.to_dict()
        # Save data to the database
        save_data_to_db(data)
