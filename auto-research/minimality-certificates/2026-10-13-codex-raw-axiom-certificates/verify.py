"""Finite exact verification and adversarial controls; run from any directory."""
from copy import deepcopy
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import random

from build import certificate
from check import check, InvalidCertificate, require


HERE = Path(__file__).resolve().parent


def least(a, b):
    # Independent direct product; generator uses a diagonal-bound recurrence.
    small, large = sorted((a, b))
    value = Q(2*large + small - 1, 2)
    for m in range(1, small):
        value *= Q(3*m+1, 3*m)
    return value


def reject(cert, reason):
    try:
        check(cert)
    except InvalidCertificate:
        return reason
    raise RuntimeError("negative control accepted: " + reason)


def main():
    results = json.loads((HERE / "RESULT.json").read_text())
    settings = results["coverage"]
    domain = [(a, b) for a in range(1, settings["square_max"]+1)
              for b in range(1, settings["square_max"]+1)]
    domain += [tuple(pair) for pair in settings["additional_pairs"]]
    random.Random(results["assignment_seed"]).shuffle(domain)
    max_rows = 0
    for a, b in domain:
        cert = certificate(a, b)
        check(cert)
        require(all(row["args"] == [1] for row in cert["rows"]
                    if row["kind"] == "boundary"), "uses more than P(1,1)=1")
        require(Q(cert["target"]["lower"]) == least(a, b), "incorrect least-profile target")
        max_rows = max(max_rows, len(cert["rows"]))

    saved = json.loads((HERE / "certificate.json").read_text())
    check(saved)
    require(saved == certificate(saved["target"]["a"], saved["target"]["b"]),
            "saved certificate is not reproducible")
    controls = []
    bad = deepcopy(saved)
    bad["target"]["lower"] = str(Q(bad["target"]["lower"])+1)
    controls.append(reject(bad, "inflate target by one"))
    bad = deepcopy(saved)
    row = next(row for row in bad["rows"] if row["kind"] == "tripling")
    row["weight"] = str(-Q(row["weight"]))
    controls.append(reject(bad, "negative tripling multiplier"))
    bad = deepcopy(saved)
    index = next(i for i, row in enumerate(bad["rows"]) if row["kind"] == "concavity")
    del bad["rows"][index]
    controls.append(reject(bad, "omit required concavity row"))
    bad = deepcopy(saved)
    row = next(row for row in bad["rows"] if row["kind"] == "boundary")
    row["args"][0] += 1
    controls.append(reject(bad, "alter boundary equality"))
    bad = deepcopy(saved)
    row = next(row for row in bad["rows"] if row["kind"] == "tripling")
    row["args"][1] += 1
    controls.append(reject(bad, "alter tripling source index"))
    # Invalid row domain must be rejected even at zero multiplier.
    bad = deepcopy(saved)
    bad["rows"].append({"kind": "concavity", "args": [1, 1], "weight": "0"})
    controls.append(reject(bad, "concavity outside positive domain"))

    # Concrete counterexample if the additive a-1 in tripling were omitted.
    require(least(2, 6) < 3*least(2, 2), "unshifted-tripling control failed")
    controls.append("unshifted tripling rejected at (2,2): 26/3 < 10")

    # A sharp bound cannot be deduced without the boundary normalization:
    # zero satisfies symmetry/concavity/tripling but violates P(1,1)=1.
    bad = deepcopy(saved)
    bad["rows"] = [row for row in bad["rows"] if row["kind"] != "boundary"]
    controls.append(reject(bad, "omit boundary normalization"))

    manifest = json.loads((HERE / "MANIFEST.json").read_text())
    actual_names = {str(p.relative_to(HERE)) for p in HERE.rglob("*") if p.is_file()
                    and "__pycache__" not in p.parts and p.name != "MANIFEST.json"}
    require(actual_names == set(manifest["files"]), "manifest file set differs")
    for name, expected in manifest["files"].items():
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
                "manifest hash differs: " + name)
    summary = {"certificates_checked": len(domain), "max_rows": max_rows,
               "negative_controls": len(controls), "saved_certificate_rows": len(saved["rows"])}
    require(summary == results["expected_summary"], "summary differs from RESULT.json")
    print("PASS " + json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
