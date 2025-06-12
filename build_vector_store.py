# build_vector_store.py

import os
import fitz  # PyMuPDF
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# Parameters
PDF_FOLDER = "data"
CHUNK_SIZE = 1000  # characters per chunk

# Load and extract text from all PDF files in /data
chunks = []
pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]
print(f"Found {len(pdf_files)} PDF(s) in '{PDF_FOLDER}'...")

for file_name in pdf_files:
    file_path = os.path.join(PDF_FOLDER, file_name)
    print(f"Processing: {file_name}")
    doc = fitz.open(file_path)
    for page in doc:
        text = page.get_text()
        if text:
            # Chunk the text from each page
            for i in range(0, len(text), CHUNK_SIZE):
                chunk = text[i:i + CHUNK_SIZE]
                if chunk.strip():
                    chunks.append(chunk)
    doc.close()

print(f"Total chunks created: {len(chunks)}")

# Generate embeddings
print("Embedding chunks...")
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunks, show_progress_bar=True)

# Build FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

# Save index and chunks
faiss.write_index(index, "vectordb.index")
with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("Vector store created: 'vectordb.index' and 'chunks.pkl'")
