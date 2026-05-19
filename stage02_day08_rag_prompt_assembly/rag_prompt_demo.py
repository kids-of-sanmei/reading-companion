import argparse
import json
from pathlib import Path


DEFAULT_INPUT = Path("../stage02_day07_vector_search/search_results.json")
DEFAULT_MD_OUTPUT = Path("assembled_prompt.md")
DEFAULT_JSON_OUTPUT = Path("rag_prompt_payload.json")


SYSTEM_PROMPT = """你是一个基于资料回答问题的 RAG 助手。
回答必须遵守：
1. 只基于提供的 context 回答。
2. 如果 context 中没有足够信息，明确说“资料不足，无法确定”。
3. 回答后列出使用到的引用编号。
4. 不要编造 context 之外的事实。"""


def load_search_results(path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    if "results" not in payload or not isinstance(payload["results"], list):
        raise ValueError("search_results.json must contain a results array")
    return payload


def build_context_blocks(results):
    blocks = []
    for index, result in enumerate(results, start=1):
        blocks.append(
            {
                "ref": f"[{index}]",
                "chunk_id": result.get("chunk_id"),
                "source": result.get("source"),
                "score": result.get("score"),
                "text": result.get("text", ""),
            }
        )
    return blocks


def render_context(blocks):
    rendered = []
    for block in blocks:
        rendered.append(
            "\n".join(
                [
                    f"{block['ref']} chunk_id={block['chunk_id']} source={block['source']} score={block['score']}",
                    block["text"],
                ]
            )
        )
    return "\n\n".join(rendered)


def build_payload(query, blocks):
    context_text = render_context(blocks)
    user_prompt = f"""请根据以下 context 回答问题。

## Context

{context_text}

## Question

{query}"""
    return {
        "system": SYSTEM_PROMPT,
        "user": user_prompt,
        "context_blocks": blocks,
        "question": query,
    }


def write_markdown(path, payload):
    content = "\n\n".join(
        [
            "# Assembled RAG Prompt",
            "## System",
            payload["system"],
            "## User",
            payload["user"],
        ]
    )
    path.write_text(content, encoding="utf-8")


def write_json(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args():
    parser = argparse.ArgumentParser(description="Assemble a RAG prompt from vector search results.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Path to search_results.json")
    parser.add_argument("--md-output", default=str(DEFAULT_MD_OUTPUT), help="Markdown prompt output path")
    parser.add_argument("--json-output", default=str(DEFAULT_JSON_OUTPUT), help="JSON prompt payload output path")
    parser.add_argument("--query", default=None, help="Override query from search_results.json")
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    search_payload = load_search_results(input_path)
    query = args.query or search_payload.get("query")
    if not query:
        raise SystemExit("No query provided and input file has no query field.")

    blocks = build_context_blocks(search_payload["results"])
    payload = build_payload(query, blocks)
    write_markdown(Path(args.md_output), payload)
    write_json(Path(args.json_output), payload)

    print(f"Context blocks: {len(blocks)}")
    print(f"Question: {query}")
    print(f"Wrote markdown: {args.md_output}")
    print(f"Wrote json: {args.json_output}")


if __name__ == "__main__":
    main()
