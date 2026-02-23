"""
Step 1: Copper-Plate, Single Hour Market Clearing
Uses Gurobi to solve the market-clearing optimization problem.
"""

import gurobipy as gp
from gurobipy import GRB
from data import (
    generators,
    load_profile,
    load_distribution,
    generator_bid_prices,
    load_bid_prices,
)

# =============================================================================
# PARAMETERS
# =============================================================================

# Pick a single hour to solve (change this to test different hours)
HOUR = 12
total_load_MW = load_profile[HOUR]

# Extract single-hour bid prices (from the hourly dictionaries in data.py)
gen_bid = {g: generator_bid_prices[g][HOUR] for g in generators}
load_bid = {load: load_bid_prices[load][HOUR] for load in load_distribution}

# Compute each load's MW demand for this hour based on their percentage
load_demand = {
    load: (load_distribution[load]['percent'] / 100) * total_load_MW
    for load in load_distribution
}

# =============================================================================
# OPTIMIZATION MODEL
# =============================================================================

model = gp.Model("Copper_Plate_Single_Hour")
model.Params.OutputFlag = 0  # set to 1 to see Gurobi solver output

# --- Decision Variables ---

# Power produced by each generator (MW)
p_gen = {
    g: model.addVar(
        lb=generators[g]['Pmin_MW'], #Pmin is always 0
        ub=generators[g]['Pmax_MW'],
        name=f"p_{g}"
    )
    for g in generators
}

# Power consumed by each load (MW)
p_load = {
    load: model.addVar(
        lb=0,
        ub=load_demand[load],
        name=f"d_{load}"
    )
    for load in load_distribution
}

# --- Objective Function ---
# Maximize social welfare = sum(load bid * load consumed) - sum(gen bid * gen produced)

model.setObjective(
    gp.quicksum(load_bid[load] * p_load[load] for load in load_distribution)
    - gp.quicksum(gen_bid[g] * p_gen[g] for g in generators),
    GRB.MAXIMIZE
)

# --- Constraints ---

# Power balance: total generation = total consumption (copper-plate, no network)
balance = model.addConstr(
    gp.quicksum(p_gen[g] for g in generators) ==
    gp.quicksum(p_load[load] for load in load_distribution),
    name="power_balance"
)

# --- Solve ---
model.optimize()

# =============================================================================
# RESULTS
# =============================================================================

if model.status == GRB.OPTIMAL:

    # Market-Clearing Price = dual variable of the power balance constraint
    mcp = balance.Pi

    print("\n" + "="*60)
    print(f"  MARKET CLEARING RESULTS - HOUR {HOUR}")
    print("="*60)
    print(f"\n  Market-Clearing Price (MCP): {mcp:.2f} $/MWh")

    # --- Social Welfare and Operating Cost ---
    total_gen_cost    = sum(gen_bid[g] * p_gen[g].X for g in generators)
    social_welfare    = model.ObjVal

    print(f"  Total Operating Cost:        {total_gen_cost:.2f} $")
    print(f"  Social Welfare:              {social_welfare:.2f} $")

    # --- Generator Results ---
    print("\n" + "-"*60)
    print(f"  {'Generator':<10} {'Bid ($/MWh)':<15} {'Output (MW)':<15} {'Profit ($)':<15} {'Status'}")
    print("-"*60)
    for g in generators:
        output = p_gen[g].X
        bid    = gen_bid[g]
        profit = (mcp - bid) * output
        if output < 1e-4:
            status = "rejected"
        elif output >= generators[g]['Pmax_MW'] - 1e-4:
            status = "accepted (at max)"
        else:
            status = "marginal"
        print(f"  {g:<10} {bid:<15.2f} {output:<15.2f} {profit:<15.2f} {status}")

    # --- Load Results ---
    print("\n" + "-"*60)
    print(f"  {'Load':<10} {'Bid ($/MWh)':<15} {'Consumed (MW)':<15} {'Utility ($)':<15} {'Status'}")
    print("-"*60)
    for load in load_distribution:
        consumed   = p_load[load].X
        bid        = load_bid[load]
        utility    = consumed * (bid - mcp)
        max_demand = load_demand[load]
        if consumed < 1e-4:
            status = "rejected"
        elif consumed >= max_demand - 1e-4:
            status = "accepted (full)"
        else:
            status = "marginal"
        print(f"  {load:<10} {bid:<15.2f} {consumed:<15.2f} {utility:<15.2f} {status}")

    # --- KKT Verification ---
    print("\n" + "="*60)
    print("  KKT CONDITIONS VERIFICATION")
    print("="*60)
    print(f"\n  MCP = {mcp:.2f} $/MWh (dual variable of the power balance constraint)")
    print("\n  Stationarity conditions for generators:")
    for g in generators:
        output = p_gen[g].X
        bid    = gen_bid[g]
        if output < 1e-4:
            print(f"    {g}: REJECTED  - bid ({bid:.2f}) > MCP ({mcp:.2f}), output = 0")
        elif output >= generators[g]['Pmax_MW'] - 1e-4:
            print(f"    {g}: ACCEPTED  - bid ({bid:.2f}) < MCP ({mcp:.2f}), output = Pmax")
        else:
            print(f"    {g}: MARGINAL  - bid ({bid:.2f}) ≈ MCP ({mcp:.2f}), sets the price")

else:
    print("No optimal solution found. Gurobi status:", model.status)