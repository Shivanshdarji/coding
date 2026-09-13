import json
from datetime import datetime
from pathlib import Path

from src.config import OUTPUT_DIR
from src.models.content import ContentItem, ContentSuggestion
from src.models.pipeline import PipelineResult
from src.models.strategy import ContentStrategyReport


def ensure_output_dir() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def save_json(data: list | dict, filename: str) -> Path:
    out_dir = ensure_output_dir()
    filepath = out_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str, ensure_ascii=False)
    return filepath


def items_to_dict(items: list[ContentItem]) -> list[dict]:
    return [item.model_dump() for item in items]


def suggestions_to_dict(suggestions: list[ContentSuggestion]) -> list[dict]:
    return [s.model_dump() for s in suggestions]


def timestamped_name(prefix: str) -> str:
    import re
    # Replace invalid filename characters and whitespace with underscores
    sanitized = re.sub(r'[\s<>:"/\\|?*\x00-\x1f]+', '_', prefix)
    # Collapse multiple underscores
    sanitized = re.sub(r'_{2,}', '_', sanitized)
    # Strip leading/trailing underscores and periods
    sanitized = sanitized.strip('_.')
    if not sanitized:
        sanitized = "content"
    # Truncate to a reasonable length to avoid MAX_PATH issues
    sanitized = sanitized[:100].rstrip('_')
    
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{sanitized}_{ts}.json"


def load_json_file(path: str | Path) -> list | dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_scraped_content(path: str | Path) -> list[ContentSuggestion]:
    """Load suggestions or raw trending JSON from output folder."""
    data = load_json_file(path)

    if isinstance(data, dict) and "per_post_analyses" in data:
        raise ValueError("This file is already a strategy report. Use a suggestions or trending file.")

    if isinstance(data, list) and data and "item" in data[0]:
        return [ContentSuggestion.model_validate(entry) for entry in data]

    if isinstance(data, list) and data and "url" in data[0]:
        items = [ContentItem.model_validate(entry) for entry in data]
        return [
            ContentSuggestion(rank=i, item=item, why_trending="", content_ideas=[])
            for i, item in enumerate(items, start=1)
        ]

    raise ValueError(
        f"Unrecognized format in {path}. Expected suggestions or trending JSON."
    )


def strategy_to_dict(report: ContentStrategyReport) -> dict:
    return report.model_dump(mode="json")


def pipeline_to_dict(result: PipelineResult) -> dict:
    return result.model_dump(mode="json")
