"""Representation of coordinates in different systems."""

__all__: list[str] = []

from typing import Any

from plum import dispatch

import quaxed.array_api as xp

from .base import Abstract3DVector, Abstract3DVectorDifferential
from .builtin import (
    Cartesian3DVector,
    CartesianDifferential3D,
    CylindricalDifferential,
    CylindricalVector,
)
from .sphere import (
    MathSphericalDifferential,
    MathSphericalVector,
    SphericalDifferential,
    SphericalVector,
)
from coordinax._base_vec import AbstractVector

###############################################################################
# 3D


@dispatch
def represent_as(
    current: Abstract3DVector, target: type[Abstract3DVector], /, **kwargs: Any
) -> Abstract3DVector:
    """Abstract3DVector -> Cartesian3D -> Abstract3DVector."""
    return represent_as(represent_as(current, Cartesian3DVector), target)


@dispatch.multi(
    (Cartesian3DVector, type[Cartesian3DVector]),
    (CylindricalVector, type[CylindricalVector]),
    (SphericalVector, type[SphericalVector]),
    (MathSphericalVector, type[MathSphericalVector]),
)
def represent_as(
    current: Abstract3DVector, target: type[Abstract3DVector], /, **kwargs: Any
) -> Abstract3DVector:
    """Self transforms for 3D vectors.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    Cartesian to Cartesian:

    >>> vec = cx.Cartesian3DVector.constructor(Quantity([1, 2, 3], "kpc"))
    >>> cx.represent_as(vec, cx.Cartesian3DVector) is vec
    True

    Cylindrical to Cylindrical:

    >>> vec = cx.CylindricalVector(rho=Quantity(1, "kpc"), phi=Quantity(2, "deg"),
    ...                            z=Quantity(3, "kpc"))
    >>> cx.represent_as(vec, cx.CylindricalVector) is vec
    True

    Spherical to Spherical:

    >>> vec = cx.SphericalVector(r=Quantity(1, "kpc"), theta=Quantity(2, "deg"),
    ...                          phi=Quantity(3, "deg"))
    >>> cx.represent_as(vec, cx.SphericalVector) is vec
    True

    MathSpherical to MathSpherical:

    >>> vec = cx.MathSphericalVector(r=Quantity(1, "kpc"), phi=Quantity(2, "deg"),
    ...                              theta=Quantity(3, "deg"))
    >>> cx.represent_as(vec, cx.MathSphericalVector) is vec
    True

    """
    return current


@dispatch.multi(
    (CartesianDifferential3D, type[CartesianDifferential3D], AbstractVector),
    (CylindricalDifferential, type[CylindricalDifferential], AbstractVector),
    (SphericalDifferential, type[SphericalDifferential], AbstractVector),
    (MathSphericalDifferential, type[MathSphericalDifferential], AbstractVector),
)
def represent_as(
    current: Abstract3DVectorDifferential,
    target: type[Abstract3DVectorDifferential],
    position: AbstractVector,
    /,
    **kwargs: Any,
) -> Abstract3DVectorDifferential:
    """Self transforms for 3D differentials.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    For these transformations the position does not matter since the
    self-transform returns the differential unchanged.

    >>> vec = cx.Cartesian3DVector.constructor(Quantity([1, 2, 3], "kpc"))

    Cartesian to Cartesian Differential:

    >>> dif = cx.CartesianDifferential3D.constructor(Quantity([1, 2, 3], "km/s"))
    >>> cx.represent_as(dif, cx.CartesianDifferential3D, vec) is dif
    True

    >>> dif = cx.CylindricalDifferential(d_rho=Quantity(1, "km/s"),
    ...                                  d_phi=Quantity(2, "mas/yr"),
    ...                                  d_z=Quantity(3, "km/s"))
    >>> cx.represent_as(dif, cx.CylindricalDifferential, vec) is dif
    True

    >>> dif = cx.SphericalDifferential(d_r=Quantity(1, "km/s"),
    ...                                d_phi=Quantity(2, "mas/yr"),
    ...                                d_theta=Quantity(3, "mas/yr"))
    >>> cx.represent_as(dif, cx.SphericalDifferential, vec) is dif
    True

    >>> dif = cx.MathSphericalDifferential(d_r=Quantity(1, "km/s"),
    ...                                    d_theta=Quantity(2, "mas/yr"),
    ...                                    d_phi=Quantity(3, "mas/yr"))
    >>> cx.represent_as(dif, cx.MathSphericalDifferential, vec) is dif
    True

    """
    return current


# =============================================================================
# Cartesian3DVector


@dispatch
def represent_as(
    current: Cartesian3DVector, target: type[CylindricalVector], /, **kwargs: Any
) -> CylindricalVector:
    """Cartesian3DVector -> CylindricalVector.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> vec = cx.Cartesian3DVector.constructor(Quantity([1, 2, 3], "km"))
    >>> print(cx.represent_as(vec, cx.CylindricalVector))
    <CylindricalVector (rho[km], phi[rad], z[km])
        [2.236 1.107 3.   ]>

    """
    rho = xp.sqrt(current.x**2 + current.y**2)
    phi = xp.atan2(current.y, current.x)
    return target(rho=rho, phi=phi, z=current.z)


@dispatch
def represent_as(
    current: Cartesian3DVector, target: type[SphericalVector], /, **kwargs: Any
) -> SphericalVector:
    """Cartesian3DVector -> SphericalVector.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> vec = cx.Cartesian3DVector.constructor(Quantity([1, 2, 3], "km"))
    >>> print(cx.represent_as(vec, cx.SphericalVector))
    <SphericalVector (r[km], phi[rad], theta[rad])
        [3.742 1.107 0.641]>

    """
    r = xp.sqrt(current.x**2 + current.y**2 + current.z**2)
    phi = xp.atan2(current.y, current.x)
    theta = xp.acos(current.z / r)
    return target(r=r, phi=phi, theta=theta)


@dispatch
def represent_as(
    current: Cartesian3DVector, target: type[MathSphericalVector], /, **kwargs: Any
) -> MathSphericalVector:
    """Cartesian3DVector -> MathSphericalVector.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> vec = cx.Cartesian3DVector.constructor(Quantity([1, 2, 3], "km"))
    >>> print(cx.represent_as(vec, cx.MathSphericalVector))
    <MathSphericalVector (r[km], theta[rad], phi[rad])
        [3.742 1.107 0.641]>

    """
    r = xp.sqrt(current.x**2 + current.y**2 + current.z**2)
    theta = xp.atan2(current.y, current.x)
    phi = xp.acos(current.z / r)
    return target(r=r, theta=theta, phi=phi)


# =============================================================================
# CylindricalVector


@dispatch
def represent_as(
    current: CylindricalVector, target: type[Cartesian3DVector], /, **kwargs: Any
) -> Cartesian3DVector:
    """CylindricalVector -> Cartesian3DVector.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> vec = cx.CylindricalVector(rho=Quantity(1., "kpc"), phi=Quantity(90, "deg"),
    ...                            z=Quantity(1, "kpc"))
    >>> print(cx.represent_as(vec, cx.Cartesian3DVector))
    <Cartesian3DVector (x[kpc], y[kpc], z[kpc])
        [-4.371e-08  1.000e+00  1.000e+00]>

    """
    x = current.rho * xp.cos(current.phi)
    y = current.rho * xp.sin(current.phi)
    z = current.z
    return target(x=x, y=y, z=z)


@dispatch
def represent_as(
    current: CylindricalVector, target: type[SphericalVector], /, **kwargs: Any
) -> SphericalVector:
    """CylindricalVector -> SphericalVector.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> vec = cx.CylindricalVector(rho=Quantity(1., "kpc"), phi=Quantity(90, "deg"),
    ...                            z=Quantity(1, "kpc"))
    >>> print(cx.represent_as(vec, cx.SphericalVector))
    <SphericalVector (r[kpc], phi[deg], theta[rad])
        [ 1.414 90.     0.785]>

    """
    r = xp.sqrt(current.rho**2 + current.z**2)
    theta = xp.acos(current.z / r)
    phi = current.phi
    return target(r=r, phi=phi, theta=theta)


@dispatch
def represent_as(
    current: CylindricalVector, target: type[MathSphericalVector], /, **kwargs: Any
) -> MathSphericalVector:
    """CylindricalVector -> MathSphericalVector.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> vec = cx.CylindricalVector(rho=Quantity(1., "kpc"), phi=Quantity(90, "deg"),
    ...                            z=Quantity(1, "kpc"))
    >>> print(cx.represent_as(vec, cx.MathSphericalVector))
    <MathSphericalVector (r[kpc], theta[deg], phi[rad])
        [ 1.414 90.     0.785]>

    """
    r = xp.sqrt(current.rho**2 + current.z**2)
    theta = current.phi
    phi = xp.acos(current.z / r)
    return target(r=r, theta=theta, phi=phi)


# =============================================================================
# SphericalVector


@dispatch
def represent_as(
    current: SphericalVector, target: type[Cartesian3DVector], /, **kwargs: Any
) -> Cartesian3DVector:
    """SphericalVector -> Cartesian3DVector.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> vec = cx.SphericalVector(r=Quantity(1., "kpc"), phi=Quantity(90, "deg"),
    ...                          theta=Quantity(90, "deg"))
    >>> print(cx.represent_as(vec, cx.Cartesian3DVector))
    <Cartesian3DVector (x[kpc], y[kpc], z[kpc])
        [-4.371e-08  1.000e+00 -4.371e-08]>

    """
    x = current.r * xp.sin(current.theta) * xp.cos(current.phi)
    y = current.r * xp.sin(current.theta) * xp.sin(current.phi)
    z = current.r * xp.cos(current.theta)
    return target(x=x, y=y, z=z)


@dispatch
def represent_as(
    current: SphericalVector, target: type[CylindricalVector], /, **kwargs: Any
) -> CylindricalVector:
    """SphericalVector -> CylindricalVector.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> vec = cx.SphericalVector(r=Quantity(1., "kpc"), phi=Quantity(90, "deg"),
    ...                          theta=Quantity(90, "deg"))
    >>> print(cx.represent_as(vec, cx.CylindricalVector))
    <CylindricalVector (rho[kpc], phi[deg], z[kpc])
        [ 1.000e+00  9.000e+01 -4.371e-08]>

    """
    rho = xp.abs(current.r * xp.sin(current.theta))
    phi = current.phi
    z = current.r * xp.cos(current.theta)
    return target(rho=rho, phi=phi, z=z)


@dispatch
def represent_as(
    current: SphericalVector, target: type[MathSphericalVector], /, **kwargs: Any
) -> MathSphericalVector:
    """SphericalVector -> MathSphericalVector.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> vec = cx.SphericalVector(r=Quantity(1., "kpc"), phi=Quantity(90, "deg"),
    ...                          theta=Quantity(90, "deg"))
    >>> print(cx.represent_as(vec, cx.MathSphericalVector))
    <MathSphericalVector (r[kpc], theta[deg], phi[deg])
        [ 1. 90. 90.]>

    """
    return target(r=current.r, theta=current.phi, phi=current.theta)


# =============================================================================
# MathSphericalVector


@dispatch
def represent_as(
    current: MathSphericalVector, target: type[Cartesian3DVector], /, **kwargs: Any
) -> Cartesian3DVector:
    """MathSphericalVector -> Cartesian3DVector.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> vec = cx.MathSphericalVector(r=Quantity(1., "kpc"), theta=Quantity(90, "deg"),
    ...                              phi=Quantity(90, "deg"))
    >>> print(cx.represent_as(vec, cx.Cartesian3DVector))
    <Cartesian3DVector (x[kpc], y[kpc], z[kpc])
        [-4.371e-08  1.000e+00 -4.371e-08]>

    """
    x = current.r * xp.sin(current.phi) * xp.cos(current.theta)
    y = current.r * xp.sin(current.phi) * xp.sin(current.theta)
    z = current.r * xp.cos(current.phi)
    return target(x=x, y=y, z=z)


@dispatch
def represent_as(
    current: MathSphericalVector, target: type[CylindricalVector], /, **kwargs: Any
) -> CylindricalVector:
    """MathSphericalVector -> CylindricalVector.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> vec = cx.MathSphericalVector(r=Quantity(1., "kpc"), theta=Quantity(90, "deg"),
    ...                              phi=Quantity(90, "deg"))
    >>> print(cx.represent_as(vec, cx.CylindricalVector))
    <CylindricalVector (rho[kpc], phi[deg], z[kpc])
        [ 1.000e+00  9.000e+01 -4.371e-08]>

    """
    rho = xp.abs(current.r * xp.sin(current.phi))
    phi = current.theta
    z = current.r * xp.cos(current.phi)
    return target(rho=rho, phi=phi, z=z)


@dispatch
def represent_as(
    current: MathSphericalVector, target: type[SphericalVector], /, **kwargs: Any
) -> SphericalVector:
    """MathSphericalVector -> SphericalVector.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> vec = cx.MathSphericalVector(r=Quantity(1., "kpc"), theta=Quantity(90, "deg"),
    ...                              phi=Quantity(90, "deg"))
    >>> print(cx.represent_as(vec, cx.SphericalVector))
    <SphericalVector (r[kpc], phi[deg], theta[deg])
        [ 1. 90. 90.]>

    """
    return target(r=current.r, theta=current.phi, phi=current.theta)
