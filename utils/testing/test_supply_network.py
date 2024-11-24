"""
Test module for supply network design optimization notebook.
Tests network flow optimization and supply chain network design functions.
"""

import numpy as np
import pytest
from pulp import *

def test_network_flow():
    """Test basic network flow optimization."""
    # Test data
    nodes = range(4)  # 0,1 are suppliers, 2,3 are customers
    suppliers = [0, 1]
    customers = [2, 3]
    
    supply = {0: 100, 1: 150}
    demand = {2: 120, 3: 130}
    
    # All possible arcs
    arcs = [(i,j) for i in suppliers for j in customers]
    costs = {(i,j): 10 for i,j in arcs}  # Unit transportation costs
    
    # Create model
    model = LpProblem("Network_Flow", LpMinimize)
    
    # Variables
    flow = LpVariable.dicts("flow", arcs, 0)
    
    # Objective
    model += lpSum(costs[i,j] * flow[i,j] for i,j in arcs)
    
    # Constraints
    for i in suppliers:
        model += lpSum(flow[i,j] for j in customers) <= supply[i]
    
    for j in customers:
        model += lpSum(flow[i,j] for i in suppliers) == demand[j]
    
    # Solve
    model.solve()
    
    # Verify solution
    assert LpStatus[model.status] == 'Optimal'
    assert value(model.objective) > 0
    
    # Check flow conservation
    for j in customers:
        inflow = sum(value(flow[i,j]) for i in suppliers)
        assert np.isclose(inflow, demand[j])

def test_capacity_expansion():
    """Test network capacity expansion decisions."""
    locations = range(3)
    periods = range(2)
    
    # Test data
    base_capacity = {i: 100 for i in locations}
    expansion_cost = {i: 1000 for i in locations}
    expansion_size = {i: 50 for i in locations}
    demand = {(t,i): 120 for t in periods for i in locations}
    
    # Create model
    model = LpProblem("Capacity_Expansion", LpMinimize)
    
    # Variables
    expand = LpVariable.dicts("expand", 
                            ((t,i) for t in periods for i in locations),
                            0, 1, LpBinary)
    production = LpVariable.dicts("produce",
                               ((t,i) for t in periods for i in locations),
                               0)
    
    # Objective
    model += lpSum(expansion_cost[i] * expand[t,i] 
                  for t in periods for i in locations)
    
    # Constraints
    for t in periods:
        for i in locations:
            # Capacity constraint
            model += (production[t,i] <= base_capacity[i] + 
                     expansion_size[i] * lpSum(expand[tt,i] for tt in range(t+1)))
            # Demand satisfaction
            model += production[t,i] >= demand[t,i]
    
    # Solve
    model.solve()
    
    # Verify solution
    assert LpStatus[model.status] == 'Optimal'
    assert value(model.objective) >= 0
    
    # Check capacity constraints
    for t in periods:
        for i in locations:
            assert value(production[t,i]) >= demand[t,i]

def test_multi_echelon_network():
    """Test multi-echelon supply chain network optimization."""
    plants = range(2)
    warehouses = range(2)
    customers = range(3)
    
    # Test data
    production_capacity = {p: 200 for p in plants}
    warehouse_capacity = {w: 150 for w in warehouses}
    customer_demand = {c: 100 for c in customers}
    
    # Transportation costs
    plant_to_wh_cost = {(p,w): 10 for p in plants for w in warehouses}
    wh_to_cust_cost = {(w,c): 5 for w in warehouses for c in customers}
    
    # Create model
    model = LpProblem("Multi_Echelon", LpMinimize)
    
    # Variables
    ship_to_wh = LpVariable.dicts("plant_to_wh",
                                ((p,w) for p in plants for w in warehouses),
                                0)
    ship_to_cust = LpVariable.dicts("wh_to_cust",
                                  ((w,c) for w in warehouses for c in customers),
                                  0)
    
    # Objective
    model += (lpSum(plant_to_wh_cost[p,w] * ship_to_wh[p,w] 
                   for p in plants for w in warehouses) +
             lpSum(wh_to_cust_cost[w,c] * ship_to_cust[w,c]
                   for w in warehouses for c in customers))
    
    # Constraints
    for p in plants:
        model += lpSum(ship_to_wh[p,w] for w in warehouses) <= production_capacity[p]
    
    for w in warehouses:
        model += (lpSum(ship_to_wh[p,w] for p in plants) ==
                 lpSum(ship_to_cust[w,c] for c in customers))
        model += lpSum(ship_to_cust[w,c] for c in customers) <= warehouse_capacity[w]
    
    for c in customers:
        model += lpSum(ship_to_cust[w,c] for w in warehouses) == customer_demand[c]
    
    # Solve
    model.solve()
    
    # Verify solution
    assert LpStatus[model.status] == 'Optimal'
    assert value(model.objective) > 0
    
    # Check flow conservation
    for w in warehouses:
        inflow = sum(value(ship_to_wh[p,w]) for p in plants)
        outflow = sum(value(ship_to_cust[w,c]) for c in customers)
        assert np.isclose(inflow, outflow)
    
    # Check demand satisfaction
    for c in customers:
        supply = sum(value(ship_to_cust[w,c]) for w in warehouses)
        assert np.isclose(supply, customer_demand[c])

def test_risk_mitigation():
    """Test supply chain network design with risk considerations."""
    locations = range(3)
    scenarios = range(2)  # Normal and disruption scenarios
    
    # Test data
    capacity = {i: 100 for i in locations}
    demand = {i: 80 for i in locations}
    disruption_prob = {i: 0.1 for i in locations}
    
    # Create model
    model = LpProblem("Risk_Mitigation", LpMinimize)
    
    # Variables
    # x[i,j,s] = flow from i to j in scenario s
    x = LpVariable.dicts("flow",
                       ((i,j,s) for i in locations 
                        for j in locations for s in scenarios),
                       0)
    
    # Objective: minimize expected cost
    scenario_prob = {0: 0.9, 1: 0.1}  # Probability of each scenario
    model += lpSum(scenario_prob[s] * x[i,j,s]
                  for i in locations for j in locations for s in scenarios)
    
    # Constraints
    for s in scenarios:
        for j in locations:
            # Demand satisfaction
            model += (lpSum(x[i,j,s] for i in locations) >= 
                     demand[j] * (1 - disruption_prob[j]))
            
            # Capacity constraints
            model += lpSum(x[i,j,s] for i in locations) <= capacity[j]
    
    # Solve
    model.solve()
    
    # Verify solution
    assert LpStatus[model.status] == 'Optimal'
    assert value(model.objective) >= 0
    
    # Check if demand is met in each scenario
    for s in scenarios:
        for j in locations:
            supply = sum(value(x[i,j,s]) for i in locations)
            assert supply >= demand[j] * (1 - disruption_prob[j])

if __name__ == '__main__':
    pytest.main([__file__])
