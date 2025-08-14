import streamlit as st
from utils import authenticate_user, save_feedback
from diabetes_model import diabetes_prediction
from heart_model import heart_prediction
from parkinson_model import parkinson_prediction
import time  # For delay before redirect

# Title
st.set_page_config(page_title="MediScan AI", layout="centered")
st.title("🧠 MediScan AI: Smart Disease Diagnosis App")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# ------------------------
# Login Form
# ------------------------
if not st.session_state["authenticated"]:
   with st.form("login_form"):
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    submit = st.form_submit_button("Login")  # ✅ Submit button inside the form

    if submit:
        if authenticate_user(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
        
            st.success("✅ Login Successful!")
        else:
            st.error("❌ Invalid credentials")



# ------------------------
# Main App after login
# ------------------------
if st.session_state["authenticated"]:
    st.sidebar.title("Choose Diagnosis")
    choice = st.sidebar.radio("Select an option", [
        "✅ Diabetes Prediction",
        "✅ Heart Disease Prediction",
        "✅ Parkinson’s Prediction",
        "📝 Submit Feedback"
    ])

    if choice == "✅ Diabetes Prediction":
        diabetes_prediction()
        

    elif choice == "✅ Heart Disease Prediction":
        heart_prediction()
        

    elif choice == "✅ Parkinson’s Prediction":
        parkinson_prediction()
        

    

    elif choice == "📝 Submit Feedback":
        st.subheader("💬 Feedback")
        feedback = st.text_area("Leave your feedback here...")

        if st.button("Submit Feedback"):
            if feedback.strip():
                save_feedback(st.session_state["username"], feedback)
                st.success("✅ Feedback submitted. Thank you!")

                # Delay to show success message
                time.sleep(2)

                # 🔒 Auto logout
                st.session_state["authenticated"] = False
                st.session_state["username"] = ""

                st.info("🔁 Redirecting to login page for next user...")
                time.sleep(1)
                st.rerun()  # Force app to show login form again
            else:
                st.warning("⚠️ Please enter your feedback before submitting.") 


