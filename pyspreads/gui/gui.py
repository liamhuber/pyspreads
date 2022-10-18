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
        clear_portfolio_button = widgets.Button(description="Clear portfolio")
        clear_portfolio_button.on_click(self.on_click_clear_portfolio)
        self.portfolio_summary = widgets.VBox(
            [
                widgets.Label(f"MAX RETURN = {self.max_return}"),
                widgets.Label(f"EXPECTATION = {self.expectation}"),
                widgets.Label(f"MAX DRAWDOWN = {self.max_drawdown}"),
                clear_portfolio_button
            ]
        )
        self.trade_screen = widgets.HBox(
            [
                self.market_gui.widget,
                self.portfolio_display,
                widgets.VBox(
                    [self.market_display, self.portfolio_summary],
                    layout=widgets.Layout(width='33%')
                )
            ]
        )

        self.tabs = widgets.Tab(
            [
                self.trade_screen,
                self.market_display,
                widgets.HBox([self.portfolio_display, self.portfolio_summary])
            ],
            layout=widgets.Layout(height='500px')
        )
        self.tabs.set_title(0, 'Trade')
        self.tabs.set_title(1, 'Market')
        self.tabs.set_title(2, 'Portfolio')

    def draw_market_plot(self):
        self.market_display.clear_output()
        with self.market_display:
            display(self.plot_market()[0])

    def draw_portfolio_plot(self):
        self.portfolio_display.clear_output()
        with self.portfolio_display:
            display(self.plot_value()[0])

    def update_portfolio_summary(self):
        self.portfolio_summary.children[0].value = f"MAX RETURN = {self.max_return}"
        self.portfolio_summary.children[1].value = f"EXPECTATION = {self.expectation}"
        self.portfolio_summary.children[2].value = f"MAX DRAWDOWN = {self.max_drawdown}"

    def update_market_gui(self):
        """Careful, this one is expensive"""
        self.market_gui = SASEMarketGUI(self)
        self.market_gui.draw()

    def update_market(self):
        self.update_market_gui()
        self.draw_market_plot()

    def update_portfolio(self):
        self.draw_portfolio_plot()
        self.update_portfolio_summary()

    def update(self):
        self.update_market()
        self.update_portfolio()

    def draw(self):
        self.update()
        return self.tabs

    def take_position(self, price: float, strike: float, long_or_short: str, call_or_put: str):
        super().take_position(price=price, strike=strike, long_or_short=long_or_short, call_or_put=call_or_put)
        self.update_portfolio()

    def remove_position(self, strike: float, long_or_short: str, call_or_put: str):
        super().remove_position(strike=strike, long_or_short=long_or_short, call_or_put=call_or_put)
        self.update_portfolio()

    def clear_portfolio(self):
        super().clear_portfolio()
        self.update_portfolio()
        # self.market_gui.unpress_all()
        for hbox in self.tabs.children[0].children[0].children[1].children:
            for tb in hbox.children:
                if isinstance(tb, widgets.ToggleButton) and tb.value == True:
                    tb.value = False
        # TODO: Figure out why the buttons list in the market_gui is not the same as these children

    def on_click_clear_portfolio(self, change):
        self.clear_portfolio()
