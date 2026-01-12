"""tokeydokey - Create random identifiers using a fixed number of non-overlapping LLM tokens.

Generate token-efficient random identifiers where each segment is guaranteed to be
exactly one token, making token budgets predictable and maximizing entropy per token.

Examples:
    >>> import tokeydokey
    >>> tokeydokey.generate()
    'cache.Enable-Thread.sort'
    >>> tokeydokey.generate(n=5)
    'db.Connection-Reset.queue.ready'
    >>> tokeydokey.pool_size()
    (38949, 6381)
    >>> tokeydokey.combinations(4)
    10119581342877609
"""

from ._generator import combinations, entropy_bits, generate, pool_size

__version__ = "1.0.2"
__all__ = ["generate", "pool_size", "combinations", "entropy_bits"]
