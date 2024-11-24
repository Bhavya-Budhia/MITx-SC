"""Test suite for all problem types."""
import pytest
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression

# Import test modules
from .test_beverageco import (
    test_beverageco_data_structures,
    test_solution_feasibility,
    test_production_efficiency
)
from .test_riskshield import (
    test_riskshield_data_structures,
    test_solution_feasibility as test_risk_solution_feasibility,
    test_risk_metrics
)
from .test_greenchain import *  # Import GreenChain tests

def test_all():
    """Run all tests."""
    # Test optimization problems
    print("Testing BeverageCo...")
    test_beverageco_data_structures()
    test_solution_feasibility()
    test_production_efficiency()
    
    print("Testing RiskShield...")
    test_riskshield_data_structures()
    test_risk_solution_feasibility()
    test_risk_metrics()
    
    print("All tests passed!")

if __name__ == '__main__':
    test_all()
