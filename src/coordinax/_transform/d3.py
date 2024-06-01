"""Transformations between representations."""

__all__ = ["represent_as"]

from typing import Any
from warnings import warn

from plum import dispatch

import quaxed.array_api as xp

from coordinax._d1.builtin import CartesianPosition1D, RadialPosition
from coordinax._d2.base import AbstractPosition2D
from coordinax._d2.builtin import CartesianPosition2D, PolarPosition
from coordinax._d3.builtin import CartesianPosition3D, CylindricalVector
from coordinax._d3.sphere import MathSphericalVector, SphericalVector
from coordinax._exceptions import IrreversibleDimensionChange

# =============================================================================
# CartesianPosition3D


# -----------------------------------------------
# 1D


@dispatch
def represent_as(
    current: CartesianPosition3D, target: type[CartesianPosition1D], /, **kwargs: Any
) -> CartesianPosition1D:
    """CartesianPosition3D -> CartesianPosition1D.

    The `y` and `z` coordinates are dropped.

    Examples
    --------
    >>> import warnings
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> x = cx.CartesianPosition3D.constructor(Quantity([1.0, 2.0, 3.0], "km"))

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("ignore")
    ...     x2 = cx.represent_as(x, cx.CartesianPosition1D)
    >>> x2
    CartesianPosition1D(
      x=Quantity[PhysicalType('length')](value=f32[], unit=Unit("km"))
    )

    """
    warn("irreversible dimension change", IrreversibleDimensionChange, stacklevel=2)
    return target(x=current.x)


@dispatch
def represent_as(
    current: CartesianPosition3D, target: type[RadialPosition], /, **kwargs: Any
) -> RadialPosition:
    """CartesianPosition3D -> RadialPosition.

    Examples
    --------
    >>> import warnings
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> x = cx.CartesianPosition3D.constructor(Quantity([1.0, 2.0, 3.0], "km"))

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("ignore")
    ...     x2 = cx.represent_as(x, cx.RadialPosition)
    >>> x2
    RadialPosition(r=Distance(value=f32[], unit=Unit("km")))

    """
    warn("irreversible dimension change", IrreversibleDimensionChange, stacklevel=2)
    return target(r=xp.sqrt(current.x**2 + current.y**2 + current.z**2))


# -----------------------------------------------
# 2D


@dispatch
def represent_as(
    current: CartesianPosition3D, target: type[CartesianPosition2D], /, **kwargs: Any
) -> CartesianPosition2D:
    """CartesianPosition3D -> CartesianPosition2D.

    Examples
    --------
    >>> import warnings
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> x = cx.CartesianPosition3D.constructor(Quantity([1.0, 2.0, 3.0], "km"))

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("ignore")
    ...     x2 = cx.represent_as(x, cx.CartesianPosition2D)
    >>> x2
    CartesianPosition2D( x=Quantity[...](value=f32[], unit=Unit("km")),
                       y=Quantity[...](value=f32[], unit=Unit("km")) )

    """
    warn("irreversible dimension change", IrreversibleDimensionChange, stacklevel=2)
    return target(x=current.x, y=current.y)


@dispatch.multi(
    (CartesianPosition3D, type[PolarPosition]),
)
def represent_as(
    current: CartesianPosition3D, target: type[AbstractPosition2D], /, **kwargs: Any
) -> AbstractPosition2D:
    """CartesianPosition3D -> Cartesian2D -> AbstractPosition2D.

    Examples
    --------
    >>> import warnings
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> x = cx.CartesianPosition3D.constructor(Quantity([1.0, 2.0, 3.0], "km"))

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("ignore")
    ...     x2 = cx.represent_as(x, cx.PolarPosition)
    >>> x2
    PolarPosition( r=Distance(value=f32[], unit=Unit("km")),
                 phi=Quantity[...](value=f32[], unit=Unit("rad")) )

    """
    warn("irreversible dimension change", IrreversibleDimensionChange, stacklevel=2)
    cart2 = represent_as(current, CartesianPosition2D)
    return represent_as(cart2, target)


# =============================================================================
# CylindricalVector


# -----------------------------------------------
# 1D


@dispatch
def represent_as(
    current: CylindricalVector, target: type[CartesianPosition1D], /, **kwargs: Any
) -> CartesianPosition1D:
    """CylindricalVector -> CartesianPosition1D.

    Examples
    --------
    >>> import warnings
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> x = cx.CylindricalVector(rho=Quantity(1.0, "km"), phi=Quantity(10.0, "deg"),
    ...                          z=Quantity(14, "km"))

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("ignore")
    ...     x2 = cx.represent_as(x, cx.CartesianPosition1D)
    >>> x2
    CartesianPosition1D( x=Quantity[...](value=f32[], unit=Unit("km")) )

    """
    warn("irreversible dimension change", IrreversibleDimensionChange, stacklevel=2)
    return target(x=current.rho * xp.cos(current.phi))


@dispatch
def represent_as(
    current: CylindricalVector, target: type[RadialPosition], /, **kwargs: Any
) -> RadialPosition:
    """CylindricalVector -> RadialPosition.

    Examples
    --------
    >>> import warnings
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> x = cx.CylindricalVector(rho=Quantity(1.0, "km"), phi=Quantity(10.0, "deg"),
    ...                          z=Quantity(14, "km"))

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("ignore")
    ...     x2 = cx.represent_as(x, cx.RadialPosition)
    >>> x2
    RadialPosition(r=Distance(value=f32[], unit=Unit("km")))

    """
    warn("irreversible dimension change", IrreversibleDimensionChange, stacklevel=2)
    return target(r=current.rho)


# -----------------------------------------------
# 2D


@dispatch
def represent_as(
    current: CylindricalVector, target: type[CartesianPosition2D], /, **kwargs: Any
) -> CartesianPosition2D:
    """CylindricalVector -> CartesianPosition2D.

    Examples
    --------
    >>> import warnings
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> x = cx.CylindricalVector(rho=Quantity(1.0, "km"), phi=Quantity(10.0, "deg"),
    ...                          z=Quantity(14, "km"))

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("ignore")
    ...     x2 = cx.represent_as(x, cx.CartesianPosition2D)
    >>> x2
    CartesianPosition2D( x=Quantity[...](value=f32[], unit=Unit("km")),
                       y=Quantity[...](value=f32[], unit=Unit("km")) )

    """
    warn("irreversible dimension change", IrreversibleDimensionChange, stacklevel=2)
    x = current.rho * xp.cos(current.phi)
    y = current.rho * xp.sin(current.phi)
    return target(x=x, y=y)


@dispatch
def represent_as(
    current: CylindricalVector, target: type[PolarPosition], /, **kwargs: Any
) -> PolarPosition:
    """CylindricalVector -> PolarPosition.

    Examples
    --------
    >>> import warnings
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> x = cx.CylindricalVector(rho=Quantity(1.0, "km"), phi=Quantity(10.0, "deg"),
    ...                          z=Quantity(14, "km"))

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("ignore")
    ...     x2 = cx.represent_as(x, cx.PolarPosition)
    >>> x2
    PolarPosition( r=Distance(value=f32[], unit=Unit("km")),
                 phi=Quantity[...](value=f32[], unit=Unit("deg")) )

    """
    warn("irreversible dimension change", IrreversibleDimensionChange, stacklevel=2)
    return target(r=current.rho, phi=current.phi)


# =============================================================================
# SphericalVector


# -----------------------------------------------
# 1D


@dispatch
def represent_as(
    current: SphericalVector, target: type[CartesianPosition1D], /, **kwargs: Any
) -> CartesianPosition1D:
    """SphericalVector -> CartesianPosition1D.

    Examples
    --------
    >>> import warnings
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> x = cx.SphericalVector(r=Quantity(1.0, "km"), theta=Quantity(14, "deg"),
    ...                        phi=Quantity(10.0, "deg"))

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("ignore")
    ...     x2 = cx.represent_as(x, cx.CartesianPosition1D)
    >>> x2
    CartesianPosition1D( x=Quantity[...](value=f32[], unit=Unit("km")) )

    """
    warn("irreversible dimension change", IrreversibleDimensionChange, stacklevel=2)
    return target(x=current.r * xp.sin(current.theta) * xp.cos(current.phi))


@dispatch
def represent_as(
    current: SphericalVector, target: type[RadialPosition], /, **kwargs: Any
) -> RadialPosition:
    """SphericalVector -> RadialPosition.

    Examples
    --------
    >>> import warnings
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> x = cx.SphericalVector(r=Quantity(1.0, "km"), theta=Quantity(14, "deg"),
    ...                        phi=Quantity(10.0, "deg"))

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("ignore")
    ...     x2 = cx.represent_as(x, cx.RadialPosition)
    >>> x2
    RadialPosition(r=Distance(value=f32[], unit=Unit("km")))

    """
    warn("irreversible dimension change", IrreversibleDimensionChange, stacklevel=2)
    return target(r=current.r)


# -----------------------------------------------
# 2D


@dispatch
def represent_as(
    current: SphericalVector, target: type[CartesianPosition2D], /, **kwargs: Any
) -> CartesianPosition2D:
    """SphericalVector -> CartesianPosition2D.

    Examples
    --------
    >>> import warnings
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> x = cx.SphericalVector(r=Quantity(1.0, "km"), theta=Quantity(14, "deg"),
    ...                        phi=Quantity(10.0, "deg"))

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("ignore")
    ...     x2 = cx.represent_as(x, cx.CartesianPosition2D)
    >>> x2
    CartesianPosition2D( x=Quantity[...](value=f32[], unit=Unit("km")),
                       y=Quantity[...](value=f32[], unit=Unit("km")) )

    """
    warn("irreversible dimension change", IrreversibleDimensionChange, stacklevel=2)
    x = current.r * xp.sin(current.theta) * xp.cos(current.phi)
    y = current.r * xp.sin(current.theta) * xp.sin(current.phi)
    return target(x=x, y=y)


@dispatch
def represent_as(
    current: SphericalVector, target: type[PolarPosition], /, **kwargs: Any
) -> PolarPosition:
    """SphericalVector -> PolarPosition.

    Examples
    --------
    >>> import warnings
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> x = cx.SphericalVector(r=Quantity(1.0, "km"), theta=Quantity(14, "deg"),
    ...                        phi=Quantity(10.0, "deg"))

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("ignore")
    ...     x2 = cx.represent_as(x, cx.PolarPosition)
    >>> x2
    PolarPosition( r=Distance(value=f32[], unit=Unit("km")),
                 phi=Quantity[...](value=f32[], unit=Unit("deg")) )

    """
    warn("irreversible dimension change", IrreversibleDimensionChange, stacklevel=2)
    return target(r=current.r * xp.sin(current.theta), phi=current.phi)


# =============================================================================
# MathSphericalVector


# -----------------------------------------------
# 1D


@dispatch
def represent_as(
    current: MathSphericalVector, target: type[CartesianPosition1D], /, **kwargs: Any
) -> CartesianPosition1D:
    """MathSphericalVector -> CartesianPosition1D.

    Examples
    --------
    >>> import warnings
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> x = cx.MathSphericalVector(r=Quantity(1.0, "km"), theta=Quantity(10.0, "deg"),
    ...                            phi=Quantity(14, "deg"))

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("ignore")
    ...     x2 = cx.represent_as(x, cx.CartesianPosition1D)
    >>> x2
    CartesianPosition1D( x=Quantity[...](value=f32[], unit=Unit("km")) )

    """
    warn("irreversible dimension change", IrreversibleDimensionChange, stacklevel=2)
    return target(x=current.r * xp.sin(current.phi) * xp.cos(current.theta))


@dispatch
def represent_as(
    current: MathSphericalVector, target: type[RadialPosition], /, **kwargs: Any
) -> RadialPosition:
    """MathSphericalVector -> RadialPosition.

    Examples
    --------
    >>> import warnings
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> x = cx.MathSphericalVector(r=Quantity(1.0, "km"), theta=Quantity(10.0, "deg"),
    ...                            phi=Quantity(14, "deg"))

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("ignore")
    ...     x2 = cx.represent_as(x, cx.RadialPosition)
    >>> x2
    RadialPosition(r=Distance(value=f32[], unit=Unit("km")))

    """
    warn("irreversible dimension change", IrreversibleDimensionChange, stacklevel=2)
    return target(r=current.r)


# -----------------------------------------------
# 2D


@dispatch
def represent_as(
    current: MathSphericalVector, target: type[CartesianPosition2D], /, **kwargs: Any
) -> CartesianPosition2D:
    """MathSphericalVector -> CartesianPosition2D.

    Examples
    --------
    >>> import warnings
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> x = cx.MathSphericalVector(r=Quantity(1.0, "km"), theta=Quantity(10.0, "deg"),
    ...                            phi=Quantity(14, "deg"))

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("ignore")
    ...     x2 = cx.represent_as(x, cx.CartesianPosition2D)
    >>> x2
    CartesianPosition2D( x=Quantity[...](value=f32[], unit=Unit("km")),
                       y=Quantity[...](value=f32[], unit=Unit("km")) )

    """
    warn("irreversible dimension change", IrreversibleDimensionChange, stacklevel=2)
    x = current.r * xp.sin(current.phi) * xp.cos(current.theta)
    y = current.r * xp.sin(current.phi) * xp.sin(current.theta)
    return target(x=x, y=y)


@dispatch
def represent_as(
    current: MathSphericalVector, target: type[PolarPosition], /, **kwargs: Any
) -> PolarPosition:
    """MathSphericalVector -> PolarPosition.

    Examples
    --------
    >>> import warnings
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> x = cx.MathSphericalVector(r=Quantity(1.0, "km"), theta=Quantity(10.0, "deg"),
    ...                            phi=Quantity(14, "deg"))

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter("ignore")
    ...     x2 = cx.represent_as(x, cx.PolarPosition)
    >>> x2
    PolarPosition( r=Distance(value=f32[], unit=Unit("km")),
                 phi=Quantity[...](value=f32[], unit=Unit("deg")) )

    """
    warn("irreversible dimension change", IrreversibleDimensionChange, stacklevel=2)
    return target(r=current.r * xp.sin(current.phi), phi=current.theta)
