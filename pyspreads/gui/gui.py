import ipywidgets as widgets

from pyspreads.gui.about import About
from pyspreads.gui.data import Loader
from pyspreads.gui.market import MarketGUI
from pyspreads.gui.positions import PositionsGUI


class VerticalGUI(MarketGUI, PositionsGUI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trade_widget = self._build_trade_widget()

        self.clear_positions_button.on_click(self.on_click_clear_positions)

        self.trade_screen = widgets.HBox(
            [
                self.trade_widget,
                self.positions_widget,
                self.market_widget
            ]
        )
        self.loader = Loader(self)

        self._app_tabs = [
            self.trade_screen,
            self.market_screen,
            self.positions_screen,
            self.loader.screen,
            About().screen
        ]
        self._app_tab_labels = ['Trade', 'Market', 'Positions', 'Load data', 'About']
        self._loading_tabs = [
            widgets.Label("Loading...")
        ]
        self._loading_tab_labels = ['Please wait']
        self.tabs = widgets.Tab([], layout=widgets.Layout(height='550px'))
        self.tabs_to_app()

        self.observe(self.update_trade, names=['market', 'asset'])
        self.observe(self.reset_positions, names=['market', 'asset'])
        self.update_all()

    def _build_trade_children(self):
        row_layout = widgets.Layout(min_height='35px')
        header = widgets.HBox(
            [self.make_label(text) for text in ["Call Bid", "Call Ask", "Strike", "Put Bid", "Put Ask"]],
            layout=row_layout
        )

        rows = []
        for row in self.market.T:
            rows.append(widgets.HBox(
                [
                    self.make_option_button(row[1], row[0], 'short', 'call'),
                    self.make_option_button(row[2], row[0], 'long', 'call'),
                    self.make_label(self.price_to_string(row[0])),
                    self.make_option_button(row[3], row[0], 'short', 'put'),
                    self.make_option_button(row[4], row[0], 'long', 'put'),
                ],
                layout=row_layout
            ))
        button_panel = widgets.VBox(rows)
        return header, button_panel

    def _build_trade_widget(self):
        header, button_panel = self._build_trade_children()
        return widgets.VBox(
            [header, button_panel],
            layout=widgets.Layout(height='450px', min_width='320px')
        )

    def make_label(self, text):
        return widgets.Label(text, layout=self.button_layout)

    def make_option_button(self, price: float, strike: float, long_or_short: str, call_or_put: str):
        if (strike < self.asset and call_or_put == 'call') or (self.asset < strike and call_or_put == 'put'):
            style_kwarg = {'button_style': 'success'}
        else:
            style_kwarg = {}
        button = widgets.ToggleButton(
            description=self.price_to_string(price),
            layout=self.button_layout,
            **style_kwarg
        )
        button.price = price
        button.strike = strike
        button.long_or_short = long_or_short
        button.call_or_put = call_or_put
        if self.position_name(strike, long_or_short, call_or_put) in self.positions.keys():
            button.value = True
        button.observe(self._on_option_button_toggle, names=['value'])
        return button

    @staticmethod
    def price_to_string(price):
        return f"{price:2.2f}"

    def _on_option_button_toggle(self, change):
        button = change['owner']
        if change['new']:  # Pressed
            self.take_position(button.price, button.strike, button.long_or_short, button.call_or_put)
        else:  # Unpressed
            try:
                self.remove_position(button.strike, button.long_or_short, button.call_or_put)
            except KeyError:
                pass
                # TODO: This is an ugly hack to do with unpressing a button after the portfolio has been cleared.
                #       Find a  nicer way to deal with it.

    def unpress_all_trade_buttons(self):
        """
        TODO: Be more elegant and store the pressed ones somewhere to avoid the loop
        """
        for hbox in self.trade_widget.children[1].children:
            for button in hbox.children:
                if isinstance(button, widgets.ToggleButton) and button.value:
                    button.value = False

    def clear_positions(self):
        super().clear_positions()
        # self.unpress_all_trade_buttons()
        for hbox in self._app_tabs[0].children[0].children[1].children:
            for tb in hbox.children:
                if isinstance(tb, widgets.ToggleButton) and tb.value == True:
                    tb.value = False
        # TODO: Figure out why the buttons list in the market_gui is not the same as these children

    def _set_tabs(self, tabs, labels, selected_index=0):
        self.tabs.children = tabs
        self.tabs.selected_index = selected_index
        for i, label in enumerate(labels):
            self.tabs.set_title(i, label)

    def tabs_to_loading(self):
        self._set_tabs(self._loading_tabs, self._loading_tab_labels)

    def tabs_to_app(self):
        self._set_tabs(self._app_tabs, self._app_tab_labels)

    def on_click_clear_positions(self, change):
        self.clear_positions()

    def update_trade(self, change=None):
        self.trade_widget.children = self._build_trade_children()

    def update_all(self):
        self.update_market()
        self.update_positions()
        self.update_trade()

    def show(self):
        return self.tabs
