from urllib.parse import quote_plus


PLATFORM_SEARCH = {
    "Amazon": "https://www.amazon.in/s?k={query}",
    "Flipkart": "https://www.flipkart.com/search?q={query}",
    "IKEA": "https://www.ikea.com/in/en/search/?q={query}",
    "Swiggy": "https://www.swiggy.com/search?query={query}",
    "Zomato": "https://www.zomato.com/search?q={query}",
    "OYO": "https://www.oyorooms.com/search?q={query}",
}


def search_url(platform: str, query: str) -> str:
    template = PLATFORM_SEARCH.get(platform)
    if not template:
        return "https://www.google.com/search?q=" + quote_plus(query)
    return template.format(query=quote_plus(query))


def platform_for_category(category: str) -> str:
    category_lower = category.lower()
    if any(word in category_lower for word in ("food", "catering", "cake", "restaurant")):
        return "Zomato"
    if any(word in category_lower for word in ("venue", "stay", "hotel", "accommodation")):
        return "OYO"
    if any(word in category_lower for word in ("furniture", "desk", "table", "storage")):
        return "IKEA"
    if any(word in category_lower for word in ("jewelry", "earring", "necklace", "bracelet", "ring")):
        return "Amazon"
    return "Amazon"
