"""Full end-to-end pipeline: scrape -> rank -> analyze -> strategy."""

import time
from pathlib import Path

from src.agent.content_analyzer import analyze_post
from src.agent.strategy_agent import generate_strategy_report
from src.analyzer.content_ranker import generate_suggestions
from src.models.content import ContentItem, ContentSuggestion
from src.models.pipeline import PipelineInput, PipelineProgress, PipelineResult
from src.models.strategy import ContentStrategyReport
from src.scrapers.hashtag import scrape_hashtag
from src.scrapers.trending import scrape_trending
from src.utils import (
    items_to_dict,
    load_scraped_content,
    save_json,
    strategy_to_dict,
    suggestions_to_dict,
    timestamped_name,
)


def _items_from_suggestions(suggestions: list[ContentSuggestion]) -> list[ContentItem]:
    return [s.item for s in suggestions]


class PipelineRunner:
    """Orchestrates the complete content strategy workflow."""

    def __init__(self, config: PipelineInput):
        self.config = config
        self.progress_log: list[PipelineProgress] = []
        self._on_progress = None

    def _log(self, stage: str, detail: str = ""):
        entry = PipelineProgress(stage=stage, detail=detail)
        self.progress_log.append(entry)
        if self._on_progress:
            self._on_progress(stage, detail)
        else:
            print(f"[{stage}] {detail}" if detail else f"[{stage}]")

    def _scrape(self) -> list[ContentItem]:
        cfg = self.config
        all_items: list[ContentItem] = []

        self._log("scrape", f"Scraping {cfg.scrape_count} trending posts ({cfg.country})...")
        trending = scrape_trending(max_results=cfg.scrape_count, country=cfg.country)
        all_items.extend(trending)
        self._log("scrape", f"Got {len(trending)} trending posts")

        for tag in cfg.hashtags:
            clean = tag.lstrip("#").strip()
            self._log("scrape", f"Scraping #{clean} top posts...")
            hashtag_items = scrape_hashtag(
                hashtag=clean,
                scrape_type="top",
                max_items=cfg.hashtag_scrape_count,
            )
            all_items.extend(hashtag_items)
            self._log("scrape", f"Got {len(hashtag_items)} posts from #{clean}")

        return all_items

    def _rank(self, items: list[ContentItem]) -> list[ContentSuggestion]:
        self._log("rank", f"Ranking top {self.config.top_n} by viral score...")
        suggestions = generate_suggestions(items, top_n=self.config.top_n)
        self._log("rank", f"Ranked {len(suggestions)} top content pieces")
        return suggestions

    def _analyze(self, suggestions: list[ContentSuggestion]):
        analyses = []
        for i, suggestion in enumerate(suggestions, start=1):
            item = suggestion.item
            label = "Reel" if item.is_video else "Post"
            self._log("analyze", f"Deep-analyzing {label} #{i} @{item.username}...")
            analysis = analyze_post(item, rank=i, use_vision=self.config.use_vision)
            analyses.append(analysis)
        return analyses

    def _build_strategy(
        self,
        analyses,
        all_items: list[ContentItem],
    ) -> ContentStrategyReport:
        self._log("strategy", f"Building {self.config.weeks}-week content plan...")
        report = generate_strategy_report(
            analyses=analyses,
            all_items=all_items,
            weeks=self.config.weeks,
            niche=self.config.niche,
        )
        self._log("strategy", "Content strategy report ready")
        return report

    def _save_outputs(
        self,
        all_items: list[ContentItem],
        suggestions: list[ContentSuggestion],
        report: ContentStrategyReport,
    ) -> dict[str, str]:
        files = {}
        prefix = (self.config.niche or "content").replace(" ", "_").lower()

        scraped_path = save_json(
            items_to_dict(all_items),
            timestamped_name(f"scraped_{prefix}"),
        )
        files["scraped"] = str(scraped_path)

        suggestions_path = save_json(
            suggestions_to_dict(suggestions),
            timestamped_name(f"suggestions_{prefix}"),
        )
        files["suggestions"] = str(suggestions_path)

        strategy_path = save_json(
            strategy_to_dict(report),
            timestamped_name(f"strategy_{prefix}"),
        )
        files["strategy"] = str(strategy_path)

        return files

    def run(self, *, on_progress=None) -> PipelineResult:
        """Execute the full pipeline from scrape to strategy."""
        self._on_progress = on_progress
        start = time.time()
        cfg = self.config

        # Stage 1: Scrape
        all_items = self._scrape()
        if not all_items:
            raise ValueError("Scraping returned no content. Try different inputs.")

        # Stage 2: Rank & suggest
        suggestions = self._rank(all_items)
        if not suggestions:
            raise ValueError("No content ranked. Check scrape results.")

        # Stage 3: Deep-analyze top posts/reels
        analyses = self._analyze(suggestions)

        # Stage 4: Build full strategy
        report = self._build_strategy(analyses, all_items)

        # Stage 5: Save outputs
        output_files = {}
        if cfg.save_outputs:
            self._log("save", "Saving output files...")
            output_files = self._save_outputs(all_items, suggestions, report)

        self._log("done", "Pipeline complete")

        return PipelineResult(
            status="completed",
            input=cfg,
            progress_log=self.progress_log,
            scraped_count=len(all_items),
            suggestions=suggestions,
            strategy_report=report,
            output_files=output_files,
            elapsed_seconds=round(time.time() - start, 1),
        )


def run_full_pipeline(
    config: PipelineInput,
    *,
    on_progress=None,
) -> PipelineResult:
    """Run scrape -> rank -> analyze -> strategy in one call."""
    return PipelineRunner(config).run(on_progress=on_progress)


def run_strategy_pipeline(
    *,
    input_file: str | Path | None = None,
    count: int = 50,
    country: str = "United States",
    hashtags: list[str] | None = None,
    top_n: int = 5,
    weeks: int = 2,
    niche: str | None = None,
    use_vision: bool = True,
    on_progress=None,
) -> ContentStrategyReport:
    """Backward-compatible wrapper around the full pipeline."""
    if input_file:
        suggestions = load_scraped_content(input_file)
        all_items = _items_from_suggestions(suggestions)
        top_items = all_items[:top_n]

        def log(stage, detail=""):
            if on_progress:
                on_progress(stage, detail)
            else:
                print(f"[{stage}] {detail}" if detail else f"[{stage}]")

        analyses = []
        for i, item in enumerate(top_items, start=1):
            label = "Reel" if item.is_video else "Post"
            log("analyze", f"Analyzing {label} #{i} @{item.username}...")
            analyses.append(analyze_post(item, rank=i, use_vision=use_vision))

        log("strategy", f"Building {weeks}-week content strategy...")
        return generate_strategy_report(
            analyses=analyses,
            all_items=all_items,
            weeks=weeks,
            niche=niche,
        )

    result = run_full_pipeline(
        PipelineInput(
            niche=niche,
            country=country,
            hashtags=hashtags or [],
            scrape_count=count,
            top_n=top_n,
            weeks=weeks,
            use_vision=use_vision,
            save_outputs=False,
        ),
        on_progress=on_progress,
    )
    return result.strategy_report
