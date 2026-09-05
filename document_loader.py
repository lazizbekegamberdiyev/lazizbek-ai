from pypdf import PdfReader


def load_pdf_pages(file_path):
    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages, 1):
        text = page.extract_text()

        if text:
            pages.append({
                "page": page_number,
                "text": text.strip()
            })

    return pages


def create_page_chunks(pages, chunk_size=1000):
    chunks = []

    for page in pages:
        text = page["text"]
        page_number = page["page"]

        for i in range(0, len(text), chunk_size):
            chunk_text = text[i:i + chunk_size].strip()

            if chunk_text:
                chunks.append({
                    "page": page_number,
                    "text": chunk_text
                })

    return chunks


if __name__ == "__main__":

    pages = load_pdf_pages("1_lecture01.pdf")
    chunks = create_page_chunks(pages)

    print(f"📄 Pages: {len(pages)}")
    print(f"🧩 Chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks[:3], 1):
        print(f"\n--- Chunk {i} | Page {chunk['page']} ---")
        print(chunk["text"])
