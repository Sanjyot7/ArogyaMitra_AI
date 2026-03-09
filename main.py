# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import uvicorn
import os

# Create the FastAPI app
app = FastAPI(title="ArogyaMitra API", description="AI-powered disease prediction and chatbot")

# ---------------------------------------------------------
# Global Variable for Model & Simple Symptom Memory
# ---------------------------------------------------------
# NOTE: Using global variables for model is fine, but for
# user_symptoms, it's ONLY good for a single-user demo.
# For production, use session/database storage.
model = None
user_symptoms = {
    "fever": 0,
    "cough": 0,
    "tiredness": 0,
    "headache": 0
}

# ---------------------------------------------------------
# Event Handlers: Load the Model on Startup
# ---------------------------------------------------------
@app.on_event("startup")
def load_model():
    """Load the machine learning model when the application starts."""
    global model
    model_path = "disease_model.pkl"
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            print(f"Model loaded successfully from '{model_path}'")
        except Exception as e:
            print(f"Error loading the model: {e}")
            model = None
    else:
        print(f"Error: Model file '{model_path}' not found. Please run 'train_model.py' first.")
        model = None

# ---------------------------------------------------------
# Pydantic Schemas for Data Validation
# ---------------------------------------------------------
class SymptomInput(BaseModel):
    fever: int      # 1 for Yes, 0 for No
    cough: int      # 1 for Yes, 0 for No
    tiredness: int  # 1 for Yes, 0 for No
    headache: int   # 1 for Yes, 0 for No

class ChatInput(BaseModel):
    message: str

# ---------------------------------------------------------
# Prediction Endpoint
# ---------------------------------------------------------
@app.post("/predict-disease", summary="Predict disease from symptoms")
def predict_disease(data: SymptomInput):
    """
    Directly predicts a disease based on a full set of symptom inputs.
    """
    if model is None:
        return {"error": "Model not loaded. Please ensure the model file exists and is accessible."}

    # Create a DataFrame from the input data, matching training columns
    df = pd.DataFrame([{
        "fever": data.fever,
        "cough": data.cough,
        "tiredness": data.tiredness,
        "headache": data.headache
    }])

    # Make a prediction
    prediction = model.predict(df)

    # Return the first (and only) prediction
    return {"predicted_disease": prediction[0]}

# ---------------------------------------------------------
# Chatbot Endpoint
# ---------------------------------------------------------
@app.post("/chat", summary="Chat with the medical bot")
def chat(data: ChatInput):
    """
    Iteratively collects symptoms from the user to provide a prediction.
    A simple demonstration with global state.
    """
    if model is None:
        return {"bot_reply": "I'm sorry, I cannot make predictions right now. Please try again later."}

    msg = data.message.strip().lower()

    # Special command to reset symptoms for a new test
    if msg in ["reset", "start over", "clear"]:
        global user_symptoms
        user_symptoms = {"fever": 0, "cough": 0, "tiredness": 0, "headache": 0}
        return {"bot_reply": "Hello! Please tell me your symptoms to begin."}

    # Capture symptoms sequentially and prompt for the next one
    if "fever" in msg:
        user_symptoms["fever"] = 1
        return {"bot_reply": "Do you also have a cough? (Yes/No)"}

    # Simplified checks for common confirmations
    if msg in ["yes", "yep", "yeah"]:
        # We need to infer what they said "yes" to. This is very fragile but
        # demonstrates the flow.
        if user_symptoms["fever"] == 1 and user_symptoms["cough"] == 0:
            user_symptoms["cough"] = 1
            return {"bot_reply": "Are you feeling tired?"}
        elif user_symptoms["tiredness"] == 0:
            user_symptoms["tiredness"] = 1
            return {"bot_reply": "Do you have a headache?"}
        elif user_symptoms["headache"] == 0:
            user_symptoms["headache"] = 1
            # After getting the last symptom, make the prediction
            df = pd.DataFrame([user_symptoms])
            prediction = model.predict(df)
            return {
                "bot_reply": f"Based on your symptoms, a possible disease is: {prediction[0]}"
            }

    # Provide an initial prompt if no symptoms have been detected
    return {"bot_reply": "Please tell me your symptoms (e.g., 'I have a fever')."}

# Main entry point to run the application with uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)