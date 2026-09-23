"""Solver-free checks of the separate farm initialization followup."""
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch
import pyomo.environ as pe
from pyomo.gdp import Disjunct
from pyomo.opt import WriterFactory
from pyomo.solvers.plugins.solvers.GAMS import check_expr_evaluation
import lbesh_legacy_initialization as followup


def algebra(model):
    return dict(variables=[(v.name, v.bounds, v.fixed) for v in model.component_data_objects(
                    pe.Var, active=None, descend_into=(pe.Block, Disjunct))],
                constraints=[(c.name, str(c.expr), c.active) for c in model.component_data_objects(
                    pe.Constraint, active=None, descend_into=(pe.Block, Disjunct))],
                objectives=[(o.name, str(o.expr), o.sense) for o in model.component_data_objects(pe.Objective)])


class FarmInitializationContracts(unittest.TestCase):
    def test_all_seven_keep_algebra_bounds_bigm_and_emit_valid_initial_levels(self):
        for name in followup.INSTANCES[:-1]:
            with self.subTest(name=name):
                source = followup.primary._build(name)
                initialized = source.clone()
                before = algebra(source)
                changes = followup.initialize_widths(initialized)
                self.assertEqual(algebra(initialized), before)
                self.assertEqual({x['variable'] for x in changes}, {v.name for v in source.plot_width.values()})
                for change in changes:
                    self.assertIsNone(change['old_value'])
                    self.assertGreater(change['new_value'], 0)
                pe.TransformationFactory('gdp.bigm').apply_to(source)
                pe.TransformationFactory('gdp.bigm').apply_to(initialized)
                self.assertEqual(algebra(source), algebra(initialized))
                check_expr_evaluation(initialized, None, 'shell')
                output = io.StringIO()
                _, symbols = WriterFactory('gams')(initialized, output, lambda _: True, {})
                for variable in initialized.plot_width.values():
                    self.assertIn(symbols.getSymbol(variable) + '.l = ', output.getvalue())

    def test_three_methods_call_identical_frozen_adapter_and_do_not_export_initialization(self):
        fake = dict(native_gams={'OBJVAL': None}, has_solution=False, dual_bound=0,
                    bound_valid=True, options={'retained_native_options': True})
        for method in followup.METHODS:
            with self.subTest(method=method), tempfile.TemporaryDirectory() as tmp:
                with patch.object(followup.primary, '_gams', return_value=fake) as adapter:
                    rec = followup.run_one(followup.INSTANCES[0], method, Path(tmp))
                args = adapter.call_args.args
                self.assertEqual(args[1:], (method.split('-')[1], 'bigm', 120., 1, Path(tmp), 1))
                self.assertEqual(adapter.call_args.kwargs, {})
                self.assertEqual(rec['options'], fake['options'])
                self.assertIsNone(rec['witness'])
                self.assertFalse(rec['assessment']['solved'])

    def test_invalid_returned_witness_rejected_by_original_model(self):
        def fake(model, *args):
            for var in model.component_data_objects(pe.Var, active=None, descend_into=(pe.Block, Disjunct)):
                if var.value is None:
                    var.set_value(0, skip_validation=True)
            return dict(native_gams={'OBJVAL': 0}, has_solution=True, dual_bound=0, bound_valid=True)
        with tempfile.TemporaryDirectory() as tmp, patch.object(followup.primary, '_gams', side_effect=fake):
            rec = followup.run_one(followup.INSTANCES[0], followup.METHODS[0], Path(tmp))
        self.assertEqual(rec['outcome'], 'completed')
        self.assertFalse(rec['validation']['feasible'])
        self.assertFalse(rec['assessment']['solved'])

    def test_declared_schedule_is_complete_and_legacy_sources_are_hashed(self):
        plan = followup.schedule(1, 20260927)
        self.assertEqual(len(plan['instances']), 8)
        self.assertEqual(len(plan['methods']), 3)
        self.assertEqual(len(set(map(tuple, plan['ordered_jobs']))), 24)
        self.assertEqual(set(map(tuple, plan['ordered_jobs'])),
                         {(name, method) for name in followup.INSTANCES for method in followup.METHODS})
        self.assertEqual((plan['time_limit'], plan['wall_limit'], plan['threads']), (120, 150, 1))
        self.assertIn('instances/pyomo_examples_src/examples/gdp/farm_layout/farm_layout.py',
                      plan['metadata']['source_sha256'])
        with patch.object(followup, 'ADAPTER_SHA256', 'incorrect'):
            with self.assertRaisesRegex(RuntimeError, 'adapter hash'):
                followup.metadata()

    def test_nonpositive_or_wrong_affine_bound_is_refused(self):
        model = followup.primary._build(followup.INSTANCES[0])
        model.width_bounds[1].set_value((0, model.plot_width[1], 30))
        with self.assertRaisesRegex(ValueError, 'positive'):
            followup.initialize_widths(model)
        model.width_bounds[1].set_value((1, 2 * model.plot_width[1], 30))
        with self.assertRaisesRegex(ValueError, 'direct affine'):
            followup.initialize_widths(model)

    def test_unused_batch_initialization_is_valid_preserved_by_loader_and_algebra_unchanged(self):
        from pyomo.opt import SolverResults, SolverStatus
        model = followup.primary._build('gdplib.batch_processing')
        before = algebra(model)
        uninitialized = model.clone()
        changes = followup.initialize_model('gdplib.batch_processing', model)
        self.assertEqual(algebra(model), before)
        self.assertEqual([c['variable'] for c in changes], ['storageTankSize_log[10]'])
        var = model.storageTankSize_log[10]
        self.assertEqual(var.value, var.lb)
        results = SolverResults()
        results.solver.status = SolverStatus.ok
        solution = results.solution.add()
        solution._cuid = False
        solution.variable['volume_log[1]'] = {'Value': model.volume_log[1].lb}
        model.solutions.load_from(results)
        self.assertEqual(var.value, var.lb)
        self.assertTrue(var.stale)
        pe.TransformationFactory('gdp.bigm').apply_to(uninitialized)
        pe.TransformationFactory('gdp.bigm').apply_to(model)
        self.assertEqual(algebra(uninitialized), algebra(model))
        model.sentinel = pe.Constraint(expr=var >= var.lb)
        with self.assertRaisesRegex(ValueError, 'referenced by sentinel'):
            followup.initialize_model('gdplib.batch_processing', model)

    def test_timeout_kills_entire_worker_group_and_ignores_partial_result(self):
        process = Mock(pid=23456)
        process.wait.side_effect = [subprocess.TimeoutExpired('worker', 150), -9]
        with tempfile.TemporaryDirectory() as tmp:
            def launch(command, **kwargs):
                Path(command[-1]).write_text(json.dumps({'outcome': 'completed'}))
                return process
            with patch.object(followup.subprocess, 'Popen', side_effect=launch) as spawn, \
                 patch.object(followup.os, 'killpg', side_effect=ProcessLookupError) as kill:
                rec = followup.execute(followup.INSTANCES[0], followup.METHODS[0], Path(tmp))
            self.assertEqual(rec['outcome'], 'wall_timeout')
            self.assertFalse(rec['bound_valid'])
            kill.assert_called_once_with(23456, followup.signal.SIGKILL)
            self.assertTrue(spawn.call_args.kwargs['start_new_session'])
            self.assertEqual(spawn.call_args.kwargs['env']['OMP_NUM_THREADS'], '1')
            self.assertIn('lbesh_legacy_initialization.py', spawn.call_args.args[0][1])


if __name__ == '__main__':
    unittest.main()
