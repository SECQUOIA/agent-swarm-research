# Stage 3a, round 1, independent review 5

Verdict: **no major issues; four minor corrections**.

Scope: all of `06-coherent.tex` and `07-scalar-realizations.tex`, the extended
accuracy range in `03-classical.tex`, their access-model interfaces, the
Stage 3a source dispositions, and the primary literature identified below.
I did not read other review reports or edit the manuscript.

## Numbered findings

1. **Minor — expose the central-path multiplier in the box-centering gap.**
   `07-scalar-realizations.tex:404–413` gives the exact coordinate
   `rho(eta) h Phi`, but the sufficient subproblem gap displayed in the
   following prose has no `rho(eta)^2` factor. The correct uniform
   consequence of the proved error bound is
   `tau <= c rho(eta)^2 (beta-alpha)^2 delta^2 / K`.
   Since eta is explicitly fixed, this can instead be written with a
   constant `c_eta`; that is likely the intended interpretation. Make one
   of these choices explicit. An absolute constant valid for arbitrary
   small positive eta is not justified: the hard coordinate shrinks with
   rho while the current perturbation allowance does not. This is a local
   parameter-clarity correction, not a failure of the reduction.

2. **Minor — specify a fixed success margin for reusable sampler setups.**
   `07-scalar-realizations.tex:609–618` says a constant number of setups
   suffices provided setup success exceeds one half. Uniform constant
   overhead needs success at least `1/2 + c_setup` for an absolute positive
   constant (for example, two thirds). Otherwise the number of setups and
   conditional draws needed for reliable majority can depend on a vanishing
   margin. State the fixed margin, or charge its dependence explicitly. The
   one-setup versus per-draw contamination distinction itself is correct.

3. **Minor — repair the product-tree summation label.**
   `07-scalar-realizations.tex:531–533` contains the literal TeX
   `\sum_{v\ {` followed by `m internal}}`, rather than a text condition
   saying that v is internal. Replace it by, for example,
   `\sum_{v\text{ internal}}`. The current expression introduces a
   meaningless mathematical m and is visible despite a clean build log.

4. **Minor — add the closest positive-definite access-model comparator.**
   The discussion in `06-coherent.tex:140–165` should briefly cite and
   distinguish Orsucci and Dunjko, *On solving classes of positive-definite
   quantum linear systems with quadratically improved runtime in the
   condition number*, Quantum 5, 573 (2021), DOI
   `10.22331/q-2021-11-08-573`. The paper is already in the repository's
   literature folder. Its Proposition 6 gives a positive-definite
   solution-state lower bound linear in condition, while Sections 4.2–4.3
   explain the improved polynomial degree under a normalized encoding of
   `I-eta A`. This is directly relevant to the manuscript's explanation of
   why its bounded transform has linear degree despite the classical SPD
   Chebyshev square-root degree. The output and shifted-access contracts
   differ from the present relative scalar theorem, so this comparator
   does not invalidate the result. A short explicit comparison will keep
   the claimed contribution appropriately narrow.

## Coherent theorem and primary-source verification

- Independently checked [CGJ's full Theorem 33](https://arxiv.org/html/1804.01973).
  Its `c=1/2`, `max(1,c)=1` substitution gives the displayed implementation,
  state-preparation, confidence, and encoding-accuracy dependences. Squaring
  an epsilon/3 relative norm estimate gives the promised relative quadratic
  estimate. The upper primitive is properly attributed.
- The three-dimensional lower-bound family satisfies the spectral promise
  and exact condition number, including at kappa four. Its output intervals
  are disjoint in the stated epsilon range. Only one scalar block of its
  completion changes, away from the square-root singularity; the norm
  difference and hybrid argument give the claimed lower bound, including
  controlled and inverse calls.
- The exact-entry bypass is valid, and the separate sparse-value lower and
  upper bounds are not falsely declared tight. The public-eigenbasis
  counting comparison has the correctly weaker condition dependence.
- The fixed-transform probability error bound has the correct cross term,
  and its required operator tolerance scales as epsilon divided by the
  square root of condition. Both Bernstein arguments are valid on their
  stated bounded domains. They do not apply to general rational,
  postselected, or variable-time algorithms, as the manuscript says.
- Checked [Alase et al.'s primary paper](https://arxiv.org/pdf/2111.10485),
  Theorem II.19, Theorem IV.13, and its expectation-value versus
  system-of-equations distinction. Section 6 correctly associates the tight
  observable-query rate with the normalized expectation subproblem and
  does not remove the conditioning dependence from the full linear-system
  task.
- Checked [Orsucci–Dunjko's primary text](https://arxiv.org/html/2101.11868),
  Proposition 6 and the shifted-encoding construction, for finding 4.

## Optimization and parameter checks

- The cyclic forward/hold/reverse gate product is the identity. Even clock
  length gives both extremal singular values of M. The inverse series,
  exact norm R, plateau mass, and effective condition identities are
  correct. The public row/column norm and sampling tables follow from
  disjoint clock supports. The Hessian and right-hand side simulations
  neither expose nor assume a history-state data structure.
- The allowed even lengths have bounded gaps, so the rounding losses in T,
  ell, p, and R are uniform for sufficiently small absolute delta. The
  matrix dimensions are explicitly parameter-selected. The factors lost
  when expressing hardness in ambient dimension are polylogarithmic there.
- The one-cone optimizer, constant unperturbed value, parameter-one
  restricted barrier, first Newton direction, and central ray all agree.
  The sparse accumulator preserves the intended scalar and full-SQ
  formulation access without asserting a condition bound for a redundant
  augmented KKT matrix.
- Exactly feasible objective-gap output implies the stated scalar error.
  The manuscript correctly separates that lower-bound transfer from the
  quantum algorithm's numerical scalar output.
- Checked [Bansal–Sinha's primary theorem and corollary](https://arxiv.org/html/2008.07003),
  including the positive high promise, fixed-k denominator, and bounded
  error amplification. Their results support the fixed-order corollary;
  extending a magnitude-output domain does not invalidate the lower bound.
- The inverse-transpose tilt norm is independent of the hidden circuit by
  the plateau gauge identity. The homogeneous recurrence proves both its
  lower bound and the plateau-restricted optimality statement. The smaller
  fallback tilt and the larger normalized signal have the claimed scales.
- The tilted value and Newton decrement identities are exact. The reduced
  right-hand side is a mixture on disjoint public regions, so granting its
  SQ interface does not shortcut the reduction.
- The box LP reproduces the local decrement but not the SOCP optimal value,
  as correctly stated. Its central-subproblem strong-convexity argument is
  valid, subject to the explicit eta-dependence in finding 1.
- The affine-slice optimum, equality-operator condition range, parameter-one
  intrinsic barrier, and projected decrement are correct. The multiplicity
  argument preserves the smallest singular value after adding `ee^T`.
  Supplying a projected objective would supply the hard data, and the paper
  correctly excludes it from the input contract.
- The extended inverse-overlap range `0<epsilon<=R_e/2` is supported by the
  unchanged proof: its residual tolerance is at most one eighth and its
  sample count remains bounded below by a positive constant. Its use with
  the exact public `R=Theta(sqrt(K))` gives the claimed affine upper
  exponent, including accuracies above one half.
- The norm-tree feasible projection, analytic center, zero leaf/tree cross
  Hessian, and leaf coefficient `2(D-1)` are correct. Padding by fixed zero
  leaves does not change these free-coordinate calculations. The barrier
  and full-Hessian qualifications prevent a false small-iteration claim.

## Sampling contracts and prior-work positioning

The projected perturbation inequality proves the square-root-of-plateau
vector-error threshold. Bernoulli sampling costs order one over plateau
mass, so the two delta/zeta repetition penalties are warranted. The
per-call contamination condition and the alternative reusable-setup
contract are distinct and correctly analyzed, with the constant-margin
clarification in finding 2. The direct SPD Newton system has inverse
solution proportional to the same cyclic history.

The explicit family sampling upper bounds and the generic feasible-sample
upper serve different purposes. The latter's residual controls angular
error and hence quadratic objective gap; scalar normalization preserves
the sample law but does not give a free norm or coordinate oracle. That
limitation is expressly retained.

Checked [Apers–Gribling's primary Lemma 8.5](https://arxiv.org/html/2311.03215),
which already gives full-SQ LP optimal-value hardness. The manuscript
appropriately avoids claiming the first such optimization or scalar
hardness theorem. Its narrower novelty language concerns the parameter,
public-norm, and precise Newton/affine realizations. The Stage 3a source
map covers these relevant developments; the separate global lift-minimality
program is not needed to prove any retained result here.

## Diagnostics

Ran the cyclic verification script using the qipm interpreter. It passed
the cyclic spectrum/inverse, public metadata and norms, tilt/decrement,
tree center/Hessian, and completion-distance checks. I also checked the
displayed algebra independently as described above; these finite examples
are not treated as query-complexity or asymptotic proofs.
