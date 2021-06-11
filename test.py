from Option import *
from Underlying import *
from ZeroCouponBond import *
from PositionManager import *

call30 = Option(30)
pos1 = Position(call30, 1.50)

put30 = Option(30, 'P')
pos2 = Position(put30, 1.50, "+", 2)

portfolio = PositionAggregator([pos1, pos2])
portfolio.plot_payoff(0,51,10)