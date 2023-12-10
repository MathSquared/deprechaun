from decimal import Decimal
from typing import Protocol, Tuple

from deprechaun.asset import Asset


ONE: Decimal = Decimal('1')
ZERO: Decimal = Decimal('0')


class DepreciationMethod(Protocol):
    def __call__(self, asset: Asset, period: Decimal = ...) -> Tuple[Decimal, Asset]: ...


def straight_line(asset: Asset, period: Decimal = ONE) -> Tuple[Decimal, Asset]:
    if period >= asset.life:
        dep = asset.basis
        ret = Asset(basis=ZERO, life=ZERO, method=asset.method)
    else:
        dep = asset.basis / asset.life * period
        rbasis = asset.basis - dep
        rlife = asset.life - period
        ret = Asset(basis=rbasis, life=rlife, method=asset.method)
    return dep, ret
