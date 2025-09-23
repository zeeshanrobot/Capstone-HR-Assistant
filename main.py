from crewai import Agent, Task, Crew  # components of Aghentic AI 
from agents.hr_agent import HRAgent   ## on boarding agent
from agents.alert_agent import AlertAgent  ## risk agent
from agents.feedback_agent import FeedbackAgent  ## feedback agent


import os
from dotenv import load_dotenv
from crewai import LLM
import datarobot as dr
import openai

feedback_logic = FeedbackAgent(test_data_path='data/test_data.csv')

#---------------- Load environment variables from .env
load_dotenv()

#--------------------------------------------------------------------------------- Initialize LLM for mistral (via DataRobot) gateways:
dr_client = dr.Client()

llm = LLM(
    model="bedrock/mistral.mixtral-8x7b-instruct-v0:1",
    api_key=dr_client.token,
    base_url=dr_client.endpoint + "/genai/llmgw",
    custom_llm_provider="openai"
)

# ----- existing logic with GPT + SendGrid
hr_logic = HRAgent(
    test_data_path='data/test_data.csv',  
    course_path='data/course_plan.xlsx'
)

#hr_alert_logic = HRAlertAgent(alert_email='hr@datarobot.com')  ##  --- Alert logic for churn customers check alert_agent.py file
alert_logic = AlertAgent(hr_logic.at_risk_df)


# --------: Real callback function that triggers onboarding

##------------------------------ agent for onboarding email:
def trigger_onboarding(_):
    print(" Triggering onboarding logic from CrewAI callback...")
    hr_logic.onboard() 

##------------------------------ alert agent for high risk joiners :
def alert_high_risk_joiners(_):
    print(" Sending alert to HR about high-risk joiners...")
    alert_logic.alert()


##------------------------------ feedback agent:
def trigger_feedback(_):
    print("Triggering feedback collection...")
    feedback_logic.send_feedback_requests()
    

# -------CrewAI agents and tasks

hr_agent = Agent(
    role="HR Specialist",
    goal="Send onboarding emails",
    backstory="You're an HR assistant...",
    llm=llm,
    verbose=True
)

alert_agent = Agent(
    role="HR Risk Monitor",
    goal="Alert HR about high-risk employees",
    backstory="You monitor churn predictions and escalate risk cases to HR.",
    llm=llm,
    verbose=True
)

feedback_agent = Agent(
    role="Feedback Collector",
    goal="Gather feedback from new joiners",
    backstory="You're an HR assistant checking in after 15 or 30 days to improve onboarding experience.",
    llm=llm,
    verbose=True
)

email_task = Task(
    description="Trigger onboarding logic via callback.",
    expected_output="All onboarding emails are sent successfully.",
    agent=hr_agent,
    callback=trigger_onboarding,
    async_execution=False
)

alert_task = Task(
    description="Alert HR about high-churn-risk new joiners via callback.",
    expected_output="HR is notified with the list of high-risk employees.",
    agent=alert_agent,
    callback=alert_high_risk_joiners,
    async_execution=False
)

feedback_task = Task(
    description="Send personalized onboarding feedback request to joiners after 15 or 30 days.",
    expected_output="Feedback request emails are sent to eligible joiners.",
    agent=feedback_agent,
    callback=trigger_feedback,
    async_execution=False
)

crew = Crew(
    agents=[hr_agent, alert_agent, feedback_agent],
    tasks=[email_task, alert_task, feedback_task],
    verbose=True
)

if __name__ == "__main__":
    crew.kickoff()
