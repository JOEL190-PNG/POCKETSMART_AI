import json
from typing import Any
from PIL import Image
from google import genai
from google.genai import types
from app.config import get_settings
from app.schemas import RecommendationResponse


class GeminiService:
    def __init__(self):
        self.settings = get_settings()
        self.client = None
        if self.settings.gemini_api_key and not self.settings.use_mock_ai:
            self.client = genai.Client(api_key=self.settings.gemini_api_key)

    @property
    def enabled(self) -> bool:
        return self.client is not None

    def generate(
        self,
        prompt: str,
        payload: dict[str, Any],
        image: Image.Image | None = None,
    ) -> RecommendationResponse:
        if not self.enabled:
            raise RuntimeError("Gemini is not configured")

        contents: list[Any] = [prompt + "\n\nUSER INPUT:\n" + json.dumps(payload, indent=2)]
        if image is not None:
            contents.append(image)

        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=4000,
                response_mime_type="application/json",
                response_schema=RecommendationResponse,
            ),
        )

        parsed = getattr(response, "parsed", None)
        if parsed is not None:
            if isinstance(parsed, RecommendationResponse):
                return parsed
            return RecommendationResponse.model_validate(parsed)

        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response")

        return RecommendationResponse.model_validate_json(text)
