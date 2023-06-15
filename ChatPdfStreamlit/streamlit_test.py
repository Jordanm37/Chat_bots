import os
import streamlit as st
from io import StringIO
import re
import sys
from streamlit_chat import message

# Assuming ChatBot is the chatbot model you're using
from chatbot import ChatBot 
from layout import Layout

st.set_page_config(layout="wide")

# Instantiate the chatbot and layout
chatbot = ChatBot()
layout = Layout()

# Display the header of the app
layout.show_header()
st.markdown("## Welcome to the AI Assistant for Local Town Planning Regulation")
st.markdown("### Please ask me any questions related to the following topics:")
st.markdown("""
1. Zoning regulations
2. Building codes and permits
3. Land use regulations
4. Environmental regulations
5. Planning and development processes

I am well-versed in the legal framework and regulations governing these areas, and can provide you with accurate and personalized guidance based on your specific needs and circumstances.

If you have any questions related to these topics, please don't hesitate to ask. I am here to help you navigate the complex world of local town planning regulation and ensure that you are in compliance with all applicable laws and regulations."""
)
# """As an AI Assistant with expertise in local town planning regulation, I am here to assist you with any queries you may have. Please feel free to ask me any questions related to the following topics:

# 1. Zoning regulations
# 2. Building codes and permits
# 3. Land use regulations
# 4. Environmental regulations
# 5. Planning and development processes

# I am well-versed in the legal framework and regulations governing these areas, and can provide you with accurate and personalized guidance based on your specific needs and circumstances.

# If you have any questions related to these topics, please don't hesitate to ask. I am here to help you navigate the complex world of local town planning regulation and ensure that you are in compliance with all applicable laws and regulations."""

# # Initialize the chat history if not already done
# st.session_state["history"] = st.session_state.get("history", [])

# def append_message(sender, message):
#     st.session_state["history"].append((sender, message))



#### V1 ####
# Display the chat history
# with st.container():
#     for i, (sender, message) in enumerate(st.session_state["history"]):
#         if sender == "user":
#             st.markdown(f"**User**: {message}")
#         else:
#             st.markdown(f"**Assistant**: {message}")

# Display the chat history
# with st.container():
#     for i, (sender, message) in enumerate(st.session_state["history"]):
#         if sender == "user":
#             st.markdown(f"<div style='text-align: right'><b>User</b>: {message}</div>", unsafe_allow_html=True)
#         else:
#             st.markdown(f"Assistant: {message}")


            
# # Main loop
# with st.form(key="my_form", clear_on_submit=True):
#     is_ready, user_input = layout.prompt_form()

#     if is_ready:
#         # Update the chat history and display the chat messages
#         append_message("user", user_input)
#         output = chatbot.chat_bot_response(user_input) # replace this with your chatbot's method of generating a response
#         append_message("assistant", output)


#### V2 ####
# def display_chat(container):
#     # Clear the container to remove previous chat
#     container.empty()

#     # Display the chat history
#     with container:
#         for i, (sender, message) in enumerate(st.session_state["history"]):
#             if sender == "user":
#                 st.markdown(f"<div style='text-align: right'><b>User</b>: {message}</div>", unsafe_allow_html=True)
#             else:
#                 st.markdown(f"Assistant: {message}")

# # Container for the chat history
# chat_container = st.container()

# # Main loop
# with st.form(key="my_form", clear_on_submit=True):
#     is_ready, user_input = layout.prompt_form()

#     if is_ready:
#         # Update the chat history and display the chat messages
#         append_message("user", user_input)
#         output = chatbot.chat_bot_response(user_input) # replace this with your chatbot's method of generating a response
#         append_message("assistant", output)

#         # Update the chat display
#         display_chat(chat_container)
        
        
        
        
#### V3 ####    
# Initialize the chat history if not already done
# st.session_state["user"] = st.session_state.get("user", [])
# st.session_state["assistant"] = st.session_state.get("assistant", [])

# def append_message(sender, message):
#     st.session_state[sender].append(message)

# def generate_messages(container):
#     if st.session_state["assistant"]:
#         with container:
#             for i in range(min(len(st.session_state["user"]), len(st.session_state["assistant"]))):
#                 message(
#                     st.session_state["user"][i],
#                     is_user=True,
#                     key=f"history_{i}_user",
#                     avatar_style="big-smile",
#                 )
#                 message(st.session_state["assistant"][i], key=str(i), avatar_style="thumbs")

# # Container for the chat history
# chat_container = st.container()

# # Main loop
# with st.form(key="my_form", clear_on_submit=True):
#     is_ready, user_input = layout.prompt_form()

#     if is_ready:
#         # Update the chat history and display the chat messages
#         append_message("user", user_input)
#         output = chatbot.chat_bot_response(user_input) # replace this with your chatbot's method of generating a response
#         append_message("assistant", output)

#         # Generate the chat messages with avatars
#         generate_messages(chat_container)

#     with st.expander("Show Messages"):
#         st.write('st.session_state["user"]')     





# #### V4 #### Doesnt work
# if "history" not in st.session_state:
#     st.session_state["history"] = []
# # Initialize the chat history if not already done
# st.session_state["user"] = st.session_state.get("user", [])
# st.session_state["assistant"] = st.session_state.get("assistant", [])

# def append_message(sender, message):
#     st.session_state[sender].append(message)

# def generate_messages(container):
#     if st.session_state["assistant"]:
#         with container:
#             for i in range(min(len(st.session_state["user"]), len(st.session_state["assistant"]))):
#                 message(
#                     st.session_state["user"][i],
#                     is_user=True,
#                     key=f"history_{i}_user",
#                     avatar_style="big-smile",
#                 )
#                 message(st.session_state["assistant"][i], key=str(i), avatar_style="thumbs")

# # Container for the chat history
# chat_container = st.container()

# def extract_answer_and_sources(response):
#     answer = response['answer']
#     sources = [doc.metadata['source'] for doc in response['source_documents']]
#     return answer, sources


# def chat_bot_response(chatbot, user_input, chat_history):
#     response = chatbot.chat_bot_response(user_input, chat_history)
#     answer, sources = extract_answer_and_sources(response)
#     return answer, sources

# # Main loop
# with st.form(key="my_form", clear_on_submit=True):
#     is_ready, user_input = layout.prompt_form()

#     if is_ready:
#         # Update the chat history and display the chat messages
#         output, sources = chat_bot_response(chatbot, user_input, st.session_state["history"])
#         st.session_state["history"].append((user_input, output))

#         # Generate the chat messages with avatars
#         generate_messages(chat_container)

#         # Add sources expander
#         with st.expander("Sources"):
#             for source in sources:
#                 st.write(source)


#### V5 ####
if "history" not in st.session_state:
    st.session_state["history"] = []
# Initialize the chat history if not already done
st.session_state["user"] = st.session_state.get("user", [])
st.session_state["assistant"] = st.session_state.get("assistant", [])

def append_message(sender, message):
    st.session_state[sender].append(message)

def generate_messages(container):
    if st.session_state["assistant"]:
        with container:
            for i in range(min(len(st.session_state["user"]), len(st.session_state["assistant"]))):
                message(
                    st.session_state["user"][i],
                    is_user=True,
                    key=f"history_{i}_user",
                    avatar_style="big-smile",
                )
                message(st.session_state["assistant"][i], key=str(i), avatar_style="thumbs")

def extract_answer_and_sources(response):
    answer = response['answer']
    sources = [doc for doc in response['source_documents']]
    # sources = [doc.metadata['page'] for doc in response['source_documents']]
    return answer, sources


def chat_bot_response(chatbot, user_input, chat_history):
    response = chatbot.chat_bot_response(user_input, chat_history)
    print(response)
    answer, sources = extract_answer_and_sources(response)
    return answer, sources

# Container for the chat history
chat_container = st.container()

# Main loop
with st.form(key="my_form", clear_on_submit=True):
    is_ready, user_input = layout.prompt_form()

    if is_ready:
        # Update the chat history and display the chat messages
        append_message("user", user_input)
        output, sources = chat_bot_response(chatbot, user_input, st.session_state["history"])
        st.session_state["history"].append((user_input, output))
        append_message("assistant", output)

        # Generate the chat messages with avatars
        generate_messages(chat_container)

        with st.expander("Sources"):
            for source in sources:
                st.write(f'Page: {source}')  
                





#TODO add a button to clear the chat history
# with st.form(key="my_form", clear_on_submit=True):
#TODO re do and use roby chat messages since stremalit chat allows for avartars
# https://github.com/yvann-hub/Robby-chatbot/blob/30cc180c1fd29bd12cae2be1e7b6dae25ca034c0/src/modules/history.py
# TODO make into generalised repo for chatting and add pages 

"""As an AI Assistant with expertise in local town planning regulation, I am here to assist you with any queries you may have. Please feel free to ask me any questions related to the following topics:

1. Zoning regulations
2. Building codes and permits
3. Land use regulations
4. Environmental regulations
5. Planning and development processes

I am well-versed in the legal framework and regulations governing these areas, and can provide you with accurate and personalized guidance based on your specific needs and circumstances.

If you have any questions related to these topics, please don't hesitate to ask. I am here to help you navigate the complex world of local town planning regulation and ensure that you are in compliance with all applicable laws and regulations."""