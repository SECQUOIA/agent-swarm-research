# Independent review of the KAN rigorous-exp verifier

Review date: 2026-10-04. Scope: the six `kan_r3_h1_n4/n5/n9` and
`kan_r5_h1_n3/n5/n8` instances, the replacement of the independent verifier's
certifying exp path, and the arithmetic supporting its dual bounds for the
network relaxation R. The exactly infeasible OSIL models and the separately
certified primal points were context, not proofs rerun in this review.

**Verdict: verified within this scope, with three minor disclosure or
documentation issues below.** The diff changes only the exp enclosure and its
import. The enclosure's constants pass independent exact rational checks.
All three r3 instances were rerun to completion and reproduce every archived
result field except elapsed time. No arithmetic defect was found that
invalidates the archived KAN bounds. The three r5 full searches were not rerun;
their archive consistency, comparison with the original bounds, and targeted
exp arguments were checked. Numerical tests supplement the enclosure proof;
they do not prove it.

All executable repository sources were copied beneath `/tmp/sol-kan-review/`
before import. OSIL inputs were copied there too. Repository sources were read
only. The only repository file written by this review is this report. At most
two single-thread numerical processes ran concurrently; OpenBLAS, OpenMP, MKL
and NumExpr thread limits were set to one. No commits, project-wide checks or
CI inspections were performed.

**1. Diff and provenance.** The comparison was between
`research-20260929/reviews/wave3-verification/kan_bnb.py` and
`paper-open-minlplib/development/dossiers/ann-kan-checks/kan_bnb_rigexp.py`.
There is exactly one diff hunk: 14 added and three deleted lines, excluding
diff headers. It adds `import kan_iv as _KIV` and replaces `iexp` at lines
124–132. The new function obtains the lower endpoint from
`iexp_pt_fast(x.lo).lo` and the upper endpoint from
`iexp_pt_fast(x.hi).hi`, preserving scalar/array shapes. Monotonicity of exp
makes this an interval enclosure. No further widening is required because
those endpoints already enclose the point values.

An AST comparison, after removing just that import and the two versions of
`iexp`, finds identical syntax trees. Thus bounds, polynomial coefficients,
piece selection, search order, local optimization, tolerances, pruning and
output code are unchanged. The added import does execute `kan_iv`'s
initialization, including constant generation and its SiLU assertions; that
dependency is part of the change's trust base.

The reviewed SHA-256 hashes are:

| Source | SHA-256 |
|---|---|
| Original `kan_bnb.py` | `8ecad18222979a1964ab56fc73a8931e3ee7546977fc75acddcf343317f95d66` |
| `kan_bnb_rigexp.py` | `82ca1dbd5def9b4bb2b701650e6961b53833f0074383dce20e509d7a86b29b33` |
| `kan_decode.py` | `db515efa223f0d56cafd523abafadf72be12daac8acae856fbc1a487eb14ee9c` |
| `kan_iv.py` | `88cafda895f759e7eb5fdead9d793b6f70c0fd0b516f9b0f1b048d5f8fade38b` |
| `ia.py` | `53a35bc1661178cb3f0e0b78baca668b3a955d87e6bb9d5fde6a3912dedbc18c` |

**2. Rigorous exp enclosure.** I read `kan_iv.py` and its `ia.NI` dependency
in full. For a binary64 point x, the fast routine selects an integer m,
encloses r = x − m ln(2)/64, writes m = 64k + j with 0 ≤ j < 64, and uses

exp(x) = 2^k exp(j ln(2)/64) exp(r).

The approximate reciprocal of ln 2 and `rint` select m; they need not themselves
be an enclosure. The residual is then computed with outward interval
arithmetic, and its absolute endpoints are asserted to be at most the
binary64 value `0.0055`. Horner evaluation of the degree-eight Taylor polynomial
uses interval reciprocal factorials. Subtracting/adding `_REM2` and widening
outward covers the Taylor remainder. Multiplication by the enclosed table
entry and power-of-two scaling complete the enclosure.

The `|x| ≤ 700` assertion keeps m within a small exactly representable integer
range and k between −1010 and 1009. The final scaled endpoints are normal,
finite doubles, so `ldexp` scales them exactly. This step would require
additional rounding if extended to an underflow range. Integer conversion,
floor division and j computation are exact here. Assertions were enabled in
all runs.

Independent checks in `/tmp/sol-kan-review/audit.py` use Python `Fraction`,
not mpmath values as proof endpoints:

- ln 2 was bracketed by Σ(q=1..220) 1/(q·2^q), with tail bounded by
  1/(221·2^220). The bracket width is about 2.6854e-69. It lies inside the
  actual binary64 `LN2` endpoints, `0x1.62e42fefa39efp-1` and
  `0x1.62e42fefa39f0p-1`, and inside `LN2_64` after division by 64.
- Each of the 64 table entries was checked against rational exp bounds at
  j times the rational ln 2 endpoints divided by 64. A degree-60 series with
  an exact geometric bound on its omitted absolute terms supplies those
  bounds. All 64 pass. Their endpoint hex values and exact-check margins
  are recorded in `evidence/table-exact.json`.
- The actual floating products computing factorials 0!..18! equal their
  exact integer values. Every `_INVFACT` interval contains 1/q! exactly;
  the fast routine uses entries 0..8.
- Using the exact rational values of the binary64 cutoff and remainder
  constants, the degree-eight remainder is at most about
  1.2761149372367262e-26, below `_REM2 = 1e-25`. The degree-18 remainder used
  during module initialization is at most about 4.375210038853757e-26,
  below `_REM = 1e-21`. These comparisons account for decimal literals being
  binary64 values rather than exact decimal rationals.

`NI` widens every elementary addition, subtraction, multiplication and division
by `nextafter` in the appropriate direction. Negation and endpoint selections
are exact. The `ia` module also defines exp/log routines with empirical libm
assumptions, but none is called by this exp enclosure or its initialization.

The separate numerical check used **100 decimal digits** and 19,916 distinct
binary64 arguments. These include ±700 and adjacent floats, signed zero,
smallest signed subnormals, floats around ln(2)/64 reduction boundaries and
half-boundaries, 10,000 random values across [−700,700], arguments captured
from the full r3 searches, and six-model root/centre/Taylor probes. Every true
value lay inside the returned interval. Maximum relative interval width was
3.4474e-13, at the scale of large arguments; the minimum sampled relative
endpoint margin was 3.9442e-16. This is an enclosure test, not a relative-error
assumption on a computed exp value.

All exp arguments in the full r3 reruns were observed:

| Instance | Minimum argument | Maximum argument | Maximum residual magnitude |
|---|---:|---:|---:|
| r3 n4 | −1.8310774037467945 | 1.7659378374391452 | 0.005415205828414261 |
| r3 n5 | −1.7599015341987636 | 2.3591470607253773 | 0.005415201828420591 |
| r3 n9 | −1.7599015341987636 | 1.7659378374391452 | 0.005415207103729947 |

The r5 probes covered [−3.087302763349407, 2.999265823941238] for n3,
[−2.277352667860784, 2.2319012900017636] for n5, and
[−3.078959765092831, 2.398262654320774] for n8. Those are probe ranges,
not claimed extrema of the archived full r5 searches. The enclosure proof
applies throughout the asserted domain, so validity does not depend on
assuming that unobserved arguments stay in these narrower ranges.

**3. Other arithmetic affecting validity.** The following inventory covers
the certifying formulas and the ordinary floating computations around them.
Line numbers refer to the reviewed `kan_bnb_rigexp.py`.

| Operations | What validity relies on |
|---|---|
| `fdn`, `fup`; exact polynomial shifts and knot differences (lines 52–60, 199–259) | Decimal OSIL coefficients and bounds are decoded as exact rationals. Float conversion is checked by converting the result back to `Fraction`; one adjacent float encloses the rational. The shifts themselves use exact rational arithmetic. Floating centres and knot anchors are arbitrary exact binary64 anchors, not approximations substituted for model coefficients. |
| `Iv` operations; `isig`; SiLU values and derivatives (63–195) | IEEE binary64 elementary operations followed by one outward `nextafter`. Products consider all four endpoint products. Sigmoid denominators are positive. Negation, abs, min/max, hulls, intersections and selections do not introduce rounding error. The SiLU identities are analytic identities; the global minimum constants need a separate certificate. |
| `_zstar` (144–159) | `findroot` and ordinary mpmath exp locate a candidate. As written, mpmath interval exp certifies signs and a minimum enclosure; float conversions are padded by `1e-15`. I independently checked the actual resulting constants with rational exp intervals and a mean-value bound, eliminating reliance on mpmath correctness for these particular values. |
| Polynomial ranges, mean-value intersections, knot penalties, LB1/LB2 (261–516) | Outward interval operations and explicit `up`/`dn` at each scalar bound operation. Radii cover the interval around the chosen centre. Integer piece counts and conservative outward knot endpoints include admissible pieces. Intersections are legitimate because both operands enclose the same quantity. Penalties cover changes of the reference polynomial; the common SiLU term cancels between pieces. |
| Midpoints, coefficient centres, slope centres and Hessian centres | Ordinary floating sums/halves choose an anchor. The anchor is then treated as an exact float, and displacement or error radii are computed outward. It need not equal the real midpoint. Finite input-box centres lie inside their boxes, which also supports the displacement-sign condition used by `minquad`. |
| `minquad` (375–390) | Outward endpoint objective values and outward −g²/(2m) vertex values. The unrounded vertex division is used only for inclusion. Its `1e-9` padding is conservative for the caller's signed displacement interval, sl ≤ 0 ≤ sh, at the observed finite scales. Including an extra vertex is harmless. Unrounded `0.5*m` relies on exact power-of-two scaling without loss at a subnormal boundary; see issue 3. |
| LB3 Hessian and gradient errors, penalties, sums (519–583) | Interval differentiation of the reference network, outward componentwise Hessian radii, outward accumulated gradient/Hessian errors and penalties. `0.5` in the error sum is followed by outward rounding. All certifying sums are loops rounding outward after each addition, not unrounded NumPy reductions. |
| `eigvalsh`, `solve`, `einsum`, `est` (584–598) | Heuristics deciding whether to attempt LB3. The accepted result comes only from `_half_ginv_g`: exact rational LDLᵀ proves the float matrix positive definite and computes gᵀH⁻¹g/2 exactly, then rounds it upward. The final subtraction is downward-rounded. Wrong numerical estimates can miss a useful bound but cannot supply an unchecked bound. There is no LP solution used as a bound. |
| Objective map and certifying sums (601–625) | Outward sums; outward rational-to-float coefficient enclosures; sign-aware multiplication by positive A; outward addition of beta0 and B. |
| `vfloat_factory`, SciPy local search (643–677) | NumPy exp, unrounded polynomial evaluations, `.sum()`, objective penalties and both optimizers are heuristic. Each candidate is checked again by `Model.evaluate` using interval arithmetic and inward feasibility endpoints before it can be an incumbent. Their numerical accuracy is unnecessary for the dual certificate. |
| Random starts, widths, argpartition/argmax, bisection (680–741) | These choose search order and box splits. The children share exactly the same computed split coordinate and cover the parent; rounding the split does not create a gap. Start bounds enclose the exact input box. Time limits and heuristic selection affect completeness, not a surviving box's bound. |
| `tol`, `UB-tol`, pruning and final minimum (691–744) | The floating threshold is itself the exact dyadic number used in comparisons. A discarded box has a certified bound at least that number. UB only decreases; for the finite values and small positive tolerance here the threshold decreases with UB. Final `dn(min(threshold, open bounds))` covers discarded and open boxes. Correctness does not require interpreting the tolerance product as an exact real decimal product, or even require UB to be feasible for this lower-bound argument. |
| `check_exp` (628–640) | Diagnostic only. It still tests ordinary NumPy exp at 40 digits and has no role in the revised certificate. |

For the verifier's SiLU constants the exact checks found
`ZS_LO = -1.2784645427610748`, `ZS_HI = -1.2784645427610726`,
`SMIN_LO = -0.27846454276107474`. The derivative is negative at the left
endpoint and positive at the right endpoint. A rational mean-value lower bound
exceeds `SMIN_LO` by about 9.4524e-16. To justify the global minimum, write
s(z)=1/(1+exp(−z)) and g(z)=1+z(1−s(z)). For z<0,
g′(z)=(1−s(z))(1−z s(z))>0; for z≥0, g(z)>0. Thus the bracket contains the
unique critical point and global minimum of z s(z). The imported `kan_iv`
SiLU constants were also checked exactly.

As a targeted check of `minquad`, 2,000 finite signed-displacement cases were
compared with exact rational endpoint and admissible-vertex minima; all returned
valid lower bounds. A second complete n4 run instrumented its 79,119 quadratic
entries: no nonfinite input, no wrong displacement sign and no inexact halving
occurred. Maximum absolute displacement was 1.7326490425233891. Its result
again matched the archive. This instrumentation resolves those conditions for
that run; it is not a general proof for arbitrary inputs to `minquad`.

**4. Reproduction and six-instance archive comparison.** The first full reruns
used the unchanged copied verifier with observational wrappers around
`iexp_pt_fast`. The wrappers recorded extrema and selected arguments; the
original routine supplied every endpoint. Arguments to `bnb` were
`<name>, 4e-11, 1800, 1024`, with default seed zero and no supplied start.
The environment was Python 3.13.11, NumPy 2.5.1, SciPy 1.18.0 and mpmath 1.3.0.

| Instance | Reproduced lower bound | Processed boxes | Seconds |
|---|---:|---:|---:|
| kan_r3_h1_n4 | 0.0027812371878503973 | 26,353 | 21.29 |
| kan_r3_h1_n5 | −0.011042679449683842 | 22,301 | 20.01 |
| kan_r3_h1_n9 | 0.012963660028294303 | 42,633 | 53.78 |

Each had `done=true`, zero open boxes, and identical `UB`, `ub_u`, `tol`,
`lower_bound`, `processed` and other non-time fields to the dossier JSON.

For all six, the JSON object embedded in the `.rigexp.log` equals the companion
`.bnb.json`. Exact comparisons of archived binary64 values confirm five lower
bounds are bit-identical to the original verifier's `.bnb_v2.json`. For
`kan_r5_h1_n3`, the rigorous-exp bound is `−262.8642258941303`, lower by
exactly 3.183231456205249e-12 and still above the author's
`−262.86422590922143` by 1.5091131899680477e-8. All six rigorous-exp lower
bounds exceed their respective author bounds. The r5 n3 incumbent also changed;
the dossier's detailed rerun table correctly records this.

Commands actually run, with all repository-script imports resolving into the
copied tree, included:

```bash
diff -u research-20260929/reviews/wave3-verification/kan_bnb.py \
  paper-open-minlplib/development/dossiers/ann-kan-checks/kan_bnb_rigexp.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python -u /tmp/sol-kan-review/run_review.py kan_r3_h1_n4
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python -u /tmp/sol-kan-review/run_review.py kan_r3_h1_n5
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python -u /tmp/sol-kan-review/run_review.py kan_r3_h1_n9
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python -u /tmp/sol-kan-review/audit.py
```

The n5 and n9 commands ran sequentially in a shell loop; n4 was repeated with
the quadratic instrumentation described above. Logs and scripts remain under
`/tmp/sol-kan-review/`, especially `evidence/audit.log`,
`evidence/<name>.rerun.log`, `evidence/<name>.args.json`,
`evidence/kan_r3_h1_n4.guard-rerun.log` and `evidence/exp-test-summary.json`.
These are targeted local results, not CI results.

**5. Numbered issues.**

1. **Minor: stale exp documentation and diagnostic.** The file's introductory
   docstring still describes the empirical NumPy exp assumption, and
   `--check-exp` still checks the old exp at 40 digits. `EXPREL` remains solely
   for that diagnostic. Update the description and name the diagnostic clearly
   when packaging the artifact. None affects the revised certifying path.
2. **Minor: qualify independence and constant generation.** The revised
   independent verifier shares `kan_iv.iexp_pt_fast` and its `ia.NI` core with
   the author path, as already noted in critique C3. Also, generating constants
   with high-precision mpmath and widening one ulp is not, by itself, an exact
   proof of their accuracy. Exact rational checks prove the concrete constants
   reviewed here. Archive those checks and disclose the shared dependency;
   distinguish this checked execution from unchecked future regeneration under
   another environment. This resolves the original empirical-exp concern
   without making both implementations independent of the common exp code.
3. **Minor: `minquad` has implicit arithmetic preconditions.** The comment
   `half_m = 0.5*m # exact` is conditional: halving can round at the subnormal
   boundary. Its padded vertex-inclusion check also relies on the caller's
   sl≤0≤sh displacements. The latter follows from the finite in-box centres
   used here; both conditions were checked over the complete instrumented n4
   run. State these contracts or certify the halving when presenting this as
   a reusable general interval routine. No violation was found in the checks
   performed; this review does not certify arbitrary subnormal inputs or all
   intermediates of the unrepeated r5 searches.

**6. Precise trust base after the change.** For the reviewed execution,
the KAN dual bounds for R rely on: faithful decimal-preserving OSIL parsing;
the exact decoder's derivation of R, including class bounds and selected
polynomials; correctness of the natural, mean-value, Taylor, knot-penalty and
covering arguments; correct Python integer/Fraction arithmetic and checked
rational-to-float conversion; IEEE binary64 elementary operations and
`nextafter` with gradual underflow, finite arithmetic where the formulas
require it, and the stated exact-scaling/domain conditions; correctness of
the shared exp interval core with the actual constants certified above; and
faithful execution and recording of the search. This is a source-and-execution
review, not a machine-checked proof of the entire verifier.

The concrete mpmath-generated exp and SiLU constants were certified independently
with exact rationals, so mpmath transcendental accuracy is not a premise for
these checked constants. An unchecked fresh execution of the scripts still
generates them with mpmath and uses mpmath interval exp in `_zstar`; either
trust those computations or repeat the exact checks on its resulting constants.
NumPy exp accuracy, SciPy optimization accuracy, and LAPACK eigenvalue/linear
solve accuracy are not premises of the certifying lower bounds. Rigorously
rounded sums and exact rational LDLᵀ supply the accepted bounds. The separate
primal certificates and exact infeasibility certificates have their own trust
bases and were not replaced by this exp review.

For the paper's weaker reported L, the appropriate two-path statement is:
**with common parsing/arithmetic/exp components correct, L is valid if either
bound implementation is correct.** Agreement does not remove a common-component
failure. The reviewed exp replacement removes the empirical relative-error
assumption from path I, and the independent exact constant checks substantially
strengthen the evidence for that shared component.
