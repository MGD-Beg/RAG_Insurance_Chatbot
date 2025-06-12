import sys
import asyncio

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import streamlit as st
import faiss
import pickle
from ollama import chat

# Load FAISS index and chunks
index = faiss.read_index("vectordb.index")
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

st.title("Document QA Chatbot (Gemma 3B, Local)")
st.write("Ask a question about the documents. The answer will be based *only* on those PDFs, or it will reply 'I don’t know' if not answerable.")

query = st.text_input("Enter your question:", "")
if st.button("Submit") and query:
    # Defer import to avoid global torch conflict
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')

    q_emb = model.encode([query])
    k = 3
    distances, indices = index.search(q_emb, k)
    context_chunks = [chunks[idx] for idx in indices[0] if idx != -1]

    if len(context_chunks) == 0:
        answer = "I don't know"
    else:
        context_text = "\n\n".join(context_chunks)
        system_msg = ("You are an assistant that answers with details questions using only the given context. "
                      "If the answer is not contained in the context, reply 'I don’t know'.")
        user_msg = f"Context:\n{context_text}\n\nQuestion: {query}\nAnswer:"

        response = chat(model="gemma3:1b", messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ])
        answer = response['message']['content'].strip() or "I don't know"

    st.markdown("**Answer:**")
    st.write(answer)
