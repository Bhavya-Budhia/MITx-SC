"""Test functions for GameStop Pre-order Bonus Analysis."""
import numpy as np
from scipy import stats

def check_single_event_prob(prob, expected=0.2167, tolerance=0.001):
    """
    Check if probability of getting a Rare Weapons card is correct.
    
    Args:
        prob (float): Calculated probability (should be 65/300)
        expected (float): Expected probability (0.2167)
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if probability is within tolerance of expected value
    """
    if prob is None:
        return False
    return abs(prob - expected) <= tolerance

def check_conditional_prob(prob, expected=0.2131, tolerance=0.001):
    """
    Check probability of getting a second Rare Weapons card given first was Rare Weapons.
    
    Args:
        prob (float): Calculated probability (should be 64/299)
        expected (float): Expected probability (0.2131)
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if probability is within tolerance of expected value
    """
    if prob is None:
        return False
    return abs(prob - expected) <= tolerance

def check_multiple_event_prob(prob, expected=0.0183, tolerance=0.001):
    """
    Check probability of getting 2 Epic Locations and 1 Boss Battles card in 3 draws.
    
    Args:
        prob (float): Calculated probability
        expected (float): Expected probability (0.0183)
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if probability is within tolerance of expected value
    """
    if prob is None:
        return False
    return abs(prob - expected) <= tolerance

def calculate_combination(n, r):
    """
    Calculate combination (n choose r) for multiple card draws.
    
    Args:
        n (int): Total number of cards
        r (int): Number of cards to draw
        
    Returns:
        int: Number of possible combinations
    """
    return int(stats.comb(n, r))

def verify_probability_sum(probs, tolerance=0.001):
    """
    Verify that probabilities sum to approximately 1.
    
    Args:
        probs (list): List of probabilities for all possible card types
        tolerance (float): Acceptable difference from 1
        
    Returns:
        bool: True if sum is approximately 1
    """
    if not probs:
        return False
    return abs(sum(probs) - 1.0) <= tolerance
