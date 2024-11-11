import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np


class Preprocessor:
    def __init__(self):
        # Define transformers
        self.age_binner = AgeBinner()
        self.blood_pressure_splitter = BloodPressureSplitter()

        # Column transformers
        self.column_transformer = ColumnTransformer(
            transformers=[
                ('num', Pipeline(steps=[
                    ('imputer', SimpleImputer(strategy='mean')),
                    ('scaler', StandardScaler())
                ]), ['Systolic', 'Diastolic']),
                ('gender', OneHotEncoder(), ['Gender']),
                ('label_encoder', LabelEncoderTransformer(columns=['Occupation', 'BMICategory', 'Age Group']), ['Occupation', 'BMICategory', 'Age Group'])
            ],
            remainder='passthrough'
        )

    def fit(self, X, y=None):
        # Apply the full preprocessing pipeline
        X = self.age_binner.fit_transform(X)
        X = self.blood_pressure_splitter.fit_transform(X)
        self.column_transformer.fit(X)
        return self

    def transform(self, X):
        X = self.age_binner.transform(X)
        X = self.blood_pressure_splitter.transform(X)
        print(X.columns)
        self.column_transformer.fit(X)
        X=self.column_transformer.transform(X)
        
        return X

    def fit_transform(self, X, y=None):
        X = self.age_binner.fit_transform(X)
        X = self.blood_pressure_splitter.fit_transform(X)
        return self.column_transformer.fit_transform(X, y)


class AgeBinner(TransformerMixin, BaseEstimator):
    """Custom transformer to bin the 'Age' column."""
    def fit(self, X, y=None):
        return self      
    
    def transform(self, X):
        X = X.copy()
        bins = [0, 20, 30, 40, 50, 60, 70]
        labels = ['<20', '21-30', '31-40', '41-50', '51-60', '61-70']
        X['Age Group'] = pd.cut(X['Age'], bins=bins, labels=labels, right=False)
        return X


class BloodPressureSplitter(TransformerMixin, BaseEstimator):
    """Custom transformer to split 'Blood Pressure' column into Systolic and Diastolic."""
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        # Split the 'Blood Pressure' column into Systolic and Diastolic
        bp_split = X['BloodPressure'].str.split('/', expand=True)
        X['Systolic'] = bp_split[0].astype(int)
        X['Diastolic'] = bp_split[1].astype(int)
        X.drop(columns=['BloodPressure'], inplace=True)
        return X


class LabelEncoderTransformer(BaseEstimator, TransformerMixin):
    """Applies Label Encoding to specific columns."""
    def __init__(self, columns):
        self.columns = columns
        self.label_encoders = {col: LabelEncoder() for col in columns}
    
    def fit(self, X, y=None):
        for col in self.columns:
            self.label_encoders[col].fit(X[col])
        return self
    
    def transform(self, X):
        X = X.copy()
        for col in self.columns:
            X[col] = self.label_encoders[col].transform(X[col])
        return X
