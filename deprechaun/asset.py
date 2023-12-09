from __future__ import annotations

from decimal import Decimal
from typing import Callable, NamedTuple, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from deprechaun.method import DepreciationMethod


class Asset(NamedTuple):
    basis: Decimal
    life: Decimal
    method: 'DepreciationMethod'
