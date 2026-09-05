from pathlib import Path

from document_loader import load_pdf_pages, create_page_chunks
from sentence_transformers import SentenceTransformer
import chromadb


DOCUMENTS_DIR = Path("documents")
COLLECTION_NAME = "lazizbek_documents"
DB_PATH = "./chroma_db"


print("📚 Scanning documents folder...")

pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf"))

if not pdf_files:
    print("❌ No PDF files found.")
    exit()


print(f"📄 Found {len(pdf_files)} PDF file(s):")

for pdf in pdf_files:
    print(f"   - {pdf.name}")


print("\n🧠 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")


print("💾 Connecting to ChromaDB...")
client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


print("\n📖 Processing documents...")

all_chunks = []

for pdf_file in pdf_files:

    print(f"\n📄 Processing: {pdf_file.name}")

    pages = load_pdf_pages(str(pdf_file))
    chunks = create_page_chunks(pages)

    print(f"   Pages: {len(pages)}")
    print(f"   Chunks: {len(chunks)}")

    for chunk_index, chunk in enumerate(chunks):

        all_chunks.append({
            "id": f"{pdf_file.name}_page_{chunk['page']}_chunk_{chunk_index}",
            "source": pdf_file.name,
            "page": chunk["page"],
            "text": chunk["text"]
        })


print(f"\n🧩 Total chunks: {len(all_chunks)}")


print("🔢 Creating embeddings...")

texts = [
    chunk["text"]
    for chunk in all_chunks
]

embeddings = model.encode(
    texts,
    show_progress_bar=True
).tolist()


print("💾 Saving to ChromaDB...")

collection.upsert(
    ids=[
        chunk["id"]
        for chunk in all_chunks
    ],
    documents=texts,
    embeddings=embeddings,
    metadatas=[
        {
            "source": chunk["source"],
            "page": chunk["page"]
        }
        for chunk in all_chunks
    ]
)


print("\n✅ Safe RAG indexing complete!")
print(f"📚 Documents: {len(pdf_files)}")
print(f"🧩 Chunks: {len(all_chunks)}")
print("💾 Metadata: source + page")
print("🔄 Safe re-indexing: ON")
