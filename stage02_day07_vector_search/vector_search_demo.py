import argparse
import hashlib
import json
import math
import re
from pathlib import Path


DEFAULT_INPUT = Path("../stage02_day06_embeddings/embeddings.jsonl")
DEFAULT_OUTPUT = Path("search_results.json")


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
            embedding = item.get("embedding")
            if not isinstance(embedding, list) or not embedding:
                raise ValueError(f"Line {line_number} is missing a non-empty embedding array")
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
    return [value / length for value in vector]


def cosine_similarity(left, right):
    if len(left) != len(right):
        raise ValueError(f"Vector dimensions do not match: {len(left)} != {len(right)}")

    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def search(records, query, top_k):
    dim = len(records[0]["embedding"])
    query_embedding = offline_embedding(query, dim)

    scored = []
    for record in records:
        score = cosine_similarity(query_embedding, record["embedding"])
        scored.append(
            {
                "chunk_id": record.get("chunk_id"),
                "source": record.get("source"),
                "start_char": record.get("start_char"),
                "end_char": record.get("end_char"),
                "score": round(score, 6),
                "text": record.get("text", ""),
            }
        )

    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:top_k]


def write_results(path, query, top_k, results):
    payload = {
        "query": query,
        "top_k": top_k,
        "results": results,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def print_results(results):
    for index, result in enumerate(results, start=1):
        print(f"{index}. {result['chunk_id']} score={result['score']} source={result['source']}")
        print(result["text"])
        print()


def parse_args():
    parser = argparse.ArgumentParser(description="Search local embedding JSONL with cosine similarity.")
    parser.add_argument("query", help="Question or search query")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Path to embeddings.jsonl")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Path to write search results JSON")
    parser.add_argument("--top-k", type=int, default=3, help="Number of chunks to return")
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")
    if args.top_k <= 0:
        raise SystemExit("--top-k must be greater than 0")

    records = read_jsonl(input_path)
    results = search(records, args.query, min(args.top_k, len(records)))
    write_results(output_path, args.query, args.top_k, results)

    print(f"Query: {args.query}")
    print(f"Loaded records: {len(records)}")
    print(f"Saved results: {output_path}")
    print()
    print_results(results)


if __name__ == "__main__":
    main()
