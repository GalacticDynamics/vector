# pylint: disable=import-error

"""Copyright (c) 2023 Nathaniel Starkman. All rights reserved.

coordinax: Vectors in JAX
"""

from jaxtyping import install_import_hook

from . import operators
from ._coordinax import (
    _d1,
    _d2,
    _d3,
    base,
    base_acc,
    base_pos,
    base_vel,
    d4,
    dn,
    exceptions,
    funcs,
    space,
    transform,
    typing,
    utils,
)
from ._coordinax._d1 import *
from ._coordinax._d2 import *
from ._coordinax._d3 import *
from ._coordinax.base import *
from ._coordinax.base_acc import *
from ._coordinax.base_pos import *
from ._coordinax.base_vel import *
from ._coordinax.d4 import *
from ._coordinax.dn import *
from ._coordinax.exceptions import *
from ._coordinax.funcs import *
from ._coordinax.space import *
from ._coordinax.transform import *
from ._coordinax.typing import *
from ._coordinax.utils import *
from ._version import version as __version__
from .setup_package import RUNTIME_TYPECHECKER

__all__ = ["__version__", "operators"]
__all__ += funcs.__all__
__all__ += base.__all__
__all__ += base_pos.__all__
__all__ += base_vel.__all__
__all__ += base_acc.__all__
__all__ += _d1.__all__
__all__ += _d2.__all__
__all__ += _d3.__all__
__all__ += d4.__all__
__all__ += dn.__all__
__all__ += space.__all__
__all__ += exceptions.__all__
__all__ += transform.__all__
__all__ += typing.__all__
__all__ += utils.__all__

# Interoperability
# Astropy
from ._coordinax._interop import coordinax_interop_astropy  # noqa: E402

# Runtime Typechecker
install_import_hook("coordinax", RUNTIME_TYPECHECKER)

# Cleanup
del (
    base,
    base_vel,
    base_pos,
    base_acc,
    space,
    exceptions,
    transform,
    typing,
    utils,
    _d1,
    _d2,
    _d3,
    d4,
    dn,
    funcs,
    RUNTIME_TYPECHECKER,
    coordinax_interop_astropy,
)
