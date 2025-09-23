import os
from utils.emailer import send_email
from dotenv import load_dotenv
load_dotenv()

class AlertAgent:
    def __init__(self, risky_df):
        self.risky_df = risky_df

    def alert(self):
        risky_names = self.risky_df['Name'].tolist()
        risky_emails = self.risky_df['Email'].tolist()

        risk_summary = "\n".join([f"{name} ({email})" for name, email in zip(risky_names, risky_emails)])

        message = f"""🚨 The following new joiners are predicted to be at high churn risk:

{risk_summary}

Please consider reaching out to them for proactive retention.
"""

        send_email(
            to=os.getenv("HR_TEAM_EMAIL"),
            subject="⚠️ High-Risk Joiners Alert: Churn Prediction",
            body=message
        )
