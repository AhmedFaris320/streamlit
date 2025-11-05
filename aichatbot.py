import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage  
from langchain_groq import ChatGroq

llm = ChatGroq(
    groq_api_key="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",  # or rely on environment variable
    model="llama-3.3-70b-versatile"         # example model, you can change
)
st.set_page_config(page_title="AI Chat Bot", page_icon=":robot_face:", layout="centered")
st.title("AI Chat Bot")
st.subheader("Your personal AI assistant")
st.subheader("Powered by Groq and Langchain")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []      

if "conversation" not in st.session_state:
    st.session_state.conversation = ChatGroq(
        groq_api_key="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",  # or rely on environment variable
        model="llama-3.3-70b-versatile"         # example model, you can change
    )
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    else:
        with st.chat_message("assistant"):
            st.write(message.content)
userinput = st.chat_input("Type your message here")
if userinput:
    st.session_state.chat_history.append(HumanMessage(content=userinput))
    with st.chat_message("user"):
        st.write(userinput)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Convert chat history to messages format
            messages = []
            for msg in st.session_state.chat_history[:-1]:  # Exclude the current user message
                messages.append(msg)
            messages.append(HumanMessage(content=userinput))
            
            response = st.session_state.conversation.invoke(messages)
            ai_response = response.content
            st.session_state.chat_history.append(AIMessage(content=ai_response))
            st.write(ai_response)           
    with st.sidebar:
        st.title('options') 
        if st.button("Clear Conversation"):
            st.session_state.chat_history = []      
            st.session_state.conversation = ChatGroq(
                groq_api_key="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",  # or rely on environment variable
                model="llama-3.3-70b-versatile"         # example model, you can change
            )
            st.rerun()
st.subheader("about")  
st.write("This app is built using [Streamlit](https://streamlit.io/), [Langchain](https://python.langchain.com/en/latest/) and [Groq](https://www.groq.com/). The model used is [Llama 3.3 70B Versatile](https://www.groq.com/models/llama-3-3-70b-versatile).")          