import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pickle

def train_sklearn_model(data):
    X = data.drop('total_mass_co2_sequestered', axis=1)
    y = data['total_mass_co2_sequestered']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    
    with open('/app/ml_models/sklearn_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    return mse

def predict_with_sklearn_model(input_data):
    with open('/app/ml_models/sklearn_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    return model.predict(input_data)
