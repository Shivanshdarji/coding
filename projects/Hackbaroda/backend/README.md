# Instagram Content Scraper + Strategy Agent

Scrape **top & trending Instagram content** using Apify, then use **OpenAI** to deeply analyze every post/reel and generate a complete 1-2 week content strategy.

## What it does

- **Trending feed** — Pulls posts from Instagram's Explore page (what's trending right now)
- **Hashtag top posts** — Scrapes the best-performing posts for any hashtag
- **Content suggestions** — Ranks content by viral score and gives you ideas to recreate trending formats
- **AI deep analysis** — OpenAI reverse-engineers how each viral post/reel was made
- **Content strategy agent** — Full 1-2 week plan with hooks, scripts, captions, and posting times
- **Engagement scoring** — Weighs likes, comments, plays, recency, and format (reels get boosted)

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add your API keys

Copy `.env.example` to `.env` and add both keys:

```
APIFY_API_TOKEN=your_apify_token_here
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-4o-mini
```

- Apify token: https://console.apify.com/account/integrations
- OpenAI key: https://platform.openai.com/api-keys

## Usage

### CLI

**Scrape Instagram Explore trending content:**

```bash
python main.py trend --count 50 --country "United States"
```

**Scrape top posts from a hashtag:**

```bash
python main.py hashtag fitness --type top --count 50
```

**Get content suggestions (trending + optional hashtags):**

```bash
python main.py suggest --count 100 --top 15
python main.py suggest --hashtags fitness travel food --top 10
```

**Full pipeline — everything at once (recommended):**

```bash
python main.py run --niche music --hashtags kpop reels --count 30 --top 5 --weeks 2
```

This runs: scrape -> rank -> AI analyze each post/reel -> 2-week strategy -> saves 3 JSON files.

**Full AI content strategy (analyze + 2-week plan):**

```bash
# From existing scraped data (fastest, no extra Apify credits)
python main.py strategy --input output/suggestions_20260607_132532.json --top 5 --weeks 2

# Scrape fresh + analyze + build strategy
python main.py strategy --count 30 --top 5 --niche "fitness" --weeks 2
```

### API Server (for frontend)

```bash
uvicorn api:app --reload
```

**Main endpoint for your frontend:**

```bash
POST http://localhost:8000/pipeline
```

```json
{
  "niche": "fitness",
  "country": "United States",
  "hashtags": ["fitness", "gym"],
  "scrape_count": 50,
  "hashtag_scrape_count": 50,
  "top_n": 5,
  "weeks": 2,
  "use_vision": true,
  "save_outputs": true
}
```

Returns the complete result: scraped data, suggestions, strategy report, output file paths, and progress log.

API docs at: http://localhost:8000/docs

## Output

Results are saved to the `output/` folder as JSON.

### Strategy report (`strategy_*.json`) includes:

| Section | What you get |
|---------|-------------|
| `executive_summary` | High-level strategy overview |
| `per_post_analyses` | Full breakdown of how each viral post/reel was made |
| `winning_hooks` | Hook patterns that are working right now |
| `why_content_goes_viral` | Reasons behind viral performance |
| `weekly_plan` | Day-by-day content plan for 1-2 weeks |
| `posting_strategy` | When and how often to post |
| `content_pillars` | Themes to build your content around |
| `detailed_recommendations` | Actionable optimization tips |

### Suggestions file includes:

| Field | Description |
|-------|-------------|
| `viral_score` | Composite engagement score |
| `likes / comments / plays` | Raw engagement metrics |
| `section / topic` | Instagram Explore category labels |
| `why_trending` | Why this content is performing well |
| `content_ideas` | Actionable ideas to create similar content |

## Apify Actors Used

| Actor | Purpose | Cost |
|-------|---------|------|
| [Instagram Trending Scraper](https://apify.com/agentx/instagram-trending-scraper) | Explore feed trending | ~$4/1K results |
| [Instagram Hashtag Posts Scraper](https://apify.com/breathtaking_anthem/instagram-hashtag-posts-scraper) | Hashtag top/recent posts | ~$1.4/1K posts |

## Supported Countries

United States, Canada, UK, Australia, Germany, France, Italy, Spain, Brazil, Mexico, Japan, South Korea, India, Indonesia, UAE, Turkey, and more.

## Project Structure

```
├── main.py              # CLI entry point
├── api.py               # FastAPI server
├── src/
│   ├── scrapers/        # Apify integration (trending + hashtag)
│   ├── analyzer/        # Viral score ranking & suggestions
│   ├── agent/           # OpenAI content strategy agent
│   └── models/          # Data models
└── output/              # Scraped results + strategy reports (JSON)
```
