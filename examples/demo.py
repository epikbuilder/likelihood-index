from likelihood_index import LikelihoodIndex

model = LikelihoodIndex()

signals = {
    "share_search": 1.2,
    "consideration": 0.8,
    "purchase_intent": 0.6,
    "creator_sentiment": 0.7,
    "reviews": 0.9,
    "wom": 0.5,
    "creative_resonance": 1.0,
    "organic_signal": 0.4,
    "paid_signal": 0.8,
    "distribution": 0.2,
    "instock": 0.1,
    "ai_visibility": 0.3,
    "search_visibility": 0.5,
    "meaning": 0.4,
    "difference": 0.2,
    "salience": 0.6,
}

print(model.score(signals).as_dict())
