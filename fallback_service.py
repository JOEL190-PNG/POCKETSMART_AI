from app.schemas import RecommendationResponse, Recommendation
from app.services.catalog_service import search_url, platform_for_category


def money(value: float) -> float:
    return round(max(0.0, value), 2)


def home_fallback(data: dict) -> RecommendationResponse:
    budget = float(data["budget"])
    items = data["items"]
    recommendations = []
    allocations = {}
    remaining = budget

    for item in items:
        max_budget = min(float(item["max_budget"]) * int(item["quantity"]), remaining)
        per_item = max_budget / int(item["quantity"])
        platform = platform_for_category(item["category"])
        title = f"{item['category']} — {item['item']}"
        recommendations.append(
            Recommendation(
                title=title,
                category=item["category"],
                platform=platform,
                estimated_price=money(per_item),
                quantity=int(item["quantity"]),
                reason=f"Fits the requested {data['style']} style and stays within the item budget.",
                search_url=search_url(platform, item["item"]),
            )
        )
        allocations[item["category"]] = money(max_budget)
        remaining -= max_budget

    total = money(budget - remaining)
    return RecommendationResponse(
        planner="home",
        summary="Fallback plan generated locally because live Gemini AI is not enabled.",
        budget=budget,
        estimated_total=total,
        remaining_budget=money(remaining),
        allocations=allocations,
        recommendations=recommendations,
        notes=["Estimated prices are placeholders; verify current prices and availability before purchase."],
    )


def party_fallback(data: dict) -> RecommendationResponse:
    budget = float(data["budget"])
    allocations = {
        "Catering": money(budget * 0.45),
        "Venue": money(budget * 0.25),
        "Decoration": money(budget * 0.15),
        "Entertainment": money(budget * 0.10),
        "Contingency": money(budget * 0.05),
    }

    recs = [
        Recommendation(
            title=f"Catering for {data['guests']} guests",
            category="Catering",
            platform="Zomato",
            estimated_price=allocations["Catering"],
            quantity=1,
            reason="Budget allocation based on guest count and event type.",
            search_url=search_url("Zomato", f"{data['event_type']} catering {data['city']}"),
        ),
        Recommendation(
            title=f"Venue option in {data['city']}",
            category="Venue",
            platform="OYO",
            estimated_price=allocations["Venue"],
            quantity=1,
            reason="Example venue/accommodation search aligned with the venue preference.",
            search_url=search_url("OYO", f"event venue {data['city']}"),
        ),
        Recommendation(
            title="Party decoration package",
            category="Decoration",
            platform="Amazon",
            estimated_price=allocations["Decoration"],
            quantity=1,
            reason="General decoration allocation for the selected event.",
            search_url=search_url("Amazon", f"{data['event_type']} party decoration"),
        ),
        Recommendation(
            title="Entertainment supplies",
            category="Entertainment",
            platform="Amazon",
            estimated_price=allocations["Entertainment"],
            quantity=1,
            reason="Starter entertainment allocation.",
            search_url=search_url("Amazon", "party entertainment supplies"),
        ),
    ]
    return RecommendationResponse(
        planner="party",
        summary="Fallback party budget plan generated locally.",
        budget=budget,
        estimated_total=money(budget - allocations["Contingency"]),
        remaining_budget=allocations["Contingency"],
        allocations=allocations,
        recommendations=recs,
        notes=["The venue, food, and service links are search links rather than verified live availability."],
    )


def jewelry_fallback(data: dict) -> RecommendationResponse:
    budget = float(data["budget"])
    allocations = {
        "Necklace": money(budget * 0.45),
        "Earrings": money(budget * 0.30),
        "Bracelet": money(budget * 0.15),
        "Reserve": money(budget * 0.10),
    }
    recs = [
        Recommendation(
            title=f"{data['style'].title()} necklace",
            category="Jewelry",
            platform="Amazon",
            estimated_price=allocations["Necklace"],
            quantity=1,
            reason=f"Selected for the {data['occasion']} occasion and {data['metal']} metal preference.",
            search_url=search_url("Amazon", f"{data['style']} {data['metal']} necklace"),
        ),
        Recommendation(
            title=f"{data['style'].title()} earrings",
            category="Jewelry",
            platform="Flipkart",
            estimated_price=allocations["Earrings"],
            quantity=1,
            reason="A complementary accessory that can coordinate with the outfit.",
            search_url=search_url("Flipkart", f"{data['style']} {data['metal']} earrings"),
        ),
        Recommendation(
            title=f"{data['style'].title()} bracelet",
            category="Jewelry",
            platform="Amazon",
            estimated_price=allocations["Bracelet"],
            quantity=1,
            reason="Optional coordinating piece within the remaining budget.",
            search_url=search_url("Amazon", f"{data['style']} {data['metal']} bracelet"),
        ),
    ]
    return RecommendationResponse(
        planner="jewelry",
        summary="Fallback jewelry plan generated locally.",
        budget=budget,
        estimated_total=money(budget - allocations["Reserve"]),
        remaining_budget=allocations["Reserve"],
        allocations=allocations,
        recommendations=recs,
        notes=["If an outfit image was uploaded, fallback mode cannot analyze it; use Gemini mode for image-aware suggestions."],
    )
