# pylint: disable=duplicate-code
"""3-dimensional."""

__all__: list[str] = []

from jaxtyping import Shaped
from plum import convert

from jax_quantity import Quantity

from .spacetime import FourVector
from coordinax.operators._base import AbstractOperator, op_call_dispatch


@op_call_dispatch  # type: ignore[misc]
def call(
    self: AbstractOperator, x: Shaped[Quantity["length"], "*batch 4"], /
) -> Shaped[Quantity["length"], "*batch 4"]:
    """Dispatch to the operator's `__call__` method."""
    return convert(self(FourVector.constructor(x)), Quantity)