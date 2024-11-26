"""Test functions for CustomFit Tailoring Time Prediction."""
import numpy as np
from scipy import stats
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

def _get_actual_coefficients():
    """Calculate actual coefficients from the data."""
    alterations = np.array([3, 7, 2, 8, 1, 4, 6, 2, 3, 7, 5, 4, 5, 6])
    times = np.array([45, 95, 35, 105, 25, 55, 85, 30, 40, 90, 70, 50, 75, 80])
    X = alterations.reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, times)
    return float(model.coef_[0]), float(model.intercept_)

def check_coefficients(slope, intercept, tolerance=1.0):
    """
    Check if regression coefficients match the actual data.
    
    Args:
        slope (float): Calculated slope (minutes per alteration)
        intercept (float): Calculated intercept (base time)
        tolerance (float): Acceptable difference from expected values
        
    Returns:
        bool: True if coefficients are within tolerance of expected values
    """
    if slope is None or intercept is None:
        print("Please calculate the slope and intercept first!")
        return False
    
    actual_slope, actual_intercept = _get_actual_coefficients()
    
    slope_ok = abs(slope - actual_slope) <= tolerance
    intercept_ok = abs(intercept - actual_intercept) <= tolerance
    
    if not slope_ok:
        print(f"Slope {slope:.2f} is not close enough to expected {actual_slope:.2f}")
    if not intercept_ok:
        print(f"Intercept {intercept:.2f} is not close enough to expected {actual_intercept:.2f}")
    
    return slope_ok and intercept_ok

def check_prediction(pred_time, alterations, tolerance=2.0):
    """
    Check if predicted tailoring time matches the actual model.
    
    Args:
        pred_time (float): Predicted completion time
        alterations (int): Number of alterations
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if prediction is within tolerance of expected value
    """
    if pred_time is None:
        print("Please calculate the predicted time first!")
        return False
    
    actual_slope, actual_intercept = _get_actual_coefficients()
    expected_time = actual_intercept + actual_slope * alterations
    
    if abs(pred_time - expected_time) > tolerance:
        print(f"Prediction {pred_time:.2f} is not close enough to expected {expected_time:.2f}")
    
    return abs(pred_time - expected_time) <= tolerance

def check_diagnostics(diagnostics):
    """
    Check if model diagnostics are reasonable.
    
    Args:
        diagnostics (dict): Dictionary with diagnostic results
        
    Returns:
        bool: True if diagnostics are reasonable
    """
    if diagnostics is None:
        print("Please calculate the model diagnostics first!")
        return False
    
    if not isinstance(diagnostics, dict):
        print("Model diagnostics should be a dictionary!")
        return False
    
    required_keys = ['r2', 'residuals_normal', 'homoscedastic']
    if not all(key in diagnostics for key in required_keys):
        print(f"Missing required keys in diagnostics. Need: {required_keys}")
        return False
    
    # Check that R-squared is reasonable (above 0.75 for this data)
    # and other diagnostics are boolean
    r2_ok = (isinstance(diagnostics['r2'], (float, np.float64)) and 
             0.75 <= diagnostics['r2'] <= 1.0)
    normal_ok = isinstance(diagnostics['residuals_normal'], bool)
    homo_ok = isinstance(diagnostics['homoscedastic'], bool)
    
    if not r2_ok:
        print(f"R-squared {diagnostics['r2']} should be between 0.75 and 1.0")
    if not normal_ok:
        print("residuals_normal should be a boolean value")
    if not homo_ok:
        print("homoscedastic should be a boolean value")
    
    return r2_ok and normal_ok and homo_ok

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
