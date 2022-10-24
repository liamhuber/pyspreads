import ipywidgets as widgets

from pyspreads.gui.base import GUIBase
from pyspreads.model.market import HasMarket


class MarketGUI(HasMarket, GUIBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.market_output = widgets.Output()
        self.premium_output = widgets.Output()
        self.deviation_output = widgets.Output()

        control_layout = widgets.Layout(width='190px')
        style = {'description_width': '110px'}
        self.smoothing_window_widget = widgets.BoundedIntText(
            description="Savgol smoothing window",
            value=self.smoothing_window,
            min=3,
            max=len(self.asset_prices),
            style=style,
            layout=control_layout
        )
        self.smoothing_order_widget = widgets.BoundedIntText(
            description="Savgol smoothing order",
            value=self.smoothing_order,
            min=2,
            max=len(self.asset_prices) - 1,
            style=style,
            layout=control_layout
        )

        self.smoothing_window_widget.observe(self._update_savgol_window, 'value')
        self.smoothing_order_widget.observe(self._update_savgol_order, 'value')
        self.observe(self.update_market, names=['market', 'smoothing_window', 'smoothing_order'])

    def _update_savgol_window(self, change):
        self.smoothing_window = change['new']

    def _update_savgol_order(self, change):
        self.smoothing_order = change['new']

    def draw_market_plot(self):
        self._output_plot(self.market_output, self.plot_market()[0])

    def draw_premium_plot(self):
        self._output_plot(self.premium_output, self.plot_premium()[0])

    def draw_deviations_plot(self):
        self._output_plot(self.deviation_output, self.plot_deviations()[0])

    def update_market(self, change=None):
        self.draw_market_plot()
        self.draw_premium_plot()
        self.draw_deviations_plot()
        self.smoothing_window_widget.max = len(self.asset_prices)
        self.smoothing_order_widget.max = len(self.asset_prices) - 1

    @property
    def market_screen(self):
        return widgets.VBox(
            [
                widgets.HBox(
                    [
                        self.asset_label,
                        self.smoothing_window_widget,
                        self.smoothing_order_widget
                    ]
                ),
                widgets.VBox(
                    [
                        self.market_output,
                        self.premium_output,
                        self.deviation_output
                    ]
                )
            ]
        )

    @property
    def market_widget(self):
        return widgets.VBox(
                    [
                        self.premium_output,
                        self.deviation_output,
                        self.asset_label
                    ]
                )


