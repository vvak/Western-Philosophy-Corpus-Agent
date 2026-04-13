#!/usr/bin/env python3
"""Count tokens for normalized corpus JSONL records.

The default backend uses the target Gemma 4 Hugging Face AutoProcessor. A
simple regex tokenizer is available only when explicitly requested for rough
local smoke tests.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable


DEFAULT_INPUT = Path("corpus/normalized/jsonl/gutenberg.jsonl")
DEFAULT_OUTPUT = Path("corpus/reports/token_counts.jsonl")
DEFAULT_PARQUET_OUTPUT = Path("corpus/reports/token_counts.parquet")
DEFAULT_SUMMARY_OUTPUT = Path("corpus/reports/token_counts_summary.json")
DEFAULT_BACKEND = "huggingface_auto_processor"
DEFAULT_TARGET_FAMILY = "gemma4"
DEFAULT_MODEL_ID = "google/gemma-4-E2B-it"
DEFAULT_TIKTOKEN_ENCODING = "cl100k_base"
TOKEN_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)
REGEX_TOKENIZER_VERSION = "1"


@dataclass(frozen=True)
class TokenCounter:
    target_family: str | None
    backend: str
    tokenizer: str
    tokenizer_version: str | None
    model_id: str | None
    processor_revision: str | None
    context_length: int | None
    add_special_tokens: bool
    plain_text_tokenization: bool
    chat_template_applied: bool
    enable_thinking: bool | None
    count_tokens: Callable[[str], int]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Count tokens for normalized JSONL documents.")
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Normalized JSONL input path. Default: {DEFAULT_INPUT}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"JSONL output path. Default: {DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "--parquet-output",
        type=Path,
        default=DEFAULT_PARQUET_OUTPUT,
        help=f"Optional parquet output path. Default: {DEFAULT_PARQUET_OUTPUT}",
    )
    parser.add_argument(
        "--tokenizer",
        default=DEFAULT_TIKTOKEN_ENCODING,
        help=f"tiktoken encoding name when --backend tiktoken is used. Default: {DEFAULT_TIKTOKEN_ENCODING}",
    )
    parser.add_argument(
        "--backend",
        choices=("huggingface_auto_processor", "tiktoken", "regex"),
        default=DEFAULT_BACKEND,
        help=(
            "Tokenizer backend. Gemma 4 AutoProcessor is the default target backend; "
            "use regex only for rough estimates. Default: huggingface_auto_processor"
        ),
    )
    parser.add_argument(
        "--target-family",
        default=DEFAULT_TARGET_FAMILY,
        help=f"Target model family metadata for AutoProcessor counts. Default: {DEFAULT_TARGET_FAMILY}",
    )
    parser.add_argument(
        "--model-id",
        default=DEFAULT_MODEL_ID,
        help=f"Hugging Face model id for AutoProcessor counts. Default: {DEFAULT_MODEL_ID}",
    )
    parser.add_argument(
        "--revision",
        default=None,
        help="Optional Hugging Face model revision to load and record.",
    )
    parser.add_argument(
        "--context-length",
        type=int,
        default=None,
        help="Optional context-length assumption to record. Defaults to tokenizer.model_max_length when sensible.",
    )
    parser.add_argument(
        "--local-files-only",
        action="store_true",
        help="Load the Hugging Face AutoProcessor from local cache only.",
    )
    parser.add_argument(
        "--trust-remote-code",
        action="store_true",
        help="Pass trust_remote_code=True to AutoProcessor.from_pretrained.",
    )
    parser.add_argument(
        "--write-parquet",
        action="store_true",
        help="Also write parquet output. Requires pyarrow.",
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=DEFAULT_SUMMARY_OUTPUT,
        help=f"Aggregate summary JSON output path. Default: {DEFAULT_SUMMARY_OUTPUT}",
    )
    parser.add_argument(
        "--no-summary",
        action="store_true",
        help="Do not write aggregate summary JSON.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Count only the first N records, useful for smoke tests.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate input and tokenizer setup without writing reports.",
    )
    return parser.parse_args()


def iter_jsonl(path: Path, limit: int | None = None) -> Iterable[dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"Input JSONL does not exist: {path}")

    yielded = 0
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if limit is not None and yielded >= limit:
                return
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
                yielded += 1
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_number}: invalid JSON: {exc}") from exc


def load_counter(args: argparse.Namespace) -> TokenCounter:
    if args.backend == "regex":
        return TokenCounter(
            target_family=None,
            backend="regex",
            tokenizer="regex_word_punct_v1",
            tokenizer_version=REGEX_TOKENIZER_VERSION,
            model_id=None,
            processor_revision=None,
            context_length=args.context_length,
            add_special_tokens=False,
            plain_text_tokenization=True,
            chat_template_applied=False,
            enable_thinking=None,
            count_tokens=lambda text: len(TOKEN_RE.findall(text)),
        )

    if args.backend == "huggingface_auto_processor":
        return load_huggingface_auto_processor_counter(args)

    try:
        import tiktoken  # type: ignore
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "tiktoken is not installed. Install it to use --backend tiktoken, "
            "or rerun with --backend regex for rough estimates only."
        ) from exc

    try:
        encoding = tiktoken.get_encoding(args.tokenizer)
    except Exception as exc:
        raise SystemExit(f"Unable to load tiktoken encoding {args.tokenizer!r}: {exc}") from exc

    tokenizer_name = f"tiktoken:{args.tokenizer}"
    tokenizer_version = importlib.metadata.version("tiktoken")
    return TokenCounter(
        target_family=None,
        backend="tiktoken",
        tokenizer=tokenizer_name,
        tokenizer_version=tokenizer_version,
        model_id=None,
        processor_revision=None,
        context_length=args.context_length,
        add_special_tokens=False,
        plain_text_tokenization=True,
        chat_template_applied=False,
        enable_thinking=None,
        count_tokens=lambda text: len(encoding.encode(text)),
    )


def load_huggingface_auto_processor_counter(args: argparse.Namespace) -> TokenCounter:
    try:
        from transformers import AutoProcessor  # type: ignore
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "transformers is not installed. Install transformers to count Gemma 4 "
            "AutoProcessor tokens, or rerun with --backend regex for rough smoke tests only."
        ) from exc

    kwargs: dict[str, Any] = {"local_files_only": args.local_files_only}
    if args.revision:
        kwargs["revision"] = args.revision
    if args.trust_remote_code:
        kwargs["trust_remote_code"] = True

    processor = None
    tokenizer = None
    processor_load_error: Exception | None = None

    try:
        processor = AutoProcessor.from_pretrained(args.model_id, **kwargs)
        tokenizer = getattr(processor, "tokenizer", None)
    except Exception as exc:
        processor_load_error = exc

    if tokenizer is None:
        # AutoProcessor failed or did not expose a tokenizer (typically because
        # PyTorch or Torchvision is missing). Fall back to AutoTokenizer, which
        # only requires the transformers library.
        try:
            from transformers import AutoTokenizer  # type: ignore

            tokenizer = AutoTokenizer.from_pretrained(args.model_id, **kwargs)
            if processor_load_error:
                print(
                    f"Warning: AutoProcessor failed ({processor_load_error!r}); "
                    "fell back to AutoTokenizer. Token counts are equivalent for "
                    "plain-text tokenization.",
                    file=__import__("sys").stderr,
                )
        except Exception as exc2:
            raise SystemExit(
                f"Unable to load AutoProcessor for {args.model_id!r}: {processor_load_error}\n"
                f"Unable to load AutoTokenizer fallback: {exc2}\n"
                "Ensure transformers is installed and the model is cached locally."
            ) from exc2

    context_length = resolve_context_length(tokenizer, args.context_length)
    processor_revision = resolve_processor_revision(processor or tokenizer, tokenizer, args.revision)
    tokenizer_version = package_version("transformers")
    tokenizer_name = f"huggingface_auto_processor:{args.model_id}"

    def count_tokens(text: str) -> int:
        encoded = tokenizer(text, add_special_tokens=False)
        try:
            input_ids = encoded["input_ids"]
        except (KeyError, TypeError):
            input_ids = getattr(encoded, "input_ids", None)
        if input_ids is None:
            raise RuntimeError("Tokenizer output did not include input_ids.")
        if input_ids and isinstance(input_ids[0], list):
            return len(input_ids[0])
        return len(input_ids)

    return TokenCounter(
        target_family=args.target_family,
        backend="huggingface_auto_processor",
        tokenizer=tokenizer_name,
        tokenizer_version=tokenizer_version,
        model_id=args.model_id,
        processor_revision=processor_revision,
        context_length=context_length,
        add_special_tokens=False,
        plain_text_tokenization=True,
        chat_template_applied=False,
        enable_thinking=None,
        count_tokens=count_tokens,
    )


def resolve_context_length(tokenizer: Any, explicit_context_length: int | None) -> int | None:
    if explicit_context_length is not None:
        if explicit_context_length <= 0:
            raise SystemExit("--context-length must be positive")
        return explicit_context_length

    value = getattr(tokenizer, "model_max_length", None)
    if isinstance(value, int) and 0 < value < 1_000_000_000:
        return value
    return None


def resolve_processor_revision(processor: Any, tokenizer: Any, requested_revision: str | None) -> str | None:
    for obj in (tokenizer, processor):
        init_kwargs = getattr(obj, "init_kwargs", None)
        if isinstance(init_kwargs, dict):
            for key in ("_commit_hash", "revision"):
                value = init_kwargs.get(key)
                if value:
                    return str(value)
        for attr in ("_commit_hash", "_revision", "revision"):
            value = getattr(obj, attr, None)
            if value:
                return str(value)
    return requested_revision


def package_version(package_name: str) -> str | None:
    try:
        return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        return None


def build_count_record(
    doc: dict[str, Any],
    counter: TokenCounter,
    token_count: int,
    counted_at_utc: str,
) -> dict[str, Any]:
    return {
        "doc_id": doc.get("doc_id"),
        "work_id": doc.get("work_id"),
        "version_id": doc.get("version_id"),
        "author": doc.get("author"),
        "title": doc.get("title"),
        "period": doc.get("period"),
        "language": doc.get("language"),
        "source": doc.get("source"),
        "quality_tier": doc.get("quality_tier"),
        "target_family": counter.target_family,
        "backend": counter.backend,
        "model_id": counter.model_id,
        "tokenizer": counter.tokenizer,
        "tokenizer_version": counter.tokenizer_version,
        "processor_revision": counter.processor_revision,
        "context_length": counter.context_length,
        "add_special_tokens": counter.add_special_tokens,
        "plain_text_tokenization": counter.plain_text_tokenization,
        "chat_template_applied": counter.chat_template_applied,
        "enable_thinking": counter.enable_thinking,
        "token_count": token_count,
        "char_count": len(doc.get("text", "")),
        "counted_at_utc": counted_at_utc,
    }


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    temp_path.replace(path)


def write_parquet(path: Path, records: list[dict[str, Any]]) -> None:
    try:
        import pyarrow as pa  # type: ignore
        import pyarrow.parquet as pq  # type: ignore
    except ModuleNotFoundError as exc:
        raise SystemExit("pyarrow is required for --write-parquet output.") from exc

    path.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pylist(records)
    pq.write_table(table, path)


def write_summary(path: Path, summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp_path.replace(path)


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    by_author = Counter()
    by_period = Counter()
    by_language = Counter()
    by_source = Counter()
    by_quality_tier = Counter()
    by_work = Counter()
    total = 0

    for record in records:
        token_count = int(record["token_count"])
        total += token_count
        by_author[record.get("author")] += token_count
        by_period[record.get("period")] += token_count
        by_language[record.get("language")] += token_count
        by_source[record.get("source")] += token_count
        by_quality_tier[record.get("quality_tier")] += token_count
        by_work[record.get("work_id")] += token_count

    return {
        "documents": len(records),
        "total_tokens": total,
        "tokenization": tokenization_summary(records),
        "by_author": dict(by_author),
        "by_period": dict(by_period),
        "by_language": dict(by_language),
        "by_source": dict(by_source),
        "by_quality_tier": dict(by_quality_tier),
        "top_10_works": by_work.most_common(10),
    }


def tokenization_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not records:
        return {}
    first = records[0]
    fields = (
        "target_family",
        "backend",
        "model_id",
        "tokenizer",
        "tokenizer_version",
        "processor_revision",
        "context_length",
        "add_special_tokens",
        "plain_text_tokenization",
        "chat_template_applied",
        "enable_thinking",
    )
    return {field: first.get(field) for field in fields}


def main() -> int:
    args = parse_args()
    if args.limit is not None and args.limit < 0:
        raise SystemExit("--limit must be non-negative")
    if args.context_length is not None and args.context_length <= 0:
        raise SystemExit("--context-length must be positive")

    counter = load_counter(args)
    docs = list(iter_jsonl(args.input, args.limit))

    if args.dry_run:
        print("Dry run only; no token reports will be written.")
        print(f"Input: {args.input}")
        print(f"Records selected: {len(docs)}")
        print(f"Backend: {counter.backend}")
        print(f"Target family: {counter.target_family}")
        print(f"Model id: {counter.model_id}")
        print(f"Tokenizer: {counter.tokenizer} ({counter.tokenizer_version})")
        print(f"Processor revision: {counter.processor_revision}")
        print(f"Context length: {counter.context_length}")
        print("Plain-text tokenization: True; add_special_tokens=False; chat_template_applied=False")
        return 0

    counted_at_utc = datetime.now(timezone.utc).isoformat()
    records = [
        build_count_record(
            doc,
            counter,
            counter.count_tokens(doc.get("text", "")),
            counted_at_utc,
        )
        for doc in docs
    ]
    write_jsonl(args.output, records)
    if args.write_parquet:
        write_parquet(args.parquet_output, records)

    summary = summarize(records)
    if not args.no_summary:
        write_summary(args.summary_output, summary)

    print(f"Wrote {summary['documents']} token count records to {args.output}.")
    print(f"Backend: {counter.backend}")
    print(f"Target family: {counter.target_family}")
    print(f"Model id: {counter.model_id}")
    print(f"Tokenizer: {counter.tokenizer} ({counter.tokenizer_version})")
    print(f"Total tokens: {summary['total_tokens']}")
    if not args.no_summary:
        print(f"Wrote summary report to {args.summary_output}.")
    if args.write_parquet:
        print(f"Wrote parquet report to {args.parquet_output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
