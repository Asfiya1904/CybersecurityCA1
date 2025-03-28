
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="🔐 Threat Detector AI", layout="wide")

# Header with icon and subtitle
st.markdown("""
<style>
    .main-title {
        font-size: 2.5em;
        font-weight: bold;
        color: #2c3e50;
    }
    .sub-title {
        font-size: 1.2em;
        color: #7f8c8d;
    }
    .metric-box {
        padding: 10px;
        background-color: #f5f5f5;
        border-radius: 10px;
        text-align: center;
    }
    .block-container {
        padding-top: 1rem;
    }
</style>
<div class='main-title'>🛡️ AI-Powered Threat Detection Dashboard</div>
<div class='sub-title'>Upload data from any domain (finance, systems, logs) and detect anomalies in real-time.</div>
<br>
""", unsafe_allow_html=True)

# Sidebar nav
st.sidebar.image("https://img.icons8.com/external-flat-icons-inmotus-design/67/null/external-cyber-security-security-flat-icons-inmotus-design.png", width=60)
st.sidebar.title("🔍 Navigation")
section = st.sidebar.radio("Jump to:", ["📂 Upload & Detect", "🧠 Awareness Quiz", "ℹ️ About"])
role = st.sidebar.selectbox("🔐 Logged in as", ["Admin", "Analyst", "User"])

# === Section 1: Upload & Detect
if section == "📂 Upload & Detect":
    st.subheader("📁 Upload Your Dataset")
    uploaded_file = st.file_uploader("Supported format: CSV only", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ File uploaded successfully!")
            st.dataframe(df.head(), use_container_width=True)

            # Filter numerical columns
            numeric_df = df.select_dtypes(include=[np.number])
            if numeric_df.empty:
                st.warning("⚠️ No numeric features found. Please upload a dataset with numeric values.")
            else:
                st.info(f"🧠 Using {numeric_df.shape[1]} numeric features: {list(numeric_df.columns)}")
                X = numeric_df.fillna(0)

                if st.button("🚨 Run Threat Detection"):
                    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
                    model.fit(X)
                    predictions = model.predict(X)
                    df["Threat_Detected"] = [1 if p == -1 else 0 for p in predictions]

                    # Display metrics
                    threat_count = df["Threat_Detected"].sum()
                    normal_count = len(df) - threat_count

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("🚫 Threats", threat_count)
                    with col2:
                        st.metric("✅ Normal", normal_count)

                    st.subheader("📊 Detection Chart")
                    fig, ax = plt.subplots()
                    sns.countplot(x=df["Threat_Detected"], ax=ax)
                    ax.set_xticklabels(["Normal", "Threat"])
                    ax.set_title("Threat vs Normal Distribution")
                    st.pyplot(fig)

                    st.subheader("📥 Download Results")
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("⬇️ Download CSV", csv, file_name="detection_results.csv", mime="text/csv")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# === Section 2: Awareness Quiz
elif section == "🧠 Awareness Quiz":
    st.subheader("🧠 Cybersecurity Awareness Quiz")
    questions = [
        {"question": "Best way to store passwords?", "options": ["Notebook", "Sticky Notes", "Password Manager", "Same password everywhere"], "answer": "Password Manager"},
        {"question": "Sign of phishing email?", "options": ["Unexpected attachment", "Hi from boss", "Secure domain", "Perfect grammar"], "answer": "Unexpected attachment"},
        {"question": "What to do after a breach?", "options": ["Ignore it", "Fix it alone", "Report to IT", "Log out"], "answer": "Report to IT"}
    ]

    score = 0
    for q in questions:
        ans = st.radio(q["question"], q["options"], key=q["question"])
        if ans == q["answer"]:
            st.success("✅ Correct!")
            score += 1
        else:
            st.error(f"❌ Incorrect. Correct: {q['answer']}")

    if st.button("Submit Quiz"):
        st.markdown(f"### 🧾 Your Score: `{score}/{len(questions)}`")
        if score >= 2:
            st.success("🎉 Passed! You are cybersecurity aware.")
        else:
            st.warning("⚠️ Review the policies and try again.")

# === Section 3: About
elif section == "ℹ️ About":
    st.subheader("📘 About This Project")
    st.markdown("""
This web app uses machine learning to detect anomalies in any CSV-based dataset, whether from:
- 💳 Financial records
- 💻 System activity logs
- 📈 Transaction summaries

Built with:
- 🧠 **Isolation Forest** for anomaly detection
- 🎨 **Streamlit** for the web interface
- 📊 **Seaborn** and **Matplotlib** for visual output

This system is designed for non-technical users to quickly detect threats and download results, while also learning cybersecurity basics.
""")
    st.markdown("Made with ❤️ for MSc Cybersecurity")

st.markdown("---")
st.caption("Deployed with Streamlit • By Asfiya")
