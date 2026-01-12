# tokeydokey

Create random identifiers using a fixed number of non-overlapping LLM tokens.

## Quick start

```bash
uv add tokeydokey
uv run python - <<'PY'
import tokeydokey

print(tokeydokey.generate())
# e.g. "cache.Enable-Thread.sort" (4 by default)
print(tokeydokey.generate(n=5))
# e.g. "db.Connection-Reset.queue.ready"
PY
```

## Development

```bash
uv sync --group dev
uv run pytest
```

### Regenerate pools

```bash
uv run python scripts/generate_pools.py
uv run python scripts/generate_pools.py --encoding cl100k_base --out src/tokeydokey/_pools.py
```

## Example pool math (o200k_base, dot/dash union)

Start pool N = 3.89×10<sup>4</sup> (alnum tokens), next pool M = 6.38×10<sup>3</sup> (".word" or "-word").

| Tokens | Combinations                           | Tokens | Combinations                            | Tokens | Combinations                            |
| -----: | -------------------------------------- | -----: | --------------------------------------- | -----: | --------------------------------------- |
|      1 | 3.89×10<sup>4</sup> (~2<sup>15</sup>)  |      5 | 6.46×10<sup>19</sup> (~2<sup>66</sup>)  |      9 | 1.07×10<sup>35</sup> (~2<sup>116</sup>) |
|      2 | 2.49×10<sup>8</sup> (~2<sup>28</sup>)  |      6 | 4.12×10<sup>23</sup> (~2<sup>78</sup>)  |     10 | 6.83×10<sup>38</sup> (~2<sup>129</sup>) |
|      3 | 1.59×10<sup>12</sup> (~2<sup>41</sup>) |      7 | 2.63×10<sup>27</sup> (~2<sup>91</sup>)  |     11 | 4.36×10<sup>42</sup> (~2<sup>142</sup>) |
|      4 | 1.01×10<sup>16</sup> (~2<sup>53</sup>) |      8 | 1.68×10<sup>31</sup> (~2<sup>104</sup>) |     12 | 2.78×10<sup>46</sup> (~2<sup>154</sup>) |

Note: For ~128 bits of entropy, base64 needs 22 chars (132 bits) which average ~15.2 tokens in o200k_base; dot/dash union needs ~10 tokens. This is roughly 50% more token-efficient than random base64 identifiers.

## Alternatives considered

- CamelTitle (Titlecase 2-12 chars): pool size 8,482, 100% compatible for concatenation.
- Word/(Word+Number) alternating: union pool size 9,482 (adds 0-999), 100% compatible.
- Dot-only: next pool 4,410, 100% compatible.
- Base62: around 8.6 bits per token in o200k_base; token count varies.

## License

MIT
