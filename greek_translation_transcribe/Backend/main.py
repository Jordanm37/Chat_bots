from fastapi import FastAPI
from .models.translation import Translation
from .models.transcription import Transcription
from .models.document_translation import DocumentTranslation

app = FastAPI()

@app.get("/translate")
async def translate():
    # Use the Translation class here
    pass

@app.get("/transcribe")
async def transcribe():
    # Use the Transcription class here
    pass

@app.get("/document-transcribe")
async def document_transcribe():
    # Use the DocumentTranslation class here
    pass
