🛡️ Secure-Collab-Redactor

A Streamlit web app for writing and sharing reports with automatic privacy redaction.
Sensitive information (emails, phone numbers, API keys, etc.) is automatically detected and replaced with safe tokens before saving.

✨ Features
Submit text reports or upload log files.
Automatic detection & redaction of sensitive data.
Save reports as structured JSON for later review.

🚀 Getting Started
1. Clone the repo
        git clone https://github.com/MitraShabani/Secure-Collab-Redactor.git
        cd Secure-Collab-Redactor
2. Install dependencies
        pip install -r requirements.txt
3. Run the app
        streamlit run app.py

The app will open in your browser at http://localhost:8501.

🛠️ Tech Stack
Streamlit
Python Regex
JSON

📌 Example Use Case
A developer pastes error logs that include emails and API keys.
App detects and replaces sensitive data with [REDACTED].
Clean report is saved and can be safely shared.