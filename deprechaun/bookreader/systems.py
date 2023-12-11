import calendar
from decimal import Decimal
from enum import auto, Enum
from typing import Any, NamedTuple, Protocol, Sequence

from deprechaun.asset import Asset
from deprechaun.method import DepreciationMethod
from . import BookAsset


class Hydrator(Protocol):
    """A function, defined for a system, to check asset validity and compute any necessary data.

    This is one of three functions defined for a given depreciation system, the others being the translator and the stepper. It:

    - checks that all assets defined under the system are validly defined;
    - computes any values that the system requires to be computed rather than defined by the asset owner; and
    - returns a list of new assets containing the precomputed values.

    The returned list is in the same order as the input sequence. All assets are the same, except that those whose ``system`` is the system for which the hydrator is written may be different.

    Args:
        assets (Sequence[BookAsset]): **All** of the assets, including those with a different system.

    Returns:
        list[BookAsset]: A list of hydrated assets, as described above.
    """
    def __call__(self, assets: Sequence[BookAsset]) -> list[BookAsset]: ...


class Translator(Protocol):
    """A function, defined for a system, that converts a ``BookAsset`` into an ``Asset.``

    This is the second function defined for a system. It converts a given book asset, which must be hydrated by the system's hydrator, into a depreciable asset.

    Args:
        asset (BookAsset): An asset, which must be hydrated by the system's hydrator, and whose ``system`` must be the system for which this translator is written.

    Returns:
        Asset: A depreciable asset based on this book asset.

    Raises:
        ValueError: If the book asset's ``system`` does not match the system for this translator.
    """
    def __call__(self, asset: BookAsset) -> Asset: ...


class Stepper(Protocol):
    """A function, defined for a system, that indicates the period over which a ``BookAsset`` should be depreciated in a given year.

    This is the third function defined for a system. Generally, it is used to give effect to an offset parameter or similar, since this is not preserved with the ``Asset``.

    This does not take into account the asset's disposal date or the elapsing of its useful life.

    Args:
        asset (BookAsset): An asset, which must be hydrated by the system's hydrator, and whose ``system`` must be the system for which this translator is written.
        year (int): The tax year for which to depreciate the asset.

    Returns:
        Decimal: The period (fraction of the year) over which to depreciate the asset for the given tax year.
    """
    # TODO should it take disposal into account? user may need to specify how to prorate that date
    def __call__(self, asset: BookAsset, year: int) -> Decimal: ...


_SYSTEMS: dict[str, tuple[Hydrator, Translator, Stepper]] = {}  # TODO define functions that must be registered for a system


def systems() -> list[str]:
    """Returns a list of registered system names."""
    return list(_SYSTEMS.keys())


def system(name: str) -> tuple[Hydrator, Translator, Stepper]:
    """Returns the hydrator, translator, and stepper for a given system.

    Raises:
        KeyError: if a system by the given name is not registered.
    """
    return _SYSTEMS[name]


def register_system(name: str, hydrator: Hydrator, translator: Translator, stepper: Stepper):
    if name in _SYSTEMS:
        raise KeyError(name)
    _SYSTEMS[name] = (hydrator, translator, stepper)


### TIME SYSTEM ###


class TimeSystemOffsetSubstitute(Enum):
    """The method of basing the offset on the asset's time in service instead of specifying it manually.

    Attributes:
        DAY: The offset is the proportion of the days of the year that fall on or after the in-service date.
        MONTH: The offset is the proportion of the months of the year that fall on or after the month of the in-service date.
    """
    DAY = auto()
    MONTH = auto()


class TimeSystemData(NamedTuple):
    """Data for the time system.

    Attributes:
        life (Decimal): The useful life of the asset, in years.
        offset (Decimal | TimeSystemOffsetSubstitute): The period during the year during which the asset is **not** in service; or, a description of how this is to be computed from the asset's in-service date. For the year the asset is placed in service, its depreciation period is ``1`` minus the offset.
        method (DepreciationMethod): The depreciation method to be used for the asset.
    """
    life: Decimal
    offset: Decimal | TimeSystemOffsetSubstitute
    method: DepreciationMethod


def time_system_hydrate(assets: Sequence[BookAsset]) -> list[BookAsset]:
    """Hydrates assets for the time system.

    The time system is for depreciation over a fixed term of years where no specific system (such as MACRS) applies, meaning all depreciation details are specified manually.
    """
    ret = []
    for asset in assets:
        if asset.system == 'time':
            if isinstance(asset.system_data.offset, TimeSystemOffsetSubstitute):
                offset = asset.system_data.offset
                in_service = asset.in_service
                
                # Overall strategy: count the {days,months} *before*, exclusive, the in-service date
                if offset == TimeSystemOffsetSubstitute.DAY:
                    day_of_year = in_service.toordinal() - in_service.replace(month=1, day=1).toordinal()  # zero-based
                    days_in_year = 366 if calendar.isleap(in_service.year) else 365
                    new_offset = Decimal(day_of_year) / days_in_year
                elif offset == TimeSystemOffsetSubstitute.MONTH:
                    new_offset = (Decimal(in_service.month) - 1) / 12  # month placed in service doesn't count
                else:
                    raise ValueError('impossible TimeSystemOffsetSubstitute: should never happen')
                new_data = asset.system_data._replace(offset=new_offset)
                new_asset = asset._replace(system_data=new_data)
                ret.append(new_asset)
            else:
                ret.append(asset)
        else:
            ret.append(asset)
    return ret


def time_system_translate(asset: BookAsset) -> Asset:
    """Translates an asset with the time system into an ``Asset`` for depreciation."""
    if asset.system != 'time':
        raise ValueError(f'asset system {asset.system} not equal to time')
    basis = asset.basis_start + sum(asset.basis_impairment) + sum(asset.basis_adjustment)
    life = asset.system_data.life  # offset must be tracked separately to depreciate the right amount
    method = asset.system_data.method
    precision = asset.precision
    return Asset(basis=basis, life=life, method=method, precision=precision)


def time_system_step(asset: BookAsset, year: int) -> Decimal:
    """Returns the period over which an asset with the time system should be depreciated in a given year."""
    # TODO account for disposal, potentially with offset substitute
    if asset.system != 'time':
        raise ValueError(f'asset system {asset.system} not equal to time')
    if year != asset.in_service.year:
        return Decimal('1')
    return Decimal('1') - asset.system_data.offset


register_system('time', time_system_hydrate, time_system_translate, time_system_step)
