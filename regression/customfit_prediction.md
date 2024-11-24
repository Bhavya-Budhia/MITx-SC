# CustomFit Tailoring Time Prediction

CustomFit is a premium tailoring service that wants to better predict alteration times for customer garments. They've collected data on garment complexity (measured by number of alterations needed) and the total time taken to complete the alterations.

## Sample Data

| Alterations Required | Completion Time (minutes) |
|---------------------|--------------------------|
| 3 | 45 |
| 7 | 95 |
| 2 | 35 |
| 8 | 105 |
| 1 | 25 |
| 4 | 55 |
| 6 | 85 |
| 2 | 30 |
| 3 | 40 |
| 7 | 90 |
| 5 | 70 |
| 4 | 50 |
| 5 | 75 |
| 6 | 80 |

## Part 1: Linear Regression Analysis

```python
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Your code here to:
# 1. Prepare data
# 2. Fit linear regression model
# 3. Calculate coefficients and intercept
```

### Questions:
1. What is the intercept (β₀)?
2. What is the slope (β₁)?
3. What is the R² value?
4. What is the p-value for the slope?

## Part 2: Prediction

```python
# Your code here to:
# 1. Create prediction function
# 2. Calculate confidence intervals
# 3. Make specific predictions
```

### Questions:
1. Predict time for 5 alterations
2. Calculate 95% confidence interval
3. Calculate prediction interval

## Part 3: Model Diagnostics

```python
# Your code here to:
# 1. Calculate residuals
# 2. Check normality
# 3. Check homoscedasticity
```

### Questions:
1. Are residuals normally distributed?
2. Is variance constant?
3. Are there any influential points?

## Solution Testing

```python
from utils.testing.regression_tests import (
    check_coefficients,
    check_prediction,
    check_diagnostics
)

# Test your calculations
results = {
    'intercept': your_intercept,
    'slope': your_slope,
    'r_squared': your_r_squared
}

if check_coefficients(results):
    print("✓ Regression coefficients correct!")
else:
    print("✗ Check your regression calculations")

# Similar tests for other parts...
```

## Visualization

```python
# Create visual representations of:
# 1. Scatter plot with regression line
# 2. Residual plot
# 3. Q-Q plot for normality
```

## Extension Questions

1. Model Improvements:
   - What other variables might be relevant?
   - How could we handle non-linear relationships?

2. Business Applications:
   - How can this improve scheduling?
   - What are the limitations of this model?

## Mathematical Notes

Key concepts used:
1. Simple Linear Regression
2. Least Squares Estimation
3. Statistical Inference
4. Residual Analysis

Remember:
- Assumptions of linear regression
- Interpretation of coefficients
- Confidence vs. prediction intervals
