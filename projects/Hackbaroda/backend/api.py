"""
FastAPI server for the Instagram Content Strategy Pipeline.

Run: uvicorn api:app --reload
"""

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.agent.pipeline import run_full_pipeline, run_strategy_pipeline
from src.analyzer.content_ranker import generate_suggestions, rank_content
from src.config import SUPPORTED_COUNTRIES, validate_openai_key, validate_token
from src.models.pipeline import PipelineInput
from src.agent.openai_client import generate_ad_image, get_client
from pydantic import BaseModel, Field
from src.scrapers.hashtag import scrape_hashtag
from src.scrapers.trending import scrape_trending
from src.utils import pipeline_to_dict, strategy_to_dict

app = FastAPI(
    title="Instagram Content Strategy Pipeline",
    description="Scrape trending Instagram content, analyze with AI, and generate a full content strategy",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Individual step endpoints (optional, for debugging) ---

class TrendingRequest(BaseModel):
    count: int = Field(default=50, ge=10, le=500)
    country: str = "United States"


class HashtagRequest(BaseModel):
    hashtag: str
    scrape_type: str = Field(default="top", pattern="^(top|recent)$")
    count: int = Field(default=50, ge=24, le=200)


class SuggestRequest(BaseModel):
    count: int = Field(default=100, ge=10, le=500)
    country: str = "United States"
    hashtags: list[str] = Field(default_factory=list)
    top_n: int = Field(default=10, ge=1, le=50)


class StrategyRequest(BaseModel):
    count: int = Field(default=50, ge=10, le=200)
    country: str = "United States"
    hashtags: list[str] = Field(default_factory=list)
    top_n: int = Field(default=5, ge=1, le=15)
    weeks: int = Field(default=2, ge=1, le=2)
    niche: Optional[str] = None
    use_vision: bool = True

class GeneratePostRequest(BaseModel):
    niche: str
    topic: str
    brand_context: str

class GeneratePostResponse(BaseModel):
    passage: str
    image_b64: str


# --- Main pipeline endpoint (for frontend) ---

class PipelineRequest(BaseModel):
    """Full pipeline input — connect your frontend to POST /pipeline."""

    niche: Optional[str] = Field(default=None, examples=["fitness", "music", "travel"])
    country: str = Field(default="United States")
    hashtags: list[str] = Field(default_factory=list, examples=[["fitness", "gym"]])
    scrape_count: int = Field(default=50, ge=10, le=500)
    hashtag_scrape_count: int = Field(default=50, ge=24, le=200)
    top_n: int = Field(default=5, ge=1, le=20)
    weeks: int = Field(default=2, ge=1, le=2)
    use_vision: bool = True
    save_outputs: bool = True


@app.get("/")
def root():
    return {
        "name": "Instagram Content Strategy Pipeline",
        "version": "2.0.0",
        "main_endpoint": "POST /pipeline",
        "description": "Runs scrape -> rank -> AI analyze -> strategy in one call",
        "endpoints": {
            "POST /pipeline": "Full pipeline (use this for frontend)",
            "POST /trending": "Scrape only",
            "POST /hashtag": "Hashtag scrape only",
            "POST /suggest": "Scrape + rank only",
            "POST /strategy": "Analyze + strategy only",
            "GET /countries": "Supported countries",
            "GET /health": "Health check",
        },
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/countries")
def countries():
    return {"countries": SUPPORTED_COUNTRIES}


@app.post("/pipeline")
def pipeline(req: PipelineRequest):
    """
    Full end-to-end pipeline.

    1. Scrapes Instagram Explore trending + hashtag top posts
    2. Ranks content by viral score
    3. Deep-analyzes top posts/reels with OpenAI
    4. Generates 1-2 week content strategy
    5. Returns everything + saves JSON files
    """
    try:
        validate_token()
        validate_openai_key()

        config = PipelineInput(**req.model_dump())
        result = run_full_pipeline(config)
        return pipeline_to_dict(result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        err = str(e)
        if "invalid_api_key" in err:
            raise HTTPException(status_code=401, detail="Invalid OpenAI API key")
        raise HTTPException(status_code=500, detail=err)


@app.post("/trending")
def trending(req: TrendingRequest):
    try:
        validate_token()
        items = scrape_trending(max_results=req.count, country=req.country)
        ranked = rank_content(items)
        return {"count": len(ranked), "items": [i.model_dump() for i in ranked]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/hashtag")
def hashtag(req: HashtagRequest):
    try:
        validate_token()
        items = scrape_hashtag(
            hashtag=req.hashtag,
            scrape_type=req.scrape_type,
            max_items=req.count,
        )
        ranked = rank_content(items)
        return {"count": len(ranked), "items": [i.model_dump() for i in ranked]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/suggest")
def suggest(req: SuggestRequest):
    try:
        validate_token()
        all_items = scrape_trending(max_results=req.count, country=req.country)
        for tag in req.hashtags:
            all_items.extend(scrape_hashtag(hashtag=tag, scrape_type="top", max_items=50))
        suggestions = generate_suggestions(all_items, top_n=req.top_n)
        return {
            "count": len(suggestions),
            "suggestions": [s.model_dump() for s in suggestions],
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/strategy")
def strategy(req: StrategyRequest):
    try:
        validate_token()
        validate_openai_key()
        report = run_strategy_pipeline(
            count=req.count,
            country=req.country,
            hashtags=req.hashtags,
            top_n=req.top_n,
            weeks=req.weeks,
            niche=req.niche,
            use_vision=req.use_vision,
        )
        return strategy_to_dict(report)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate-post")
def generate_post(req: GeneratePostRequest) -> GeneratePostResponse:
    try:
        validate_openai_key()
        
        system_prompt = (
            "You are an elite, highly abstract copywriter. You write in a wide, detailed, "
            "and deeply atmospheric passage format. DO NOT use bullet points. DO NOT use lists. "
            "Craft a single, flowing, and profound passage that captures the essence of the brand."
        )
        
        user_prompt = f"Niche: {req.niche}\nTopic: {req.topic}\nBrand Context/Taboos: {req.brand_context}\nWrite the post passage now."
        
        client = get_client()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        
        passage = response.choices[0].message.content or ""
        
        # Now generate the image
        image_prompt = f"A highly aesthetic, premium, and visually stunning image for an Instagram post about {req.topic} in the {req.niche} niche. Do not include any text in the image."
        b64_img = generate_ad_image(image_prompt)
        
        return GeneratePostResponse(passage=passage, image_b64=b64_img)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

