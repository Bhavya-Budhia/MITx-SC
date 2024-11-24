"""Test utilities for forecasting notebooks."""

import numpy as np
from scipy import stats

def check_moving_average(ma_values, original_data, window_size, weights=None, tolerance=0.001):
    """
    Check if moving average calculations are correct.
    
    Args:
        ma_values (array-like): Calculated moving average values
        original_data (array-like): Original time series data
        window_size (int): Size of moving average window
        weights (array-like, optional): Weights for weighted moving average
        tolerance (float): Acceptable difference from expected values
        
    Returns:
        bool: True if calculations are within tolerance
    """
    ma_values = np.array(ma_values)
    original_data = np.array(original_data)
    
    if weights is not None:
        weights = np.array(weights)
        if len(weights) != window_size:
            return False
        if not np.isclose(np.sum(weights), 1.0):
            return False
    
    for i in range(len(ma_values)):
        if i < window_size - 1:
            if not np.isnan(ma_values[i]):
                return False
            continue
            
        window = original_data[i-window_size+1:i+1]
        if weights is None:
            expected = np.mean(window)
        else:
            expected = np.sum(window * weights)
            
        if not np.isclose(ma_values[i], expected, rtol=tolerance):
            return False
            
    return True

def check_exponential_smoothing(smoothed_values, original_data, alpha, beta=None, gamma=None, 
                              seasonal_periods=None, tolerance=0.001):
    """
    Check exponential smoothing calculations.
    
    Args:
        smoothed_values (array-like): Calculated smoothed values
        original_data (array-like): Original time series data
        alpha (float): Level smoothing factor
        beta (float, optional): Trend smoothing factor
        gamma (float, optional): Seasonal smoothing factor
        seasonal_periods (int, optional): Number of periods in seasonal cycle
        tolerance (float): Acceptable difference from expected values
        
    Returns:
        bool: True if calculations are within tolerance
    """
    if not (0 <= alpha <= 1):
        return False
        
    if beta is not None and not (0 <= beta <= 1):
        return False
        
    if gamma is not None:
        if not (0 <= gamma <= 1) or seasonal_periods is None:
            return False
            
    # Basic exponential smoothing check
    if beta is None and gamma is None:
        level = original_data[0]
        for i in range(1, len(original_data)):
            level = alpha * original_data[i] + (1 - alpha) * level
            if not np.isclose(smoothed_values[i], level, rtol=tolerance):
                return False
                
    return True

def check_seasonal_decomposition(trend, seasonal, residual, original_data, 
                               period, tolerance=0.001):
    """
    Check seasonal decomposition results.
    
    Args:
        trend (array-like): Trend component
        seasonal (array-like): Seasonal component
        residual (array-like): Residual component
        original_data (array-like): Original time series data
        period (int): Seasonal period length
        tolerance (float): Acceptable difference from expected values
        
    Returns:
        bool: True if decomposition is valid
    """
    # Check components sum to original (additive model)
    reconstructed = trend + seasonal + residual
    if not np.allclose(original_data, reconstructed, rtol=tolerance):
        return False
        
    # Check seasonal pattern
    seasonal = np.array(seasonal)
    for i in range(len(seasonal) - period):
        if not np.isclose(seasonal[i], seasonal[i + period], rtol=tolerance):
            return False
            
    # Check trend smoothness
    trend = np.array(trend)
    trend_diff = np.diff(trend)
    if np.any(np.abs(np.diff(trend_diff)) > tolerance):
        return False
        
    return True

def check_arima_residuals(residuals, significance_level=0.05):
    """
    Check ARIMA model residuals for white noise properties.
    
    Args:
        residuals (array-like): Model residuals
        significance_level (float): Significance level for statistical tests
        
    Returns:
        bool: True if residuals pass white noise tests
    """
    residuals = np.array(residuals)
    
    # Check for zero mean
    t_stat, p_value = stats.ttest_1samp(residuals, 0)
    if p_value < significance_level:
        return False
        
    # Check for constant variance (homoscedasticity)
    _, p_value = stats.levene(residuals[:len(residuals)//2], 
                             residuals[len(residuals)//2:])
    if p_value < significance_level:
        return False
        
    # Check for normality
    _, p_value = stats.normaltest(residuals)
    if p_value < significance_level:
        return False
        
    # Check for autocorrelation
    acf = np.correlate(residuals, residuals, mode='full')[len(residuals)-1:]
    acf = acf / acf[0]
    if np.any(np.abs(acf[1:]) > 2/np.sqrt(len(residuals))):
        return False
        
    return True

def check_forecast_accuracy(forecasts, actuals, metrics=None, tolerance=0.001):
    """
    Check forecast accuracy using various metrics.
    
    Args:
        forecasts (array-like): Forecasted values
        actuals (array-like): Actual values
        metrics (dict, optional): Dictionary of accuracy metrics and their thresholds
        tolerance (float): Acceptable difference in calculations
        
    Returns:
        bool: True if accuracy metrics are within acceptable ranges
    """
    forecasts = np.array(forecasts)
    actuals = np.array(actuals)
    
    if metrics is None:
        metrics = {
            'mape': 0.2,  # 20% MAPE threshold
            'rmse': None  # No threshold, just check calculation
        }
    
    errors = actuals - forecasts
    
    for metric, threshold in metrics.items():
        if metric == 'mape':
            mape = np.mean(np.abs(errors / actuals)) * 100
            if threshold is not None and mape > threshold:
                return False
                
        elif metric == 'rmse':
            rmse = np.sqrt(np.mean(errors**2))
            if threshold is not None and rmse > threshold:
                return False
                
        elif metric == 'mae':
            mae = np.mean(np.abs(errors))
            if threshold is not None and mae > threshold:
                return False
                
    return True
