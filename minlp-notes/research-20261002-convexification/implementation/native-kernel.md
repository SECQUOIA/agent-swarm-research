# Optional polynomial sampling kernel

The prototype now has an optional C implementation of repeated polynomial
feature evaluation. It accelerates candidate generation for suitable workloads.
It does not implement nonlinear separation, exact arithmetic, certificate
checking, or a native SCIP nonlinear handler. Its microbenchmark establishes
sampling speed, not an improvement in complete solver runtime.

## Interface and validity boundary

```python
from native_sampling import build_native, sampled_features

build_native()  # Optional: compile and load once, or return None.
values = sampled_features(features, symbols, points)
```

`features` is a tuple of real polynomial SymPy expressions, `symbols` contains
one or two distinct SymPy symbols, and `points` is a finite array of shape
`(N, len(symbols))`. The result has shape `(N, len(features))`, including empty
feature tuples and empty point arrays. Noncontiguous and unaligned input arrays
are accepted; native calls receive aligned, contiguous copies when needed.
Unsupported expressions, symbolic coefficients, nonreal coefficients, and
coefficients that are not finite in float64 are rejected.

Both implementations use floating-point values. Exact polynomial coefficients
are converted to float64 only for this sampling step. A candidate direction
obtained from these samples must subsequently be checked against the original
exact expressions. Agreement between C and NumPy, even exact agreement, is not
a validity certificate. Large finite inputs can overflow during evaluation;
the caller must reject nonfinite candidate data.

Importing the module and sampling never starts a compiler. An explicit
`build_native()` uses `cc -O3 -std=c99 -fPIC -shared`, places the library in a
private temporary directory, and loads it with `ctypes`. The first build
attempt and its result are retained for the process. If temporary storage,
compilation, or loading fails, the function returns `None` and sampling
continues with NumPy. There is
no external package dependency beyond NumPy and SymPy, and no compiled binary
is stored in this repository.

Expression preparation uses a bounded cache of 128 immutable expression and
symbol tuples. It does not cache values on caller-owned mutable point arrays.
The C implementation reuses each point's integer powers across the features.
The NumPy implementation uses one cached `lambdify` function with common
subexpression elimination. It evaluates numerical constants such as `zeta(3)`
and algebraic roots before generating NumPy code, while retaining the original
polynomial's factorization.

## Dispatch and measured cost

NumPy remains the default unless the user or caller explicitly builds the
library. Even after a successful build, the public interface uses C only for
at least 256 points and an individual-variable polynomial degree between 3
and 64. Lower-degree arrays stay with NumPy. Degrees above 64 use NumPy,
avoiding an unbounded native power workspace. These are conservative
engineering choices based on this microbenchmark; they are not universal
crossover bounds.

The measurement on October 2, 2026 used Python 3.13.11, NumPy 2.5.1, SymPy
1.14.0, and Ubuntu GCC 13.3.0 on x86-64 Linux under WSL2. The library build and
load took 0.268 seconds. The script measures the median of 11 batches, each
containing 20 warmed evaluations, and reports expression preparation
separately. Other research tasks shared the host, so small timing differences
and differences between separately timed kernel and public calls should not
be interpreted precisely.

At 4,096 points, the recorded kernel times were:

| Features | NumPy (microseconds) | C (microseconds) | NumPy/C time ratio | Public choice |
| --- | ---: | ---: | ---: | --- |
| `x**2` | 5.20 | 30.20 | 0.17 | NumPy |
| `x*y` | 6.18 | 19.89 | 0.31 | NumPy |
| `x, y, x*y, x**2, y**2` | 30.81 | 48.46 | 0.64 | NumPy |
| `x**4` | 236.94 | 27.76 | 8.54 | C |
| `x, ..., x**6` | 972.95 | 43.51 | 22.36 | C |
| Eight bivariate features, including `(x-y)**4` | 303.68 | 99.21 | 3.06 | C |
| 24 shifted quartics with a bilinear term | 6176.34 | 390.89 | 15.80 | C |

The 24 quartics are `(x + i*y/8)**4 + i*x*y/13` for integer `i` from 1 to 24.
The eight-feature case is defined explicitly in `benchmark()`. The benchmark
also covers 32, 256, 1,024, and 16,384 points. A single `x**4` feature at 32
points was slower in C (17.70 versus 9.04 microseconds), which supports keeping
small arrays in NumPy. For this feature at 256 points C took 14.63 versus
21.84 microseconds. The lower-degree cases demonstrate why a point-count
threshold alone would be insufficient.

Ignoring common preparation and using the 4,096-point kernel savings, about
47 repeated calls to the 24-feature quartic case amortize the measured build
cost. The corresponding estimates are about 289 calls for six univariate
powers, 1,284 for one quartic, and 1,313 for the eight-feature bivariate case.
These estimates exclude the remaining solver work. They do not justify
building a native library for a one-off separation call. The default requires
an explicit build so applications can decide whether such reuse exists.

Preparation took approximately 1.1--5.3 milliseconds for the smaller cases
after the initial SymPy/NumPy setup; the initial square case took 66.3
milliseconds and the 24-feature case took 81.2 milliseconds. This cost is
common to both evaluation choices in this implementation. C and NumPy outputs
agreed within the benchmark's `rtol=atol=2e-13` comparison; the largest
absolute difference was about `1.42e-13`. This is numerical cross-checking
only.

## Reproduction and targeted verification

From the repository root:

```sh
python3 -m unittest discover -s research-20261002-convexification/solver -p test_native_sampling.py -v
python3 research-20261002-convexification/solver/native_sampling.py > /tmp/convexification-native-kernel-benchmark.json
```

The six targeted tests passed. They cover direct polynomial values and
agreement across implementations; constant, empty, noncontiguous, and unaligned
inputs; special numerical constants; rejection of invalid domains and features;
and continued NumPy operation without repeated build attempts when the compiler
or temporary storage is unavailable. The benchmark
completed all 35 feature-count/grid-size combinations and their numerical
comparisons. No project-wide verification or CI checks were run for this
component.

The retained [benchmark JSON](native-kernel-benchmark.json) records all timings,
runtime versions, the selected backend, and both source hashes. The C source
hash for the table above is
`b78231ad142e33a135319f6492219b1848830406728bf5db738586ea90821ff0`;
the Python source hash is
`989130d4cfa49b3930b8a9db6e295e1aac8664a51b53e684b3df55fd781dc213`.
