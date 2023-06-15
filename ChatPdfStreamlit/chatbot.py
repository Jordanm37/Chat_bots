from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.llm import LLMChain
from langchain import PromptTemplate
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from dotenv import load_dotenv
import os
import openai

from dotenv import load_dotenv

load_dotenv('.env')
# openai.api_key = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

### For testing ###
# class ChatBot():
    
    # def chat_bot_response(self, user_content):
    #     response = openai.ChatCompletion.create(
    #         model="gpt-4",
    #         messages=[
    #             {"role": "system", "content": "You are a chatbot. Hold a conversation. Respond using markdown."},
    #             {"role": "user", "content": user_content},
    #         ],
    #     )
    #     return response["choices"][0]["message"]["content"]


class ChatBot:
    def __init__(self):
        # load vector db from disk
        self.persist_directory = 'db'
        self.embedding = OpenAIEmbeddings()

        self.vectordb = Chroma(persist_directory=self.persist_directory, 
                            embedding_function=self.embedding)

        # custom prompts
        self.CONDENSE_PROMPT = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

        Chat History:
        {chat_history}
        Follow Up Input: {question}
        Standalone question:"""

        self.QA_PROMPT = """You will act as an AI Assistant that I am having a conversation with. You have the expertise of a lawer with 10 years of experience in local town planning regulation. You will provide answers and guidance from your extensive knowledge and will always provide answer when requested with exact reference . Additionally, you will ask follow-up questions to clarify the last response and provide more accurate and personalized answers. If the answer is not included in your knowledge base, you will say "Hmm, This may be the answer, but you should double check." and continue to answer normally using the context given. Your goal is to provide the best possible guidance and support to help me with my queries and problems related to your expertise.  

        {summaries}

        Question: {question}
        Helpful answer in markdown or latex where equations are included:"""

        # Create PromptTemplate instances
        self.CONDENSE_QUESTION_PROMPT = PromptTemplate(
            input_variables=["chat_history", "question"], 
            template=self.CONDENSE_PROMPT
        )

        self.QA_PROMPT_TEMPLATE = PromptTemplate(
            input_variables=["summaries", "question"], 
            template=self.QA_PROMPT
        )

        # initialise llm instances and chains
        self.gpt3 = ChatOpenAI(temperature=0, model_name = 'gpt-3.5-turbo')
        self.gpt4 = ChatOpenAI(temperature=0, model_name = 'gpt-3.5-turbo')
        self.question_generator = LLMChain(llm=self.gpt3, prompt=self.CONDENSE_QUESTION_PROMPT)
        self.doc_chain = load_qa_with_sources_chain(self.gpt4, chain_type="stuff", prompt=self.QA_PROMPT_TEMPLATE)

        # declare main retrieval chain
        self.chain = ConversationalRetrievalChain(
            retriever=self.vectordb.as_retriever(),
            question_generator=self.question_generator,
            combine_docs_chain=self.doc_chain,
            return_source_documents = True
        )

    def chat_bot_response(self, message, chat_history):
        # chat_history.append(message)
        result = self.chain({"question": message, "chat_history": chat_history})
        return result
    
