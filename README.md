# HR Assistant Application

This project is an **Agentic AI-powered HR Assistant** that automates HR onboarding workflows.  
It integrates **DataRobot predictive modeling, Azure OpenAI GPT-4o, CrewAI agents, and SendGrid** to provide a complete HR automation system.

- Document link - https://docs.google.com/document/d/1ilwBKPlnHCCku3SYqvcc574E9l27lF-BHWuC57jDKhE/edit?tab=t.wsseyd30gkh1


# The Problem
In most companies,HR teams spend a lot of time in manual effort
- Sending onboarding emails
- tracking employee risk
- collecting feedback
- and answering repetitive questions about company policies
This leads to wasted time and delays in employee engagement

---

## The Solution
- **Onboarding Automation**  
  - Sends personalized onboarding emails to new joiners.  
- **Churn Prediction**  
  - Uses a **DataRobot classification model** to predict employee churn risk.  
  - Alerts HR about **high-risk joiners**.  
- **Feedback Collection**  
  - Sends feedback request emails after joiners complete days in the company.  
  - Notifies HR when new feedback is submitted.  
- **RAG Chatbot**  
  - A Streamlit-based chatbot (`rag_chatbot_app.py`) for new joiners to ask onboarding-related questions.  
- **Agentic AI**  
  - Built with **CrewAI**, combining multiple agents:
    - HR Agent → onboarding emails.  
    - Alert Agent → high-risk alerts.  
    - Feedback Agent → feedback requests + notifications.  

---


## 📂 Project Structure
```
Capstone-HR-Assistant/
│── main.py                  # -----------------------------Orchestrator – runs agents and workflow
│── rag_chatbot_app.py       # ------------------------------RAG-powered chatbot (Streamlit)
│── requirements.txt         # ------------------------------Dependencies
│── .env.example             # -------------------------------Example environment variables
│
│── agents/                  # --------------------------------CrewAI agents
│   ├── hr_agent.py          # --------------------------------HR Agent (onboarding emails)
│   ├── alert_agent.py       # ---------------------------------Alert Agent (HR risk alerts)
│   ├── feedback_agent.py    # ---------------------------------Feedback Agent (feedback collection in google form)
│
│── utils/                   
│   ├── churn_predictor.py   # ---------------------------------Calls DataRobot predictive model to predict churn of new employees
│   ├── emailer.py           # --------------------------------- Handles SendGrid email delivery
│
│── data/                    # ---------------------------------Input data files
│   ├── test_data.csv        # ---------------------------Test dataset to which onboarding email will be send
│   ├── course_plan.xlsx     # ----------------------------Onboarding course outline month wise
```
## API Keys & Setup
- **SendGrid:** Create API Key → Add to `.env` as `SENDGRID_API_KEY`.
- **DataRobot:** Use `hr_onboarding_risk_training_data/` to train churn model (target column = `Churned`). Get Deployment ID and add to .env file.
-  Create GPT-4o mini deployment → Add credentials once deployment is done (`API_UL`, `API_KEY`, `DATAROBOT_KEY`, `DEPLOYMENT_ID`) to `.env`.

## Additional Folders
- **Churn Model Training Data/** → Historical dataset for churn model training (target = `churned`).
- **DataRobot_Policy_VDB_RAG/** → Policy documents used for creating vector database for chatbot (RAG).
---

## ⚙️ Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/zeeshanrobot/Capstone-HR-Assistant.git
cd Capstone-HR-Assistant
```

### 2. Create Environment File
Copy `.env.example` → `.env` and add your real secrets:

Fill `.env` with:
```
OPENAI_API_KEY=
OPENAI_API_VERSION=2024-10-21
OPENAI_API_BASE=https://datarobot-genai-enablement.openai.azure.com/
OPENAI_API_DEPLOYMENT_ID=gpt-4

TRACKER_LINK=https://docs.google.com/spreadsheets/d/1_EggujojD4pxLV6GFLLfr-O8TBN_vDmvlpT6veKVd-k/edit?usp=sharing
COURSE_LINK=https://enablement.datarobot.com/

SENDGRID_API_KEY=your-sendgrid-key
EMAIL_SENDER=xyzf@gmail.com
HR_TEAM_EMAIL=hr@example.com

CHURN_DEPLOYMENT_ID=
FEEDBACK_FORM_LINK=https://docs.google.com/forms/d/1kpLYCBGJt-RUYj5_hhHmT2mjWENThtDbnMm2_6-DCmw/edit#responses
HR_CHATBOT_LINK=

## Text Generation LLM Model ------------- keys:

API_URL=   # noqa
API_KEY=
DATAROBOT_KEY=
DEPLOYMENT_ID=
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

##  Running the Application

### Run Full HR Workflow (agents + predictions + emails)

### Run Chatbot App
```bash
streamlit run rag_chatbot_app.py
```
- open session environment and click on port 8501
- Opens a web UI at `http://localhost:8501`  
- New joiners can chat with the onboarding assistant.  
---

```bash
python main.py
```
- Scores new joiners with churn model.  
- Sends onboarding emails (low-risk joiners).  
- Alerts HR about high-risk joiners.  
- Sends feedback requests to all the new joiners for the onboarding experience

---

## Models & AI Used
- **DataRobot Churn Prediction Model**  
  - Classification model deployed in DataRobot.  
  - Predicts risk of employee churn.  

- **Azure OpenAI GPT-4o (via LangChain)**  
  - Generates onboarding email bodies.  

- **AWS Bedrock Mistral (via DataRobot LLM Gateway)**  
  - Powers CrewAI agent reasoning and task execution logs.  

---
---

## 📌 Summary
This application combines **predictive AI (DataRobot)**, **Generative AI (Azure GPT-4o + Mistral)**, and **Agentic AI (CrewAI)** to automate HR workflows:  
- Onboarding  
- Risk alerts  
- Feedback collection  
- Employee support chatbot  

---
