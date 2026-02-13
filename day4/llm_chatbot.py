import streamlit as st
from groq import Groq


client = Groq(api_key="ENTER_YOUR_KEY_HERE")

st.title("Groq LLM Chatbot")


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


user_input = st.chat_input("Ask Something")

if user_input:
    
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    
    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=st.session_state.messages
)


    reply = response.choices[0].message.content


    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

   
    with st.chat_message("assistant"):
        st.write(reply)
