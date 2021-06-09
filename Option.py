import math

class Option:
    def __init__(self, strike, side="C", type="EU"):
        # Int for strike price of option
        self.strike = strike
        # "C" or "P" for Call or Put
        self.side = side
        # "EU" or "US" for American or European
        self.type = type

    def test_range(self, rfr, spot, ttm, premium):
        if self.type == "EU":
            if self.side == 'C':
                lower_bound = max(0, spot - self.strike * math.exp(-rfr * ttm))
                upper_bound = spot
            elif self.side == 'P':
                lower_bound = max(0, self.strike * math.exp(-rfr * ttm) - spot)
                upper_bound = self.strike * math.exp(-rfr * ttm)
        elif self.type == "US":
            if self.side == 'C':
                lower_bound = max(0, spot - self.strike * math.exp(-rfr * ttm))
            elif self.side == 'P':
                lower_bound = max(0, self.strike - spot)

            if self.side == 'C':
                upper_bound = spot
            elif self.side == 'P':
                upper_bound = self.strike
            
        if premium < lower_bound:
            # Return that option is cheap
            return -1
        elif premium > upper_bound:
            # Rreturn that option is expensive
            return 1
        else:
            # Return that option is within arbitrage ranges
            return 0

    def test_parity(self, rfr, spot, ttm, call_premium, put_premium):
        # rfr = risk free rate in decimal form (e.g. 0.01 is 1%)
        # spot = float of current spot price of underlying asset
        # ttm = time to maturity in trading days
        # call_premium / put_premium = float of price of call and put options being tested
        
        if self.type == "EU":
            left = call_premium + self.strike * math.exp(-rfr * ttm)
            right = put_premium + spot
    
            if left < right:
                # Return that position of call + bond that pays present value of strike price is cheap
                return -1
            elif left > right:
                # Return that position of put + 1 unit of underlying is cheap
                return 1
            else:
                # Return that options fall within put/call parity
                return 0

        elif self.type == "US":
            left = spot - self.strike
            spread = call_premium - put_premium
            right = spot - self.strike * math.exp(-rfr * ttm)

            if left > spread:
                return -1
            elif right < spread:
                return 1
            else:
                return 0

    def payoff(self, spot_exercise):
       if type == 'C':
            if self.strike <= spot_exercise:
                return (spot_exercise - self.strike)
            else:
                return 0
       elif type == 'P':
           if self.strike >= spot_exercise:
               return (self.strike - spot_exercise)
           else:
               return 0
