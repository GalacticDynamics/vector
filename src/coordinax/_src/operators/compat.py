"""Intra-ecosystem Compatibility."""

__all__: list[str] = []


from typing import TypeAlias

from jaxtyping import Shaped
from plum import convert

import unxt as u

from .base import AbstractOperator
from coordinax._src.typing import TimeBatchOrScalar
from coordinax._src.vectors.d1 import CartesianPos1D
from coordinax._src.vectors.d2 import CartesianPos2D
from coordinax._src.vectors.d3 import CartesianPos3D
from coordinax._src.vectors.d4 import FourVector

# ============================================================================
# 1-Dimensional

Q1: TypeAlias = Shaped[u.Quantity["length"], "*#batch 1"]


@AbstractOperator.__call__.dispatch
def call(self: AbstractOperator, x: Q1, /) -> Q1:
    """Dispatch to the operator's `__call__` method.

    Examples
    --------
    >>> import unxt as u
    >>> import coordinax as cx

    >>> op = cx.ops.GalileanSpatialTranslation.from_([1], "kpc")
    >>> q = u.Quantity([0], "kpc")
    >>> op(q)
    Quantity['length'](Array([1.], dtype=float32), unit='kpc')

    """
    # Quantity -> CartesianPos1D -> [Operator] -> Quantity
    return convert(self(CartesianPos1D.from_(x)), u.Quantity)


@AbstractOperator.__call__.dispatch
def call(
    self: AbstractOperator, x: Q1, t: TimeBatchOrScalar, /
) -> tuple[Q1, TimeBatchOrScalar]:
    """Dispatch to the operator's `__call__` method.

    Examples
    --------
    >>> import unxt as u
    >>> import coordinax as cx

    >>> op = cx.ops.GalileanSpatialTranslation.from_([1], "kpc")
    >>> q = u.Quantity([0], "kpc")
    >>> op(q, u.Quantity(0, "s"))
    (Quantity['length'](Array([1.], dtype=float32), unit='kpc'),
     Quantity['time'](Array(0, dtype=int32, ...), unit='s'))

    """
    vec, t = self(CartesianPos1D.from_(x), t)
    return convert(vec, u.Quantity), t


# ============================================================================
# 2-Dimensional


Q2: TypeAlias = Shaped[u.Quantity["length"], "*#batch 2"]


@AbstractOperator.__call__.dispatch
def call(self: AbstractOperator, x: Q2, /) -> Q2:
    """Dispatch to the operator's `__call__` method.

    Examples
    --------
    >>> import unxt as u
    >>> import coordinax as cx

    >>> q = u.Quantity([1, 2], "m")
    >>> op = cx.ops.GalileanSpatialTranslation(u.Quantity([-1, -1], "m"))
    >>> op(q)
    Quantity['length'](Array([0., 1.], dtype=float32), unit='m')

    """
    return convert(self(CartesianPos2D.from_(x)), u.Quantity)


@AbstractOperator.__call__.dispatch
def call(
    self: AbstractOperator, x: Q2, t: TimeBatchOrScalar, /
) -> tuple[Q2, TimeBatchOrScalar]:
    """Dispatch to the operator's `__call__` method.

    Examples
    --------
    >>> import unxt as u
    >>> import coordinax as cx

    >>> q = u.Quantity([1, 2], "m")
    >>> op = cx.ops.GalileanSpatialTranslation(u.Quantity([-1, -1], "m"))
    >>> op(q, u.Quantity(0, "s"))
    (Quantity['length'](Array([0., 1.], dtype=float32), unit='m'),
     Quantity['time'](Array(0, dtype=int32, ...), unit='s'))

    """
    vec, t = self(CartesianPos2D.from_(x), t)
    return convert(vec, u.Quantity), t


# ============================================================================
# 3-Dimensional


Q3: TypeAlias = Shaped[u.Quantity["length"], "*#batch 3"]


@AbstractOperator.__call__.dispatch
def call(self: AbstractOperator, q: Q3, /) -> Q3:
    r"""Operate on a 3D Quantity.

    `q` is the position vector. This is interpreted as a 3D CartesianVector.
    See :class:`coordinax.CartesianPos3D` for more details.

    Returns
    -------
    x' : Quantity['length', '*#batch 3']
        The operated-upon position vector.

    Examples
    --------
    >>> import unxt as u
    >>> import coordinax as cx

    >>> shift = u.Quantity([1.0, 2.0, 3.0], "kpc")
    >>> op = cx.ops.GalileanSpatialTranslation(shift)

    >>> q = u.Quantity([0.0, 0, 0], "kpc")
    >>> op(q)
    Quantity['length'](Array([1., 2., 3.], dtype=float32), unit='kpc')

    """
    cart = CartesianPos3D.from_(q)
    result = self(cart)
    return convert(result.represent_as(CartesianPos3D), u.Quantity)


@AbstractOperator.__call__.dispatch
def call(
    self: AbstractOperator, x: Q3, t: TimeBatchOrScalar, /
) -> tuple[Q3, TimeBatchOrScalar]:
    """Dispatch to the operator's `__call__` method.

    Examples
    --------
    >>> import unxt as u
    >>> import coordinax as cx

    We can then create a spatial translation operator:

    >>> op = cx.ops.GalileanSpatialTranslation.from_([1, 2, 3], "kpc")
    >>> op
    GalileanSpatialTranslation(CartesianPos3D( ... ))

    We can then apply the operator to a position:

    >>> q = u.Quantity([1.0, 2.0, 3.0], "kpc")
    >>> t = u.Quantity(0.0, "Gyr")

    >>> op(q, t)
    (Quantity['length'](Array([2., 4., 6.], dtype=float32), unit='kpc'),
     Quantity['time'](Array(0., dtype=float32, ...), unit='Gyr'))

    """
    vec, t = self(CartesianPos3D.from_(x), t)
    return convert(vec, u.Quantity), t


# ============================================================================
# 4-Dimensional


@AbstractOperator.__call__.dispatch
def call(self: AbstractOperator, v4: FourVector, /) -> FourVector:
    """Dispatch to the operator's `__call__` method.

    Examples
    --------
    >>> import coordinax as cx

    We can then create a spatial translation operator:

    >>> op = cx.ops.GalileanSpatialTranslation.from_([1, 2, 3], "kpc")
    >>> op
    GalileanSpatialTranslation(CartesianPos3D( ... ))

    We can then apply the operator to a position:

    >>> pos = cx.FourVector.from_([0, 1.0, 2.0, 3.0], "kpc")
    >>> pos
    FourVector( t=Quantity[PhysicalType('time')](...), q=CartesianPos3D( ... ) )

    >>> newpos = op(pos)
    >>> newpos
    FourVector( t=Quantity[PhysicalType('time')](...), q=CartesianPos3D( ... ) )
    >>> newpos.q.x
    Quantity['length'](Array(2., dtype=float32), unit='kpc')

    """
    q, t = self(v4.q, v4.t)
    return FourVector(t=t, q=q)


@AbstractOperator.__call__.dispatch
def call(
    self: AbstractOperator, x: Shaped[u.Quantity["length"], "*batch 4"], /
) -> Shaped[u.Quantity["length"], "*batch 4"]:
    """Dispatch to the operator's `__call__` method.

    Examples
    --------
    >>> import unxt as u
    >>> import coordinax as cx

    We can then create a spatial translation operator:

    >>> op = cx.ops.GalileanSpatialTranslation.from_([1, 2, 3], "kpc")
    >>> op
    GalileanSpatialTranslation(CartesianPos3D( ... ))

    We can then apply the operator to a position:

    >>> pos = u.Quantity([0, 1.0, 2.0, 3.0], "kpc")
    >>> pos
    Quantity['length'](Array([0., 1., 2., 3.], dtype=float32), unit='kpc')

    >>> newpos = op(pos)
    >>> newpos
    Quantity['length'](Array([0., 2., 4., 6.], dtype=float32), unit='kpc')

    """
    return convert(self(FourVector.from_(x)), u.Quantity)