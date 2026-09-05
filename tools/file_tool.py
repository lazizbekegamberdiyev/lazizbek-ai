from pathlib import Path


ALLOWED_EXTENSIONS = {
    ".csv",
    ".txt",
    ".json",
    ".xlsx",
    ".pdf",
}


def list_files(directory="documents"):
    path = Path(directory)

    if not path.exists():
        return []

    return [
        file.name
        for file in sorted(path.iterdir())
        if file.is_file()
        and file.suffix.lower() in ALLOWED_EXTENSIONS
    ]


if __name__ == "__main__":
    print("📂 Available files:")
    for file in list_files():
        print(f"- {file}")


def read_file(filename, directory="documents"):
    path = Path(directory) / filename

    if not path.exists():
        return f"File not found: {filename}"

    if path.suffix.lower() not in {".txt", ".json", ".csv"}:
        return f"Unsupported file type: {path.suffix}"

    return path.read_text(encoding="utf-8")
