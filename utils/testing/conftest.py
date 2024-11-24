"""Configuration file for pytest."""
import pytest
import numpy as np
from scipy import stats

@pytest.fixture
def sample_probability_data():
    """Sample data for probability tests."""
    return {
        'total_items': 300,
        'rare_items': 65,
        'target_items': 2,
        'draws': 3
    }

@pytest.fixture
def sample_inventory_data():
    """Sample data for inventory tests."""
    return {
        'mean': 75,
        'std_dev': 25,
        'store_stock': 80,
        'warehouse_stock': 40,
        'service_level': 0.90
    }

@pytest.fixture
def sample_hypothesis_data():
    """Sample data for hypothesis tests."""
    return np.array([685, 695, 701, 688, 692, 679, 683, 698, 691, 687])

@pytest.fixture
def sample_regression_data():
    """Sample data for regression tests."""
    X = np.array([3, 7, 2, 8, 1, 4, 6, 2, 3, 7, 5, 4, 5, 6]).reshape(-1, 1)
    y = np.array([45, 95, 35, 105, 25, 55, 85, 30, 40, 90, 70, 50, 75, 80])
    return X, y
