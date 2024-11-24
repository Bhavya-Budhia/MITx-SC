# SunGlass Hut Inventory Management

You're the new supply chain analyst at SunGlass Hut, managing inventory for their premium "RayMaster" aviator sunglasses across 150 retail locations. Historical data shows that monthly demand per store follows a normal distribution with a mean of 75 units and standard deviation of 25 units. You're considering stocking 90 units per store.

## Part 1: Basic Probability Analysis

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Define parameters
mean = 75
std_dev = 25
stock_level = 90

# Your code here to calculate:
# a) Probability of meeting demand with k=90 units
# b) Probability of stockout
# c) Z-value for k=90
# d) Verify using standard normal distribution
```

### Questions to Answer:
1. What's the probability of meeting demand with 90 units?
2. What's the stockout probability?
3. What's the z-value for inventory level k=90?
4. Using standard normal form, verify your probability from question 1

## Part 2: Service Level Analysis

```python
# Your code here to calculate:
# a) Units needed for 90% service level
# b) Units needed for 95% service level
# c) Z-value for 95% service level
# d) Verify inventory level calculation
```

### Questions to Answer:
1. How many units needed to meet 90% of demand?
2. How many units needed to meet 95% of demand?
3. What's the z-value for 95% service level?
4. Verify your inventory level calculation

## Part 3: Two-Stage Inventory System

```python
# Your code here to analyze:
# Store stock: 80 units
# Warehouse backup: 40 units
# Calculate various probabilities
```

### Questions to Answer:
1. Probability of meeting demand from store stock only
2. Probability of needing warehouse stock but not exceeding total stock
3. Probability of total stockout
4. Overall probability of meeting demand

## Solution Testing

```python
from utils.testing.inventory_tests import (
    check_service_level,
    check_z_score,
    check_two_stage_system
)

# Test your calculations
results = {
    'service_level_90': your_service_level_90,
    'z_score_95': your_z_score_95,
    'total_stockout_prob': your_stockout_prob
}

if check_service_level(results['service_level_90'], 0.90):
    print("✓ Service level calculation correct!")
else:
    print("✗ Check your service level calculation")

# Similar tests for other parts...
```

## Visualization

```python
# Create visual representations of:
# 1. Normal distribution with key points
# 2. Service levels and corresponding inventory
# 3. Two-stage system probabilities
```

## Extension Questions

1. Cost Analysis:
   - How would holding costs affect optimal inventory levels?
   - What's the trade-off between service level and inventory cost?

2. Multi-Store Strategy:
   - How could you optimize inventory across stores?
   - What factors might affect store-specific demand distributions?

## Mathematical Notes

Key concepts used:
1. Normal Distribution Properties
2. Z-score Transformation
3. Service Level Calculations
4. Probability Integration

Remember:
- Standard normal table values
- Relationship between z-scores and probabilities
- Cumulative distribution function usage
