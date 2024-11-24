# QuickPrint Processing Time Analysis

QuickPrint is a digital printing service that's testing a new pre-processing workflow to reduce printing times for their high-volume color documents. The standard processing time is 720 seconds with a variance of 30 seconds. To improve efficiency during peak hours, the team is experimenting with a new AI-powered pre-processing system.

## Experiment Data

The team collected the following processing times (in seconds) using the new system:

| Print Job | Processing Time (seconds) |
|-----------|-------------------------|
| 1 | 685 |
| 2 | 695 |
| 3 | 701 |
| 4 | 688 |
| 5 | 692 |
| 6 | 679 |
| 7 | 683 |
| 8 | 698 |
| 9 | 691 |
| 10 | 687 |

## Part 1: Hypothesis Formation

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Your code here to:
# 1. State null hypothesis
# 2. State alternative hypothesis
# 3. Identify test type needed
```

### Questions:
1. What is the null hypothesis?
2. What is the alternative hypothesis?
3. Why is this the appropriate test?

## Part 2: Test Statistics

```python
# Your code here to:
# 1. Calculate sample statistics
# 2. Compute test statistic
# 3. Determine degrees of freedom
```

### Questions:
1. What is the sample mean?
2. What is the sample standard deviation?
3. What is the test statistic?
4. What are the degrees of freedom?

## Part 3: Analysis and Conclusion

```python
# Your code here to:
# 1. Calculate p-value
# 2. Compare to significance level (α = 0.05)
# 3. Make conclusion
```

### Questions:
1. What is the p-value?
2. Do we reject the null hypothesis?
3. What does this mean in business terms?

## Solution Testing

```python
from utils.testing.hypothesis_tests import (
    check_test_statistic,
    check_p_value,
    check_conclusion
)

# Test your calculations
results = {
    'test_statistic': your_test_statistic,
    'p_value': your_p_value,
    'reject_null': your_reject_decision
}

if check_test_statistic(results['test_statistic']):
    print("✓ Test statistic calculation correct!")
else:
    print("✗ Check your test statistic calculation")

# Similar tests for other parts...
```

## Visualization

```python
# Create visual representations of:
# 1. Sample distribution
# 2. Test statistic on t-distribution
# 3. Critical region and p-value
```

## Extension Questions

1. Statistical Power:
   - What is the power of this test?
   - How many samples would we need for higher confidence?

2. Business Impact:
   - What is the practical significance of the time reduction?
   - How would this affect daily throughput?

## Mathematical Notes

Key concepts used:
1. Hypothesis Testing Framework
2. T-distribution Properties
3. P-value Interpretation
4. Statistical Power Analysis

Remember:
- Assumptions of t-test
- Relationship between sample size and power
- Practical vs. statistical significance
