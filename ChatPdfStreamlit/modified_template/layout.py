import streamlit as st

class Layout:
    
    def show_header(self):
        """
        Displays the header of the app
        """
        st.markdown(
            f"""
            <h1 style='text-align: center;'> Ask about your regulations ! 😁</h1>
            """,
            unsafe_allow_html=True,
        )

    # def prompt_form(self):
    #     """
    #     Displays the prompt form
    #     """
    #     with st.form(key="my_form", clear_on_submit=True):
    #         user_input = st.text_area(
    #             "Query:",
    #             placeholder="Ask me anything about the document...",
    #             key="input",
    #             label_visibility="collapsed",
    #         )
    #         submit_button = st.form_submit_button(label="Send")
            
    #         is_ready = submit_button and user_input
    #     return is_ready, user_input
    
    def prompt_form(self):
        user_input = st.text_area(
            "Query:",
            placeholder="Ask me anything...",
            key="input",
            label_visibility="collapsed",
        )
        submit_button = st.form_submit_button(label="Send")
        is_ready = submit_button and user_input
        return is_ready, user_input