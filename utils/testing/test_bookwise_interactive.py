"""
Test module for Bookwise Interactive notebook.
Tests demand forecasting and probability calculations.
"""

import numpy as np
import pytest
from scipy import stats

def test_demand_forecast():
    """Test demand forecasting calculations."""
    # Generate sample data
    np.random.seed(42)
    historical_data = np.random.normal(100, 20, 50)
    
    def forecast_demand(historical_data, confidence_level=0.95):
        """Forecast future demand with confidence intervals."""
        mean_demand = np.mean(historical_data)
        std_demand = np.std(historical_data)
        z_score = stats.norm.ppf((1 + confidence_level) / 2)
        
        lower_bound = mean_demand - z_score * std_demand
        upper_bound = mean_demand + z_score * std_demand
        
        return mean_demand, (lower_bound, upper_bound)
    
    # Test basic forecasting
    mean_pred, (lower, upper) = forecast_demand(historical_data)
    assert lower < mean_pred < upper
    assert np.isclose(mean_pred, np.mean(historical_data))
    
    # Test confidence interval width
    ci_width = upper - lower
    assert ci_width > 0
    assert ci_width < 4 * np.std(historical_data)  # Should be within 4 standard deviations

def test_confidence_levels():
    """Test different confidence levels."""
    np.random.seed(42)
    historical_data = np.random.normal(100, 20, 50)
    
    def forecast_demand(historical_data, confidence_level=0.95):
        """Forecast future demand with confidence intervals."""
        mean_demand = np.mean(historical_data)
        std_demand = np.std(historical_data)
        z_score = stats.norm.ppf((1 + confidence_level) / 2)
        
        lower_bound = mean_demand - z_score * std_demand
        upper_bound = mean_demand + z_score * std_demand
        
        return mean_demand, (lower_bound, upper_bound)
    
    # Test 90% confidence interval
    mean_90, (lower_90, upper_90) = forecast_demand(historical_data, 0.90)
    
    # Test 99% confidence interval
    mean_99, (lower_99, upper_99) = forecast_demand(historical_data, 0.99)
    
    # 99% CI should be wider than 90% CI
    assert (upper_99 - lower_99) > (upper_90 - lower_90)
    
    # Mean should be the same regardless of confidence level
    assert np.isclose(mean_90, mean_99)

def test_input_validation():
    """Test input validation for forecasting."""
    def forecast_demand(historical_data, confidence_level=0.95):
        """Forecast future demand with confidence intervals."""
        if len(historical_data) < 2:
            raise ValueError("Need at least 2 data points")
        if not (0 < confidence_level < 1):
            raise ValueError("Confidence level must be between 0 and 1")
            
        mean_demand = np.mean(historical_data)
        std_demand = np.std(historical_data)
        z_score = stats.norm.ppf((1 + confidence_level) / 2)
        
        lower_bound = mean_demand - z_score * std_demand
        upper_bound = mean_demand + z_score * std_demand
        
        return mean_demand, (lower_bound, upper_bound)
    
    # Test empty data
    with pytest.raises(ValueError):
        forecast_demand([])
    
    # Test single data point
    with pytest.raises(ValueError):
        forecast_demand([100])
    
    # Test invalid confidence level
    with pytest.raises(ValueError):
        forecast_demand([100, 200], confidence_level=1.5)

if __name__ == '__main__':
    pytest.main([__file__])
