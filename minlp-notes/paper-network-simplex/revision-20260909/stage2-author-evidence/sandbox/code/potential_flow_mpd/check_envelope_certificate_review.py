"""Independent standard-library-only checks of the rational verifier."""

from copy import deepcopy
from dataclasses import replace
from fractions import Fraction as F
import json
from pathlib import Path
from random import Random
import subprocess
import sys
from tempfile import TemporaryDirectory

from envelope_rational_certificates import (
    Certificate, law, make_certificate, upward_root, verify_certificate,
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def check_known_states():
    cases = [
        ([(0, 1)], [2, -2], [3], [7], [2], [12, 0]),
        ([(0, 1)], [-2, 2], [3], [7], [-2], [-28, 0]),
        ([(0, 1)], [0, 0], [3], [7], [0], [0, 0]),
        ([(0, 1), (0, 1)], [3, -3], [1, 4], [1, 4], [2, 1], [4, 0]),
    ]
    for edges, b, pos, neg, flow, potentials in cases:
        b, pos, neg, flow, potentials = [list(map(F, values))
                                        for values in (b, pos, neg, flow, potentials)]
        cert = make_certificate(edges, b, pos, neg, flow, potentials)
        require(cert.gap == cert.radius == 0, "exact state should have zero gap and radius")
    edges = [(0, 1), (1, 2), (0, 2)]
    b = list(map(F, [3, 0, -3]))
    coeffs = list(map(F, [3, 1, 1]))
    exact = list(map(F, [1, 1, 2]))
    y = [F(5, 4), F(5, 4), F(7, 4)]
    potentials = list(map(F, [4, 1, 0]))
    cert = make_certificate(edges, b, coeffs, coeffs, y, potentials)
    require(cert.radius >= F(1, 4), "certified radius misses known exact state")
    require(law(y[2]-cert.radius, F(1), F(1)) <= 4 <=
            law(y[2]+cert.radius, F(1), F(1)), "pressure interval misses exact drop")
    for bad in [replace(cert, radius=0.0), replace(cert, gap=float(cert.gap))]:
        try:
            verify_certificate(edges, b, coeffs, coeffs, bad)
        except ValueError:
            pass
        else:
            raise RuntimeError("nonrational direct certificate accepted")
    return 5


def check_roots():
    rng = Random(83)
    count = 0
    for _ in range(100):
        value = F(rng.randrange(10**8), rng.randrange(1, 10**6))
        for degree in (2, 3):
            for bits in (0, 1, 8, 40):
                upper = upward_root(value, degree, bits)
                step = F(1, 1 << bits)
                require(upper**degree >= value, "root enclosure rounds down")
                require(upper == 0 or (upper-step)**degree < value,
                        "root enclosure is not the smallest dyadic upper bound")
                count += 1
    return count


def check_saved_file():
    directory = Path(__file__).resolve().parent
    verifier = directory / "envelope_rational_certificates.py"
    original = json.loads((directory / "envelope_certificate_example.json").read_text())
    bad = []
    for key in ("flow", "b"):
        payload = deepcopy(original)
        payload[key][0] = str(F(payload[key][0])+1)
        bad.append(payload)
    for key, value in (("root_upper", "0"), ("positive", "0")):
        payload = deepcopy(original)
        payload[key][0] = value
        bad.append(payload)
    payload = deepcopy(original)
    payload["gap"] = str(F(payload["gap"])+1)
    bad.append(payload)
    payload = deepcopy(original)
    payload["radius"] = "0"
    bad.append(payload)
    payload = deepcopy(original)
    payload["edges"][0][0] = -1
    bad.append(payload)
    payload = deepcopy(original)
    payload["flow"].pop()
    bad.append(payload)
    count = 0
    with TemporaryDirectory(prefix="envelope-review-") as temp:
        path = Path(temp) / "certificate.json"
        for optimized in (False, True):
            prefix = [sys.executable]+(["-O"] if optimized else [])+[str(verifier), "--verify", str(path)]
            path.write_text(json.dumps(original))
            result = subprocess.run(prefix, capture_output=True, text=True)
            require(result.returncode == 0 and "verified" in result.stdout,
                    "valid saved certificate rejected")
            for payload in bad:
                path.write_text(json.dumps(payload))
                result = subprocess.run(prefix, capture_output=True, text=True)
                require(result.returncode != 0 and "verified" not in result.stdout,
                        "corrupted file accepted")
                count += 1
    return count


if __name__ == "__main__":
    states = check_known_states()
    roots = check_roots()
    corruptions = check_saved_file()
    print(f"PASS: {states} exact known states; {roots} root minimality checks; "
          f"{corruptions} file corruption rejections in normal/optimized Python; "
          "valid saved file accepted in both modes; float gap/radius rejected")
