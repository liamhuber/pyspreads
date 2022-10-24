from abc import ABC

import ipywidgets as widgets
from IPython.display import display

from pyspreads.model.base import HasAsset


class GUIBase(HasAsset, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.button_layout = widgets.Layout(width='60px', justify_content='center')
        self.asset_label = widgets.Label(f"Asset price = {self.asset}")
        self.observe(self._update_asset_label, names=['asset'])

    def _update_asset_label(self, change):
        self.asset_label.value = f"Asset price = {change['new']}"

    @staticmethod
    def _output_plot(output, plot):
        output.clear_output()
        with output:
            display(plot)

