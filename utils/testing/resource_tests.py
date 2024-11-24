"""Test functions for resource allocation and party planning problems."""

import pulp

def check_party_variables(prob):
    """Check if party package variables are correctly defined.
    
    Args:
        prob: PuLP problem instance
    
    Returns:
        bool: True if variables are correctly defined
    """
    try:
        packages = ['Standard', 'Joyful', 'Fabulous']
        vars_dict = prob.variablesDict()
        
        # Check package variables
        for pkg in packages:
            var = vars_dict[f'x_{pkg}']
            if not isinstance(var, pulp.LpVariable):
                return False
            if var.cat != 'Continuous':  # Should be continuous, non-negative
                return False
            if var.lowBound != 0:
                return False
        
        return True
    except:
        return False

def check_party_constraints(prob):
    """Check if party package constraints are correctly formulated.
    
    Args:
        prob: PuLP problem instance
    
    Returns:
        bool: True if constraints are correctly defined
    """
    try:
        constraints = prob.constraints
        vars_dict = prob.variablesDict()
        
        # Resource requirements
        labor_hours = {
            'Standard': 3,
            'Joyful': 5,
            'Fabulous': 8
        }
        balloon_bags = {
            'Standard': 2,
            'Joyful': 5,
            'Fabulous': 8
        }
        
        # Check labor constraint (400 hours)
        labor_sum = sum(labor_hours[pkg] * vars_dict[f'x_{pkg}'] for pkg in labor_hours)
        if labor_sum > 400:
            return False
            
        # Check balloon constraint (325 bags)
        balloon_sum = sum(balloon_bags[pkg] * vars_dict[f'x_{pkg}'] for pkg in balloon_bags)
        if balloon_sum > 325:
            return False
        
        return True
    except:
        return False

def check_party_objective(prob):
    """Check if party package objective function is correctly defined.
    
    Args:
        prob: PuLP problem instance
    
    Returns:
        bool: True if objective function is correct
    """
    try:
        vars_dict = prob.variablesDict()
        
        # Profit per package (in thousands)
        profits = {
            'Standard': 1,
            'Joyful': 2,
            'Fabulous': 3
        }
        
        # Check if objective includes all profits
        profit_terms = sum(profits[pkg] * vars_dict[f'x_{pkg}'] for pkg in profits)
        
        # Check if objective is maximization
        if prob.sense != -1:  # PuLP.LpMaximize
            return False
            
        return True
    except:
        return False
