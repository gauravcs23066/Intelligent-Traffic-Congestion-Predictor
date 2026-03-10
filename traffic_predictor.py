import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

def generate_synthetic_data(num_samples=1000, random_seed=42):
    """Generates synthetic traffic time-series data."""
    np.random.seed(random_seed)
    
    # Features
    # Time of day (0 to 23 hours)
    hours = np.random.randint(0, 24, num_samples)
    
    # Volume (vehicles per hour) and Speed (km/h) based on time of day
    volume = np.zeros(num_samples)
    speed = np.zeros(num_samples)
    
    # Simulate peak hours (morning: 7-9, evening: 17-19)
    for i in range(num_samples):
        h = hours[i]
        if (7 <= h <= 9) or (17 <= h <= 19):
            # Rush hour
            volume[i] = np.random.normal(1500, 200)   # High volume
            speed[i] = np.random.normal(25, 10)       # Low speed
        elif (10 <= h <= 16):
            # Mid-day
            volume[i] = np.random.normal(800, 150)
            speed[i] = np.random.normal(50, 15)
        else:
            # Night/Early morning
            volume[i] = np.random.normal(200, 50)
            speed[i] = np.random.normal(80, 10)
            
    # Clip values to realistic ranges
    volume = np.clip(volume, 0, 2500)
    speed = np.clip(speed, 5, 120)
    
    data = pd.DataFrame({
        'hour': hours,
        'volume': volume,
        'speed': speed
    })
    
    return data

def assign_traffic_labels(data):
    """
    Labels: 
    0: Clear 
    1: Moderate 
    2: Congested
    """
    conditions = [
        (data['speed'] < 30) & (data['volume'] > 1200),
        (data['speed'] >= 30) & (data['speed'] < 60) & (data['volume'] >= 500) & (data['volume'] <= 1200),
        (data['speed'] >= 60) | (data['volume'] < 500)
    ]
    choices = [2, 1, 0]
    # Default to 1 (Moderate) if it doesn't strictly match the extremes perfectly
    data['state'] = np.select(conditions, choices, default=1)
    return data

def train_probabilistic_model(X, y):
    """Trains a Gaussian Naive Bayes Model."""
    model = GaussianNB()
    model.fit(X, y)
    return model

def trigger_alerts(probabilities, threshold=0.7):
    """
    Evaluates probabilities and triggers congestion alerts.
    Args:
        probabilities: Array of class probabilities from model.predict_proba
        threshold: Probability threshold above which an alert is triggered (0-1)
    """
    # Assuming class '2' is Congested (index 2 in probabilities if classes are 0,1,2)
    # Be careful: Naive Bayes might not output all classes if they aren't in the training set
    # but we will assume it does for our large synthetic dataset.
    congested_probs = probabilities[:, 2] 
    
    alerts = []
    for i, prob in enumerate(congested_probs):
        if prob > threshold:
            alerts.append({'index': i, 'probability': prob})
            
    return alerts

def main():
    print("--- Intelligent Traffic Congestion Predictor ---")
    
    # 1. Generate Data
    print("\n1. Generating Synthetic Traffic Data...")
    df = generate_synthetic_data(num_samples=2000)
    df = assign_traffic_labels(df)
    print(f"Dataset Shape: {df.shape}")
    print("Class Distribution (0:Clear, 1:Moderate, 2:Congested):")
    print(df['state'].value_counts().sort_index())
    
    # 2. Train Probabilistic reasoning model (Gaussian Naive Bayes)
    print("\n2. Training Probabilistic Reasoning Model (Gaussian Naive Bayes)...")
    X = df[['hour', 'volume', 'speed']]
    y = df['state']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = train_probabilistic_model(X_train, y_train)
    
    # 3. Predict and Evaluate
    print("\n3. Evaluating Model...")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # 4. Probabilistic Reasoning & Alerts
    print("\n4. Triggering Congestion Alerts on Test Data...")
    y_prob = model.predict_proba(X_test)
    
    ALERT_THRESHOLD = 0.85
    print(f"Alert Threshold set to: {ALERT_THRESHOLD*100}% probability of Congestion.")
    
    alerts = trigger_alerts(y_prob, threshold=ALERT_THRESHOLD)
    print(f"Total Congestion Alerts Triggered: {len(alerts)} out of {len(X_test)} simulated points")
    
    if len(alerts) > 0:
        print("\nSample Alerts (First 5):")
        for alert in alerts[:5]:
            idx = alert['index']
            prob = alert['probability']
            row = X_test.iloc[idx]
            print(f"  [ALERT!] High probability of Congestion: {prob:.2%} | Conditions: Hour={row['hour']}, Vol={row['volume']:.0f}, Speed={row['speed']:.1f} km/h")

    # Optional visualization
    try:
        plt.figure(figsize=(10, 6))
        
        # Scatter plot colored by predicted state (0, 1, 2)
        scatter = plt.scatter(X_test['volume'], X_test['speed'], c=y_pred, cmap='viridis', alpha=0.7)
        plt.xlabel('Volume (Vehicles/Hour)')
        plt.ylabel('Speed (km/h)')
        plt.title('Predicted Traffic State: Volume vs Speed')
        plt.colorbar(scatter, label='State (0:Clear, 1:Mod, 2:Cong)')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Save the plot
        plt.savefig('traffic_prediction_plot.png')
        print("\nSaved prediction visualization to 'traffic_prediction_plot.png'")
        
    except Exception as e:
        print(f"\nCould not generate plot due to: {e}")
        print("Install matplotlib to see visualizations.")

if __name__ == "__main__":
    main()
