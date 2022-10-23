from __future__ import annotations

from typing import TYPE_CHECKING

import ipywidgets as widgets

from pyspreads.model.market import HasMarket

if TYPE_CHECKING:
    from pyspreads.gui.gui import VerticalGUI


class MarketGUI(HasMarket):
    def __init__(self, gui: VerticalGUI):
        super().__init__(gui=gui)
        self.button_layout = widgets.Layout(width='60px', justify_content='center')
        self.row_layout = widgets.Layout(min_height='35px')
        self.buttons = []

        self.market_output = widgets.Output()
        self.

    @staticmethod
    def price_to_string(price):
        return f"{price:2.2f}"

    def label(self, text):
        return widgets.Label(text, layout=self.button_layout)

    def option_button(self, price: float, strike: float, long_or_short: str, call_or_put: str):
        button = widgets.ToggleButton(
            description=self.price_to_string(price),
            layout=self.button_layout
        )
        button.price = price
        button.strike = strike
        button.long_or_short = long_or_short
        button.call_or_put = call_or_put
        if self.gui.position_name(strike, long_or_short, call_or_put) in self.gui.positions.keys():
            button.value = True
        button.observe(self._on_option_button_toggle, names=['value'])
        if (strike < self.gui.asset and call_or_put == 'call') or (self.gui.asset < strike and call_or_put == 'put'):
            button.style.text_color = 'darkgreen'
        return button

    def _on_option_button_toggle(self, change):
        button = change['owner']
        if change['new']:  # Pressed
            self.gui.take_position(button.price, button.strike, button.long_or_short, button.call_or_put)
        else:  # Unpressed
            try:
                self.gui.remove_position(button.strike, button.long_or_short, button.call_or_put)
            except KeyError:
                pass
                # TODO: This is an ugly hack to do with unpressing a button after the portfolio has been cleared.
                #       Find a  nicer way to deal with it.

    def draw(self):
        header = widgets.HBox(
            [self.label(text) for text in ["Call Bid", "Call Ask", "Strike", "Put Bid", "Put Ask"]],
            layout=self.row_layout
        )

        rows = []
        for row in self.gui.market.T:
            rows.append(widgets.HBox(
                [
                    self.option_button(row[1], row[0], 'short', 'call'),
                    self.option_button(row[2], row[0], 'long', 'call'),
                    self.label(self.price_to_string(row[0])),
                    self.option_button(row[3], row[0], 'short', 'put'),
                    self.option_button(row[4], row[0], 'long', 'put'),
                ],
                layout=self.row_layout
            ))

        # panel_layout =
        panel = widgets.VBox(rows) #, layout=panel_layout)

        return widgets.VBox([header, panel], layout=widgets.Layout(height='450px', min_width='320px'))

    def unpress_all(self):
        """
        TODO: Be more elegant and store the pressed ones somewhere to avoid the loop
        """
        for hbox in self.widget.children[1].children:
            for button in hbox.children:
                if isinstance(button, widgets.ToggleButton) and button.value:
                    button.value = False
