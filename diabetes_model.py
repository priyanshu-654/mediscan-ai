import streamlit as st
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

@st.cache_resource
def load_diabetes_model():
    df = pd.read_csv('data/diabetes.csv')
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    return model, X.columns.tolist()

def diabetes_prediction():
    st.subheader("🧪 Diabetes Prediction")
    model, features = load_diabetes_model()

    user_data = {}
    for col in features:
        user_data[col] = st.number_input(f"Enter {col}", value=0.0)

    if st.button("Predict Diabetes"):
        input_df = pd.DataFrame([user_data])
        prediction = model.predict(input_df)[0]
        result = "✅ Not Diabetic" if prediction == 0 else "⚠️ Diabetic"
        st.success(f"Prediction Result: {result}")