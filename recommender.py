from PIL import Image
from app.schemas import HomeRequest, PartyRequest, JewelryRequest, RecommendationResponse
from app.services.gemini_service import GeminiService
from app.services.fallback_service import home_fallback, party_fallback, jewelry_fallback
from app.services.prompts import HOME_PROMPT, PARTY_PROMPT, JEWELRY_PROMPT


class RecommendationEngine:
    def __init__(self):
        self.gemini = GeminiService()

    def home(self, request: HomeRequest) -> RecommendationResponse:
        data = request.model_dump()
        if self.gemini.enabled:
            try:
                return self.gemini.generate(HOME_PROMPT, data)
            except Exception:
                pass
        return home_fallback(data)

    def party(self, request: PartyRequest) -> RecommendationResponse:
        data = request.model_dump()
        if self.gemini.enabled:
            try:
                return self.gemini.generate(PARTY_PROMPT, data)
            except Exception:
                pass
        return party_fallback(data)

    def jewelry(
        self,
        request: JewelryRequest,
        image: Image.Image | None = None,
    ) -> RecommendationResponse:
        data = request.model_dump()
        if self.gemini.enabled:
            try:
                return self.gemini.generate(JEWELRY_PROMPT, data, image=image)
            except Exception:
                pass
        return jewelry_fallback(data)


engine = RecommendationEngine()
