import sys
import os
import joblib
import pandas as pd
import json

def main():
    if len(sys.argv) != 4:
        print(json.dumps({"error": "Expected 3 arguments: hour, volume, speed"}))
        sys.exit(1)

    try:
        hour = float(sys.argv[1])
        volume = float(sys.argv[2])
        speed = float(sys.argv[3])
        
        model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
        if not os.path.exists(model_path):
            print(json.dumps({"error": "Model not found. Run train_model.py first."}))
            sys.exit(1)
            
        model = joblib.load(model_path)
        
        input_data = pd.DataFrame([{'hour': hour, 'volume': volume, 'speed': speed}])
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0].tolist()
        
        status_map = {0: "Clear", 1: "Moderate", 2: "Congested"}
        
        result = {
            "prediction": int(prediction),
            "status": status_map.get(int(prediction), "Unknown"),
            "probabilities": probabilities
        }
        
        print(json.dumps(result))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
