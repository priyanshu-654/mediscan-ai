import streamlit as st
from utils import authenticate_user, save_feedback
from diabetes_model import diabetes_prediction
from heart_model import heart_prediction
from parkinson_model import parkinson_prediction
import time  # For delay before redirect
import webbrowser
import urllib.parse

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
        "🗺️ Nearby Help",
        "📝 Submit Feedback"
    ])

    if choice == "✅ Diabetes Prediction":
        diabetes_prediction()

    elif choice == "✅ Heart Disease Prediction":
        heart_prediction()

    elif choice == "✅ Parkinson’s Prediction":
        parkinson_prediction()

    # ------------------------
    # Nearby Help Section
    # ------------------------
    elif choice == "🗺️ Nearby Help":
        st.subheader("Find Nearby Help 🏥")

        # Added "Hospitals" here
        search_choice = st.selectbox(
            "What do you want to search?",
            ["Doctors", "Clinics", "Hospitals", "Medical Stores"]
        )
        location = st.text_input("Optional: enter a city or address (leave blank for 'near me')")

        # Build search query
        if location.strip():
            query_text = f"{search_choice} near {location.strip()}"
        else:
            query_text = f"{search_choice} near me"

        encoded_query = urllib.parse.quote_plus(query_text)
        google_maps_url = f"https://www.google.com/maps/search/{encoded_query}"

        # Button (local open)
        if st.button("Open Google Maps (local)"):
            try:
                opened = webbrowser.open(google_maps_url)
                if opened:
                    st.success("Opening Google Maps in your browser...")
                else:
                    st.info("Could not open browser automatically. Use the link below ⬇️")
            except Exception:
                st.error("Browser opening not supported on this server. Use the link below ⬇️")

        # Always show link (works everywhere, including Streamlit Cloud)
        st.markdown(
            f'<a href="{google_maps_url}" target="_blank" rel="noopener noreferrer">'
            "➡️ Open Google Maps in a new tab</a>",
            unsafe_allow_html=True
        )

    # ------------------------
    # Feedback Section
    # ------------------------
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

        # Optional: show the actual URL for debugging
        st.caption(google_maps_url)


