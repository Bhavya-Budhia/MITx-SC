# GameStop Pre-order Bonus Analysis

As a marketing manager at GameStop, Sarah Chen is preparing special collector's cards as pre-order bonuses for the launch of "Stellar Odyssey VII". For every $50 spent on pre-orders, customers receive one random collector's card from a limited edition set. Sarah has prepared 300 cards total, and once a card is given away, it won't be replaced.

## Card Distribution
| Card Type | Quantity |
|-----------|----------|
| Legendary Heroes | 35 |
| Rare Weapons | 65 |
| Epic Locations | 42 |
| Special Moves | 48 |
| Boss Battles | 55 |
| Secret Areas | 25 |
| Hidden Quests | 30 |

## Problem Analysis

### Part 1: Single Event Probability
```python
import numpy as np
from scipy import stats

# Your code here to calculate:
# What is the probability that the first customer who spends $75 
# (earning one card) gets a Rare Weapons card?
```

### Part 2: Conditional Probability
```python
# Your code here to calculate:
# Given that the first card was a Rare Weapons card,
# what is the probability that the second customer who spends $50
# also gets a Rare Weapons card?
```

### Part 3: Multiple Event Probability
```python
# Your code here to calculate:
# A customer spends $150 (earning 3 cards)
# What is the probability of getting:
# - 2 Epic Locations cards
# - 1 Boss Battles card
# (order doesn't matter)
```

## Solution Testing

```python
from utils.testing.probability_tests import (
    check_single_event_prob,
    check_conditional_prob,
    check_multiple_event_prob
)

# Test your probability calculations
probabilities = {
    'single_event': your_single_event_prob,
    'conditional': your_conditional_prob,
    'multiple_event': your_multiple_event_prob
}

if check_single_event_prob(probabilities['single_event']):
    print("✓ Single event probability correct!")
else:
    print("✗ Check your single event calculation")

# Similar tests for other parts...
```

## Extension Questions

1. Probability Analysis:
   - How would the probabilities change if cards were replaced after each draw?
   - What's the probability of getting at least one Legendary Heroes card in 3 draws?

2. Business Strategy:
   - Should GameStop offer different odds for different spending levels?
   - How could they optimize the distribution of cards to maximize customer satisfaction?

## Mathematical Notes

For reference, here are the key probability concepts used:
1. Single Event Probability: P(A) = n(A)/n(S)
2. Conditional Probability: P(B|A) = P(A∩B)/P(A)
3. Multiple Event Probability (without replacement): Uses combination formula

Remember to account for:
- Sample space changes after each draw
- Order doesn't matter for multiple events
- Total probability must sum to 1
