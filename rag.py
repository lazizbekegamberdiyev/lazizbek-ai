from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from document_loader import load_pdf_pages, create_page_chunks


COLLECTION_NAME = "lazizbek_documents"
DB_PATH = "./chroma_db"

# Smaller distance = more relevant
RELEVANCE_THRESHOLD = 1.5

DOCUMENTS_DIR = Path("documents")

print("🧠 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("💾 Connecting to ChromaDB...")
client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def build_index():
    print("📚 Building RAG index...")

    pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        print("❌ No PDF files found.")
        return

    all_chunks = []

    for pdf_file in pdf_files:
        print(f"📄 Processing: {pdf_file.name}")

        pages = load_pdf_pages(str(pdf_file))
        chunks = create_page_chunks(pages)

        for chunk_index, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{pdf_file.name}_page_{chunk['page']}_chunk_{chunk_index}",
                "source": pdf_file.name,
                "page": chunk["page"],
                "text": chunk["text"]
            })

    if not all_chunks:
        print("❌ No chunks created.")
        return

    print(f"🧩 Total chunks: {len(all_chunks)}")
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

    print("✅ RAG indexing complete!")


# If the collection is empty, build the index automatically.
if collection.count() == 0:
    build_index()
else:
    print(f"✅ Existing RAG index found: {collection.count()} chunks")


def search_documents(query, n_results=3):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    sources = []
    seen = set()

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        if distance >= RELEVANCE_THRESHOLD:
            continue

        key = (
            metadata["source"],
            metadata["page"],
            document
        )

        if key in seen:
            continue

        seen.add(key)

        sources.append({
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"],
            "distance": distance
        })

    return sources
