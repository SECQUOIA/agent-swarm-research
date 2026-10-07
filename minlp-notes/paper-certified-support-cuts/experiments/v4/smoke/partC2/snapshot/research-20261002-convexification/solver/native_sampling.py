"""Cached 1D/2D polynomial sampling for floating-point cut candidates.

The optional C kernel evaluates coefficients converted to double precision. Its
output, including the NumPy fallback, is never a validity certificate. Importing
this module and calling ``sampled_features`` never runs a compiler; call
``build_native()`` explicitly before requesting the compiled implementation.
"""
from __future__ import annotations

import ctypes
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
import time

import numpy as np
import sympy as sp


_library: ctypes.CDLL | None = None
_build_attempted = False
_native_path: Path | None = None
# NumPy wins on elementary quadratic expressions; C helps repeated higher powers.
_MIN_NATIVE_POINTS = 256
_MAX_NATIVE_DEGREE = 64


def build_native(compiler: str | None = None) -> Path | None:
    """Compile/load once and return the library path, or None if unavailable.

    Build artifacts live in a private temporary directory. Failure leaves the
    deterministic NumPy implementation available and is not retried repeatedly.
    """
    global _library, _build_attempted, _native_path
    if _build_attempted:
        return _native_path
    _build_attempted = True
    executable = shutil.which(compiler or "cc")
    if executable is None:
        return None
    source = Path(__file__).with_suffix(".c")
    directory = None
    try:
        directory = Path(tempfile.mkdtemp(prefix="minlp-polynomial-sampling-"))
        target = directory / "sampling.so"
        subprocess.run(
            [executable, "-O3", "-std=c99", "-fPIC", "-shared", str(source),
             "-o", str(target)],
            check=True, capture_output=True, timeout=60,
        )
        library = ctypes.CDLL(str(target))
        vector = ctypes.POINTER(ctypes.c_double)
        indices = ctypes.POINTER(ctypes.c_size_t)
        exponents = ctypes.POINTER(ctypes.c_uint)
        library.sample_polynomials.argtypes = [
            ctypes.c_size_t, ctypes.c_size_t, ctypes.c_size_t, vector, indices,
            vector, exponents, exponents, ctypes.c_uint, ctypes.c_uint, vector,
        ]
        library.sample_polynomials.restype = ctypes.c_int
    except (OSError, subprocess.SubprocessError, AttributeError):
        if directory is not None:
            shutil.rmtree(directory, ignore_errors=True)
        return None
    _library, _native_path = library, target
    return target


@lru_cache(maxsize=128)
def _prepare(features: tuple[sp.Expr, ...], symbols: tuple[sp.Symbol, ...]):
    if len(symbols) not in (1, 2) or len(set(symbols)) != len(symbols):
        raise ValueError("sampling requires one or two distinct symbols")
    if any(not isinstance(symbol, sp.Symbol) for symbol in symbols):
        raise ValueError("sampling variables must be SymPy symbols")
    offsets, coefficients, xexponents, yexponents = [0], [], [], []
    for feature in features:
        try:
            polynomial = sp.Poly(feature, *symbols)
        except sp.PolynomialError as error:
            raise ValueError("sampling features must be polynomials") from error
        for powers, coefficient in polynomial.terms():
            if coefficient.free_symbols or coefficient.is_real is not True:
                raise ValueError("polynomial coefficients must be real constants")
            value = float(coefficient)
            if not np.isfinite(value):
                raise ValueError("polynomial coefficients must be finite in float64")
            coefficients.append(value)
            xexponents.append(powers[0])
            yexponents.append(powers[1] if len(symbols) == 2 else 0)
        offsets.append(len(coefficients))
    xdegree, ydegree = max(xexponents, default=0), max(yexponents, default=0)
    # Retain arbitrary-degree NumPy support without truncating native exponents.
    native_data = None
    if max(xdegree, ydegree) <= _MAX_NATIVE_DEGREE:
        native_data = (
            np.asarray(offsets, dtype=np.uintp),
            np.asarray(coefficients, dtype=np.float64),
            np.asarray(xexponents, dtype=np.uint32),
            np.asarray(yexponents, dtype=np.uint32),
            xdegree, ydegree,
        )
    # Numericize constants that NumPy cannot evaluate (for example zeta(3) or
    # CRootOf) while retaining the original polynomial's useful factorization.
    numeric_features = tuple(sp.N(feature, 17) for feature in features)
    function = sp.lambdify(symbols, numeric_features, modules="numpy", cse=True)
    return function, native_data


def _numpy_sample(function, points: np.ndarray, nfeatures: int) -> np.ndarray:
    if nfeatures == 0 or len(points) == 0:
        return np.empty((len(points), nfeatures), dtype=np.float64)
    values = function(*(points[:, i] for i in range(points.shape[1])))
    return np.column_stack([
        np.broadcast_to(np.asarray(value, dtype=np.float64), (len(points),))
        for value in values
    ])


def _native_sample(data, points: np.ndarray, nfeatures: int) -> np.ndarray:
    output = np.empty((len(points), nfeatures), dtype=np.float64)
    if output.size == 0:
        return output
    offsets, coefficients, xexponents, yexponents, xdegree, ydegree = data
    double_pointer = ctypes.POINTER(ctypes.c_double)
    status = _library.sample_polynomials(
        len(points), points.shape[1], nfeatures,
        points.ctypes.data_as(double_pointer),
        offsets.ctypes.data_as(ctypes.POINTER(ctypes.c_size_t)),
        coefficients.ctypes.data_as(double_pointer),
        xexponents.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        yexponents.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        xdegree, ydegree, output.ctypes.data_as(double_pointer),
    )
    if status:
        raise MemoryError("native polynomial sampler could not allocate workspace")
    return output


def sampled_features(
    features: tuple[sp.Expr, ...], symbols: tuple[sp.Symbol, ...], points: np.ndarray,
) -> np.ndarray:
    """Return values shaped (number of points, number of features).

    Expressions are real polynomials with finite float64 coefficients. Points
    must be finite, with shape (N, D), where D is one or two. The bounded cache
    stores expression preparation, never values on mutable point arrays.
    """
    features, symbols = tuple(features), tuple(symbols)
    function, data = _prepare(features, symbols)
    points = np.asarray(points, dtype=np.float64)
    if points.ndim != 2 or points.shape[1] != len(symbols):
        raise ValueError("points must have shape (N, number of symbols)")
    if not np.isfinite(points).all():
        raise ValueError("sampling points must be finite")
    if (_library is not None and data is not None
            and max(data[-2:]) >= 3 and len(points) >= _MIN_NATIVE_POINTS):
        return _native_sample(data, np.require(points, requirements=["C", "A"]), len(features))
    return _numpy_sample(function, points, len(features))


def _median_seconds(function, repeats: int = 11) -> float:
    function()
    timings = []
    for _ in range(repeats):
        start = time.perf_counter()
        for _ in range(20):
            function()
        timings.append((time.perf_counter() - start) / 20)
    return float(np.median(timings))


def benchmark() -> dict:
    """Measure reusable sampling separately from cold preparation and building."""
    start = time.perf_counter()
    path = build_native()
    build_seconds = time.perf_counter() - start
    rng = np.random.default_rng(20261002)
    x, y = sp.symbols("x y", real=True)
    cases = (
        ("univariate_square", (x,), (x*x,)),
        ("bivariate_bilinear", (x, y), (x*y,)),
        ("bivariate_quadratic_5", (x, y), (x, y, x*y, x*x, y*y)),
        ("univariate_quartic", (x,), (x**4,)),
        ("univariate_6", (x,), tuple(x**i for i in range(1, 7))),
        ("bivariate_8", (x, y), (x, y, x*y, x*x, y*y, x*x*y, x*y*y, (x-y)**4)),
        ("bivariate_24", (x, y), tuple(
            (x + sp.Rational(i, 8)*y)**4 + sp.Rational(i, 13)*x*y
            for i in range(1, 25))),
    )
    rows = []
    for name, symbols, features in cases:
        _prepare.cache_clear()
        start = time.perf_counter()
        function, data = _prepare(features, symbols)
        preparation_seconds = time.perf_counter() - start
        for npoints in (32, 256, 1024, 4096, 16384):
            points = rng.uniform(-1.0, 1.0, (npoints, len(symbols)))
            numpy_seconds = _median_seconds(lambda: _numpy_sample(function, points, len(features)))
            row = dict(case=name, points=npoints, features=len(features),
                       preparation_seconds=preparation_seconds, numpy_seconds=numpy_seconds)
            if path is not None:
                native_seconds = _median_seconds(lambda: _native_sample(data, points, len(features)))
                expected = _numpy_sample(function, points, len(features))
                actual = _native_sample(data, points, len(features))
                np.testing.assert_allclose(actual, expected, rtol=2e-13, atol=2e-13)
                row.update(native_seconds=native_seconds,
                           native_speedup=numpy_seconds/native_seconds,
                           max_absolute_difference=float(np.max(np.abs(actual-expected))))
            row.update(
                selected_backend=("native" if path is not None and
                                  max(data[-2:]) >= 3 and npoints >= _MIN_NATIVE_POINTS else "numpy"),
                public_seconds=_median_seconds(lambda: sampled_features(features, symbols, points)),
            )
            rows.append(row)
    source = Path(__file__).with_suffix(".c")
    return dict(
        platform=platform.platform(), python=platform.python_version(),
        numpy=np.__version__, sympy=sp.__version__,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        python_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        native_available=path is not None, build_seconds=build_seconds,
        native_minimum_points=_MIN_NATIVE_POINTS, rows=rows,
        scope="Floating-point polynomial sampling only; excludes separation, certificates, and solving.",
    )


if __name__ == "__main__":
    print(json.dumps(benchmark(), indent=2))
