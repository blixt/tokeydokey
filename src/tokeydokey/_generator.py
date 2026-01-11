"""Core identifier generation logic for tokeydokey."""

from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING

from ._pools import NEXT, START

if TYPE_CHECKING:
    from random import Random


def generate(n: int = 4, *, rng: Random | None = None) -> str:
    """Generate a random identifier with exactly n tokens.

    Each identifier consists of alphanumeric segments separated by dots or dashes,
    where each segment is guaranteed to be exactly one token in the o200k_base
    encoding.

    Args:
        n: Number of tokens in the identifier. Must be at least 1. Default is 4.
        rng: Random number generator to use. Defaults to secrets.SystemRandom()
            for cryptographically secure randomness.

    Returns:
        A string identifier like "cache.Enable-Thread.sort" with exactly n tokens.

    Raises:
        ValueError: If n is less than 1.

    Examples:
        >>> generate()
        'cache.Enable-Thread.sort'
        >>> generate(n=2)
        'db.Connection'
        >>> generate(n=5)
        'menn.Enable.Immutable-Men.sort'
    """
    if n < 1:
        raise ValueError("n must be at least 1")

    if rng is None:
        rng = random.SystemRandom()

    # Pick first token from start pool
    start_text, _ = rng.choice(START)

    if n == 1:
        return start_text

    # Pick remaining tokens from next pool
    parts = [start_text]
    for _ in range(n - 1):
        next_text, _ = rng.choice(NEXT)
        parts.append(next_text)

    # Concatenate directly (next tokens include their separator)
    return "".join(parts)


def pool_size() -> tuple[int, int]:
    """Return the size of the start and next token pools.

    Returns:
        A tuple of (start_pool_size, next_pool_size).
    """
    return len(START), len(NEXT)


def combinations(n: int) -> int:
    """Return total possible combinations for n tokens.

    Args:
        n: Number of tokens.

    Returns:
        The total number of unique identifiers that can be generated with n tokens.
    """
    if n < 1:
        return 0
    start_size = len(START)
    if n == 1:
        return start_size
    next_size = len(NEXT)
    return int(start_size * (next_size ** (n - 1)))


def entropy_bits(n: int) -> float:
    """Return entropy in bits for n tokens.

    This represents the equivalent number of random bits needed to uniquely
    identify each possible combination.

    Args:
        n: Number of tokens.

    Returns:
        Entropy in bits.
    """
    combos = combinations(n)
    if combos <= 0:
        return 0.0
    return math.log2(combos)
