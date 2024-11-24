"""Test suite for all problem types."""
import pytest
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression

# Import test modules - Optimization
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
from .test_greenchain import (
    test_greenchain_data_structures,
    test_environmental_impact,
    test_network_flow
)
from .test_warehouse_location import (
    test_warehouse_location_data,
    test_distance_calculation,
    test_facility_location,
    test_multi_period_planning
)
from .test_supply_network import (
    test_network_data,
    test_flow_optimization,
    test_capacity_expansion,
    test_risk_mitigation
)
from .test_production_optimization import (
    test_production_data,
    test_production_planning,
    test_resource_allocation,
    test_setup_times
)
from .test_booboo_interactive import (
    test_risk_probability,
    test_risk_boundaries,
    test_input_validation as test_risk_validation
)
from .test_bookwise_interactive import (
    test_demand_forecast,
    test_confidence_levels,
    test_input_validation as test_forecast_validation
)

# Import test functions - Analytics
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

@pytest.fixture
def sample_probability_data():
    return {
        'rare_items': 10,
        'total_items': 100,
        'target_items': 5,
        'draws': 3
    }

@pytest.fixture
def sample_inventory_data():
    return {
        'store_stock': 50,
        'service_level': 0.95,
        'mean': 40,
        'std_dev': 10,
        'warehouse_stock': 100
    }

@pytest.fixture
def sample_hypothesis_data():
    return np.array([700, 710, 720, 730, 740, 750, 760, 770, 780, 790])

@pytest.fixture
def sample_regression_data():
    return np.array([[1, 2], [2, 4], [3, 6], [4, 8], [5, 10]])

@pytest.fixture
def optimization_test_data():
    """Fixture for optimization test data."""
    return {
        'warehouse_data': {
            'locations': [(0,0), (1,1), (2,2)],
            'demands': [100, 200, 300],
            'capacities': [500, 500, 500]
        },
        'network_data': {
            'nodes': ['A', 'B', 'C'],
            'edges': [('A','B'), ('B','C')],
            'costs': {'A': 10, 'B': 20, 'C': 30}
        },
        'production_data': {
            'products': ['P1', 'P2'],
            'resources': ['R1', 'R2'],
            'capacity': [100, 200]
        }
    }

def test_probability(sample_probability_data):
    """Test probability calculation functions."""
    print("\nTesting Probability Functions...")
    
    # Test single event probability
    p_single = sample_probability_data['rare_items'] / sample_probability_data['total_items']
    assert check_single_event_prob(p_single)
    
    # Test conditional probability
    p_cond = (sample_probability_data['rare_items'] - 1) / (sample_probability_data['total_items'] - 1)
    assert check_conditional_prob(p_cond)
    
    # Test multiple event probability
    p_multi = (sample_probability_data['target_items'] / sample_probability_data['total_items']) ** sample_probability_data['draws']
    assert check_multiple_event_prob(p_multi)

def test_inventory(sample_inventory_data):
    """Test inventory management functions."""
    print("\nTesting Inventory Functions...")
    
    # Test service level
    assert check_service_level(
        sample_inventory_data['store_stock'],
        sample_inventory_data['service_level'],
        sample_inventory_data['mean'],
        sample_inventory_data['std_dev']
    )
    
    # Test z-score
    z = (sample_inventory_data['store_stock'] - sample_inventory_data['mean']) / sample_inventory_data['std_dev']
    assert check_z_score(z, 0.2)  # Example expected z-score
    
    # Test two-stage system
    results = check_two_stage_system(
        sample_inventory_data['store_stock'],
        sample_inventory_data['warehouse_stock'],
        sample_inventory_data['mean'],
        sample_inventory_data['std_dev']
    )
    assert isinstance(results, dict)

def test_hypothesis(sample_hypothesis_data):
    """Test hypothesis testing functions."""
    print("\nTesting Hypothesis Functions...")
    
    # Test statistic calculation
    mu0 = 690  # Example null hypothesis mean
    test_stat = (np.mean(sample_hypothesis_data) - mu0) / (np.std(sample_hypothesis_data, ddof=1) / np.sqrt(len(sample_hypothesis_data)))
    assert check_test_statistic(test_stat)
    
    # Test p-value
    p_val = 2 * (1 - stats.t.cdf(abs(test_stat), df=len(sample_hypothesis_data)-1))
    assert check_p_value(p_val)
    
    # Test conclusion
    results = check_conclusion(sample_hypothesis_data, mu0)
    assert isinstance(results, dict)

def test_regression(sample_regression_data):
    """Test regression analysis functions."""
    print("\nTesting Regression Functions...")
    
    X = sample_regression_data[:, 0].reshape(-1, 1)
    y = sample_regression_data[:, 1]
    model = LinearRegression().fit(X, y)
    
    # Test coefficients
    coef_results = check_coefficients(model.coef_[0], model.intercept_)
    assert isinstance(coef_results, dict)
    
    # Test prediction
    X_new = np.array([[10]])  # Example new data point
    y_pred = model.predict(X_new)
    assert check_prediction(y_pred[0])
    
    # Test diagnostics
    diag_results = check_diagnostics(model, X, y)
    assert isinstance(diag_results, dict)

def test_all():
    """Run all test suites."""
    try:
        print("\nRunning All Tests...")
        
        # Run original tests
        test_probability(sample_probability_data())
        test_inventory(sample_inventory_data())
        test_hypothesis(sample_hypothesis_data())
        test_regression(sample_regression_data())
        
        # Get optimization test data
        opt_data = optimization_test_data()
        
        # Run optimization tests
        print("\nTesting Optimization Problems...")
        test_beverageco_data_structures()
        test_solution_feasibility()
        test_production_efficiency()
        test_risk_solution_feasibility()
        test_risk_metrics()
        
        # Test GreenChain
        test_greenchain_data_structures()
        test_environmental_impact()
        test_network_flow()
        
        # Run new supply chain optimization tests
        print("\nTesting Supply Chain Optimization...")
        test_warehouse_location_data(opt_data['warehouse_data'])
        test_distance_calculation(opt_data['warehouse_data'])
        test_facility_location(opt_data['warehouse_data'])
        test_multi_period_planning(opt_data['warehouse_data'])
        
        test_network_data(opt_data['network_data'])
        test_flow_optimization(opt_data['network_data'])
        test_capacity_expansion(opt_data['network_data'])
        test_risk_mitigation(opt_data['network_data'])
        
        test_production_data(opt_data['production_data'])
        test_production_planning(opt_data['production_data'])
        test_resource_allocation(opt_data['production_data'])
        test_setup_times(opt_data['production_data'])
        
        # Run new probability case study tests
        print("\nTesting Probability Case Studies...")
        test_risk_probability()
        test_risk_boundaries()
        test_risk_validation()
        
        test_demand_forecast()
        test_confidence_levels()
        test_forecast_validation()
        
        print("\nAll tests completed successfully!")
    except Exception as e:
        print(f"\nError running tests: {str(e)}")
        raise

if __name__ == '__main__':
    test_all()
