"""Representation of coordinates in different systems."""

__all__: list[str] = []


import equinox as eqx

import quaxed.numpy as xp
import unxt as u
from unxt.quantity import AbstractQuantity

from coordinax._src.angle import Angle
from coordinax._src.typing import BatchableAngleQ

_0d = Angle(0, "rad")
_pid = Angle(180, "deg")
_2pid = Angle(360, "deg")


def check_r_non_negative(r: AbstractQuantity) -> AbstractQuantity:
    """Check that the radial distance is non-negative.

    Examples
    --------
    >>> import unxt as u

    Pass through the input if the radial distance is non-negative.

    >>> x = u.Quantity([0, 1, 2], "m")
    >>> check_r_non_negative(x)
    Quantity['length'](Array([0, 1, 2], dtype=int32), unit='m')

    Raise an error if the radial distance is negative.

    >>> x = u.Quantity([-1, 1, 2], "m")
    >>> try: check_r_non_negative(x)
    ... except Exception: pass

    """
    return check_non_negative(r, "radial distance")


def check_polar_range(
    polar: BatchableAngleQ,
    /,
    _l: Angle = _0d,
    _u: Angle = _pid,
) -> BatchableAngleQ:
    """Check that the polar angle is in the range.

    Examples
    --------
    >>> import unxt as u
    >>> from coordinax._src.vectors.checks import check_polar_range

    Pass through the input if it's in the range.

    >>> x = u.Quantity([0., 1, 2], "deg")
    >>> check_polar_range(x)
    Quantity['angle'](Array([0., 1., 2.], dtype=float32), unit='deg')

    Raise an error if anything is outside the range.

    >>> x = u.Quantity([0., 1, 2], "m")
    >>> try: check_polar_range(x)
    ... except Exception as e: print("wrong units")
    wrong units

    >>> x = u.Quantity([-1., 1, 2], "deg")
    >>> try: check_polar_range(x)
    ... except Exception: pass

    """
    polar = eqx.error_if(
        polar,
        not u.is_unit_convertible("deg", polar),
        "The polar angle must be in angular units.",
    )
    return eqx.error_if(
        polar,
        xp.any(xp.logical_or((polar < _l), (polar > _u))),
        "The inclination angle must be in the range [0, pi].",
    )


def check_non_negative(x: AbstractQuantity, /, name: str = "") -> AbstractQuantity:
    """Check that the input is non-negative.

    Examples
    --------
    >>> from unxt import Quantity

    Pass through the input if the value is non-negative.

    >>> x = Quantity([0, 1, 2], "m")
    >>> check_non_negative(x)
    Quantity['length'](Array([0, 1, 2], dtype=int32), unit='m')

    Raise an error if any value is negative.

    >>> x = Quantity([-1, 1, 2], "m")
    >>> try: check_non_negative(x)
    ... except Exception: pass

    """
    name = f" {name}" if name else name
    return eqx.error_if(x, xp.any(x < 0), "The input{name} must be non-negative.")


def check_less_than_equal(
    x: AbstractQuantity, max_val: AbstractQuantity, /, name: str = ""
) -> AbstractQuantity:
    """Check that the input value is less than or equal to the input maximum value.

    Examples
    --------
    >>> from unxt import Quantity

    Raise an error if the input is larger than the maximum value.

    >>> x = Quantity([-1, 1, 2], "m")
    >>> try: check_less_than(x, 1.5)
    ... except Exception: pass

    """
    name = f" {name}" if name else name
    msg = f"The input{name} must be less than or equal to the specified maximum value."
    return eqx.error_if(x, xp.any(x > max_val), msg)


def check_greater_than_equal(
    x: AbstractQuantity, min_val: AbstractQuantity, /, name: str = ""
) -> AbstractQuantity:
    """Check that the input value is greater than or equal to the input minimum value.

    Examples
    --------
    >>> from unxt import Quantity

    Raise an error if the input is smaller than the minimum value.

    >>> x = Quantity([-1, 1, 2], "m")
    >>> try: check_greater_than(x, 1.0)
    ... except Exception: pass

    """
    name = f" {name}" if name else name
    msg = (
        f"The input{name} must be greater than or equal to the specified minimum "
        "value."
    )
    return eqx.error_if(x, xp.any(x < min_val), msg)
