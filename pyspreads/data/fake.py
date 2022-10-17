import numpy as np

PRICE = 100.

def premium_curve(x, x0, m=2, a=1, c=0., noise=0.):
    return c + (a / (1 + np.exp(-(x - x0) / m))) + a * noise * (np.random.rand(len(x)) - 0.5)

def fake_data(price=PRICE, range_=20, n=80, spread_factor=0.8, volatility=10, inefficiency=0.02):
    price = 100
    range_ = 20
    n = 80
    strike_prices = np.linspace(price - range_, price + range_, n)

    spread_factor = 0.8
    volatility = 10
    inefficiency = 0.02

    call_bid = premium_curve(strike_prices, price, m=volatility, noise=inefficiency, a=spread_factor)[::-1]
    call_ask = premium_curve(strike_prices, price, m=volatility, noise=inefficiency)[::-1]
    put_bid = premium_curve(strike_prices, price, m=volatility, noise=inefficiency, a=spread_factor)
    put_ask = premium_curve(strike_prices, price, m=volatility, noise=inefficiency)

    return np.vstack((
        strike_prices,
        call_bid,
        call_ask,
        put_bid,
        put_ask
    ))