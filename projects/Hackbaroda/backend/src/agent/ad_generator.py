"""Generate mock advertisement images for the brand using DALL-E 3."""

from src.agent.openai_client import call_structured, generate_ad_image
from src.models.strategy import ContentStrategyReport, MockAdvertisement
from pydantic import BaseModel


class AdPrompts(BaseModel):
    """AI-generated DALL-E prompts for mock ads."""
    story_post_prompt: str
    story_post_caption: str
    product_highlight_prompt: str
    product_highlight_caption: str
    reel_thumbnail_prompt: str
    reel_thumbnail_caption: str


def _build_prompt_request(niche: str, aesthetics: list[str], visual_texture: str, strategy_summary: str) -> tuple[str, str]:
    system = (
        "You are a creative director at a premium advertising agency. "
        "Generate DALL-E 3 image prompts for mock social media advertisements. "
        "Each prompt must be detailed, specifying style, composition, lighting, colors, and mood. "
        "Do NOT include any text/words/letters in the image prompts — DALL-E should generate pure visual content. "
        "Captions should be Instagram-ready with emojis and hooks."
    )
    user = (
        f"Brand niche: {niche}\n"
        f"Aesthetic direction: {', '.join(aesthetics) if aesthetics else 'modern, clean'}\n"
        f"Visual texture: {visual_texture}\n"
        f"Strategy summary: {strategy_summary[:500]}\n\n"
        "Generate 3 DALL-E prompts and matching Instagram captions for:\n"
        "1. A brand story post — lifestyle/aspirational image\n"
        "2. A product/service highlight — showcase/detail image\n"
        "3. A reel thumbnail — eye-catching, scroll-stopping image\n\n"
        "Make each prompt specific to this brand's aesthetic and niche."
    )
    return system, user


def generate_mock_ads(
    niche: str,
    aesthetics: list[str] | None = None,
    visual_texture: str = "linen",
    strategy_summary: str = "",
) -> list[MockAdvertisement]:
    """Generate 3 mock advertisement images with captions."""
    aesthetics = aesthetics or []

    system, user = _build_prompt_request(niche, aesthetics, visual_texture, strategy_summary)
    prompts = call_structured(system, user, AdPrompts)

    ads = []
    ad_configs = [
        ("Brand Story", prompts.story_post_prompt, prompts.story_post_caption, "story_post"),
        ("Product Highlight", prompts.product_highlight_prompt, prompts.product_highlight_caption, "product_highlight"),
        ("Reel Thumbnail", prompts.reel_thumbnail_prompt, prompts.reel_thumbnail_caption, "reel_thumbnail"),
    ]

    for title, prompt, caption, ad_type in ad_configs:
        print(f"[Ad Gen] Generating {title}...")
        image_b64 = generate_ad_image(prompt, size="1024x1024")
        ads.append(MockAdvertisement(
            title=title,
            description=f"AI-generated {title.lower()} for your {niche} brand",
            image_base64=image_b64,
            suggested_caption=caption,
            ad_type=ad_type,
            hashtags=[],
            prompt_used=prompt,
        ))

    return ads
