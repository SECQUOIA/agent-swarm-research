"""Targeted sampling contracts; no sample is treated as a validity proof."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

import numpy as np
import sympy as sp

import native_sampling as sampling


class SamplingTests(unittest.TestCase):
    def test_numpy_constants_zero_features_and_noncontiguous_points(self):
        x, y = sp.symbols("x y", real=True)
        points = np.arange(24.0).reshape(6, 4)[:, ::2] / 7
        features = (sp.Integer(3), x-y, x*y+sp.Rational(2, 7))
        expected = np.column_stack((np.full(6, 3), points[:, 0]-points[:, 1],
                                    points[:, 0]*points[:, 1]+2/7))
        with patch.object(sampling, "_library", None):
            np.testing.assert_allclose(sampling.sampled_features(features, (x, y), points), expected)
            self.assertEqual(sampling.sampled_features((), (x, y), points).shape, (6, 0))
            self.assertEqual(sampling.sampled_features(features, (x, y), points[:0]).shape, (0, 3))

    def test_compiled_agrees_with_direct_values_and_numpy(self):
        if sampling.build_native() is None:
            self.skipTest("C compiler or shared-library loading unavailable")
        x, y = sp.symbols("x y", real=True)
        rng = np.random.default_rng(1729)
        for symbols, features in (
            ((x,), (sp.Integer(0), sp.Rational(1, 3), x, x**8-3*x**2+2)),
            ((x, y), (sp.Integer(4), x*y, (x-2*y)**6+sp.Rational(2, 7)*x*y)),
        ):
            points = rng.uniform(-1, 1, (600, len(symbols)))
            actual = sampling.sampled_features(features, symbols, points)
            with patch.object(sampling, "_library", None):
                fallback = sampling.sampled_features(features, symbols, points)
            np.testing.assert_allclose(actual, fallback, rtol=2e-13, atol=2e-13)
            for i in (0, 125, 599):
                direct = [float(expression.subs(dict(zip(symbols, points[i])))) for expression in features]
                np.testing.assert_allclose(actual[i], direct, rtol=2e-13, atol=2e-13)

    def test_unaligned_native_points(self):
        if sampling.build_native() is None:
            self.skipTest("C compiler or shared-library loading unavailable")
        points = np.ndarray((256, 1), dtype=np.float64, buffer=bytearray(2049), offset=1)
        points[:, 0] = np.linspace(-1, 1, 256)
        self.assertFalse(points.flags.aligned)
        x = sp.Symbol("x", real=True)
        with patch.object(sampling, "_native_sample", wraps=sampling._native_sample) as native:
            result = sampling.sampled_features((x**3,), (x,), points)
            self.assertTrue(native.call_args.args[1].flags.aligned)
        np.testing.assert_allclose(result[:, 0], points[:, 0]**3, rtol=2e-13, atol=2e-13)

    def test_real_numeric_special_constants(self):
        x, t = sp.symbols("x t", real=True)
        constants = (sp.zeta(3), sp.CRootOf(t**5-t-1, 0))
        features = tuple(coefficient*x**3 for coefficient in constants)
        points = np.linspace(-1, 1, 256)[:, None]
        expected = np.column_stack([float(coefficient)*points[:, 0]**3 for coefficient in constants])
        with patch.object(sampling, "_library", None):
            np.testing.assert_allclose(sampling.sampled_features(features, (x,), points),
                                       expected, rtol=2e-13, atol=2e-13)
        if sampling.build_native() is not None:
            np.testing.assert_allclose(sampling.sampled_features(features, (x,), points),
                                       expected, rtol=2e-13, atol=2e-13)

    def test_build_failures_do_not_retry_or_disable_sampling(self):
        # A separate module preserves the library used by other tests.
        spec = importlib.util.spec_from_file_location("sampling_without_compiler", Path(sampling.__file__))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with patch.object(module.shutil, "which", return_value=None) as which:
            self.assertIsNone(module.build_native())
            self.assertIsNone(module.build_native())
            self.assertEqual(which.call_count, 1)
        x = sp.Symbol("x", real=True)
        points = np.linspace(-1, 1, 512)[:, None]
        np.testing.assert_allclose(module.sampled_features((x*x,), (x,), points)[:, 0], points[:, 0]**2)
        spec.loader.exec_module(module)
        with patch.object(module.shutil, "which", return_value="cc"), \
                patch.object(module.tempfile, "mkdtemp", side_effect=OSError("storage unavailable")) as temporary:
            self.assertIsNone(module.build_native())
            self.assertIsNone(module.build_native())
            self.assertEqual(temporary.call_count, 1)
        np.testing.assert_allclose(module.sampled_features((x*x,), (x,), points)[:, 0], points[:, 0]**2)

    def test_invalid_domains_and_nonpolynomial_features_fail(self):
        x, y = sp.symbols("x y", real=True)
        cases = (
            ((sp.sin(x),), (x,), np.zeros((1, 1))),
            ((y*x,), (x,), np.zeros((1, 1))),
            ((sp.I*x,), (x,), np.zeros((1, 1))),
            ((x,), (x,), np.zeros((2, 2))),
            ((x,), (x,), np.array([[np.nan]])),
            ((x,), (x, x), np.zeros((1, 2))),
        )
        for features, symbols, points in cases:
            with self.subTest(features=features, symbols=symbols, points=points):
                with self.assertRaises(ValueError):
                    sampling.sampled_features(features, symbols, points)


if __name__ == "__main__":
    unittest.main()
