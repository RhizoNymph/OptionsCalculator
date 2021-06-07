# OptionsCalculator by QuantNymph

This is just the options calculator I built for payoff charts during my Derivatives course for my Master's instead of drawing them with excel.
The code in the initial commit was designed without the idea of other people using it or even really expanding it, but I'm changing that.

I will be adding comments and documentation over time, I'll be expanding this into a derivatives analytics suite with some monte carlo simulation tools
that use the payoff calculations to test derivatives strategies with simulated geometric brownian motion with stochastic correlation and volatility across series.

I'm open to suggestions and will keep this open source so people can work on it.

Right now it's just some functions but the code at the bottom shows the format and how to run for now. It can handle long and short options positions with different 
quantities, as well as holding units of the underlying asset. There are also some sanity checks for put/call parity and arbitrage ranges. I'll change these to be more modular
and object oriented over time and I'm having someone make a frontend so you don't have to run it with code.

This is only the beginning.
