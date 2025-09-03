import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

def main():    
    load_dotenv()
    model_name = "openai/gpt-4o"
    token = os.environ["GGITHUB_TOKEN"]
    endpoint = "https://models.github.ai/inference"
    st.title("MyGPT")
    st.header("Your Personal AI Assistant")
    message("Hello! I'm your personal AI assistant. How can I help you today?", key="assistant_start")


    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant that helps people find information.")
        ]
    
    with st.sidebar:
        st.image("https://img.freepik.com/free-vector/robot-chatting-concept-illustration_114360-2500.jpg?w=740&t=st=1696540803~exp=1696541403~hmac=1f0a5e2a4a")
        user_input = st.text_input("Enter your message here:", key="user_input")
    if user_input:
        
        
        st.session_state.messages.append(UserMessage(content=user_input))
        with st.spinner("AI is thinking..."):
            response = client.complete(
                model= model_name,  # Replace with your preferred Deepseek model
                messages=st.session_state.messages,
                temperature=0.3
            )
        ai_response = response.choices[0].message.content
        st.session_state.messages.append(AssistantMessage(content=ai_response))
       
    messages=st.session_state.get("messages", [])
    for i, msg in enumerate(messages[1:]):
        if isinstance(msg, UserMessage):
            message(msg.content, is_user=True, key=f"user_{i}")
        elif isinstance(msg, AssistantMessage):
            message(msg.content, key=f"assistant_{i}")
        



if __name__ == "__main__":
    

    main()
