from decimal import Decimal
from typing import Protocol, Tuple

from deprechaun.asset import Asset


ONE: Decimal = Decimal('1')
ZERO: Decimal = Decimal('0')


class DepreciationMethod(Protocol):
    """Depreciates an asset over a given period.

    Functions with this protocol implement various depreciation methods. The interface for all such methods is given here.

    These functions will not depreciate an asset beyond its useful life. If the period is greater than or equal to the asset's remaining life, the asset will be depreciated over its remaining useful life.

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


_DECLINING_BALANCE_ONLY_MEMO: dict[Decimal, DepreciationMethod] = {}

def declining_balance_only(rate: int | str | Decimal) -> DepreciationMethod:
    """Returns a function for the declining-balance depreciation method, without switching to straight-line.

    See IRS, "How to Depreciate Property," Publication 946 (2022), 38-39. Note that salvage value is not supported.

    If you are using MACRS, this is probably not what you're looking for, since MACRS requires switching to the straight-line method when it returns an equal or greater deduction. Instead, use ``declining_balance_macrs``.

    Args:
        rate (int | str | Decimal): The declining-balance rate, **in percent** (so call ``declining_balance_only(40)`` for 40%). This is the declining-balance percentage **divided by the useful life of the property**.

    Returns:
        DepreciationMethod: A function implementing the declining-balance depreciation method for the given rate. This will be the same function for the same rate.
    """
    rate = Decimal(rate)
    if rate in _DECLINING_BALANCE_ONLY_MEMO:
        return _DECLINING_BALANCE_ONLY_MEMO[rate]
    else:
        def declining_balance_only_impl(asset: Asset, period: Decimal = ONE) -> Decimal:
            return asset.basis * rate / 100 * min(period, asset.life)
        _DECLINING_BALANCE_ONLY_MEMO[rate] = declining_balance_only_impl
        return declining_balance_only_impl


_DECLINING_BALANCE_MACRS_MEMO: dict[Decimal, DepreciationMethod] = {}

def declining_balance_macrs(rate: int | str | Decimal) -> DepreciationMethod:
    """Returns a function for the declining-balance depreciation method, switching to straight-line when it produces an equal or greater deduction.

    See IRS, "How to Depreciate Property," Publication 946 (2022), 38-39. Note that salvage value is not supported.

    Args:
        rate (int | str | Decimal): The declining-balance rate, **in percent** (so call ``declining_balance_macrs(40)`` for 40%). This is the declining-balance percentage **divided by the recovery period of the property**.

    Returns:
        DepreciationMethod: A function implementing the declining-balance MACRS depreciation method for the given rate. This will be the same function for the same rate.
    """
    rate = Decimal(rate)
    if rate in _DECLINING_BALANCE_MACRS_MEMO:
        return _DECLINING_BALANCE_MACRS_MEMO[rate]
    else:
        def declining_balance_macrs_impl(asset: Asset, period: Decimal = ONE) -> Decimal:
            return max(straight_line(asset, period), declining_balance_only(rate)(asset, period))
        _DECLINING_BALANCE_MACRS_MEMO[rate] = declining_balance_macrs_impl
        return declining_balance_macrs_impl
