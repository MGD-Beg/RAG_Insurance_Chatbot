 # 🧠 Local RAG Chatbot (Gemma3:1B + Ollama + Streamlit)
 
 This project implements a **Retrieval-Augmented Generation (RAG) chatbot** using the **Gemma 3B model from Ollama**, powered by a vector store built from custom PDF documents. The chatbot can answer user questions using only the contents of the provided documents and responds with **"I don't know"** if the information is not found.
 
 ---
 
 ## 📌 Features
 
 - 🔍 Retrieves relevant content from PDF documentation.
 - 🧠 Uses local LLM (Gemma3:1B via [Ollama](https://ollama.com)) for generation.
 - ⚡ Fast semantic search with FAISS + Sentence-Transformers.
 - 🖥️ User-friendly web interface with Streamlit.
 - 🚫 No OpenAI or paid APIs – fully local and free.
 
 ---
 
 ## 🗂️ Project Structure
 
 ```
 RAG_Chatbot/
 │
 ├── app.py                   # Streamlit app for chat interface
 ├── build_vector_store.py    # Script to parse PDFs and build FAISS index
 ├── vectordb.index           # FAISS vector index (generated)
 ├── chunks.pkl               # Pickled list of text chunks (generated)
 ├── requirements.txt         # Python dependencies
 ├── README.md                # You're here!
 │
 ├── data/                    # Folder for all PDF source files
 │   ├── some_document.pdf
 │   └── another_doc.pdf
 ```
 
 ---
 
 ## ✅ Requirements
 
 - Python 3.8+
 - [Ollama](https://ollama.com) (installed and running locally)
 - PDF documents placed in the `/data` folder
 
 ---
 
 ## 🛠️ Installation
 
 ### 1. Clone the repository
 
 ```bash
 git clone https://github.com/yourname/local-rag-chatbot.git
 cd local-rag-chatbot
 ```
 
 ### 2. Create a virtual environment
 
 ```bash
 python -m venv venv
 source venv/bin/activate   # On Windows: venv\Scripts\activate
 ```
 
 ### 3. Install dependencies
 
 ```bash
 pip install -r requirements.txt
 ```
 
 If you don’t have `requirements.txt`, install manually:
 
 ```bash
 pip install streamlit pymupdf faiss-cpu sentence-transformers ollama
 ```
 
 ---
 
 ## 🤖 Setup Ollama with Gemma
 
 1. **Install Ollama** from [https://ollama.com](https://ollama.com)
 2. **Pull the Gemma model**:
 
 ```bash
 ollama pull gemma:2b
 ```
 
 3. **Start the model server**:
 
 ```bash
 ollama run gemma:2b
 ```
 
 Ollama will serve the model locally at `http://localhost:11434`.
 
 ---
 
 ## 📚 Prepare the Knowledge Base
 
 1. Place your PDF documents inside the `data/` directory.
 2. Run the vector store builder:
 
 ```bash
 python build_vector_store.py
 ```
 
 This will:
 - Extract text from all PDFs in `/data`
 - Chunk the text into ~1000 characters
 - Create sentence embeddings
 - Save the FAISS index and chunk data as:
   - `vectordb.index`
   - `chunks.pkl`
 
 ---
 
 ## 🚀 Run the Chatbot App
 
 Start the Streamlit interface:
 
 ```bash
 streamlit run app.py
 ```
 
 Then open [http://localhost:8501](http://localhost:8501) in your browser.
 
 ---
 
 ## 💬 How It Works
 
 1. You enter a question in the Streamlit app.
 2. Your question is embedded using `all-MiniLM-L6-v2`.
 3. FAISS retrieves the top 3 most relevant chunks from the PDFs.
 4. The context chunks and your question are sent to **Gemma** via **Ollama**.
 5. If the answer exists in the context, the model will respond.
 6. If the context doesn't contain an answer, it will respond: **"I don't know."**
 
 ---
 
 ## 🧪 Example Questions
 
 - ✅ “What is the deductible for the America’s Choice 2500 Gold plan?”
 - ❌ “Who is the president of the US?” → “I don’t know”
 
 ---
 
 ## 🛑 Windows Users – Fix for Runtime Errors
 
 If you get this error:
 
 ```
 RuntimeError: no running event loop
 ```
 
 Add this to the top of `app.py`:
 
 ```python
 import sys, asyncio
 if sys.platform.startswith('win'):
     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
 ```
 
 Also move this import **inside the button click handler** to prevent PyTorch/Streamlit clashes:
 
 ```python
 from sentence_transformers import SentenceTransformer
 ```
 
 ---
 
 ## 📄 License
 
 MGD License – free to use and modify locally.
 
 ---
 
 ## 🙋‍♂️ Credits
 
 - 💬 LLM: [Gemma by Google](https://ollama.com/library/gemma)
 - 🧠 Host: [Ollama](https://ollama.com)
 - 🧮 Embeddings: [Sentence-Transformers](https://www.sbert.net/)
 - 🧱 Vector Search: [FAISS](https://github.com/facebookresearch/faiss)
 - 🎨 UI: [Streamlit](https://streamlit.io)
 
 ---
