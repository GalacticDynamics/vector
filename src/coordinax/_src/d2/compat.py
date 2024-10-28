"""Intra-ecosystem Compatibility."""

__all__: list[str] = []


from typing import TypeAlias

from jaxtyping import Shaped
from plum import convert

from unxt import Quantity

from .cartesian import CartesianPos2D
from coordinax._src.operators.base import AbstractOperator, op_call_dispatch
from coordinax._src.typing import TimeBatchOrScalar

Q2: TypeAlias = Shaped[Quantity["length"], "*#batch 2"]


@op_call_dispatch
def call(self: AbstractOperator, x: Q2, /) -> Q2:
    """Dispatch to the operator's `__call__` method.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax.operators as cxo

    >>> q = Quantity([1, 2], "m")
    >>> op = cxo.GalileanSpatialTranslationOperator(Quantity([-1, -1], "m"))
    >>> op(q)
    Quantity['length'](Array([0., 1.], dtype=float32), unit='m')

    """
    return convert(self(CartesianPos2D.from_(x)), Quantity)


@op_call_dispatch
def call(
    self: AbstractOperator, x: Q2, t: TimeBatchOrScalar, /
) -> tuple[Q2, TimeBatchOrScalar]:
    """Dispatch to the operator's `__call__` method."""
    vec, t = self(CartesianPos2D.from_(x), t)
    return convert(vec, Quantity), t
