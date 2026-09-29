# Independent review of the finite-state kernel extension

Date: 2026-09-28. Reviewed and revised
[mixed-discrete-extension.md](mixed-discrete-extension.md) against the
explicit rational kernel interface in
[sparse-kernel-rounding.md](sparse-kernel-rounding.md).

**Verdict:** The mixed-state theorem follows from the companion kernel
under the stated total-degree preordering constraints. No additional
continuous-domain hypothesis is hidden in the extension: every label must
share the same full box. The finite-state labels are preserved exactly.
An independent subreview checked the mass bounds, zero-mass annihilation,
pruning, and strict feasibility. These proof reviews are evidence, not a
machine-checked proof or a publication-priority finding.

## Corrections and explicit conventions

The preceding draft deferred the degree interface and used an abstract
Jackson estimate with a `pi^2` constant. The revised theorem uses exactly
`r>=max(w,d)`, `m=floor(r/w)+1`, and `delta_r=3/(2m^2+1)`. The local kernel
certificate has total degree at most `2|C_b|(m-1)<=2r`. Objective moment
control uses `deg f_{b,a}<=r`. All-discrete models (`w=0`) are handled
separately and exactly, without forming `r/w`.

The preceding draft's sentence about algebraic kernel coefficients was
replaced: the chosen squared-Fejer kernel has rational coefficients.
Chebyshev extraction nodes are real algebraic, so this correction supplies
no rational-output or bit-complexity guarantee.

The relaxation's *optimum* is a lower bound. An arbitrary feasible moment
objective need not be a lower bound. The revised text distinguishes these
statements while retaining rounding for every feasible moment point.

## Adversarial proof checks

1. **State sums on mixed separators.** Marginalizing a bag requires summing
   all its local labels with the same separator assignment. Individual
   labelled functionals cannot be equated across bags. The revised
   definition imposes equations for every separator assignment, including
   those with an empty fiber on one side. This last condition is necessary:
   if two adjacent bags allow only shared values `0` and `1`, respectively,
   restricting equations to assignments allowed on both sides would leave
   an infeasible discrete model spuriously feasible.

2. **No lost integrality.** Each `h_{b,a}` is a nonnegative density of mass
   `tau_{b,a}`. Smoothing touches only continuous coordinates. Equation (2)
   makes the *mixed* separator measures equal, after summing label fibers.
   Gluing yields a global law, and the finite union of forbidden-label
   events remains null. Zero-mass separator events can receive arbitrary
   conditional laws without changing any bag marginal.

3. **Mass scaling, including zero.** The truncated Chebyshev identity gives
   `0<=L(T_alpha^2)<=tau` for `|alpha|<=r`. Moment Cauchy--Schwarz gives
   `|L(T_alpha)|^2<=tau L(T_alpha^2)<=tau^2`. This uses no normalization
   by `tau`. The zero-mass case therefore has exactly zero cost error.
   Summing label errors gives the stronger mass-weighted bound before the
   bagwise maximum is taken.

4. **Entire zero-mass blocks vanish.** When `tau=0`, every diagonal in the
   Chebyshev moment basis of degree at most `r` is zero. Positive
   semidefiniteness makes every matrix entry zero. Products of two
   degree-at-most-`r` polynomials span all moments through `2r`.
   The independent subreview also supplied a separate monomial proof:
   singleton box localizers imply
   `0<=L(x^(2alpha))<=L(x^(2(alpha-e_i)))<=tau`, and Cauchy--Schwarz then
   bounds every moment through `2r` by `tau` in absolute value.

5. **Pruning and Slater.** Separator mass equations first give a genuine
   global finite-state law. An unextendable local label must have zero
   mass, hence zero entire functional by the preceding check. Pruning
   therefore preserves the primal feasible set and objective after zero
   blocks are identified. A positive distribution over all feasible global
   labels, independent of a positive-density box measure, makes every
   retained localizing matrix positive definite. Empty continuous bags
   give positive scalar blocks. Redundant equality rows do not obstruct
   this conic Slater condition. Dual attainment is asserted directly for
   the pruned finite SDP; no unsupported transfer to an unpruned dual is
   used.

6. **Finite-grid consequence.** For `w>=1`, the companion quadrature degree
   `N=m+floor(d_infty/2)` integrates every labelled density and its cost
   product exactly. Label sums commute with finite quadrature. Thus the
   same mixed separator equalities survive on the grid. This is established
   tree optimization applied to the resulting finite tables; it is not a
   new dynamic-programming algorithm or a general polynomial-time MINLP
   result.

## Targeted computational verification

Command actually run:

```text
python research-20260928/solver/check_mixed_discrete.py
```

Result: **PASS**. The script uses exact `Fraction` arithmetic. At moment
orders `r=2,4,6`, it checks a three-bag mixed tree, including an empty
continuous bag, globally unextendable labels, and extendable labels of
zero mass. It verifies 759 exact density evaluations, full polynomial
separator identities after summing labels, unit total bag masses,
Chebyshev diagonalization, the mass-weighted objective-error inequality,
and pruning against exhaustive enumeration of 12 feasible global labels.
An additional all-discrete check confirms the cost comparison in that
finite example.

These test functionals come from a genuine finite global measure. The
checks challenge state indexing, tensor-degree conventions, signs,
normalization, and edge-case handling. They do **not** prove nonnegativity
for arbitrary nonrepresentable truncated functionals, universal gluing,
or Slater; those conclusions rely on the proofs above and the companion
kernel theorem. No numerical SDP solve or Lean verification was performed.
No project-wide checks or CI inspection were run.

## Significance and literature limits

The local materials examined were the companion kernel theorem,
[its independent prior-work audit](prior-independent.md), and
[its parallel audit](kernel-prior.md). The latter audits contain the
primary-source comparisons, including the existing sparse convergence
bounds, dense box-kernel results, tree measure gluing, mixed-integer
bounded-treewidth approximation, and second-order grid approximation.
This extension review did not conduct an additional primary-source search
and does not certify separate novelty for the labelled formulation.

The extension's proved contribution is a precise transfer of the box
hierarchy bound to a finite-state model with exact local combinatorial
feasibility. It does not cover label-dependent continuous bounds, arbitrary
continuous constraints, or the smaller quadratic-module hierarchy.
Exponential label lists and the elementary grid comparator are explicit
limitations. A practical solver speedup, an improved general approximation
exponent, and rational bit-complexity guarantees remain unproved.
