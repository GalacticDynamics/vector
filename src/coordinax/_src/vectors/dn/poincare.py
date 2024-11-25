"""Poincare."""

__all__ = ["PoincarePolarVector"]

from functools import partial
from typing import final

import equinox as eqx
from jaxtyping import Shaped

from unxt import Quantity

import coordinax._src.typing as ct
from coordinax._src.utils import classproperty
from coordinax._src.vectors.base import AbstractPos, AbstractVel


@final
class PoincarePolarVector(AbstractPos):  # TODO: better name
    """Poincare vector + differential."""

    rho: ct.BatchableLength = eqx.field(
        converter=partial(Quantity["length"].from_, dtype=float)
    )
    r"""Cylindrical radial distance :math:`\rho \in [0,+\infty)`."""

    pp_phi: Shaped[Quantity, "*#batch"] = eqx.field()  # TODO: dimension annotation
    r"""Poincare phi-like variable."""

    z: ct.BatchableLength = eqx.field(
        converter=partial(Quantity["length"].from_, dtype=float)
    )
    r"""Height :math:`z \in (-\infty,+\infty)`."""

    d_rho: ct.BatchableSpeed = eqx.field(
        converter=partial(Quantity["speed"].from_, dtype=float)
    )
    r"""Cyindrical radial speed :math:`d\rho/dt \in [-\infty, \infty]."""

    d_pp_phi: Shaped[Quantity, "*#batch"] = eqx.field()  # TODO: dimension annotation
    r"""Poincare phi-like velocity variable."""

    d_z: ct.BatchableSpeed = eqx.field(
        converter=partial(Quantity["speed"].from_, dtype=float)
    )
    r"""Vertical speed :math:`dz/dt \in [-\infty, \infty]."""

    @classproperty
    @classmethod
    def _cartesian_cls(cls) -> type[AbstractPos]:
        """Return the corresponding Cartesian vector class."""
        raise NotImplementedError

    @classproperty
    @classmethod
    def differential_cls(cls) -> type[AbstractVel]:
        """Return the corresponding differential vector class."""
        raise NotImplementedError