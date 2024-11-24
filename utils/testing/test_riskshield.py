import pytest
import pulp
import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to the path so we can import the notebooks
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def test_riskshield_data_structures():
    """Test that the data structures in the RiskShield problem are valid"""
    try:
        from optimization.risk.riskshield.riskshield_solution import (
            components, suppliers, regions, reliability, cost,
            geo_risk, demand, service_level
        )
        
        # Test basic structures
        assert len(components) == 3, "Should have 3 components"
        assert len(suppliers) == 5, "Should have 5 suppliers"
        assert len(regions) == 3, "Should have 3 regions"
        
        # Test reliability scores
        for s in suppliers:
            assert s in reliability, f"Missing reliability score for {s}"
            assert 0 <= reliability[s] <= 1, "Reliability score should be between 0 and 1"
            
        # Test costs
        for c in components:
            assert c in cost, f"Missing cost data for {c}"
            for s in suppliers:
                assert s in cost[c], f"Missing cost for {c} from {s}"
                assert cost[c][s] > 0, "Cost should be positive"
                
        # Test geographic risk
        for s in suppliers:
            assert s in geo_risk, f"Missing geographic risk for {s}"
            assert 0 <= geo_risk[s] <= 1, "Geographic risk should be between 0 and 1"
            
        # Test demand and service levels
        for c in components:
            assert c in demand, f"Missing demand for {c}"
            assert c in service_level, f"Missing service level for {c}"
            assert demand[c] > 0, "Demand should be positive"
            assert 0 <= service_level[c] <= 1, "Service level should be between 0 and 1"
            
    except ImportError:
        pytest.skip("Solution notebook not available or not completed")

def test_solution_feasibility():
    """Test that the solution satisfies all constraints"""
    try:
        from optimization.risk.riskshield.riskshield_solution import (
            prob, order, use_supplier, buffer,
            components, suppliers, demand, service_level
        )
        
        # Check if solution exists
        assert prob.status == pulp.LpStatusOptimal, "Problem should have an optimal solution"
        
        # Test non-negativity
        for c in components:
            for s in suppliers:
                assert order[c,s].value() >= 0, f"Negative order quantity for {c} from {s}"
            assert buffer[c].value() >= 0, f"Negative buffer inventory for {c}"
                
        # Test binary variables
        for c in components:
            for s in suppliers:
                assert use_supplier[c,s].value() in [0, 1], f"Use supplier variable not binary for {c}, {s}"
                
        # Test demand satisfaction
        for c in components:
            total_supply = sum(order[c,s].value() for s in suppliers)
            assert total_supply + buffer[c].value() >= demand[c], \
                f"Demand not met for {c}"
                
        # Test supplier usage consistency
        for c in components:
            for s in suppliers:
                if order[c,s].value() > 0:
                    assert use_supplier[c,s].value() == 1, \
                        f"Supplier usage inconsistent for {c}, {s}"
                
    except ImportError:
        pytest.skip("Solution notebook not available or not completed")

def test_risk_metrics():
    """Test risk-related metrics of the solution"""
    try:
        from optimization.risk.riskshield.riskshield_solution import (
            prob, order, use_supplier,
            components, suppliers, reliability, geo_risk
        )
        
        if prob.status != pulp.LpStatusOptimal:
            pytest.skip("Solution is not optimal, skipping risk metrics tests")
            
        # Test supplier diversification
        for c in components:
            suppliers_used = sum(use_supplier[c,s].value() for s in suppliers)
            assert suppliers_used >= 2, f"Too few suppliers used for {c}"
            
        # Test geographic risk balance
        for c in components:
            weighted_geo_risk = sum(
                geo_risk[s] * order[c,s].value()
                for s in suppliers
            ) / sum(order[c,s].value() for s in suppliers)
            assert weighted_geo_risk <= 0.15, f"Geographic risk too high for {c}"
            
        # Test reliability metrics
        for c in components:
            weighted_reliability = sum(
                reliability[s] * order[c,s].value()
                for s in suppliers
            ) / sum(order[c,s].value() for s in suppliers)
            assert weighted_reliability >= 0.9, f"Overall reliability too low for {c}"
            
    except ImportError:
        pytest.skip("Solution notebook not available or not completed")
