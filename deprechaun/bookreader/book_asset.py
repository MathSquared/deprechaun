from datetime import date
from decimal import Decimal
from typing import Any, NamedTuple

from .systems import SystemData


class BookAsset(NamedTuple):
    """An asset recorded on the accounting books.

    Attributes:
        name (str): A short name for the asset. Generally used to correlate records in accounting books.
        acquired (date): The date the asset was acquired.
        basis_start (Decimal): The adjusted basis in the asset when it was placed in service.
        basis_impairment (list[Decimal]): The depreciation deductions for this asset in each year, beginning with the year the asset was placed in service, and stored as negative numbers.
        basis_adjustment (list[Decimal]): Any other changes in the asset's basis during the year, starting from when it was placed in service.
        system (str): The depreciation system used for the asset, which provides the specific method of computing a depreciation allowance for this kind of asset.
        system_data (SystemData): Any data used for the depreciation system. The format of this data will depend on the depreciation system.
        long_name (str | None): A long name for the asset, which provides a fuller description.
        placed_in_service (date | None): The date the asset was placed in service. ``None`` means it was placed in service immediately when acquired.
        disposed (date | None): The date the asset was disposed of. ``None`` means the asset has not been disposed of.
        salvage (Decimal): The salvage value of the asset, if any.
    """
    name: str
    acquired: date
    basis_start: Decimal
    basis_impairment: list[Decimal]
    basis_adjustment: list[Decimal]
    system: str
    system_data: SystemData
    long_name: str | None = None
    placed_in_service: date | None = None
    disposed: date | None = None
    salvage: Decimal = Decimal('0')

    @property
    def display_name(self) -> str:
        """The long name if it is defined, or the (short) name otherwise."""
        return self.long_name if self.long_name is not None else self.name

    @property
    def in_service(self) -> date:
        """The delayed in service date if it is defined, or the acquisition date otherwise."""
        return self.placed_in_service if self.placed_in_service is not None else self.acquired
