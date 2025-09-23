# agents/feedback_agent.py

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='/home/notebooks/storage/.env')
import pandas as pd
from datetime import datetime
from utils.emailer import send_email
from langchain.chat_models import AzureChatOpenAI
FEEDBACK_FORM_LINK = os.getenv("FEEDBACK_FORM_LINK")
#FEEDBACK_FORM_LINK="https://docs.google.com/forms/d/1kpLYCBGJt-RUYj5_hhHmT2mjWENThtDbnMm2_6-DCmw/edit#responses"

class FeedbackAgent:
    def __init__(self, test_data_path):
        self.joiners_df = pd.read_csv(test_data_path)
        self.llm = AzureChatOpenAI(
            deployment_name=os.getenv("OPENAI_API_DEPLOYMENT_ID"),
            temperature=0.5
        )

    def send_feedback_requests(self):
        today = datetime.today().date()
        feedback_candidates = []

        for _, row in self.joiners_df.iterrows():
            name = row['Name']
            email = row['Email']
            joining_date = pd.to_datetime(row['JoinDate'], dayfirst=True).date()
            days_active = (today - joining_date).days
            print("%%%%%%%%%%%%%%%%%%%%%%%%  Dya Active : ",days_active)

            if days_active > 0:  #------------- Trigger days
                feedback_candidates.append((name, email, days_active))

        for name, email, days in feedback_candidates:

            prompt = f"""
You are an HR assistant at DataRobot.
A new employee named {name} joined {days} days ago.

Write a friendly email body requesting their feedback about their onboarding experience so far.
- Ask if they faced any blockers.
- Encourage them to share suggestions.
- Include this feedback form link: {FEEDBACK_FORM_LINK}

IMPORTANT: You must include the feedback form link exactly as shown: {FEEDBACK_FORM_LINK}

Don't include the subject line.
"""
            #print("*****************%%%%%%%%%%%%%📬 Prompt being sent to LLM:\n", prompt)
            
            message = self.llm.predict(prompt)
            send_email(
                to=email,
                subject="We'd love your feedback on your onboarding experience!",
                body=message
            )
            print(f"✅ Feedback request sent to {name} ({email})")
