import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
# from sklearn.ensemble import RandomForestClassifier # Keep if needed for other models
from sklearn.preprocessing import StandardScaler, LabelEncoder # LabelEncoder might not be needed now
from sklearn.impute import SimpleImputer
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

def train_and_save_model(df, target_column, model_filename, drop_cols=None, categorical_cols=None, target_map=None):
    """
    A comprehensive function to preprocess, train, and save a model, scaler, and imputer.
    """
    print(f"--- Training {model_filename} ---")
    try:
        models_path = "models" # Ensure saving to the models folder
        if not os.path.exists(models_path):
             os.makedirs(models_path)

        # Drop unnecessary columns
        if drop_cols:
            df = df.drop(columns=drop_cols, errors='ignore')

        # Handle target column mapping
        if target_map:
            df[target_column] = df[target_column].map(target_map)

        # Separate features (X) and target (y)
        X = df.drop(columns=[target_column])
        y = df[target_column].values

        # --- Preprocessing X ---

        # 1. Handle categorical columns with pd.get_dummies
        if categorical_cols:
            for col in categorical_cols:
                if col in X.columns:
                    X[col] = X[col].astype(str)
            X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

        # 2. Force remaining non-numeric columns to numeric
        numeric_cols = X.select_dtypes(include='number').columns
        non_numeric_cols = X.select_dtypes(exclude='number').columns
        for col in non_numeric_cols:
             X[col] = pd.to_numeric(X[col], errors='coerce')
        # Ensure all columns intended to be numeric are included
        X = X.astype(float)


        # 3. Impute missing values (NaN)
        imputer = SimpleImputer(strategy='mean')
        X_imputed = imputer.fit_transform(X)
        imputer.feature_names_in_ = X.columns # Store column names

        # 4. Scale the data
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_imputed)
        scaler.feature_names_in_ = X.columns # Store column names


        # --- Model Training ---
        model = LogisticRegression(max_iter=1000)
        model.fit(X_scaled, y)
        try:
             model.feature_names_in_ = X.columns
        except AttributeError:
             pass


        # --- Saving Artifacts ---
        model_save_path = os.path.join(models_path, model_filename)
        with open(model_save_path, 'wb') as f:
            pickle.dump(model, f)

        scaler_filename = model_filename.replace('.pkl', '_scaler.pkl')
        scaler_save_path = os.path.join(models_path, scaler_filename)
        with open(scaler_save_path, 'wb') as f:
            pickle.dump(scaler, f)

        imputer_filename = model_filename.replace('.pkl', '_imputer.pkl')
        imputer_save_path = os.path.join(models_path, imputer_filename)
        with open(imputer_save_path, 'wb') as f:
            pickle.dump(imputer, f)

        print(f"✅ {model_filename}, scaler, and imputer saved successfully.")
        return True

    except Exception as e:
        print(f"❌ Error training {model_filename}: {e}")
        import traceback
        traceback.print_exc()
        return False


# --- Main Training Execution ---
if __file__ == "_main_":
    # Ensure data folder exists
    if not os.path.exists('data'):
        print("❌ Error: 'data' folder not found. Please create it and add CSV files.")
    else:
        all_successful = True # Flag to track if all trainings worked

        # --- 1. Diabetes ---
        try:
            df_diabetes = pd.read_csv('data/diabetes.csv')
            if not train_and_save_model(df_diabetes, 'Outcome', 'diabetes_model.pkl'):
                all_successful = False
        except FileNotFoundError:
            print("❌ Error: data/diabetes.csv not found.")
            all_successful = False
        except Exception as e:
            print(f"❌ Error processing diabetes: {e}")
            all_successful = False


        # --- 2. Heart Disease ---
        try:
            df_heart = pd.read_csv('data/heart.csv')
            # Assuming 'target' is the correct column name based on previous steps
            if not train_and_save_model(df_heart, 'target', 'heart_model.pkl'):
                 all_successful = False
        except FileNotFoundError:
             print("❌ Error: data/heart.csv not found.")
             all_successful = False
        except Exception as e:
            print(f"❌ Error processing heart: {e}")
            all_successful = False

        # --- 3. Parkinson's Disease ---
        # ** THIS CALL WAS MISSING BEFORE **
        try:
            df_parkinsons = pd.read_csv('data/parkinson.csv') # Make sure filename matches
            # Assuming 'status' is target, drop 'name' if exists
            drop_cols = ['name'] if 'name' in df_parkinsons.columns else None
            if not train_and_save_model(df_parkinsons, 'status', 'parkinson_model.pkl', drop_cols=drop_cols):
                 all_successful = False
        except FileNotFoundError:
             print("❌ Error: data/parkinson.csv not found.") # Check filename
             all_successful = False
        except Exception as e:
            print(f"❌ Error processing parkinson's: {e}")
            all_successful = False

        # --- Final Summary ---
        print("\n--- Training complete ---")
        if all_successful:
            print("✅ All requested models, scalers, and imputers appear to have been saved.")
        else:
             print("⚠ Some models failed to train or save. Please check errors above.")

        # Verify files were created
        print("Checking created files in 'models' folder:")
        if os.path.exists('models'):
            print(os.listdir('models'))
        else:
            print("'models' folder not found.")
