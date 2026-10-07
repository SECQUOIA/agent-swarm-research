**Independent research-agent review, 2026-10-02.** The revised arguments
and implementation pass this review within their stated scope. Three
implementation soundness defects were found, reported, repaired by the
author, and independently checked after repair. No substantive mathematical
gap remains in the reviewed construction. This is an adversarial internal
review, not journal peer review or a publication-priority assessment.

The actual files reviewed were `note.md`, `mincut_recourse.py`,
`check_recourse.py`, `check-results.json`, `mixed-submodular-recourse.md`,
`check_mixed_submodular.py`, and `mixed-submodular-results.json`. The main
note was reread after its deterministic exact-output proof was added.
The linked conditional-value, exact quadratic box-stable recourse, and
polynomial box-stable recourse notes were read to check the imported
interfaces. The local GLS full text confirms Theorem 6.4.9 and Lemma
6.5.15 on exact rational oracle optimization and recovery of an optimal
basic dual solution from oracle inequalities. The earlier finite-noise
tail results are prerequisites; their complete underlying proofs were
not independently reproved in this review.

The mathematical checks support the following conclusions.

- Separate residual concavity permits sequential endpoint rounding without
  increasing the objective. Inward rounding of integer bounds is necessary
  and sufficient for the stated mixed-domain extension. Fixed sign reversals
  preserve the class on every rational subbox. The binary coefficients,
  terminal-arc signs, opposite pair arcs, and constant offset in the cut
  construction are correct. Skew flow capacity constraints, conservation,
  and equality with the cut value prove optimality in exact arithmetic.
- Infimum over the fixed residual domain preserves upper coordinate
  curvature. Rounding only the continuous core gives error `kLh^2/8`.
  Updating the incumbent before retention preserves every optimizer cell.
  The trace checker reconstructs candidate children and all corners, so a
  supplied list of retained cells cannot silently omit an unchecked branch.
  Its completed and unfinished enclosures have the stated meaning.
- The conditional-neighbor noise intervals depend on the fixed grid tuple
  and residual noise, not on other core noise. Their length bound is
  `Lh(1+k/2)`. The finite-grid atom correction and the `M>=2^J` condition
  justify the factor `H` and the stated expected query count. Residual
  dimension enters the polynomial oracle cost. This result still requires
  the supplied core and a positive noise scale.
- In the exact-output extension, multiplying by `T=S^3` clears every
  coefficient after residual endpoint substitution. A smallest optimal core
  face has a nonsingular free Hessian unless it has no free variable.
  Determinants therefore give the uniform objective-value denominator bound
  `D=T(k!H_A^k)^2`. The best point for the incumbent residual label lies
  between the true optimum and the incumbent. A certified interval shorter
  than `1/D^2` forces equality of the two rational optimum values.
  `verify_exact` can consequently verify a feasible output without repeating
  face enumeration. An insufficient execution limit is correctly reported
  as unfinished. The final note correctly separates this algorithm from the
  finite-noise expected bound; its sampling-precision warning is essential.
- The imported continuous exact theorem applies because rational box
  restrictions and linear changes preserve the cut class. Binary residual
  coordinates can be recovered by endpoint rounding of an optimal
  continuous relaxation. General integer widths require rescaled parameters,
  as stated. The polynomial extension retains an exact cut only because the
  residual unary concavity and pair-sign certificates are supplied and checked.
- In the mixed supplement, minimization over the continuous convex block
  preserves lattice submodularity. Its exact convex-QP values and rational
  gradient certificates are sufficient even for singular PSD blocks.
  Convex combinations of greedy base vectors give the claimed lower bound.
  The LP dual signs, decreasing-order greedy separator, polynomial coefficient
  heights, oracle dual recovery, and `m+1` support bound are consistent.
  The oracle needs a product box and a PSD continuous block; neither general
  continuous submodular QP nor integer variables in that block follows.

The repaired defects were observable incorrect certifications, rather than
style issues.

1. A one-pass `integer_indices` iterable was consumed before being retained.
   For `F(x)=-x` on `[1/3,5/3]`, `iter([0])` caused the solver and verifier
   to accept `x=5/3`, although the integer optimum is `x=1`. The public
   search boundaries and network compiler now normalize the iterable before
   repeated use. The exact integer optimum is returned and verified.
2. Float entries in a supplied flow could erase conservation deficits. With
   `N=2^54` and the rational objective
   `-x+(2N-1)y-2(N-1)xy` on the unit square, the optimum is `-1`.
   A false certificate at `(0,0)` used float flow `N` on terminal arcs and
   rational flow `N-1` on the internal arc. It previously certified value
   zero. The verifier now rejects nonexact point, value, and flow entries.
3. Float endpoint signs such as `1.0` passed the sign-membership test and
   contaminated otherwise exact arithmetic. The same rational example was
   incorrectly solved with value zero. Float signs are now rejected, and
   exact signs return value `-1`. The author's separate coefficient-type
   guard also rejects float model coefficients.

The independent diagnostic is [check_independent.py](check_independent.py).
The command actually run after the final relevant code changes was:

```text
python research-20261002-decomposition/conditional-messages/reviews/check_independent.py
```

It passed 120 new exact comparisons with one to three core coordinates,
including coupled and indefinite cores, and 423 certified level enclosures.
These comparisons use independently implemented residual endpoint and full
core-face enumeration; they do not reuse the author's exact comparison
helpers. The objective denominator bound was also checked against each
result. Twenty-four further cases compared completed exact outputs with
independent optima after arbitrary variable permutations and reversed core
orders. Twenty-four supplement cases used a coupled two-dimensional convex
block, including 12 singular Laplacians, and checked endpoint reduction,
all set-submodularity inequalities, and a tight mixture of the two greedy
base vectors. All three repaired soundness examples passed their independent
regressions.

The author's recorded checks were inspected separately. They are not being
reported as additional reviewer runs. The general mixed SFM/ellipsoid oracle,
the full smoothed closure/fallback algorithm, and polynomial coefficient
support are theorem-level extensions rather than implemented components of
this prototype. The experiments establish operation on the stated classes;
they do not establish competitive solver performance or a general
treewidth-only algorithm. No project-wide verification or CI inspection was
performed.
