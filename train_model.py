import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import joblib

def generate_simple_data(num_samples=2000):
    print("Generating simple synthetic traffic data...")
    np.random.seed(42)
    hours = np.random.randint(0, 24, num_samples)
    volume = np.zeros(num_samples)
    speed = np.zeros(num_samples)
    
    for i in range(num_samples):
        h = hours[i]
        if (7 <= h <= 9) or (17 <= h <= 19): # Rush hour
            volume[i] = np.random.normal(2000, 300)
            speed[i] = np.random.normal(20, 10)
        else: # Normal hours
            volume[i] = np.random.normal(800, 200)
            speed[i] = np.random.normal(60, 15)
            
    volume = np.clip(volume, 0, 3000)
    speed = np.clip(speed, 5, 120)
    
    df = pd.DataFrame({'hour': hours, 'volume': volume, 'speed': speed})
    return df

def assign_labels(data):
    # Simple labels: 0: Clear, 1: Moderate, 2: Congested
    conditions = [
        (data['speed'] < 30) & (data['volume'] > 1500),
        (data['speed'] >= 30) & (data['speed'] < 60) & (data['volume'] >= 500),
        (data['speed'] >= 60) | (data['volume'] < 500)
    ]
    choices = [2, 1, 0]
    data['state'] = np.select(conditions, choices, default=1)
    return data

def train_and_save():
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    
    if os.path.exists(model_path):
        print("Model already exists. Skipping training.")
        return

    df = generate_simple_data()
    df = assign_labels(df)
    
    X = df[['hour', 'volume', 'speed']]
    y = df['state']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = GaussianNB()
    print("Training basic Naive Bayes model...")
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_and_save()
