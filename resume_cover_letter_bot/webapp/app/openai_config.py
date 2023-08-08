# openai_config.py
import openai
from dotenv import load_dotenv
import os
import logging

load_dotenv(".env")
openai.api_key = os.environ.get("OPENAI_API_KEY")

logger = logging.getLogger(__name__)
logger.info(f"OpenAI API key configured: {openai.api_key is not None}")
