from decimal import Decimal
from typing import Protocol, Tuple

from deprechaun.asset import Asset


ONE: Decimal = Decimal('1')
ZERO: Decimal = Decimal('0')


class DepreciationMethod(Protocol):
    """Depreciates an asset over a given period.

    Functions with this protocol implement various depreciation methods. The interface for all such methods is given here.

    These functions will not depreciate an asset beyond its useful life. If the period is greater than the asset's remaining life, the entire basis will be returned as the depreciation value, and the returned asset will have its basis and life both set to zero.

    Args:
        asset (Asset): The asset to depreciate.
        period (Decimal): The period over which to depreciate the asset. For example, for the year the asset was placed in service, this could reflect the time during the year that it was placed in service, or the convention used for depreciation.

    Returns:
        Tuple[Decimal, Asset]: The amount of depreciation, and a new asset with the basis reduced by the depreciation amount, the life reduced by the period, and the same method as the original asset.
    """
    def __call__(self, asset: Asset, period: Decimal = ...) -> Tuple[Decimal, Asset]: ...


def straight_line(asset: Asset, period: Decimal = ONE) -> Tuple[Decimal, Asset]:
    """The straight-line depreciation method.

    See IRS, "How to Depreciate Property," Publication 946 (2022), 39. Note that salvage value is not supported.
    """
    if period >= asset.life:
        dep = asset.basis
        ret = Asset(basis=ZERO, life=ZERO, method=asset.method)
    else:
        dep = asset.basis / asset.life * period
        rbasis = asset.basis - dep
        rlife = asset.life - period
        ret = Asset(basis=rbasis, life=rlife, method=asset.method)
    return dep, ret
