from abc import ABC

import ipywidgets as widgets
from IPython.display import display

from pyspreads.model.base import HasAsset


class GUIBase(HasAsset, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.button_layout = widgets.Layout(width='60px', justify_content='center')
        self.asset_label = widgets.Label(f"Asset price = {self.asset}")

    @staticmethod
    def _output_plot(output, plot):
        output.clear_output()
        with output:
            display(plot)

