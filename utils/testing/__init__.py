"""Testing utilities for math problems."""

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
    check_conclusion,
    check_assumptions
)

from .regression_tests import (
    check_coefficients,
    check_prediction,
    check_diagnostics,
    calculate_intervals
)

__all__ = [
    # Probability
    'check_single_event_prob',
    'check_conditional_prob',
    'check_multiple_event_prob',
    
    # Inventory
    'check_service_level',
    'check_z_score',
    'check_two_stage_system',
    
    # Hypothesis
    'check_test_statistic',
    'check_p_value',
    'check_conclusion',
    'check_assumptions',
    
    # Regression
    'check_coefficients',
    'check_prediction',
    'check_diagnostics',
    'calculate_intervals'
]
