import math

class ZeroCouponBond:

    def __init__(self, principal, premium=0):
        self.principal = principal
        self.premium = premium

    def cont_rate(self, ttm):
        return math.log(self.premium/self.principal)/-ttm

    def simple_rate(self, ttm):
        return (self.principal/self.premium)**(1/ttm) - 1

    # spot expiry not needed but fits rest of package, will add mode switching later
    def payoff(self, spot_expiry):
        return self.principal
