"""Test suite for all problem types."""
import pytest
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression

from .probability_tests import (
    check_single_event_prob,
    check_conditional_prob,
    check_multiple_event_prob
)
from .inventory_tests import (
    check_service_level,
    check_z_score,
    check_two_stage_system
)
from .hypothesis_tests import (
    check_test_statistic,
    check_p_value,
    check_conclusion
)
from .regression_tests import (
    check_coefficients,
    check_prediction,
    check_diagnostics
)
from .test_beverageco import (
    test_beverageco_data_structures,
    test_solution_feasibility,
    test_production_efficiency
)
from .test_riskshield import (
    test_riskshield_data_structures,
    test_solution_feasibility,
    test_risk_metrics
)
from .test_greenchain import *  # Import GreenChain tests

def test_probability_functions(sample_probability_data):
    """Test probability calculation functions."""
    # Test single event probability
    p_single = 65/300  # Example calculation
    assert check_single_event_prob(p_single, expected=65/300)
    
    # Test conditional probability
    p_cond = 64/299  # Example calculation
    assert check_conditional_prob(p_cond, expected=64/299)

def test_inventory_functions(sample_inventory_data):
    """Test inventory management functions."""
    # Test service level calculation
    units = 90
    assert check_service_level(
        units,
        sample_inventory_data['service_level'],
        sample_inventory_data['mean'],
        sample_inventory_data['std_dev']
    )
    
    # Test two-stage system
    results = check_two_stage_system(
        sample_inventory_data['store_stock'],
        sample_inventory_data['warehouse_stock']
    )
    assert 0 <= results['store_sufficient'] <= 1
    assert 0 <= results['warehouse_needed'] <= 1
    assert 0 <= results['total_stockout'] <= 1

def test_hypothesis_functions(sample_hypothesis_data):
    """Test hypothesis testing functions."""
    # Test statistic calculation
    mu0 = 720
    test_stat = (np.mean(sample_hypothesis_data) - mu0) / (np.std(sample_hypothesis_data, ddof=1) / np.sqrt(len(sample_hypothesis_data)))
    assert check_test_statistic(test_stat)
    
    # Test conclusion
    results = check_conclusion(sample_hypothesis_data)
    assert isinstance(results['reject_null'], bool)

def test_regression_functions(sample_regression_data):
    """Test regression analysis functions."""
    X, y = sample_regression_data
    model = LinearRegression().fit(X, y)
    
    # Test coefficient checking
    results = {
        'intercept': model.intercept_,
        'slope': model.coef_[0],
        'r_squared': model.score(X, y)
    }
    
    # Test diagnostics
    diag_results = check_diagnostics(model, X, y)
    assert isinstance(diag_results['normality_satisfied'], bool)
    assert isinstance(diag_results['homoscedasticity_satisfied'], bool)

def test_all():
    """Run all tests."""
    # Test optimization problems
    test_beverageco_data_structures()
    test_solution_feasibility()
    test_production_efficiency()
    
    test_riskshield_data_structures()
    test_solution_feasibility()
    test_risk_metrics()
    
    # Test probability calculation functions
    test_probability_functions(sample_probability_data)
    
    # Test inventory management functions
    test_inventory_functions(sample_inventory_data)
    
    # Test hypothesis testing functions
    test_hypothesis_functions(sample_hypothesis_data)
    
    # Test regression analysis functions
    test_regression_functions(sample_regression_data)

if __name__ == '__main__':
    test_all()
