from __future__ import annotations

from typing import TYPE_CHECKING

import ipywidgets as widgets

from pyspreads.data.parser import read
from pyspreads.gui.base import SubWidget

if TYPE_CHECKING:
    from pyspreads.gui.gui import VerticalGUI


class Loader(SubWidget):
    def __init__(self, gui: VerticalGUI):
        super().__init__(gui=gui)
        control_layout = widgets.Layout(width='190px')
        style = {'description_width': '110px'}
        self.asset = widgets.FloatText(description="Asset price", style=style, layout=control_layout)
        self.row_delimiter = widgets.Text(description="Row delimiter", value='\n', style=style, layout=control_layout)
        self.col_delimiter = widgets.Text(description="Col delimiter", value='\t', style=style, layout=control_layout)
        self.comments = widgets.Text(description="Comments", value='#', style=style, layout=control_layout)
        self.skiprows = widgets.IntText(description="Skip rows", value=0, style=style, layout=control_layout)
        self.strike_col = widgets.IntText(description="Strike column", value=8, style=style, layout=control_layout)
        self.call_bid_col = widgets.IntText(description="Call bid column", value=1, style=style, layout=control_layout)
        self.call_ask_col = widgets.IntText(description="Call ask column", value=2, style=style, layout=control_layout)
        self.put_bid_col = widgets.IntText(description="Put bid column", value=11, style=style, layout=control_layout)
        self.put_ask_col = widgets.IntText(description="Put ask column", value=12, style=style, layout=control_layout)
        self.load = widgets.Button(description="Load data", layout=control_layout)
        self.load.on_click(self._on_load)

        self.controls = widgets.VBox(
            [
                self.asset,
                self.row_delimiter,
                self.col_delimiter,
                self.strike_col,
                self.call_bid_col,
                self.call_ask_col,
                self.put_bid_col,
                self.put_ask_col,
                self.comments,
                self.skiprows,
                self.load
            ],
            layout=widgets.Layout(min_width='200px')
        )

        self.data = widgets.Textarea(
            placeholder="Enter columnar market data here",
            layout=widgets.Layout(height='400px', width='100%')
        )

    def draw(self):
        return widgets.HBox([self.controls, self.data])

    def _on_load(self, change):
        asset = self.asset.value
        market = read(
            self.data.value,
            row_delimiter=self.row_delimiter.value,
            col_delimiter=self.col_delimiter.value,
            strike_col=self.strike_col.value,
            call_bid_col=self.call_bid_col.value,
            call_ask_col=self.call_ask_col.value,
            put_bid_col=self.put_bid_col.value,
            put_ask_col=self.put_ask_col.value,
            comments=self.comments.value,
            skiprows=self.skiprows.value
        )
        self.gui.asset = asset
        self.gui.market = market
        self.gui.update()
