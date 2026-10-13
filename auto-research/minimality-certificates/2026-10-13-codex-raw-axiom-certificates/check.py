"""Independently expand raw axioms and check a rational lower-bound certificate.

Only the standard library is used. Does not import the generator, repository
tests, sympy, a profile formula, or a lemma from the analytic proof.
"""
import argparse
from fractions import Fraction
import json


class InvalidCertificate(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidCertificate(message)


def check(cert):
    require(cert.get("schema") == "raw-profile-lower-bound-v1", "unknown schema")
    target = cert["target"]
    a, b = target["a"], target["b"]
    require(all(type(n) is int and n >= 1 for n in (a, b)), "invalid target")
    coefficients = {}
    constant = Fraction(0)

    def put(x, y, value):
        # Quotient variables by the exact symmetry equality P(x,y)=P(y,x).
        key = (min(x, y), max(x, y))
        coefficients[key] = coefficients.get(key, Fraction(0)) + value

    for row in cert["rows"]:
        kind, indices = row["kind"], row["args"]
        weight = Fraction(row["weight"])
        require(all(type(n) is int and n >= 1 for n in indices), "invalid axiom indices")
        if kind == "boundary":
            require(len(indices) == 1, "boundary arity")
            n, = indices
            put(1, n, weight)
            constant -= weight*n
        elif kind == "concavity":
            require(len(indices) == 2 and indices[1] >= 2, "concavity domain")
            require(weight >= 0, "negative inequality multiplier")
            x, y = indices
            put(x, y, 2*weight)
            put(x, y-1, -weight)
            put(x, y+1, -weight)
        elif kind == "tripling":
            require(len(indices) == 2, "tripling arity")
            require(weight >= 0, "negative inequality multiplier")
            x, h = indices
            put(x, 3*h+x-1, weight)
            put(x, h, -3*weight)
        else:
            raise InvalidCertificate("unknown raw axiom: " + str(kind))
    put(a, b, -1)
    constant += Fraction(target["lower"])
    residual = {key: str(value) for key, value in coefficients.items() if value}
    require(not residual and not constant,
            "coefficient identity failed: " + str(residual) + "; constant=" + str(constant))
    return {"a": a, "b": b, "lower": target["lower"], "rows": len(cert["rows"])}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate")
    args = parser.parse_args()
    with open(args.certificate, encoding="utf-8") as source:
        certificate = json.load(source)
    print("PASS " + json.dumps(check(certificate), sort_keys=True))
