import streamlit as st
import os
from typing import List

# LangChain imports
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Page config
st.set_page_config(page_title="Code-Aware RAG Assistant 💻", layout="wide")

# Title
st.title("💻 Code-Aware RAG Assistant")
st.caption("Upload code/docs → Auto-index → Ask questions with retrieval-augmented generation")

# --- Session state for persistence ---
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "messages" not in st.session_state:
    st.session_state.messages = []

# Config
@st.cache_resource
def get_llm():
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)

@st.cache_resource
def get_embeddings():
    return OpenAIEmbeddings(model="text-embedding-ada-002")

llm = get_llm()
embeddings = get_embeddings()

# --- File upload & indexing ---
st.markdown("---")
st.subheader("📁 Upload code / docs to index")

uploaded_files = st.file_uploader(
    "Choose .py, .txt, .md, .json files", 
    accept_multiple_files=True, 
    type=["py", "txt", "md", "json"]
)

if st.button("🔄 Index files", type="primary") and uploaded_files:
    with st.spinner("Indexing..."):
        texts = []
        for file in uploaded_files:
            content = file.read().decode("utf-8", errors="ignore")
            texts.append(content)
        
        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        docs = splitter.create_documents(texts)
        
        # Create/update vector store
        st.session_state.vector_store = Chroma.from_documents(
            docs, embeddings, persist_directory="./chroma_db"
        )
        st.session_state.vector_store.persist()
        
        st.success(f"✅ Indexed {len(docs)} chunks from {len(uploaded_files)} files!")
        st.balloons()

# Show indexed status
if st.session_state.vector_store:
    st.success("✅ Vector store ready! Ask questions below.")
else:
    st.info("👆 Upload & index files first")

# --- Chat interface ---
st.markdown("---")
st.subheader("💬 Chat with your code base")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about your code/docs... (e.g., 'Explain the main function')"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response if vector store exists
    with st.chat_message("assistant"):
        if not st.session_state.vector_store:
            st.warning("❌ Index files first!")
        else:
            with st.spinner("Retrieving relevant code..."):
                # Get retriever
                retriever = st.session_state.vector_store.as_retriever(
                    search_type="similarity", search_kwargs={"k": 4}
                )
                
                # Build RAG chain
                prompt_template = ChatPromptTemplate.from_template(
                    """You are a code-aware assistant. Use ONLY the provided context to answer.

Context from your docs:
{context}

Chat history:
{chat_history}

Question: {question}

Answer concisely with code examples where relevant:"""
                )
                
                def format_history():
                    hist = []
                    for msg in st.session_state.chat_history[-6:]:  # Last 3 exchanges
                        role = "User" if isinstance(msg, HumanMessage) else "Assistant"
                        hist.append(f"{role}: {msg.content}")
                    return "\n".join(hist)
                
                rag_chain = (
                    {
                        "context": retriever,
                        "chat_history": RunnablePassthrough().assign(hist=format_history),
                        "question": RunnablePassthrough(),
                    }
                    | prompt_template
                    | llm
                )
                
                # Invoke
                response = rag_chain.invoke(prompt)
                response_text = response.content
                
                st.markdown(response_text)
                
                # Update histories
                st.session_state.chat_history.append(HumanMessage(content=prompt))
                st.session_state.chat_history.append(AIMessage(content=response_text))
                st.session_state.messages.append({"role": "assistant", "content": response_text})

# Sidebar: Clear & info
with st.sidebar:
    st.markdown("### 🔧 Controls")
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("### 📊 Status")
    st.info(f"Indexed chunks: {len(st.session_state.vector_store.get()['ids']) if st.session_state.vector_store else 0}")
    st.code("""
    Tech stack:
    • LangChain (RAG pipeline)
    • Chroma (vector DB)
    • OpenAI (embeddings + LLM)
    • Streamlit (UI)
    """)
