from __future__ import annotations

from decimal import Decimal
from typing import Callable, NamedTuple, Tuple


class Asset(NamedTuple):
    basis: Decimal
    life: Decimal
    method: Callable[[Asset], Tuple[Decimal, Asset]]
