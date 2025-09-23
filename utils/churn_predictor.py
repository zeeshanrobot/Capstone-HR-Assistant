import os
import pandas as pd
import datarobot as dr
from datarobot_predict.deployment import predict
from dotenv import load_dotenv

load_dotenv()

dr.Client()  
DEPLOYMENT_ID = os.getenv("CHURN_DEPLOYMENT_ID")

def get_churn_scores(payload: pd.DataFrame) -> pd.DataFrame:
    predictions_df, _ = predict(
        deployment=dr.Deployment.get(DEPLOYMENT_ID),
        data_frame=payload
    )
    payload["churn_score"] = predictions_df["Churned_PREDICTION"]
    return payload
