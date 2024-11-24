"""Test functions for regression analysis problems."""
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def check_coefficients(results, tolerance=0.01):
    """
    Check if regression coefficients are correct.
    
    Args:
        results (dict): Dictionary with intercept, slope, and R²
        tolerance (float): Acceptable difference from expected values
        
    Returns:
        bool: True if all coefficients are within tolerance
    """
    expected = {
        'intercept': 15.234,
        'slope': 12.456,
        'r_squared': 0.987
    }
    
    return all(abs(results[key] - expected[key]) <= tolerance 
              for key in expected.keys())

def check_prediction(model, X_new, tolerance=0.01):
    """
    Check if prediction is reasonable.
    
    Args:
        model: Fitted regression model
        X_new (float): New input value
        tolerance (float): Acceptable difference from expected value
        
    Returns:
        bool: True if prediction is reasonable
    """
    prediction = model.predict([[X_new]])[0]
    expected = 15.234 + 12.456 * X_new
    
    return abs(prediction - expected) <= tolerance

def check_diagnostics(model, X, y):
    """
    Check regression diagnostics.
    
    Args:
        model: Fitted regression model
        X (array): Input features
        y (array): Target values
        
    Returns:
        dict: Dictionary with diagnostic results
    """
    # Get predictions and residuals
    y_pred = model.predict(X)
    residuals = y - y_pred
    
    # Normality test of residuals
    _, p_value_normality = stats.shapiro(residuals)
    
    # Homoscedasticity (Breusch-Pagan test)
    _, p_value_homoscedasticity = stats.levene(y_pred, residuals)
    
    # Cook's distance for influential points
    n = len(y)
    p = X.shape[1]
    mse = np.sum(residuals**2) / (n-p)
    h_ii = np.diagonal(X.dot(np.linalg.inv(X.T.dot(X))).dot(X.T))
    cooks_d = (residuals**2 * h_ii) / (p * mse * (1-h_ii)**2)
    
    return {
        'normality_satisfied': p_value_normality > 0.05,
        'homoscedasticity_satisfied': p_value_homoscedasticity > 0.05,
        'influential_points': np.where(cooks_d > 4/n)[0]
    }

def verify_model_assumptions(X, y):
    """
    Verify all assumptions for linear regression.
    
    Args:
        X (array): Input features
        y (array): Target values
        
    Returns:
        dict: Dictionary with assumption verification results
    """
    # Linearity check using correlation coefficient
    correlation = np.corrcoef(X.flatten(), y)[0,1]
    
    # Independence check using Durbin-Watson
    model = LinearRegression().fit(X, y)
    residuals = y - model.predict(X)
    dw_statistic = np.sum(np.diff(residuals)**2) / np.sum(residuals**2)
    
    return {
        'linearity_satisfied': abs(correlation) > 0.7,
        'independence_satisfied': 1.5 < dw_statistic < 2.5,
        'correlation': correlation,
        'durbin_watson': dw_statistic
    }
