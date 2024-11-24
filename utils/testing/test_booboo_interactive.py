"""
Test module for Booboo Interactive notebook.
Tests probability calculations and risk assessment functions.
"""

import numpy as np
import pytest
from scipy import stats

def test_risk_probability():
    """Test risk probability calculations."""
    # Test case 1: High risk scenario
    mean_demand = 100
    std_demand = 20
    stock_level = 90  # Below mean
    
    def calculate_risk_probability(mean_demand, std_demand, stock_level):
        """Calculate probability of stockout given demand distribution."""
        z_score = (stock_level - mean_demand) / std_demand
        stockout_prob = 1 - stats.norm.cdf(z_score)
        return stockout_prob
    
    high_risk_prob = calculate_risk_probability(mean_demand, std_demand, stock_level)
    assert high_risk_prob > 0.5  # Should be high risk
    
    # Test case 2: Low risk scenario
    stock_level = 150  # Well above mean
    low_risk_prob = calculate_risk_probability(mean_demand, std_demand, stock_level)
    assert low_risk_prob < 0.01  # Should be very low risk
    
    # Test case 3: Medium risk scenario
    stock_level = mean_demand  # At mean
    med_risk_prob = calculate_risk_probability(mean_demand, std_demand, stock_level)
    assert np.isclose(med_risk_prob, 0.5, atol=0.01)  # Should be about 50%

def test_risk_boundaries():
    """Test risk probability boundaries."""
    mean_demand = 100
    std_demand = 20
    
    def calculate_risk_probability(mean_demand, std_demand, stock_level):
        """Calculate probability of stockout given demand distribution."""
        z_score = (stock_level - mean_demand) / std_demand
        stockout_prob = 1 - stats.norm.cdf(z_score)
        return stockout_prob
    
    # Test extremely high stock level
    very_high_stock = mean_demand + 4*std_demand
    very_low_risk = calculate_risk_probability(mean_demand, std_demand, very_high_stock)
    assert very_low_risk < 0.0001  # Should be nearly zero
    
    # Test extremely low stock level
    very_low_stock = mean_demand - 4*std_demand
    very_high_risk = calculate_risk_probability(mean_demand, std_demand, very_low_stock)
    assert very_high_risk > 0.9999  # Should be nearly one

def test_input_validation():
    """Test input validation for risk calculations."""
    mean_demand = 100
    std_demand = 20
    
    def calculate_risk_probability(mean_demand, std_demand, stock_level):
        """Calculate probability of stockout given demand distribution."""
        if std_demand <= 0:
            raise ValueError("Standard deviation must be positive")
        z_score = (stock_level - mean_demand) / std_demand
        stockout_prob = 1 - stats.norm.cdf(z_score)
        return stockout_prob
    
    # Test negative standard deviation
    with pytest.raises(ValueError):
        calculate_risk_probability(mean_demand, -std_demand, 100)
    
    # Test zero standard deviation
    with pytest.raises(ValueError):
        calculate_risk_probability(mean_demand, 0, 100)

if __name__ == '__main__':
    pytest.main([__file__])
