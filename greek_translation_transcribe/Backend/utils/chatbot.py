import logging
from dotenv import load_dotenv
import os
import openai

load_dotenv(".env")
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Create a logger
logging.basicConfig(filename='debug.log',level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


# Generic Chatgpt chat completition with input arguments for system message and user message

def chatbot_completition(system_message, user_message):
    response = openai.ChatCompletion.create(
        model = 'gpt-4',
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )
    
    prompt, reply = response['usage']['prompt_tokens'], response['usage']['completion_tokens']
    cost = (0.03/1000)*prompt + (0.06/1000)*reply
    ## calculate api costs and log it
    logger.info(f"Prompt tokens: {prompt}, Completion tokens: {reply}, Cost: {cost}")

    return response["choices"][0]["message"]["content"]


