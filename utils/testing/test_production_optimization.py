"""
Test module for basic production optimization notebook.
Tests production planning, scheduling, and resource allocation functions.
"""

import numpy as np
import pytest
from pulp import *

def test_basic_production_planning():
    """Test basic production planning optimization."""
    products = range(2)
    resources = range(2)
    
    # Test data
    profit = {0: 100, 1: 150}  # Profit per unit
    demand = {0: 50, 1: 30}    # Maximum demand
    resource_capacity = {0: 200, 1: 180}  # Resource availability
    
    # Resource usage per unit
    resource_usage = {
        (0,0): 2, (0,1): 3,  # Product 0 resource usage
        (1,0): 4, (1,1): 2   # Product 1 resource usage
    }
    
    # Create model
    model = LpProblem("Production_Planning", LpMaximize)
    
    # Variables
    x = LpVariable.dicts("produce", products, 0)
    
    # Objective
    model += lpSum(profit[p] * x[p] for p in products)
    
    # Constraints
    for r in resources:
        model += (lpSum(resource_usage[p,r] * x[p] for p in products) 
                 <= resource_capacity[r])
    
    for p in products:
        model += x[p] <= demand[p]
    
    # Solve
    model.solve()
    
    # Verify solution
    assert LpStatus[model.status] == 'Optimal'
    assert value(model.objective) > 0
    
    # Check demand constraints
    for p in products:
        assert value(x[p]) <= demand[p]
    
    # Check resource constraints
    for r in resources:
        usage = sum(resource_usage[p,r] * value(x[p]) for p in products)
        assert usage <= resource_capacity[r]

def test_multi_period_production():
    """Test multi-period production planning with inventory."""
    products = range(2)
    periods = range(3)
    
    # Test data
    production_cost = {p: 50 for p in products}
    holding_cost = {p: 10 for p in products}
    demand = {(t,p): 100 for t in periods for p in products}
    capacity = {p: 150 for p in products}
    
    # Create model
    model = LpProblem("Multi_Period_Production", LpMinimize)
    
    # Variables
    produce = LpVariable.dicts("produce",
                            ((t,p) for t in periods for p in products),
                            0)
    inventory = LpVariable.dicts("inventory",
                              ((t,p) for t in periods for p in products),
                              0)
    
    # Objective
    model += (lpSum(production_cost[p] * produce[t,p] +
                   holding_cost[p] * inventory[t,p]
                   for t in periods for p in products))
    
    # Constraints
    for t in periods:
        for p in products:
            # Inventory balance
            if t == 0:
                model += (inventory[t,p] == 0 + produce[t,p] - demand[t,p])
            else:
                model += (inventory[t,p] == inventory[t-1,p] + 
                         produce[t,p] - demand[t,p])
            
            # Capacity constraints
            model += produce[t,p] <= capacity[p]
    
    # Solve
    model.solve()
    
    # Verify solution
    assert LpStatus[model.status] == 'Optimal'
    assert value(model.objective) >= 0
    
    # Check capacity constraints
    for t in periods:
        for p in products:
            assert value(produce[t,p]) <= capacity[p]
    
    # Check inventory balance
    for t in periods:
        for p in products:
            if t == 0:
                balance = value(inventory[t,p]) == (0 + value(produce[t,p]) - 
                                                  demand[t,p])
            else:
                balance = value(inventory[t,p]) == (value(inventory[t-1,p]) + 
                                                  value(produce[t,p]) - 
                                                  demand[t,p])
            assert np.isclose(balance, True)

def test_resource_allocation():
    """Test resource allocation and scheduling optimization."""
    machines = range(2)
    jobs = range(3)
    periods = range(4)
    
    # Test data
    processing_time = {(j,m): 2 for j in jobs for m in machines}
    due_date = {j: 3 for j in jobs}
    tardiness_cost = {j: 100 for j in jobs}
    
    # Create model
    model = LpProblem("Resource_Allocation", LpMinimize)
    
    # Variables
    x = LpVariable.dicts("schedule",
                       ((j,m,t) for j in jobs 
                        for m in machines for t in periods),
                       0, 1, LpBinary)
    completion = LpVariable.dicts("completion", jobs, 0)
    tardiness = LpVariable.dicts("tardiness", jobs, 0)
    
    # Objective
    model += lpSum(tardiness_cost[j] * tardiness[j] for j in jobs)
    
    # Constraints
    for j in jobs:
        # Each job must be processed exactly once
        model += (lpSum(x[j,m,t] for m in machines for t in periods) == 1)
        
        # Calculate completion time
        model += (completion[j] == 
                 lpSum((t + processing_time[j,m]) * x[j,m,t] 
                      for m in machines for t in periods))
        
        # Calculate tardiness
        model += tardiness[j] >= completion[j] - due_date[j]
        model += tardiness[j] >= 0
    
    # Machine capacity constraints
    for m in machines:
        for t in periods:
            # No overlap of jobs
            model += (lpSum(x[j,m,tt] 
                          for j in jobs 
                          for tt in range(max(0, t-processing_time[j,m]+1), t+1))
                     <= 1)
    
    # Solve
    model.solve()
    
    # Verify solution
    assert LpStatus[model.status] == 'Optimal'
    assert value(model.objective) >= 0
    
    # Check if each job is scheduled exactly once
    for j in jobs:
        scheduled = sum(value(x[j,m,t]) 
                      for m in machines for t in periods)
        assert np.isclose(scheduled, 1)
    
    # Check machine capacity
    for m in machines:
        for t in periods:
            usage = sum(value(x[j,m,tt])
                      for j in jobs
                      for tt in range(max(0, t-processing_time[j,m]+1), t+1))
            assert usage <= 1

def test_setup_times():
    """Test production planning with setup times."""
    products = range(2)
    periods = range(2)
    
    # Test data
    setup_time = {(i,j): 1 for i in products for j in products}
    production_time = {p: 2 for p in products}
    demand = {(t,p): 10 for t in periods for p in products}
    capacity = 50  # Time capacity per period
    
    # Create model
    model = LpProblem("Setup_Times", LpMinimize)
    
    # Variables
    produce = LpVariable.dicts("produce",
                            ((t,p) for t in periods for p in products),
                            0)
    setup = LpVariable.dicts("setup",
                          ((t,i,j) for t in periods 
                           for i in products for j in products),
                          0, 1, LpBinary)
    
    # Objective: minimize setups
    model += lpSum(setup[t,i,j] for t in periods 
                  for i in products for j in products)
    
    # Constraints
    for t in periods:
        # Capacity constraint including setup times
        model += (lpSum(production_time[p] * produce[t,p] for p in products) +
                 lpSum(setup_time[i,j] * setup[t,i,j] 
                      for i in products for j in products) <= capacity)
        
        # Setup forcing constraints
        for p in products:
            model += produce[t,p] <= capacity * lpSum(setup[t,i,p] 
                                                    for i in products)
    
        # Flow conservation of setups
        for j in products:
            model += lpSum(setup[t,i,j] for i in products) == lpSum(setup[t,j,k] 
                                                                   for k in products)
    
    # Solve
    model.solve()
    
    # Verify solution
    assert LpStatus[model.status] == 'Optimal'
    assert value(model.objective) >= 0
    
    # Check capacity constraints
    for t in periods:
        time_used = (sum(production_time[p] * value(produce[t,p]) 
                        for p in products) +
                    sum(setup_time[i,j] * value(setup[t,i,j])
                        for i in products for j in products))
        assert time_used <= capacity

if __name__ == '__main__':
    pytest.main([__file__])
