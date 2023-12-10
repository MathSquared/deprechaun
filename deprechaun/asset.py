from decimal import Decimal, ROUND_HALF_UP
from typing import NamedTuple, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from deprechaun.method import DepreciationMethod


_ZERO: Decimal = Decimal('0')
_ONE: Decimal = Decimal('1')


class Asset(NamedTuple):
    """A depreciable asset.

    This class includes all information about an asset necessary to depreciate it.

    It deliberately does not include the name of the asset, date it was placed in service, or similar information that is used to identify the asset but is not relevant to depreciation. It also does not include when in the year the asset was placed in service, the convention that is used, or similar. The amount that remains to be recovered in the last year of depreciation should be represented as the fractional part of the life parameter.

    Attributes:
        basis (Decimal): The adjusted basis of the asset for depreciation, less any depreciation that has already been deducted.
        life (Decimal): The remaining useful life or recovery period of the asset, in years.
        method (DepreciationMethod): The default depreciation method for the asset.
        precision (int | None): The exponent to which to round all depreciation values, or None to use exact values (as far as the thread's decimal context will allow). For example, ``-2`` to round to the nearest cent.
    """
    basis: Decimal
    life: Decimal
    method: 'DepreciationMethod'
    precision: int | None = None

    def depreciate(self, period: Decimal = _ONE) -> Tuple[Decimal, 'Asset']:
        """Depreciates the asset using its configured depreciation method.

        Generally, calls the asset's method attribute with the provided period. The depreciation method's return value is the depreciation value returned from this method. The returned asset is a new asset with the basis deducted by the depreciation value and the life deducted by the provided period.

        This method will not depreciate the asset beyond its useful life. If the period is greater than the asset's remaining life, the depreciation method is called using the remaining life as the depreciation period, and the returned asset will have its basis and life both set to zero.

        If the asset's precision is not None, the return value of the depreciation method is rounded to ``10**precision``, with the ``ROUND_HALF_UP`` rounding method, before it is subtracted from the basis. Thus, if the asset's original basis is specified only within the given precision, fractional cents will be allocated to one or another year, and the sum of the rounded depreciation values will equal the original basis.

        Args:
            period (Decimal): The period over which to depreciate the asset. For example, for the year the asset was placed in service, this could reflect the time during the year that it was placed in service, or the convention used for depreciation.

        Returns:
            Tuple[Decimal, Asset]: The amount of depreciation, and a new asset with a basis equal to this asset's basis less the depreciation amount, a life equal to this asset's life less the depreciation period (but no less than zero), and the same method as this asset.
        """
        if period < self.life:
            dep = self.method(self, period=period)
            if self.precision is not None:
                dep = dep.quantize(Decimal(10)**self.precision, ROUND_HALF_UP)
            rbasis = self.basis - dep
            rlife = self.life - period
            return dep, Asset(basis=rbasis, life=rlife, method=self.method)
        else:
            dep = self.method(self, period=self.life)
            if self.precision is not None:
                dep = dep.quantize(Decimal(10)**self.precision, ROUND_HALF_UP)
            return dep, Asset(basis=_ZERO, life=_ZERO, method=self.method)
