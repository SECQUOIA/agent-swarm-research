"""Targeted polynomial bounds, integer-output, and replay regressions."""
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
from math import comb
import json
import unittest

from polynomial_grid import PolynomialBox, PolynomialFactor, polynomial_grid_dp, solve
from verify_polynomial import CertificateError, polynomial_interval, verify_polynomial


def shifted_power(coordinate, root, degree):
    return PolynomialFactor((coordinate,), [(comb(degree, k) * (-root) ** (degree-k), (k,))
                                            for k in range(degree+1)])


def quartic_chain():
    # (x^2-1/4)^2+(y-x)^2+(z-y)^2 has exact value 0 at constant +/-1/2.
    return PolynomialBox([(-1, 1)]*3, [
        PolynomialFactor((0,), [(1,(4,)), (F(-1,2),(2,)), (F(1,16),(0,))]),
        PolynomialFactor((0,1), [(1,(2,0)), (-2,(1,1)), (1,(0,2))]),
        PolynomialFactor((1,2), [(1,(2,0)), (-2,(1,1)), (1,(0,2))])],
        bags=[(0,1),(1,2)], edges=[(0,1)])


class PolynomialGridTests(unittest.TestCase):
    def test_derivatives_intervals_and_roundtrip(self):
        factor = PolynomialFactor((1,0), [(2,(2,3)), (-3,(0,2)), (1,(0,0)), (2,(0,0))])
        problem = PolynomialBox([(-2,3),(-1,2)], [factor])
        p = (F(1,2), F(-1,3))
        self.assertEqual(factor.value(p), 2*p[1]**2*p[0]**3-3*p[0]**2+3)
        self.assertEqual(factor.derivative(0).value(p), 6*p[1]**2*p[0]**2-6*p[0])
        for indices in [(), (0,0), (0,0,1)]:
            self.assertEqual(problem.derivative_bounds(indices), polynomial_interval(problem,problem.bounds,indices))
        lo, hi = factor.interval(problem.bounds)
        for p in product(range(-2,4), range(-1,3)):
            self.assertLessEqual(lo,factor.value(p))
            self.assertLessEqual(factor.value(p),hi)
        self.assertEqual(PolynomialBox.from_dict(json.loads(json.dumps(problem.to_dict()))).to_dict(),problem.to_dict())

    def test_general_tree_dp_matches_enumeration(self):
        problem = quartic_chain()
        grids = [(F(-1),F(-1,2),F(0),F(1,2),F(1))]*3
        caps = tuple(map(F,problem.curvature_certificate()["caps"]))
        penalties = [tuple(cap/32 for _ in row) for cap,row in zip(caps,grids)]
        result = polynomial_grid_dp(problem,grids,penalties)
        margins = [[None]*len(row) for row in grids]
        exact = None
        for indices in product(*(range(len(row)) for row in grids)):
            p = tuple(grids[i][k] for i,k in enumerate(indices))
            value = problem.value(p)-sum(penalties[i][k] for i,k in enumerate(indices))
            exact = value if exact is None else min(exact,value)
            for i,k in enumerate(indices):
                margins[i][k] = value if margins[i][k] is None else min(margins[i][k],value)
        self.assertEqual(result["lower"],exact)
        self.assertEqual(result["marginals"],tuple(map(tuple,margins)))

    def test_coupled_quartic_pruning_and_replay(self):
        proof = solve(quartic_chain(),F(1,100),max_stages=40,time_limit=15,max_table_states=20000)
        self.assertIn(proof["status"],("certified","exact"))
        self.assertLessEqual(F(proof["lower"]),0)
        self.assertGreaterEqual(F(proof["upper"]),0)
        self.assertLessEqual(F(proof["gap"]),F(1,100))
        self.assertTrue(any(stage["removed_intervals"] for stage in proof["stages"]))
        self.assertTrue(verify_polynomial(json.loads(json.dumps(proof)))["valid"])
        for x in (F(1,2),F(-1,2)):
            self.assertTrue(all(F(lo)<=x<=F(hi) for lo,hi in proof["retained_bounds"]))

    def test_exact_native_integer_degree_six(self):
        problem = PolynomialBox([(-3,4)]*2,[shifted_power(0,F(2),6),
            PolynomialFactor((0,1),[(1,(2,0)),(-2,(1,1)),(1,(0,2))])],integers=[0,1])
        proof = solve(problem,0,max_stages=20,time_limit=5,max_table_states=1000)
        exact = min(problem.value(tuple(map(F,p))) for p in product(range(-3,5),repeat=2))
        self.assertEqual(proof["status"],"exact")
        self.assertEqual(F(proof["lower"]),exact)
        self.assertEqual(proof["point"],["2","2"])
        self.assertTrue(verify_polynomial(proof)["valid"])

    def test_mixed_integer_label_hull_becomes_singleton(self):
        problem = PolynomialBox([(0,2),(0,1)],[shifted_power(0,F(1),2),
            PolynomialFactor((1,),[(1,(4,)),(F(-1,2),(2,)),(F(1,16),(0,))])],integers=[0])
        proof = solve(problem,F(1,1000),max_stages=32,time_limit=5)
        self.assertEqual(proof["retained_bounds"][0],["1","1"])
        self.assertLessEqual(F(proof["lower"]),0)
        self.assertTrue(verify_polynomial(proof)["valid"])

    def test_concave_cubic_uses_only_endpoints(self):
        problem = PolynomialBox([(0,1)],[PolynomialFactor((0,),[(1,(1,)),(F(-1,4),(2,)),(F(1,100),(3,))])])
        proof = solve(problem,0,max_stages=2)
        self.assertEqual(proof["curvature"]["caps"],["0"])
        self.assertEqual(proof["status"],"exact")
        self.assertEqual(proof["stages"][0]["grids"],[["0","1"]])
        self.assertEqual(proof["point"],["0"])
        self.assertTrue(verify_polynomial(proof)["valid"])

    def test_fixed_empty_scope_and_integer_rounding(self):
        problem = PolynomialBox([(F(-1,3),F(4,3)),(F(1,3),F(1,3))],[
            PolynomialFactor((),[(F(2,7),())]),shifted_power(0,F(2),4),shifted_power(1,F(0),3)],integers=[0])
        proof = solve(problem,0)
        self.assertEqual(problem.bounds[0],(F(0),F(1)))
        self.assertEqual(proof["status"],"exact")
        self.assertEqual(F(proof["upper"]),1+F(2,7)+F(1,27))
        self.assertTrue(verify_polynomial(proof)["valid"])

    def test_limits_keep_original_domain_proof(self):
        for options,status in (({"time_limit":0},"time_limit"),({"max_stages":0},"stage_limit"),({"max_table_states":1},"table_limit")):
            proof = solve(quartic_chain(),0,**options)
            self.assertEqual(proof["status"],status)
            self.assertTrue(verify_polynomial(proof)["valid"])
        proof = solve(quartic_chain(),0,max_stages=3)
        self.assertEqual(len(proof["stages"]),3)
        self.assertTrue(verify_polynomial(proof)["valid"])

    def test_uniform_unpruned_and_replay_callback(self):
        proof = solve(quartic_chain(),F(1,10),grid_mode="uniform",pruning=False,max_stages=20,time_limit=10)
        self.assertEqual(proof["retained_bounds"],[["-1","1"]]*3)
        calls=[]
        self.assertTrue(verify_polynomial(proof,check=lambda:calls.append(1))["valid"])
        self.assertGreater(len(calls),10)

    def test_tampering_rejected(self):
        proof = solve(quartic_chain(),0,max_stages=3)
        mutations=[lambda c:c["curvature"]["caps"].__setitem__(0,"0"),
            lambda c:c["curvature"]["diagonal_bounds"][0].__setitem__(1,"0"),
            lambda c:c["stages"][0]["messages"][0]["rows"][0].update(value="999"),
            lambda c:c["stages"][0]["next_bounds"][0].__setitem__(0,"0"),
            lambda c:c["retained_bounds"][0].__setitem__(0,"0"),
            lambda c:c.update(status="exact"),
            lambda c:c["stages"][0]["grids"][0].__setitem__(0,"-1/2")]
        for mutation in mutations:
            bad=deepcopy(proof)
            mutation(bad)
            with self.assertRaises(CertificateError): verify_polynomial(bad)

    def test_invalid_models(self):
        for terms in [[(0.5,(1,))],[(1,(-1,))],[(1,(True,))],[(1,(1,2))]]:
            with self.assertRaises(ValueError): PolynomialFactor((0,),terms)
        with self.assertRaises(ValueError):
            PolynomialBox([(0,1)]*2,[PolynomialFactor((0,1),[(1,(1,1))])],bags=[(0,),(1,)],edges=[(0,1)])
        with self.assertRaises(ValueError): PolynomialBox([(F(1,3),F(2,3))],[],integers=[0])


if __name__ == "__main__": unittest.main()
