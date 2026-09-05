from sentence_transformers import SentenceTransformer
import chromadb


COLLECTION_NAME = "lazizbek_documents"

print("🧠 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("💾 Connecting to ChromaDB...")
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection(
    name=COLLECTION_NAME
)


def search_documents(query, n_results=3):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results


if __name__ == "__main__":

    query = "What is panel data?"

    print()
    print(f"🔎 Query: {query}")
    print()

    results = search_documents(query, 3)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for i, (document, metadata) in enumerate(
        zip(documents, metadatas), 1
    ):
        print(
            f"--- Relevant Chunk {i} | "
            f"Page {metadata['page']} ---"
        )

        print(f"📄 Source: {metadata['source']}")
        print()
        print(document)
        print()
