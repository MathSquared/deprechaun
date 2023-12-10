from __future__ import annotations

from decimal import Decimal
from typing import Callable, NamedTuple, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from deprechaun.method import DepreciationMethod


class Asset(NamedTuple):
    """A depreciable asset.

    This class includes all information about an asset necessary to depreciate it.

    It deliberately does not include the name of the asset, date it was placed in service, or similar information that is used to identify the asset but is not relevant to depreciation. It also does not include when in the year the asset was placed in service, the convention that is used, or similar. The amount that remains to be recovered in the last year of depreciation should be represented as the fractional part of the life parameter.

    Attributes:
        basis (Decimal): The adjusted basis of the asset for depreciation, less any depreciation that has already been deducted.
        life (Decimal): The remaining useful life or recovery period of the asset, in years.
        method (DepreciationMethod): The default depreciation method for the asset.
    """
    basis: Decimal
    life: Decimal
    method: 'DepreciationMethod'
