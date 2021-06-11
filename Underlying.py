class Underlying:
    def __init__(self, premium):
        self.premium = premium

    def payoff(self, spot_expiry):
        return spot_expiry