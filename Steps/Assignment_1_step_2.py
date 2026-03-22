# ==========================================================
# STEP 2: MULTI-HOUR MARKET MODEL WITH STORAGE
# ==========================================================

import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8-whitegrid")

T = range(1, 25)

# ---------------------------------------------------------
# LOAD WIND DATA
# ---------------------------------------------------------

def load_wind_data():

    W1 = pd.read_csv(r'data_from_Jakob\scen_zone1.csv').iloc[1:25,1:].mean(axis=1)
    W2 = pd.read_csv(r'data_from_Jakob\scen_zone2.csv').iloc[1:25,1:].mean(axis=1)
    W3 = pd.read_csv(r'data_from_Jakob\scen_zone3.csv').iloc[1:25,1:].mean(axis=1)
    W4 = pd.read_csv(r'data_from_Jakob\scen_zone4.csv').iloc[1:25,1:].mean(axis=1)
    W5 = pd.read_csv(r'data_from_Jakob\scen_zone5.csv').iloc[1:25,1:].mean(axis=1)
    W6 = pd.read_csv(r'data_from_Jakob\scen_zone6.csv').iloc[1:25,1:].mean(axis=1)

    return [W1, W2, W3, W4, W5, W6]


Wind_CF = load_wind_data()

# ---------------------------------------------------------
# MARKET MODEL
# ---------------------------------------------------------

def run_market_model(P_ch, P_dis, E_max, plot_results=False):

    model = gp.Model("Copperplate")

    eta_ch = 0.90
    eta_dis = 0.95

    # ------------------------------------------------------
    # STORAGE VARIABLES
    # ------------------------------------------------------

    p_ch = {t: model.addVar(lb=0, ub=P_ch) for t in T}
    p_dis = {t: model.addVar(lb=0, ub=P_dis) for t in T}
    e = {t: model.addVar(lb=0, ub=E_max) for t in T}

    from data import load_distribution, load_profile, generators, generator_bid_prices, Prices_for_loads

    VARIABLES = list(generators.keys())
    LOAD_VARIABLES = list(load_distribution.keys())

    Generation_price = [v[1] for v in generator_bid_prices.values()]
    objective_coeff = {VARIABLES[i]: Generation_price[i] for i in range(len(VARIABLES))}

    Load_percentage = [v['percent'] for v in load_distribution.values()]
    Load_t = {t: load_profile[t] for t in T}

    Load_node_t = {t: [Load_t[t]*(i/100) for i in Load_percentage] for t in T}

    Load_coefficients = {}
    for t in T:
        prices_t = np.array(sorted(Prices_for_loads[t], reverse=True))
        for i, l in enumerate(LOAD_VARIABLES):
            Load_coefficients[(l, t)] = prices_t[i]

    Generator_UB = {k: v['Pmax_MW'] for k, v in generators.items() if k.startswith('G')}

    Wind_UB_t = {
        t: np.array([Wind_CF[i].iloc[t-1] for i in range(6)]) * 200
        for t in T
    }

    # ------------------------------------------------------
    # GENERATION & LOAD VARIABLES
    # ------------------------------------------------------
    variables = {(v, t): model.addVar(lb=0) for v in VARIABLES for t in T}

    # LOAD VARIABLES
    load_variables = {
        (l, t): model.addVar(lb=0, ub=Load_node_t[t][i])
        for i, l in enumerate(LOAD_VARIABLES)
        for t in T
    }

    # OBJECTIVE FUNCTION
    objective = gp.quicksum(
        Load_coefficients[(l, t)] * load_variables[(l, t)]
        for l in LOAD_VARIABLES for t in T
    ) - gp.quicksum(
        objective_coeff[v] * variables[(v, t)]
        for v in VARIABLES for t in T
    )

    model.setObjective(objective, GRB.MAXIMIZE)

    # GENERATOR LIMITS
    for v in VARIABLES:
        for t in T:
            if v in Generator_UB:
                model.addConstr(variables[(v, t)] <= Generator_UB[v])

    # WIND LIMITS
    for t in T:
        for i in range(6):
            wind_var = VARIABLES[-6 + i]
            model.addConstr(variables[(wind_var, t)] <= Wind_UB_t[t][i])

    # POWER BALANCE
    balance = {}
    for t in T:
        balance[t] = model.addConstr(
            gp.quicksum(variables[(v, t)] for v in VARIABLES)
            + p_dis[t] - p_ch[t]
            ==
            gp.quicksum(load_variables[(l, t)] for l in LOAD_VARIABLES)
        )

    # STORAGE DYNAMICS
    model.addConstr(e[1] == p_ch[1]*eta_ch - p_dis[1]/eta_dis)

    for t in range(2, 25):
        model.addConstr(e[t] == e[t-1] + p_ch[t]*eta_ch - p_dis[t]/eta_dis)

    model.addConstr(e[24] == 0)

    model.optimize()

    # PRICES
    prices = {t: -balance[t].Pi for t in T}

    price_table = pd.DataFrame({
        "Hour": list(T),
        "Market Price (€/MWh)": [prices[t] for t in T]
    })

    print(price_table)

    # ------------------------------------------------------
    # MARGINAL GENERATOR
    # ------------------------------------------------------

    marginal_info = {}

    for t in T:
        active_generators = []

        for v in VARIABLES:
            gen = variables[(v, t)].X

            if gen > 1e-3:
                if v in Generator_UB:
                    if gen < Generator_UB[v] - 1e-3:
                        active_generators.append((v, objective_coeff[v]))
                else:
                    active_generators.append((v, objective_coeff[v]))

        if active_generators:
            marginal = max(active_generators, key=lambda x: x[1])
            marginal_info[t] = marginal
        else:
            marginal_info[t] = ("None", None)

    # Compare price vs marginal cost
    print("\n=== Price vs Marginal Cost ===")

    for t in T:
        gen_name, gen_cost = marginal_info[t]
        print(f"Hour {t}: Price = {prices[t]:.2f}, Marginal cost = {gen_cost}, Generator = {gen_name}")

    # ------------------------------------------------------
    # STORAGE ACTIVITY
    # ------------------------------------------------------

    print("\n=== Storage Activity ===")

    for t in T:
        print(f"Hour {t}: Charge = {p_ch[t].X:.2f}, Discharge = {p_dis[t].X:.2f}")

    # ------------------------------------------------------
    # PROFITS
    # ------------------------------------------------------

    # PRODUCERS PROFITS
    profits = {}

    for v in VARIABLES:
        profits[v] = sum(
            (prices[t] - objective_coeff[v]) * variables[(v, t)].X
            for t in T
        )

    profit_table = pd.DataFrame({
        "Generator": list(profits.keys()),
        "Profit (€)": list(profits.values())
    })

    print("\n=== Producer Profits ===")
    print(profit_table)

    # STORAGE PROFIT
    storage_profit = sum(
        prices[t] * (p_dis[t].X - p_ch[t].X)
        for t in T
    )

    print(f"\nStorage Profit: {storage_profit:.2f} €")

    # CHARGE/DISCHARGE
    charge = [p_ch[t].X for t in T]
    discharge = [p_dis[t].X for t in T]

    total_supply = [sum(variables[(v, t)].X for v in VARIABLES) for t in T]
    total_demand = [sum(load_variables[(l, t)].X for l in LOAD_VARIABLES) for t in T]

    # SOC
    soc = [e[t].X for t in T]

    # ------------------------------------------------------
    # SOCIAL WELFARE
    # ------------------------------------------------------

    # Total utility
    total_utility = sum(
        Load_coefficients[(l, t)] * load_variables[(l, t)].X
        for l in LOAD_VARIABLES for t in T
    )

    # Total generation cost
    total_cost = sum(
        objective_coeff[v] * variables[(v, t)].X
        for v in VARIABLES for t in T
    )

    # Social welfare
    social_welfare = total_utility - total_cost

    print(f"Total Utility: {total_utility:.2f} €")
    print(f"Total Generation Cost: {total_cost:.2f} €")
    print(f"Social Welfare: {social_welfare:.2f} €")

    # ---------------------------------------------------------
    # PLOTTING
    # ---------------------------------------------------------

    if plot_results:

        hours = list(T)

        plt.rcParams.update({
            "font.size": 18,
            "axes.titlesize": 18,
            "axes.labelsize": 14,
            "xtick.labelsize": 14,
            "ytick.labelsize": 14,
            "legend.fontsize": 14,
        })

        # Plot charging and discharging power profile over 24 hours
        plt.figure(figsize=(10, 5))
        plt.plot(hours, charge,    label="Charging")      # FIX: was storage_charge
        plt.plot(hours, discharge, label="Discharging")   # FIX: was storage_discharge
        plt.xlabel("Hour")
        plt.ylabel("Power (MW)")
        plt.title("Storage Operation")
        plt.legend()
        plt.grid()
        # plt.show()

        # Plot stored energy level over 24 hours
        plt.figure(figsize=(10, 5))
        plt.plot(hours, soc, marker='o')                  # FIX: was storage_energy
        plt.xlabel("Hour")
        plt.ylabel("Energy (MWh)")
        plt.title("Stored Energy Level")
        plt.grid()
        # plt.show()

        # Combined supply/demand + storage figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

        # --------------------------
        # TOP: Supply/Demand + Price
        # --------------------------

        ax1.plot(hours, total_supply,
                 color="tab:green",
                 linewidth=2.5,
                 label="Total Supply")

        ax1.plot(hours, total_demand,
                 color="tab:red",
                 linewidth=2.5,
                 label="Total Demand")

        ax1.set_ylabel("Power (MW)")

        ax_price = ax1.twinx()

        ax_price.plot(hours,
                      list(prices.values()),
                      color="black",
                      marker="o",
                      linewidth=2,
                      label="Market Price")

        ax_price.set_ylabel("Price (€/MWh)")
        ax_price.set_yticks(np.arange(5, 10.5, 1))

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax_price.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

        # --------------------------
        # BOTTOM: Storage Operation
        # --------------------------

        ax2.bar(hours, charge,
                width=0.5,
                alpha=0.6,
                color="tab:blue",
                label="Charging")

        ax2.bar(hours, [-d for d in discharge],
                width=0.5,
                alpha=0.7,
                color="tab:orange",
                label="Discharging")

        ax2.set_ylabel("Storage Power (MW)")
        ax2.set_xlabel("Hour")
        ax2.axhline(0, color="black", linewidth=1)

        ax_soc = ax2.twinx()

        ax_soc.plot(hours, soc,
                    color="black",
                    linestyle="--",
                    linewidth=2,
                    marker="o",
                    label="State of Charge")

        ax_soc.set_ylabel("Energy (MWh)")
        ax_soc.set_yticks(np.arange(0, 450, 50))

        lines1, labels1 = ax2.get_legend_handles_labels()
        lines2, labels2 = ax_soc.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

        plt.tight_layout()
        plt.savefig("Results/Step2_market_model.png")
        plt.close()

    return list(prices.values()), charge, discharge, soc


# ---------------------------------------------------------
# BASE RUN
# ---------------------------------------------------------

run_market_model(100, 100, 400, plot_results=True)

# ---------------------------------------------------------
# SENSITIVITY ANALYSIS
# ---------------------------------------------------------

title_size = 18
label_size = 14
tick_size = 14
legend_size = 14

colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]

hours = list(T)

# ==========================================================
# SENSITIVITY 1 — STORAGE ENERGY CAPACITY
# ==========================================================

sizes = [0, 400, 500]
results = {}
storage_sizes = []     # FIX: was undefined
peak_prices_E = []     # FIX: was undefined

for E in sizes:
    P = E / 4 if E > 0 else 0
    prices_list, charge, discharge, soc = run_market_model(P, P, E, plot_results=False)
    results[E] = (prices_list, charge, discharge, soc)
    storage_sizes.append(E)
    peak_prices_E.append(max(prices_list))

# Price profiles
fig, ax1 = plt.subplots(figsize=(12, 6))

for i, E in enumerate(sizes):
    prices_list = results[E][0]
    ax1.plot(hours, prices_list,
             marker=None,
             color=colors[i],
             linewidth=2,
             label=f"E={E} MWh")

ax1.set_xlabel("Hour", fontsize=label_size)
ax1.set_ylabel("Price (€/MWh)", fontsize=label_size)
ax1.tick_params(axis='both', which='major', labelsize=tick_size)
ax1.grid(True, linestyle="--", alpha=0.6)
ax1.legend(fontsize=legend_size)
plt.tight_layout()
plt.savefig("Results/Step2_storage_size_sensitivity.png")
plt.close()

# Peak price vs storage capacity
plt.figure(figsize=(10, 5))
plt.plot(storage_sizes, peak_prices_E, linewidth=2)
plt.scatter(storage_sizes, peak_prices_E)
plt.title("Effect of Storage Energy Capacity on Peak Electricity Price")
plt.xlabel("Storage Capacity (MWh)")
plt.ylabel("Peak Market Price (€/MWh)")
plt.grid(True)
# plt.show()
plt.savefig("Results/Step2_storage_capacity_peak.png")
plt.close()

# ==========================================================
# SENSITIVITY 2 — CHARGING POWER LIMIT
# ==========================================================

charging_limits = np.linspace(0, 400, 10)
peak_prices_ch = []

for P in charging_limits:
    prices_list, *_ = run_market_model(P_ch=P, P_dis=100, E_max=400)  # FIX: unpack tuple, not dict
    peak_prices_ch.append(max(prices_list))

plt.figure(figsize=(10, 5))
plt.plot(charging_limits, peak_prices_ch, linewidth=2)
plt.scatter(charging_limits, peak_prices_ch)
plt.title("Effect of Charging Power on Peak Electricity Price")
plt.xlabel("Charging Power Limit (MW)")
plt.ylabel("Peak Market Price (€/MWh)")
plt.grid(True)
# plt.show()
plt.savefig("Results/Step2_charging_power_peak.png")
plt.close()

# ==========================================================
# SENSITIVITY 3 — CHARGING POWER (price profiles)
# ==========================================================

E_fixed = 400
P_discharge_fixed = 100

charge_sizes = [50, 100, 400]
results_charge = {}

for P_charge in charge_sizes:
    results_charge[P_charge] = run_market_model(
        P_charge, P_discharge_fixed, E_fixed, plot_results=False
    )

fig, ax1 = plt.subplots(figsize=(12, 6))

for i, P_charge in enumerate(charge_sizes):
    prices_list = results_charge[P_charge][0]
    ax1.plot(hours, prices_list,
             marker=None,
             color=colors[i],
             linewidth=2,
             label=f"P_charge={P_charge} MW")

ax1.set_xlabel("Hour")
ax1.set_ylabel("Price (€/MWh)")
ax1.grid(True, linestyle="--", alpha=0.6)
ax1.legend()
plt.tight_layout()
plt.savefig("Results/Step2_Charging_power_sensitivity.png")
plt.close()

# ==========================================================
# SENSITIVITY 4 — DISCHARGING POWER LIMIT
# ==========================================================

discharging_limits = np.linspace(0, 400, 10)   # FIX: was undefined
peak_prices_dis = []                            # FIX: was undefined

for P in discharging_limits:
    prices_list, *_ = run_market_model(P_ch=100, P_dis=P, E_max=400)
    peak_prices_dis.append(max(prices_list))

plt.figure(figsize=(10, 5))
plt.plot(discharging_limits, peak_prices_dis, linewidth=2)
plt.scatter(discharging_limits, peak_prices_dis)
plt.title("Effect of Discharging Power on Peak Electricity Price")
plt.xlabel("Discharging Power Limit (MW)")
plt.ylabel("Peak Market Price (€/MWh)")
plt.grid(True)
# plt.show()
plt.savefig("Results/Step2_discharging_power_peak.png")
plt.close()

# ==========================================================
# SENSITIVITY 5 — DISCHARGING POWER (price profiles)
# ==========================================================

P_charge_fixed = 100

discharge_sizes = [50, 100, 400]
results_discharge = {}

for P_discharge in discharge_sizes:
    results_discharge[P_discharge] = run_market_model(
        P_charge_fixed, P_discharge, E_fixed, plot_results=False
    )

fig, ax1 = plt.subplots(figsize=(12, 6))

for i, P_discharge in enumerate(discharge_sizes):
    prices_list = results_discharge[P_discharge][0]
    ax1.plot(hours, prices_list,
             marker=None,
             color=colors[i],
             linewidth=2,
             label=f"P_discharge={P_discharge} MW")

ax1.set_xlabel("Hour")
ax1.set_ylabel("Price (€/MWh)")
ax1.grid(True, linestyle="--", alpha=0.6)
ax1.legend()
plt.tight_layout()
plt.savefig("Results/Step2_discharging_power_sensitivity.png")
plt.close()

# ---------------------------------------------------------
# TABLE: STORAGE SIZE SUMMARY
# ---------------------------------------------------------

summary_storage = []

for E in sizes:
    prices_list, charge, discharge, _ = results[E]

    summary_storage.append({
        "Storage Size (MWh)": E,
        "Avg Price": np.mean(prices_list),
        "Price Std": np.std(prices_list),
        "Max Price": np.max(prices_list),
        "Min Price": np.min(prices_list),
        "Price Spread": np.max(prices_list) - np.min(prices_list),
        "Total Charge (MWh)": sum(charge),
        "Total Discharge (MWh)": sum(discharge)
    })

df_storage = pd.DataFrame(summary_storage)

pd.set_option('display.max_columns', None)
print("\n=== STORAGE SIZE SENSITIVITY ===")
print(df_storage.round(2))