"""Built-in vector classes."""

__all__ = [
    # Position
    "Cartesian2DVector",
    "PolarVector",
    # "LnPolarVector",
    # "Log10PolarVector",
    # Differential
    "CartesianDifferential2D",
    "PolarDifferential",
]

from functools import partial
from typing import ClassVar, final

import array_api_jax_compat as xp
import equinox as eqx
import jax

from vector._checks import check_phi_range, check_r_non_negative
from vector._typing import (
    BatchableAngle,
    BatchableAngularSpeed,
    BatchableLength,
    BatchableSpeed,
)
from vector._utils import converter_quantity_array

from .base import Abstract2DVector, Abstract2DVectorDifferential

# =============================================================================
# 2D


@final
class Cartesian2DVector(Abstract2DVector):
    """Cartesian vector representation."""

    x: BatchableLength = eqx.field(converter=converter_quantity_array)
    r"""X coordinate :math:`x \in (-\infty,+\infty)`."""

    y: BatchableLength = eqx.field(converter=converter_quantity_array)
    r"""Y coordinate :math:`y \in (-\infty,+\infty)`."""

    @partial(jax.jit)
    def norm(self) -> BatchableLength:
        """Return the norm of the vector."""
        return xp.sqrt(self.x**2 + self.y**2)


@final
class PolarVector(Abstract2DVector):
    """Polar vector representation.

    We use the symbol `phi` instead of `theta` to adhere to the ISO standard.
    """

    r: BatchableLength = eqx.field(converter=converter_quantity_array)
    r"""Radial distance :math:`r \in [0,+\infty)`."""

    phi: BatchableAngle = eqx.field(converter=converter_quantity_array)
    r"""Polar angle :math:`\phi \in [0,2\pi)`."""

    def __check_init__(self) -> None:
        """Check the initialization."""
        check_r_non_negative(self.r)
        check_phi_range(self.phi)

    @partial(jax.jit)
    def norm(self) -> BatchableLength:
        """Return the norm of the vector."""
        return self.r


# class LnPolarVector(Abstract2DVector):
#     """Log-polar vector representation."""

#     lnr: BatchableFloatScalarQ = eqx.field(converter=converter_quantity_array)
#     theta: BatchableFloatScalarQ = eqx.field(converter=converter_quantity_array)


# class Log10PolarVector(Abstract2DVector):
#     """Log10-polar vector representation."""

#     log10r: BatchableFloatScalarQ = eqx.field(converter=converter_quantity_array)
#     theta: BatchableFloatScalarQ = eqx.field(converter=converter_quantity_array)


##############################################################################


@final
class CartesianDifferential2D(Abstract2DVectorDifferential):
    """Cartesian differential representation."""

    d_x: BatchableSpeed = eqx.field(converter=converter_quantity_array)
    r"""X coordinate differential :math:`\dot{x} \in (-\infty,+\infty)`."""

    d_y: BatchableSpeed = eqx.field(converter=converter_quantity_array)
    r"""Y coordinate differential :math:`\dot{y} \in (-\infty,+\infty)`."""

    vector_cls: ClassVar[type[Cartesian2DVector]] = Cartesian2DVector  # type: ignore[misc]

    @partial(jax.jit)
    def norm(self, _: Abstract2DVector | None = None, /) -> BatchableSpeed:
        """Return the norm of the vector."""
        return xp.sqrt(self.d_x**2 + self.d_y**2)


@final
class PolarDifferential(Abstract2DVectorDifferential):
    """Polar differential representation."""

    d_r: BatchableSpeed = eqx.field(converter=converter_quantity_array)
    r"""Radial speed :math:`dr/dt \in [-\infty,+\infty]`."""

    d_phi: BatchableAngularSpeed = eqx.field(converter=converter_quantity_array)
    r"""Polar angular speed :math:`d\phi/dt \in [-\infty,+\infty]`."""

    vector_cls: ClassVar[type[PolarVector]] = PolarVector  # type: ignore[misc]