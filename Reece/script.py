from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.llm import LLMChain
from langchain import PromptTemplate
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from dotenv import load_dotenv
import streamlit as st
import os


load_dotenv()

# load the API key from the .env file
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# load vector db from disk
persist_directory = 'db'
## here we are using OpenAI embeddings but in future we will swap out to local embeddings
embedding = OpenAIEmbeddings()

vectordb = Chroma(persist_directory=persist_directory, 
                  embedding_function=embedding)



# custom prompts
CONDENSE_PROMPT = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

QA_PROMPT = """You will act as an AI Assistant that I am having a conversation with. You have access to a clients training records and will be asked questions relating to their performance. You will ask follow-up questions to clarify the last response and provide more accurate and personalized answers. If the answer is not included in your knowledge base, you will say 'Hmm, I am not sure.' and stop after that. Your goal is to provide the best possible guidance and support to help me with my queries and problems. You think things through step by step every time and show your working. You break down problems into simple steps before solving and always double check your answers. 

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

# initialise llm instances and chains
gpt3 = ChatOpenAI(temperature=0, model_name = 'gpt-3.5-turbo')
gpt4 = ChatOpenAI(temperature=0, model_name = 'gpt-4')
question_generator = LLMChain(llm=gpt3, prompt=CONDENSE_QUESTION_PROMPT)
doc_chain = load_qa_with_sources_chain(gpt4, chain_type="stuff", prompt=QA_PROMPT_TEMPLATE)

# declare main retrieval chain
chain = ConversationalRetrievalChain(
    retriever=vectordb.as_retriever(),
    question_generator=question_generator,
    combine_docs_chain=doc_chain,
    return_source_documents = True
)

def chat_bot_response(message, chat_history):
    # chat_history.append(message)
    result = chain({"question": message, "chat_history": chat_history})
    return result

def main():
    st.title('Simple Streamlit App')
    chat_history = []
    user_input = st.text_input("Please enter your question here")
    if st.button('Submit'):
        response = chat_bot_response(user_input,chat_history)
        answer = response['answer']
        sources = response['source_documents']
        st.write(f'Your message: {user_input}')
        st.write(f'Bot response: {answer}')
        with st.expander("Sources"):
                for source in sources:
                    st.write(f'Page: {source}')  
if __name__ == "__main__":
    main()