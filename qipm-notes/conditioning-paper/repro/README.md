# Reproduction package

Run from the paper directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python repro/reproduce.py
```

The program uses Python's standard library plus NumPy, SciPy, and Matplotlib. It verifies certificates, computes every table and figure, and writes `results/manifest.json`. A successful run prints `All reproduction checks passed.` No external data access is needed. The script locates all inputs relative to itself, so the working directory is not essential.

## Inputs and provenance

`data/{afiro,sc50b,adlittle}.json` defines three frozen standard-form LPs. Each JSON number is first parsed as float64 and then, for exact certificate checking, interpreted as that float's binary rational value. This convention is essential: it does not claim that presolve preserved every exact-decimal property of the original MPS. The objective offset is recorded, but cancels from objective gaps.

`data/provenance.json` records the original MPS and cached standard-form hashes, dimensions, and transformation. The original MPS models were presolved with HiGHS 1.15.1 default settings, then shifted/split/slack-converted to `Ax=b, x>=0`. No artificial bound or additional face reduction was applied. The final frozen coordinates carry the fixed Euclidean metric. Their Hessian condition numbers are not attributed to the original MPS representation.

`prepare_data.py` is the one-time capture/certificate-generation script. Its optional command is `python repro/prepare_data.py --cache /path/to/netlib`, where that cache contains the already prepared `.std` NPZ files and original `.mps` files. It reads but does not modify that source cache. It does not itself run MPS presolve; the recorded frozen arrays are the definitive numerical input. Ordinary reproduction never calls `prepare_data.py` as a script, although it imports its elementary rational linear algebra helpers.

Every input contains:

- an exactly feasible strictly positive rational point;
- a nonsingular column basis, also verified by rational elimination;
- rational `y` and `eta>=0` with `A^T y+eta c>0`, proving compactness of objective sublevels (`eta=0` proves the entire feasible set bounded);
- exactly feasible primal and dual points certifying an interval containing the optimal value.

All equalities, signs, and objective bounds above are checked with `Fraction`, without tolerances. The NumPy nullspace basis and centering calculations remain finite precision.

## Outputs and their contracts

- `fractional_sdp.csv`: 80-digit Decimal scalar formulas for all four Hessian eigenvalues and the two-dimensional section, exported as float64 numbers for plotting. A separate direct trace-product Hessian calculation at gaps `1e-2`, `1e-4`, `1e-6` must agree within relative `1e-7`. This is an independent check of formulas whose proof is in the paper.
- `simplex.csv`: 70-digit monotone scalar centering and factor-SVD condition numbers for the near-degenerate simplex, with its exact limiting formula. The internal field `theta` denotes the manuscript's perturbation parameter ϑ.
- `degenerate_lp.csv`: finite-precision continuation and the separately computed limiting matrix spectrum. The final condition-number ratio must agree within `1e-5`; stored centrality residuals expose solver quality.
- `oscillatory.csv`: 80-digit stable quadratic roots on the explicit subsequence, showing weak forcing suppression and the different relative solution error.
- `netlib.csv`: **all 81 attempted points**, including failed or unresolved rows. Newton solves use the SVD of `Diag(1/x) W`, not a normal-matrix solve. The decrement is that of `F+c^T x/mu`, not `mu F+c^T x`. Before reporting a gap, an iterate is rationally repaired to exact feasibility and its objective evaluated exactly against the certified optimum bracket.
- `netlib_summary.csv`: the last accepted point per instance, not a fitted exponent or a certified asymptotic limit.
- `cg.csv`: float64 CG on 60-dimensional synthetic two-interval matrices, with final true residual and energy error computed at 80 digits for the exact binary-rational matrix and right-hand side used by the iteration. The matrix is symmetrized before both computations. Its two spectral intervals are prescribed before floating-point construction. `cg_systems.json` stores the actual rounded matrices and right-hand sides. `cg_history.csv` retains the intermediate float64 residual and reference-spectrum diagnostics; the final high-precision results in `cg.csv` take precedence.
- `certificate_checks.json`: results of exact input checks. These certify instance hypotheses and optimal-value brackets, not floating-point Hessian eigenvalues.
- `manifest.json`: commands, environment versions, seed, precision settings, acceptance thresholds, and SHA-256 hashes of inputs, scripts, raw results, and generated TeX/PDF artifacts. The manifest excludes its own hash.

A Netlib point is accepted only if its exact rational repair is positive, maximum relative coordinate repair is at most `1e-4`, scaled equality residual is at most `1e-12`, unscaled decrement is at most `1e-5`, and its positive objective-gap bracket has relative width at most `1%`. Additionally, `eps * max(n,d) * kappa(B) <= 1e-6` is required as a conservative numerical resolution screen for the SVD factor. This last threshold is a numerical indicator, not a rigorous singular-value interval bound. Rejected points remain in the CSV and are omitted from the plotted curves. Centring statuses such as `roundoff_stop` are separate from these final acceptance tests.

The CG stopping test uses the recursive relative residual `<=1e-8`, with at most 500 iterations. True residual and energy error are separately reported. Exact arithmetic would terminate within the dimension; larger float64 counts illustrate lost conjugacy. The experiment is synthetic and makes no claim that the matrix is a Newton Hessian. The original repository's highly symmetric 40-variable toy and its unbundled high-precision claims are not used.

## Reproducibility limits

PDF creation timestamps are suppressed. Numeric CSVs and figures reproduce identically in the recorded environment. Different NumPy/SciPy/BLAS versions can perturb thresholds or signs of a nullspace basis; the qualitative conclusions are analytic theorems, not inferred from those implementation-sensitive counts. The high-precision reference solver uses only Decimal arithmetic and checks its residual before reporting CG errors. No timings, extrapolated asymptotic fits, or quantum runtime claims are generated.
