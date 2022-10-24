import ipywidgets as widgets

from pyspreads.gui.base import GUIBase
from pyspreads.model.model import VerticalModel


class PositionsGUI(VerticalModel, GUIBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.positions_output = widgets.Output()

        self.clear_positions_button = widgets.Button(description="Clear positions")
        self.positions_summary = widgets.VBox(
            [
                widgets.Label("Per-contract values:"),
                widgets.Label(f"Max return (if bounded) = NaN"),
                widgets.Label(f"'Expected' return = NaN"),
                widgets.Label(f"Max drawdown (if bounded) = NaN"),
                self.clear_positions_button
            ]
        )
        self._update_positions_summary()

        self.observe(self.update_positions, names=['positions'])

    def _update_positions_summary(self):
        self.positions_summary.children[1].value = f"Max return (if bounded) = {self.max_return:.3f}"
        self.positions_summary.children[2].value = f"'Expected' return = {self.expectation:.3f}"
        self.positions_summary.children[3].value = f"Max drawdown (if bounded) = {self.max_drawdown:.3f}"

    def draw_positions_plot(self):
        self._output_plot(self.positions_output, self.plot_positions()[0])

    def update_positions(self, change=None):
        self._update_positions_summary()
        self.draw_positions_plot()

    @property
    def positions_screen(self):
        return widgets.HBox([self.positions_output, self.positions_summary])

    @property
    def positions_widget(self):
        return widgets.VBox([self.positions_output, self.positions_summary])
