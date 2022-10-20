from abc import ABC, abstractmethod


class SubWidget(ABC):
    def __init__(self, gui):
        self.gui = gui
        self._widget = None

    @property
    def widget(self):
        if self._widget is None:
            self._widget = self.draw()
        return self._widget

    @abstractmethod
    def draw(self):
        pass
