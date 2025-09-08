import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

@st.cache_resource
def load_parkinson_model():
    df = pd.read_csv('./data/parkinson.csv')
    df = df.drop(['name'], axis=1)  # Drop 'name' if exists
    X = df.drop('status', axis=1)
    y = df['status']
    model = RandomForestClassifier()
    model.fit(X, y)
    return model, X.columns.tolist()

def parkinson_prediction():
    st.subheader("🧠 Parkinson’s Disease Prediction")

    try:
        model, features = load_parkinson_model()
    except FileNotFoundError as e:
        st.error(f"❌ Dataset not found! {e}")
        return

    st.markdown("### 🧾 Enter Patient Details Below:")
    user_data = {}
    for col in features:
        user_data[col] = st.number_input(f"{col}", step=0.1)

    if st.button("🔍 Predict Parkinson’s Disease"):
        input_df = pd.DataFrame([user_data])
        prediction = model.predict(input_df)[0]
        result = "✅ No Parkinson’s Disease" if prediction == 0 else "⚠️ At Risk of Parkinson’s Disease"
        st.success(f"**Prediction Result:** {result}")
