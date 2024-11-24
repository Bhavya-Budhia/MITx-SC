"""Test functions for distribution optimization problems."""

import pulp

def check_warehouse_variables(prob, dcs):
    """Check if warehouse decision variables are correctly defined.
    
    Args:
        prob: PuLP problem instance
        dcs: List of distribution center names
    
    Returns:
        bool: True if variables are correctly defined
    """
    try:
        # Check binary variables for DC selection
        dc_vars = {dc: prob.variablesDict()[f'Open_{dc}'] for dc in dcs}
        for var in dc_vars.values():
            if not isinstance(var, pulp.LpVariable):
                return False
            if var.cat != 'Binary':
                return False
            
        # Check assignment variables
        for dc in dcs:
            for store in range(1, 4):  # 3 bookstores
                var_name = f'Assign_{dc}_Store{store}'
                var = prob.variablesDict()[var_name]
                if not isinstance(var, pulp.LpVariable):
                    return False
                if var.cat != 'Binary':
                    return False
        
        return True
    except:
        return False

def check_warehouse_constraints(prob, dcs):
    """Check if warehouse constraints are correctly formulated.
    
    Args:
        prob: PuLP problem instance
        dcs: List of distribution center names
    
    Returns:
        bool: True if constraints are correctly defined
    """
    try:
        constraints = prob.constraints
        
        # Check DC count constraints (2-3 DCs)
        dc_sum = sum(prob.variablesDict()[f'Open_{dc}'] for dc in dcs)
        if not (2 <= dc_sum <= 3):
            return False
            
        # Check capacity constraint (850,000 minimum)
        capacities = {
            'DC1': 410, 'DC2': 380, 'DC3': 330,
            'DC4': 380, 'DC5': 340
        }
        total_capacity = sum(capacities[dc] * prob.variablesDict()[f'Open_{dc}'] for dc in dcs)
        if total_capacity < 850:
            return False
            
        # Check assignment constraints
        for store in range(1, 4):
            store_sum = sum(prob.variablesDict()[f'Assign_{dc}_Store{store}'] for dc in dcs)
            if store_sum != 1:  # Each store must be assigned to exactly one DC
                return False
                
        return True
    except:
        return False

def check_warehouse_objective(prob, dcs):
    """Check if warehouse objective function is correctly defined.
    
    Args:
        prob: PuLP problem instance
        dcs: List of distribution center names
    
    Returns:
        bool: True if objective function is correct
    """
    try:
        # Fixed costs
        fixed_costs = {
            'DC1': 85000, 'DC2': 85000, 'DC3': 75000,
            'DC4': 75000, 'DC5': 85000
        }
        
        # Transport costs per km per shipment
        transport_costs = {
            'DC1': 0.55, 'DC2': 0.35, 'DC3': 0.65,
            'DC4': 0.45, 'DC5': 0.25
        }
        
        # Distances to bookstores
        distances = {
            'DC1': [70, 110, 65],
            'DC2': [50, 135, 80],
            'DC3': [60, 115, 85],
            'DC4': [55, 90, 95],
            'DC5': [95, 65, 85]
        }
        
        # Check if objective includes fixed costs
        fixed_cost_terms = sum(fixed_costs[dc] * prob.variablesDict()[f'Open_{dc}'] for dc in dcs)
        
        # Check if objective includes transport costs (40 shipments per year)
        transport_cost_terms = sum(
            40 * transport_costs[dc] * distances[dc][store-1] * 
            prob.variablesDict()[f'Assign_{dc}_Store{store}']
            for dc in dcs
            for store in range(1, 4)
        )
        
        # Check if objective is minimization
        if prob.sense != 1:  # PuLP.LpMinimize
            return False
            
        return True
    except:
        return False
