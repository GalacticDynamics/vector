"""Representation of coordinates in different systems."""

__all__: list[str] = []

from typing import Any

from plum import dispatch

from .base import AbstractPosition1D, AbstractVelocity1D
from .builtin import (
    Cartesian1DVector,
    CartesianDifferential1D,
    RadialDifferential,
    RadialVector,
)
from coordinax._base_pos import AbstractPosition

###############################################################################
# 1D


@dispatch(precedence=1)
def represent_as(
    current: Cartesian1DVector, target: type[Cartesian1DVector], /, **kwargs: Any
) -> Cartesian1DVector:
    """Self transform of 1D vectors."""
    return current


@dispatch(precedence=1)
def represent_as(
    current: RadialVector, target: type[RadialVector], /, **kwargs: Any
) -> RadialVector:
    """Self transform of 1D vectors."""
    return current


@dispatch
def represent_as(
    current: AbstractPosition1D, target: type[AbstractPosition1D], /, **kwargs: Any
) -> AbstractPosition1D:
    """AbstractPosition1D -> Cartesian1D -> AbstractPosition1D.

    This is the base case for the transformation of 1D vectors.
    """
    cart1d = represent_as(current, Cartesian1DVector)
    return represent_as(cart1d, target)


@dispatch.multi(
    (CartesianDifferential1D, type[CartesianDifferential1D], AbstractPosition),
    (RadialDifferential, type[RadialDifferential], AbstractPosition),
)
def represent_as(
    current: AbstractVelocity1D,
    target: type[AbstractVelocity1D],
    position: AbstractPosition,
    /,
    **kwargs: Any,
) -> AbstractVelocity1D:
    """Self transform of 1D Differentials."""
    return current


# =============================================================================
# Cartesian1DVector


@dispatch
def represent_as(
    current: Cartesian1DVector, target: type[RadialVector], /, **kwargs: Any
) -> RadialVector:
    """Cartesian1DVector -> RadialVector.

    The `x` coordinate is converted to the radial coordinate `r`.
    """
    return target(r=current.x)


# =============================================================================
# RadialVector


@dispatch
def represent_as(
    current: RadialVector, target: type[Cartesian1DVector], /, **kwargs: Any
) -> Cartesian1DVector:
    """RadialVector -> Cartesian1DVector.

    The `r` coordinate is converted to the `x` coordinate of the 1D system.
    """
    return target(x=current.r.distance)
