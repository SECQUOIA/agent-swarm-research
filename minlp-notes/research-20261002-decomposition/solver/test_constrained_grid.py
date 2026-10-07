"""Targeted behavior, exact output and rejection tests for constrained grids."""
import copy
from fractions import Fraction as F
import unittest

from constrained_grid import ConstrainedQP, solve
from verify_constrained import CertificateError, verify


def model(H=None, b=None, bounds=None, labels=None, rows=None, rhs=None,
          senses=None, bags=None, edges=None, tu_certificate=None, curvature=None,
          constant=0):
    H = [[2]] if H is None else H
    n = len(H)
    rows = [] if rows is None else rows
    return ConstrainedQP(H, [F(-2, 3)]*n if b is None else b,
                         [(0, 1)]*n if bounds is None else bounds,
                         {} if labels is None else labels, rows,
                         [1]*len(rows) if rhs is None else rhs,
                         ["<="]*len(rows) if senses is None else senses,
                         [tuple(range(n))] if bags is None else bags,
                         [] if edges is None else edges,
                         {"kind": "network"} if tu_certificate is None else tu_certificate,
                         curvature, constant)


class ConstrainedGridTests(unittest.TestCase):
    def test_exact_nondyadic_with_no_face_search(self):
        p = model(constant=F(1, 9))
        cert = solve(p, exact=True, max_exact_faces=0, max_recovery_pivots=0, time_limit=5)
        self.assertEqual(cert["status"], "exact")
        self.assertEqual(cert["point"], ["1/3"])
        self.assertEqual(cert["upper"], "0")
        self.assertEqual(verify(cert)["status"], "exact")

    def test_exact_constrained_active_face(self):
        # On x+y=1 the exact optimum is (1/3,2/3), outside every dyadic grid.
        p = model(H=[[2, 0], [0, 2]], b=[F(-2, 3), F(-4, 3)],
                  rows=[[1, 1]], rhs=[1], senses=["=="], constant=F(5, 9))
        cert = solve(p, exact=True, max_stages=100, time_limit=8)
        self.assertEqual(cert["status"], "exact")
        self.assertEqual(cert["point"], ["1/3", "2/3"])
        self.assertEqual(verify(cert)["upper"], "0")

    def test_branching_resource_tree_and_repeated_separator(self):
        n = 5
        H = [[2*int(i == j) for j in range(n)] for i in range(n)]
        target = [F(1, 3)] + [F(2, 3)]*4
        rows = [[int(j in (0, i)) for j in range(n)] for i in range(1, n)]
        p = model(H=H, b=[-2*v for v in target], rows=rows, rhs=[1]*4,
                  senses=["=="]*4, bags=[(0,)] + [(0, i) for i in range(1, n)],
                  edges=[(0, i) for i in range(1, n)],
                  tu_certificate={"kind": "consecutive_ones"}, constant=sum(v*v for v in target))
        cert = solve(p, epsilon="1/128", time_limit=5)
        checked = verify(cert)
        self.assertEqual(checked["status"], "epsilon")
        self.assertLessEqual(F(checked["lower"]), 0)
        self.assertGreaterEqual(F(checked["upper"]), 0)

    def test_mixed_network_with_arbitrary_integer_column(self):
        # x+y=3z; z has a nonconsecutive native label set.
        p = model(H=[[2, 0, 0], [0, 2, 0], [0, 0, 0]], b=[-2, -4, -1],
                  bounds=[(0, 3), (0, 3), (0, 2)], labels={2: [0, 1, 2]},
                  rows=[[1, 1, -3]], rhs=[0], senses=["=="], constant=6)
        cert = solve(p, epsilon="1/128", time_limit=5)
        self.assertIn(cert["status"], ("exact", "epsilon"))
        self.assertEqual(cert["point"][2], "1")
        self.assertLessEqual(F(cert["lower"]), 0)
        self.assertGreaterEqual(F(cert["upper"]), 0)
        verify(cert)

    def test_equality_tangent_ignores_normal_energy(self):
        p = model(H=[[2002, -2000], [-2000, 2002]], b=[-1, -1],
                  rows=[[1, -1]], rhs=[0], senses=["=="],
                  curvature={"L": 2, "mode": "equalities"})
        cert = solve(p, epsilon="1/128", time_limit=5)
        self.assertIn(cert["status"], ("exact", "epsilon"))
        verify(cert)
        with self.assertRaisesRegex(ValueError, "curvature"):
            model(H=[[0, 2], [2, 0]], b=[0, 0], rows=[[1, -1]], rhs=[0],
                  senses=["=="], curvature={"L": 0, "mode": "equalities"})

    def test_concave_fibers_exact_on_unit_mesh(self):
        p = model(H=[[-2, 0], [0, -2]], b=[0, 0], rows=[[1, 1]], rhs=[1],
                  curvature={"L": 0, "mode": "full"})
        cert = solve(p, exact=True)
        self.assertEqual(cert["status"], "exact")
        self.assertEqual(cert["upper"], "-1")
        self.assertEqual(len(cert["stages"]), 1)
        verify(cert)

    def test_infeasibility_and_native_labels(self):
        p = model(H=[[0, 0], [0, 0]], b=[0, -1], labels={1: [0, 2]},
                  bounds=[(0, 1), (0, 2)], rows=[[1, -1]], rhs=[3], senses=["=="])
        cert = solve(p)
        self.assertEqual(cert["status"], "infeasible")
        verify(cert)
        p = model(H=[[0]], b=[-1], bounds=[(0, 3)], labels={0: [0, 3]})
        cert = solve(p, exact=True)
        self.assertEqual(cert["point"], ["3"])
        self.assertEqual(cert["upper"], "-3")
        verify(cert)

    def test_non_tu_and_unaligned_models_rejected(self):
        with self.assertRaisesRegex(ValueError, "non-TU"):
            model(H=[[0, 0], [0, 0]], b=[0, 0], rows=[[1, 1], [1, -1]],
                  rhs=[1, 0], tu_certificate={"kind": "all_minors"})
        with self.assertRaisesRegex(ValueError, "integral"):
            model(rows=[[1]], rhs=[F(1, 3)], senses=["=="])
        with self.assertRaisesRegex(ValueError, "bounds"):
            model(bounds=[(0, F(1, 3))])
        with self.assertRaisesRegex(ValueError, "scope"):
            model(H=[[0, 0], [0, 0]], b=[0, 0], rows=[[1, 1]],
                  bags=[(0,), (1,)], edges=[(0, 1)])

    def test_structural_tu_and_bounded_minors(self):
        model(H=[[0, 0], [0, 0]], b=[0, 0], rows=[[1, 1], [0, -1]],
              tu_certificate={"kind": "network", "row_signs": [1, 1]})
        with self.assertRaisesRegex(ValueError, "consecutive"):
            model(H=[[0]], b=[0], rows=[[1], [0], [1]], rhs=[1, 1, 1],
                  tu_certificate={"kind": "consecutive_ones"})
        p = model(rows=[[1]], tu_certificate={"kind": "all_minors"})
        cert = solve(p, epsilon="1/8")
        with self.assertRaisesRegex(CertificateError, "budget"):
            verify(cert, max_tu_minors=0)

    def test_certificate_tampering_and_missing_history(self):
        cert = solve(model(), epsilon="1/4096", time_limit=5)
        self.assertGreater(len(cert["stages"]), 2)
        for change in ("lower", "retained", "grid", "history", "curvature"):
            bad = copy.deepcopy(cert)
            if change == "lower":
                bad["lower"] = "99"
            elif change == "retained":
                bad["stages"][0]["retained"][0] = ["0", "0"]
            elif change == "grid":
                bad["stages"][1]["grids"][0][0] = "1/3"
            elif change == "history":
                del bad["stages"][0]
            else:
                bad["problem"]["curvature"]["L"] = "0"
            with self.subTest(change=change), self.assertRaises(CertificateError):
                verify(bad)

    def test_exact_proof_tampering(self):
        cert = solve(model(constant=F(1, 9)), exact=True, time_limit=5)
        self.assertIsNotNone(cert["exact_proof"])
        for change in ("height", "point", "bound"):
            bad = copy.deepcopy(cert)
            if change == "height":
                bad["exact_proof"]["height"]["V"] = 1
            elif change == "point":
                bad["exact_proof"]["point"] = ["1/2"]
            else:
                bad["exact_proof"]["comparison_lower"] = "100"
            with self.subTest(change=change), self.assertRaises(CertificateError):
                verify(bad)

    def test_limits_preserve_honest_partial_certificates(self):
        cert = solve(model(bounds=[(0, 100)]), max_table_states=2)
        self.assertEqual(cert["status"], "limit")
        self.assertIsNone(cert["lower"])
        verify(cert)
        cert = solve(model(), exact=True, max_stages=1, max_exact_faces=0)
        self.assertEqual(cert["status"], "limit")
        self.assertIsNotNone(cert["lower"])
        verify(cert)

    def test_union_filter_and_nonunique_exact_lp_recovery(self):
        # Two disconnected minima; taking the hull preserves the entire x0
        # interval. Union filtering keeps small endpoint neighborhoods.
        p = model(H=[[-2, 0, 0], [0, 2, 0], [0, 0, 2]],
                  b=[1, F(-2, 3), F(-2, 3)], rows=[[0, 1, -1]], rhs=[0],
                  senses=["=="], bags=[(0,), (1, 2)], edges=[(0, 1)], constant=F(2, 9))
        cert = solve(p, exact=True, retain_unions=True, max_exact_faces=0,
                     max_table_states=2000, time_limit=5)
        self.assertEqual(cert["status"], "exact")
        self.assertEqual(cert["upper"], "0")
        self.assertEqual(cert["statistics"]["exact_faces_attempted"], 0)
        self.assertGreater(cert["statistics"]["recovery_lp_calls"], 0)
        self.assertTrue(any(len(stage["retained"][0]) == 2 for stage in cert["stages"]))
        verify(cert, max_table_states=2000)
        hull = solve(p, exact=True, max_exact_faces=0, max_table_states=2000, time_limit=5)
        self.assertEqual(hull["status"], "limit")
        self.assertEqual(hull["reason"], "table-state limit")
        verify(hull, max_table_states=2000)
        bad = copy.deepcopy(cert)
        split = next(s for s in bad["stages"] if len(s["retained"][0]) == 2)
        split["retained"][0] = [[split["retained"][0][0][0], split["retained"][0][-1][1]]]
        with self.assertRaises(CertificateError):
            verify(bad)

    def test_union_fixed_coordinate_and_recovery_limits(self):
        p = model(H=[[0, 0], [0, 2]], b=[0, F(-2, 3)], bounds=[(1, 1), (0, 1)])
        cert = solve(p, epsilon="1/1024", retain_unions=True)
        self.assertIn(cert["status"], ("exact", "epsilon"))
        self.assertEqual(cert["point"][0], "1")
        verify(cert)
        # A discovery LP limit cannot alter an unconditional grid bound.
        cert = solve(p, exact=True, retain_unions=True, max_recovery_pivots=1,
                     max_exact_faces=0, max_stages=3)
        self.assertEqual(cert["status"], "limit")
        self.assertGreater(cert["statistics"]["recovery_lp_limits"], 0)
        verify(cert)


if __name__ == "__main__":
    unittest.main()
