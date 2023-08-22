**Component Details:**

1. **Activity Generator:**
        - The activity generator will provide engaging language learning activities based on user proficiency.
    - Input: User's current proficiency level, learning history, preferences.
    - Output: Generated activity that matches user's current level and learning style.
    - The back-end will use the `activity_generator.py` script that communicates with the OpenAI API.
    - The front-end will render the generated activity and handle user interactions.
2. **Translation (with dictionary definitions as source):**
    - The translation feature allows the user to input a word or phrase in their language and get the translation in Greek.
    - Input: User's text in source language.
    - Output: Translated text in Greek.
    - The back-end uses `translation.py` script that utilizes the OpenAI API.
    - The front-end will have a form for users to input text and a display area to present translated text.
3. **Real-time Transcription and Translation:**
    - This feature transcribes spoken language and translates it into Greek in real-time.
    - Input: Spoken language through a microphone.
    - Output: Transcribed and translated text in Greek.
    - The back-end leverages `transcription.py` and `real_time_translation.py` scripts, interfacing with OpenAI API.
    - The front-end will require microphone access and display the transcribed and translated text.
4. **PDF Translation:**
    - Users can upload a PDF in their language and get it translated into Greek.
    - Input: PDF document.
    - Output: Translated PDF text in Greek.
    - The back-end utilizes `pdf_extractor.py` and `pdf_translation.py` scripts.
    - The front-end will need to include a PDF upload feature and display the translated content.
5. **Lesson Plan Generator:**
    - The lesson plan generator will tailor-make lessons based on user proficiency and interests.
    - Input: User's current proficiency level, learning history, preferences.
    - Output: Personalized lesson plan.
    - The back-end uses `lesson_plan_generator.py` script interfacing with the OpenAI API.
    - The front-end displays the lesson plans in an interactive and user-friendly format.

**Front-End:**
The front-end should be a Single-Page Application (SPA) built using React.js. It should provide an intuitive and engaging user interface for users to interact with the various components of the GLLC.

Key Pages:
- Home Page
- Activity Page
- Translation Page
- Transcription Page
- PDF Translation Page
- Lesson Plan Page
- User Profile Page

Use cases:
	- Tutor bot - ask questions
	- Translator
	- Transcribe and translation


Prioirities:
1. Translate
2. real time transcription and translate

Dictionary sources:
- Oxford api https://developer.oxforddictionaries.com/documentation/making-requests-to-the-api
- parse xdxf file and index to use as dictionary
- use compsable index llma index for querying over index of indexes - can index by letters[Composability - LlamaIndex 🦙 0.6.9 (gpt-index.readthedocs.io)](https://gpt-index.readthedocs.io/en/latest/how_to/index_structs/composability.html)
Resources:
- Use whisper in first demo, then implement faster whisper
- [e-johnstonn/wingmanAI: Real-time transcription of audio, integrated with ChatGPT for interactive use. Save, load, and append transcripts for effective context management in conversations. (github.com)](https://github.com/e-johnstonn/wingmanAI)

Code outline:

**Python Libraries:**

- **openai**: To communicate with the OpenAI GPT model.
- **requests**: To send HTTP requests.
- **fastapi**: To create the backend server.
- **sqlalchemy**: To interface with the database.
- **pdfplumber**: To extract text from PDFs.
- **whisper**: OpenAI's Whisper ASR API for audio transcription.

**Key Functions:**

1. **Activity Generator:**
    - `generate_activity(user_proficiency, user_history, user_preferences)`: Uses the OpenAI API to generate an activity based on the user's proficiency, history, and preferences.
    - `evaluate_activity(user_input, activity)`: Evaluates the user's input for an activity and provides feedback.
2. **Translation:**
    - `translate_text(user_text, target_language)`: Uses the OpenAI API to translate the user's text into the target language.
    - `get_definition(word, language)`: Accesses the dictionary definitions for a word in a certain language.
3. **Real-time Transcription and Translation:**
    - `transcribe_audio(audio_input)`: Transcribes the audio input using Whisper ASR.
    - `translate_transcription(transcription, target_language)`: Translates the transcribed text into the target language.
4. **PDF Translation:**
    - `extract_pdf_text(pdf_file)`: Extracts text from a PDF file.
    - `translate_pdf_text(pdf_text, target_language)`: Translates the extracted PDF text into the target language.
5. **Lesson Plan Generator:**
    - `generate_lesson_plan(user_proficiency, user_history, user_preferences)`: Generates a lesson plan based on the user's proficiency, history, and preferences.
    - `evaluate_lesson_plan(user_feedback, lesson_plan)`: Evaluates the effectiveness of a lesson plan based on user feedback.

**Frontend Libraries (React.js):**
- **react-router-dom**: For routing and navigation in the application.
- **axios**: To send HTTP requests from the frontend to the backend.
- **react-bootstrap**: For pre-styled components and responsive layout.
- **react-pdf**: For rendering PDF documents.
- **react-mic**: To capture audio input from the user.

