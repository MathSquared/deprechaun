from decimal import Decimal
from typing import Protocol, Tuple

from deprechaun.asset import Asset


ONE: Decimal = Decimal('1')
ZERO: Decimal = Decimal('0')


class DepreciationMethod(Protocol):
    """Depreciates an asset over a given period.

    Functions with this protocol implement various depreciation methods. The interface for all such methods is given here.

    These functions will not depreciate an asset beyond its useful life. If the period is greater than the asset's remaining life, the asset will be depreciated over its remaining useful life.

    Args:
        asset (Asset): The asset to depreciate.
        period (Decimal): The period over which to depreciate the asset. For example, for the year the asset was placed in service, this could reflect the time during the year that it was placed in service, or the convention used for depreciation.

    Returns:
        Decimal: The amount of depreciation.
    """
    def __call__(self, asset: Asset, period: Decimal = ...) -> Decimal: ...


def straight_line(asset: Asset, period: Decimal = ONE) -> Decimal:
    """The straight-line depreciation method.

    See IRS, "How to Depreciate Property," Publication 946 (2022), 39. Note that salvage value is not supported.
    """
    if period >= asset.life:
        return asset.basis
    else:
        return asset.basis / asset.life * period
