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
    'L22': {'from': 13, 'to': 23, 'reactance': 0.0884, 'capacity_MVA': 250}, #renewable scenario
    'L23': {'from': 14, 'to': 16, 'reactance': 0.0594, 'capacity_MVA': 250}, #renewable scenario
    'L24': {'from': 15, 'to': 16, 'reactance': 0.0172, 'capacity_MVA': 500},
    'L25': {'from': 15, 'to': 21, 'reactance': 0.0249, 'capacity_MVA': 400}, #renewable scenario
    'L26': {'from': 15, 'to': 24, 'reactance': 0.0529, 'capacity_MVA': 500},
    'L27': {'from': 16, 'to': 17, 'reactance': 0.0263, 'capacity_MVA': 500},
    'L28': {'from': 16, 'to': 19, 'reactance': 0.0234, 'capacity_MVA': 500},
    'L29': {'from': 17, 'to': 18, 'reactance': 0.0143, 'capacity_MVA': 500},
    'L30': {'from': 17, 'to': 22, 'reactance': 0.1069, 'capacity_MVA': 500},
    'L31': {'from': 18, 'to': 21, 'reactance': 0.0132, 'capacity_MVA': 1000},
    'L32': {'from': 19, 'to': 20, 'reactance': 0.0203, 'capacity_MVA': 1000},
    'L33': {'from': 20, 'to': 23, 'reactance': 0.0112, 'capacity_MVA': 1000},
    'L34': {'from': 21, 'to': 22, 'reactance': 0.0692, 'capacity_MVA': 500},
}


# Bid prices ($/MWh) - can be updated per hour
# Generators: set to marginal cost (renewables = 0)
# Loads: set high to ensure most demand is served
# G3, G4, G5, G9, G11, G13 are renewables (marginal cost = 0)

generator_bid_prices = {
    'G1':  {h: 13.32 for h in range(1, 25)},  # conventional
    'G2':  {h: 13.32 for h in range(1, 25)},  # conventional
    'G3':  {h: 20.7  for h in range(1, 25)},  # conventional
    'G4':  {h: 20.93  for h in range(1, 25)},  # conventional
    'G5':  {h: 26.11  for h in range(1, 25)},  # conventional
    'G6':  {h: 10.52 for h in range(1, 25)},  # conventional
    'G7':  {h: 10.52 for h in range(1, 25)},  # conventional
    'G8':  {h: 6.02 for h in range(1, 25)},  # conventional
    'G9':  {h: 5.47  for h in range(1, 25)},  # conventional
    'G10': {h: 0 for h in range(1, 25)},  # conventional
    'G11': {h: 10.52  for h in range(1, 25)},  # conventional
    'G12': {h: 10.89 for h in range(1, 25)},  # conventional
    'W1': {h: 0  for h in range(1, 25)},  # renewable
    'W2': {h: 0  for h in range(1, 25)},  # renewable
    'W3': {h: 0  for h in range(1, 25)},  # renewable
    'W4': {h: 0  for h in range(1, 25)},  # renewable
    'W5': {h: 0  for h in range(1, 25)},  # renewable
    'W6': {h: 0  for h in range(1, 25)},  # renewable
}

price_profile = { #this is in per hour, in EUR/MWh, taken from Nordpool for 24-02-2026 and averaged per hour
 1:	86.03,
2:	85.00,
3:	86.26,
4:	86.50,
5:	88.22,
6:	94.18,
7:	111.70,
8:	133.35,
9:	147.59,
10:	140.94,
11:	128.91,
12:	111.62,
13:	102.38,
14:	101.22,
15:	100.06,
16:	109.54,
17:	126.02,
18:	182.80,
19:	184.07,
20:	145.81,
21:	119.01,
22:	108.73,
23:	101.71,
24:	93.90,
}