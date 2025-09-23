import smtplib
from email.message import EmailMessage
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")



def send_email(to, subject, body):
    print("---- EMAIL DEBUG INFO ----")
    print("FROM:", EMAIL_SENDER)
    print("TO:", to)
    print("SUBJECT:", subject)
    #print("BODY:", body)
    print("---------------------------")

    message = Mail(
        from_email=EMAIL_SENDER,
        to_emails=to,
        subject=subject,
        plain_text_content=body
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"✅ Email sent to {to} (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Failed to send email to {to}: {e}")
        if hasattr(e, 'body'):
            print("📄 SendGrid Error:", e.body)