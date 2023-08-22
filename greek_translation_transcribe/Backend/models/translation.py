from ..utils.chatbot import chatbot_completion
import logging


# Translation chain
class Translation:
    def __init__(self, source_language, target_language):
        self.source_language = source_language
        self.target_language = target_language
        
    def translate(self, text):
        logger.info("Starting translation...")
        
        logger.info("Extracting context...")
        context = self.extract_context(text)
        logger.info(f"Context extracted: {context}")
        
        logger.info("Extracting key words...")
        key_words = self.extract_key_words(text)
        logger.info(f"Key words extracted: {key_words}")
        
        SYSTEM = f"""You are an expert {self.target_language} translator. Your role is to carefully examine the given text, which may be written in {self.source_language}, and translate it accurately into {self.target_language}. Your translation work should account for not only literal translation but also cultural and contextual nuances. You'll be given text that has to be translated into {self.target_language}, the context of the text and key words with possible translations. Your task is to ensure the translated text preserves the original message while being grammatically correct and contextually appropriate in {self.target_language}. If the text is not in {self.source_language} you will say "Please enter text in {self.source_language} to translate" Respond using markdown."""
        
        example_en_to_gr = f"""                    
                    "Given this text to translate: "It's a beautiful sunny day at the beach."
                    Translate it from English to Greek:
                    Given the context: "This sentence is describing a pleasant weather condition at a seaside location." and key words: "beautiful (όμορφος), sunny (ηλιόλουστος), day (μέρα), beach (παραλία)"
                    The translation is: "Είναι μια όμορφη ηλιόλουστη μέρα στην παραλία." 
                    """
        example_gr_to_en = f"""
                    "Given this text to translate: "Είναι μια όμορφη ηλιόλουστη μέρα στην παραλία."
                    Translate it from Greek to English:
                    Given the context: "This sentence is describing a pleasant weather condition at a seaside location." and key words: "όμορφη (beautiful), ηλιόλουστη (sunny), μέρα (day), παραλία (beach)"
                    The translation is: "It's a beautiful sunny day at the beach." " 
                    """
                    
        if self.source_language == "English":
            example = example_en_to_gr
        else:
            example = example_gr_to_en
                
        PROMPT = f"""
                    Translate from {self.source_language} to {self.target_language}:
                    
                    Example:
                    {example}
                    
                    Now, given this text to translate: "{text}"
       
                    Given the context: "{context}" and key words: "{key_words}"
                    
                    The translation is:
                    """
        logger.info("Translating text...")
        translation = chatbot_completition(SYSTEM, PROMPT)
        logger.info(f"Translation completed: {translation}")
        
        return translation, key_words
        
    
    def extract_context(self, text):
        '''Extracts context from text using chatgpt api call'''
        
        SYSTEM = "You are a sophisticated AI model capable of understanding and interpreting English text. Your task is to identify and describe the overall context or main topic of the following text."
        PROMPT = f"Please identify the context of this text: \"{text}\""
        context = chatbot_completition(SYSTEM, PROMPT)
        
        return context

    def extract_key_words(self, text):
        '''Extracts key words from text using chatgpt api call'''
        
        if self.source_language == "English":
            SYSTEM = """You are a sophisticated AI model trained to identify key words and phrases in English text. Your task is to extract the most important words or phrases that capture the main points of the following text.
            Example:
            Text:"It's a beautiful sunny day at the beach."
            key words: "beautiful (όμορφος), sunny (ηλιόλουστος), day (μέρα), beach (παραλία)"
            """
        else:
            SYSTEM = """You are a sophisticated AI model trained to identify key words and phrases in Greek text. Your task is to extract the most important words or phrases that capture the main points of the following text.
            Example:
            Text:"Είναι μια όμορφη ηλιόλουστη μέρα στην παραλία."
            Key words: "όμορφη (beautiful), ηλιόλουστη (sunny), μέρα (day), παραλία (beach)"
            """
        PROMPT = f"""Please extract the key words from this text: \"{text}\ and their possible translations in {self.target_language}.
        """
        key_words = chatbot_completition(SYSTEM, PROMPT)
        return key_words
