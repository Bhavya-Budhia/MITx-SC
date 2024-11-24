import pytest
import pulp
import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to the path so we can import the notebooks
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def test_greenchain_data_structures():
    """Test that the data structures in the GreenChain problem are valid"""
    try:
        from optimization.network.greenchain.greenchain_solution import (
            production_cost, transport_cost, emissions,
            suppliers, facilities, customers, products, modes
        )
        
        # Test list completeness
        assert len(suppliers) == 4, "Should have 4 suppliers"
        assert len(facilities) == 3, "Should have 3 facilities"
        assert len(customers) == 6, "Should have 6 customer zones"
        assert len(products) == 2, "Should have 2 products"
        assert len(modes) == 2, "Should have 2 transportation modes"
        
        # Test production cost structure
        for product in products:
            assert product in production_cost, f"Missing {product} in production costs"
            for facility in facilities:
                assert facility in production_cost[product], f"Missing {facility} for {product}"
                assert isinstance(production_cost[product][facility], (int, float)), "Cost should be numeric"
                assert production_cost[product][facility] > 0, "Cost should be positive"
        
        # Test transport cost structure
        for mode in modes:
            assert mode in transport_cost, f"Missing {mode} in transport costs"
            assert isinstance(transport_cost[mode], (int, float)), "Transport cost should be numeric"
            assert transport_cost[mode] > 0, "Transport cost should be positive"
            
        # Test emissions data
        for mode in modes:
            assert mode in emissions, f"Missing {mode} in emissions data"
            assert isinstance(emissions[mode], (int, float)), "Emissions should be numeric"
            assert emissions[mode] > 0, "Emissions should be positive"
            assert emissions[mode] < transport_cost[mode], "Emissions (kg CO2) should be less than cost ($)"
            
    except ImportError:
        pytest.skip("Solution notebook not available or not completed")

def test_solution_feasibility():
    """Test that the solution satisfies all constraints"""
    try:
        from optimization.network.greenchain.greenchain_solution import (
            prob, production, transport,
            products, facilities, customers, modes
        )
        
        # Check if solution exists
        assert prob.status == pulp.LpStatusOptimal, "Problem should have an optimal solution"
        
        # Test non-negativity
        for p in products:
            for f in facilities:
                assert production[p,f].value() >= 0, f"Negative production for {p} at {f}"
                
        for p in products:
            for f in facilities:
                for c in customers:
                    for m in modes:
                        assert transport[p,f,c,m].value() >= 0, \
                            f"Negative transport for {p} from {f} to {c} via {m}"
        
        # Test flow conservation
        for p in products:
            for f in facilities:
                prod = production[p,f].value()
                ship = sum(transport[p,f,c,m].value() 
                         for c in customers 
                         for m in modes)
                assert abs(prod - ship) < 1e-6, \
                    f"Production-shipment mismatch at {f} for {p}"
                    
    except ImportError:
        pytest.skip("Solution notebook not available or not completed")

def test_sustainability_metrics():
    """Test that the solution meets sustainability criteria"""
    try:
        from optimization.network.greenchain.greenchain_solution import (
            prob, transport, emissions, modes,
            products, facilities, customers
        )
        
        if prob.status != pulp.LpStatusOptimal:
            pytest.skip("Solution is not optimal, skipping sustainability tests")
            
        # Calculate total emissions
        total_emissions = sum(
            emissions[m] * transport[p,f,c,m].value()
            for p in products
            for f in facilities
            for c in customers
            for m in modes
        )
        
        # Test modal split (at least 30% should use rail for sustainability)
        total_rail = sum(
            transport[p,f,c,'Rail'].value()
            for p in products
            for f in facilities
            for c in customers
        )
        
        total_transport = sum(
            transport[p,f,c,m].value()
            for p in products
            for f in facilities
            for c in customers
            for m in modes
        )
        
        rail_percentage = total_rail / total_transport if total_transport > 0 else 0
        assert rail_percentage >= 0.3, "Rail usage should be at least 30% for sustainability"
        
        # Test emissions intensity (kg CO2 per unit transported)
        emissions_intensity = total_emissions / total_transport if total_transport > 0 else 0
        assert emissions_intensity <= 0.08, "Emissions intensity too high"
        
    except ImportError:
        pytest.skip("Solution notebook not available or not completed")
