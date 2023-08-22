from ..utils.chatbot import chatbot_completion
import whisper
import logging

class Transcription:
    def __init__(self, source_language, target_language):
        self.source_language = source_language
        self.target_language = target_language
        self.model = whisper.load_model("large")
        self.translate = Translation(source_language, target_language)

    def transcribe(self, audio_file):
        '''Transcribes the audio file and proofreads the transcription'''

        ### Size (in bytes) = (Sample Rate) * (Bit Depth/8) * (Number of Channels) * (Duration in seconds)
        ### Size = 44,100 * (16/8) * 1 * 60 = 5,292,000 bytes, which is approximately 5 MB.

        # Calculate the size of the audio file
        audio_file_size = os.path.getsize(audio_file)
        audio_length = audio_file_size / ( 44100 * (16/8) * 1 )
        logger.info(f"Audio file size: {audio_file_size} bytes and {audio_length} seconds")

        # Transcribe the audio
        logger.info("Starting transcription...")
        transcription = self.transcribe_audio(audio_file)
        logger.info(f"Transcription completed: {transcription}")

        # Proofread the transcription
        logger.info("Proofreading transcription...")
        proofread_transcription = self.proofread_transcription(transcription)
        logger.info(f"Proofread transcription: {proofread_transcription}")

        # Translate the transcription
        translation,key_words = self.translate.translate(proofread_transcription)
        
        return proofread_transcription, translation, key_words

    def transcribe_audio(self, audio_path):
        '''Transcribes an audio file using the whisper model'''
        
        # Check if file size is less than 25 MB
        file_size = os.path.getsize(audio_path) / (1024 * 1024) # size in MB
        if file_size > 25:
            raise ValueError(f"The file size is {file_size:.2f} MB which exceeds the 25 MB limit.")

        # Check if file extension is supported
        supported_file_types = ['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm']
        file_extension = os.path.splitext(audio_path)[1][1:]
        if file_extension not in supported_file_types:
            raise ValueError(f"The file type '{file_extension}' is not supported. Please use one of the following: {', '.join(supported_file_types)}.")

        # If checks pass, transcribe the audio
        audio_file = open(audio_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

        # Always close the file you opened
        audio_file.close()

        return transcript
        
        # result = self.model.transcribe(audio_file)        
        # return result["text"]

    def proofread_transcription(self, transcription):
        '''Improves the transcription quality using GPT-4'''
        
        SYSTEM = """You are an expert {self.source_langauge} transcription agent. In particular, an advanced language model trained to proofread and correct text based on grammar, syntax, and coherence in context. Your role is to carefully examine the given text in {self.source_langauge}, identify semantic errors resulting from transcription, and then correct these errors. Use your knowledge of {self.source_language} language and syntax to ensure the accuracy and coherence of the transcriptions. Your task is crucial for the quality and usefulness of the transcriptions. You will be given {self.source_langauge} text that has been transcribed but may contain errors. Your job is to fix these errors to the best of your ability. Respond using markdown.
        
        You will work through proofreading and correcting the transcription in the following way step by step:
        
        Identify the context: [context]
        Identify key words: [key words]
        Correct the transcription: [transcription]
        
        You will not add any additional detail to the transcription. You will only correct the transcription. You will only return the transcription. You will not return the context or key words.
        
        Write the transcription here:
               
        
        """
        
        PROMPT = f"Please proofread and correct this transcription: \"{transcription}\""
        proofread_transcription = chatbot_completition(SYSTEM, PROMPT)
        return proofread_transcription