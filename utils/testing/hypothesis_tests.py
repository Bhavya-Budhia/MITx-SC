"""Test functions for hypothesis testing problems."""
import numpy as np
from scipy import stats

def check_test_statistic(test_stat, expected=-8.742, tolerance=0.01):
    """
    Check if calculated test statistic is correct.
    
    Args:
        test_stat (float): Calculated test statistic
        expected (float): Expected test statistic
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if test statistic is within tolerance of expected value
    """
    return abs(test_stat - expected) <= tolerance

def check_p_value(p_value, alpha=0.05, tolerance=0.001):
    """
    Check if calculated p-value is correct and interpreted properly.
    
    Args:
        p_value (float): Calculated p-value
        alpha (float): Significance level
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        dict: Dictionary with validation results
    """
    expected_p = 0.0000124  # Example expected p-value
    p_value_correct = abs(p_value - expected_p) <= tolerance
    decision_correct = (p_value < alpha)
    
    return {
        'p_value_correct': p_value_correct,
        'decision_correct': decision_correct
    }

def check_conclusion(sample_data, mu0=720, alpha=0.05):
    """
    Verify hypothesis test conclusion based on sample data.
    
    Args:
        sample_data (list): List of sample measurements
        mu0 (float): Null hypothesis value
        alpha (float): Significance level
        
    Returns:
        dict: Dictionary with test results
    """
    # Calculate sample statistics
    n = len(sample_data)
    sample_mean = np.mean(sample_data)
    sample_std = np.std(sample_data, ddof=1)
    
    # Calculate test statistic
    t_stat = (sample_mean - mu0) / (sample_std / np.sqrt(n))
    
    # Calculate p-value (one-tailed test)
    p_value = stats.t.cdf(t_stat, df=n-1)
    
    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'reject_null': p_value < alpha
    }

def verify_assumptions(sample_data):
    """
    Check if assumptions for t-test are met.
    
    Args:
        sample_data (list): List of sample measurements
        
    Returns:
        dict: Dictionary with assumption test results
    """
    # Check normality using Shapiro-Wilk test
    _, p_value_normality = stats.shapiro(sample_data)
    
    # Check for outliers using z-score method
    z_scores = np.abs(stats.zscore(sample_data))
    has_outliers = any(z_scores > 3)
    
    return {
        'normality_satisfied': p_value_normality > 0.05,
        'no_outliers': not has_outliers
    }
