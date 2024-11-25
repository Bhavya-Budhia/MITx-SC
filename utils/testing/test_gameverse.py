import pytest
import pulp
import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to the path so we can import the notebooks
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

@pytest.mark.skip(reason="Solution file not available in test environment")
def test_gameverse_data_structures():
    """Test that the data structures in the GameVerse problem are valid"""
    # Import the dictionaries from the notebook
    from optimization.network.gameverse.gameverse_solution import (
        inbound_dict, outbound_dict, demand_dict, capacity_dict
    )
    
    # Test data structure completeness
    products = ['Pro', 'Standard']
    factories = [f'Factory {i}' for i in range(1, 6)]
    consolidation = [f'Consolidation {i}' for i in range(1, 3)]
    warehouses = [f'Warehouse {i}' for i in range(1, 6)]
    
    # Test inbound dictionary
    for product in products:
        assert product in inbound_dict, f"Product {product} missing from inbound_dict"
        for factory in factories:
            assert factory in inbound_dict[product], f"Factory {factory} missing for {product} in inbound_dict"
            for cons in consolidation:
                assert cons in inbound_dict[product][factory], f"Consolidation {cons} missing for {factory}, {product}"
                assert isinstance(inbound_dict[product][factory][cons], (int, float)), "Cost should be numeric"
                
    # Test outbound dictionary
    for product in products:
        assert product in outbound_dict, f"Product {product} missing from outbound_dict"
        for cons in consolidation:
            assert cons in outbound_dict[product], f"Consolidation {cons} missing for {product} in outbound_dict"
            for warehouse in warehouses:
                assert warehouse in outbound_dict[product][cons], f"Warehouse {warehouse} missing for {cons}, {product}"
                assert isinstance(outbound_dict[product][cons][warehouse], (int, float)), "Cost should be numeric"
                
    # Test demand dictionary
    for product in products:
        assert product in demand_dict, f"Product {product} missing from demand_dict"
        for warehouse in warehouses:
            assert warehouse in demand_dict[product], f"Warehouse {warehouse} missing for {product} in demand_dict"
            assert isinstance(demand_dict[product][warehouse], (int, float)), "Demand should be numeric"
            assert demand_dict[product][warehouse] >= 0, "Demand should be non-negative"
            
    # Test capacity dictionary
    assert all(product in capacity_dict for product in products + ['Combined']), "Missing product types in capacity_dict"
    for product in products + ['Combined']:
        for factory in factories:
            assert factory in capacity_dict[product], f"Factory {factory} missing for {product} in capacity_dict"
            assert isinstance(capacity_dict[product][factory], (int, float)), "Capacity should be numeric"
            assert capacity_dict[product][factory] >= 0, "Capacity should be non-negative"

@pytest.mark.skip(reason="Solution file not available in test environment")
def test_solution_feasibility():
    """Test that the solution satisfies all constraints"""
    try:
        from optimization.network.gameverse.gameverse_solution import (
            prob, factory_to_cons, cons_to_warehouse,
            inbound_dict, outbound_dict, demand_dict, capacity_dict
        )
        
        # Check if solution exists
        assert prob.status == pulp.LpStatusOptimal, "Problem should have an optimal solution"
        
        products = ['Pro', 'Standard']
        factories = [f'Factory {i}' for i in range(1, 6)]
        consolidation = [f'Consolidation {i}' for i in range(1, 3)]
        warehouses = [f'Warehouse {i}' for i in range(1, 6)]
        
        # Test flow conservation at consolidation centers
        for product in products:
            for cons in consolidation:
                inflow = sum(factory_to_cons[product][factory][cons].value() 
                           for factory in factories)
                outflow = sum(cons_to_warehouse[product][cons][warehouse].value() 
                            for warehouse in warehouses)
                assert abs(inflow - outflow) < 1e-6, f"Flow conservation violated at {cons} for {product}"
        
        # Test demand satisfaction
        for product in products:
            for warehouse in warehouses:
                received = sum(cons_to_warehouse[product][cons][warehouse].value() 
                             for cons in consolidation)
                assert abs(received - demand_dict[product][warehouse]) < 1e-6, \
                    f"Demand not met at {warehouse} for {product}"
        
        # Test capacity constraints
        for factory in factories:
            total_pro = sum(factory_to_cons['Pro'][factory][cons].value() 
                          for cons in consolidation)
            total_std = sum(factory_to_cons['Standard'][factory][cons].value() 
                          for cons in consolidation)
            
            assert total_pro <= capacity_dict['Pro'][factory] + 1e-6, \
                f"Pro capacity exceeded at {factory}"
            assert total_std <= capacity_dict['Standard'][factory] + 1e-6, \
                f"Standard capacity exceeded at {factory}"
            assert total_pro + total_std <= capacity_dict['Combined'][factory] + 1e-6, \
                f"Combined capacity exceeded at {factory}"
            
    except ImportError:
        pytest.skip("Solution notebook not available or not completed")
