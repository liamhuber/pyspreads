from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from pyspreads.model.market import SingleAssetSingleExpiry as SASEMarket
from pyspreads.model.portfolio import SingleAssetSingleExpiry as SASEPortfolio


class VerticalModel(SASEMarket, SASEPortfolio):
    def plot_value(self, figax: Optional[tuple] = None, show_legend=True):
        fig, ax = plt.subplots() if figax is None else figax
        super().plot_value(self.asset_prices, figax=(fig, ax))
        ax2 = ax.twinx()
        self.plot_expectation(figax=(fig, ax2))
        if show_legend:
            fig.legend()
        fig.tight_layout()
        return fig, ax

    @property
    def expectation(self):
        return np.sum(self.value(self.asset_prices) * self.expectation_curve)

    @property
    def max_drawdown(self):
        # TODO: Check derivatives at maxima to allow for an "unbounded" response
        return np.amin(self.value(self.asset_prices))

    @property
    def max_return(self):
        raise NotImplementedError
