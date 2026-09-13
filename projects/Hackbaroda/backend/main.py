"""
Instagram Content Scraper + Strategy Agent.

Usage:
  python main.py trend --count 50 --country "United States"
  python main.py hashtag fitness --type top --count 50
  python main.py suggest --count 100 --top 15
  python main.py strategy --input output/suggestions_xxx.json --top 5 --weeks 2
  python main.py strategy --count 30 --top 5 --niche fitness --weeks 2
  python main.py run --niche music --hashtags kpop reels --count 30 --top 5 --weeks 2
"""

import argparse
import sys

# Fix Windows terminal unicode output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.agent.pipeline import run_full_pipeline, run_strategy_pipeline
from src.models.pipeline import PipelineInput
from src.analyzer.content_ranker import generate_suggestions, rank_content
from src.scrapers.hashtag import scrape_hashtag
from src.scrapers.trending import scrape_trending
from src.utils import (
    items_to_dict,
    save_json,
    strategy_to_dict,
    suggestions_to_dict,
    timestamped_name,
)

console = Console(legacy_windows=False)


def display_suggestions(suggestions):
    for s in suggestions:
        item = s.item
        content_type = "Reel" if item.is_video else item.content_type.title()

        panel_text = (
            f"[bold]@{item.username}[/bold] | {content_type} | Score: {item.viral_score:,.0f}\n"
            f"[dim]{item.url}[/dim]\n\n"
            f"[yellow]Why trending:[/yellow] {s.why_trending}\n\n"
            f"[green]Likes:[/green] {item.likes:,}  "
            f"[green]Comments:[/green] {item.comments:,}  "
            f"[green]Plays:[/green] {item.plays:,}\n"
        )

        if item.section:
            panel_text += f"[cyan]Category:[/cyan] {item.section}"
            if item.topic:
                panel_text += f" -> {item.topic}"
            panel_text += "\n"

        if item.caption:
            caption_preview = item.caption[:200]
            if len(item.caption) > 200:
                caption_preview += "..."
            panel_text += f"\n[white]{caption_preview}[/white]\n"

        if s.content_ideas:
            panel_text += "\n[bold magenta]Content ideas:[/bold magenta]\n"
            for idea in s.content_ideas:
                panel_text += f"  - {idea}\n"

        console.print(Panel(panel_text, title=f"#{s.rank} Top Content", border_style="bright_blue"))


def display_table(items, title="Scraped Content"):
    table = Table(title=title)
    table.add_column("Rank", style="cyan", width=5)
    table.add_column("User", style="bold")
    table.add_column("Type", width=8)
    table.add_column("Likes", justify="right")
    table.add_column("Comments", justify="right")
    table.add_column("Plays", justify="right")
    table.add_column("Score", justify="right", style="green")

    for i, item in enumerate(items, 1):
        content_type = "Reel" if item.is_video else item.content_type[:8]
        table.add_row(
            str(i),
            f"@{item.username}",
            content_type,
            f"{item.likes:,}",
            f"{item.comments:,}",
            f"{item.plays:,}",
            f"{item.viral_score:,.0f}",
        )

    console.print(table)


def display_strategy_summary(report):
    console.print(Panel(
        report.executive_summary,
        title="Executive Summary",
        border_style="green",
    ))

    console.print("\n[bold cyan]Niche Detected:[/bold cyan]", report.niche_detected)
    console.print("[bold cyan]Top Formats:[/bold cyan]", ", ".join(report.top_performing_formats))

    console.print("\n[bold yellow]Winning Hooks:[/bold yellow]")
    for hook in report.winning_hooks[:5]:
        console.print(f"  [bold]{hook.pattern}[/bold]")
        console.print(f"    Example: {hook.example_from_scrape}")
        console.print(f"    Why: {hook.why_it_works}")

    console.print("\n[bold magenta]Why Content Goes Viral:[/bold magenta]")
    for reason in report.why_content_goes_viral[:5]:
        console.print(f"  - {reason}")

    console.print("\n[bold green]Content Pillars:[/bold green]")
    for pillar in report.content_pillars:
        console.print(f"  - {pillar}")

    console.print(f"\n[bold]Weekly Plan:[/bold] {len(report.weekly_plan)} days")
    for day in report.weekly_plan[:7]:
        console.print(
            f"  Day {day.day_number} ({day.day}): [{day.content_type}] {day.topic}\n"
            f"    Hook: {day.hook[:100]}{'...' if len(day.hook) > 100 else ''}"
        )
    if len(report.weekly_plan) > 7:
        console.print(f"  ... and {len(report.weekly_plan) - 7} more days in the JSON file")

    console.print("\n[bold]Top Post Analyses:[/bold]")
    for analysis in report.per_post_analyses[:3]:
        made = analysis.how_it_was_made
        hook = analysis.hook_analysis
        if len(made) > 300:
            made = made[:300] + "..."
        if len(hook) > 200:
            hook = hook[:200] + "..."
        console.print(Panel(
            f"[bold]@{analysis.username}[/bold] | {analysis.format_label}\n"
            f"{analysis.url}\n\n"
            f"[yellow]How it was made:[/yellow]\n{made}\n\n"
            f"[yellow]Hook:[/yellow] {hook}",
            title=f"#{analysis.rank} Deep Analysis",
            border_style="blue",
        ))


def cmd_trend(args):
    items = scrape_trending(
        max_results=args.count,
        country=args.country,
    )
    ranked = rank_content(items)

    filepath = save_json(items_to_dict(ranked), timestamped_name("trending"))
    console.print(f"[green]Saved {len(ranked)} items to {filepath}[/green]\n")
    display_table(ranked[:args.top], "Trending Instagram Content")


def cmd_hashtag(args):
    items = scrape_hashtag(
        hashtag=args.hashtag,
        scrape_type=args.type,
        max_items=args.count,
    )
    ranked = rank_content(items)

    filepath = save_json(items_to_dict(ranked), timestamped_name(f"hashtag_{args.hashtag}"))
    console.print(f"[green]Saved {len(ranked)} items to {filepath}[/green]\n")
    display_table(ranked[:args.top], f"#{args.hashtag.lstrip('#')} Top Posts")


def cmd_suggest(args):
    all_items = []

    console.print("[bold]Fetching Instagram Explore trending content...[/bold]")
    trending = scrape_trending(max_results=args.count, country=args.country)
    all_items.extend(trending)

    if args.hashtags:
        for tag in args.hashtags:
            console.print(f"[bold]Fetching top posts for #{tag}...[/bold]")
            hashtag_items = scrape_hashtag(hashtag=tag, scrape_type="top", max_items=50)
            all_items.extend(hashtag_items)

    suggestions = generate_suggestions(all_items, top_n=args.top)

    filepath = save_json(suggestions_to_dict(suggestions), timestamped_name("suggestions"))
    console.print(f"[green]Saved {len(suggestions)} suggestions to {filepath}[/green]\n")
    display_suggestions(suggestions)


def cmd_run(args):
    """Full end-to-end pipeline: scrape -> rank -> analyze -> strategy."""
    console.print("[bold]Starting Full Content Pipeline...[/bold]\n")

    config = PipelineInput(
        niche=args.niche,
        country=args.country,
        hashtags=args.hashtags or [],
        scrape_count=args.count,
        hashtag_scrape_count=args.hashtag_count,
        top_n=args.top,
        weeks=args.weeks,
        use_vision=not args.no_vision,
        save_outputs=not args.no_save,
    )

    result = run_full_pipeline(config)

    console.print(f"\n[green]Pipeline complete in {result.elapsed_seconds}s[/green]")
    console.print(f"[green]Scraped {result.scraped_count} posts, analyzed top {len(result.suggestions)}[/green]\n")

    if result.output_files:
        console.print("[bold]Output files:[/bold]")
        for key, path in result.output_files.items():
            console.print(f"  {key}: {path}")

    if result.strategy_report:
        try:
            console.print()
            display_strategy_summary(result.strategy_report)
        except UnicodeEncodeError:
            console.print("[yellow]Summary display skipped (terminal encoding). See JSON output files.[/yellow]")


def cmd_strategy(args):
    console.print("[bold]Starting Content Strategy Agent...[/bold]\n")

    report = run_strategy_pipeline(
        input_file=args.input,
        count=args.count,
        country=args.country,
        hashtags=args.hashtags,
        top_n=args.top,
        weeks=args.weeks,
        niche=args.niche,
        use_vision=not args.no_vision,
    )

    filepath = save_json(strategy_to_dict(report), timestamped_name("strategy"))
    console.print(f"\n[green]Saved full strategy report to {filepath}[/green]\n")
    display_strategy_summary(report)


def main():
    parser = argparse.ArgumentParser(
        description="Instagram Content Scraper — find top & trending content via Apify"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # trend command
    trend_parser = subparsers.add_parser("trend", help="Scrape Instagram Explore trending feed")
    trend_parser.add_argument("--count", type=int, default=50, help="Number of posts to scrape")
    trend_parser.add_argument("--country", default="United States", help="Target country for Explore")
    trend_parser.add_argument("--top", type=int, default=20, help="Show top N ranked results")
    trend_parser.set_defaults(func=cmd_trend)

    # hashtag command
    hashtag_parser = subparsers.add_parser("hashtag", help="Scrape top posts from a hashtag")
    hashtag_parser.add_argument("hashtag", help="Hashtag to scrape (without #)")
    hashtag_parser.add_argument("--type", choices=["top", "recent"], default="top", help="Feed type")
    hashtag_parser.add_argument("--count", type=int, default=50, help="Max posts to scrape")
    hashtag_parser.add_argument("--top", type=int, default=20, help="Show top N ranked results")
    hashtag_parser.set_defaults(func=cmd_hashtag)

    # suggest command
    suggest_parser = subparsers.add_parser("suggest", help="Get top content suggestions with ideas")
    suggest_parser.add_argument("--count", type=int, default=100, help="Trending posts to scrape")
    suggest_parser.add_argument("--country", default="United States", help="Target country")
    suggest_parser.add_argument("--hashtags", nargs="*", help="Extra hashtags to include")
    suggest_parser.add_argument("--top", type=int, default=10, help="Number of suggestions")
    suggest_parser.set_defaults(func=cmd_suggest)

    # strategy command
    strategy_parser = subparsers.add_parser(
        "strategy",
        help="AI content strategy agent: analyze posts/reels and build a weekly plan",
    )
    strategy_parser.add_argument(
        "--input", "-i",
        help="Use existing scraped JSON (suggestions or trending file from output/)",
    )
    strategy_parser.add_argument("--count", type=int, default=50, help="Posts to scrape if no --input")
    strategy_parser.add_argument("--country", default="United States")
    strategy_parser.add_argument("--hashtags", nargs="*", help="Extra hashtags to scrape")
    strategy_parser.add_argument("--top", type=int, default=5, help="Top posts to deep-analyze")
    strategy_parser.add_argument("--weeks", type=int, default=2, help="Weeks of content plan (1 or 2)")
    strategy_parser.add_argument("--niche", help="Your niche for personalized strategy")
    strategy_parser.add_argument("--no-vision", action="store_true", help="Skip thumbnail image analysis")
    strategy_parser.set_defaults(func=cmd_strategy)

    # run command — full pipeline (main entry point for frontend)
    run_parser = subparsers.add_parser(
        "run",
        help="Full pipeline: scrape -> rank -> analyze -> strategy (all at once)",
    )
    run_parser.add_argument("--niche", help="Your content niche e.g. fitness, music, travel")
    run_parser.add_argument("--country", default="United States")
    run_parser.add_argument("--hashtags", nargs="*", help="Hashtags to scrape top posts from")
    run_parser.add_argument("--count", type=int, default=50, help="Trending posts to scrape")
    run_parser.add_argument("--hashtag-count", type=int, default=50, help="Posts per hashtag")
    run_parser.add_argument("--top", type=int, default=5, help="Top posts to deep-analyze")
    run_parser.add_argument("--weeks", type=int, default=2, choices=[1, 2])
    run_parser.add_argument("--no-vision", action="store_true")
    run_parser.add_argument("--no-save", action="store_true", help="Skip saving JSON files")
    run_parser.set_defaults(func=cmd_run)

    args = parser.parse_args()

    try:
        args.func(args)
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled.[/yellow]")
        sys.exit(0)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        err = str(e)
        if "invalid_api_key" in err or "Incorrect API key" in err:
            console.print("[red]OpenAI API key is invalid. Update OPENAI_API_KEY in .env[/red]")
            console.print("Get a new key: https://platform.openai.com/api-keys")
        else:
            console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
