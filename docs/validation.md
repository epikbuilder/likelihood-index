# Validation Roadmap

The public reference model uses conservative starting weights. Those weights are hypotheses.

## Minimum viable validation

For one brand/category, assemble a time series containing:

### Leading signals
- share of search
- consideration
- purchase intent
- review strength / velocity
- creator or advocacy signal
- paid creative resonance
- organic engagement quality
- availability / in-stock
- search visibility
- AI / answer-engine visibility
- brand meaning / salience measures

### Future outcomes
Keep these outside the index:
- sales
- market share
- penetration
- new-customer rate
- repeat rate

## Recommended process

1. Normalize each signal using only information available at that time.
2. Calculate the index at each historical period.
3. Lag business outcomes forward by several horizons.
4. Test directional accuracy and rank correlation.
5. Use rolling or holdout validation.
6. Compare against simpler baselines such as:
   - share of search alone,
   - consideration alone,
   - media spend alone.
7. Only retain complexity that improves out-of-sample performance.

## Anti-overfitting principle

A more complicated model is not automatically a better model.

The open framework should earn its complexity by outperforming simple baselines on future data.
