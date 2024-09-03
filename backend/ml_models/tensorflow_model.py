import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pandas as pd

def train_tensorflow_model(data):
    X = data.drop('total_mass_co2_sequestered', axis=1)
    y = data['total_mass_co2_sequestered']

    model = Sequential([
        Dense(64, activation='relu', input_shape=(X.shape[1],)),
        Dense(64, activation='relu'),
        Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=50, batch_size=32)
    
    model.save('/app/ml_models/tensorflow_model.h5')
    
    return model.evaluate(X, y)

def predict_with_tensorflow_model(input_data):
    model = tf.keras.models.load_model('/app/ml_models/tensorflow_model.h5')
    return model.predict(input_data)
