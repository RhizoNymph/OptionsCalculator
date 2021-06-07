import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
from math import exp

def get_payoff(spot_expiry, option):
    sign = option[0]
    if option[2] in ['C', 'P', 'U', 'L', 'B']:
        magnitude = int(option[1])
        type = option[2]
        if type != 'U':
            strike = float(option[3:])
    else:
        magnitude = int(option[1:3])
        type = option[3]
        if type != 'U':
            strike = float(option[4:])

    if type == 'C':
        if strike <= spot_expiry:
            if sign == '+':
                return magnitude * (spot_expiry - strike)
            else:
                return -magnitude * (spot_expiry - strike)
        else:
            return 0
    elif type == 'P':
        if strike >= spot_expiry:
            if sign == '+':
                return magnitude * (strike - spot_expiry)
            else:
                return -magnitude * (strike - spot_expiry)
        else:
            return 0
    elif type == 'U':
        if sign == '+':
            return magnitude * spot_expiry
        else:
            return -magnitude * spot_expiry

def plot_options(options, premiums, expiry_range):
    dict = {'expiry_price': []}
    for option in options:
        dict[option] = []
    for p in expiry_range:
        dict['expiry_price'].append(p)
        for option in options:
            dict[option].append(get_payoff(p, option))

    df = pd.DataFrame(dict).set_index('expiry_price')
    df['payoff'] = df.sum(axis=1)
    df['profit'] = df['payoff'] - premiums.sum()

    fig, ax = plot.subplots(2)
    df.drop(['payoff', 'profit'], axis=1).plot(ax=ax[0], grid='major')
    df[['payoff', 'profit']].plot(ax=ax[1], grid='major')
    plot.show()

def test_parity_eu(rfr, spot, strike, ttm, call_premium, put_premium):
    left = call_premium + strike * exp(-rfr * ttm)
    right = put_premium + spot

    return left == right

def test_parity_us(rfr, spot, strike, ttm, call_premium, put_premium):
    left = spot - strike
    spread = call_premium - put_premium
    right = spot - strike * exp(-rfr * ttm)

    if left > spread:
        return -1
    elif right < spread:
        return 1
    else:
        return 0

def test_range_eu(rfr, spot, strike, ttm, premium, type):
    if type == 'C':
        lower_bound = max(0, spot - strike * exp(-rfr * ttm))
    elif type == 'P':
        lower_bound = max(0, strike * exp(-rfr * ttm) - spot)

    if type == 'C':
        upper_bound = spot
    elif type == 'P':
        upper_bound = strike * exp(-rfr * ttm)

    if premium < lower_bound:
        return -1
    elif premium > upper_bound:
        return 1
    else:
        return 0

def test_range_us(rfr, spot, strike, ttm, premium, type):
    if type == 'C':
        lower_bound = max(0, spot - strike * exp(-rfr * ttm))
    elif type =='P':
        lower_bound = max(0, strike - spot)

    if type == 'C':
        upper_bound = spot
    elif type =='P':
        upper_bound = strike

    if premium < lower_bound:
        return -1
    elif premium > upper_bound:
        return 1
    else:
        return 0

expiry_range = np.arange(0, 150, 5)
options = ['+1C35', '-1P100', '-1U']
premiums = np.array([-6.48, 2.53, 22])

plot_options(options, premiums, expiry_range)