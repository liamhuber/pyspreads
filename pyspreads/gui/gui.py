from pyspreads.gui.market import SingleAssetSingleExpiry as SASEMarketGUI
from pyspreads.model import VerticalModel


class VerticalGUI(VerticalModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.market_gui = SASEMarketGUI(self)

    def draw(self):
        self.market_gui.draw()
        return self.market_gui.widget