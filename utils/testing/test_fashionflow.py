import pytest
import pulp
import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to the path so we can import the notebooks
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def test_fashionflow_data_structures():
    """Test that the data structures in the FashionFlow problem are valid"""
    # Import the dictionaries from the notebook
    from optimization.network.fashionflow.fashionflow_solution import (
        inbound_dict, outbound_dict, demand_dict, capacity_dict
    )
    
    # Test data structure completeness
    products = ['Premium', 'Casual']
    factories = [f'Factory {i}' for i in range(1, 6)]
    crossdocks = [f'CrossDock {i}' for i in range(1, 3)]
    distribution = [f'DC {i}' for i in range(1, 6)]
    
    # Test inbound dictionary
    for product in products:
        assert product in inbound_dict, f"Product {product} missing from inbound_dict"
        for factory in factories:
            assert factory in inbound_dict[product], f"Factory {factory} missing for {product} in inbound_dict"
            for dock in crossdocks:
                assert dock in inbound_dict[product][factory], f"CrossDock {dock} missing for {factory}, {product}"
                assert isinstance(inbound_dict[product][factory][dock], (int, float)), "Cost should be numeric"
                assert inbound_dict[product][factory][dock] >= 0, "Cost should be non-negative"
                
    # Test outbound dictionary
    for product in products:
        assert product in outbound_dict, f"Product {product} missing from outbound_dict"
        for dock in crossdocks:
            assert dock in outbound_dict[product], f"CrossDock {dock} missing for {product} in outbound_dict"
            for dc in distribution:
                assert dc in outbound_dict[product][dock], f"DC {dc} missing for {dock}, {product}"
                assert isinstance(outbound_dict[product][dock][dc], (int, float)), "Cost should be numeric"
                assert outbound_dict[product][dock][dc] >= 0, "Cost should be non-negative"
                
    # Test demand dictionary
    for product in products:
        assert product in demand_dict, f"Product {product} missing from demand_dict"
        for dc in distribution:
            assert dc in demand_dict[product], f"DC {dc} missing for {product} in demand_dict"
            assert isinstance(demand_dict[product][dc], (int, float)), "Demand should be numeric"
            assert demand_dict[product][dc] >= 0, "Demand should be non-negative"
            
    # Test capacity dictionary
    assert all(product in capacity_dict for product in products + ['Combined']), "Missing product types in capacity_dict"
    for product in products + ['Combined']:
        for factory in factories:
            assert factory in capacity_dict[product], f"Factory {factory} missing for {product} in capacity_dict"
            assert isinstance(capacity_dict[product][factory], (int, float)), "Capacity should be numeric"
            assert capacity_dict[product][factory] >= 0, "Capacity should be non-negative"

def test_solution_feasibility():
    """Test that the solution satisfies all constraints"""
    try:
        from optimization.network.fashionflow.fashionflow_solution import (
            prob, factory_to_dock, dock_to_dc,
            inbound_dict, outbound_dict, demand_dict, capacity_dict
        )
        
        # Check if solution exists
        assert prob.status == pulp.LpStatusOptimal, "Problem should have an optimal solution"
        
        products = ['Premium', 'Casual']
        factories = [f'Factory {i}' for i in range(1, 6)]
        crossdocks = [f'CrossDock {i}' for i in range(1, 3)]
        distribution = [f'DC {i}' for i in range(1, 6)]
        
        # Test flow conservation at cross-docks
        for product in products:
            for dock in crossdocks:
                inflow = sum(factory_to_dock[product][factory][dock].value() 
                           for factory in factories)
                outflow = sum(dock_to_dc[product][dock][dc].value() 
                            for dc in distribution)
                assert abs(inflow - outflow) < 1e-6, f"Flow conservation violated at {dock} for {product}"
        
        # Test demand satisfaction
        for product in products:
            for dc in distribution:
                received = sum(dock_to_dc[product][dock][dc].value() 
                             for dock in crossdocks)
                assert abs(received - demand_dict[product][dc]) < 1e-6, \
                    f"Demand not met at {dc} for {product}"
        
        # Test capacity constraints
        for factory in factories:
            total_premium = sum(factory_to_dock['Premium'][factory][dock].value() 
                              for dock in crossdocks)
            total_casual = sum(factory_to_dock['Casual'][factory][dock].value() 
                             for dock in crossdocks)
            
            assert total_premium <= capacity_dict['Premium'][factory] + 1e-6, \
                f"Premium capacity exceeded at {factory}"
            assert total_casual <= capacity_dict['Casual'][factory] + 1e-6, \
                f"Casual capacity exceeded at {factory}"
            assert total_premium + total_casual <= capacity_dict['Combined'][factory] + 1e-6, \
                f"Combined capacity exceeded at {factory}"

    except ImportError:
        pytest.skip("Solution notebook not available or not completed")

def test_solution_optimality():
    """Test that the solution is optimal by checking KKT conditions"""
    try:
        from optimization.network.fashionflow.fashionflow_solution import (
            prob, factory_to_dock, dock_to_dc,
            inbound_dict, outbound_dict
        )
        
        if prob.status != pulp.LpStatusOptimal:
            pytest.skip("Solution is not optimal, skipping optimality tests")
            
        # Get dual values (shadow prices) for constraints
        dual_values = {name: constraint.pi for name, constraint in prob.constraints.items()}
        
        # Check complementary slackness
        # This is a simplified check - in practice, we'd need to check all KKT conditions
        for constraint in prob.constraints.values():
            slack = constraint.slack
            dual = constraint.pi
            # Either slack is 0 or dual is 0 (allowing for numerical precision)
            assert abs(slack * dual) < 1e-6, "Complementary slackness condition violated"
            
        # Check reduced costs for non-basic variables
        # In an optimal solution, reduced costs should be non-negative for non-basic variables at their lower bound
        # and non-positive for non-basic variables at their upper bound
        for var in prob.variables():
            if abs(var.value()) < 1e-6:  # Variable at lower bound
                assert var.dj >= -1e-6, f"Reduced cost condition violated for {var.name}"
                
    except (ImportError, AttributeError):
        pytest.skip("Solution notebook not available or PuLP version doesn't support duals")
