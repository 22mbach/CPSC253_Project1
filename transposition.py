from typing import List

def _rail_pattern(n: int, rails: int) -> List[int]:
    """Create the rail-fence zig-zag pattern of rail indices for a given string length."""
    if rails < 2:
        return list(range(n))
    pattern: List[int] = []
    r = 0
    step = 1
    for _ in range(n):
        pattern.append(r)
        r += step
        if r == 0 or r == rails - 1:
            step *= -1
    return pattern


def rail_fence_encrypt(s: str, rails: int) -> str:
    """Apply rail-fence transposition to reorder characters by rails."""
    if not s:
        return s
    pattern = _rail_pattern(len(s), rails)
    buckets: List[List[str]] = [[] for _ in range(rails)]
    for ch, r in zip(s, pattern):
        buckets[r].append(ch)
    return ''.join(''.join(b) for b in buckets)


def rail_fence_decrypt(s: str, rails: int) -> str:
    """Reverse rail-fence transposition to restore original character order."""
    if not s:
        return s
    n = len(s)
    pattern = _rail_pattern(n, rails)

    counts = [0] * rails
    for r in pattern:
        counts[r] += 1

    pos = 0
    rails_str: List[List[str]] = []
    for c in counts:
        rails_str.append(list(s[pos:pos + c]))
        pos += c

    idx = [0] * rails
    out: List[str] = []
    for r in pattern:
        out.append(rails_str[r][idx[r]])
        idx[r] += 1
    return ''.join(out)
