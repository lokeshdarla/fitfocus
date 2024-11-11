import pandas as pd
from app.preprocessing import Preprocessor
from app.model import DecisionTreeModel
from sklearn.model_selection import train_test_split
import sqlite3

def retrain_model():
    # Connect to SQLite database
    conn = sqlite3.connect('sleep_data.db')
    df = pd.read_sql('SELECT * FROM sleep_data', conn)
    
    # Preprocess data
    preprocessor = Preprocessor()
    processed_data = preprocessor.transform(df)

    # Prepare data for model retraining
    X = processed_data.drop(columns=['sleep_disorder'])
    y = processed_data['sleep_disorder']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and retrain the model
    model = DecisionTreeModel(max_depth=5)
    model.train(X, y)
  
    model.save_model('decision_tree_model.pkl')
    
    print("Model retrained and saved successfully.")
