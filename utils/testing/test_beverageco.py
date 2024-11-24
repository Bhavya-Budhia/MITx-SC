import pytest
import pulp
import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to the path so we can import the notebooks
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def test_beverageco_data_structures():
    """Test that the data structures in the BeverageCo problem are valid"""
    try:
        from optimization.production.beverageco.beverageco_solution import (
            products, months, shelf_life, production_cost, setup_cost,
            storage_cost, price, demand
        )
        
        # Test basic structures
        assert len(products) == 3, "Should have 3 products"
        assert len(list(months)) == 6, "Should have 6 months"
        
        # Test shelf life
        for p in products:
            assert p in shelf_life, f"Missing shelf life for {p}"
            assert isinstance(shelf_life[p], int), "Shelf life should be integer"
            assert shelf_life[p] > 0, "Shelf life should be positive"
            
        # Test costs and prices
        for p in products:
            assert p in production_cost, f"Missing production cost for {p}"
            assert p in setup_cost, f"Missing setup cost for {p}"
            assert p in price, f"Missing price for {p}"
            assert production_cost[p] > 0, "Production cost should be positive"
            assert setup_cost[p] > 0, "Setup cost should be positive"
            assert price[p] > production_cost[p], "Price should exceed production cost"
            
        # Test storage costs
        for p in products:
            assert p in storage_cost, f"Missing storage cost for {p}"
            for m in months:
                assert m in storage_cost[p], f"Missing storage cost for {p} in month {m}"
                assert storage_cost[p][m] > 0, "Storage cost should be positive"
                # Summer months (3-4) should have higher storage costs
                if m in [3, 4]:
                    assert storage_cost[p][m] > storage_cost[p][1], "Summer storage cost should be higher"
                    
        # Test demand
        for p in products:
            assert p in demand, f"Missing demand for {p}"
            for m in months:
                assert m in demand[p], f"Missing demand for {p} in month {m}"
                assert demand[p][m] > 0, "Demand should be positive"
                # Summer months should have higher demand
                if m in [3, 4]:
                    assert demand[p][m] > demand[p][1], "Summer demand should be higher"
                    
    except ImportError:
        pytest.skip("Solution notebook not available or not completed")

def test_solution_feasibility():
    """Test that the solution satisfies all constraints"""
    try:
        from optimization.production.beverageco.beverageco_solution import (
            prob, production, inventory, setup,
            products, months, demand, shelf_life
        )
        
        # Check if solution exists
        assert prob.status == pulp.LpStatusOptimal, "Problem should have an optimal solution"
        
        # Test non-negativity
        for p in products:
            for m in months:
                assert production[p,m].value() >= 0, f"Negative production for {p} in month {m}"
                assert inventory[p,m].value() >= 0, f"Negative inventory for {p} in month {m}"
                
        # Test setup variables are binary
        for p in products:
            for m in months:
                assert setup[p,m].value() in [0, 1], f"Setup variable not binary for {p} in month {m}"
                
        # Test inventory balance
        for p in products:
            for m in months:
                if m == 1:
                    prev_inv = 0
                else:
                    prev_inv = inventory[p,m-1].value()
                    
                balance = prev_inv + production[p,m].value() - demand[p][m]
                assert abs(balance - inventory[p,m].value()) < 1e-6, \
                    f"Inventory balance violated for {p} in month {m}"
                    
        # Test shelf life constraints
        for p in products:
            for m in months:
                # Sum inventory of product older than its shelf life
                old_inventory = sum(
                    inventory[p,max(1, m-i)].value()
                    for i in range(shelf_life[p], m)
                    if m-i > 0
                )
                assert old_inventory < 1e-6, f"Expired inventory found for {p} in month {m}"
                
    except ImportError:
        pytest.skip("Solution notebook not available or not completed")

def test_production_efficiency():
    """Test production efficiency metrics"""
    try:
        from optimization.production.beverageco.beverageco_solution import (
            prob, production, setup, inventory,
            products, months, production_cost, storage_cost
        )
        
        if prob.status != pulp.LpStatusOptimal:
            pytest.skip("Solution is not optimal, skipping efficiency tests")
            
        # Calculate capacity utilization
        for m in months:
            total_production = sum(production[p,m].value() for p in products)
            assert total_production > 0, f"No production in month {m}"
            
        # Check for reasonable inventory levels (not too high)
        for p in products:
            for m in months:
                prod = production[p,m].value()
                inv = inventory[p,m].value()
                assert inv <= 2 * prod, f"Excessive inventory for {p} in month {m}"
                
        # Check setup patterns
        for p in products:
            setups = sum(setup[p,m].value() for m in months)
            assert setups >= 2, f"Too few setups for {p}"  # Should produce at least twice in 6 months
            assert setups <= 5, f"Too many setups for {p}"  # Shouldn't set up every month
            
    except ImportError:
        pytest.skip("Solution notebook not available or not completed")
