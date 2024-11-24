# BookWise Distribution Center Optimization Exercise

In this exercise, you will solve a warehouse location and distribution optimization problem using linear programming. You will:
1. Define decision variables for warehouse selection and assignment
2. Create constraints for capacity and coverage
3. Build the objective function to minimize total cost
4. Solve and analyze the results

## Problem Statement

BookWise Publishing is expanding their textbook distribution network in the Pacific Northwest. They need to optimize their warehouse locations to better serve their three main university bookstore partners.

### Requirements:
- Must open at least 2 and at most 3 distribution centers (DCs)
- Combined storage capacity must be at least 850,000 textbooks
- Each DC will make 40 shipments per year to each university bookstore it serves

### Distribution Center Data:
| DC | Fixed Cost ($/year) | Transport Cost ($/km/shipment) | Capacity (1000 books) |
|----|--------------------|-----------------------------|---------------------|
| DC1| 85,000            | 0.55                          | 410                |
| DC2| 85,000            | 0.35                          | 380                |
| DC3| 75,000            | 0.65                          | 330                |
| DC4| 75,000            | 0.45                          | 380                |
| DC5| 85,000            | 0.25                          | 340                |

### Distance to University Bookstores (km):
| DC | Bookstore 1 | Bookstore 2 | Bookstore 3 |
|----|-------------|-------------|-------------|
| DC1| 70         | 110         | 65          |
| DC2| 50         | 135         | 80          |
| DC3| 60         | 115         | 85          |
| DC4| 55         | 90          | 95          |
| DC5| 95         | 65          | 85          |

## Step 1: Setup and Variable Definition

First, let's import the required packages and define our decision variables.

```python
# Required packages
import pulp
import numpy as np
import pandas as pd

# Your code here to define:
# 1. Binary variables for DC selection (Open_DC1, Open_DC2, etc.)
# 2. Binary variables for bookstore assignment (Assign_DC1_Store1, etc.)
```

## Step 2: Create Constraints

Now, create the necessary constraints:
1. Must open 2-3 DCs
2. Total capacity must be at least 850,000 books
3. Each bookstore must be assigned to exactly one DC
4. Can only assign bookstores to open DCs

```python
# Your code here to create constraints
```

## Step 3: Define Objective Function

Create the objective function that minimizes:
1. Fixed costs of opening DCs
2. Transportation costs (40 shipments × distance × cost per km per shipment)

```python
# Your code here to create objective function
```

## Step 4: Solve and Analyze

Solve the problem and analyze the results:
1. Which DCs should be opened?
2. Which bookstores should be served by which DCs?
3. What is the total annual cost?

```python
# Your code here to solve and analyze results
```

## Testing Your Solution

Use these functions to check your work:

```python
from utils.testing.distribution_tests import (
    check_warehouse_variables,
    check_warehouse_constraints,
    check_warehouse_objective
)

# Test your variable definitions
if check_warehouse_variables(prob, ['DC1', 'DC2', 'DC3', 'DC4', 'DC5']):
    print("✓ Variables correctly defined!")
else:
    print("✗ Check your variable definitions")

# Test your constraints
if check_warehouse_constraints(prob, ['DC1', 'DC2', 'DC3', 'DC4', 'DC5']):
    print("✓ Constraints correctly formulated!")
else:
    print("✗ Check your constraints")

# Test your objective function
if check_warehouse_objective(prob, ['DC1', 'DC2', 'DC3', 'DC4', 'DC5']):
    print("✓ Objective function correctly defined!")
else:
    print("✗ Check your objective function")
```
