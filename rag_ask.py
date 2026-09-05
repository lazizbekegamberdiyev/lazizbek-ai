from google import genai
from dotenv import load_dotenv

from rag_search import search_documents


load_dotenv()

client = genai.Client()


def ask_from_documents(question):
    results = search_documents(question, n_results=3)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for i, (document, metadata) in enumerate(
        zip(documents, metadatas), 1
    ):
        context_parts.append(
            f"""
[Source {i}]
File: {metadata['source']}
Page: {metadata['page']}

Content:
{document}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are Lazizbek AI's document assistant.

Answer the user's question using ONLY the provided document context.

Rules:
- Do not invent information.
- If the documents do not contain enough information, say so.
- Give a clear, useful answer.
- At the end, provide a Sources section.
- In Sources, list the file name and page number used.
- Only cite pages that actually support your answer.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    question = input("📚 Ask about your document: ")

    answer = ask_from_documents(question)

    print()
    print("🤖 AI:")
    print(answer)
