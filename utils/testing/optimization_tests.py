import pulp
import numpy as np

def check_variables(model, vars, use_line):
    """Check if variables are correctly defined"""
    try:
        # Check if model is created correctly
        assert isinstance(model, pulp.LpProblem), "Model should be a PuLP LpProblem"
        assert model.sense == pulp.LpMaximize, "Model should be a maximization problem"
        
        # Check production variables
        production_lines = ['T1', 'M1', 'C', 'T2', 'M2']
        warehouses = ['WH1', 'WH2']
        
        for i in production_lines:
            for j in warehouses:
                assert isinstance(vars[i,j], pulp.LpVariable), f"Variable for {i},{j} should be a PuLP variable"
                assert vars[i,j].lowBound == 0, f"Variable for {i},{j} should have lower bound 0"
                assert vars[i,j].cat == 'Integer', f"Variable for {i},{j} should be Integer"
        
        # Check binary variables
        for line in ['T2', 'M2']:
            assert isinstance(use_line[line], pulp.LpVariable), f"Use line variable for {line} should be a PuLP variable"
            assert use_line[line].cat == 'Binary', f"Use line variable for {line} should be Binary"
        
        print("✓ All variables are correctly defined!")
        return True
    except AssertionError as e:
        print(f"❌ Error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error: Make sure all variables are defined: {str(e)}")
        return False

def check_constraints(model, vars, use_line, capacities):
    """Check if constraints are correctly defined"""
    try:
        production_lines = ['T1', 'M1', 'C', 'T2', 'M2']
        warehouses = ['WH1', 'WH2']
        demands = {'WH1': 6000, 'WH2': 5200}
        
        constraints = list(model.constraints.values())
        
        # Check demand constraints
        demand_constraints = [c for c in constraints if "Demand" in c.name]
        assert len(demand_constraints) == 2, "Should have exactly 2 demand constraints"
        
        # Check capacity constraints
        capacity_constraints = [c for c in constraints if "Capacity" in c.name]
        assert len(capacity_constraints) == 5, "Should have exactly 5 capacity constraints"
        
        # Check optional line constraint
        optional_constraints = [c for c in constraints if "Optional" in c.name]
        assert len(optional_constraints) == 1, "Should have exactly 1 optional line constraint"
        
        # Check linking constraints
        linking_constraints = [c for c in constraints if "Link" in c.name]
        assert len(linking_constraints) == 4, "Should have exactly 4 linking constraints"
        
        print("✓ All constraints are correctly defined!")
        return True
    except AssertionError as e:
        print(f"❌ Error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error: Make sure all constraints are defined: {str(e)}")
        return False

def check_objective(model, vars, use_line, profits, fixed_costs):
    """Check if objective function is correctly defined"""
    try:
        # Get the objective function
        obj = model.objective
        
        # Check if it includes all production variables
        production_lines = ['T1', 'M1', 'C', 'T2', 'M2']
        warehouses = ['WH1', 'WH2']
        
        for i in production_lines:
            for j in warehouses:
                assert any(term.name == vars[i,j].name for term in obj.terms()), f"Objective should include variable for {i},{j}"
        
        # Check if it includes fixed costs
        for line in ['T2', 'M2']:
            assert any(term.name == use_line[line].name for term in obj.terms()), f"Objective should include fixed cost for {line}"
        
        print("✓ Objective function is correctly defined!")
        return True
    except AssertionError as e:
        print(f"❌ Error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error: Make sure objective function is defined: {str(e)}")
        return False
