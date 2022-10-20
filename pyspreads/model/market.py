from typing import Optional

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import savgol_filter
from traitlets import default, Dict, Instance, Int

from pyspreads.model.base import HasAsset
from pyspreads.data.parser import read
from pyspreads.data.placeholder import REAL_PATH


class SingleAssetSingleExpiry(HasAsset):
    market = Instance(
        klass=np.ndarray,
        help="With columns strike price, call bid, call ask, put bid, put ask."
    )
    smoothing_window = Int(default_value=7, help="Window size for Savitzky-Golay smoothing")
    smoothing_order = Int(default_value=3, help="Polynomial order for Savitzky-Golay smoothing")
    colors = Dict()

    @default('market')
    def _read_placeholder_data(self):
        return read(REAL_PATH)

    @default('colors')
    def _palette(self):
        palette = sns.color_palette('vlag', n_colors=5)
        return {
            'call bid': palette[0],
            'call ask': palette[1],
            'put bid': palette[4],
            'put ask': palette[3],
            'expectation': 'black'
        }

    @property
    def asset_prices(self):
        return self.market[0]

    @property
    def call_bid(self):
        return self.market[1]

    @property
    def call_ask(self):
        return self.market[2]

    @property
    def put_bid(self):
        return self.market[3]

    @property
    def put_ask(self):
        return self.market[4]

    @property
    def smooth_call_bid(self):
        # TODO: Do it with a decorator or something
        y = self.call_bid
        return savgol_filter(y, self.smoothing_window, self.smoothing_order)

    @property
    def smooth_call_ask(self):
        y = self.call_ask
        return savgol_filter(y, self.smoothing_window, self.smoothing_order)

    @property
    def smooth_put_bid(self):
        y = self.put_bid
        return savgol_filter(y, self.smoothing_window, self.smoothing_order)

    @property
    def smooth_put_ask(self):
        y = self.put_ask
        return savgol_filter(y, self.smoothing_window, self.smoothing_order)

    def plot_matrix(self, figax: Optional[tuple] = None):
        fig, ax = plt.subplots() if figax is None else figax
        for label, raw, smooth in zip(
            ['call bid', 'call ask', 'put bid', 'put ask'],
            [self.call_bid, self.call_ask, self.put_bid, self.put_ask],
            [self.smooth_call_bid, self.smooth_call_ask, self.smooth_put_bid, self.smooth_put_ask]
        ):
            ax.scatter(self.asset_prices, raw, color=self.colors[label])
            ax.plot(self.asset_prices, smooth, label=label, color=self.colors[label])
        ax.set_ylabel("contract [$]")
        ax.set_xlabel("asset [$]")
        return fig, ax

    def plot_deviations(self, figax: Optional[tuple] = None, show_legend: bool = True):
        fig, ax = plt.subplots() if figax is None else figax
        for label, raw, smooth in zip(
                ['call bid', 'call ask', 'put bid', 'put ask'],
                [self.call_bid, self.call_ask, self.put_bid, self.put_ask],
                [self.smooth_call_bid, self.smooth_call_ask, self.smooth_put_bid, self.smooth_put_ask]
        ):
            ax.scatter(self.asset_prices, (raw - smooth)/smooth, label=label, color=self.colors[label])
        ax.axhline(0, color='k')
        ax.axvline(self.asset, linestyle='--', color='k')
        ax.set_ylabel("contract deviation [%]")
        ax.set_xlabel("asset [$]")
        if show_legend:
            fig.legend()
        fig.tight_layout()
        return fig, ax

    @property
    def premium_curve(self):
        return np.append(
            self.market[4][self.asset_prices < self.asset],
            self.market[2][self.asset_prices >= self.asset]
        )

    def plot_premium(self, figax: Optional[tuple] = None):
        fig, ax = plt.subplots() if figax is None else figax
        ax.plot(self.asset_prices, self.premium_curve)
        return fig, ax

    @property
    def expectation_curve(self):
        eps = 1e-8
        exp = np.exp(-1 / (self.premium_curve + eps))
        return exp / np.trapz(exp, x=self.asset_prices)

    def plot_expectation(self, figax: Optional[tuple] = None):
        fig, ax = plt.subplots() if figax is None else figax
        ax.plot(self.asset_prices, self.expectation_curve, label="expectation", color=self.colors['expectation'])
        ax.axvline(self.asset, linestyle='--', color=self.colors['expectation'])
        ax.set_ylabel("<asset>")
        ax.set_xlabel("asset [$]")
        return fig, ax

    def plot_market(self, figax: Optional[tuple] = None, show_legend=True):
        fig, ax = plt.subplots() if figax is None else figax
        self.plot_matrix(figax=(fig, ax))
        ax2 = ax.twinx()
        self.plot_expectation(figax=(fig, ax2))
        if show_legend:
            fig.legend()
        fig.tight_layout()
        return fig, ax
