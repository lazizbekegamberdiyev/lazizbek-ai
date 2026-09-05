from sentence_transformers import SentenceTransformer
import chromadb


COLLECTION_NAME = "lazizbek_documents"
DB_PATH = "./chroma_db"

# Smaller distance = more relevant
RELEVANCE_THRESHOLD = 1.5

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_collection(
    name=COLLECTION_NAME
)


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
