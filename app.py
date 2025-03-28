
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Set up Streamlit page
st.set_page_config(page_title="🛡️ Threat Detection Dashboard", layout="centered")
st.title("🛡️ AI-Powered Threat Detection System")

# Sidebar navigation
st.sidebar.title("🔍 Navigation")
section = st.sidebar.radio("Go to", ["Upload & Detect", "Awareness Quiz", "About"])
role = st.sidebar.selectbox("🔐 Login as", ["Admin", "Analyst", "User"])

# Shared variables
data = None

# === SECTION: Upload & Detect ===
if section == "Upload & Detect":
    st.subheader("📁 Upload Logs")
    uploaded_file = st.file_uploader("Upload a CSV log file", type=["csv"])

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.success("Log file uploaded!")
        st.write("Preview of data:")
        st.dataframe(data.head())

        # Drop label column if exists
        if "Class" in data.columns:
            X = data.drop("Class", axis=1)
        else:
            X = data.copy()

        st.subheader("🚨 Run Threat Detection")
        if st.button("Detect Threats"):
            model = IsolationForest(n_estimators=100, contamination=0.002, random_state=42)
            model.fit(X)
            predictions = model.predict(X)
            predicted = [1 if x == -1 else 0 for x in predictions]

            data["Threat_Detected"] = predicted
            threat_count = sum(predicted)

            # Display metrics
            col1, col2 = st.columns(2)
            col1.metric("🚫 Threats Detected", threat_count)
            col2.metric("✅ Normal Logs", len(data) - threat_count)

            # Show updated table
            st.subheader("📊 Detection Results")
            st.dataframe(data.tail(10))

            # Chart
            fig, ax = plt.subplots()
            sns.countplot(x=predicted, ax=ax)
            ax.set_xticklabels(["Normal", "Threat"])
            ax.set_title("Detection Summary")
            st.pyplot(fig)

            # Download
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Report", csv, "incident_report.csv", "text/csv")

# === SECTION: Awareness Quiz ===
elif section == "Awareness Quiz":
    st.subheader("🧠 Cybersecurity Awareness Quiz")

    questions = [
        {
            "question": "What’s the best way to manage passwords?",
            "options": ["Use same password everywhere", "Sticky notes", "Password manager", "Share with coworkers"],
            "answer": "Password manager"
        },
        {
            "question": "Which of these is a sign of phishing?",
            "options": ["Secure domain", "Email from boss", "Unexpected attachment", "Good grammar"],
            "answer": "Unexpected attachment"
        },
        {
            "question": "What should you do if you suspect a breach?",
            "options": ["Ignore it", "Fix it yourself", "Report to IT", "Log out and pray"],
            "answer": "Report to IT"
        },
    ]

    score = 0
    for q in questions:
        user_answer = st.radio(q["question"], q["options"], key=q["question"])
        if user_answer == q["answer"]:
            st.success("✅ Correct")
            score += 1
        else:
            st.error(f"❌ Incorrect – Correct answer: {q['answer']}")

    if st.button("Submit Quiz"):
        st.markdown(f"### Your Score: {score} / {len(questions)}")
        if score >= 2:
            st.success("🎉 Training Passed – Well done!")
        else:
            st.warning("⚠️ Please review cybersecurity policies and retake the quiz.")

# === SECTION: About ===
elif section == "About":
    st.subheader("📘 About This System")
    st.markdown("""
This is a prototype AI-based Threat Detection and Incident Response System, built for academic and awareness purposes.  
It allows:
- Uploading of network/system logs
- AI-based anomaly detection using Isolation Forest
- Simulated incident response
- Role-based access views
- User awareness training via quiz
""")
    st.markdown("Made with ❤️ using Streamlit")

# Footer
st.markdown("---")
st.caption("📍 MSc Cybersecurity Project • Deployed with Streamlit Cloud")
