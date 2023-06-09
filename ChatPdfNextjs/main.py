from fastapi import FastAPI
import openai
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi import FastAPI, Request
import asyncio
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from dotenv import load_dotenv
import os

load_dotenv(".env")
openai.api_key = os.environ.get("OPENAI_API_KEY")


persist_directory = 'db'
## here we are using OpenAI embeddings but in future we will swap out to local embeddings
embedding = OpenAIEmbeddings()

vectordb = Chroma(persist_directory=persist_directory, 
                  embedding_function=embedding)

CONDENSE_PROMPT = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

QA_PROMPT = """You will act as an AI Assistant that I am having a conversation with. You have the expertise of an expert physics professor that specialises in advanced mathematical physics and dynamical mechanics. You will provide answers and guidance from your extensive knowledge, and will always provide relevant theorems when requested. Additionally, you will ask follow-up questions to clarify the last response and provide more accurate and personalized answers. If the answer is not included in your knowledge base, you will say 'Hmm, I am not sure.' and stop after that. Your goal is to provide the best possible guidance and support to help me with my queries and problems. You think things through step by step every time and show your working. You break down problems into simple steps before solving and always double check your answers. 

{summaries}

Question: {question}
Helpful answer in markdown or latex where equations are included:"""

# Create PromptTemplate instances
CONDENSE_QUESTION_PROMPT = PromptTemplate(
    input_variables=["chat_history", "question"], 
    template=CONDENSE_PROMPT
)

QA_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["summaries", "question"], 
    template=QA_PROMPT
)


gpt3 = ChatOpenAI(temperature=0, model_name = 'gpt-3.5-turbo')
gpt4 = ChatOpenAI(temperature=0, model_name = 'gpt-4')
question_generator = LLMChain(llm=gpt3, prompt=CONDENSE_QUESTION_PROMPT)
doc_chain = load_qa_with_sources_chain(gpt4, chain_type="stuff", prompt=QA_PROMPT_TEMPLATE)

chain = ConversationalRetrievalChain(
    retriever=vectordb.as_retriever(),
    question_generator=question_generator,
    combine_docs_chain=doc_chain,
    return_source_documents = True
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat(request: Request):
    chat_in = await request.json()
    user_content = chat_in.get('content')

    chat_history = []  # You might want to store chat history somewhere else to keep it between different requests
    query = user_content
    result = chain({"question": query, "chat_history": chat_history})

    return {
        "answer": result['answer'],
        "source_documents": result['source_documents']
    }
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    

#TODO - add a chat history to the request and return it in the response
#TODO - add a chat history input to the chain
#TODO - add a chat history to the chain
#TODO - Add custom bufer memory in the chain or frontend
