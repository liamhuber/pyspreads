import ipywidgets as widgets
from IPython.display import display

from pyspreads.gui.market import SingleAssetSingleExpiry as SASEMarketGUI
from pyspreads.model import VerticalModel


class VerticalGUI(VerticalModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.market_gui = SASEMarketGUI(self)
        self.market_display = widgets.Output()
        self.portfolio_display = widgets.Output()

    def draw(self):
        self.market_gui.draw()
        self.market_display.clear_output()
        with self.market_display:
            display(self.plot_market()[0])
        self.portfolio_display.clear_output()
        with self.portfolio_display:
            display(self.plot_value()[0])

        return widgets.HBox(
            [
                self.market_gui.widget,
                self.portfolio_display,
                widgets.VBox(
                    [
                        self.market_display,
                        widgets.Label(f"MAX RETURN = {self.max_return}"),
                        widgets.Label(f"EXPECTATION = {self.expectation}"),
                        widgets.Label(f"MAX DRAWDOWN = {self.max_drawdown}"),
                    ],
                    layout=widgets.Layout(width='25%')
                )
            ]
        )
