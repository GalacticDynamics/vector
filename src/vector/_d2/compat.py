"""Compatibility via :func:`plum.convert`."""

__all__: list[str] = []


import array_api_jax_compat as xp
from jax_quantity import Quantity
from plum import conversion_method

from vector._utils import dataclass_values, full_shaped

from .base import Abstract2DVector
from .builtin import Cartesian2DVector, CartesianDifferential2D

#####################################################################
# Quantity


@conversion_method(type_from=Abstract2DVector, type_to=Quantity)  # type: ignore[misc]
def vec_to_q(obj: Abstract2DVector, /) -> Quantity["length"]:
    """`vector.Abstract2DVector` -> `jax_quantity.Quantity`."""
    cart = full_shaped(obj.represent_as(Cartesian2DVector))
    return xp.stack(tuple(dataclass_values(cart)), axis=-1)


@conversion_method(type_from=CartesianDifferential2D, type_to=Quantity)  # type: ignore[misc]
def vec_diff_to_q(obj: CartesianDifferential2D, /) -> Quantity["speed"]:
    """`vector.CartesianDifferential2D` -> `jax_quantity.Quantity`."""
    return xp.stack(tuple(dataclass_values(full_shaped(obj))), axis=-1)