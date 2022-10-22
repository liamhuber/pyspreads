from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from pyspreads.model.market import HasMarket
from pyspreads.model.portfolio import HasPositions


class VerticalModel(HasMarket, HasPositions):
    def plot_positions(self, figax: Optional[tuple] = None, show_legend=True):
        fig, ax = plt.subplots() if figax is None else figax
        if len(self.positions) > 0:
            super().plot_positions(self.asset_prices, figax=(fig, ax))
        ax2 = ax.twinx()
        self.plot_expectation(figax=(fig, ax2))
        if show_legend:
            fig.legend()
        fig.tight_layout()
        return fig, ax

    @property
    def expectation(self):
        return float(np.sum(self.value(self.asset_prices) * self.expectation_curve))

    @property
    def max_drawdown(self):
        # TODO: Check derivatives at maxima to allow for an "unbounded" response
        return float(np.amin(self.value(self.asset_prices)))

    @property
    def max_return(self):
        return float(np.amax(self.value(self.asset_prices)))
