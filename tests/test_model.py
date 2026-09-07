from likelihood_index import LikelihoodIndex

model = LikelihoodIndex()

ALL = {
    "share_search": 0.0,
    "consideration": 0.0,
    "purchase_intent": 0.0,
    "creator_sentiment": 0.0,
    "reviews": 0.0,
    "wom": 0.0,
    "creative_resonance": 0.0,
    "organic_signal": 0.0,
    "paid_signal": 0.0,
    "distribution": 0.0,
    "instock": 0.0,
    "ai_visibility": 0.0,
    "search_visibility": 0.0,
    "meaning": 0.0,
    "difference": 0.0,
    "salience": 0.0,
}


def test_neutral_baseline():
    r = model.score(ALL)
    assert r.likelihood_index == 50.0
    assert r.evidence_confidence == 100.0
    assert r.system_coherence == 100.0


def test_broad_positive_movement_beats_neutral():
    r = model.score({k: 0.9 for k in ALL})
    assert r.likelihood_index > 60
    assert r.system_coherence > 95


def test_one_viral_signal_does_not_hijack_index():
    x = dict(ALL)
    x["organic_signal"] = 3.0
    r = model.score(x)
    assert r.likelihood_index < 55


def test_contradiction_reduces_coherence():
    x = dict(ALL)
    x.update({
        "creative_resonance": 1.5,
        "organic_signal": 1.3,
        "paid_signal": 1.5,
        "distribution": -1.3,
        "instock": -1.8,
    })
    r = model.score(x)
    assert r.system_coherence < 70


def test_missingness_reduces_confidence():
    x = {k: (0.8 if i % 2 == 0 else None) for i, k in enumerate(ALL)}
    r = model.score(x)
    assert r.evidence_confidence < 70


def test_zero_source_confidence_reduces_confidence():
    conf = {k: 0.5 for k in ALL}
    r = model.score(ALL, conf)
    assert r.evidence_confidence == 50.0


def test_empty_input_is_neutral_but_untrusted():
    r = model.score({})
    assert r.likelihood_index == 50.0
    assert r.evidence_confidence == 0.0
    assert r.system_coherence == 0.0
