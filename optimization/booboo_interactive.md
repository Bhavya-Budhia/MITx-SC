# BooBoo Magicians Party Package Optimization Exercise

In this exercise, you will help BooBoo Magicians optimize their party package offerings using linear programming. You will:
1. Define decision variables for package quantities
2. Create resource constraints
3. Build the objective function to maximize profit
4. Solve and analyze the results

## Problem Statement

BooBoo Magicians offers three types of party packages and needs to determine the optimal mix to maximize profit while respecting resource constraints.

### Available Packages:
1. Standard Package: Basic party entertainment
2. Joyful Package: Enhanced entertainment with more features
3. Fabulous Package: Premium entertainment experience

### Resource Requirements and Financials:
| Resource/Financial | Standard | Joyful | Fabulous |
|-------------------|----------|---------|-----------|
| Labor (hours)     | 3        | 5       | 8         |
| Balloons (bags)   | 2        | 5       | 8         |
| Cost              | $2K      | $3K     | $4K       |
| Price             | $3K      | $5K     | $7K       |
| Profit            | $1K      | $2K     | $3K       |

### Resource Constraints (January):
- Available balloon bags: 325
- Available labor hours: 400

### Additional Information:
- All packages produced will be sold (guaranteed demand)
- Goal: Maximize total profit

## Step 1: Setup and Variable Definition

First, let's import the required packages and define our decision variables.

```python
# Required packages
import pulp
import numpy as np
import pandas as pd

# Your code here to define:
# 1. Decision variables for each package type (x_Standard, x_Joyful, x_Fabulous)
# 2. Set variable bounds (non-negative)
```

## Step 2: Create Constraints

Now, create the necessary constraints:
1. Labor hours constraint (≤ 400 hours)
2. Balloon bags constraint (≤ 325 bags)
3. Non-negativity constraints (already handled in variable definition)

```python
# Your code here to create constraints
```

## Step 3: Define Objective Function

Create the objective function that maximizes total profit:
- Standard Package: $1,000 profit per package
- Joyful Package: $2,000 profit per package
- Fabulous Package: $3,000 profit per package

```python
# Your code here to create objective function
```

## Step 4: Solve and Analyze

Solve the problem and analyze the results:
1. How many of each package should be offered?
2. What is the total profit?
3. Which resources are fully utilized (binding constraints)?

```python
# Your code here to solve and analyze results
```

## Testing Your Solution

Use these functions to check your work:

```python
from utils.testing.resource_tests import (
    check_party_variables,
    check_party_constraints,
    check_party_objective
)

# Test your variable definitions
if check_party_variables(prob):
    print("✓ Variables correctly defined!")
else:
    print("✗ Check your variable definitions")

# Test your constraints
if check_party_constraints(prob):
    print("✓ Constraints correctly formulated!")
else:
    print("✗ Check your constraints")

# Test your objective function
if check_party_objective(prob):
    print("✓ Objective function correctly defined!")
else:
    print("✗ Check your objective function")
```

## Extension Questions

1. Sensitivity Analysis:
   - How would the solution change if more labor hours were available?
   - What if balloon costs increased?

2. Additional Constraints:
   - How would the solution change if you needed to offer at least 10 Standard packages?
   - What if you could only offer a maximum of 30 Fabulous packages?
