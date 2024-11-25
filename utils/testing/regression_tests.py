"""Test functions for CustomFit Tailoring Time Prediction."""
import numpy as np
from scipy import stats
from sklearn.metrics import r2_score

def check_coefficients(slope, intercept, slope_expected=13.5, intercept_expected=15.0, tolerance=0.1):
    """
    Check if regression coefficients for tailoring time prediction are correct.
    
    Args:
        slope (float): Calculated slope (minutes per alteration)
        intercept (float): Calculated intercept (base time)
        slope_expected (float): Expected slope (13.5)
        intercept_expected (float): Expected intercept (15.0)
        tolerance (float): Acceptable difference from expected values
        
    Returns:
        bool: True if coefficients are within tolerance of expected values
    """
    if slope is None or intercept is None:
        return False
    return (abs(slope - slope_expected) <= tolerance and 
            abs(intercept - intercept_expected) <= tolerance)

def check_prediction(pred_time, alterations, tolerance=5.0):
    """
    Check if predicted tailoring time is reasonable.
    
    Args:
        pred_time (float): Predicted completion time
        alterations (int): Number of alterations
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if prediction is within tolerance of expected value
    """
    if pred_time is None:
        return False
    expected_time = 15.0 + 13.5 * alterations
    return abs(pred_time - expected_time) <= tolerance

def check_diagnostics(diagnostics):
    """
    Check if model diagnostics are correct.
    
    Args:
        diagnostics (dict): Dictionary with diagnostic results
        
    Returns:
        bool: True if diagnostics are correct
    """
    if diagnostics is None or not isinstance(diagnostics, dict):
        return False
        
    required_keys = ['r2', 'residuals_normal', 'homoscedastic']
    if not all(key in diagnostics for key in required_keys):
        return False
        
    # Check specific values
    return (
        diagnostics['r2'] >= 0.90 and  # Strong fit required
        diagnostics['residuals_normal'] and  # Normality assumption
        diagnostics['homoscedastic']  # Constant variance
    )

def calculate_intervals(X, y, x_new, model, alpha=0.05):
    """
    Calculate confidence and prediction intervals.
    
    Args:
        X (array): Feature matrix
        y (array): Target values
        x_new (float): New x value for prediction (scalar)
        model: Fitted regression model
        alpha (float): Significance level
        
    Returns:
        dict: Dictionary with interval calculations
    """
    n = len(X)
    p = 1  # Number of parameters (assuming simple linear regression)
    
    # Get prediction for new x value
    x_new_array = np.array([[x_new]])  # Reshape for sklearn
    y_pred = model.predict(x_new_array)[0]
    
    # Calculate MSE and standard errors
    y_fit = model.predict(X)
    mse = np.sum((y - y_fit) ** 2) / (n - p - 1)
    
    # Calculate confidence interval
    x_mean = np.mean(X)
    x_std = np.std(X)
    se = np.sqrt(mse * (1/n + (x_new - x_mean)**2 / ((n-1)*x_std**2)))
    t_val = stats.t.ppf(1 - alpha/2, n - p - 1)
    
    ci_lower = y_pred - t_val * se
    ci_upper = y_pred + t_val * se
    
    # Calculate prediction interval
    se_pred = np.sqrt(mse * (1 + 1/n + (x_new - x_mean)**2 / ((n-1)*x_std**2)))
    pi_lower = y_pred - t_val * se_pred
    pi_upper = y_pred + t_val * se_pred
    
    return {
        'y_pred': y_pred,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'pi_lower': pi_lower,
        'pi_upper': pi_upper
    }
