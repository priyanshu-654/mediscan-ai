import os

# Simple login dictionary
user_credentials = {
    "user1": "pass123",
    "admin": "admin123",
    "demo": "demo123"
}

# -----------------------
# Authenticate function
# -----------------------
def authenticate_user(username, password):
    if username in user_credentials and user_credentials[username] == password:
        return True
    return False

# -----------------------
# Save feedback function
# -----------------------
def save_feedback(username, feedback):
    feedback_dir = "reports/user_reports"
    os.makedirs(feedback_dir, exist_ok=True)
    with open(os.path.join(feedback_dir, f"{username}_feedback.txt"), "a") as f:
        f.write(feedback + "\n---\n")
