"""Exact local-pair versus merged-star diagnostic, independent of SCIP."""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "theory"))
from quadratic_star import replay_star, support_star


def diagnostic():
    # Variables x,y,z; y is the common center.
    c = {(0, 0, 0): Q(1, 16), (1, 0, 0): Q(5, 4), (0, 1, 0): Q(-1, 2),
         (0, 0, 1): Q(1), (2, 0, 0): Q(-3, 4), (0, 2, 0): Q(2),
         (0, 0, 2): Q(-39, 64), (1, 1, 0): Q(-1), (0, 1, 1): Q(-5, 4)}
    left = [(Q(1, 2), (Q(0), Q(1, 4))), (Q(1, 2), (Q(1), Q(3, 4)))]
    right = [(Q(1, 5), (Q(0), Q(0))), (Q(4, 5), (Q(5, 8), Q(1)))]
    left_y = [sum(p * y**k for p, (x, y) in left) for k in (0, 1, 2)]
    right_y = [sum(p * y**k for p, (y, z) in right) for k in (0, 1, 2)]
    assert left_y == right_y == [Q(1), Q(1, 2), Q(5, 16)]
    left_value = sum(p * ((y - Q(1, 4) - x / 2)**2 + x*(1-x)) for p, (x, y) in left)
    right_value = sum(p * ((y - Q(5, 8)*z)**2 + z*(1-z)) for p, (y, z) in right)
    assert left_value == right_value == 0
    certificate = support_star(((0, 1),) * 3, (), c, center=1)
    assert certificate["bound"] == "1/128"
    assert replay_star(((0, 1),) * 3, (), c, 1, certificate)
    point = [Q(x) for x in certificate["minimizer"]]
    value = sum(coefficient * point[0]**powers[0] * point[1]**powers[1] * point[2]**powers[2]
                for powers, coefficient in c.items())
    assert value == Q(1, 128)
    mutated = dict(c)
    mutated[(0, 0, 0)] += Q(1, 1024)
    assert not replay_star(((0, 1),) * 3, (), mutated, 1, certificate)
    return {
        "variables": ["x", "y", "z"], "center": "y", "domain": "[0,1]^3",
        "objective": "(y-1/4-x/2)^2 + (y-5z/8)^2 + x(1-x) + z(1-z)",
        "left_measure": [[str(p), [str(t) for t in xy]] for p, xy in left],
        "right_measure": [[str(p), [str(t) for t in yz]] for p, yz in right],
        "shared_center_moments": [str(q) for q in left_y],
        "left_expected_objective": str(left_value), "right_expected_objective": str(right_value),
        "exact_pair_hull_bound": "0", "exact_star_minimum": str(value),
        "star_certificate_replayed": True, "changed_objective_rejected": True,
        "certificate": certificate,
        "scope": "Two local pair graph hulls agreeing on E[y] and E[y^2]; no dominance claim over dense PSD/RLT.",
        "source_sha256": {str(p.relative_to(HERE.parent)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in (Path(__file__), HERE.parent / "theory/quadratic_star.py",
                                    HERE.parent / "theory/quadratic_polygon.py")},
    }


if __name__ == "__main__":
    result = diagnostic()
    (HERE / "star-mechanism.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("certificate", "source_sha256")}, indent=2))
