"""Transformations between representations."""

__all__: list[str] = []

from dataclasses import replace
from math import prod
from typing import Any, cast

import equinox as eqx
import jax
from plum import dispatch

import quaxed.numpy as jnp
import unxt as u
from dataclassish import field_items

from coordinax._src.distances import AbstractDistance
from coordinax._src.vectors.base_acc import AbstractAcc
from coordinax._src.vectors.base_pos import AbstractPos
from coordinax._src.vectors.base_vel import AbstractVel
from coordinax._src.vectors.d1 import AbstractAcc1D
from coordinax._src.vectors.d2 import AbstractAcc2D
from coordinax._src.vectors.d3 import AbstractAcc3D


# TODO: implement for cross-representations
@dispatch.multi(
    # N-D -> N-D
    (
        type[AbstractAcc1D],
        AbstractAcc1D,
        AbstractVel | u.Quantity["speed"],
        AbstractPos | u.Quantity["length"],
    ),
    (
        type[AbstractAcc2D],
        AbstractAcc2D,
        AbstractVel | u.Quantity["speed"],
        AbstractPos | u.Quantity["length"],
    ),
    (
        type[AbstractAcc3D],
        AbstractAcc3D,
        AbstractVel | u.Quantity["speed"],
        AbstractPos | u.Quantity["length"],
    ),
)
def vconvert(
    target: type[AbstractAcc],
    current: AbstractAcc,
    velocity: AbstractVel | u.Quantity["speed"],
    position: AbstractPos | u.Quantity["length"],
    /,
    **kwargs: Any,
) -> AbstractAcc:
    """AbstractAcc -> Cartesian -> AbstractAcc.

    This is the base case for the transformation of accelerations.

    Parameters
    ----------
    current
        The vector acceleration to transform.
    target
        The target type of the vector acceleration.
    velocity
        The velocity vector used to transform the acceleration.
    position
        The position vector used to transform the acceleration.
    **kwargs
        Additional keyword arguments.

    Examples
    --------
    >>> import unxt as u
    >>> import coordinax as cx

    Let's start in 1D:

    >>> q = cx.vecs.CartesianPos1D(x=u.Quantity(1.0, "km"))
    >>> p = cx.vecs.CartesianVel1D(x=u.Quantity(1.0, "km/s"))
    >>> a = cx.vecs.CartesianAcc1D(x=u.Quantity(1.0, "km/s2"))
    >>> cx.vconvert(cx.vecs.RadialAcc, a, p, q)
    RadialAcc( r=Quantity[...](value=f32[], unit=Unit("km / s2")) )

    Now in 2D:

    >>> q = cx.vecs.CartesianPos2D.from_([1.0, 2.0], "km")
    >>> p = cx.vecs.CartesianVel2D.from_([1.0, 2.0], "km/s")
    >>> a = cx.vecs.CartesianAcc2D.from_([1.0, 2.0], "km/s2")
    >>> cx.vconvert(cx.vecs.PolarAcc, a, p, q)
    PolarAcc(
      r=Quantity[...](value=f32[], unit=Unit("km / s2")),
      phi=Quantity[...]( value=f32[], unit=Unit("rad / s2") )
    )

    And in 3D:

    >>> q = cx.CartesianPos3D.from_([1.0, 2.0, 3.0], "km")
    >>> p = cx.CartesianVel3D.from_([1.0, 2.0, 3.0], "km/s")
    >>> a = cx.vecs.CartesianAcc3D.from_([1.0, 2.0, 3.0], "km/s2")
    >>> cx.vconvert(cx.vecs.SphericalAcc, a, p, q)
    SphericalAcc(
      r=Quantity[...](value=f32[], unit=Unit("km / s2")),
      theta=Quantity[...]( value=f32[], unit=Unit("rad / s2") ),
      phi=Quantity[...]( value=f32[], unit=Unit("rad / s2") )
    )

    If given a position as a Quantity, it will be converted to the appropriate
    Cartesian vector:

    >>> cx.vconvert(cx.vecs.SphericalAcc, a,
    ...             u.Quantity([1.0, 2.0, 3.0], "km/s"),
    ...             u.Quantity([1.0, 2.0, 3.0], "km"))
    SphericalAcc(
      r=Quantity[...](value=f32[], unit=Unit("km / s2")),
      theta=Quantity[...]( value=f32[], unit=Unit("rad / s2") ),
      phi=Quantity[...]( value=f32[], unit=Unit("rad / s2") )
    )

    """
    # TODO: not require the shape munging / support more shapes
    shape = current.shape
    flat_shape = prod(shape)

    # Parse the velocity to an AbstractVel # Q -> Cart<X>D
    vel_cls = cast(AbstractVel, current.time_antiderivative_cls)
    velvec = cast(
        AbstractVel,
        velocity
        if isinstance(velocity, AbstractVel)
        else vel_cls.cartesian_type.from_(velocity),
    )

    # Parse the position to an AbstractPos (Q -> Cart<X>D)
    pos_cls = cast(AbstractPos, vel_cls.time_antiderivative_cls)
    posvec = cast(
        AbstractPos,
        position
        if isinstance(position, AbstractPos)
        else pos_cls.cartesian_type.from_(position),
    )

    posvec = posvec.reshape(flat_shape)  # flattened
    velvec = velvec.reshape(flat_shape)  # flattened

    # Start by transforming the position to the type required by the
    # differential to construct the Jacobian.
    current_pos = vconvert(current.time_nth_derivative_cls(-2), posvec, **kwargs)
    # TODO: not need to cast to distance
    current_pos = replace(
        current_pos,
        **{
            k: v.distance
            for k, v in field_items(current_pos)
            if isinstance(v, AbstractDistance)
        },
    )
    # The Jacobian requires the position to be a float
    dtype = jnp.result_type(float)  # TODO: better match e.g. int16 to float16?
    current_pos = current_pos.astype(dtype, copy=False)  # cast to float

    # Takes the Jacobian through the representation transformation function.  This
    # returns a representation of the target type, where the value of each field the
    # corresponding row of the Jacobian. The value of the field is a Quantity with
    # the correct numerator unit (of the Jacobian row). The value is a Vector of the
    # original type, with fields that are the columns of that row, but with only the
    # denomicator's units.
    jac_nested_vecs = jac_rep_as(target.time_nth_derivative_cls(-2), current_pos)

    # This changes the Jacobian to be a dictionary of each row, with the value
    # being that row's column as a dictionary, now with the correct units for
    # each element:  {row_i: {col_j: Quantity(value, row.unit / column.unit)}}
    jac_rows = {
        k: {
            kk: u.Quantity(vv.value, unit=v.unit / vv.unit)
            for kk, vv in field_items(v.value)
        }
        for k, v in field_items(jac_nested_vecs)
    }

    # Now we can use the Jacobian to transform the differential.
    flat_current = current.reshape(flat_shape)
    newvec = target(
        **{  # Each field is the dot product of the row of the J and the diff column.
            k: jnp.sum(  # Doing the dot product.
                jnp.stack(
                    tuple(j_c * getattr(flat_current, kk) for kk, j_c in j_r.items())
                ),
                axis=0,
            )
            for k, j_r in jac_rows.items()
        }
    ).reshape(shape)

    # TODO: add  df(q)/dt, which is 0 for all current transforms
    #       This is necessary for the df/dt * vel term in the chain rule.

    return newvec  # noqa: RET504


# TODO: situate this better to show how vconvert is used
jac_rep_as = eqx.filter_jit(
    jax.vmap(jax.jacfwd(vconvert, argnums=1), in_axes=(None, 0))
)
