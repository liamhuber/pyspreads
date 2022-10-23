from typing import Optional

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import savgol_filter
from traitlets import default, Dict, Instance, Int

from pyspreads.model.base import HasAsset
from pyspreads.data.parser import read
from pyspreads.data.placeholder import REAL_PATH


class HasMarket(HasAsset):
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

    def smooth(self, x):
        return savgol_filter(x, self.smoothing_window, self.smoothing_order)

    def call_premium(self, x):
        return np.append(
            (x - self.asset + self.asset_prices)[self.asset_prices <= self.asset],
            x[self.asset_prices > self.asset]
        )

    def put_premium(self, x):
        return np.append(
            x[self.asset_prices < self.asset],
            (x + self.asset - self.asset_prices)[self.asset_prices >= self.asset]
        )

    @property
    def smoothed(self):
        return np.array([self.smooth(x) for x in self.market[1:]])

    @property
    def premiums(self):
        return np.array([
            self.call_premium(self.call_bid),
            self.call_premium(self.call_ask),
            self.put_premium(self.put_bid),
            self.put_premium(self.put_ask)
        ])

    @property
    def smoothed_premiums(self):
        return np.array([
            self.call_premium(self.smooth(self.call_bid)),
            self.call_premium(self.smooth(self.call_ask)),
            self.put_premium(self.smooth(self.put_bid)),
            self.put_premium(self.smooth(self.put_ask))
        ])

    @property
    def normalized_deviations(self):
        return (self.premiums - self.smoothed_premiums) / self.smoothed_premiums

    def plot_matrix(self, figax: Optional[tuple] = None):
        fig, ax = plt.subplots() if figax is None else figax
        for label, raw, smooth in zip(
            ['call bid', 'call ask', 'put bid', 'put ask'],
            self.market[1:],
            self.smoothed
        ):
            ax.scatter(self.asset_prices, raw, color=self.colors[label])
            ax.plot(self.asset_prices, smooth, label=label, color=self.colors[label])
        ax.set_ylabel("contract [$]")
        ax.set_xlabel("asset [$]")
        return fig, ax

    def plot_deviations(self, figax: Optional[tuple] = None, show_legend: bool = True):
        fig, ax = plt.subplots() if figax is None else figax
        for label, deviation in zip(
                ['call bid', 'call ask', 'put bid', 'put ask'],
                self.normalized_deviations * 100
        ):
            ax.scatter(self.asset_prices, deviation, label=label, color=self.colors[label])
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
        self.plot_deviations(figax=(fig, ax))
        ax2 = ax.twinx()
        self.plot_expectation(figax=(fig, ax2))
        if show_legend:
            fig.legend()
        fig.tight_layout()
        return fig, ax
