from multiprocessing import Pool
import dask
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Position:
    def __init__(self, asset, sign, magnitude, premium):
        self.asset = asset
        self.sign = sign
        self.magnitude = magnitude
        self.premium = premium

    def profit(self, spot_expiry):
        return self.sign * self.magnitude * (self.asset.payoff(spot_expiry) - self.premium)

    def payoff(self, spot_expiry):
        return self.sign * self.magnitude * self.asset.payoff(spot_expiry)

def position_payoff(position, spot_expiry):
    return position.payoff(spot_expiry)

def position_premium(position):
    return position.premium

class PositionAggregator:
    def __init__(self, position_list):
        self.positions = position_list
        self.premium = 0
        self.update_position_premium_agg()

    def add_position(self, position):
        self.positions.append(position)
        self.update_position_premium_agg()

    def position_payoff_agg(self, spot_expiry):
        payoffs = []
        for pos in self.positions:
            payoffs.append(dask.delayed(position_payoff)(pos, spot_expiry))
        return np.sum(dask.compute(payoffs)[0])

    def update_position_premium_agg(self):
        premiums = []
        for pos in self.positions:
            premiums.append(dask.delayed(position_premium)(pos))
        self.premium = np.sum(dask.compute(premiums)[0])

    def profit(self, spot_expiry):
        return self.position_payoff_agg(spot_expiry) - self.premium

    def plot_payoff(self, range_low, range_high, step):
        # I know this part sucks, I got lazy and will fix it later
        spot_expiries = []
        payoffs = []
        profits = []
        for i in range(range_low, range_high, step):
            spot_expiries.append(i)
            payoffs.append(self.position_payoff_agg(i))
            profits.append(self.profit(i))

        df = pd.DataFrame({'Spot_Expiry': spot_expiries, 'Payoff': payoffs, 'Profit': profits})
        df.plot(x='Spot_Expiry')
        plt.show()
