import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

def train_and_save_model():
    # We are changing the 'labels' to be more medically accurate 
    # for isolated symptoms.
    data = {
        "fever":      [1, 1, 1, 0, 0, 0, 1, 1],
        "cough":      [1, 1, 0, 1, 0, 0, 0, 1],
        "tiredness":  [1, 0, 0, 0, 1, 0, 0, 1],
        "headache":   [0, 1, 0, 0, 1, 0, 0, 1],
        "disease": [
            "Flu",           # Fever + Cough
            "COVID-19",      # Fever + Cough + Headache
            "Viral Fever",   # JUST FEVER (Changed from Cold)
            "Mild Cold",     # Just Cough
            "Fatigue",       # Just Tiredness
            "Healthy",       # Nothing
            "Viral Fever",   # Just Fever (Repeat for weight)
            "COVID-19"       # All symptoms
        ]
    }

    df = pd.DataFrame(data)
    X = df[["fever", "cough", "tiredness", "headache"]]
    y = df["disease"]

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X, y)

    joblib.dump(model, "disease_model.pkl")
    print("Model updated: Fever alone will now predict 'Viral Fever'.")

if __name__ == "__main__":
    train_and_save_model()