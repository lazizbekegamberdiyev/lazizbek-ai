from pypdf import PdfReader


def read_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def chunk_text(text, chunk_size=1000):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size].strip()

        if chunk:
            chunks.append(chunk)

    return chunks


if __name__ == "__main__":
    text = read_pdf("1_lecture01.pdf")
    chunks = chunk_text(text)

    print(f"📄 Total characters: {len(text)}")
    print(f"🧩 Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks[:3], 1):
        print(f"\n--- Chunk {i} ---")
        print(chunk)
