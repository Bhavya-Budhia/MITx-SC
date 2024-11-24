"""Test functions for cost accounting and analysis problems."""

def check_activity_costs(activity_costs, total_cost):
    """Check if activity costs are correctly calculated.
    
    Args:
        activity_costs: Dictionary of activity costs
        total_cost: Total cost to compare against
    
    Returns:
        bool: True if costs are correctly calculated
    """
    try:
        # Expected cost components
        expected_components = {
            'order_entry',
            'warehouse_handling',
            'delivery',
            'freight'
        }
        
        # Check if all components are present
        if not all(comp in activity_costs for comp in expected_components):
            return False
            
        # Check if costs sum to total
        cost_sum = sum(activity_costs.values())
        if abs(cost_sum - total_cost) > 0.01:  # Allow for small rounding differences
            return False
            
        return True
    except:
        return False

def check_customer_profitability(revenue, costs):
    """Check if customer profitability analysis is correct.
    
    Args:
        revenue: Dictionary of revenue by customer
        costs: Dictionary of costs by customer
    
    Returns:
        bool: True if profitability is correctly calculated
    """
    try:
        # Check if same customers in both dictionaries
        if set(revenue.keys()) != set(costs.keys()):
            return False
            
        # Check if values are non-negative
        if any(v < 0 for v in revenue.values()) or any(v < 0 for v in costs.values()):
            return False
            
        # Calculate profitability
        profitability = {
            cust: revenue[cust] - costs[cust]
            for cust in revenue
        }
        
        return True
    except:
        return False

def check_cost_allocation(total_cost, cost_drivers, activities):
    """Check if cost allocation to activities is correct.
    
    Args:
        total_cost: Total cost to allocate
        cost_drivers: Dictionary of cost driver volumes
        activities: Dictionary of activity data
    
    Returns:
        bool: True if allocation is correct
    """
    try:
        # Check if all activities have cost drivers
        if set(activities.keys()) != set(cost_drivers.keys()):
            return False
            
        # Calculate allocated costs
        allocated_costs = {
            activity: (activities[activity]['rate'] * cost_drivers[activity])
            for activity in activities
        }
        
        # Check if allocation sums to total
        total_allocated = sum(allocated_costs.values())
        if abs(total_allocated - total_cost) > 0.01:  # Allow for small rounding differences
            return False
            
        return True
    except:
        return False
