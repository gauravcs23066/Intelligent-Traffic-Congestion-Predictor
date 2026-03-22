import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

class TrafficDataHandler:
    def __init__(self, dataset_name="hasnainjaved/traffic-prediction-dataset", fallback_samples=5000):
        self.dataset_name = dataset_name
        self.fallback_samples = fallback_samples
        
    def fetch_data(self):
        # Attempt to use Kaggle API
        kaggle_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(kaggle_dir, exist_ok=True)
        try:
            import kaggle
            print("Attempting to download Kaggle dataset...")
            kaggle.api.authenticate()
            kaggle.api.dataset_download_files(self.dataset_name, path=kaggle_dir, unzip=True)
            # Find the csv file
            for file in os.listdir(kaggle_dir):
                if file.endswith('.csv'):
                    df = pd.read_csv(os.path.join(kaggle_dir, file))
                    return self._process_kaggle_data(df)
            print("No CSV found in Kaggle dataset.")
        except BaseException as e:
            print(f"Kaggle download failed or unauthorized: {e}. Falling back to advanced synthetic data.")
            
        return self._generate_synthetic_data(self.fallback_samples)

    def _process_kaggle_data(self, df):
        print("Processing Kaggle Data...")
        if 'Vehicles' in df.columns and 'DateTime' in df.columns:
            df['hour'] = pd.to_datetime(df['DateTime']).dt.hour
            df['volume'] = df['Vehicles'] * 10  # Scale up for realism
            df['speed'] = np.clip(100 - (df['volume'] / 50), 10, 100) # Simple inverse relation
            return df[['hour', 'volume', 'speed']]
        else:
            print("Unrecognized Kaggle data structure. Using synthetic.")
            return self._generate_synthetic_data(self.fallback_samples)

    def _generate_synthetic_data(self, num_samples):
        print("Generating advanced synthetic time-series data...")
        np.random.seed(42)
        hours = np.random.randint(0, 24, num_samples)
        volume = np.zeros(num_samples)
        speed = np.zeros(num_samples)
        
        for i in range(num_samples):
            h = hours[i]
            if (7 <= h <= 9) or (17 <= h <= 19):
                # Rush hour
                volume[i] = np.random.normal(1800, 300)
                speed[i] = np.random.normal(20, 8)
            elif (10 <= h <= 16):
                # Mid-day
                volume[i] = np.random.normal(900, 200)
                speed[i] = np.random.normal(45, 12)
            else:
                # Night/Early morning
                volume[i] = np.random.normal(300, 100)
                speed[i] = np.random.normal(75, 15)
                
        volume = np.clip(volume, 0, 3000)
        speed = np.clip(speed, 5, 120)
        
        df = pd.DataFrame({'hour': hours, 'volume': volume, 'speed': speed})
        
        # Add some complex non-linear noise
        df['volume'] += np.sin(df['hour'] * np.pi / 12) * 200
        df['speed'] -= np.cos(df['hour'] * np.pi / 12) * 10
        
        return df

    def assign_traffic_labels(self, data):
        # 0: Clear, 1: Moderate, 2: Congested, 3: Gridlock (New severe class)
        conditions = [
            (data['speed'] < 15) & (data['volume'] > 2000),
            (data['speed'] < 30) & (data['volume'] > 1200),
            (data['speed'] >= 30) & (data['speed'] < 60) & (data['volume'] >= 500),
            (data['speed'] >= 60) | (data['volume'] < 500)
        ]
        choices = [3, 2, 1, 0]
        data['state'] = np.select(conditions, choices, default=1)
        return data

class TrafficModel:
    def __init__(self, model_path="model.joblib"):
        # Put the model relative to this file
        self.model_path = os.path.join(os.path.dirname(__file__), model_path)
        self.model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        self.is_trained = False
        
    def train(self, X, y):
        print("Training Random Forest Classifier...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"Model Accuracy: {acc:.4f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        
        joblib.dump(self.model, self.model_path)
        self.is_trained = True
        print(f"Model saved to {self.model_path}")
        
    def load(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_trained = True
            print("Model loaded from disk.")
        else:
            print("Model not found on disk. Needs training.")
            
    def predict(self, features):
        if not self.is_trained:
            raise ValueError("Model is not trained yet.")
        probabilities = self.model.predict_proba(features)
        predictions = self.model.predict(features)
        return predictions, probabilities

if __name__ == "__main__":
    handler = TrafficDataHandler()
    df = handler.fetch_data()
    df = handler.assign_traffic_labels(df)
    
    X = df[['hour', 'volume', 'speed']]
    y = df['state']
    
    model = TrafficModel()
    model.train(X, y)
