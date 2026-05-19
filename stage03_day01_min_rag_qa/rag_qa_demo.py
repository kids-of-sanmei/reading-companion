import argparse
import hashlib
import json
import math
import os
import re
from pathlib import Path


DEFAULT_INPUT = Path("../stage02_day06_embeddings/embeddings.jsonl")
DEFAULT_ANSWER = Path("answer.md")
DEFAULT_TRACE = Path("rag_trace.json")
DEFAULT_MODEL = "gpt-4.1-mini"


SYSTEM_PROMPT = """你是一个基于资料回答问题的 RAG 助手。
只能基于提供的 context 回答。
如果资料不足，明确说明资料不足。
回答必须列出引用编号。"""


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
            item = json.loads(line)
            if "embedding" not in item or "text" not in item:
                raise ValueError(f"Line {line_number} must contain embedding and text")
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


def retrieve(records, query, top_k):
    dim = len(records[0]["embedding"])
    query_embedding = offline_embedding(query, dim)
    results = []

    for record in records:
        score = cosine_similarity(query_embedding, record["embedding"])
        results.append(
            {
                "chunk_id": record.get("chunk_id"),
                "source": record.get("source"),
                "score": round(score, 6),
                "text": record["text"],
            }
        )

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k]


def build_context(results):
    blocks = []
    for index, result in enumerate(results, start=1):
        blocks.append(
            "\n".join(
                [
                    f"[{index}] chunk_id={result['chunk_id']} source={result['source']} score={result['score']}",
                    result["text"],
                ]
            )
        )
    return "\n\n".join(blocks)


def build_prompt(query, retrieved_context):
    user_prompt = f"""请根据以下 context 回答问题。

## Context

{retrieved_context}

## Question

{query}"""
    return {"system": SYSTEM_PROMPT, "user": user_prompt}


def offline_answer(query, results):
    if not results:
        return "资料不足，无法确定。\n\n引用：无"

    useful = [result for result in results if result["score"] > 0]
    if not useful:
        return "资料不足，无法确定。\n\n引用：无"

    lines = [
        f"问题：{query}",
        "",
        "基于当前检索到的资料，可以先给出一个资料内回答：",
    ]
    for index, result in enumerate(useful[:3], start=1):
        lines.append(f"- [{index}] {result['text']}")
    refs = ", ".join(f"[{index}]" for index in range(1, min(len(useful), 3) + 1))
    lines.extend(["", f"引用：{refs}"])
    return "\n".join(lines)


def api_answer(prompt, model):
    load_dotenv_if_available()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set. Use offline mode or create a .env file.")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Missing dependency: pip install openai python-dotenv") from exc

    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]},
        ],
    )
    return response.output_text


def write_outputs(answer_path, trace_path, trace):
    answer_path.write_text(trace["answer"], encoding="utf-8")
    trace_path.write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args():
    parser = argparse.ArgumentParser(description="Minimal local RAG QA demo.")
    parser.add_argument("query", help="Question to answer")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Path to embeddings.jsonl")
    parser.add_argument("--answer-output", default=str(DEFAULT_ANSWER), help="Answer markdown output")
    parser.add_argument("--trace-output", default=str(DEFAULT_TRACE), help="RAG trace JSON output")
    parser.add_argument("--top-k", type=int, default=3, help="Number of chunks to retrieve")
    parser.add_argument("--api", action="store_true", help="Use OpenAI API for answer generation")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model for --api mode")
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")
    if args.top_k <= 0:
        raise SystemExit("--top-k must be greater than 0")

    records = read_jsonl(input_path)
    retrieved = retrieve(records, args.query, min(args.top_k, len(records)))
    context = build_context(retrieved)
    prompt = build_prompt(args.query, context)
    answer = api_answer(prompt, args.model) if args.api else offline_answer(args.query, retrieved)

    trace = {
        "query": args.query,
        "top_k": args.top_k,
        "mode": "api" if args.api else "offline",
        "retrieved_context": retrieved,
        "prompt": prompt,
        "answer": answer,
    }
    write_outputs(Path(args.answer_output), Path(args.trace_output), trace)

    print(f"Query: {args.query}")
    print(f"Retrieved chunks: {len(retrieved)}")
    print(f"Mode: {trace['mode']}")
    print(f"Wrote answer: {args.answer_output}")
    print(f"Wrote trace: {args.trace_output}")


if __name__ == "__main__":
    main()
