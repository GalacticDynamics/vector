"""Built-in vector classes."""

__all__ = ["CartesianPosND", "CartesianVelocityND", "CartesianAccelerationND"]

from dataclasses import replace
from functools import partial
from typing import NoReturn, final
from typing_extensions import override

import equinox as eqx
import jax
from jaxtyping import ArrayLike, Shaped
from plum import conversion_method
from quax import register

import quaxed.lax as qlax
import quaxed.numpy as jnp
from unxt import Quantity

import coordinax._src.typing as ct
from .base import AbstractAccelerationND, AbstractPosND, AbstractVelocityND
from coordinax._src.base import AbstractPos
from coordinax._src.base.mixins import AvalMixin
from coordinax._src.utils import classproperty

##############################################################################
# Pos


@final
class CartesianPosND(AbstractPosND):
    """N-dimensional Cartesian vector representation.

    Examples
    --------
    >>> import coordinax as cx
    >>> from unxt import Quantity

    A 1D vector:

    >>> q = cx.CartesianPosND(Quantity([[1]], "kpc"))
    >>> q.q
    Quantity['length'](Array([[1.]], dtype=float32), unit='kpc')
    >>> q.shape
    (1,)

    A 2D vector:

    >>> q = cx.CartesianPosND(Quantity([1, 2], "kpc"))
    >>> q.q
    Quantity['length'](Array([1., 2.], dtype=float32), unit='kpc')
    >>> q.shape
    ()

    A 3D vector:

    >>> q = cx.CartesianPosND(Quantity([1, 2, 3], "kpc"))
    >>> q.q
    Quantity['length'](Array([1., 2., 3.], dtype=float32), unit='kpc')
    >>> q.shape
    ()

    A 4D vector:

    >>> q = cx.CartesianPosND(Quantity([1, 2, 3, 4], "kpc"))
    >>> q.q
    Quantity['length'](Array([1., 2., 3., 4.], dtype=float32), unit='kpc')
    >>> q.shape
    ()

    A 5D vector:

    >>> q = cx.CartesianPosND(Quantity([1, 2, 3, 4, 5], "kpc"))
    >>> q.q
    Quantity['length'](Array([1., 2., 3., 4., 5.], dtype=float32), unit='kpc')
    >>> q.shape
    ()

    """

    q: ct.BatchableLength = eqx.field(
        converter=partial(Quantity["length"].from_, dtype=float)
    )
    r"""N-D coordinate :math:`\vec{x} \in (-\infty,+\infty)`.

    Should have shape (*batch, F) where F is the number of features /
    dimensions. Arbitrary batch shapes are supported.
    """

    @override
    @classproperty
    @classmethod
    def differential_cls(cls) -> type["CartesianVelocityND"]:  # type: ignore[override]
        return CartesianVelocityND

    # -----------------------------------------------------
    # Unary operations

    __neg__ = jnp.negative

    # -----------------------------------------------------

    @partial(eqx.filter_jit, inline=True)
    def norm(self) -> ct.BatchableLength:
        """Return the norm of the vector.

        Examples
        --------
        >>> from unxt import Quantity
        >>> import coordinax as cx

        A 3D vector:

        >>> q = cx.CartesianPosND(Quantity([1, 2, 3], "kpc"))
        >>> q.norm()
        Quantity['length'](Array(3.7416575, dtype=float32), unit='kpc')

        """
        return jnp.linalg.vector_norm(self.q, axis=-1)


# -------------------------------------------------------------------


# TODO: move to the class in py3.11+
@CartesianPosND.from_._f.dispatch  # type: ignore[attr-defined,misc]  # noqa: SLF001
def from_(
    cls: type[CartesianPosND],
    x: Shaped[Quantity["length"], ""] | Shaped[Quantity["length"], "*batch N"],
    /,
) -> CartesianPosND:
    """Construct an N-dimensional position.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    1D vector:

    >>> cx.CartesianPosND.from_(Quantity(1, "kpc"))
    CartesianPosND(
      q=Quantity[...](value=f32[1], unit=Unit("kpc"))
    )

    >>> cx.CartesianPosND.from_(Quantity([1], "kpc"))
    CartesianPosND(
      q=Quantity[...](value=f32[1], unit=Unit("kpc"))
    )

    2D vector:

    >>> cx.CartesianPosND.from_(Quantity([1, 2], "kpc"))
    CartesianPosND(
      q=Quantity[...](value=f32[2], unit=Unit("kpc"))
    )

    3D vector:

    >>> cx.CartesianPosND.from_(Quantity([1, 2, 3], "kpc"))
    CartesianPosND(
      q=Quantity[...](value=f32[3], unit=Unit("kpc"))
    )

    4D vector:

    >>> cx.CartesianPosND.from_(Quantity([1, 2, 3, 4], "kpc"))
    CartesianPosND(
      q=Quantity[...](value=f32[4], unit=Unit("kpc"))
    )

    """
    return cls(jnp.atleast_1d(x))


@conversion_method(CartesianPosND, Quantity)  # type: ignore[misc]
def _vec_to_q(obj: CartesianPosND, /) -> Shaped[Quantity["length"], "*batch N"]:
    """`coordinax.AbstractPos3D` -> `unxt.Quantity`.

    Examples
    --------
    >>> import coordinax as cx
    >>> from plum import convert
    >>> from unxt import Quantity

    >>> vec = cx.CartesianPosND(Quantity([1, 2, 3, 4, 5], unit="kpc"))
    >>> convert(vec, Quantity)
    Quantity['length'](Array([1., 2., 3., 4., 5.], dtype=float32), unit='kpc')

    """
    return obj.q


@register(jax.lax.add_p)  # type: ignore[misc]
def _add_vcnd(lhs: CartesianPosND, rhs: AbstractPos, /) -> CartesianPosND:
    """Add two vectors.

    Examples
    --------
    >>> import coordinax as cx

    A 3D vector:

    >>> q1 = cx.CartesianPosND.from_([1, 2, 3], "kpc")
    >>> q2 = cx.CartesianPosND.from_([2, 3, 4], "kpc")
    >>> (q1 + q2).q
    Quantity['length'](Array([3., 5., 7.], dtype=float32), unit='kpc')

    """
    cart = rhs.represent_as(CartesianPosND)
    return replace(lhs, q=lhs.q + cart.q)


@register(jax.lax.mul_p)  # type: ignore[misc]
def _mul_vcnd(lhs: ArrayLike, rhs: CartesianPosND, /) -> CartesianPosND:
    """Scale a position by a scalar.

    Examples
    --------
    >>> import quaxed.numpy as jnp
    >>> from unxt import Quantity
    >>> import coordinax as cx

    >>> v = cx.CartesianPosND(Quantity([1, 2, 3, 4, 5], "kpc"))
    >>> jnp.multiply(2, v).q
    Quantity['length'](Array([ 2.,  4.,  6.,  8., 10.], dtype=float32), unit='kpc')

    """
    # Validation
    lhs = eqx.error_if(
        lhs, any(jax.numpy.shape(lhs)), f"must be a scalar, not {type(lhs)}"
    )

    # Scale the components
    return replace(rhs, q=lhs * rhs.q)


@register(jax.lax.neg_p)  # type: ignore[misc]
def _neg_p_cartnd_pos(obj: CartesianPosND, /) -> CartesianPosND:
    """Negate the `coordinax.CartesianPosND`.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    A 3D vector:

    >>> vec = cx.CartesianPosND(Quantity([1, 2, 3], "kpc"))
    >>> (-vec).q
    Quantity['length'](Array([-1., -2., -3.], dtype=float32), unit='kpc')

    """
    return jax.tree.map(qlax.neg, obj)


@register(jax.lax.sub_p)  # type: ignore[misc]
def _sub_cnd_pos(lhs: CartesianPosND, rhs: AbstractPos, /) -> CartesianPosND:
    """Subtract two vectors.

    Examples
    --------
    >>> from unxt import Quantity
    >>> from coordinax import CartesianPosND

    A 3D vector:

    >>> q1 = CartesianPosND(Quantity([1, 2, 3], "kpc"))
    >>> q2 = CartesianPosND(Quantity([2, 3, 4], "kpc"))
    >>> (q1 - q2).q
    Quantity['length'](Array([-1., -1., -1.], dtype=float32), unit='kpc')

    """
    cart = rhs.represent_as(CartesianPosND)
    return replace(lhs, q=lhs.q - cart.q)


##############################################################################
# Velocity


@final
class CartesianVelocityND(AvalMixin, AbstractVelocityND):
    """Cartesian differential representation.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    A 1D vector:

    >>> q = cx.CartesianVelocityND(Quantity([[1]], "km/s"))
    >>> q.d_q
    Quantity['speed'](Array([[1.]], dtype=float32), unit='km / s')
    >>> q.shape
    (1,)

    A 2D vector:

    >>> q = cx.CartesianVelocityND(Quantity([1, 2], "km/s"))
    >>> q.d_q
    Quantity['speed'](Array([1., 2.], dtype=float32), unit='km / s')
    >>> q.shape
    ()

    A 3D vector:

    >>> q = cx.CartesianVelocityND(Quantity([1, 2, 3], "km/s"))
    >>> q.d_q
    Quantity['speed'](Array([1., 2., 3.], dtype=float32), unit='km / s')
    >>> q.shape
    ()

    A 4D vector:

    >>> q = cx.CartesianVelocityND(Quantity([1, 2, 3, 4], "km/s"))
    >>> q.d_q
    Quantity['speed'](Array([1., 2., 3., 4.], dtype=float32), unit='km / s')
    >>> q.shape
    ()

    A 5D vector:

    >>> q = cx.CartesianVelocityND(Quantity([1, 2, 3, 4, 5], "km/s"))
    >>> q.d_q
    Quantity['speed'](Array([1., 2., 3., 4., 5.], dtype=float32), unit='km / s')
    >>> q.shape
    ()

    """

    d_q: ct.BatchableSpeed = eqx.field(
        converter=partial(Quantity["speed"].from_, dtype=float)
    )
    r"""N-D speed :math:`d\vec{x}/dt \in (-\infty, \infty).

    Should have shape (*batch, F) where F is the number of features /
    dimensions. Arbitrary batch shapes are supported.
    """

    @classproperty
    @classmethod
    def integral_cls(cls) -> type[CartesianPosND]:
        return CartesianPosND

    @override
    @classproperty
    @classmethod
    def differential_cls(cls) -> type["CartesianAccelerationND"]:
        return CartesianAccelerationND

    @partial(eqx.filter_jit, inline=True)
    def norm(self, _: AbstractPosND | None = None, /) -> ct.BatchableSpeed:
        """Return the norm of the vector.

        Examples
        --------
        >>> from unxt import Quantity
        >>> import coordinax as cx

        A 3D vector:

        >>> c = cx.CartesianVelocityND(Quantity([1, 2, 3], "km/s"))
        >>> c.norm()
        Quantity['speed'](Array(3.7416575, dtype=float32), unit='km / s')

        """
        return jnp.linalg.vector_norm(self.d_q, axis=-1)


# -------------------------------------------------------------------


# TODO: move to the class in py3.11+
@CartesianVelocityND.from_._f.dispatch  # type: ignore[attr-defined,misc]  # noqa: SLF001
def from_(
    cls: type[CartesianVelocityND],
    x: Shaped[Quantity["speed"], ""] | Shaped[Quantity["speed"], "*batch N"],
    /,
) -> CartesianVelocityND:
    """Construct an N-dimensional velocity.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    1D vector:

    >>> cx.CartesianVelocityND.from_(Quantity(1, "km/s"))
    CartesianVelocityND(
      d_q=Quantity[...]( value=f32[1], unit=Unit("km / s") )
    )

    >>> cx.CartesianVelocityND.from_(Quantity([1], "km/s"))
    CartesianVelocityND(
      d_q=Quantity[...]( value=f32[1], unit=Unit("km / s") )
    )

    2D vector:

    >>> cx.CartesianVelocityND.from_(Quantity([1, 2], "km/s"))
    CartesianVelocityND(
      d_q=Quantity[...]( value=f32[2], unit=Unit("km / s") )
    )

    3D vector:

    >>> cx.CartesianVelocityND.from_(Quantity([1, 2, 3], "km/s"))
    CartesianVelocityND(
      d_q=Quantity[...]( value=f32[3], unit=Unit("km / s") )
    )

    4D vector:

    >>> cx.CartesianVelocityND.from_(Quantity([1, 2, 3, 4], "km/s"))
    CartesianVelocityND(
      d_q=Quantity[...]( value=f32[4], unit=Unit("km / s") )
    )

    """
    return cls(jnp.atleast_1d(x))


##############################################################################
# Acceleration


@final
class CartesianAccelerationND(AvalMixin, AbstractAccelerationND):
    """Cartesian N-dimensional acceleration representation.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    A 1D vector:

    >>> q = cx.CartesianAccelerationND(Quantity([[1]], "km/s2"))
    >>> q.d2_q
    Quantity['acceleration'](Array([[1.]], dtype=float32), unit='km / s2')
    >>> q.shape
    (1,)

    A 2D vector:

    >>> q = cx.CartesianAccelerationND(Quantity([1, 2], "km/s2"))
    >>> q.d2_q
    Quantity['acceleration'](Array([1., 2.], dtype=float32), unit='km / s2')
    >>> q.shape
    ()

    A 3D vector:

    >>> q = cx.CartesianAccelerationND(Quantity([1, 2, 3], "km/s2"))
    >>> q.d2_q
    Quantity['acceleration'](Array([1., 2., 3.], dtype=float32), unit='km / s2')
    >>> q.shape
    ()

    A 4D vector:

    >>> q = cx.CartesianAccelerationND(Quantity([1, 2, 3, 4], "km/s2"))
    >>> q.d2_q
    Quantity['acceleration'](Array([1., 2., 3., 4.], dtype=float32), unit='km / s2')
    >>> q.shape
    ()

    A 5D vector:

    >>> q = cx.CartesianAccelerationND(Quantity([1, 2, 3, 4, 5], "km/s2"))
    >>> q.d2_q
    Quantity['acceleration'](Array([1., 2., 3., 4., 5.], dtype=float32), unit='km / s2')
    >>> q.shape
    ()

    """

    d2_q: ct.BatchableAcc = eqx.field(
        converter=partial(Quantity["acceleration"].from_, dtype=float)
    )
    r"""N-D acceleration :math:`d\vec{x}/dt^2 \in (-\infty, \infty).

    Should have shape (*batch, F) where F is the number of features /
    dimensions. Arbitrary batch shapes are supported.
    """

    @override
    @classproperty
    @classmethod
    def integral_cls(cls) -> type[CartesianVelocityND]:
        """Return the integral class.

        Examples
        --------
        >>> import coordinax as cx
        >>> cx.CartesianAccelerationND.integral_cls.__name__
        'CartesianVelocityND'

        """
        return CartesianVelocityND

    @classproperty
    @classmethod
    def differential_cls(cls) -> NoReturn:
        """Return the differential class.

        Examples
        --------
        >>> import coordinax as cx
        >>> try: cx.CartesianAccelerationND.differential_cls
        ... except NotImplementedError as e: print(e)
        Not yet supported

        """
        msg = "Not yet supported"
        raise NotImplementedError(msg)  # TODO: Implement this

    @override
    @partial(eqx.filter_jit, inline=True)
    def norm(
        self,
        velocity: AbstractVelocityND | None = None,
        position: AbstractPosND | None = None,
        /,
    ) -> ct.BatchableSpeed:
        """Return the norm of the vector.

        Examples
        --------
        >>> from unxt import Quantity
        >>> import coordinax as cx

        A 3D vector:

        >>> c = cx.CartesianAccelerationND(Quantity([1, 2, 3], "km/s2"))
        >>> c.norm()
        Quantity['acceleration'](Array(3.7416575, dtype=float32), unit='km / s2')

        """
        return jnp.linalg.vector_norm(self.d2_q, axis=-1)


# -------------------------------------------------------------------


# TODO: move to the class in py3.11+
@CartesianAccelerationND.from_._f.dispatch  # type: ignore[attr-defined,misc]  # noqa: SLF001
def from_(
    cls: type[CartesianAccelerationND],
    x: Shaped[Quantity["acceleration"], ""]
    | Shaped[Quantity["acceleration"], "*batch N"],
    /,
) -> CartesianAccelerationND:
    """Construct an N-dimensional acceleration.

    Examples
    --------
    >>> from unxt import Quantity
    >>> import coordinax as cx

    1D vector:

    >>> cx.CartesianAccelerationND.from_(Quantity(1, "km/s2"))
    CartesianAccelerationND(
      d2_q=Quantity[...]( value=f32[1], unit=Unit("km / s2") )
    )

    >>> cx.CartesianAccelerationND.from_(Quantity([1], "km/s2"))
    CartesianAccelerationND(
      d2_q=Quantity[...]( value=f32[1], unit=Unit("km / s2") )
    )

    2D vector:

    >>> cx.CartesianAccelerationND.from_(Quantity([1, 2], "km/s2"))
    CartesianAccelerationND(
      d2_q=Quantity[...]( value=f32[2], unit=Unit("km / s2") )
    )

    3D vector:

    >>> cx.CartesianAccelerationND.from_(Quantity([1, 2, 3], "km/s2"))
    CartesianAccelerationND(
      d2_q=Quantity[...]( value=f32[3], unit=Unit("km / s2") )
    )

    4D vector:

    >>> cx.CartesianAccelerationND.from_(Quantity([1, 2, 3, 4], "km/s2"))
    CartesianAccelerationND(
      d2_q=Quantity[...]( value=f32[4], unit=Unit("km / s2") )
    )

    """
    return cls(jnp.atleast_1d(x))
