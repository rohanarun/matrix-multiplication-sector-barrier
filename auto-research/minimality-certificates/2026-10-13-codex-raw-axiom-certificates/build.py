"""Generate rational lower-bound certificates; no profile evaluation imports."""
import argparse
from fractions import Fraction as Q
import json


def add(out, part, scale=Q(1)):
    for key, value in part.items():
        out[key] = out.get(key, Q(0)) + scale * value


def slope(a, h):
    """Certificate for (3a-1)(P(a,h+1)-P(a,h))-2P(a,a)."""
    if not (1 <= a <= h):
        raise ValueError("slope requires 1 <= a <= h")
    end = 3*h + a - 1
    result = {("tripling", a, h): Q(1)}
    for k in range(h+1, end):
        result[("concavity", a, k)] = Q(end-k)
    for k in range(a+1, h+1):
        result[("concavity", a, k)] = Q(2*(k-a))
    return result


def certificate(a, b):
    if min(a, b) < 1:
        raise ValueError("positive integer coordinates required")
    a, b = sorted((a, b))
    # Inductively certify D_a - d_a >= 0, starting with P(1,1)=1.
    weights = {("boundary", 1): Q(1)}
    diagonal = Q(1)
    for n in range(2, a+1):
        alpha = Q(3*n-3, 3*n-1)
        beta = Q(3*n-2, 3*n-4)
        step = {}
        add(step, slope(n-1, n-1), Q(1, 3*n-4))
        add(step, {("concavity", n, n): Q(1)})
        add(step, slope(n, n), Q(1, 3*n-1))
        new = {}
        add(new, step, 1/alpha)
        add(new, weights, beta/alpha)
        weights = new
        diagonal *= beta/alpha
    factor = 1 + Q(2*(b-a), 3*a-1)
    result = {}
    add(result, weights, factor)
    for h in range(a, b):
        add(result, slope(a, h), Q(1, 3*a-1))
    return {
        "schema": "raw-profile-lower-bound-v1",
        "target": {"a": a, "b": b, "lower": str(diagonal*factor)},
        "rows": [
            {"kind": key[0], "args": list(key[1:]), "weight": str(value)}
            for key, value in sorted(result.items()) if value
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("a", type=int)
    parser.add_argument("b", type=int)
    args = parser.parse_args()
    print(json.dumps(certificate(args.a, args.b), indent=2, sort_keys=True))
