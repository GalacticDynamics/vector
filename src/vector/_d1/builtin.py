"""Carteisan vector."""

__all__ = [
    # Position
    "Cartesian1DVector",
    "RadialVector",
    # Differential
    "CartesianDifferential1D",
    "RadialDifferential",
]

from dataclasses import replace
from functools import partial
from typing import Any, ClassVar, final

import equinox as eqx
import jax

import array_api_jax_compat as xp
from jax_quantity import Quantity

from .base import Abstract1DVector, Abstract1DVectorDifferential
from vector._base import AbstractVector
from vector._checks import check_r_non_negative
from vector._typing import BatchableLength, BatchableSpeed

##############################################################################
# Position


@final
class Cartesian1DVector(Abstract1DVector):
    """Cartesian vector representation."""

    x: BatchableLength = eqx.field(
        converter=partial(Quantity["length"].constructor, dtype=float)
    )
    r"""X coordinate :math:`x \in (-\infty,+\infty)`."""

    def __add__(self, other: Any, /) -> "Cartesian1DVector":
        """Add two vectors."""
        if not isinstance(other, AbstractVector):
            msg = f"Cannot add {Cartesian1DVector!r} and {type(other)!r}."
            raise TypeError(msg)

        cart = other.represent_as(Cartesian1DVector)
        return replace(self, x=self.x + cart.x)

    def __sub__(self, other: Any, /) -> "Cartesian1DVector":
        """Subtract two vectors."""
        if not isinstance(other, AbstractVector):
            msg = f"Cannot subtract {Cartesian1DVector!r} and {type(other)!r}."
            raise TypeError(msg)

        cart = other.represent_as(Cartesian1DVector)
        return replace(self, x=self.x - cart.x)

    @partial(jax.jit)
    def norm(self) -> BatchableLength:
        """Return the norm of the vector."""
        return xp.abs(self.x)


@final
class RadialVector(Abstract1DVector):
    """Radial vector representation."""

    r: BatchableLength = eqx.field(
        converter=partial(Quantity["length"].constructor, dtype=float)
    )
    r"""Radial distance :math:`r \in [0,+\infty)`."""

    def __check_init__(self) -> None:
        """Check the initialization."""
        check_r_non_negative(self.r)


##############################################################################
# Velocity


@final
class CartesianDifferential1D(Abstract1DVectorDifferential):
    """Cartesian differential representation."""

    d_x: BatchableSpeed = eqx.field(converter=Quantity["speed"].constructor)
    r"""X differential :math:`dx/dt \in (-\infty,+\infty`)`."""

    vector_cls: ClassVar[type[Cartesian1DVector]] = Cartesian1DVector  # type: ignore[misc]

    @partial(jax.jit)
    def norm(self, _: Abstract1DVector | None = None, /) -> BatchableSpeed:
        """Return the norm of the vector."""
        return xp.abs(self.d_x)


@final
class RadialDifferential(Abstract1DVectorDifferential):
    """Radial differential representation."""

    d_r: BatchableSpeed = eqx.field(converter=Quantity["speed"].constructor)
    r"""Radial speed :math:`dr/dt \in (-\infty,+\infty)`."""

    vector_cls: ClassVar[type[RadialVector]] = RadialVector  # type: ignore[misc]
