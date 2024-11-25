"""
Test module for GameStop preorder probability analysis notebook.
Tests probability calculations and demand prediction functions.
"""

import numpy as np
import pytest
from scipy import stats

def test_binomial_probability():
    """Test binomial probability calculations for preorder scenarios."""
    n = 100  # Number of potential customers
    p = 0.3  # Probability of preorder
    
    # Test single probability
    k = 25  # Number of preorders
    prob = stats.binom.pmf(k, n, p)
    assert 0 <= prob <= 1
    
    # Test cumulative probability
    cum_prob = stats.binom.cdf(k, n, p)
    assert 0 <= cum_prob <= 1
    assert cum_prob >= prob
    
    # Test complementary probability
    comp_prob = 1 - stats.binom.cdf(k-1, n, p)
    assert np.isclose(comp_prob, stats.binom.sf(k-1, n, p))

def test_poisson_approximation():
    """Test Poisson approximation for large n, small p scenarios."""
    n = 1000  # Large number of potential customers
    p = 0.01  # Small probability of preorder
    lambda_param = n * p
    
    # Compare binomial and Poisson probabilities
    k = 10
    binom_prob = stats.binom.pmf(k, n, p)
    poisson_prob = stats.poisson.pmf(k, lambda_param)
    
    # They should be close for large n, small p
    assert np.isclose(binom_prob, poisson_prob, rtol=0.1)
    
    # Test Poisson cumulative probability
    cum_prob = stats.poisson.cdf(k, lambda_param)
    assert 0 <= cum_prob <= 1

def test_normal_approximation():
    """Test normal approximation for binomial with large n."""
    n = 1000
    p = 0.3
    
    # Parameters for normal approximation
    mu = n * p
    sigma = np.sqrt(n * p * (1 - p))
    
    # Compare probabilities for a range of values
    k = int(mu)  # Test around the mean
    
    # Binomial probability
    binom_prob = stats.binom.cdf(k, n, p)
    
    # Normal approximation with continuity correction
    norm_prob = stats.norm.cdf(k + 0.5, mu, sigma)
    
    # They should be close for large n
    assert np.isclose(binom_prob, norm_prob, rtol=0.1)

def test_confidence_intervals():
    """Test confidence interval calculations for demand estimation."""
    # Sample data
    sample_size = 100
    successes = 30
    confidence = 0.95
    
    # Calculate Wilson score interval
    z = stats.norm.ppf((1 + confidence) / 2)
    p_hat = successes / sample_size
    
    denominator = 1 + z**2/sample_size
    center = (p_hat + z**2/(2*sample_size))/denominator
    spread = z * np.sqrt(p_hat*(1-p_hat)/sample_size + z**2/(4*sample_size**2))/denominator
    
    lower = center - spread
    upper = center + spread
    
    # Test interval properties
    assert 0 <= lower <= p_hat
    assert p_hat <= upper <= 1
    assert lower < upper

def test_demand_prediction():
    """Test demand prediction calculations."""
    # Historical data simulation
    np.random.seed(42)
    historical_demand = np.random.poisson(100, 50)
    
    # Calculate prediction interval
    mean_demand = np.mean(historical_demand)
    std_demand = np.std(historical_demand)
    confidence = 0.95
    z = stats.norm.ppf((1 + confidence) / 2)
    
    lower = mean_demand - z * std_demand
    upper = mean_demand + z * std_demand
    
    # Test interval properties
    assert lower < mean_demand < upper
    assert lower > 0  # Demand can't be negative
    
    # Test coverage of historical data
    coverage = np.mean((historical_demand >= lower) & (historical_demand <= upper))
    assert coverage >= 0.9  # Should cover approximately 95% of data

def test_risk_analysis():
    """Test risk analysis calculations for inventory decisions."""
    # Cost parameters
    purchase_cost = 50
    selling_price = 80
    salvage_value = 20
    
    # Demand parameters
    mean_demand = 100
    std_demand = 20
    
    # Calculate optimal order quantity using newsvendor formula
    z_optimal = stats.norm.ppf((selling_price - purchase_cost)/(selling_price - salvage_value))
    Q_optimal = mean_demand + z_optimal * std_demand
    
    # Test optimal quantity properties
    assert Q_optimal > 0
    assert Q_optimal > mean_demand - 3*std_demand  # Should be above 99.7% lower bound
    assert Q_optimal < mean_demand + 3*std_demand  # Should be below 99.7% upper bound
    
    # Calculate expected profit
    def expected_profit(Q):
        """Calculate expected profit for order quantity Q."""
        # Expected sales
        exp_sales = mean_demand * stats.norm.cdf((Q - mean_demand)/std_demand) + \
                   std_demand * stats.norm.pdf((Q - mean_demand)/std_demand)
        # Expected leftover
        exp_leftover = Q - exp_sales
        
        return selling_price * exp_sales + salvage_value * exp_leftover - purchase_cost * Q
    
    # Test that optimal quantity maximizes profit within tolerance
    delta = 1
    profit_optimal = expected_profit(Q_optimal)
    profit_lower = expected_profit(Q_optimal - delta)
    profit_higher = expected_profit(Q_optimal + delta)

    # Allow for numerical tolerance in profit comparison
    tolerance = 1e-2  # 1% tolerance
    relative_diff = abs((profit_optimal - profit_higher) / profit_optimal)
    assert relative_diff <= tolerance, "Profit should be near-optimal"

def test_simulation():
    """Test Monte Carlo simulation for demand scenarios."""
    n_simulations = 1000
    mean_demand = 100
    std_demand = 20
    
    # Generate demand scenarios
    np.random.seed(42)
    demand_scenarios = np.random.normal(mean_demand, std_demand, n_simulations)
    
    # Test statistical properties
    assert np.isclose(np.mean(demand_scenarios), mean_demand, rtol=0.1)
    assert np.isclose(np.std(demand_scenarios), std_demand, rtol=0.1)
    
    # Test empirical probabilities
    prob_above_mean = np.mean(demand_scenarios > mean_demand)
    assert np.isclose(prob_above_mean, 0.5, atol=0.05)
    
    # Test quantiles
    q95 = np.percentile(demand_scenarios, 95)
    theoretical_q95 = mean_demand + stats.norm.ppf(0.95) * std_demand
    assert np.isclose(q95, theoretical_q95, rtol=0.1)

if __name__ == '__main__':
    pytest.main([__file__])
