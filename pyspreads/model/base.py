from abc import ABC, ABCMeta

from traitlets import (
    Float,
    HasTraits,
    MetaHasTraits
)

from pyspreads.data.placeholder import REAL_PRICE


class TraitsABCMeta(MetaHasTraits, ABCMeta):
    pass


class HasAsset(HasTraits, ABC, metaclass=TraitsABCMeta):
    """
    A parent class for classes that rely on an underlying asset
    """
    asset = Float(default_value=REAL_PRICE, help="The current price of the underlying asset.")
