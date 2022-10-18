from typing import  Optional

import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from traitlets import Dict, observe

from pyspreads.model.base import HasAsset
from pyspreads.model.contract import Option


class SingleAssetSingleExpiry(HasAsset):
    """
    A model for assembling a position consisting of multiple options with the same underlying asset and expiry date.
    """

    positions = Dict(default_value={}, help="The individual options contracts held.")

    @observe('asset')
    def _update_asset_in_positions(self, change):
        for p in self.positions.values():
            p.asset = change['new']

    def value(self, asset_prices):
        return np.sum([p.value(asset_prices) for p in self.positions.values()], axis=0)

    @staticmethod
    def position_name(strike: float, long_or_short: str, call_or_put: str):
        return f"{long_or_short}_{call_or_put}_{strike:.4f}".replace('.', '_')

    def take_position(self, price: float, strike: float, long_or_short: str, call_or_put: str):
        # TODO: Maybe make a tuple of option and count instead, so multiple can be taken
        self.positions[self.position_name(strike, long_or_short, call_or_put)] = Option(
            price=price,
            strike=strike,
            asset=self.asset,
            call_or_put=call_or_put,
            long_or_short=long_or_short,
        )

    def remove_position(self, strike: float, long_or_short: str, call_or_put: str):
        self.positions.pop(self.position_name(strike, long_or_short, call_or_put))

    def buy_call(self, price: float, strike: float):
        self.take_position(price, strike, 'long', 'call')

    def sell_call(self, price: float, strike: float):
        self.take_position(price, strike, 'short', 'call')

    def buy_put(self, price: float, strike: float):
        self.take_position(price, strike, 'long', 'put')

    def sell_put(self, price: float, strike: float):
        self.take_position(price, strike, 'short', 'put')

    def plot_value(self, asset_prices, figax: Optional[tuple] = None):
        fig, ax = plt.subplots() if figax is None else figax
        ax.plot(asset_prices, self.value(asset_prices))
        ax.set_ylabel("Value")
        ax.axhline(0, color='k', linestyle='--')
        return fig, ax

    def clear_portfolio(self):
        self.positions = {}
