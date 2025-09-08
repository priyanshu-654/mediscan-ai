# MediScan AI: Smart Disease Diagnosis & Health Tracker App

MediScan AI is a **Streamlit-based web app** that predicts **Diabetes, Heart Disease, and Parkinson’s** using Machine Learning models.  
It also provides preventive suggestions, secure health report downloads, nearby doctor suggestions, and more — making it a smart health companion.

---

## ✨ Features
- 🔮 **ML Predictions**: Diabetes, Heart Disease, and Parkinson’s.
- 📊 **Data Analysis**: Feature importance & visualization.
- 📧 **Email Report Sending**: Health reports delivered to your inbox.
- 🔐 **Secure PDF Download**: Download your health report safely.
- 🗺️ **Nearby Doctor/Clinic Suggestions**: Location-based recommendations.
- 📝 **Feedback Section**: Users can share feedback to improve the app.
- 🔑 **User Authentication**: Simple login system for secure access.

## ✨ How It Works

Input: User enters health data or uploads sample data

Processing: App runs the right ML model (Diabetes / Heart / Parkinson’s)

Output: Displays prediction, charts, suggestions

Actions: User can download a PDF report or have it emailed

Extension: App may fetch nearby doctors using geolocation and allow feedback submission

---

## 🏗️ Tech Stack
- **Frontend/UI** → Streamlit  
- **Backend/ML** → Python, scikit-learn, pandas, numpy  
- **Auth & Email** → smtplib / streamlit-authenticator (if used)  
- **Visualization** → matplotlib, seaborn, plotly  

---

Screenshots
<img width="907" height="851" alt="Screenshot 2025-08-23 122532" src="https://github.com/user-attachments/assets/41f13fde-cb0b-4f86-9abb-3a85dadeba23" />
<img width="1888" height="897" alt="Screenshot 2025-08-23 122423" src="https://github.com/user-attachments/assets/6d59fa3d-f43d-44a8-a961-b632efb225de" />
<img width="1907" height="870" alt="Screenshot 2025-08-23 122741" src="https://github.com/user-attachments/assets/8d22114b-f5ec-4942-b9d0-2d50fc6ae465" />
<img width="1912" height="871" alt="Screenshot 2025-08-23 122810" src="https://github.com/user-attachments/assets/da9ecabd-3934-4cfe-88e0-ffca3c8834ef" />





## 🚀 Quick Start

### Clone the repo
```bash
git clone https://github.com/priyanshu-654/mediscan-ai.git
cd mediscan-ai

### Create a virtual environment
python -m venv .venv
# Activate:
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

### Install dependencies
pip install -r requirements.txt

[Run the app
streamlit run app.py
[🔗 Open MediScan App (local)](http://192.168.1.103:8501)
http://192.168.1.103:8501

---

## 📂 Project Structure
mediscan-ai/
│── app.py                  # Main Streamlit app
│── requirements.txt        # Python dependencies
│── README.md               # Documentation
│── LICENSE                 # License file
│
├── models/                 # ML models
├── data/                   # Datasets
├── utils/                  # Helper functions
├── assets/                 # Images, logos
└── reports/                # Generated reports

---
```

📂 Repository Structure

## app.py:
Main Flask application file.

## diabetes_model.py, heart_model.py, parkinson_model.py: 
Scripts containing the trained models for each disease prediction.

## pdf_generator.py: 
Script for generating PDF reports.

## requirements.txt: 
Lists the necessary Python packages.

## utils.py: 
Contains utility functions used across the application.

## data/: 
Directory for storing datasets.

## reports/: 
Directory for saving generated reports.

## feedback.txt: 
File to store user feedback.

## README.md: 
Documentation file with project details.

## 🧑‍💻 Author

## 🧑‍💻 Author

<a href="https://github.com/priyanshu-654" target="_blank" style="display: inline-block; background-color: #24292f; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; font-family: Arial, sans-serif;">
    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="20" style="vertical-align: middle; margin-right: 8px;" />
    Visit Priyanshu's GitHub
</a>









