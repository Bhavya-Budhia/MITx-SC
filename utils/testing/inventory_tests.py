"""Test functions for inventory management problems."""
import numpy as np
from scipy import stats

def check_service_level(units, target_level, mean=75, std_dev=25, tolerance=0.01):
    """
    Check if calculated service level is correct.
    
    Args:
        units (int): Number of units to stock
        target_level (float): Target service level (e.g., 0.90 for 90%)
        mean (float): Mean demand
        std_dev (float): Standard deviation of demand
        tolerance (float): Acceptable difference from target
        
    Returns:
        bool: True if service level is within tolerance of target
    """
    z_score = (units - mean) / std_dev
    achieved_level = stats.norm.cdf(z_score)
    return abs(achieved_level - target_level) <= tolerance

def check_z_score(z_score, expected_z, tolerance=0.01):
    """
    Check if calculated z-score is correct.
    
    Args:
        z_score (float): Calculated z-score
        expected_z (float): Expected z-score
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if z-score is within tolerance of expected value
    """
    return abs(z_score - expected_z) <= tolerance

def check_two_stage_system(store_stock, warehouse_stock, mean=75, std_dev=25):
    """
    Check probabilities for two-stage inventory system.
    
    Args:
        store_stock (int): Units in store
        warehouse_stock (int): Units in warehouse
        mean (float): Mean demand
        std_dev (float): Standard deviation of demand
        
    Returns:
        dict: Dictionary with calculated probabilities
    """
    z_store = (store_stock - mean) / std_dev
    z_total = (store_stock + warehouse_stock - mean) / std_dev
    
    # Probability of meeting demand from store stock
    p_store = stats.norm.cdf(z_store)
    
    # Probability of needing warehouse but not exceeding total
    p_warehouse = stats.norm.cdf(z_total) - stats.norm.cdf(z_store)
    
    # Probability of stockout
    p_stockout = 1 - stats.norm.cdf(z_total)
    
    return {
        'store_sufficient': p_store,
        'warehouse_needed': p_warehouse,
        'total_stockout': p_stockout
    }

def verify_inventory_levels(levels, mean=75, std_dev=25):
    """
    Verify that inventory levels are reasonable.
    
    Args:
        levels (dict): Dictionary with inventory levels
        mean (float): Mean demand
        std_dev (float): Standard deviation of demand
        
    Returns:
        bool: True if levels are reasonable
    """
    # Check if levels are within reasonable range (mean ± 4 std dev)
    for level in levels.values():
        if level < mean - 4*std_dev or level > mean + 4*std_dev:
            return False
    return True
