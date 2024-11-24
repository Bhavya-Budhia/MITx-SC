"""Test functions for probability problems."""
import numpy as np
from scipy import stats

def check_single_event_prob(prob, expected=0.2167, tolerance=0.001):
    """
    Check if calculated single event probability is correct.
    
    Args:
        prob (float): Calculated probability
        expected (float): Expected probability
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if probability is within tolerance of expected value
    """
    return abs(prob - expected) <= tolerance

def check_conditional_prob(prob, expected=0.2131, tolerance=0.001):
    """
    Check if calculated conditional probability is correct.
    
    Args:
        prob (float): Calculated conditional probability
        expected (float): Expected probability
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if probability is within tolerance of expected value
    """
    return abs(prob - expected) <= tolerance

def check_multiple_event_prob(prob, expected=0.0183, tolerance=0.001):
    """
    Check if calculated multiple event probability is correct.
    
    Args:
        prob (float): Calculated multiple event probability
        expected (float): Expected probability
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if probability is within tolerance of expected value
    """
    return abs(prob - expected) <= tolerance

def calculate_combination(n, r):
    """
    Calculate combination (n choose r).
    
    Args:
        n (int): Total number of items
        r (int): Number of items to choose
        
    Returns:
        int: Number of possible combinations
    """
    return np.math.comb(n, r)

def verify_probability_sum(probs):
    """
    Verify that probabilities sum to approximately 1.
    
    Args:
        probs (list): List of probabilities
        
    Returns:
        bool: True if sum is approximately 1
    """
    return abs(sum(probs) - 1.0) < 0.001
