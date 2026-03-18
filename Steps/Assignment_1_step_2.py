
# Wrap model into a function to allow sensitivity analysis by varying storage parameters
def run_market_model(P_ch, P_dis, E_max, plot_results=False, analyze_prices=False):

    import gurobipy as gp
    from gurobipy import GRB
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import os

    # 24 hours in a day
    T = range(1, 25)

    # ---------------------------------------------------------
    # Import wind data
    # ---------------------------------------------------------
    # Read capacity factor (CF) scenarios for each of the 6 wind zones
    # Each CSV contains multiple scenarios — we average across all scenarios per hour
    # Rows 1:25 correspond to hours 1-24, columns 1: are the scenario values
    # Final CF is a 24-element series representing the average hourly wind output fraction

    W1_data = pd.read_csv(r'data_from_Jakob\scen_zone1.csv')
    W1_CF = W1_data.iloc[1:25, 1:].mean(axis=1)

    W2_data = pd.read_csv(r'data_from_Jakob\scen_zone2.csv')
    W2_CF = W2_data.iloc[1:25, 1:].mean(axis=1)

    W3_data = pd.read_csv(r'data_from_Jakob\scen_zone3.csv')
    W3_CF = W3_data.iloc[1:25, 1:].mean(axis=1)

    W4_data = pd.read_csv(r'data_from_Jakob\scen_zone4.csv')
    W4_CF = W4_data.iloc[1:25, 1:].mean(axis=1)

    W5_data = pd.read_csv(r'data_from_Jakob\scen_zone5.csv')
    W5_CF = W5_data.iloc[1:25, 1:].mean(axis=1)

    W6_data = pd.read_csv(r'data_from_Jakob\scen_zone6.csv')
    W6_CF = W6_data.iloc[1:25, 1:].mean(axis=1)

    # Collect all wind CF series into a list for easy indexing
    Wind_CF = [W1_CF, W2_CF, W3_CF, W4_CF, W5_CF, W6_CF]

    # ---------------------------------------------------------
    # Create Gurobi model
    # ---------------------------------------------------------

    model = gp.Model("Copperplate")

    # Storage round-trip efficiency parameters
    eta_ch  = 0.90   # charging efficiency (90%)
    eta_dis = 0.95   # discharging efficiency (95%)

    # Storage decision variables for each hour t:
    # p_ch[t]  — power charged into storage [MW], bounded by max charging power P_ch
    # p_dis[t] — power discharged from storage [MW], bounded by max discharging power P_dis
    # e[t]     — stored energy level at end of hour t [MWh], bounded by energy capacity E_max
    p_ch  = {t: model.addVar(lb=0, ub=P_ch,  name=f"p_ch_{t}")  for t in T}
    p_dis = {t: model.addVar(lb=0, ub=P_dis, name=f"p_dis_{t}") for t in T}
    e     = {t: model.addVar(lb=0, ub=E_max, name=f"e_{t}")     for t in T}

    # ---------------------------------------------------------
    # Load system data
    # ---------------------------------------------------------

    from data import load_distribution, load_profile, generators, generator_bid_prices
    from data import Prices_for_loads

    # Generator and load variable name lists
    VARIABLES      = list(generators.keys())
    LOAD_VARIABLES = list(load_distribution.keys())

    # Generator bid prices (marginal costs) — extracted from hour 1 of each generator's price dict
    Generation_price = [v[1] for v in generator_bid_prices.values()]
    objective_coeff  = {VARIABLES[i]: Generation_price[i] for i in range(len(VARIABLES))}

    # Load distribution percentages and hourly total load [MW]
    Load_percentage = [v['percent'] for v in load_distribution.values()]
    Load_t          = {t: load_profile[t] for t in T}

    # Distribute total hourly load across individual load nodes by their percentage share
    Load_node_t = {
        t: [Load_t[t] * (i / 100) for i in Load_percentage]
        for t in T
    }

    # Demand bid prices per load per hour — sorted descending (highest willingness to pay first)
    # These represent the value consumers place on electricity [€/MWh]
    Load_coefficients = {}
    for t in T:
        prices_t = np.array(sorted(Prices_for_loads[t], reverse=True))
        for i, l in enumerate(LOAD_VARIABLES):
            Load_coefficients[(l, t)] = prices_t[i]

    # Maximum generation capacity per conventional generator [MW]
    Generator_UB = {
        k: v['Pmax_MW']
        for k, v in generators.items()
        if k.startswith('G')
    }

    # Wind generation upper bounds per hour: CF * installed capacity (200 MW per farm)
    Wind_UB_t = {
        t: np.array([Wind_CF[i].iloc[t - 1] for i in range(6)]) * 200
        for t in T
    }

    # ---------------------------------------------------------
    # Decision variables — generation and demand
    # ---------------------------------------------------------

    # Generation dispatch variables [MW] for each generator and hour
    variables = {
        (v, t): model.addVar(lb=0, name=f"{v}_{t}")
        for v in VARIABLES for t in T
    }

    # Load served variables [MW] for each load and hour, bounded by their node's share of total load
    load_variables = {
        (l, t): model.addVar(lb=0, ub=Load_node_t[t][i], name=f"{l}_{t}")
        for i, l in enumerate(LOAD_VARIABLES)
        for t in T
    }

    # ---------------------------------------------------------
    # Objective — maximise social welfare
    # ---------------------------------------------------------
    # Social welfare = consumer utility (value of demand served) - generation cost
    # This is the standard market welfare maximisation formulation

    objective = gp.quicksum(
        Load_coefficients[(l, t)] * load_variables[(l, t)]
        for l in LOAD_VARIABLES for t in T
    ) - gp.quicksum(
        objective_coeff[v] * variables[(v, t)]
        for v in VARIABLES for t in T
    )

    model.setObjective(objective, GRB.MAXIMIZE)

    # ---------------------------------------------------------
    # Generator capacity constraints
    # ---------------------------------------------------------

    # Conventional generators: dispatch <= Pmax
    for v in VARIABLES:
        for t in T:
            if v in Generator_UB:
                model.addConstr(variables[(v, t)] <= Generator_UB[v])

    # Wind farms: dispatch <= CF * installed capacity (varies by hour)
    for t in T:
        for i in range(6):
            wind_var = VARIABLES[-6 + i]
            model.addConstr(variables[(wind_var, t)] <= Wind_UB_t[t][i])

    # ---------------------------------------------------------
    # Power balance constraint (copperplate — no transmission limits)
    # ---------------------------------------------------------
    # For each hour: total generation + storage discharge - storage charge = total demand served
    # The dual variable (shadow price) of this constraint is the market clearing price

    balance = {}
    for t in T:
        balance[t] = model.addConstr(
            gp.quicksum(variables[(v, t)] for v in VARIABLES)
            + p_dis[t] - p_ch[t]
            ==
            gp.quicksum(load_variables[(l, t)] for l in LOAD_VARIABLES),
            name=f"balance_{t}"
        )

    # ---------------------------------------------------------
    # Storage energy dynamics
    # ---------------------------------------------------------
    # Hour 1: energy stored = energy charged * efficiency - energy discharged / efficiency
    # Subsequent hours: energy carried over from previous hour plus net charge/discharge
    # Final hour: storage must return to empty (e[24] = 0) to avoid end-of-horizon effects

    model.addConstr(e[1] == p_ch[1] * eta_ch - p_dis[1] / eta_dis)

    for t in range(2, 25):
        model.addConstr(
            e[t] == e[t - 1] + p_ch[t] * eta_ch - p_dis[t] / eta_dis
        )

    # End-of-horizon constraint: storage must be empty at end of day 
    model.addConstr(e[24] == 0)

    # ---------------------------------------------------------
    # Solve
    # ---------------------------------------------------------

    model.optimize()

    # Extract market clearing prices as the negative dual of the balance constraint
    # (Gurobi convention: dual of equality constraint has sign depending on formulation)
    prices_with_storage = {t: -balance[t].Pi for t in T}

    # ---------------------------------------------------------
    # Optional plots
    # ---------------------------------------------------------

    if plot_results:

        storage_charge    = [p_ch[t].X  for t in T]
        storage_discharge = [p_dis[t].X for t in T]
        storage_energy    = [e[t].X     for t in T]

        # Plot charging and discharging power profile over 24 hours
        plt.figure(figsize=(10, 5))
        plt.plot(T, storage_charge,    label="Charging")
        plt.plot(T, storage_discharge, label="Discharging")
        plt.xlabel("Hour")
        plt.ylabel("Power (MW)")
        plt.title("Storage Operation")
        plt.legend()
        plt.grid()
        plt.show()

        # Plot stored energy level over 24 hours
        plt.figure(figsize=(10, 5))
        plt.plot(T, storage_energy, marker='o')
        plt.xlabel("Hour")
        plt.ylabel("Energy (MWh)")
        plt.title("Stored Energy Level")
        plt.grid()
        plt.show()

    return prices_with_storage


# ==========================================================
# BASE RUN — default storage parameters
# ==========================================================

run_market_model(
    P_ch=100,
    P_dis=100,
    E_max=400,
    plot_results=True
)


# ==========================================================
# SENSITIVITY 1 — STORAGE ENERGY CAPACITY
# ==========================================================
# Vary total energy capacity E_max from 0 to 1000 MWh
# Power limits scale proportionally at E/4 (C-rate of 0.25)
# Observe how peak market price changes as more energy storage is available

import numpy as np
import matplotlib.pyplot as plt

storage_sizes = np.linspace(0, 1000, 10)
peak_prices_E = []

for E in storage_sizes:
    prices = run_market_model(P_ch=E/4, P_dis=E/4, E_max=E)
    peak_prices_E.append(max(prices.values()))

plt.figure(figsize=(10, 5))
plt.plot(storage_sizes, peak_prices_E, linewidth=2)
plt.scatter(storage_sizes, peak_prices_E)
plt.title("Effect of Storage Energy Capacity on Peak Electricity Price")
plt.xlabel("Storage Capacity (MWh)")
plt.ylabel("Peak Market Price (€/MWh)")
plt.grid(True)
plt.show()


# ==========================================================
# SENSITIVITY 2 — CHARGING POWER LIMIT
# ==========================================================
# Vary max charging power P_ch from 0 to 400 MW
# Discharging fixed at 100 MW, energy capacity fixed at 400 MWh
# Higher charging power allows storage to absorb more excess generation,
# potentially lowering peak prices by shifting energy to high-demand hours

charging_limits = np.linspace(0, 400, 10)
peak_prices_ch  = []

for P in charging_limits:
    prices = run_market_model(P_ch=P, P_dis=100, E_max=400)
    peak_prices_ch.append(max(prices.values()))

plt.figure(figsize=(10, 5))
plt.plot(charging_limits, peak_prices_ch, linewidth=2)
plt.scatter(charging_limits, peak_prices_ch)
plt.title("Effect of Charging Power on Peak Electricity Price")
plt.xlabel("Charging Power Limit (MW)")
plt.ylabel("Peak Market Price (€/MWh)")
plt.grid(True)
plt.show()


# ==========================================================
# SENSITIVITY 3 — DISCHARGING POWER LIMIT
# ==========================================================
# Vary max discharging power P_dis from 0 to 400 MW
# Charging fixed at 100 MW, energy capacity fixed at 400 MWh
# Higher discharging power allows storage to inject more power during peak hours,
# reducing peak prices by supplementing generation capacity

discharging_limits = np.linspace(0, 400, 10)
peak_prices_dis    = []

for P in discharging_limits:
    prices = run_market_model(P_ch=100, P_dis=P, E_max=400)
    peak_prices_dis.append(max(prices.values()))

plt.figure(figsize=(10, 5))
plt.plot(discharging_limits, peak_prices_dis, linewidth=2)
plt.scatter(discharging_limits, peak_prices_dis)
plt.title("Effect of Discharging Power on Peak Electricity Price")
plt.xlabel("Discharging Power Limit (MW)")
plt.ylabel("Peak Market Price (€/MWh)")
plt.grid(True)
plt.show()