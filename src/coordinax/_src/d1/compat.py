"""Intra-ecosystem Compatibility."""

__all__: list[str] = []


from typing import TypeAlias

from jaxtyping import Shaped
from plum import convert

from unxt import Quantity

from .cartesian import CartesianPosition1D
from coordinax._src.operators.base import AbstractOperator, op_call_dispatch
from coordinax._src.typing import TimeBatchOrScalar

Q1: TypeAlias = Shaped[Quantity["length"], "*#batch 1"]


@op_call_dispatch
def call(self: AbstractOperator, x: Q1, /) -> Q1:
    """Dispatch to the operator's `__call__` method."""
    return self(CartesianPosition1D.constructor(x))


@op_call_dispatch
def call(
    self: AbstractOperator, x: Q1, t: TimeBatchOrScalar, /
) -> tuple[Q1, TimeBatchOrScalar]:
    """Dispatch to the operator's `__call__` method."""
    vec, t = self(CartesianPosition1D.constructor(x), t)
    return convert(vec, Quantity), t
