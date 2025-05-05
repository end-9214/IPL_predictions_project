from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "deepseek-r1-distill-llama-70b"


def analyze_predictions(predictions):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a cricket analyst. you have to talk like a cricket commentator . You will be given predictions for IPL matches. Your task is to analyze the predictions and provide insights on the match outcomes, team performance, and any other relevant information. and only return 'insights' in json format. just give two json dictonaries like match1 and match2 and inside those contain your analysis. If its only one match then return only one json dictionary. and if there were 2 matches then return 2 json dictionaries. and if there are no matches then return empty json dictionary.And always remember to give the analysis in a very human language.",
            },
            {
                "role": "user",
                "content": f"Analyze the following predictions: {predictions} in json form",
            },
        ],
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    raw_response = response.choices[0].message.content
    parsed_response = json.loads(raw_response)
    return parsed_response

def analyze_model_training(result):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a IPL winner prediction Machine learning analyzer, analyze the result of model evaluation in very human terms. and respond in json format only. You have to explain what those metrics in a very human language.",
            },
            {
                "role": "user",
                "content": f"Analyze the following Model evaluations: {result} in json form",
            },
        ],
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    raw_response = response.choices[0].message.content
    parsed_response = json.loads(raw_response)
    return parsed_response