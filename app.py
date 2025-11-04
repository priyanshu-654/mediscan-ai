# app.py (Enhanced Register + Login + Full Dashboard Input/Prediction)
import streamlit as st
import pandas as pd
import pickle
import os
import requests
from streamlit_lottie import st_lottie
from passlib.hash import pbkdf2_sha256
import json
import numpy as np

# ---------------- Load Lottie Animations ----------------
def load_lottie_local(path_relative):
    """Load a local Lottie JSON file from assets folder."""
    path = os.path.join(os.path.dirname(__file__), path_relative)
    if not os.path.exists(path):
        print(f"[Lottie] File not found: {path}")
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Lottie] Error loading {path}: {e}")
        return None


def load_lottie_url(url):
    """Load a Lottie animation from a given URL."""
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        return None


# Animation URLs
lottie_register_url = "https://assets10.lottiefiles.com/packages/lf20_ydo1amjm.json"
lottie_dashboard_url = "https://assets10.lottiefiles.com/packages/lf20_x62chJ.json"


# ---------------- Authentication Utils ----------------
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                content = f.read()
                if not content:
                    return {}
                return json.loads(content)
        except json.JSONDecodeError:
            return {}
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(username, password, email=None):
    username = username.strip().lower()
    if not username or not password:
        return False, "Username and password cannot be empty."
    if email and "@" not in email:
        return False, "Invalid email format."

    users = load_users()
    if username in users:
        return False, "User already exists. Click 'Login Now' below!"

    hashed = pbkdf2_sha256.hash(password)
    users[username] = {"password": hashed, "email": email}
    save_users(users)
    return True, "Registration successful! Please login."

def verify_user(username, password):
    username = username.strip().lower()
    users = load_users()
    if username not in users:
        return False, "User does not exist or incorrect password"
    if "password" not in users[username]:
        return False, "User data incomplete."
    if pbkdf2_sha256.verify(password, users[username]["password"]):
        return True, "Login successful"
    return False, "User does not exist or incorrect password"


# ---------------- Load ML Models ----------------
models_path = "models"

try:
    diabetes_model = pickle.load(open(os.path.join(models_path, "diabetes_model.pkl"), "rb"))
    heart_model = pickle.load(open(os.path.join(models_path, "heart_model.pkl"), "rb"))
    parkinsons_model = pickle.load(open(os.path.join(models_path, "parkinson_model.pkl"), "rb"))
except FileNotFoundError as e:
    st.error(f"Model file not found: {e}. Please ensure models exist.")
    st.stop()
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()


# ---------------- Streamlit Settings ----------------
st.set_page_config(page_title="MediScan AI", layout="centered")

if "view" not in st.session_state:
    st.session_state.view = "register"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""


# ---------------- REGISTER PAGE ----------------
if st.session_state.view == "register":
    st.markdown("""
        <style>
        .stApp { background-color: #2a7cf7; }
        h1 { text-align: center; color: white; margin-bottom: 1rem; }
        .register-card {
            background-color: white; padding: 2rem; border-radius: 20px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
            width: 420px; margin: 1rem auto; text-align: center; color: #333;
        }
        .stButton>button {
            background-color: #00c851; color: white; border: none;
            padding: 10px 40px; border-radius: 10px;
            font-size: 1rem; cursor: pointer; transition: 0.3s;
            width: 100%; margin-top: 1rem;
        }
        .stButton>button:hover { background-color: #009e3c; }
        .switch-link {
            margin-top: 1.5rem; font-size: 0.9rem; color: #555;
        }
        .switch-link span {
            color: #007bff; cursor: pointer; text-decoration: underline;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>Mediscan AI App</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        lottie = load_lottie_local("assets/doctor.json") or load_lottie_url(lottie_register_url)
        if lottie:
            st_lottie(lottie, height=450, key="register_anim", loop=True)
        else:
            st.warning("Doctor animation not found.")

    with col2:
        st.markdown("<div class='register-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Register Now</h3>", unsafe_allow_html=True)
        reg_email = st.text_input("Email")
        reg_password = st.text_input("Password", type="password")
        if st.button("Register Account"):
            if reg_email and reg_password:
                ok, msg = register_user(reg_email, reg_password, reg_email)
                st.info(msg)
                if ok:
                    st.session_state.view = "login"
                    st.rerun()
            else:
                st.error("Please fill all fields!")

        st.markdown("<div class='switch-link'>Already have an account? <span id='login-link'>Login here</span></div>", unsafe_allow_html=True)
        if st.button("Go to Login", key="hidden_login"):
            st.session_state.view = "login"
            st.rerun()


# ---------------- LOGIN PAGE ----------------
elif st.session_state.view == "login":
    st.markdown("""
        <style>
        .stApp { background-color: #2a7cf7; }
        h1 { text-align: center; color: white; margin-bottom: 1rem; }
        .login-card {
            background-color: white; padding: 2rem; border-radius: 20px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
            width: 420px; margin: 1rem auto; text-align: center; color: #333;
        }
        .stButton>button {
            background-color: #00c851; color: white; border: none;
            padding: 10px 40px; border-radius: 10px;
            font-size: 1rem; cursor: pointer; transition: 0.3s;
            width: 100%; margin-top: 1rem;
        }
        .stButton>button:hover { background-color: #009e3c; }
        .switch-link {
            margin-top: 1.5rem; font-size: 0.9rem; color: #555;
        }
        .switch-link span {
            color: #007bff; cursor: pointer; text-decoration: underline;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>Mediscan AI App</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        lottie = load_lottie_local("assets/doctor.json") or load_lottie_url(lottie_register_url)
        if lottie:
            st_lottie(lottie, height=450, key="login_anim", loop=True)
        else:
            st.warning("Doctor animation not found.")

    with col2:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Login to MediScan AI</h3>", unsafe_allow_html=True)
        login_email = st.text_input("Email")
        login_password = st.text_input("Password", type="password")
        if st.button("Login"):
            ok, msg = verify_user(login_email, login_password)
            st.info(msg)
            if ok:
                st.session_state.logged_in = True
                st.session_state.username = login_email
                st.session_state.view = "dashboard"
                st.rerun()

        st.markdown("<div class='switch-link'>Don't have an account? <span id='register-link'>Register here</span></div>", unsafe_allow_html=True)
        if st.button("Go to Register", key="hidden_register"):
            st.session_state.view = "register"
            st.rerun()


# ---------------- DASHBOARD PAGE ----------------
# --- VIEW 3: DASHBOARD PAGE (Only if logged_in is True) ---
elif st.session_state.view == "dashboard" and st.session_state.logged_in:
    st.set_page_config(layout="wide") # Switch to wide layout for dashboard

    st.sidebar.title(f"Welcome, {st.session_state.username}!")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.view = "login" # Go back to login on logout
        st.rerun() # Rerun to show login page

    st.sidebar.header("Select Disease Prediction")
    # Use keys without emojis for easier dictionary lookup
    disease_options_display = ["Diabetes 🩸", "Heart Disease ❤️", "Parkinson's 🧠"]
    disease_options_keys = ["Diabetes", "Heart Disease", "Parkinson's"]
    disease_choice_display = st.sidebar.radio("Choose a disease:", disease_options_display, key="disease_choice_dash_v2")
    # Find the corresponding key
    selected_model_key = disease_choice_display.split(" ")[0].lower() # Gets 'diabetes', 'heart', 'parkinson'


    # --- Dashboard Title and Animation ---
    st.title("🩺 MediScan AI Dashboard") # Keep this title for the dashboard
    lottie_dash_json = load_lottie_url(lottie_dashboard_url)
    if lottie_dash_json:
        st_lottie(lottie_dash_json, height=150, key="dash_anim_v2")
    st.markdown("---") # Separator


    # --- Helper function to display results in styled card ---
    def display_result_card(prediction, positive_msg, negative_msg, confidence_score=""):
        if prediction == 1: # High Risk / Positive
            result_text = positive_msg
            color = "#FF4B4B"; background_color = "#FFE0E0"; border_color = "#FF4B4B"; icon = "⚠️"
        else: # Low Risk / Negative
            result_text = negative_msg
            color = "#28A745"; background_color = "#E0FFE0"; border_color = "#28A745"; icon = "✅"

        st.markdown(f"""
            <div style="border: 2px solid {border_color}; background-color: {background_color};
                        border-radius: 10px; padding: 1.5rem; text-align: center; margin-top: 1rem;">
                <h4 style="color: #333; margin-bottom: 0.5rem; font-weight: bold;">Prediction Result</h4>
                <p style="color: {color}; font-size: 2rem; font-weight: bold; margin-bottom: 0.25rem;">
                    {icon} {result_text}
                </p>
                <p style="color: #555; font-size: 0.9rem; margin: 0;">
                    Confidence: {confidence_score}
                </p>
            </div>
            """, unsafe_allow_html=True)

    # --- Helper function to make predictions using models, scalers, imputers ---
    def make_prediction(model_key, input_data_dict):
        try:
            assets = model[model_key] # Use passed dictionary # Use the global 'models' dictionary
            model = assets['model']
            scaler = assets['scaler']
            imputer = assets['imputer']

            input_df = pd.DataFrame([input_data_dict])
            required_features = imputer.feature_names_in_

            # Handle categorical columns (get_dummies) - Important for Heart Disease
            categorical_cols_def = {"heart": ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']}
            categorical_cols_present = [col for col in categorical_cols_def.get(model_key, []) if col in input_df.columns]
            for col in categorical_cols_present: input_df[col] = input_df[col].astype(str) # Ensure type consistency

            input_df = pd.get_dummies(input_df, columns=categorical_cols_present, drop_first=True)
            input_df = input_df.reindex(columns=required_features, fill_value=0) # Ensure all training columns are present

            # Force numeric for safety after potential get_dummies
            for col in input_df.columns:
                input_df[col] = pd.to_numeric(input_df[col], errors='coerce')

            input_imputed = imputer.transform(input_df)
            input_scaled = scaler.transform(input_imputed)

            prediction = model.predict(input_scaled)[0]
            probability = model.predict_proba(input_scaled)[0][prediction] * 100

            return prediction, f"{probability:.2f}%"

        except Exception as e:
            st.error(f"Prediction Error: {e}")
            # import traceback # Uncomment for detailed debugging
            # st.error(traceback.format_exc()) # Uncomment for detailed debugging
            return None, None


    # --- Display selected disease form ---
    st.header(f"{disease_choice_display} Prediction Input") # Use display name

    # Load reference data (only needed for default values/ranges now)
    try:
        data_file_map = {"diabetes": "diabetes.csv", "heart": "heart.csv", "parkinson": "parkinson.csv"}
        df_ref = pd.read_csv(os.path.join("data", data_file_map[selected_model_key]))

        target_col_map = {"diabetes": "Outcome", "heart": "target", "parkinson": "status"}
        target_col = target_col_map[selected_model_key]

        drop_cols = [target_col]
        if selected_model_key == 'parkinson' and 'name' in df_ref.columns: drop_cols.append('name')

        categorical_features_map = {"diabetes": [], "heart": ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal'], "parkinson": []}
        categorical_features = categorical_features_map[selected_model_key]

        col_count = 3 if selected_model_key != 'parkinson' else 4
        feature_names = df_ref.drop(columns=drop_cols).columns

    except Exception as e:
        st.error(f"Error loading data configuration: {e}")
        st.stop()


    # Create the form for input
    with st.form(f"{selected_model_key}_form_v2"): # Unique key
        input_data = {}
        cols = st.columns(col_count)

        for i, col_name in enumerate(feature_names):
            with cols[i % col_count]:
                 if col_name in categorical_features:
                      options = sorted(df_ref[col_name].unique())
                      # Ensure default_val is compatible type for index lookup
                      default_val_raw = df_ref[col_name].mode()[0] if not df_ref[col_name].mode().empty else options[0]
                      default_val = type(options[0])(default_val_raw) # Convert mode to option type
                      default_index = 0
                      try: default_index = options.index(default_val)
                      except ValueError: pass # Keep index 0 if conversion/find fails
                      input_data[col_name] = st.selectbox(
                          label=col_name, options=options, index=default_index,
                          key=f"{selected_model_key}_{col_name}_v2"
                          )
                 else: # Numerical input
                      # Define min/max/mean, handling potential NaNs
                      min_val=float(df_ref[col_name].min()) if pd.notna(df_ref[col_name].min()) else 0.0
                      max_val=float(df_ref[col_name].max()) if pd.notna(df_ref[col_name].max()) else 1000.0
                      mean_val=float(df_ref[col_name].mean()) if pd.notna(df_ref[col_name].mean()) else 0.0
                      # Ensure default value is within bounds
                      value = mean_val if pd.notna(mean_val) else 0.0
                      value = max(min_val, min(max_val, value))

                      input_data[col_name] = st.number_input(
                          label=col_name, min_value=min_val, max_value=max_val, value=value,
                          # Apply specific formatting only for non-integer float columns
                          format="%.5f" if df_ref[col_name].dtype == 'float64' and col_name not in ['Age', 'Pregnancies'] else None,
                          key=f"{selected_model_key}_{col_name}_v2"
                          )

        submit = st.form_submit_button(f"Predict {disease_choice_display.split(' ')[0]} Risk")
        if submit:
            # Call the CORRECT prediction helper
            prediction, confidence = make_prediction(selected_model_key, input_data)

            if prediction is not None:
                 st.markdown("### Prediction Result")
                 # Use the new display_result_card function
                 if selected_model_key == 'diabetes':
                     display_result_card(prediction, "High Risk", "Low Risk", confidence_score=confidence)
                 elif selected_model_key == 'heart':
                      display_result_card(prediction, "Risk Detected", "Appears Healthy", confidence_score=confidence)
                 elif selected_model_key == 'parkinson':
                      display_result_card(prediction, "Indicators Found", "No Indicators Found", confidence_score=confidence)

# Fallback view logic (if session state gets corrupted)
elif not st.session_state.logged_in:
    st.session_state.view = "login" # Go back to login if logged out but somehow stuck in dashboard view
    st.rerun()

# Close wrapper div
st.markdown("</div>", unsafe_allow_html=True)