from __future__ import annotations

from decimal import Decimal
from typing import Callable, NamedTuple, Tuple

from deprechaun.method import DepreciationMethod


class Asset(NamedTuple):
    basis: Decimal
    life: Decimal
    method: DepreciationMethod
