import pandas as pd
from utils.emailer import send_email
from crewai import Agent
from langchain.chat_models import AzureChatOpenAI
import os

from utils.churn_predictor import get_churn_scores

from dotenv import load_dotenv
load_dotenv()

#------ tracker link and course link:
TRACKER_LINK = os.getenv("TRACKER_LINK")
COURSE_LINK = os.getenv("COURSE_LINK")

## -----------------------   Streamkit chatbot link:
CHATBOT_LINK = os.getenv("HR_CHATBOT_LINK")


class HRAgent:
    def __init__(self, test_data_path, course_path):
        #-------------- Loading test data and predicting churn
        joiners_df = pd.read_csv(test_data_path)
        scored_df = get_churn_scores(joiners_df)
        scored_df.to_csv('results.csv',index =False) ##### for checking

         # -------------------Predicting churn
        self.scored_df = scored_df

        #------------- Keeping only low-risk employees
        self.eligible_df = scored_df[scored_df["churn_score"] == 0]
        self.at_risk_df = scored_df[scored_df["churn_score"] == 1]

        # ------------Loading and summarize course plan
        self.course_df = pd.read_excel(course_path)
        self.course_plan = "\n".join(
            [f"Month {row['Month']}: {row['Topic']}" for _, row in self.course_df.iterrows()]
        )

        
        self.llm = AzureChatOpenAI(
            deployment_name=os.getenv("OPENAI_API_DEPLOYMENT_ID"),
            temperature=0.4
        )

    def generate_message(self, name):
        prompt = f"""
You are a friendly HR assistant at DataRobot. 
A new employee named {name} just joined.

Please write only the **body** of a welcome email (not the subject).
It should explain:
- What the ADSA 6-month onboarding course is
- Include the course plan below
- Include links to the course and the progress tracker and HR assisatant chatbot

Do not include the subject line.

Course Outline:
{self.course_plan}

Course Link (plain URL, do not wrap in markdown): {COURSE_LINK}
Progress Tracker Link: {TRACKER_LINK}
HR Assistant Chatbot: {CHATBOT_LINK}
"""
        response = self.llm.predict(prompt)
        return response

    def onboard(self):
        print("\n **************   Sending onboarding emails to low-risk new joiners...\n")
        for _, row in self.eligible_df.iterrows():
            name = row['Name']
            email = row['Email']
            message = self.generate_message(name)
            send_email(
                to=email,
                subject="Welcome to DataRobot: Start Your ADSA Journey",
                body=message
            )
            print(f"✅ Email sent to {name} ({email})")

        print("\n🔴 🔴 🔴 🔴 🔴 The following joiners are predicted to churn. No email sent:")
        print(self.at_risk_df[['Name', 'Email', 'churn_score']])
