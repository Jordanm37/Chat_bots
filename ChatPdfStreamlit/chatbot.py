from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.llm import LLMChain
from langchain import PromptTemplate
from langchain.vectorstores import Qdrant
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
import concurrent.futures
from dotenv import load_dotenv

import qdrant_client

import os
import openai

from dotenv import load_dotenv

load_dotenv('.env')
# openai.api_key = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv('OPENAI_API_KEY')
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_API_URL = os.getenv("QDRANT_API_URL")

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
        # self.persist_directory = './db'
        # Get the absolute path to the directory of the current file
        # current_file_directory = os.path.dirname(os.path.abspath(__file__))

        # # Construct a path to the database
        # self.persist_directory = os.path.join(current_file_directory, 'db')

        self.embedding = OpenAIEmbeddings()

        # self.vectordb = Chroma(persist_directory=self.persist_directory, 
        #                     embedding_function=self.embedding)
        client = qdrant_client.QdrantClient(url=QDRANT_API_URL, prefer_grpc=True, api_key=QDRANT_API_KEY)
        self.vectordb = Qdrant(client=client, collection_name="my_documents", embeddings=self.embedding)

        # custom prompts
        self.CONDENSE_PROMPT = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

        Chat History:
        {chat_history}
        Follow Up Input: {question}
        Standalone question:"""

        self.QA_PROMPT = """You will act as an AI Assistant expert in the Nillumbik Planning Scheme that I am having a conversation with. You have the expertise of a lawer with 10 years of experience in local town planning regulation for Nillumbik in Melbourne, Australia. You will provide answers and guidance from your extensive knowledge and will always provide answer when requested with exact reference and outline from the source documents. Additionally, you will ask follow-up questions to clarify the last response and provide more accurate and personalized answers. If the answer is not included in your knowledge base, you will say "Hmm, This may be the answer, but you should double check." and continue to answer normally using the context given. Your response should be detailed and use as much of the relevant documents as possible. Your goal is to provide the best possible guidance and support to help me with my queries and problems related to your expertise.  

        Example:      
        
        Question: Does pruning of a native tree trigger a permit requirement under the Significant landscape overlay schedule 2?
        
        Response:
        Yes, pruning of a native tree does trigger a permit requirement under the Significant Landscape Overlay Schedule 2. This is stated in clause 42.03-2 of the Nillumbik Planning Scheme, which requires a permit to be obtained for the construction of a building or to carry out works, including the pruning or lopping of the trunk of a native tree, unless a schedule to the overlay specifically states that a permit is not required. Therefore, if the schedule to the overlay does not specifically state that a permit is not required for pruning of a native tree, then a permit must be obtained.

        The relevant clause is:

        VC224 Permit requirement
        A permit is required to:
        - Construct a building or to carry out works. This does not apply:
        - If a schedule to this overlay specifically states that a permit is not required.
        - To the conduct of agricultural activities including ploughing and fencing (but not the construction of dams) unless a specific requirement for that activity is specified in a schedule to this overlay.
        - Construct a fence if specified in the schedule to this overlay.
        - Remove, destroy or lop any vegetation specified in a schedule to this overlay. This does not apply:
        - Lopping or pruning native vegetation, for maintenance only, provided no more than 1/3 of the foliage of each individual plant is lopped or pruned. Lopping and pruning for maintenance.
        - Native vegetation that is to be removed, destroyed or lopped to the minimum extent necessary by the holder of an exploration, mining, prospecting, or retention license issued under the Mineral Resources (Sustainable Development) Act 1990: Mineral exploration and extraction that is low impact exploration within the meaning of Schedule 4A of the Mineral Resources (Sustainable Development) Act 1990; or in accordance with a work plan approved under Part 3 of the Mineral Resources (Sustainable Development) Act 1990.

        Now answer the following question using the same format as above:
        Relevant documents:
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
        self.gpt4 = ChatOpenAI(temperature=0, model_name = 'gpt-4')
        self.question_generator = LLMChain(llm=self.gpt3, prompt=self.CONDENSE_QUESTION_PROMPT)
        self.doc_chain = load_qa_with_sources_chain(self.gpt3, chain_type="stuff", prompt=self.QA_PROMPT_TEMPLATE)

        # declare main retrieval chain
        self.chain = ConversationalRetrievalChain(
            retriever=self.vectordb.as_retriever(),
            question_generator=self.question_generator,
            combine_docs_chain=self.doc_chain,
            return_source_documents = True
        )

    def non_db_response(self,query, chat_history):
        SYSTEM_MESSAGE = """You will act as an AI Assistant expert in the Nillumbik Planning Scheme that I am having a conversation with. You have the expertise of a lawer with 10 years of experience in local town planning regulation for Nillumbik in Melbourne, Australia. You will provide answers and guidance from your extensive knowledge and will always provide answer when requested with exact reference and outline from the source documents. Your response should be detailed and use as much of the relevant documents as possible. Your goal is to provide the best possible guidance and support to help me with my queries and problems related to your expertise.  

            Example:      
            
            Question: Does pruning of a native tree trigger a permit requirement under the Significant landscape overlay schedule 2?
            
            Response:
            Yes, pruning of a native tree does trigger a permit requirement under the Significant Landscape Overlay Schedule 2. This is stated in clause 42.03-2 of the Nillumbik Planning Scheme, which requires a permit to be obtained for the construction of a building or to carry out works, including the pruning or lopping of the trunk of a native tree, unless a schedule to the overlay specifically states that a permit is not required. Therefore, if the schedule to the overlay does not specifically state that a permit is not required for pruning of a native tree, then a permit must be obtained.

            The relevant clause is:

            VC224 Permit requirement
            A permit is required to:
            - Construct a building or to carry out works. This does not apply:
            - If a schedule to this overlay specifically states that a permit is not required.
            - To the conduct of agricultural activities including ploughing and fencing (but not the construction of dams) unless a specific requirement for that activity is specified in a schedule to this overlay.
            - Construct a fence if specified in the schedule to this overlay.
            - Remove, destroy or lop any vegetation specified in a schedule to this overlay. This does not apply:
            - Lopping or pruning native vegetation, for maintenance only, provided no more than 1/3 of the foliage of each individual plant is lopped or pruned. Lopping and pruning for maintenance.
            - Native vegetation that is to be removed, destroyed or lopped to the minimum extent necessary by the holder of an exploration, mining, prospecting, or retention license issued under the Mineral Resources (Sustainable Development) Act 1990: Mineral exploration and extraction that is low impact exploration within the meaning of Schedule 4A of the Mineral Resources (Sustainable Development) Act 1990; or in accordance with a work plan approved under Part 3 of the Mineral Resources (Sustainable Development) Act 1990.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": f"Given this previous conversation: {chat_history} and in the context of the Nillumbik Planning Scheme: {query}"},
            ],
        )
        return response["choices"][0]["message"]["content"]


    def summarise(self, fist_response, second_response, query):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You will be provided with two responses to a question concurrently. Your task is to merge these responses into a more comprehensive and thorough one. Begin with the details from the second response, then interweave the details from the first response without leaving out any information. Your aim is to generate a richer, more complete answer than either individual response could offer. Since it relates to legal content, all numbers and exact values must be inlcluded in the reponse. If you encounter contradictions between the two responses, please present both viewpoints to provide a balanced perspective. Remember, absolutely every detail is valuable and needs to be included in the final output.  DO NOT use the words 'response 1' or 'response 2'. Respond using markdown."},
                {"role": "user", "content": f"Response 1: {fist_response} Response 2: {second_response} Question: {query}"},
            ],
        )
        return response["choices"][0]["message"]["content"]

    def chat_bot_response(self, message, chat_history):
        # chat_history.append(message)
        response1 = self.chain({"question": message, "chat_history": chat_history})
        response2 = self.non_db_response(message, chat_history)
        summary = self.summarise(response1['answer'],response2, message)
        return summary, response1['source_documents']
    
    ### Multithreaded version###
    def chat_bot_response_simult(self, message, chat_history):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future1 = executor.submit(self.chain, {"question": message, "chat_history": chat_history})
            future2 = executor.submit(self.non_db_response, message, chat_history)
            response1 = future1.result()
            response2 = future2.result()

        summary = self.summarise(response1['answer'], response2, message)
        return summary, response1['source_documents']