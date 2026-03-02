#Import relevant libraries
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

#24 hours
T = range(1,25) 

#--------------------------------------------------------------------------------------------------------------
### import wind CF data for 6 windfarms and cut to be 24 hours and average out

# Define base directory (where 46755-Group03 is located)
BASE_DIR = r'C:\Users\20221122\Downloads\DTU\SEMESTER 2\Renewables in electricity markets\46755-Group03'

# Define data folder
DATA_DIR = os.path.join(BASE_DIR, 'data_from_Jakob')

# Read all zone files safely
W1_data = pd.read_csv(os.path.join(DATA_DIR, 'scen_zone1.csv'))
W1_CF = W1_data.iloc[1:25, 1:].mean(axis=1)

W2_data = pd.read_csv(os.path.join(DATA_DIR, 'scen_zone2.csv'))
W2_CF = W2_data.iloc[1:25, 1:].mean(axis=1)

W3_data = pd.read_csv(os.path.join(DATA_DIR, 'scen_zone3.csv'))
W3_CF = W3_data.iloc[1:25, 1:].mean(axis=1)

W4_data = pd.read_csv(os.path.join(DATA_DIR, 'scen_zone4.csv'))
W4_CF = W4_data.iloc[1:25, 1:].mean(axis=1)

W5_data = pd.read_csv(os.path.join(DATA_DIR, 'scen_zone5.csv'))
W5_CF = W5_data.iloc[1:25, 1:].mean(axis=1)

W6_data = pd.read_csv(os.path.join(DATA_DIR, 'scen_zone6.csv'))
W6_CF = W6_data.iloc[1:25, 1:].mean(axis=1)

#Create model
model = gp.Model("Copperplate_singlehour")

#--------------------------------------------------------------------------------------------------------------
#Add storage unit
# Storage parameters
P_ch = 300
P_dis = 300
E_max = 1000

eta_ch = 0.9
eta_dis = 0.95

# Storage variables
p_ch = {t: model.addVar(lb=0, ub=P_ch, name=f"p_ch_{t}") for t in T}
p_dis = {t: model.addVar(lb=0, ub=P_dis, name=f"p_dis_{t}") for t in T}
e = {t: model.addVar(lb=0, ub=E_max, name=f"e_{t}") for t in T}

#--------------------------------------------------------------------------------------------------------------
# create variable list with the names of the variables as strings

from data import load_distribution, load_profile, generators, generator_bid_prices
from data import Prices_for_loads


VARIABLES = list(generators.keys())

LOAD_VARIABLES = list(load_distribution.keys())


#create a list of the cost coefficients for each variable
Generation_price = [v[1] for v in generator_bid_prices.values()]

#writes a list that converts the cost coefficient to this form objective_coeff = {'G1': 13.32, 'G2': 13.32, ...}
objective_coeff = {VARIABLES[i]: Generation_price[i] for i in range(len(VARIABLES))}


#write the load percentages for each node
Load_percentage = [v['percent'] for v in load_distribution.values()]
#multiply the load percentage with the total load to get the actual load in MW

Load_t = {t: load_profile[t] for t in T}

Load_node_t = {
   t: [Load_t[t] * (i / 100) for i in Load_percentage]
    for t in T
}


#demand bids are higher during peak hours: time-dependent 

Load_coefficients = {}

for t in T:
    prices_t = np.array(sorted(Prices_for_loads[t], reverse=True)) 
    for i, l in enumerate(LOAD_VARIABLES):
        Load_coefficients[(l,t)] = prices_t[i]

#create a upper bound for the production variables
Generator_UB = {
    k: v['Pmax_MW']
    for k, v in generators.items()
    if k.startswith('G')
}

#Generator_UB = [152,152,350,591,60,155,155,400,400,300,310,350] #MW
Wind_CF = [W1_CF, W2_CF, W3_CF, W4_CF, W5_CF, W6_CF]

Wind_UB_t = {
    t: np.array([Wind_CF[i].iloc[t-1] for i in range(6)]) * 200
    for t in T
}


#create constraints sense list with 18 values of GRB.LESS_EQUAL
constraints_sense = [GRB.LESS_EQUAL] * 18


#--------------------------------------------------------------------------------------------------------------


#Add variables
variables = {
    (v, t): model.addVar(lb=0, name=f"{v}_{t}")
    for v in VARIABLES
    for t in T
}

#Add load variables
#load_variables = {l: model.addVar(lb=0, name=f'variable {l}') for l in LOAD_VARIABLES}

load_variables = {
    (l,t): model.addVar(
        lb=0,
        ub=Load_node_t[t][i],
        name=f"{l}_{t}"
    )
    for i, l in enumerate(LOAD_VARIABLES)
    for t in T
}

#--------------------------------------------------------------------------------------------------------------
# Set objective function and optimization direction of the Gurobi model

objective = gp.quicksum(
    Load_coefficients[(l,t)] * load_variables[(l,t)]
    for l in LOAD_VARIABLES for t in T
) - gp.quicksum(
    objective_coeff[v] * variables[(v,t)]
    for v in VARIABLES for t in T
)

model.setObjective(objective, GRB.MAXIMIZE)


#--------------------------------------------------------------------------------------------------------------
# Add constraints to the Gurobi model


#Upper bound for conventional generators (same every hour)

for v in VARIABLES:
    for t in T:
        if v in Generator_UB:
            model.addConstr(
                variables[(v, t)] <= Generator_UB[v],
                name=f"UB_{v}_{t}"
            )

# Wind hourly upper bounds (assuming last 6 generators are wind)

for t in T:
    for i in range(6):
        wind_var = VARIABLES[-6 + i]
        model.addConstr(
            variables[(wind_var, t)] <= Wind_UB_t[t][i],
            name=f"Wind_UB_{wind_var}_{t}"
        )



#Balance 
balance = {}
for t in T:
    balance[t] = model.addConstr(
        gp.quicksum(variables[(v, t)] for v in VARIABLES)
        + p_dis[t] - p_ch[t]
        == gp.quicksum(load_variables[(l, t)] for l in LOAD_VARIABLES),
        name=f"balance_{t}"
    )

#Storage energy constraints
for t in T:
    if t == 1:
        model.addConstr(
            e[t] == 0 + p_ch[t]*eta_ch - p_dis[t]/eta_dis,
            name=f"storage_balance_{t}"
        )
    else:
        model.addConstr(
            e[t] == e[t-1] + p_ch[t]*eta_ch - p_dis[t]/eta_dis,
            name=f"storage_balance_{t}"
        )

# End-of-day condition
model.addConstr(e[24] == 0, name="terminal_energy")

#--------------------------------------------------------------------------------------------------------------
model.optimize()


#-------CALCULATE OUTCOMES------------------------------------------------------------------------------------------

#Market-clearing prices (one per hour) under a uniform pricing scheme
prices = {t: -balance[t].Pi for t in T}

#Total operating cost over 24 hours
total_cost = sum(
    objective_coeff[v] * variables[(v,t)].X
    for v in VARIABLES for t in T
)

#Total social welfare over 24 hours
total_welfare = model.ObjVal

#Total profit of each producer over 24 hours 
generator_profit = {}

for v in VARIABLES:
    profit = sum(
        prices[t] * variables[(v,t)].X
        - objective_coeff[v] * variables[(v,t)].X
        for t in T
    )
    generator_profit[v] = profit

#Total profit of the storage unit over 24 hours 
storage_profit = sum(
    prices[t] * p_dis[t].X
    - prices[t] * p_ch[t].X
    for t in T
)


#-------PRINT OUTCOMES------------------------------------------------------------------------------------------
print("\n================ STEP 2 RESULTS ================\n")

# Market-clearing prices
print("Market-clearing prices (€/MWh):")
for t in T:
    print(f"Hour {t:2d}: {prices[t]:.2f}")

# Total operating cost
print("\nTotal operating cost over 24 hours:")
print(f"{total_cost:,.2f} €")

# Total social welfare
print("\nTotal social welfare over 24 hours:")
print(f"{total_welfare:,.2f} €")

# Generator profits
print("\nTotal profit of each producer over 24 hours:")
for v, profit in generator_profit.items():
    print(f"{v}: {profit:,.2f} €")

# Storage profit
print("\nTotal profit of the storage unit over 24 hours:")
print(f"{storage_profit:,.2f} €")

print("\n================================================\n")