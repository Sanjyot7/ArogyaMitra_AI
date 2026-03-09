# ArogyaMitra AI 🩺

ArogyaMitra is a FastAPI-based healthcare assistant that uses a Machine Learning (Decision Tree) model to predict potential diseases based on user symptoms.

## Features
- **Disease Prediction:** POST endpoint for direct symptom analysis.
- **Interactive Chatbot:** Step-by-step symptom collection via API.
- **SQLite Integration:** User management system.

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/arogyamitra-ai.git](https://github.com/your-username/arogyamitra-ai.git)
   cd arogyamitra-ai
2. Create a Virtual Environment
It is highly recommended to use a virtual environment to avoid conflicts with other Python packages.

Windows:

Bash
python -m venv venv
.\venv\Scripts\activate
macOS/Linux:

Bash
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Once the virtual environment is active, install the required libraries:

Bash
pip install -r requirements.txt
4. Initialize Data & Model
Before starting the server, you must set up the database and train the AI model:

Bash
python database.py
python train_model.py
5. Run the Application
Start the FastAPI server using Uvicorn:

Bash
python main.py
🚀 How to Use
Interactive Docs: Once the server is running, visit http://127.0.0.1:8000/docs.

Direct Prediction: Use the /predict-disease endpoint to send a JSON body of symptoms.

Chatbot: Use the /chat endpoint for a guided symptom conversation.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

⚠️ Disclaimer
This tool is for educational purposes only. It does not provide professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider.


---

### Important: Create the `requirements.txt` File
For the `pip install -r requirements.txt` command in your README to work, you **must** create a file named `requirements.txt` in your project folder with these lines:

```text
fastapi[all]
pandas
scikit-learn
joblib
