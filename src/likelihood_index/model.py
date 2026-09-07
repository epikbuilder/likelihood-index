from __future__ import annotations

from dataclasses import dataclass, asdict
from math import sqrt, tanh
from typing import Dict, Mapping, Optional


DEFAULT_DOMAINS = {
    "Demand Formation": {
        "weight": 0.25,
        "metrics": ("share_search", "consideration", "purchase_intent"),
    },
    "Social Proof": {
        "weight": 0.20,
        "metrics": ("creator_sentiment", "reviews", "wom"),
    },
    "Media Resonance": {
        "weight": 0.20,
        "metrics": ("creative_resonance", "organic_signal", "paid_signal"),
    },
    "Availability": {
        "weight": 0.15,
        "metrics": ("distribution", "instock"),
    },
    "Discoverability": {
        "weight": 0.10,
        "metrics": ("ai_visibility", "search_visibility"),
    },
    "Brand Meaning": {
        "weight": 0.10,
        "metrics": ("meaning", "difference", "salience"),
    },
}


@dataclass(frozen=True)
class LikelihoodResult:
    likelihood_index: float
    evidence_confidence: float
    system_coherence: float
    domain_effects: Dict[str, float]
    domain_confidence: Dict[str, float]

    def as_dict(self) -> dict:
        return asdict(self)


class LikelihoodIndex:
    """Reference implementation of the open Likelihood Index.

    Metric values are expected to be standardized directional effects
    (for example z-scores versus a trailing brand baseline or category norm).

    This is an index, not a literal individual purchase probability.
    """

    def __init__(self, domains: Optional[Mapping] = None, scale: float = 38.0):
        self.domains = dict(domains or DEFAULT_DOMAINS)
        self.scale = float(scale)

        total_weight = sum(float(spec["weight"]) for spec in self.domains.values())
        if abs(total_weight - 1.0) > 1e-9:
            raise ValueError("Domain weights must sum to 1.0")

    @staticmethod
    def _bounded_effect(z: float) -> float:
        return tanh(float(z) / 2.0)

    def score(
        self,
        values: Mapping[str, Optional[float]],
        metric_confidence: Optional[Mapping[str, float]] = None,
    ) -> LikelihoodResult:
        metric_confidence = metric_confidence or {}

        domain_effects: Dict[str, float] = {}
        domain_confidence: Dict[str, float] = {}

        weighted_effect = 0.0
        weighted_confidence = 0.0
        present_domain_weight = 0.0

        for domain_name, spec in self.domains.items():
            metrics = tuple(spec["metrics"])
            observations = []

            for metric in metrics:
                raw = values.get(metric)
                if raw is None:
                    continue

                confidence = float(metric_confidence.get(metric, 1.0))
                if not 0.0 <= confidence <= 1.0:
                    raise ValueError(f"Confidence for {metric} must be between 0 and 1")

                observations.append((self._bounded_effect(raw), confidence))

            if not observations:
                continue

            confidence_weight_sum = sum(c for _, c in observations)
            if confidence_weight_sum == 0:
                domain_effect = 0.0
            else:
                domain_effect = sum(e * c for e, c in observations) / confidence_weight_sum

            coverage = len(observations) / len(metrics)
            mean_source_confidence = sum(c for _, c in observations) / len(observations)
            d_confidence = coverage * mean_source_confidence

            domain_effects[domain_name] = domain_effect
            domain_confidence[domain_name] = d_confidence

            weight = float(spec["weight"])
            weighted_effect += weight * domain_effect
            weighted_confidence += weight * d_confidence
            present_domain_weight += weight

        if not present_domain_weight:
            return LikelihoodResult(
                likelihood_index=50.0,
                evidence_confidence=0.0,
                system_coherence=0.0,
                domain_effects={},
                domain_confidence={},
            )

        raw_index_effect = weighted_effect / present_domain_weight
        likelihood_index = max(0.0, min(100.0, 50.0 + self.scale * raw_index_effect))

        evidence_confidence = max(0.0, min(100.0, 100.0 * weighted_confidence))

        if len(domain_effects) == 1:
            system_coherence = 40.0
        else:
            total = sum(float(self.domains[d]["weight"]) for d in domain_effects)
            mean = sum(
                float(self.domains[d]["weight"]) * effect
                for d, effect in domain_effects.items()
            ) / total
            variance = sum(
                float(self.domains[d]["weight"]) * (effect - mean) ** 2
                for d, effect in domain_effects.items()
            ) / total
            system_coherence = max(0.0, min(100.0, 100.0 - 105.0 * sqrt(variance)))

        return LikelihoodResult(
            likelihood_index=round(likelihood_index, 1),
            evidence_confidence=round(evidence_confidence, 1),
            system_coherence=round(system_coherence, 1),
            domain_effects={k: round(v, 4) for k, v in domain_effects.items()},
            domain_confidence={k: round(v, 4) for k, v in domain_confidence.items()},
        )
