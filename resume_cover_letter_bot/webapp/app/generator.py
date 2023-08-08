import logging
import openai
import os

logging.basicConfig(filename='example.log',level=logging.INFO)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv(".env")
openai.api_key = os.environ.get("OPENAI_API_KEY")

from .helpers import create_docx, extract_key_words_and_resp, filter_key_words, extract_resume_exp, write_coverletter


def generate_cover_letter(personal_details, extra_instructions, job_descr, resume):
    try:
        key_words = extract_key_words_and_resp(job_descr)

        filtered_key_words = filter_key_words(key_words,resume)

        relevant_exp = extract_resume_exp(filtered_key_words,resume)

        cover_letter = write_coverletter(job_descr, filtered_key_words,relevant_exp, personal_details, extra_instructions)

        file_path = create_docx(cover_letter)

        return file_path
    except Exception as e:
        logger.error(f"Failed to generate cover letter: {e}")
        raise
