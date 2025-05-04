from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "deepseek-r1-distill-llama-70b"


def analyze_predictions(predictions):

    client = Groq()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a cricket analyst. you have to talk like a cricket commentator . You will be given predictions for IPL matches. Your task is to analyze the predictions and provide insights on the match outcomes, team performance, and any other relevant information. and only return 'insights' in json format. just give two json dictonaries like match1 and match2 and inside those contain your analysis.",
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
