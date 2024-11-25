"""
Test module for warehouse location optimization notebook.
Tests the implementation of facility location models and optimization functions.
"""

import numpy as np
import pytest
from pulp import *

def test_distance_calculation():
    """Test the calculation of distances between warehouses and customers."""
    warehouse_locations = [(0, 0), (1, 1)]
    customer_locations = [(0, 1), (1, 0)]
    
    def calculate_distances(warehouses, customers):
        distances = {}
        for i, w in enumerate(warehouses):
            for j, c in enumerate(customers):
                distances[i,j] = np.sqrt((w[0]-c[0])**2 + (w[1]-c[1])**2)
        return distances
    
    distances = calculate_distances(warehouse_locations, customer_locations)
    assert np.isclose(distances[0,0], 1.0)
    assert np.isclose(distances[0,1], 1.0)
    assert np.isclose(distances[1,0], 1.0)
    assert np.isclose(distances[1,1], 1.0)

def test_basic_facility_location():
    """Test basic facility location model with fixed costs and capacities."""
    # Test data
    warehouses = range(2)
    customers = range(2)
    demand = {0: 100, 1: 150}
    capacity = {0: 200, 1: 200}
    fixed_cost = {0: 1000, 1: 1200}
    transport_cost = {(0,0): 2, (0,1): 3, (1,0): 3, (1,1): 2}
    
    # Create optimization model
    model = LpProblem("Facility_Location", LpMinimize)
    
    # Decision variables
    x = LpVariable.dicts("ship", ((w,c) for w in warehouses for c in customers), 0)
    y = LpVariable.dicts("build", warehouses, 0, 1, LpBinary)
    
    # Objective function
    model += (lpSum(fixed_cost[w] * y[w] for w in warehouses) +
             lpSum(transport_cost[w,c] * x[w,c] for w in warehouses for c in customers))
    
    # Constraints
    for c in customers:
        model += lpSum(x[w,c] for w in warehouses) == demand[c]
    
    for w in warehouses:
        model += lpSum(x[w,c] for c in customers) <= capacity[w] * y[w]
    
    # Solve model
    model.solve()
    
    # Verify solution
    assert LpStatus[model.status] == 'Optimal'
    total_cost = value(model.objective)
    assert total_cost > 0
    
    # Check if solution meets demand
    for c in customers:
        customer_supply = sum(value(x[w,c]) for w in warehouses)
        assert np.isclose(customer_supply, demand[c])
    
    # Check capacity constraints
    for w in warehouses:
        warehouse_shipments = sum(value(x[w,c]) for c in customers)
        assert warehouse_shipments <= capacity[w]

def test_multi_period_planning():
    """Test multi-period warehouse planning with inventory."""
    periods = range(2)
    warehouses = range(2)
    customers = range(2)

    # Test data
    demand = {(t,c): 100 for t in periods for c in customers}
    capacity = {w: 250 for w in warehouses}
    holding_cost = 1
    initial_inventory = {w: 100 for w in warehouses}  # Add initial inventory

    # Create model
    model = LpProblem("Multi_Period_Planning", LpMinimize)

    # Variables
    x = LpVariable.dicts("ship", ((t,w,c) for t in periods for w in warehouses for c in customers), 0)
    i = LpVariable.dicts("inventory", ((t,w) for t in periods for w in warehouses), 0)

    # Objective: minimize total cost
    model += (lpSum(holding_cost * i[t,w] for t in periods for w in warehouses))

    # Constraints
    for t in periods:
        for c in customers:
            # Demand satisfaction
            model += lpSum(x[t,w,c] for w in warehouses) == demand[t,c]

        for w in warehouses:
            # Inventory balance
            if t == 0:
                # First period uses initial inventory
                model += (i[t,w] == initial_inventory[w] - lpSum(x[t,w,c] for c in customers))
            else:
                # Other periods use previous period's inventory
                model += (i[t,w] == i[t-1,w] - lpSum(x[t,w,c] for c in customers))

            # Capacity constraint includes both shipments and inventory
            model += (lpSum(x[t,w,c] for c in customers) + i[t,w]) <= capacity[w]

    # Solve
    model.solve()

    # Verify solution
    assert LpStatus[model.status] == 'Optimal'

    # Check solution properties
    for t in periods:
        for w in warehouses:
            # Inventory should be non-negative
            assert value(i[t,w]) >= 0
            # Total flow should respect capacity
            assert sum(value(x[t,w,c]) for c in customers) + value(i[t,w]) <= capacity[w]

def test_transportation_costs():
    """Test transportation cost calculations and optimization."""
    warehouses = range(2)
    customers = range(2)
    
    # Test data
    distances = {(w,c): 100 for w in warehouses for c in customers}
    demand = {c: 100 for c in customers}
    capacity = {w: 200 for w in warehouses}
    cost_per_mile = 2
    
    # Calculate transportation costs
    transport_cost = {(w,c): distances[w,c] * cost_per_mile 
                     for w in warehouses for c in customers}
    
    # Create model
    model = LpProblem("Transportation", LpMinimize)
    
    # Variables
    x = LpVariable.dicts("ship", ((w,c) for w in warehouses for c in customers), 0)
    
    # Objective
    model += lpSum(transport_cost[w,c] * x[w,c] for w in warehouses for c in customers)
    
    # Constraints
    for c in customers:
        model += lpSum(x[w,c] for w in warehouses) == demand[c]
    
    for w in warehouses:
        model += lpSum(x[w,c] for c in customers) <= capacity[w]
    
    # Solve
    model.solve()
    
    # Verify solution
    assert LpStatus[model.status] == 'Optimal'
    assert value(model.objective) > 0
    
    # Check demand satisfaction
    for c in customers:
        supply = sum(value(x[w,c]) for w in warehouses)
        assert np.isclose(supply, demand[c])

if __name__ == '__main__':
    pytest.main([__file__])
