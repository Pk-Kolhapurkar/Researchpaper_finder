import streamlit as st
import taskingai
import os
import pprint as pp

# Read the API key from an environment variable
api_key = os.getenv("TASKINGAI_API_KEY")
if not api_key:
    st.error("API key not found. Please set the TASKINGAI_API_KEY environment variable.")
else:
    # Initialize the Tasking AI with your API key
    taskingai.init(api_key)

    # Set up Streamlit page configuration
    st.set_page_config(
        page_title="Research Paper Finder",
        page_icon="🔍",
        menu_items={
            'About': "# Made by Prathamesh Khade"
        }
    )

    # Title of the app
    st.title("Research Paper Finder")
    st.markdown("## Find the latest research papers.")

    # User input with text_area for multi-line input
    user_input = st.text_area(
        "Enter your query:",
        value="Get me a list of RAG papers from 2024.",
        height=150
    )

    # Append fixed information to ensure these details are always included
    fixed_details = " Include the source, title, author, publication date, a brief summary, GitHub link, and a link to each paper."
    full_query = user_input.strip() + fixed_details

    # Initialize the arxiv_qa_assistant
    assistants = taskingai.assistant.list_assistants()
    arxiv_qa_assistant = next((assistant for assistant in assistants if assistant.name == "arxivagent"), None)

    if arxiv_qa_assistant:
        new_chat = taskingai.assistant.create_chat(assistant_id=arxiv_qa_assistant.assistant_id)

        if st.button("Find Papers"):
            with st.spinner("Finding papers..."):
                user_message = taskingai.assistant.create_message(
                    assistant_id=arxiv_qa_assistant.assistant_id,
                    chat_id=new_chat.chat_id,
                    text=full_query
                )
                
                assistant_message = taskingai.assistant.generate_message(
                    assistant_id=arxiv_qa_assistant.assistant_id,
                    chat_id=new_chat.chat_id
                )
                
                # Extract the text content from the assistant_message
                response_text = assistant_message.content.text
                
                # Display the result
                st.success("Papers found!")
                st.markdown(response_text)
    else:
        st.error("Could not find arxiv_qa_assistant. Please check the assistant name.")

# Run Streamlit app
if __name__ == '__main__':
    st.write("Welcome to the Research Paper Finder app. Enter your query and find the latest papers!")
