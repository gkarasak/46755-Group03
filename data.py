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


Prices_for_loads ={ # this is the nordpool prices randomized for each load by multiplying by 0.7 and 1.2 for each hour in EUR/MWh. 
  1: [87.73, 61.30, 72.05, 69.82, 91.90, 89.33, 98.60, 63.96, 78.37, 61.50, 69.63, 81.96, 61.36, 68.77, 88.18, 83.66, 69.70],
  2: [84.54, 93.90, 59.78, 93.75, 89.17, 73.96, 66.11, 100.18, 73.81, 63.44, 63.61, 95.52, 85.16, 93.80, 90.51, 82.29, 100.86],
  3: [76.71, 84.19, 96.15, 87.06, 97.55, 85.28, 90.77, 62.36, 70.21, 72.86, 63.82, 70.42, 64.74, 72.37, 87.80, 76.12, 76.35],
  4: [69.61, 72.10, 101.06, 88.58, 86.89, 67.95, 92.08, 67.62, 76.96, 103.35, 88.23, 84.64, 90.16, 97.00, 94.11, 70.46, 61.94],
  5: [75.67, 73.56, 71.06, 103.35, 100.41, 75.63, 90.67, 79.21, 102.09, 81.99, 73.44, 72.63, 86.52, 73.34, 87.54, 101.36, 79.37],
  6: [76.25, 112.90, 89.92, 70.21, 68.14, 71.09, 95.47, 103.23, 85.81, 68.92, 83.90, 112.83, 90.84, 111.65, 106.46, 66.47, 99.86],
  7: [116.26, 108.18, 93.09, 113.99, 84.42, 102.47, 103.53, 131.46, 127.11, 92.90, 106.15, 88.17, 129.16, 126.81, 94.86, 113.88, 112.20],
  8: [103.54, 144.19, 129.31, 145.26, 128.71, 93.38, 114.96, 94.64, 155.29, 151.93, 148.80, 113.85, 97.21, 151.89, 156.48, 99.06, 125.75],
  9: [108.42, 159.44, 159.83, 112.79, 138.39, 143.89, 122.87, 167.69, 134.54, 118.94, 143.11, 157.18, 118.16, 126.32, 176.75, 151.27, 135.64],
  10: [135.13, 107.19, 114.49, 122.48, 140.12, 114.87, 114.18, 103.66, 143.13, 114.79, 162.46, 159.24, 103.65, 115.43, 145.80, 113.76, 107.98],
  11: [150.54, 127.04, 120.70, 140.81, 142.28, 102.51, 96.48, 118.02, 117.54, 120.34, 137.23, 133.64, 153.67, 96.58, 116.19, 112.11, 145.78],
  12: [92.01, 88.75, 103.17, 101.68, 93.68, 92.08, 129.66, 102.87, 126.21, 108.85, 80.96, 133.90, 124.79, 132.21, 129.83, 125.50, 87.42],
  13: [96.53, 82.61, 92.20, 74.67, 91.07, 122.10, 85.24, 111.80, 94.96, 93.32, 120.67, 122.62, 100.12, 108.44, 79.59, 86.85, 121.25],
  14: [100.17, 98.29, 108.71, 73.75, 100.42, 96.30, 114.01, 78.82, 119.48, 74.91, 80.26, 100.97, 105.03, 82.76, 76.92, 115.91, 83.31],
  15: [99.79, 101.03, 91.02, 99.24, 96.20, 116.81, 80.26, 105.87, 81.98, 89.84, 103.65, 85.05, 85.86, 107.66, 73.67, 92.97, 119.99],
  16: [131.23, 80.69, 88.35, 91.20, 127.79, 124.92, 124.84, 96.92, 85.32, 122.34, 115.21, 110.18, 130.75, 112.50, 77.11, 121.43, 93.07],
  17: [130.01, 147.38, 96.68, 95.49, 94.96, 123.07, 105.37, 126.32, 133.43, 101.04, 128.18, 104.85, 119.00, 145.26, 141.53, 94.03, 114.90],
  18: [153.25, 128.28, 198.44, 186.19, 151.90, 195.71, 178.38, 167.05, 128.84, 134.84, 208.68, 210.58, 177.83, 204.24, 181.20, 141.50, 139.61],
  19: [157.22, 211.59, 202.12, 208.06, 211.58, 148.18, 151.81, 138.31, 200.65, 210.22, 166.25, 185.97, 143.07, 214.43, 208.42, 218.69, 203.47],
  20: [166.33, 103.87, 155.77, 126.28, 169.93, 160.55, 165.06, 161.17, 121.52, 159.47, 109.95, 165.65, 164.66, 118.28, 161.60, 135.63, 124.32],
  21: [130.63, 96.85, 84.72, 94.80, 102.84, 134.74, 140.84, 99.92, 121.48, 107.09, 141.69, 115.21, 139.20, 90.17, 141.05, 93.93, 140.58],
  22: [90.54, 82.00, 99.74, 115.72, 93.16, 109.07, 103.91, 97.05, 107.46, 89.96, 114.64, 76.20, 126.43, 105.38, 115.22, 116.45, 112.57],
  23: [89.72, 74.76, 104.98, 87.99, 87.16, 114.32, 107.80, 86.47, 86.93, 91.97, 91.66, 86.23, 77.67, 92.58, 119.02, 105.64, 117.11],
  24: [94.63, 79.86, 91.46, 65.75, 79.20, 85.91, 92.96, 96.47, 87.56, 86.49, 75.76, 87.95, 108.04, 103.10, 73.70, 69.71, 89.93],
}