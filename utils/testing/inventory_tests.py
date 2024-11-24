"""Test functions for inventory management problems."""
import numpy as np
from scipy import stats

def check_service_level(units, target_level, mean=75, std_dev=25, tolerance=0.01):
    """
    Check if calculated service level for RayMaster sunglasses is correct.
    
    Args:
        units (int): Number of sunglasses to stock
        target_level (float): Target service level (e.g., 0.90 for 90%)
        mean (float): Mean demand (75 units)
        std_dev (float): Standard deviation of demand (25 units)
        tolerance (float): Acceptable difference from target
        
    Returns:
        bool: True if service level is within tolerance of target
    """
    z_score = (units - mean) / std_dev
    achieved_level = stats.norm.cdf(z_score)
    return abs(achieved_level - target_level) <= tolerance

def check_z_score(z_score, expected_z=0.6, tolerance=0.01):
    """
    Check if calculated z-score for inventory level is correct.
    
    Args:
        z_score (float): Calculated z-score
        expected_z (float): Expected z-score (0.6 for k=90)
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if z-score is within tolerance of expected value
    """
    return abs(z_score - expected_z) <= tolerance

def check_two_stage_system(store_stock, warehouse_stock, mean=75, std_dev=25):
    """
    Check probabilities for two-stage inventory system.
    
    Args:
        store_stock (int): Units in store (80)
        warehouse_stock (int): Units in warehouse (40)
        mean (float): Mean demand (75 units)
        std_dev (float): Standard deviation of demand (25 units)
        
    Returns:
        dict: Dictionary with calculated probabilities
    """
    # Store level calculations
    z_store = (store_stock - mean) / std_dev
    p_store = stats.norm.cdf(z_store)
    
    # Total system calculations
    z_total = (store_stock + warehouse_stock - mean) / std_dev
    p_total = stats.norm.cdf(z_total)
    
    # Warehouse needed but sufficient
    p_warehouse = p_total - p_store
    
    # Total stockout probability
    p_stockout = 1 - p_total
    
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
        mean (float): Mean demand (75 units)
        std_dev (float): Standard deviation of demand (25 units)
        
    Returns:
        bool: True if levels are reasonable
    """
    # Check if levels are within reasonable range (mean ± 4 std dev)
    for level in levels.values():
        if level < mean - 4*std_dev or level > mean + 4*std_dev:
            return False
    return True

def check_eoq_calculation(eoq, D=1200, S=100, H=20, tolerance=1.0):
    """
    Check if EOQ calculation is correct.
    
    Args:
        eoq (float): Calculated EOQ
        D (float): Annual demand
        S (float): Ordering cost
        H (float): Holding cost
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if EOQ is within tolerance of expected value
    """
    expected_eoq = np.sqrt(2 * D * S / H)
    return abs(eoq - expected_eoq) <= tolerance

def check_total_cost(total_cost, Q, D=1200, S=100, H=20, tolerance=1.0):
    """
    Check if total cost calculation is correct.
    
    Args:
        total_cost (float): Calculated total cost
        Q (float): Order quantity
        D (float): Annual demand
        S (float): Ordering cost
        H (float): Holding cost
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if total cost is within tolerance of expected value
    """
    expected_cost = (D * S / Q) + (H * Q / 2)
    return abs(total_cost - expected_cost) <= tolerance

def check_reorder_point(rop, daily_demand, lead_time_days, safety_stock=0, tolerance=1.0):
    """
    Check if reorder point calculation is correct.
    
    Args:
        rop (float): Calculated reorder point
        daily_demand (float): Daily demand rate
        lead_time_days (float): Lead time in days
        safety_stock (float): Safety stock level
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if reorder point is within tolerance of expected value
    """
    expected_rop = (daily_demand * lead_time_days) + safety_stock
    return abs(rop - expected_rop) <= tolerance

def check_abc_classification(categories, volumes):
    """
    Check if ABC classification is correct.
    
    Args:
        categories (dict): Dictionary with category assignments
        volumes (dict): Dictionary with annual dollar volumes
        
    Returns:
        bool: True if classification is correct
    """
    total_volume = sum(volumes.values())
    
    # Calculate volume per category
    cat_volumes = {
        'A': sum(volumes[p] for p in categories if categories[p] == 'A'),
        'B': sum(volumes[p] for p in categories if categories[p] == 'B'),
        'C': sum(volumes[p] for p in categories if categories[p] == 'C')
    }
    
    # Calculate percentages
    a_percent = cat_volumes['A'] / total_volume
    b_percent = cat_volumes['B'] / total_volume
    c_percent = cat_volumes['C'] / total_volume
    
    # Check if percentages are within acceptable ranges
    return (
        0.70 <= a_percent <= 0.80 and
        0.15 <= b_percent <= 0.20 and
        0.05 <= c_percent <= 0.10
    )

def check_category_metrics(metrics, category):
    """
    Check if category metrics are reasonable.
    
    Args:
        metrics (dict): Dictionary with category metrics
        category (str): Category to check ('A', 'B', or 'C')
        
    Returns:
        bool: True if metrics are reasonable
    """
    # Expected ranges for different metrics
    ranges = {
        'A': {
            'review_freq_days': (1, 7),
            'service_level': (0.95, 0.99),
            'safety_stock_days': (3, 10)
        },
        'B': {
            'review_freq_days': (7, 14),
            'service_level': (0.90, 0.95),
            'safety_stock_days': (7, 14)
        },
        'C': {
            'review_freq_days': (30, 90),
            'service_level': (0.85, 0.90),
            'safety_stock_days': (14, 30)
        }
    }
    
    # Check if metrics are within expected ranges
    cat_ranges = ranges[category]
    for metric, (min_val, max_val) in cat_ranges.items():
        if metric in metrics:
            if metrics[metric] < min_val or metrics[metric] > max_val:
                return False
    return True

def check_safety_stock(safety_stock, demand_mean, demand_std, lead_time, service_level, tolerance=0.1):
    """
    Check if safety stock calculation is correct.
    
    Args:
        safety_stock (float): Calculated safety stock
        demand_mean (float): Mean daily demand
        demand_std (float): Standard deviation of daily demand
        lead_time (float): Lead time in days
        service_level (float): Target service level (e.g., 0.95)
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if safety stock is within tolerance of expected value
    """
    z_score = stats.norm.ppf(service_level)
    expected_ss = z_score * demand_std * np.sqrt(lead_time)
    return abs(safety_stock - expected_ss) <= tolerance * expected_ss

def check_variable_leadtime_ss(safety_stock, demand_mean, demand_std, lt_mean, lt_std, 
                             service_level, tolerance=0.1):
    """
    Check safety stock calculation with variable lead time.
    
    Args:
        safety_stock (float): Calculated safety stock
        demand_mean (float): Mean daily demand
        demand_std (float): Standard deviation of daily demand
        lt_mean (float): Mean lead time
        lt_std (float): Standard deviation of lead time
        service_level (float): Target service level
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if safety stock is within tolerance of expected value
    """
    z_score = stats.norm.ppf(service_level)
    expected_ss = z_score * np.sqrt(lt_mean * demand_std**2 + demand_mean**2 * lt_std**2)
    return abs(safety_stock - expected_ss) <= tolerance * expected_ss

def check_multi_product_ss(safety_stocks, products, service_level=0.95, tolerance=0.1):
    """
    Check safety stock calculations for multiple products.
    
    Args:
        safety_stocks (dict): Dictionary of calculated safety stocks by product
        products (dict): Dictionary of product parameters
        service_level (float): Target service level
        tolerance (float): Acceptable difference from expected values
        
    Returns:
        bool: True if all safety stocks are within tolerance
    """
    for product, ss in safety_stocks.items():
        if product not in products:
            return False
            
        params = products[product]
        expected_ss = stats.norm.ppf(service_level) * params['demand_std'] * \
                     np.sqrt(params.get('lead_time', 3))
                     
        if abs(ss - expected_ss) > tolerance * expected_ss:
            return False
            
    return True

def check_reorder_point_basic(rop, demand_mean, lead_time, safety_stock=0, tolerance=0.1):
    """
    Check basic reorder point calculation.
    
    Args:
        rop (float): Calculated reorder point
        demand_mean (float): Mean daily demand
        lead_time (float): Lead time in days
        safety_stock (float): Safety stock level
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if reorder point is within tolerance of expected value
    """
    expected_rop = (demand_mean * lead_time) + safety_stock
    return abs(rop - expected_rop) <= tolerance * expected_rop

def check_reorder_point_variable(rop, demand_mean, demand_std, lt_mean, lt_std, 
                               service_level, tolerance=0.1):
    """
    Check reorder point calculation with variable lead time.
    
    Args:
        rop (float): Calculated reorder point
        demand_mean (float): Mean daily demand
        demand_std (float): Standard deviation of daily demand
        lt_mean (float): Mean lead time
        lt_std (float): Standard deviation of lead time
        service_level (float): Target service level
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if reorder point is within tolerance of expected value
    """
    z_score = stats.norm.ppf(service_level)
    safety_stock = z_score * np.sqrt(lt_mean * demand_std**2 + demand_mean**2 * lt_std**2)
    expected_rop = (demand_mean * lt_mean) + safety_stock
    return abs(rop - expected_rop) <= tolerance * expected_rop

def check_multi_part_rop(reorder_points, parts, service_level=0.98, tolerance=0.1):
    """
    Check reorder point calculations for multiple parts.
    
    Args:
        reorder_points (dict): Dictionary of calculated reorder points by part
        parts (dict): Dictionary of part parameters
        service_level (float): Target service level
        tolerance (float): Acceptable difference from expected values
        
    Returns:
        bool: True if all reorder points are within tolerance
    """
    for part, rop in reorder_points.items():
        if part not in parts:
            return False
            
        params = parts[part]
        z_score = stats.norm.ppf(service_level)
        safety_stock = z_score * params['demand_std'] * np.sqrt(params['lead_time'])
        expected_rop = (params['demand_mean'] * params['lead_time']) + safety_stock
        
        if abs(rop - expected_rop) > tolerance * expected_rop:
            return False
            
    return True

def check_stockout_probability(stockout_prob, rop, demand_mean, demand_std, lead_time, tolerance=0.001):
    """
    Check stockout probability calculation.
    
    Args:
        stockout_prob (float): Calculated stockout probability
        rop (float): Reorder point
        demand_mean (float): Mean daily demand
        demand_std (float): Standard deviation of daily demand
        lead_time (float): Lead time in days
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if probability is within tolerance of expected value
    """
    lt_demand_mean = demand_mean * lead_time
    lt_demand_std = demand_std * np.sqrt(lead_time)
    z_score = (rop - lt_demand_mean) / lt_demand_std
    expected_prob = 1 - stats.norm.cdf(z_score)
    return abs(stockout_prob - expected_prob) <= tolerance
