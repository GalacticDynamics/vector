"""Built-in vector classes."""

__all__ = ["ProlateSpheroidalAcc", "ProlateSpheroidalPos", "ProlateSpheroidalVel"]

from dataclasses import KW_ONLY
from functools import partial
from typing import final

import equinox as eqx
from jaxtyping import Shaped

import quaxed.numpy as xp
from dataclassish.converters import Unless
from unxt import Quantity

import coordinax._src.typing as ct
from .base import AbstractAcc3D, AbstractPos3D, AbstractVel3D
from coordinax._src.angle import Angle
from coordinax._src.distance import AbstractDistance, Distance
from coordinax._src.utils import classproperty
from coordinax._src.vectors.base import VectorAttribute
from coordinax._src.vectors.checks import (
    check_greater_than_equal,
    check_less_than_equal,
    check_r_non_negative,
)
from coordinax._src.vectors.converters import converter_azimuth_to_range


@final
class ProlateSpheroidalPos(AbstractPos3D):
    """Prolate spheroidal coordinates as defined by Dejonghe & de Zeeuw 1988.

    Parameters
    ----------
    mu : `coordinax.distance.Distance`
        The spheroidal mu coordinate. This is called `lambda` by Dejonghe & de Zeeuw.
    nu : `coordinax.distance.Distance`
        The spheroidal nu coordinate.
    phi : `coordinax.angle.Angle`
        Azimuthal angle [0, 360) [deg] where 0 is the x-axis.
    Delta : `coordinax.distance.Distance`
        The focal length of the coordinate system.

    """

    mu: ct.BatchableArea = eqx.field(
        converter=partial(Quantity["area"].from_, dtype=float)
    )
    r"""Spheroidal mu coordinate :math:`\mu \in [0,+\infty)` (called :math:`\lambda` in
     some Galactic dynamics contexts)."""

    nu: ct.BatchableArea = eqx.field(
        converter=partial(Quantity["area"].from_, dtype=float)
    )
    r"""Spheroidal nu coordinate :math:`\lambda \in [-\infty,+\infty)`."""

    phi: ct.BatchableAngle = eqx.field(
        converter=Unless(
            Angle, lambda x: converter_azimuth_to_range(Angle.from_(x, dtype=float))
        )
    )
    r"""Azimuthal angle, generally :math:`\phi \in [0,360)`."""

    _: KW_ONLY
    Delta: Shaped[Quantity["length"], ""] = eqx.field(
        default=VectorAttribute(
            converter=Unless(AbstractDistance, partial(Distance.from_, dtype=float))
        ),
        repr=False,
    )
    """Focal length of the coordinate system."""

    def __check_init__(self) -> None:
        """Check the validity of the initialization."""
        check_r_non_negative(self.mu)
        check_greater_than_equal(self.mu, self.Delta**2)
        check_less_than_equal(xp.abs(self.nu), self.Delta**2)

    @classproperty
    @classmethod
    def differential_cls(cls) -> type["ProlateSpheroidalVel"]:
        return ProlateSpheroidalVel


@final
class ProlateSpheroidalVel(AbstractVel3D):
    """Prolate spheroidal differential representation."""

    d_mu: ct.BatchableDiffusivity = eqx.field(
        converter=partial(Quantity["diffusivity"].from_, dtype=float)
    )
    r"""Prolate spheroidal mu speed :math:`d\mu/dt \in [-\infty, \infty]."""

    d_nu: ct.BatchableDiffusivity = eqx.field(
        converter=partial(Quantity["diffusivity"].from_, dtype=float)
    )
    r"""Prolate spheroidal nu speed :math:`d\nu/dt \in [-\infty, \infty]."""

    d_phi: ct.BatchableAngularSpeed = eqx.field(
        converter=partial(Quantity["angular speed"].from_, dtype=float)
    )
    r"""Azimuthal speed :math:`d\phi/dt \in [-\infty, \infty]."""

    @classproperty
    @classmethod
    def integral_cls(cls) -> type[ProlateSpheroidalPos]:
        return ProlateSpheroidalPos

    @classproperty
    @classmethod
    def differential_cls(cls) -> type["ProlateSpheroidalAcc"]:
        return ProlateSpheroidalAcc


@final
class ProlateSpheroidalAcc(AbstractAcc3D):
    """Prolate spheroidal acceleration representation."""

    d2_mu: ct.BatchableSpecificEnergy = eqx.field(
        converter=partial(Quantity["specific energy"].from_, dtype=float)
    )
    r"""Prolate spheroidal mu acceleration :math:`d^2\mu/dt^2 \in [-\infty, \infty]."""

    d2_nu: ct.BatchableSpecificEnergy = eqx.field(
        converter=partial(Quantity["specific energy"].from_, dtype=float)
    )
    r"""Prolate spheroidal nu acceleration :math:`d^2\nu/dt^2 \in [-\infty, \infty]."""

    d2_phi: ct.BatchableAngularAcc = eqx.field(
        converter=partial(Quantity["angular acceleration"].from_, dtype=float)
    )
    r"""Azimuthal acceleration :math:`d^2\phi/dt^2 \in [-\infty, \infty]."""

    @classproperty
    @classmethod
    def integral_cls(cls) -> type[ProlateSpheroidalVel]:
        return ProlateSpheroidalVel
