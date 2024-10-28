"""Representation of coordinates in different systems."""

__all__: list[str] = []


from .angle import Angle
from .typing import BatchableAngle, BatchableAngleQ

_2pid = Angle(360, "deg")


def converter_azimuth_to_range(
    phi: BatchableAngle | BatchableAngleQ,
) -> BatchableAngle | BatchableAngleQ:
    """Wrap the polar angle to the range [0, 2pi).

    It's safe to do this conversion since this is a phase cut, unlike `theta`,
    which is only on half the sphere.

    Examples
    --------
    >>> from unxt import Quantity
    >>> x = Quantity(370, "deg")
    >>> converter_azimuth_to_range(x)
    Quantity['angle'](Array(10, dtype=int32, ...), unit='deg')

    """
    return phi % _2pid
