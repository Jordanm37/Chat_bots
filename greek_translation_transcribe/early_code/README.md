# Greek Audio Transcription App using Whisper

This is a Python project that allows you to transcribe an audio file using the Whisper library and a user-friendly interface built with Gradio for text translation.

# Installation

Clone the repository:


Navigate to the project directory:

```
cd audio-transcription-app
```

Create a virtual environment (optional but recommended), I tested my script on
Python 3.10:

```
python3 -m venv env
source env/bin/activate
```

or with conda:

```
conda create -n app

conda activate app
```

Install the required packages:

```
pip install -r requirements.txt
```


```
Create a .env file and create a variable 'OPENAI_API_KEY' for you api key
```


Start the application:

```
python app.py
```

Upload an audio file (in .mp3, .wav, or .flac format).

Click the "Submit" button to start the transcription process.

Wait for the application to transcribe the audio file and display the results.