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

---

## 🏗️ Tech Stack
- **Frontend/UI** → Streamlit  
- **Backend/ML** → Python, scikit-learn, pandas, numpy  
- **Auth & Email** → smtplib / streamlit-authenticator (if used)  
- **Visualization** → matplotlib, seaborn, plotly  

---

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

Screenshots

<img width="907" height="851" alt="Screenshot 2025-08-23 122532" src="https://github.com/user-attachments/assets/b4625b6d-c5fd-465e-930b-7af0b5a02644" />
<img width="1888" height="897" alt="Screenshot 2025-08-23 122423" src="https://github.com/user-attachments/assets/329bb006-6bd5-4672-b61c-68177509a8c7" />
<img width="1907" height="870" alt="Screenshot 2025-08-23 122741" src="https://github.com/user-attachments/assets/4a10bf4f-140c-4a44-b5a0-565f5e4c7f17" />
<img width="1912" height="871" alt="Screenshot 2025-08-23 122810" src="https://github.com/user-attachments/assets/e7358430-648d-4820-8a55-2ae96e3c474a" />











