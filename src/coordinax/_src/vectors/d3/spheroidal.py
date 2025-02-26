"""Built-in vector classes."""

__all__ = ["ProlateSpheroidalAcc", "ProlateSpheroidalPos", "ProlateSpheroidalVel"]

from dataclasses import KW_ONLY
from typing import final

import equinox as eqx
from jaxtyping import Shaped

import quaxed.numpy as jnp
import unxt as u
from dataclassish.converters import Unless

import coordinax._src.custom_types as ct
from .base import AbstractAcc3D, AbstractPos3D, AbstractVel3D
from coordinax._src.angles import Angle, BatchableAngleQ
from coordinax._src.vectors import checks
from coordinax._src.vectors.base import VectorAttribute
from coordinax._src.vectors.converters import converter_azimuth_to_range


@final
class ProlateSpheroidalPos(AbstractPos3D):
    """Prolate spheroidal coordinates as defined by Dejonghe & de Zeeuw 1988.

    Note that valid coordinates have:
    - mu >= Delta^2
    - |nu| <= Delta^2
    - Delta > 0

    Parameters
    ----------
    mu
        The spheroidal mu coordinate. This is called `lambda` by Dejonghe & de Zeeuw.
    nu
        The spheroidal nu coordinate.
    phi
        Azimuthal angle [0, 360) [deg] where 0 is the x-axis.
    Delta
        The focal length of the coordinate system. Must be > 0.

    Examples
    --------
    >>> import unxt as u
    >>> import coordinax as cx

    >>> vec = cx.vecs.ProlateSpheroidalPos(
    ...     mu=u.Quantity(3.0, "km2"),
    ...     nu=u.Quantity(0.5, "km2"),
    ...     phi=u.Quantity(0.25, "rad"),
    ...     Delta=u.Quantity(1.5, "km"),
    ... )
    >>> vec
    ProlateSpheroidalPos(
      mu=Quantity[PhysicalType('area')](value=...f32[], unit=Unit("km2")),
      nu=Quantity[PhysicalType('area')](value=...f32[], unit=Unit("km2")),
      phi=Angle(value=...f32[], unit=Unit("rad")),
      Delta=Quantity[PhysicalType('length')](value=...f32[], unit=Unit("km"))
    )

    This fails with a zero or negative Delta:

    >>> try: vec = cx.vecs.ProlateSpheroidalPos(
    ...     mu=u.Quantity(3.0, "km2"),
    ...     nu=u.Quantity(0.5, "km2"),
    ...     phi=u.Quantity(0.25, "rad"),
    ...     Delta=u.Quantity(0.0, "km"),
    ... )
    ... except Exception as e: pass

    Or with invalid mu and nu:

    >>> try: vec = cx.vecs.ProlateSpheroidalPos(
    ...     mu=u.Quantity(0.5, "km2"),
    ...     nu=u.Quantity(0.5, "km2"),
    ...     phi=u.Quantity(0.25, "rad"),
    ...     Delta=u.Quantity(1.5, "km"),
    ... )
    ... except Exception as e: pass

    """

    mu: ct.BBtArea = eqx.field(converter=u.Quantity["area"].from_)
    r"""Spheroidal mu coordinate :math:`\mu \in [0,+\infty)` (called :math:`\lambda` in
     some Galactic dynamics contexts)."""

    nu: ct.BBtArea = eqx.field(converter=u.Quantity["area"].from_)
    r"""Spheroidal nu coordinate :math:`\lambda \in [-\infty,+\infty)`."""

    phi: BatchableAngleQ = eqx.field(
        converter=Unless(Angle, lambda x: converter_azimuth_to_range(Angle.from_(x)))
    )
    r"""Azimuthal angle, generally :math:`\phi \in [0,360)`."""

    _: KW_ONLY
    Delta: Shaped[u.Quantity["length"], ""] = VectorAttribute()
    """Focal length of the coordinate system."""

    def __check_init__(self) -> None:
        """Check the validity of the initialization."""
        checks.check_non_negative_non_zero(self.Delta, name="Delta")
        checks.check_greater_than_equal(
            self.mu, self.Delta**2, name="mu", comparison_name="Delta^2"
        )
        checks.check_less_than_equal(
            jnp.abs(self.nu), self.Delta**2, name="nu", comparison_name="Delta^2"
        )


@final
class ProlateSpheroidalVel(AbstractVel3D):
    """Prolate spheroidal differential representation."""

    mu: ct.BBtKinematicFlux = eqx.field(converter=u.Quantity["diffusivity"].from_)
    r"""Prolate spheroidal mu speed :math:`d\mu/dt \in [-\infty, \infty]."""

    nu: ct.BBtKinematicFlux = eqx.field(converter=u.Quantity["diffusivity"].from_)
    r"""Prolate spheroidal nu speed :math:`d\nu/dt \in [-\infty, \infty]."""

    phi: ct.BBtAngularSpeed = eqx.field(converter=u.Quantity["angular speed"].from_)
    r"""Azimuthal speed :math:`d\phi/dt \in [-\infty, \infty]."""


@final
class ProlateSpheroidalAcc(AbstractAcc3D):
    """Prolate spheroidal acceleration representation."""

    mu: ct.BBtSpecificEnergy = eqx.field(converter=u.Quantity["specific energy"].from_)
    r"""Prolate spheroidal mu acceleration :math:`d^2\mu/dt^2 \in [-\infty, \infty]."""

    nu: ct.BBtSpecificEnergy = eqx.field(converter=u.Quantity["specific energy"].from_)
    r"""Prolate spheroidal nu acceleration :math:`d^2\nu/dt^2 \in [-\infty, \infty]."""

    phi: ct.BBtAngularAcc = eqx.field(
        converter=u.Quantity["angular acceleration"].from_
    )
    r"""Azimuthal acceleration :math:`d^2\phi/dt^2 \in [-\infty, \infty]."""
