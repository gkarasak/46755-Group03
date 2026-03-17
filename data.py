generators = {
    'G1':  {'node': 1,  'Pmax_MW': 152, 'Pmin_MW': 0},
    'G2':  {'node': 2,  'Pmax_MW': 152, 'Pmin_MW': 0},
    'G3':  {'node': 7,  'Pmax_MW': 350, 'Pmin_MW': 0},
    'G4':  {'node': 13, 'Pmax_MW': 591, 'Pmin_MW': 0},
    'G5':  {'node': 15, 'Pmax_MW': 60,  'Pmin_MW': 0},
    'G6':  {'node': 15, 'Pmax_MW': 155, 'Pmin_MW': 0},
    'G7':  {'node': 16, 'Pmax_MW': 155, 'Pmin_MW': 0},
    'G8':  {'node': 18, 'Pmax_MW': 400, 'Pmin_MW': 0},
    'G9':  {'node': 21, 'Pmax_MW': 400, 'Pmin_MW': 0},
    'G10': {'node': 22, 'Pmax_MW': 300, 'Pmin_MW': 0},
    'G11': {'node': 23, 'Pmax_MW': 310, 'Pmin_MW': 0},
    'G12': {'node': 23, 'Pmax_MW': 350, 'Pmin_MW': 0},
    # Wind farms (bid price = 0, capacity varies with forecast)
    'W1':  {'node': 3,  'Pmax_MW': 200, 'Pmin_MW': 0},
    'W2':  {'node': 5,  'Pmax_MW': 200, 'Pmin_MW': 0},
    'W3':  {'node': 7,  'Pmax_MW': 200, 'Pmin_MW': 0},
    'W4':  {'node': 16, 'Pmax_MW': 200, 'Pmin_MW': 0},
    'W5':  {'node': 21, 'Pmax_MW': 200, 'Pmin_MW': 0},
    'W6':  {'node': 23, 'Pmax_MW': 200, 'Pmin_MW': 0},
}

Zonal_networks = {
    'Z1': {'nodes': [18,21,23,22,20,19,16,17,15,24]},
    'Z2': {'nodes': [3,4,9,5,2,1]},
    'Z3': {'nodes': [14,11,12,13,10,6,8,7]},
    }


load_profile = { #this is in per hour, in MW
    1:  1775.835,
    2:  1669.815,
    3:  1590.3,
    4:  1563.795,
    5:  1563.795,
    6:  1590.3,
    7:  1961.37,
    8:  2279.43,
    9:  2517.975,
    10: 2544.48,
    11: 2544.48,
    12: 2517.975,
    13: 2517.975,
    14: 2517.975,
    15: 2464.965,
    16: 2464.965,
    17: 2623.995,
    18: 2650.5,
    19: 2650.5,
    20: 2544.48,
    21: 2411.955,
    22: 2199.915,
    23: 1934.865,
    24: 1669.815,
}

load_distribution = {
    'Load1':  {'node': 1,  'percent': 3.8},
    'Load2':  {'node': 2,  'percent': 3.4},
    'Load3':  {'node': 3,  'percent': 6.3},
    'Load4':  {'node': 4,  'percent': 2.6},
    'Load5':  {'node': 5,  'percent': 2.5},
    'Load6':  {'node': 6,  'percent': 4.8},
    'Load7':  {'node': 7,  'percent': 4.4},
    'Load8':  {'node': 8,  'percent': 6.0},
    'Load9':  {'node': 9,  'percent': 6.1},
    'Load10': {'node': 10, 'percent': 6.8},
    'Load11': {'node': 13, 'percent': 9.3},
    'Load12': {'node': 14, 'percent': 6.8},
    'Load13': {'node': 15, 'percent': 11.1},
    'Load14': {'node': 16, 'percent': 3.5},
    'Load15': {'node': 18, 'percent': 11.7},
    'Load16': {'node': 19, 'percent': 6.4},
    'Load17': {'node': 20, 'percent': 4.5},
}

transmission_lines = { #some lines have their capacity modified to reflect the renewable scenario
    'L1':  {'from': 1,  'to': 2,  'reactance': 0.0146, 'capacity_MVA': 175},
    'L2':  {'from': 1,  'to': 3,  'reactance': 0.2253, 'capacity_MVA': 175},
    'L3':  {'from': 1,  'to': 5,  'reactance': 0.0907, 'capacity_MVA': 350},
    'L4':  {'from': 2,  'to': 4,  'reactance': 0.1356, 'capacity_MVA': 175},
    'L5':  {'from': 2,  'to': 6,  'reactance': 0.205,  'capacity_MVA': 175},
    'L6':  {'from': 3,  'to': 9,  'reactance': 0.1271, 'capacity_MVA': 175},
    'L7':  {'from': 3,  'to': 24, 'reactance': 0.084,  'capacity_MVA': 400},
    'L8':  {'from': 4,  'to': 9,  'reactance': 0.111,  'capacity_MVA': 175},
    'L9':  {'from': 5,  'to': 10, 'reactance': 0.094,  'capacity_MVA': 350},
    'L10': {'from': 6,  'to': 10, 'reactance': 0.0642, 'capacity_MVA': 175},
    'L11': {'from': 7,  'to': 8,  'reactance': 0.0652, 'capacity_MVA': 350},
    'L12': {'from': 8,  'to': 9,  'reactance': 0.1762, 'capacity_MVA': 175},
    'L13': {'from': 8,  'to': 10, 'reactance': 0.1762, 'capacity_MVA': 175},
    'L14': {'from': 9,  'to': 11, 'reactance': 0.084,  'capacity_MVA': 400},
    'L15': {'from': 9,  'to': 12, 'reactance': 0.084,  'capacity_MVA': 400},
    'L16': {'from': 10, 'to': 11, 'reactance': 0.084,  'capacity_MVA': 400},
    'L17': {'from': 10, 'to': 12, 'reactance': 0.084,  'capacity_MVA': 400},
    'L18': {'from': 11, 'to': 13, 'reactance': 0.0488, 'capacity_MVA': 500},
    'L19': {'from': 11, 'to': 14, 'reactance': 0.0426, 'capacity_MVA': 500},
    'L20': {'from': 12, 'to': 13, 'reactance': 0.0488, 'capacity_MVA': 500},
    'L21': {'from': 12, 'to': 23, 'reactance': 0.0985, 'capacity_MVA': 500},
    'L22': {'from': 13, 'to': 23, 'reactance': 0.0884, 'capacity_MVA': 250}, # 250 #renewable scenario
    'L23': {'from': 14, 'to': 16, 'reactance': 0.0594, 'capacity_MVA': 250}, #renewable scenario
    'L24': {'from': 15, 'to': 16, 'reactance': 0.0172, 'capacity_MVA': 500},
    'L25': {'from': 15, 'to': 21, 'reactance': 0.0249, 'capacity_MVA': 400}, #renewable scenario
    'L26': {'from': 15, 'to': 24, 'reactance': 0.0529, 'capacity_MVA': 500},
    'L27': {'from': 16, 'to': 17, 'reactance': 0.0263, 'capacity_MVA': 500},
    'L28': {'from': 16, 'to': 19, 'reactance': 0.0234, 'capacity_MVA': 500},
    'L29': {'from': 17, 'to': 18, 'reactance': 0.0143, 'capacity_MVA': 500},
    'L30': {'from': 17, 'to': 22, 'reactance': 0.1069, 'capacity_MVA': 500},
    'L31': {'from': 18, 'to': 21, 'reactance': 0.0132, 'capacity_MVA': 1000}, #1000 original
    'L32': {'from': 19, 'to': 20, 'reactance': 0.0203, 'capacity_MVA': 1000}, 
    'L33': {'from': 20, 'to': 23, 'reactance': 0.0112, 'capacity_MVA': 1000}, 
    'L34': {'from': 21, 'to': 22, 'reactance': 0.0692, 'capacity_MVA': 500},
}



# Bid prices ($/MWh) - can be updated per hour
# Generators: set to marginal cost (renewables = 0)
# Loads: set high to ensure most demand is served
# G3, G4, G5, G9, G11, G13 are renewables (marginal cost = 0)

#multiplied the input data from the main source by 0.87 as per 13/03/2026 to change to eur/MWh

generator_bid_prices = {
    'G1':  {h: 11.59 for h in range(1, 25)},  # conventional
    'G2':  {h: 11.59 for h in range(1, 25)},  # conventional
    'G3':  {h: 18.01 for h in range(1, 25)},  # conventional
    'G4':  {h: 18.21 for h in range(1, 25)},  # conventional
    'G5':  {h: 22.72 for h in range(1, 25)},  # conventional
    'G6':  {h: 9.15  for h in range(1, 25)},  # conventional
    'G7':  {h: 9.15  for h in range(1, 25)},  # conventional
    'G8':  {h: 5.24  for h in range(1, 25)},  # conventional
    'G9':  {h: 4.76  for h in range(1, 25)},  # conventional
    'G10': {h: 0     for h in range(1, 25)},  # conventional
    'G11': {h: 9.15  for h in range(1, 25)},  # conventional
    'G12': {h: 9.47  for h in range(1, 25)},  # conventional
    'W1':  {h: 0     for h in range(1, 25)},  # renewable
    'W2':  {h: 0     for h in range(1, 25)},  # renewable
    'W3':  {h: 0     for h in range(1, 25)},  # renewable
    'W4':  {h: 0     for h in range(1, 25)},  # renewable
    'W5':  {h: 0     for h in range(1, 25)},  # renewable
    'W6':  {h: 0     for h in range(1, 25)},  # renewable
}

price_profile = { # this is in per hour, in EUR/MWh, taken from Nordpool for 23-03-2025
1: 3.99,
2: 5.06,
3: 3.97,
4: 5.00,
5: 6.58,
6: 7.54,
7: 4.68,
8: 3.97,
9: 3.91,
10: 2.30,
11: 2.26,
12: 0.36,
13: 0.45,
14: 0.02,
15: 1.99,
16: 3.06,
17: 13.06,
18: 32.68,
19: 33.11,
20: 38.95,
21: 33.17,
22: 33.00,
23: 32.83,
24: 32.63,
}


Prices_for_loads = {
  1: [3.58, 2.81, 3.97, 4.37, 4.52, 3.98, 4.43, 4.02, 3.12, 4.66, 3.85, 3.00, 3.67, 3.02, 3.00, 4.55, 4.50],
  2: [4.48, 5.57, 4.48, 4.46, 3.82, 3.63, 5.22, 4.41, 4.46, 5.49, 4.74, 5.70, 4.65, 5.94, 4.78, 5.67, 4.30],
  3: [3.87, 3.36, 4.27, 3.79, 4.23, 3.90, 3.76, 3.49, 3.08, 3.41, 4.49, 3.16, 2.85, 3.81, 3.19, 4.73, 4.41],
  4: [5.34, 4.48, 3.79, 4.58, 4.58, 4.53, 5.96, 4.26, 5.09, 4.71, 3.52, 3.88, 4.94, 4.33, 4.95, 4.03, 3.82],
  5: [6.88, 7.55, 4.63, 4.81, 6.63, 7.59, 6.15, 5.12, 7.45, 5.04, 6.97, 6.75, 7.40, 5.38, 5.17, 6.85, 7.40],
  6: [8.20, 7.60, 7.66, 6.30, 8.64, 6.68, 6.49, 7.16, 8.74, 8.69, 7.47, 7.80, 7.69, 8.85, 7.10, 5.69, 8.93],
  7: [4.78, 4.07, 4.60, 3.38, 4.32, 3.78, 3.52, 4.28, 4.39, 5.04, 3.33, 4.79, 3.73, 4.70, 4.94, 3.97, 4.10],
  8: [3.21, 3.80, 4.34, 4.56, 3.06, 4.12, 3.54, 4.71, 3.30, 3.08, 4.58, 3.35, 4.32, 3.78, 3.96, 4.05, 3.25],
  9: [3.24, 4.56, 3.67, 4.00, 3.90, 3.48, 2.91, 3.92, 4.67, 3.73, 3.66, 4.46, 3.15, 4.13, 2.89, 3.38, 3.20],
  10: [2.04, 2.40, 1.80, 2.48, 2.26, 1.72, 1.69, 1.97, 2.50, 2.68, 2.32, 2.50, 2.04, 1.95, 2.18, 2.31, 2.33],
  11: [1.72, 1.67, 2.24, 1.85, 2.59, 1.74, 2.34, 2.53, 2.03, 2.18, 2.07, 2.62, 2.25, 2.11, 2.37, 2.17, 2.59],
  12: [0.31, 0.42, 0.40, 0.37, 0.32, 0.29, 0.38, 0.42, 0.31, 0.37, 0.39, 0.39, 0.27, 0.28, 0.29, 0.35, 0.35],
  13: [0.41, 0.40, 0.45, 0.35, 0.39, 0.47, 0.42, 0.35, 0.40, 0.33, 0.40, 0.35, 0.43, 0.53, 0.41, 0.43, 0.36],
  14: [0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.01, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02],
  15: [1.54, 2.32, 1.53, 2.16, 2.09, 1.83, 2.22, 1.91, 1.55, 1.52, 2.20, 2.28, 1.74, 1.97, 2.09, 1.44, 1.78],
  16: [2.93, 2.49, 3.63, 3.38, 2.40, 2.80, 2.20, 2.48, 2.70, 2.35, 2.59, 3.43, 3.06, 3.62, 2.89, 3.65, 3.31],
  17: [12.85, 15.47, 12.95, 12.79, 15.03, 11.34, 15.43, 14.13, 10.84, 12.77, 10.21, 11.03, 11.21, 11.85, 13.86, 13.39, 12.64],
  18: [38.87, 35.74, 25.86, 32.69, 32.47, 29.47, 32.13, 29.72, 32.86, 35.11, 39.22, 36.18, 26.24, 30.00, 31.83, 38.98, 23.44],
  19: [28.34, 28.38, 36.15, 24.94, 33.32, 35.37, 33.71, 36.71, 30.91, 39.13, 25.24, 37.08, 34.08, 34.78, 38.07, 36.97, 25.21],
  20: [44.35, 33.03, 41.73, 33.87, 36.73, 43.40, 46.44, 42.10, 30.29, 33.19, 45.39, 39.95, 32.76, 31.24, 30.64, 36.14, 30.40],
  21: [30.28, 34.02, 24.50, 26.56, 34.70, 32.96, 26.79, 25.59, 36.14, 29.40, 26.37, 28.17, 29.06, 31.80, 27.17, 29.53, 34.39],
  22: [29.37, 32.08, 31.55, 32.51, 26.73, 26.14, 33.32, 35.65, 32.88, 23.40, 26.77, 27.90, 25.50, 37.88, 24.66, 29.64, 29.57],
  23: [37.71, 27.64, 36.88, 33.73, 24.13, 26.56, 33.86, 38.73, 34.99, 27.20, 31.99, 36.06, 35.23, 25.52, 26.01, 24.03, 39.14],
  24: [29.48, 24.85, 30.72, 23.87, 32.19, 23.21, 32.13, 35.00, 37.43, 25.48, 26.42, 25.07, 32.57, 37.28, 25.75, 37.69, 22.97],
}

