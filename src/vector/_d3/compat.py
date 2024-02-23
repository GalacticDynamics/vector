"""Compatibility via :func:`plum.convert`."""

__all__: list[str] = []


import astropy.coordinates as apyc
import astropy.units as apyu
from plum import conversion_method

from .builtin import (
    Cartesian3DVector,
    CartesianDifferential3D,
    CylindricalDifferential,
    CylindricalVector,
    SphericalDifferential,
    SphericalVector,
)

#####################################################################
# Astropy


# =====================================
# Cartesian3DVector


@conversion_method(type_from=Cartesian3DVector, type_to=apyc.CartesianRepresentation)  # type: ignore[misc]
def cart3_to_apycart3(obj: Cartesian3DVector, /) -> apyc.CartesianRepresentation:
    """`vector.Cartesian3DVector` -> `astropy.CartesianRepresentation`."""
    return apyc.CartesianRepresentation(
        x=obj.x.as_type(apyu.Quantity),
        y=obj.y.as_type(apyu.Quantity),
        z=obj.z.as_type(apyu.Quantity),
    )


@conversion_method(type_from=apyc.CartesianRepresentation, type_to=Cartesian3DVector)  # type: ignore[misc]
def apycart3_to_cart3(obj: apyc.CartesianRepresentation, /) -> Cartesian3DVector:
    """`astropy.CartesianRepresentation` -> `vector.Cartesian3DVector`."""
    return Cartesian3DVector(x=obj.x, y=obj.y, z=obj.z)


# =====================================
# SphericalVector


@conversion_method(
    type_from=SphericalVector,
    type_to=apyc.PhysicsSphericalRepresentation,  # type: ignore[misc]
)
def sph_to_apysph(obj: SphericalVector, /) -> apyc.PhysicsSphericalRepresentation:
    """`vector.SphericalVector` -> `astropy.PhysicsSphericalRepresentation`."""
    return apyc.PhysicsSphericalRepresentation(
        r=obj.r.as_type(apyu.Quantity),
        phi=obj.phi.as_type(apyu.Quantity),
        theta=obj.theta.as_type(apyu.Quantity),
    )


@conversion_method(
    type_from=apyc.PhysicsSphericalRepresentation,
    type_to=SphericalVector,  # type: ignore[misc]
)
def apysph_to_sph(obj: apyc.PhysicsSphericalRepresentation, /) -> SphericalVector:
    """`astropy.PhysicsSphericalRepresentation` -> `vector.SphericalVector`."""
    return SphericalVector(r=obj.r, phi=obj.phi, theta=obj.theta)


# =====================================
# CylindricalVector


@conversion_method(type_from=CylindricalVector, type_to=apyc.CylindricalRepresentation)  # type: ignore[misc]
def cyl_to_apycyl(obj: CylindricalVector, /) -> apyc.CylindricalRepresentation:
    """`vector.CylindricalVector` -> `astropy.CylindricalRepresentation`."""
    return apyc.CylindricalRepresentation(
        rho=obj.rho.as_type(apyu.Quantity),
        phi=obj.phi.as_type(apyu.Quantity),
        z=obj.z.as_type(apyu.Quantity),
    )


@conversion_method(type_from=apyc.CylindricalRepresentation, type_to=CylindricalVector)  # type: ignore[misc]
def apycyl_to_cyl(obj: apyc.CylindricalRepresentation, /) -> CylindricalVector:
    """`astropy.CylindricalRepresentation` -> `vector.CylindricalVector`."""
    return CylindricalVector(rho=obj.rho, phi=obj.phi, z=obj.z)


# =====================================
# CartesianDifferential3D


@conversion_method(  # type: ignore[misc]
    type_from=CartesianDifferential3D, type_to=apyc.CartesianDifferential
)
def diffcart3_to_apycart3(
    obj: CartesianDifferential3D, /
) -> apyc.CartesianDifferential:
    """`vector.CartesianDifferential3D` -> `astropy.CartesianDifferential`."""
    return apyc.CartesianDifferential(
        d_x=obj.d_x.as_type(apyu.Quantity),
        d_y=obj.d_y.as_type(apyu.Quantity),
        d_z=obj.d_z.as_type(apyu.Quantity),
    )


@conversion_method(  # type: ignore[misc]
    type_from=apyc.CartesianDifferential, type_to=CartesianDifferential3D
)
def apycart3_to_diffcart3(
    obj: apyc.CartesianDifferential, /
) -> CartesianDifferential3D:
    """`astropy.CartesianDifferential` -> `vector.CartesianDifferential3D`."""
    return CartesianDifferential3D(d_x=obj.d_x, d_y=obj.d_y, d_z=obj.d_z)


# =====================================
# SphericalDifferential


@conversion_method(  # type: ignore[misc]
    type_from=SphericalDifferential,
    type_to=apyc.PhysicsSphericalDifferential,
)
def diffsph_to_apysph(
    obj: SphericalDifferential, /
) -> apyc.PhysicsSphericalDifferential:
    """`vector.SphericalDifferential` -> `astropy.PhysicsSphericalDifferential`."""
    return apyc.PhysicsSphericalDifferential(
        d_r=obj.d_r.as_type(apyu.Quantity),
        d_phi=obj.d_phi.as_type(apyu.Quantity),
        d_theta=obj.d_theta.as_type(apyu.Quantity),
    )


@conversion_method(  # type: ignore[misc]
    type_from=apyc.PhysicsSphericalDifferential,
    type_to=SphericalDifferential,
)
def apysph_to_diffsph(
    obj: apyc.PhysicsSphericalDifferential, /
) -> SphericalDifferential:
    """`astropy.PhysicsSphericalDifferential` -> `vector.SphericalDifferential`."""
    return SphericalDifferential(d_r=obj.d_r, d_phi=obj.d_phi, d_theta=obj.d_theta)


# =====================================
# CylindricalDifferential


@conversion_method(  # type: ignore[misc]
    type_from=CylindricalDifferential, type_to=apyc.CylindricalDifferential
)
def diffcyl_to_apycyl(obj: CylindricalDifferential, /) -> apyc.CylindricalDifferential:
    """`vector.CylindricalDifferential` -> `astropy.CylindricalDifferential`."""
    return apyc.CylindricalDifferential(
        d_rho=obj.d_rho.as_type(apyu.Quantity),
        d_phi=obj.d_phi.as_type(apyu.Quantity),
        d_z=obj.d_z.as_type(apyu.Quantity),
    )


@conversion_method(  # type: ignore[misc]
    type_from=apyc.CylindricalDifferential, type_to=CylindricalDifferential
)
def apycyl_to_diffcyl(obj: apyc.CylindricalDifferential, /) -> CylindricalDifferential:
    """`astropy.CylindricalDifferential` -> `vector.CylindricalDifferential`."""
    return CylindricalDifferential(d_rho=obj.d_rho, d_phi=obj.d_phi, d_z=obj.d_z)


#####################################################################
