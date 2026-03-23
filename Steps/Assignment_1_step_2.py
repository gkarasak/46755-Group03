# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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

def run_market_model(P_ch, P_dis, E_max, plot_results=False, verbose=True):

    model = gp.Model("Copperplate")
    model.setParam("OutputFlag", 0)

    eta_ch = 0.90
    eta_dis = 0.95

    # STORAGE VARIABLES
    p_ch  = {t: model.addVar(lb=0, ub=P_ch)  for t in T}
    p_dis = {t: model.addVar(lb=0, ub=P_dis) for t in T}
    e     = {t: model.addVar(lb=0, ub=E_max) for t in T}

    from data import load_distribution, load_profile, generators, generator_bid_prices, Prices_for_loads

    VARIABLES      = list(generators.keys())
    LOAD_VARIABLES = list(load_distribution.keys())

    Generation_price = [v[1] for v in generator_bid_prices.values()]
    objective_coeff  = {VARIABLES[i]: Generation_price[i] for i in range(len(VARIABLES))}

    Load_percentage = [v['percent'] for v in load_distribution.values()]
    Load_t          = {t: load_profile[t] for t in T}
    Load_node_t     = {t: [Load_t[t]*(i/100) for i in Load_percentage] for t in T}

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

    # GENERATION VARIABLES
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

    # ---------------------------------------------------------
    # STORAGE DYNAMICS
    # e[t] = SOC at END of hour t (after charge/discharge in hour t)
    # E_init = SOC at START of hour 1 = SOC at END of hour 24 = 50%
    # ---------------------------------------------------------
    E_init = E_max / 2.0

    model.addConstr(e[1] == E_init + p_ch[1] * eta_ch - p_dis[1] / eta_dis)
    for t in range(2, 25):
        model.addConstr(e[t] == e[t-1] + p_ch[t] * eta_ch - p_dis[t] / eta_dis)
    model.addConstr(e[24] == E_init)

    model.optimize()

    # PRICES
    prices = {t: -balance[t].Pi for t in T}

    if verbose:
        price_table = pd.DataFrame({
            "Hour": list(T),
            "Market Price (EUR/MWh)": [prices[t] for t in T]
        })
        print(price_table)

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

        print("\n=== Price vs Marginal Cost ===")
        for t in T:
            gen_name, gen_cost = marginal_info[t]
            print(f"Hour {t}: Price = {prices[t]:.2f}, Marginal cost = {gen_cost}, Generator = {gen_name}")

        print("\n=== Storage Activity ===")
        for t in T:
            print(f"Hour {t}: Charge = {p_ch[t].X:.2f}, Discharge = {p_dis[t].X:.2f}")

        profits = {}
        for v in VARIABLES:
            profits[v] = sum(
                (prices[t] - objective_coeff[v]) * variables[(v, t)].X
                for t in T
            )
        profit_table = pd.DataFrame({
            "Generator": list(profits.keys()),
            "Profit (EUR)": list(profits.values())
        })
        print("\n=== Producer Profits ===")
        print(profit_table)

        storage_profit = sum(
            prices[t] * (p_dis[t].X - p_ch[t].X)
            for t in T
        )
        print(f"\nStorage Profit: {storage_profit:.2f} EUR")

        total_utility = sum(
            Load_coefficients[(l, t)] * load_variables[(l, t)].X
            for l in LOAD_VARIABLES for t in T
        )
        total_cost_val = sum(
            objective_coeff[v] * variables[(v, t)].X
            for v in VARIABLES for t in T
        )
        social_welfare = total_utility - total_cost_val
        print(f"Total Utility: {total_utility:.2f} EUR")
        print(f"Total Generation Cost: {total_cost_val:.2f} EUR")
        print(f"Social Welfare: {social_welfare:.2f} EUR")

    # CHARGE/DISCHARGE
    charge    = [p_ch[t].X  for t in T]
    discharge = [p_dis[t].X for t in T]

    total_supply = [sum(variables[(v, t)].X for v in VARIABLES) for t in T]
    total_demand = [sum(load_variables[(l, t)].X for l in LOAD_VARIABLES) for t in T]

    # SOCIAL WELFARE
    total_utility = sum(
        Load_coefficients[(l, t)] * load_variables[(l, t)].X
        for l in LOAD_VARIABLES for t in T
    )
    total_cost_val = sum(
        objective_coeff[v] * variables[(v, t)].X
        for v in VARIABLES for t in T
    )
    social_welfare = total_utility - total_cost_val

    # SOC: 25 points over hours 0..24
    # hour 0 = E_init (before any action), hours 1-24 = end-of-period SOC
    # For E_max == 0 (no storage), return None so the sensitivity plot skips it
    if E_max > 0:
        soc_pct = (
            [E_init / E_max * 100]
            + [e[t].X / E_max * 100 for t in T]
        )
    else:
        soc_pct = None

    soc_hours = list(range(0, 25))  # 0..24

    # ---------------------------------------------------------
    # BASE RUN PLOTTING
    # Two separate figures:
    #   step2_market_dispatch.png   — supply, demand, price
    #   step2_battery_dynamics.png  — charging, discharging, SOC
    # ---------------------------------------------------------

    if plot_results:

        hours = list(T)  # [1..24]

        plt.rcParams.update({
            "font.size":       18,
            "axes.titlesize":  18,
            "axes.labelsize":  16,
            "xtick.labelsize": 14,
            "ytick.labelsize": 14,
            "legend.fontsize": 14,
        })

        # --------------------------
        # FIGURE 1: Market Dispatch
        # --------------------------
        fig1, ax1 = plt.subplots(figsize=(12, 5))

        ax1.plot(hours, total_supply, color="tab:green", linewidth=2.5, label="Total Supply")
        ax1.plot(hours, total_demand, color="tab:red",   linewidth=2.5, label="Total Demand")
        ax1.set_ylabel("Power (MW)")
        ax1.set_xlabel("Hour")
        ax1.grid(True, alpha=0.3)

        ax_price = ax1.twinx()
        ax_price.grid(False)
        price_vals = list(prices.values())
        ax_price.plot(hours, price_vals, color="black", marker="o", linewidth=2, label="Market Price")
        ax_price.set_ylabel("Price (EUR/MWh)")
        price_min = min(price_vals)
        price_max = max(price_vals)
        margin = (price_max - price_min) * 0.1 if price_max != price_min else 1.0
        ax_price.set_ylim(price_min - margin, price_max + margin)

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax_price.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

        plt.tight_layout()
        plt.savefig("Results/step2_market_dispatch.png", dpi=300)
        plt.close()

        # --------------------------
        # FIGURE 2: Battery Dynamics
        # --------------------------
        fig2, ax2 = plt.subplots(figsize=(14, 6))

        bar_positions = [t - 1 for t in hours]  # [0..23]

        ax2.bar(bar_positions, charge,
                width=0.6, alpha=0.6, color="tab:blue", label="Charging (MW)")
        ax2.bar(bar_positions, [-d for d in discharge],
                width=0.6, alpha=0.7, color="tab:orange", label="Discharging (MW)")

        # Extend y-axis upward to create a clear band at the top for the legend
        ax2.set_ylim(-130, 160)
        ax2.set_ylabel("Charge / Discharge Power (MW)")
        ax2.set_xlabel("Hour")
        ax2.axhline(0, color="black", linewidth=1)
        ax2.grid(True, alpha=0.3)

        ax_soc = ax2.twinx()
        ax_soc.grid(False)

        ax_soc.plot(soc_hours, soc_pct,
                    color="black", linestyle="--", linewidth=2, marker="o",
                    label="State of Charge (%)")

        ax_soc.set_ylabel("State of Charge (%)")
        # Extend SOC axis to match: 0-100% maps into the lower part of the plot,
        # leaving the top band (above ~110%) clear for the legend
        ax_soc.set_ylim(-43, 133)
        ax_soc.set_yticks(np.arange(0, 110, 10))

        # Place legend in the upper centre — the extended top band is always empty
        lines1, labels1 = ax2.get_legend_handles_labels()
        lines2, labels2 = ax_soc.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2,
                   loc="upper center", ncol=3,
                   framealpha=0.9, edgecolor="grey")

        plt.tight_layout()
        plt.savefig("Results/step2_battery_dynamics.png", dpi=300)
        plt.close()

    return list(prices.values()), charge, discharge, soc_pct, soc_hours, social_welfare


# ---------------------------------------------------------
# BASE RUN
# ---------------------------------------------------------

run_market_model(100, 100, 400, plot_results=True, verbose=True)


# ---------------------------------------------------------
# SENSITIVITY ANALYSIS
#
# PLOT 1 (step2_sensitivity1.png):
#   Market price over hours — 4 lines
#   E = 0, 2333, 4667, 7000 MWh (equal steps 0->7000)
#   P scales proportionally at E/4 for each size
#
# PLOT 2 (step2_sensitivity2.png):
#   Delta Social Welfare vs storage capacity — 4 lines
#   X axis: E swept 0->7000 MWh (same equal steps)
#   Y axis: Delta SW = SW(E, P) - SW(0, 0)  [EUR]
#   Each line fixes P at a different constant value:
#   P = 0, 133, 267, 400 MW
# ---------------------------------------------------------

# --- PLOT 1: 4 sizes, equal steps from 0 to 7000 MWh, P = E/4 ---
top_sizes = [0, 2333, 4667, 7000]   # MWh

results_top = {}
for E in top_sizes:
    P = E / 4 if E > 0 else 0
    results_top[E] = run_market_model(P, P, E, plot_results=False, verbose=False)

# --- PLOT 2: sweep E from 0 to 7000, fix P at 4 different levels ---
bot_sizes    = [0, 2333, 4667, 7000]   # MWh — same x-axis points
fixed_powers = [0, 133, 267, 400]      # MW  — 4 constant P values

# SW baseline = no storage at all
sw_baseline = run_market_model(0, 0, 0, plot_results=False, verbose=False)[5]

results_bot = {}   # results_bot[P_fixed][E]
for P_fixed in fixed_powers:
    results_bot[P_fixed] = {}
    for E in bot_sizes:
        P = P_fixed if E > 0 else 0
        results_bot[P_fixed][E] = run_market_model(
            P, P, E, plot_results=False, verbose=False
        )

hours = list(T)  # [1..24]

# 4 clearly distinct colors used consistently across both plots
colors_4 = ["#000000",   # black  — no storage / P = 0 MW
             "#e41a1c",   # red    — medium-low
             "#377eb8",   # blue   — medium-high
             "#4daf4a"]   # green  — largest

# Font sizes — axis labels doubled relative to base run
LABEL_SIZE  = 28   # axis labels (doubled from 14)
TICK_SIZE   = 20   # tick labels
LEGEND_SIZE = 18   # legend
TITLE_SIZE  = 28   # titles if used

plt.rcParams.update({
    "font.size":        LEGEND_SIZE,
    "axes.titlesize":   TITLE_SIZE,
    "axes.labelsize":   LABEL_SIZE,
    "xtick.labelsize":  TICK_SIZE,
    "ytick.labelsize":  TICK_SIZE,
    "legend.fontsize":  LEGEND_SIZE,
})

# ---------------------------------------------------------
# SENSITIVITY PLOT 1 — Market Price vs Hour
# ---------------------------------------------------------

fig1, ax1 = plt.subplots(figsize=(12, 6))

for i, E in enumerate(top_sizes):
    price_vals = results_top[E][0]
    P_val = int(E / 4)
    label = f"E = {E} MWh, P = {P_val} MW" if E > 0 else "No storage (E = 0 MWh, P = 0 MW)"
    ax1.plot(hours, price_vals,
             color=colors_4[i], linewidth=2, alpha=0.75, label=label)

ax1.set_xlabel("Hour")
ax1.set_ylabel("Price (EUR/MWh)")
ax1.grid(True, alpha=0.3)
ax1.legend(loc="upper left")

plt.tight_layout()
plt.savefig("Results/step2_sensitivity1.png", dpi=300, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------
# SENSITIVITY PLOT 2 — Delta Social Welfare vs Storage Capacity
# ---------------------------------------------------------

fig2, ax2 = plt.subplots(figsize=(12, 6))

markers = ["o", "s", "^", "D"]

for i, P_fixed in enumerate(fixed_powers):
    delta_sw = [
        results_bot[P_fixed][E][5] - sw_baseline
        for E in bot_sizes
    ]
    label = f"P = {P_fixed} MW"
    ax2.plot(bot_sizes, delta_sw,
             color=colors_4[i], linewidth=2.5,
             marker=markers[i], markersize=8,
             alpha=0.85, label=label)

ax2.axhline(0, color="black", linewidth=1, linestyle="--")
ax2.set_xlabel("Storage Capacity (MWh)")
ax2.set_ylabel("Delta Social Welfare (EUR)")
ax2.set_xticks(bot_sizes)
ax2.grid(True, alpha=0.3)
ax2.legend(loc="upper left")

plt.tight_layout()
plt.savefig("Results/step2_sensitivity2.png", dpi=300, bbox_inches="tight")
plt.close()


# ---------------------------------------------------------
# TABLE: STORAGE SIZE SUMMARY (top sweep, P = E/4)
# ---------------------------------------------------------

summary_storage = []

for E in top_sizes:
    prices, charge, discharge, _, _, sw = results_top[E]
    summary_storage.append({
        "Storage Size (MWh)": E,
        "P_ch = P_dis (MW)": int(E / 4) if E > 0 else 0,
        "Avg Price (EUR/MWh)": np.mean(prices),
        "Price Std":           np.std(prices),
        "Max Price":           np.max(prices),
        "Min Price":           np.min(prices),
        "Price Spread":        np.max(prices) - np.min(prices),
        "Total Charge (MWh)":  sum(charge),
        "Total Discharge (MWh)": sum(discharge),
        "Social Welfare (EUR)":  round(sw, 2),
        "Delta SW vs baseline (EUR)": round(sw - sw_baseline, 2)
    })

df_storage = pd.DataFrame(summary_storage)
pd.set_option('display.max_columns', None)
print("\n=== STORAGE SIZE SENSITIVITY (P = E/4) ===")
print(df_storage.round(2))


# ---------------------------------------------------------
# PRICE COMPARISON: 0 MWh vs 400 MWh storage
# ---------------------------------------------------------

prices_no_storage  = run_market_model(0,   0,   0,   plot_results=False, verbose=False)[0]
prices_with_storage = run_market_model(100, 100, 400, plot_results=False, verbose=False)[0]

plt.rcParams.update({
    "font.size":        18,
    "axes.titlesize":   18,
    "axes.labelsize":   18,
    "xtick.labelsize":  14,
    "ytick.labelsize":  14,
    "legend.fontsize":  16,
})

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(hours, prices_no_storage,
        color="#e41a1c", linewidth=2.5, marker="o", markersize=5,
        label="No storage (E = 0 MWh)")
ax.plot(hours, prices_with_storage,
        color="#377eb8", linewidth=2.5, marker="o", markersize=5,
        label="With storage (E = 400 MWh, P = 100 MW)")

ax.set_xlabel("Hour")
ax.set_ylabel("Market Price (EUR/MWh)")
ax.grid(True, alpha=0.3)
ax.legend(loc="upper left")

plt.tight_layout()
plt.savefig("Results/step2_price_comparison.png", dpi=300, bbox_inches="tight")
plt.close()