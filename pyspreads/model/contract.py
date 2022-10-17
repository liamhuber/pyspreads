import numpy as np
from traitlets import (
    Float,
    HasTraits,
    TraitError,
    Unicode,
    validate,
)


class Option(HasTraits):
    price = Float()
    strike = Float()
    asset = Float()
    call_or_put = Unicode()
    long_or_short = Unicode()

    @validate('price')
    @validate('strike')
    @validate('underlying')
    def _non_negative(self, proposal):
        if proposal['value'] < 0:
            raise TraitError(f"{proposal['trait'].name} must be non-negative but got {proposal['value']}")
        return proposal['value']

    @staticmethod
    def _string_in(s, vals):
        if s in vals:
            return s.lower()
        else:
            raise TraitError(f"Expected one of {vals}, but got {s}")

    @validate('call_or_put')
    def _ensure_call_or_put(self, proposal):
        return self._string_in(proposal['value'], ['call', 'put'])

    @validate('long_or_short')
    def _ensure_long_or_short(self, proposal):
        return self._string_in(proposal['value'], ['long', 'short'])

    @property
    def premium(self):
        if (
                (self.call_or_put == 'call' and self.asset < self.strike)
                or
                (self.call_or_put == 'put' and self.asset > self.strike)
        ):
            return self.price
        else:
            if self.call_or_put == 'call':
                return self.price - (self.asset - self.strike)
            else:  # self.call_or_put == 'put'
                return self.price - (self.strike - self.asset)

    @property
    def _is_call(self):
        return self.call_or_put == 'call'

    @property
    def _is_put(self):
        return not self._is_call

    @property
    def _is_long(self):
        return self.long_or_short == 'long'

    @property
    def _is_short(self):
        return not self._is_long

    def value(self, asset_prices):
        # TODO: Refactor into a single statement with bool-based multipliers if this winds up looking right
        if self._is_short and self._is_call:
            return self.price - (asset_prices - self.strike).clip(min=0)
        elif self._is_long and self._is_call:
            return (asset_prices - self.strike).clip(min=0) - self.price
        elif self._is_short and self._is_put:
            return self.price - (self.strike - asset_prices).clip(min=0)
        elif self._is_long and self._is_put:
            return (self.strike - asset_prices).clip(min=0) - self.price
        else:
            raise RuntimeError("Inconceivable")
