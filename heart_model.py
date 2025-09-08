import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

@st.cache_resource
def load_heart_model():
    df = pd.read_csv('./data/heart.csv')
    X = df.drop('target', axis=1)
    y = df['target']
    model = RandomForestClassifier()
    model.fit(X, y)
    return model, X.columns.tolist()

def heart_prediction():
    st.subheader("❤️ Heart Disease Prediction")

    try:
        model, features = load_heart_model()
    except FileNotFoundError as e:
        st.error(f"❌ Dataset not found! {e}")
        return

    st.markdown("### 🧾 Enter Patient Details Below:")
    user_data = {}
    for col in features:
        user_data[col] = st.number_input(f"{col}", step=1.0)

    if st.button("🔍 Predict Heart Disease"):
        input_df = pd.DataFrame([user_data])
        prediction = model.predict(input_df)[0]
        result = "✅ No Heart Disease" if prediction == 0 else "⚠️ At Risk of Heart Disease"
        st.success(f"**Prediction Result:** {result}")
