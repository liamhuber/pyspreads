from pathlib import Path
import numpy as np

REAL_PRICE = 370.085
REAL_PATH = Path(__file__).parent.joinpath('snapshots', 't2022-10-18-0910_SPY_370.085_e2022-12-22').resolve()
FAKE_PRICE = 100.


def premium_curve(x, x0, m=2, a=1, c=0., noise=0.):
    return c + (a / (1 + np.exp(-(x - x0) / m))) + a * noise * (np.random.rand(len(x)) - 0.5)


def fake_data(price=FAKE_PRICE, range_=20, n=80, spread_factor=0.8, volatility=10, inefficiency=0.02):
    strike_prices = np.linspace(price - range_, price + range_, n)

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