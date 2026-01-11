# tokeydokey

Create random identifiers using a fixed number of non-overlapping LLM tokens.

## Quick start

```bash
uv sync
uv run python - <<'PY'
import tokeydokey

print(tokeydokey.generate())
print(tokeydokey.generate(n=5))
PY
```

## Regenerate pools

```bash
uv run python scripts/generate_pools.py
uv run python scripts/generate_pools.py --encoding cl100k_base --out src/tokeydokey/_pools.py
```

## Example pool math (o200k_base, dot/dash union)

Start pool N = 3.89×10<sup>4</sup> (alnum tokens), next pool M = 6.38×10<sup>3</sup> (".word" or "-word").

| Tokens | Combinations                         | Tokens | Combinations                         |
|--------|--------------------------------------|--------|--------------------------------------|
| 1      | 3.89×10<sup>4</sup> (~2^15)           | 4      | 1.01×10<sup>16</sup> (~2^53)         |
| 2      | 2.49×10<sup>8</sup> (~2^28)           | 5      | 6.46×10<sup>19</sup> (~2^66)         |
| 3      | 1.59×10<sup>12</sup> (~2^41)          | 6      | 4.12×10<sup>23</sup> (~2^78)         |

## Alternatives considered

- CamelTitle (Titlecase 2-12 chars): pool size 8,482, 100% compatible for concatenation.
- Word/(Word+Number) alternating: union pool size 9,482 (adds 0-999), 100% compatible.
- Dot-only: next pool 4,410, 100% compatible.
- Base62: around 8.6 bits per token in o200k_base; token count varies.

## License

MIT
