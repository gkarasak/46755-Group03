# Wrap model into a function (for sensitivity)
def run_market_model(P_ch, P_dis, E_max, plot_results=False, analyze_prices=False):

    import gurobipy as gp
    from gurobipy import GRB
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import os

    # 24 hours
    T = range(1,25)

    # ---------------------------------------------------------
    # Import wind data
    # ---------------------------------------------------------

    BASE_DIR = r'C:\Users\20221122\Downloads\DTU\SEMESTER 2\Renewables in electricity markets\46755-Group03'
    DATA_DIR = os.path.join(BASE_DIR, 'data_from_Jakob')

    W1_data = pd.read_csv(os.path.join(DATA_DIR, 'scen_zone1.csv'))
    W2_data = pd.read_csv(os.path.join(DATA_DIR, 'scen_zone2.csv'))
    W3_data = pd.read_csv(os.path.join(DATA_DIR, 'scen_zone3.csv'))
    W4_data = pd.read_csv(os.path.join(DATA_DIR, 'scen_zone4.csv'))
    W5_data = pd.read_csv(os.path.join(DATA_DIR, 'scen_zone5.csv'))
    W6_data = pd.read_csv(os.path.join(DATA_DIR, 'scen_zone6.csv'))

    W1_CF = W1_data.iloc[1:25,1:].mean(axis=1)
    W2_CF = W2_data.iloc[1:25,1:].mean(axis=1)
    W3_CF = W3_data.iloc[1:25,1:].mean(axis=1)
    W4_CF = W4_data.iloc[1:25,1:].mean(axis=1)
    W5_CF = W5_data.iloc[1:25,1:].mean(axis=1)
    W6_CF = W6_data.iloc[1:25,1:].mean(axis=1)

    Wind_CF = [W1_CF,W2_CF,W3_CF,W4_CF,W5_CF,W6_CF]

    # ---------------------------------------------------------
    # Create model
    # ---------------------------------------------------------

    model = gp.Model("Copperplate")

    eta_ch = 0.9
    eta_dis = 0.95

    # Storage variables
    p_ch = {t:model.addVar(lb=0,ub=P_ch,name=f"p_ch_{t}") for t in T}
    p_dis = {t:model.addVar(lb=0,ub=P_dis,name=f"p_dis_{t}") for t in T}
    e = {t:model.addVar(lb=0,ub=E_max,name=f"e_{t}") for t in T}

    # ---------------------------------------------------------
    # Load system data
    # ---------------------------------------------------------

    from data import load_distribution, load_profile, generators, generator_bid_prices
    from data import Prices_for_loads

    VARIABLES = list(generators.keys())
    LOAD_VARIABLES = list(load_distribution.keys())

    Generation_price = [v[1] for v in generator_bid_prices.values()]
    objective_coeff = {VARIABLES[i]:Generation_price[i] for i in range(len(VARIABLES))}

    Load_percentage = [v['percent'] for v in load_distribution.values()]
    Load_t = {t:load_profile[t] for t in T}

    Load_node_t = {
        t:[Load_t[t]*(i/100) for i in Load_percentage]
        for t in T
    }

    Load_coefficients = {}

    for t in T:
        prices_t = np.array(sorted(Prices_for_loads[t],reverse=True))
        for i,l in enumerate(LOAD_VARIABLES):
            Load_coefficients[(l,t)] = prices_t[i]

    Generator_UB = {
        k:v['Pmax_MW']
        for k,v in generators.items()
        if k.startswith('G')
    }

    Wind_UB_t = {
        t:np.array([Wind_CF[i].iloc[t-1] for i in range(6)])*200
        for t in T
    }

    # ---------------------------------------------------------
    # Variables
    # ---------------------------------------------------------

    variables = {
        (v,t):model.addVar(lb=0,name=f"{v}_{t}")
        for v in VARIABLES for t in T
    }

    load_variables = {
        (l,t):model.addVar(lb=0,ub=Load_node_t[t][i],name=f"{l}_{t}")
        for i,l in enumerate(LOAD_VARIABLES)
        for t in T
    }

    # ---------------------------------------------------------
    # Objective
    # ---------------------------------------------------------

    objective = gp.quicksum(
        Load_coefficients[(l,t)]*load_variables[(l,t)]
        for l in LOAD_VARIABLES for t in T
    ) - gp.quicksum(
        objective_coeff[v]*variables[(v,t)]
        for v in VARIABLES for t in T
    )

    model.setObjective(objective,GRB.MAXIMIZE)

    # ---------------------------------------------------------
    # Generator bounds
    # ---------------------------------------------------------

    for v in VARIABLES:
        for t in T:
            if v in Generator_UB:
                model.addConstr(variables[(v,t)] <= Generator_UB[v])

    for t in T:
        for i in range(6):
            wind_var = VARIABLES[-6+i]
            model.addConstr(variables[(wind_var,t)] <= Wind_UB_t[t][i])

    # ---------------------------------------------------------
    # Power balance
    # ---------------------------------------------------------

    balance = {}

    for t in T:
        balance[t] = model.addConstr(
            gp.quicksum(variables[(v,t)] for v in VARIABLES)
            + p_dis[t] - p_ch[t]
            ==
            gp.quicksum(load_variables[(l,t)] for l in LOAD_VARIABLES)
        )

    # ---------------------------------------------------------
    # Storage dynamics
    # ---------------------------------------------------------

    model.addConstr(e[1] == p_ch[1]*eta_ch - p_dis[1]/eta_dis)

    for t in range(2,25):
        model.addConstr(
            e[t] == e[t-1] + p_ch[t]*eta_ch - p_dis[t]/eta_dis
        )

    model.addConstr(e[24] == 0)

    # ---------------------------------------------------------
    # Solve
    # ---------------------------------------------------------

    model.optimize()

    prices_with_storage = {t:-balance[t].Pi for t in T}

    # ---------------------------------------------------------
    # Optional plots
    # ---------------------------------------------------------

    if plot_results:

        storage_charge = [p_ch[t].X for t in T]
        storage_discharge = [p_dis[t].X for t in T]
        storage_energy = [e[t].X for t in T]

        plt.figure(figsize=(10,5))
        plt.plot(T,storage_charge,label="Charging")
        plt.plot(T,storage_discharge,label="Discharging")
        plt.xlabel("Hour")
        plt.ylabel("Power (MW)")
        plt.title("Storage Operation")
        plt.legend()
        plt.grid()
        plt.show()

        plt.figure(figsize=(10,5))
        plt.plot(T,storage_energy,marker='o')
        plt.xlabel("Hour")
        plt.ylabel("Energy (MWh)")
        plt.title("Stored Energy Level")
        plt.grid()
        plt.show()

    return prices_with_storage


# ==========================================================
# BASE RUN
# ==========================================================

run_market_model(
    P_ch=300,
    P_dis=300,
    E_max=900,
    plot_results=True
)


# ==========================================================
# SENSITIVITY 1 — STORAGE ENERGY CAPACITY
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt

storage_sizes = np.linspace(0,1000,10)

peak_prices_E = []

for E in storage_sizes:

    prices = run_market_model(
        P_ch=E/3,
        P_dis=E/3,
        E_max=E
    )

    peak_prices_E.append(max(prices.values()))

plt.figure(figsize=(10,5))
plt.plot(storage_sizes, peak_prices_E, linewidth=2)
plt.scatter(storage_sizes, peak_prices_E)
plt.title("Effect of Storage Energy Capacity on Electricity Price")
plt.xlabel("Storage Capacity (MWh)")
plt.ylabel("Peak Market Price (€/MWh)")
plt.grid(True)
plt.show()


# ==========================================================
# SENSITIVITY 2 — CHARGING POWER LIMIT
# ==========================================================

charging_limits = np.linspace(0,500,10)

peak_prices_ch = []

for P in charging_limits:

    prices = run_market_model(
        P_ch=P,
        P_dis=300,
        E_max=900
    )

    peak_prices_ch.append(max(prices.values()))

plt.figure(figsize=(10,5))
plt.plot(charging_limits, peak_prices_ch, linewidth=2)
plt.scatter(charging_limits, peak_prices_ch)
plt.title("Effect of Charging Power on Electricity Price")
plt.xlabel("Charging Power Limit (MW)")
plt.ylabel("Peak Market Price (€/MWh)")
plt.grid(True)
plt.show()


# ==========================================================
# SENSITIVITY 3 — DISCHARGING POWER LIMIT
# ==========================================================

discharging_limits = np.linspace(0,500,10)

peak_prices_dis = []

for P in discharging_limits:

    prices = run_market_model(
        P_ch=300,
        P_dis=P,
        E_max=900
    )

    peak_prices_dis.append(max(prices.values()))

plt.figure(figsize=(10,5))
plt.plot(discharging_limits, peak_prices_dis, linewidth=2)
plt.scatter(discharging_limits, peak_prices_dis)
plt.title("Effect of Discharging Power on Electricity Price")
plt.xlabel("Discharging Power Limit (MW)")
plt.ylabel("Peak Market Price (€/MWh)")
plt.grid(True)
plt.show()