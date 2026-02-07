from datetime import datetime

CATEGORY_KEYWORDS = {
    "Food": [
        "swiggy",
        "zomato",
        "hotel",
        "restaurant",
        "food",
        "pizza",
        "burger",
        "tea",
        "coffee",
    ],
    "Travel": ["uber", "ola", "bus", "train", "metro", "petrol", "diesel", "flight"],
    "Shopping": ["amazon", "flipkart", "mall", "shopping", "clothes", "shoes"],
    "Bills": ["electricity", "water", "wifi", "recharge", "bill", "gas"],
    "Health": ["hospital", "medical", "medicine", "pharmacy", "doctor"],
    "Education": ["course", "udemy", "coursera", "books", "college", "fees"],
    "Entertainment": ["netflix", "prime", "movie", "spotify", "game"],
}


def today_date():
    return datetime.now().strftime("%Y-%m-%d")


def suggest_category(title: str):
    text = title.lower()

    for category, words in CATEGORY_KEYWORDS.items():
        for w in words:
            if w in text:
                return category

    return "Other"
