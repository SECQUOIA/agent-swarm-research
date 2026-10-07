"""Independent checks of the original-model and emitted-row trust boundaries.

The support algorithms have separate analytic tests. These regressions inspect
the SCIP models and actual separator API calls, where a correct support proof
could otherwise be attached to the wrong graph, domain, or coefficient vector.
"""

from dataclasses import replace
from fractions import Fraction as Q
from math import inf, nextafter
from pathlib import Path
from types import MethodType, SimpleNamespace
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solver import integration as api
from solver.certified import replay_support


def row(nl=None, *, lin=None, quad=(), lb=-inf, ub=inf):
    return dict(nl=nl, lin={} if lin is None else lin, quad=list(quad), lb=lb, ub=ub)


def instance(rows, *, bounds=((0, 1),), sense="min", constant=0):
    return api.Instance("source_model_review", [b[0] for b in bounds],
                        [b[1] for b in bounds], ["C"] * len(bounds),
                        sense, constant, rows)


class NativeModelReview(unittest.TestCase):
    def assert_native_point(self, model, values, *, feasible, objective=None):
        solution = model.createOrigSol()
        try:
            variables = {v.name: v for v in model.getVars()}
            for name, value in values.items():
                model.setSolVal(solution, variables[name], value)
            self.assertEqual(model.checkSol(solution, printreason=False,
                                            completely=True, original=True), feasible)
            if objective is not None:
                self.assertAlmostEqual(model.getSolObjVal(solution), objective)
        finally:
            model.freeSol(solution)

    def test_complete_row_binding_handles_cancellation_between_distinct_exact_atoms(self):
        square = ("square", ("var", 0))
        product = ("times", ("var", 0), ("var", 0))
        # Each atom separately has exact native coefficients. Native assembly
        # can nevertheless turn this complete source row x² into zero, while
        # separate square/product auxiliaries prevent that cancellation.
        tree = ("sum", ("times", ("num", 1e16), square), product,
                ("times", ("num", -1e16), square))
        fixtures = (
            (instance([row(tree), row(lin={0: 1}, lb=0.5, ub=0.5)]), 0.25),
            (instance([row(lin={0: 1}), row(tree, lb=0.2, ub=0.3),
                       row(lin={0: 1}, lb=0.5, ub=0.5)]), 0.5),
        )
        for inst, expected in fixtures:
            for mode in ("baseline", "control", "all", "auto"):
                with self.subTest(mode=mode, constrained=len(inst.rows) == 3):
                    try:
                        result = api.run_instance(inst, mode, time_limit=3)
                    except ValueError as exc:
                        # Explicit refusal is sound; silent different models
                        # or source-infeasible solver results are not.
                        self.assertRegex(str(exc).lower(), "source|native|bind|round|represent|semantic")
                        continue
                    if result["status"] == "source_model_mismatch":
                        self.assertIsNone(result["primal"])
                        self.assertIsNone(result["dual"])
                        self.assertEqual(result["cuts"], [])
                        continue
                    self.assertIn(result["status"], ("optimal", "gaplimit"))
                    self.assertAlmostEqual(result["primal"], expected)

    def test_cancelled_source_domain_operations_are_enforced_or_explicitly_refused(self):
        root = ("sqrt", ("var", 0))
        log = ("log", ("var", 0))
        reciprocal = ("divide", ("num", 1.0), ("var", 0))
        fixtures = (
            (("times", ("num", 0.0), root), -0.5),
            (("sum", root, ("negate", root)), -0.5),
            (("times", ("num", 0.0), log), -0.5),
            (("sum", log, ("negate", log)), -0.5),
            (("power", root, ("num", 0.0)), -0.5),
            (("times", ("num", 0.0), reciprocal), 0.0),
        )
        for tree, fixed in fixtures:
            inst = instance([row(lin={0: 1}), row(tree, ub=1),
                             row(lin={0: 1}, lb=fixed, ub=fixed)], bounds=((-1, 1),))
            for mode in ("baseline", "control", "all", "auto"):
                with self.subTest(mode=mode, tree=tree):
                    try:
                        result = api.run_instance(inst, mode, time_limit=3)
                    except ValueError as exc:
                        self.assertRegex(str(exc).lower(), "source|native|domain|bind|represent|semantic")
                        continue
                    self.assertIn(result["status"], ("infeasible", "source_model_mismatch"))
                    self.assertIsNone(result["primal"])
                    if result["status"] == "source_model_mismatch":
                        self.assertIsNone(result["dual"])
                        self.assertEqual(result["cuts"], [])

    def test_rewritten_row_is_checked_even_when_original_native_row_is_exact(self):
        square = ("square", ("var", 0))
        product = ("times", ("var", 0), ("var", 0))
        power = ("power", ("var", 0), ("num", 2.0))
        tree = ("sum", ("times", ("num", 1e16), square),
                ("times", ("num", -1e16), product), square, ("negate", power),
                ("times", ("num", -1e16), square),
                ("times", ("num", 1e16), product))
        # Source and original native objective are zero. Auxiliaries collect
        # coefficients by source-tree identity: square's 1e16+1-1e16 becomes
        # zero, product's -1e16+1e16 is zero, and -power is left. Expanding
        # these admitted auxiliaries therefore exposes a rewritten -x² row.
        fixtures = (
            (instance([row(tree), row(lin={0: 1}, lb=0.5, ub=0.5)]), 0.0),
            (instance([row(lin={0: 1}), row(tree, lb=0, ub=0),
                       row(lin={0: 1}, lb=0.5, ub=0.5)]), 0.5),
        )
        for inst, expected in fixtures:
            for mode in ("baseline", "control", "all", "auto"):
                with self.subTest(mode=mode, constrained=len(inst.rows) == 3):
                    result = api.run_instance(inst, mode, time_limit=3)
                    self.assertIn(result["status"], ("optimal", "gaplimit"))
                    self.assertAlmostEqual(result["primal"], expected)

    def test_source_tree_dedup_preserves_distinct_expression_domains(self):
        square = ("square", ("var", 0))
        restricted = ("power", ("sqrt", ("var", 0)), ("num", 4.0))
        inst = instance([row(("sum", square, restricted, square))],
                        bounds=((-1, 1),), constant=3)
        detected = api.discover(inst)
        self.assertEqual(len(detected.atoms), 2)
        self.assertEqual(detected.atoms[0].expr, detected.atoms[1].expr)
        self.assertEqual(detected.rewritten_rows[0],
                         ("sum", ("uni", 0), ("uni", 1), ("uni", 0)))
        for mode in ("baseline", "control"):
            with self.assertRaisesRegex(api.SourceModelMismatch, "domain"):
                api._build(inst, detected, mode)
        # Accepted models must prove every source operation's domain on the
        # original box. The distinct source definitions remain on a safe box.
        inst = replace(inst, var_lb=[0])
        detected = api.discover(inst)
        self.assertEqual(len(detected.atoms), 2)
        for mode in ("baseline", "control"):
            model, _, aux = api._build(inst, detected, mode)
            model.hideOutput()
            try:
                for x in (0, 0.5, 1):
                    values = {"v0": x, "objective_aux": 3*x*x + 3}
                    values.update({v.name: x*x for v in aux.values()})
                    self.assert_native_point(model, values, feasible=True)
            finally:
                model.freeProb()

    def test_auxiliary_definitions_and_objective_sense_bind_original_coordinates(self):
        # Original objective: 2*x + x*y - 3*x² + 7; at (1/2,1/4), it is 59/8.
        inst = instance([row(("times", ("num", -3.0), ("square", ("var", 0))),
                             lin={0: 2.0}, quad=[(0, 1, 1.0)])],
                        bounds=((0, 1), (0, 1)), constant=7)
        for sense in ("min", "max"):
            inst.obj_sense = sense
            detected = api.discover(inst)
            for mode in ("baseline", "control"):
                model, _, aux = api._build(inst, detected, mode)
                model.hideOutput()
                try:
                    values = {"v0": 0.5, "v1": 0.25, "objective_aux": 59/8}
                    for atom in detected.atoms:
                        if atom.index in aux:
                            values[aux[atom.index].name] = (0.25 if atom.variables == (0,) else 0.125)
                    self.assert_native_point(model, values, feasible=True, objective=59/8)
                    bad = dict(values, objective_aux=59/8 + (-1 if sense == "min" else 1))
                    self.assert_native_point(model, bad, feasible=False)
                    if aux:
                        bad = dict(values)
                        bad[next(iter(aux.values())).name] += 0.125
                        self.assert_native_point(model, bad, feasible=False)
                finally:
                    model.freeProb()

    def test_constant_infeasible_rows_survive_both_model_builds(self):
        fixtures = (row(lb=1), row(ub=-1), row(lb=2, ub=2),
                    row(("num", 3.0), lb=0, ub=2))
        for constraint in fixtures:
            inst = instance([row(lin={0: 1.0}), constraint], constant=4)
            for mode in ("baseline", "control"):
                model, _, _ = api._build(inst, api.discover(inst), mode)
                model.hideOutput()
                try:
                    model.optimize()
                    self.assertEqual(str(model.getStatus()), "infeasible")
                finally:
                    model.freeProb()

    def test_atom_limit_keeps_omitted_original_nonlinear_and_quadratic_terms(self):
        inst = instance([row(("sum", ("square", ("var", 0)),
                                    ("square", ("var", 1))),
                             quad=[(0, 1, 2.0)])], bounds=((0, 1), (0, 1)))
        detected = api.discover(inst, replace(api.Config(), max_atoms=1))
        self.assertEqual(len(detected.atoms), 1)
        self.assertTrue(detected.stats["atom_cap_reached"])
        self.assertEqual(detected.rewritten_rows[0],
                         ("sum", ("uni", 0), ("square", ("var", 1))))
        self.assertEqual(detected.quadratic_atoms, {})
        model, _, _ = api._build(inst, detected, "control")
        model.hideOutput()
        try:
            # (x+y)^2 at (1/2,1/4) is 9/16. Both omitted terms are necessary.
            values = {"v0": 0.5, "v1": 0.25, "block_aux_0": 0.25,
                      "objective_aux": 9/16}
            self.assert_native_point(model, values, feasible=True)
            self.assert_native_point(model, dict(values, objective_aux=0.25), feasible=False)
        finally:
            model.freeProb()

    def test_exact_original_rows_are_retained_without_presolve_bound_substitution(self):
        inst = instance([row(quad=[(0, 2, 1.0)]),
                         row(lin={0: 0.1, 2: 0.3}, lb=0.2, ub=0.4),
                         row(lin={0: 1}, lb=0.25, ub=0.75)],
                        bounds=((0, 1), (-5, 5), (0, 1)))
        detected = api.discover(inst)
        block, = detected.blocks
        self.assertEqual(block.variables, (0, 2))
        self.assertEqual(block.box, ((0, 1), (0, 1)))
        self.assertEqual(block.rows, (((0.1, 0.3), 0.4), ((-0.1, -0.3), -0.2),
                                      ((1.0, 0.0), 0.75), ((-1.0, -0.0), -0.25)))
        api._initialize_screen(block, detected)
        self.assertEqual(block.screening_cache.bounds, ((Q(0), Q(1)), (Q(0), Q(1))))
        self.assertEqual(block.screening_cache.rows[0], (Q(0.1), Q(0.3), Q(0.4)))
        model, _, _ = api._build(inst, detected, "control")
        model.hideOutput()
        try:
            model.presolve()
            # Original support domain remains the one bound into every proof.
            self.assertEqual(block.box, ((0, 1), (0, 1)))
            self.assertEqual(inst.var_lb, [0, -5, 0])
            self.assertEqual(inst.var_ub, [1, 5, 1])
        finally:
            model.freeProb()


class SourceScreeningReview(unittest.TestCase):
    def test_simplified_polynomial_with_source_domain_hole_has_no_screen_cache(self):
        restricted = (
            ("power", ("sqrt", ("var", 0)), ("num", 4.0)),
            ("divide", ("power", ("var", 0), ("num", 3.0)), ("var", 0)),
        )
        for tree in restricted:
            detected = api.discover(instance([row(tree)], bounds=((-1, 1),)))
            block, = detected.blocks
            self.assertEqual(block.features[-1], block.symbols[0]**2)
            api._initialize_screen(block, detected)
            self.assertIsNone(block.screening_cache)

    def test_screening_evaluates_exact_binary_constants_and_source_row_feasibility(self):
        tree = ("times", ("num", 0.1), ("var", 0), ("var", 1))
        detected = api.discover(instance([row(tree), row(lin={0: 1}, ub=0.3)],
                                         bounds=((0, 1), (0, 1))))
        block, = detected.blocks
        api._initialize_screen(block, detected)
        samples = block.screening_cache.bind([(Q(1, 4), Q(1, 2))])
        self.assertEqual(samples.values[0][-1].lower, Q(1, 4) * Q(1, 2) * Q(0.1))
        # Decimal 3/10 exceeds the original binary64 row endpoint 0.3.
        with self.assertRaisesRegex(ValueError, "affine row"):
            block.screening_cache.bind([(Q(3, 10), Q(1, 2))])


class RecordedRow(dict):
    def isLocal(self):
        return self.get("local", False)

    def getCols(self):
        return [SimpleNamespace(getVar=lambda name=name: SimpleNamespace(name=name))
                for name, _ in self["columns"]]

    def getVals(self):
        return [coefficient for _, coefficient in self["columns"]]

    def getLhs(self):
        return self["lhs"]

    def getConstant(self):
        return self.get("constant", 0)

    def getRhs(self):
        return 1e20 if self["rhs"] is None else self["rhs"]


class RecordedModel:
    """Focused SCIP API recorder; values are indexed by original columns."""

    def __init__(self, values):
        self.values = values
        self.rows = []
        self.depth = 0

    def getDepth(self):
        return self.depth

    def getSolVal(self, solution, variable):
        return self.values[variable.name]

    def getTransformedVar(self, variable):
        return SimpleNamespace(name="transformed_" + variable.name,
                               getLbGlobal=lambda: -1e20, getUbGlobal=lambda: 1e20)

    def infinity(self):
        return 1e20

    def createEmptyRowSepa(self, separator, name, **kwargs):
        result = RecordedRow(name=name, columns=[], **kwargs)
        self.rows.append(result)
        return result

    def cacheRowExtensions(self, row):
        pass

    def addVarToRow(self, row, variable, coefficient):
        row["columns"].append((variable.name, coefficient))

    def flushRowExtensions(self, row):
        pass

    def addCut(self, row, *, forcecut):
        row["forcecut"] = forcecut
        return False

    def releaseRow(self, row):
        row["released"] = True


class EmittedRowReview(unittest.TestCase):
    def test_row_audit_rejects_changed_coefficients_bounds_or_unexplained_substitution(self):
        model = RecordedModel({})
        variables = [SimpleNamespace(name="v0"), SimpleNamespace(name="v2")]
        coefficients, rhs = (0.125, -1.0), -1/64

        def valid_row():
            return RecordedRow(columns=[("transformed_v0", 0.125), ("transformed_v2", -1.0)],
                               lhs=rhs, rhs=None, constant=0)

        self.assertIsNotNone(api._audit_inserted_row(model, valid_row(), variables, coefficients, rhs))
        mutations = (
            lambda r: r["columns"].__setitem__(0, ("transformed_v0", nextafter(0.125, inf))),
            lambda r: r["columns"].__setitem__(0, ("transformed_v1", 0.125)),
            lambda r: r["columns"].pop(),
            lambda r: r.update(lhs=nextafter(rhs, inf)),
            lambda r: r.update(constant=2**-40),
            lambda r: r.update(rhs=10),
            lambda r: r.update(local=True),
        )
        for mutate in mutations:
            candidate = valid_row()
            mutate(candidate)
            self.assertIsNone(api._audit_inserted_row(model, candidate, variables, coefficients, rhs))

    def test_uncertified_presolve_fixing_does_not_authorize_column_substitution(self):
        model = RecordedModel({})
        variables = [SimpleNamespace(name="v0"), SimpleNamespace(name="v2")]
        original_getter = model.getTransformedVar

        def transformed(variable):
            if variable.name == "v0":
                return SimpleNamespace(name="transformed_v0", getLbGlobal=lambda: 0.5,
                                       getUbGlobal=lambda: 0.5)
            return original_getter(variable)

        model.getTransformedVar = transformed
        candidate = RecordedRow(columns=[("transformed_v2", -1.0)],
                                lhs=-1/64, rhs=None, constant=1/16)
        # The arithmetic substitution is exact, but its fixing came from
        # numerical presolve and has no proof against the original model.
        self.assertIsNone(api._audit_inserted_row(model, candidate, variables, (0.125, -1.0), -1/64))

    def test_actual_global_row_uses_certified_coefficients_rhs_and_original_domain(self):
        inst = instance([row(quad=[(0, 2, 1.0)]), row(lin={0: 1, 2: 1}, ub=1)],
                        bounds=((0, 1), (-5, 5), (0, 1)))
        detected = api.discover(inst)
        block, = detected.blocks
        xs = [SimpleNamespace(name=f"v{i}") for i in range(3)]
        aux = {0: SimpleNamespace(name="block_aux_0")}
        config = replace(api.Config(), max_cuts=1)
        separator = api.BlockSeparator(detected, xs, aux, "all", config, 10)
        # The extension class restricts model to a real SCIP instance. Calling
        # its callback unbound lets this test record every row API argument.
        callback = SimpleNamespace(**separator.__dict__)
        callback._find_support = MethodType(api.BlockSeparator._find_support, callback)
        callback.model = RecordedModel({"v0": 0.5, "v2": 0.5, "block_aux_0": 0.5})
        coefficients = (0.125, 0.375, -1.0)
        # On x,y>=0, x+y<=1, min(x/8+3y/8-xy)=-1/64 at (5/8,3/8).
        with patch.object(api, "propose_direction", return_value=(coefficients, -0.25, -1/64)):
            result = api.BlockSeparator.sepaexeclp(callback)
        self.assertEqual(result["result"], api.ps.SCIP_RESULT.SEPARATED)
        emitted, = callback.model.rows
        self.assertEqual(emitted["columns"], [("transformed_v0", 0.125),
                                               ("transformed_v2", 0.375),
                                               ("transformed_block_aux_0", -1.0)])
        self.assertEqual(emitted["lhs"], -1/64)
        self.assertIsNone(emitted["rhs"])
        self.assertFalse(emitted["local"])
        self.assertTrue(emitted["released"])
        record, = callback.records
        self.assertEqual(record["coefficients"], list(coefficients))
        self.assertEqual(record["rhs"], emitted["lhs"])
        self.assertEqual(record["column_names"], ["v0", "v2", "block_aux_0"])
        self.assertEqual(record["box"], [[0, 1], [0, 1]])
        self.assertEqual(record["rows"], [[[1.0, 1.0], 1.0]])
        self.assertTrue(replay_support(block.features, block.symbols, block.box,
                                       coefficients, block.rows, record["certificate"]))
        callback.model.depth = 1
        self.assertEqual(api.BlockSeparator.sepaexeclp(callback)["result"],
                         api.ps.SCIP_RESULT.DIDNOTRUN)
        self.assertEqual(len(callback.model.rows), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
