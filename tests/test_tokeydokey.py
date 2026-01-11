"""Tests for tokeydokey public API."""

import math
import random

import tiktoken

import tokeydokey


def test_generate_default() -> None:
    """Default generates 4-token identifier."""
    result = tokeydokey.generate()
    # Should have 4 parts (start + 3 next)
    # Each next part starts with . or -
    assert isinstance(result, str)
    assert len(result) > 0


def test_generate_custom_length() -> None:
    """Can generate identifiers of various lengths."""
    for n in [1, 2, 3, 5, 6]:
        result = tokeydokey.generate(n=n)
        assert isinstance(result, str)
        assert len(result) > 0


def test_generate_n_equals_one() -> None:
    """Single token identifier has no separator."""
    result = tokeydokey.generate(n=1)
    # Should be alphanumeric only (start pool token)
    assert "." not in result
    assert "-" not in result


def test_generate_invalid_n() -> None:
    """Raises ValueError for n < 1."""
    try:
        tokeydokey.generate(n=0)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert "at least 1" in str(e)

    try:
        tokeydokey.generate(n=-1)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert "at least 1" in str(e)


def test_generate_with_custom_rng() -> None:
    """Custom RNG produces reproducible results."""
    rng1 = random.Random(42)
    result1 = tokeydokey.generate(n=4, rng=rng1)

    rng2 = random.Random(42)
    result2 = tokeydokey.generate(n=4, rng=rng2)

    assert result1 == result2


def test_pool_size() -> None:
    """Pool size returns expected tuple."""
    size = tokeydokey.pool_size()
    assert isinstance(size, tuple)
    assert len(size) == 2
    start, next_ = size
    assert start == 38949
    assert next_ == 6381


def test_combinations() -> None:
    """Combinations are calculated correctly."""
    start, next_ = tokeydokey.pool_size()

    assert tokeydokey.combinations(0) == 0
    assert tokeydokey.combinations(1) == start
    assert tokeydokey.combinations(2) == start * next_
    assert tokeydokey.combinations(3) == start * next_ * next_
    assert tokeydokey.combinations(4) == start * (next_ ** 3)


def test_entropy_bits() -> None:
    """Entropy bits scale correctly with token count."""
    # entropy_bits(n) = log2(combinations(n))
    for n in [1, 2, 3, 4, 5, 6]:
        expected = math.log2(tokeydokey.combinations(n))
        actual = tokeydokey.entropy_bits(n)
        assert abs(actual - expected) < 0.01


def test_entropy_bits_zero() -> None:
    """Entropy bits is 0 for n=0."""
    assert tokeydokey.entropy_bits(0) == 0.0


def test_token_roundtrip() -> None:
    """Generated identifiers tokenize to exactly n tokens."""
    enc = tiktoken.get_encoding("o200k_base")

    for n in [1, 2, 3, 4, 5, 6]:
        # Generate a few samples for each length
        for _ in range(10):
            identifier = tokeydokey.generate(n=n)
            tokens = enc.encode(identifier)
            assert len(tokens) == n, (
                f"Expected {n} tokens, got {len(tokens)} for '{identifier}'"
            )


def test_version() -> None:
    """Version is accessible."""
    assert tokeydokey.__version__ == "1.0.0"
