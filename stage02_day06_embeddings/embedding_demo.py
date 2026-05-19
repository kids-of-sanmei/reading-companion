import argparse
import hashlib
import json
import math
import os
import re
from pathlib import Path


DEFAULT_INPUT = Path("../stage02_day05_text_chunking/chunks.jsonl")
DEFAULT_OUTPUT = Path("embeddings.jsonl")
DEFAULT_MODEL = "text-embedding-3-small"


def load_dotenv_if_available():
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv()


def read_jsonl(path):
    records = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
            if "text" not in item:
                raise ValueError(f"Line {line_number} is missing required field: text")
            records.append(item)
    return records


def tokenize(text):
    return re.findall(r"[\w\u4e00-\u9fff]+", text.lower())


def offline_embedding(text, dim):
    vector = [0.0] * dim
    tokens = tokenize(text)
    if not tokens:
        return vector

    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dim
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign

    length = math.sqrt(sum(value * value for value in vector))
    if length == 0:
        return vector
    return [round(value / length, 6) for value in vector]


def openai_embeddings(texts, model):
    load_dotenv_if_available()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set. Use offline mode or create a .env file.")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Missing dependency: pip install openai python-dotenv") from exc

    client = OpenAI()
    response = client.embeddings.create(model=model, input=texts)
    return [item.embedding for item in response.data]


def build_embedding_records(chunks, embeddings, model_name):
    records = []
    for chunk, embedding in zip(chunks, embeddings):
        records.append(
            {
                "chunk_id": chunk.get("chunk_id"),
                "source": chunk.get("source"),
                "start_char": chunk.get("start_char"),
                "end_char": chunk.get("end_char"),
                "text": chunk["text"],
                "embedding_model": model_name,
                "embedding_dim": len(embedding),
                "embedding": embedding,
            }
        )
    return records


def write_jsonl(path, records):
    with path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")


def parse_args():
    parser = argparse.ArgumentParser(description="Create embeddings JSONL from chunk JSONL.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Path to chunks.jsonl")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Path to write embeddings.jsonl")
    parser.add_argument("--dim", type=int, default=32, help="Offline embedding dimension")
    parser.add_argument("--limit", type=int, default=None, help="Only process the first N chunks")
    parser.add_argument("--api", action="store_true", help="Use the OpenAI Embeddings API")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI embedding model")
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")
    if args.dim <= 0:
        raise SystemExit("--dim must be greater than 0")

    chunks = read_jsonl(input_path)
    if args.limit is not None:
        chunks = chunks[: args.limit]
    if not chunks:
        raise SystemExit("No chunks found.")

    texts = [chunk["text"] for chunk in chunks]
    if args.api:
        embeddings = openai_embeddings(texts, args.model)
        model_name = args.model
    else:
        embeddings = [offline_embedding(text, args.dim) for text in texts]
        model_name = f"offline-hash-{args.dim}"

    records = build_embedding_records(chunks, embeddings, model_name)
    write_jsonl(output_path, records)

    print(f"Read chunks: {len(chunks)}")
    print(f"Wrote embeddings: {output_path}")
    print(f"Embedding dim: {records[0]['embedding_dim']}")
    print(f"Embedding model: {model_name}")


if __name__ == "__main__":
    main()
