from pydantic import BaseModel

from openai import OpenAI

from src.config import OPENAI_MODEL, validate_openai_key

T = type[BaseModel]


def get_client() -> OpenAI:
    return OpenAI(api_key=validate_openai_key())


def call_structured(
    system_prompt: str,
    user_prompt: str,
    response_model: T,
    *,
    image_url: str | None = None,
) -> BaseModel:
    """Call OpenAI and parse response into a Pydantic model."""
    client = get_client()

    user_content: list[dict] = [{"type": "text", "text": user_prompt}]
    if image_url:
        user_content.append({"type": "image_url", "image_url": {"url": image_url}})

    response = client.beta.chat.completions.parse(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        response_format=response_model,
        temperature=0.4,
    )

    parsed = response.choices[0].message.parsed
    if parsed is None:
        raise ValueError("OpenAI returned an empty or unparseable response")

    return parsed


def generate_ad_image(prompt: str, size: str = "1024x1024") -> str:
    """Generate a mock ad image using DALL-E 3. Returns base64 image data."""
    try:
        client = get_client()
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            response_format="b64_json",
            n=1,
        )
        return response.data[0].b64_json
    except Exception as e:
        print(f"[Ad Generation] Image generation failed: {e}")
        return ""
