"""Test functions for QuickPrint Processing Time Analysis."""
import numpy as np
from scipy import stats

def check_test_statistic(t_stat, expected=-12.45, tolerance=0.1):
    """
    Check if calculated t-statistic is correct.
    
    Args:
        t_stat (float): Calculated t-statistic
        expected (float): Expected t-statistic (-12.45)
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if t-statistic is within tolerance of expected value
    """
    if t_stat is None:
        return False
    return abs(t_stat - expected) <= tolerance

def check_p_value(p_val, expected=2.97e-7, tolerance=1e-6):
    """
    Check if calculated p-value is correct.
    
    Args:
        p_val (float): Calculated p-value
        expected (float): Expected p-value (2.97e-7)
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if p-value is within tolerance of expected value
    """
    if p_val is None:
        return False
    return abs(p_val - expected) <= tolerance

def check_conclusion(reject_null):
    """
    Check if conclusion about null hypothesis is correct.
    
    Args:
        reject_null (bool): True if null hypothesis was rejected
        
    Returns:
        bool: True if conclusion is correct
    """
    if reject_null is None:
        return False
    return reject_null is True  # We should reject H₀ in this case

def check_assumptions(times):
    """
    Check if test assumptions are satisfied.
    
    Args:
        times (array): Array of processing times
        
    Returns:
        dict: Dictionary with assumption test results
    """
    if times is None or len(times) == 0:
        return {'normality': False, 'independence': False}
        
    # Shapiro-Wilk test for normality
    _, norm_p = stats.shapiro(times)
    
    # Basic independence check (no autocorrelation)
    if len(times) > 1:
        autocorr = np.corrcoef(times[:-1], times[1:])[0,1]
        indep = abs(autocorr) < 0.5
    else:
        indep = False
    
    return {
        'normality': norm_p > 0.05,
        'independence': indep
    }

def calculate_power(effect_size=0.8, alpha=0.05, n=10):
    """
    Calculate power of the test.
    
    Args:
        effect_size (float): Cohen's d effect size
        alpha (float): Significance level
        n (int): Sample size
        
    Returns:
        float: Power of the test
    """
    return stats.t.sf(
        stats.t.ppf(1-alpha, df=n-1),
        df=n-1,
        nc=effect_size*np.sqrt(n)
    )
