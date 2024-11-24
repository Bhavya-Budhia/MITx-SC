# YOUKEA Cost Accounting Analysis Exercise

In this exercise, you will perform activity-based costing (ABC) analysis for YOUKEA's Boston branch. You will:
1. Calculate activity costs and rates
2. Analyze customer profitability
3. Make strategic recommendations based on your analysis
4. Create visualizations to support your findings

## Problem Statement

YOUKEA's Boston branch needs to assess the profitability of different business customers using activity-based costing instead of simple volume-based overhead allocation.

### Key Information:

#### 1. Order Processing Methods:
- Web orders (automated)
- Phone orders (manual entry)

#### 2. Delivery Methods:
- Common carrier (cost based on number of chairs)
- Express delivery (cost based on number of shipments)

#### 3. Volume Statistics:
- Total orders: 700
- Total chairs: 4,800
- Phone orders: 20% of total orders (140 orders)
- Phone order lines: 800
- Express deliveries: 100 shipments (800 chairs)

#### 4. Financial Data:
```
Sales:                      $2,400,000
Cost of purchased goods:    $1,400,000
Gross margin:               $1,000,000
Freight (Common carrier):   $350,000
Warehouse personnel:        $400,000
Other warehouse expenses:   $40,000
Delivery personnel:         $100,000
Other delivery expenses:    $10,000
Order entry expenses:       $20,000
Operating Income:           $80,000
```

## Step 1: Activity Cost Pool Analysis

First, let's calculate the cost pools for each activity.

```python
# Required packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Your code here to:
# 1. Calculate order entry cost pool
# 2. Calculate warehouse handling cost pool
# 3. Calculate delivery cost pool
# 4. Calculate freight cost pool
```

## Step 2: Activity Rate Calculations

Now calculate the rate for each activity:
1. Order entry rate per order (web vs. phone)
2. Warehouse handling rate per chair
3. Delivery rate per shipment
4. Freight rate per chair

```python
# Your code here to calculate activity rates
```

## Step 3: Customer Cost Analysis

Analyze costs for three customer segments:
1. Large retailers (high volume, web orders, common carrier)
2. Medium businesses (mixed orders, some express delivery)
3. Small businesses (low volume, phone orders, express delivery)

```python
# Your code here to analyze customer costs
```

## Step 4: Visualization and Recommendations

Create visualizations to support your analysis:
1. Cost breakdown by activity
2. Customer profitability comparison
3. Order method cost comparison

```python
# Your code here to create visualizations
```

## Testing Your Solution

Use these functions to check your work:

```python
from utils.testing.cost_accounting_tests import (
    check_activity_costs,
    check_customer_profitability,
    check_cost_allocation
)

# Test your activity cost calculations
activity_costs = {
    'order_entry': your_order_entry_cost,
    'warehouse_handling': your_warehouse_cost,
    'delivery': your_delivery_cost,
    'freight': your_freight_cost
}
if check_activity_costs(activity_costs, 920000):  # Total overhead cost
    print("✓ Activity costs correctly calculated!")
else:
    print("✗ Check your activity cost calculations")

# Test your customer profitability analysis
revenue = {
    'large_retailers': your_large_revenue,
    'medium_business': your_medium_revenue,
    'small_business': your_small_revenue
}
costs = {
    'large_retailers': your_large_costs,
    'medium_business': your_medium_costs,
    'small_business': your_small_costs
}
if check_customer_profitability(revenue, costs):
    print("✓ Customer profitability correctly analyzed!")
else:
    print("✗ Check your profitability calculations")
```

## Extension Questions

1. Cost Driver Analysis:
   - How would costs change if more orders moved to web-based ordering?
   - What is the cost impact of express delivery vs. common carrier?

2. Strategic Recommendations:
   - Should YOUKEA encourage more web orders? How?
   - Should they adjust pricing for different delivery methods?
   - How can they improve profitability for small business customers?
