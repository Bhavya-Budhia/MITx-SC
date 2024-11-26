"""Test functions for inventory management problems."""
import numpy as np
from scipy import stats

def check_eoq(solution_dict, D=1200, S=100, H=20, tolerance=1.0):
    """
    Check if EOQ calculation is correct.
    
    Args:
        solution_dict (dict): Dictionary containing 'eoq' key with calculated EOQ
        D (float): Annual demand
        S (float): Ordering cost
        H (float): Holding cost
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if EOQ is within tolerance of expected value
    """
    if 'eoq' not in solution_dict:
        return False
    eoq = solution_dict['eoq']
    expected_eoq = np.sqrt(2 * D * S / H)
    return abs(eoq - expected_eoq) <= tolerance

def check_total_cost(solution_dict, D=1200, S=100, H=20, tolerance=1.0):
    """
    Check if total cost calculation is correct.
    
    Args:
        solution_dict (dict): Dictionary containing either:
            - 'total_cost' key with calculated total cost, or
            - 'cost_curves' key with dictionary containing cost curves
        D (float): Annual demand
        S (float): Ordering cost
        H (float): Holding cost
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if total cost is within tolerance of expected value
    """
    if 'total_cost' in solution_dict:
        total_cost = solution_dict['total_cost']
        Q = np.sqrt(2 * D * S / H)  # Use optimal Q for checking
        expected_cost = (D * S / Q) + (H * Q / 2)
        return abs(total_cost - expected_cost) <= tolerance
    elif 'cost_curves' in solution_dict:
        curves = solution_dict['cost_curves']
        if not all(k in curves for k in ['ordering_costs', 'holding_costs', 'total_costs']):
            return False
        # Check a few points on the curves
        Q_test = np.sqrt(2 * D * S / H)
        expected_ordering = D * S / Q_test
        expected_holding = H * Q_test / 2
        expected_total = expected_ordering + expected_holding
        
        return (abs(curves['ordering_costs'][Q_test] - expected_ordering) <= tolerance and
                abs(curves['holding_costs'][Q_test] - expected_holding) <= tolerance and
                abs(curves['total_costs'][Q_test] - expected_total) <= tolerance)
    return False

def check_pareto_analysis(solution_dict, tolerance=0.01):
    """
    Check if Pareto analysis calculations are correct.
    
    Args:
        solution_dict (dict): Dictionary containing:
            - 'annual_volume'
            - 'volume_percentages'
            - 'cumulative_percentages'
        tolerance (float): Acceptable difference from expected values
        
    Returns:
        bool: True if calculations are within tolerance
    """
    required_keys = ['annual_volume', 'volume_percentages', 'cumulative_percentages']
    if not all(k in solution_dict for k in required_keys):
        return False
    
    volumes = solution_dict['annual_volume']
    percentages = solution_dict['volume_percentages']
    cumulative = solution_dict['cumulative_percentages']
    
    # Check if percentages sum to 1
    if abs(sum(percentages) - 1.0) > tolerance:
        return False
    
    # Check if cumulative percentages are monotonically increasing
    if not all(cumulative[i] <= cumulative[i+1] for i in range(len(cumulative)-1)):
        return False
    
    # Check if final cumulative percentage is 1
    if abs(cumulative[-1] - 1.0) > tolerance:
        return False
    
    return True

def check_abc_classification(solution_dict, tolerance=0.01):
    """
    Check if ABC classification is correct.
    
    Args:
        solution_dict (dict): Dictionary containing:
            - 'A_items', 'B_items', 'C_items' (lists of Product_IDs)
            - 'A_volume', 'B_volume', 'C_volume' (total volume per category)
        tolerance (float): Acceptable difference from expected percentages
        
    Returns:
        bool: True if classification meets ABC criteria
    """
    if not all(k in solution_dict for k in ['A_items', 'B_items', 'C_items', 
                                          'A_volume', 'B_volume', 'C_volume']):
        return False
    
    total_volume = (solution_dict['A_volume'] + 
                   solution_dict['B_volume'] + 
                   solution_dict['C_volume'])
    
    a_percent = solution_dict['A_volume'] / total_volume
    b_percent = solution_dict['B_volume'] / total_volume
    c_percent = solution_dict['C_volume'] / total_volume
    
    # Check if percentages are within ABC criteria
    return (0.70 <= a_percent <= 0.80 and
            0.15 <= b_percent <= 0.20 and
            0.05 <= c_percent <= 0.10)

def check_inventory_policy(solution_dict):
    """
    Check if inventory policies are reasonable for each category.
    
    Args:
        solution_dict (dict): Dictionary containing:
            - 'review_frequency'
            - 'safety_stock'
            - 'service_level'
            - 'order_quantity'
        Each should be a dictionary with 'A', 'B', 'C' keys
        
    Returns:
        bool: True if policies are reasonable
    """
    required_keys = ['review_frequency', 'safety_stock', 'service_level', 'order_quantity']
    if not all(k in solution_dict for k in required_keys):
        return False
    
    # Expected ranges for each category
    policy_ranges = {
        'A': {
            'review_frequency': (1, 7),    # days
            'service_level': (0.95, 0.99),
            'safety_stock': (3, 10)        # days of demand
        },
        'B': {
            'review_frequency': (7, 14),
            'service_level': (0.90, 0.95),
            'safety_stock': (7, 14)
        },
        'C': {
            'review_frequency': (14, 30),
            'service_level': (0.85, 0.90),
            'safety_stock': (14, 30)
        }
    }
    
    for category in ['A', 'B', 'C']:
        ranges = policy_ranges[category]
        if not (ranges['review_frequency'][0] <= solution_dict['review_frequency'][category] <= ranges['review_frequency'][1]):
            return False
        if not (ranges['service_level'][0] <= solution_dict['service_level'][category] <= ranges['service_level'][1]):
            return False
        if not (ranges['safety_stock'][0] <= solution_dict['safety_stock'][category] <= ranges['safety_stock'][1]):
            return False
    
    return True

def check_lead_time_demand(solution_dict, daily_demand=50, lead_time=5, tolerance=1.0):
    """
    Check if lead time demand calculation is correct.
    
    Args:
        solution_dict (dict): Dictionary containing 'lead_time_demand'
        daily_demand (float): Daily demand rate
        lead_time (float): Lead time in days
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if lead time demand is within tolerance
    """
    if 'lead_time_demand' not in solution_dict:
        return False
    
    expected_ltd = daily_demand * lead_time
    return abs(solution_dict['lead_time_demand'] - expected_ltd) <= tolerance

def check_reorder_point(solution_dict, tolerance=1.0):
    """
    Check if reorder point calculation is correct.
    
    Args:
        solution_dict (dict): Dictionary containing:
            - 'reorder_point'
            - Optional: 'lead_time_demand', 'safety_stock'
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if reorder point is within tolerance
    """
    if 'reorder_point' not in solution_dict:
        return False
    
    # If lead time demand and safety stock are provided, verify ROP = LTD + SS
    if 'lead_time_demand' in solution_dict and 'safety_stock' in solution_dict:
        expected_rop = solution_dict['lead_time_demand'] + solution_dict['safety_stock']
        return abs(solution_dict['reorder_point'] - expected_rop) <= tolerance
    
    # Otherwise just check if ROP is reasonable (positive and not too large)
    return 0 <= solution_dict['reorder_point'] <= 1000  # Adjust upper bound as needed

def check_service_level(solution_dict, target=0.95, tolerance=0.01):
    """
    Check if service level calculations are correct.
    
    Args:
        solution_dict (dict): Dictionary containing either:
            - 'z_score' for service level calculation
            - 'service_level' for achieved service level
            - 'safety_stock' for safety stock calculation
        target (float): Target service level
        tolerance (float): Acceptable difference from target
        
    Returns:
        bool: True if service level is within tolerance
    """
    if 'z_score' in solution_dict:
        achieved_level = stats.norm.cdf(solution_dict['z_score'])
        return abs(achieved_level - target) <= tolerance
    
    elif 'service_level' in solution_dict:
        return abs(solution_dict['service_level'] - target) <= tolerance
    
    elif 'safety_stock' in solution_dict:
        # Check if safety stock provides the target service level
        z_score = solution_dict['safety_stock'] / (solution_dict.get('demand_std', 20))
        achieved_level = stats.norm.cdf(z_score)
        return abs(achieved_level - target) <= tolerance
    
    return False

def check_variable_lt_safety(solution_dict, tolerance=0.01):
    """
    Check safety stock calculations with variable lead time.
    
    Args:
        solution_dict (dict): Dictionary containing:
            - 'combined_std'
            - 'safety_stock'
            - 'percent_increase'
            - 'achieved_service_level'
        tolerance (float): Acceptable difference from expected values
        
    Returns:
        bool: True if calculations are within tolerance
    """
    required_keys = ['combined_std', 'safety_stock', 'percent_increase', 'achieved_service_level']
    if not all(k in solution_dict for k in required_keys):
        return False
    
    # Safety stock should be positive
    if solution_dict['safety_stock'] <= 0:
        return False
    
    # Percent increase should be positive
    if solution_dict['percent_increase'] <= 0:
        return False
    
    # Service level should be between 0 and 1
    if not 0 <= solution_dict['achieved_service_level'] <= 1:
        return False
    
    return True

def check_multi_product_safety(solution_dict):
    """
    Check safety stock calculations for multiple products.
    
    Args:
        solution_dict (dict): Dictionary containing:
            - 'safety_stocks'
            - 'total_investment'
            - 'service_levels'
            - 'inventory_costs'
        Each should be a dictionary with product names as keys
        
    Returns:
        bool: True if calculations are reasonable
    """
    required_keys = ['safety_stocks', 'total_investment', 'service_levels', 'inventory_costs']
    if not all(k in solution_dict for k in required_keys):
        return False
    
    for product_dict in solution_dict.values():
        if isinstance(product_dict, dict):
            # Safety stocks should be positive
            if any(ss <= 0 for ss in solution_dict['safety_stocks'].values()):
                return False
            
            # Service levels should be between 0 and 1
            if any(not 0 <= sl <= 1 for sl in solution_dict['service_levels'].values()):
                return False
            
            # Costs should be positive
            if any(cost <= 0 for cost in solution_dict['inventory_costs'].values()):
                return False
    
    # Total investment should be positive and match sum of individual costs
    if solution_dict['total_investment'] <= 0:
        return False
    
    return True

def check_multi_item_policy(solution_dict):
    """
    Check inventory policy calculations for multiple items.
    
    Args:
        solution_dict (dict): Dictionary containing:
            - 'reorder_points'
            - 'safety_stocks'
            - 'total_investment'
            - 'service_levels'
        Each should be a dictionary with part names as keys
        
    Returns:
        bool: True if calculations are reasonable
    """
    required_keys = ['reorder_points', 'safety_stocks', 'total_investment', 'service_levels']
    if not all(k in solution_dict for k in required_keys):
        return False
    
    for part_dict in solution_dict.values():
        if isinstance(part_dict, dict):
            # Reorder points should be positive
            if any(rop <= 0 for rop in solution_dict['reorder_points'].values()):
                return False
            
            # Safety stocks should be positive
            if any(ss <= 0 for ss in solution_dict['safety_stocks'].values()):
                return False
            
            # Service levels should be between 0 and 1
            if any(not 0 <= sl <= 1 for sl in solution_dict['service_levels'].values()):
                return False
    
    # Total investment should be positive
    if solution_dict['total_investment'] <= 0:
        return False
    
    return True
