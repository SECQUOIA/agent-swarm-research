# Final whole-manuscript review 3

Reviewed the 18 frozen inputs in `final-snapshot`, including every section,
both appendices, main file, macros, bibliography, README, and all four Python
checkers. All frozen input hashes remained unchanged. I did not read other
review, author, or adjudication reports, edit manuscript inputs, or delegate.

**Decision: no major issues and no required minor corrections identified.**
The manuscript gives a complete mathematical account of its stated results.
Its significance and novelty claims are appropriately tied to the specified
electrical model and distinguish established tools from the electrical
realization. I recommend closing this review gate.

## Main mathematical assessment

- **Basic closedness and rational equivalence (`05-algebraic.tex`).** I
  reconstructed both directions of the universality theorem. The necessity
  proposition correctly protects every forward denominator and every
  substituted inverse denominator by a positive rational margin on the compact
  domain. The conditions `F(t) in T` and `G(F(t))=t` exclude all extraneous
  ambient points after denominator clearing; compactness is used exactly where
  needed. This argument works with rational maps defined on their respective
  sets, without requiring globally defined ambient rational functions.
  The three-quadrant obstruction is valid: a nonzero lowest homogeneous part
  cannot have odd degree because opposite included quadrants would force it to
  vanish on an open set. Even degree then gives nonnegativity in the excluded
  quadrant, and a direction avoiding finitely many zero sets produces the
  contradiction. Equalities and polynomials with nonzero constant term are
  handled correctly.

- **Arithmetic appendix.** Polynomial evaluation introduces uniquely
  determined coordinates. Scaling retains equivalence even before imposing
  final bounds: the paired multiplication equations recover the original
  product after division by the fixed positive epsilon. The shifted gates
  retain the original coordinates by an affine recovery map. Every apparent
  subtraction or halving is an allowed addition relation, and every reciprocal
  is an inversion relation. I independently simplified the reciprocal,
  square, product, and shifted-product identities symbolically. I also used
  exact rational interval arithmetic on the full input square with
  `delta=1/1024`, obtaining 64 strict interior output enclosures and excluding
  zero from all reciprocal denominators. This checks the uniform range
  reasoning independently of grid sampling. The nonnegative-output auxiliary
  correctly uses the boundary at one half. Constants and the midpoint/halving
  chains are uniquely fixed. Empty sets are covered, and no unsupported size
  bound is asserted for arbitrary compact descriptions.

- **Topology and algebraic degree.** The standard-simplex nonface equations
  describe exactly the support faces of the finite complex. Compact
  triangulation therefore yields the claimed semialgebraic homeomorphism,
  without confusing it with rational equivalence or requiring rational
  coefficients in the original set. The designated voltage in the algebraic
  degree theorem does generate the individual field: affine coordinate
  recovery survives every network transformation. The rational and empty
  cases are covered.

- **Foundations and ordinary electrical reduction.** I checked the injection
  sign convention and dissipation identity, complement copying, distinct
  repeated occurrences, the addition pin, and elimination of the inversion
  gadget. The inversion auxiliary has the stated range. Degree, redundant
  injection bounds, size counts, and the unique rational extension all follow
  from the construction. The certificate consequence correctly remains
  conditional on the open relation between NP and existential-real complexity.

- **Structural transformations.** The bounded crossover transmits values
  uniquely while keeping only its sum in the enlarged interval. The changed
  complement and pin constants are consistent with the ordinary gadget
  equations. The disk-and-corridor substitution accommodates the doubled
  inversion occurrence and repeated names. A selected root has sufficient
  spare degree for the fixed-voltage connector. Harmonic subdivision scales
  all endpoint injections uniformly, preserves the whole solution set,
  produces the claimed bipartition and girth, and keeps a finite data alphabet
  for fixed girth. Zero-variable cases are treated explicitly.

- **AC formulation.** I checked the rectangular signs, positive unsquared
  magnitude variables, branch-cut axis convention, and the equivalence between
  zero cycle sums and root-normalized vertex shifts. Their integrality follows
  from propagation; integer quantifiers are unnecessary. The linear variable,
  predicate and monomial counts are consistent with quadratic constraints and
  polynomial bit length. The energy argument requires the real lift that the
  paper specifies. The winding counterexample, shrinking principal windows,
  bus-angle boxes, and one-sided reactive saturation retain their separate
  scopes.

- **Residual and stability results.** I reconstructed the forward and reverse
  gadget residual estimates, including propagation through copy paths. The
  recurrence remains inside all bounds, is exactly infeasible, and has only
  the stated final pin residual under canonical extension. The compact
  connected epigraph meets the polynomial-minimum theorem's hypotheses.
  Fixed data and bounded degree give the claimed separation scale. Rounding
  with clamping preserves singleton voltage bounds, and the certificate claim
  is correctly restricted to its promise. The energy, spectral, and active
  discrepancy estimates give the constants stated in the AC residual
  corollary. No residual-preserving planarization or symmetric-reactive-
  tolerance hardness is implied.

## Prior-work verification and presentation

I checked the local primary text of **Dynamic Toolbox for ETRINV**, specifically
Theorem 1, Definition 4, and Lemma A. The paper's account is accurate: the
stated rational-equivalence notion matches, and the inactive auxiliary in the
displayed disjunction example is not unique. The manuscript proves its
replacement statement independently and does not dismiss the valid
conjunction-only arithmetic. The citation explicitly identifies v1, which
the [arXiv record](https://arxiv.org/abs/1912.08674v1) lists as its version.

I checked the cited triangulation locator directly: Theorem 1.1 provides the
triangulation, and Section 1.2 explicitly uses a finite complex for compact
sets. The bibliography's publication metadata and preprint-version note are
consistent with the [primary source](https://arxiv.org/pdf/1505.03970v2).
I also inspected Theorem 1.1 on page 242 of the cached published
Jeronimo–Perrucci–Tsigaridas paper; substituting degree two and dimension
`q=n+1` gives the displayed separation bound.

The introduction, abstract and conclusion consistently explain independent
voltage/injection intervals, simultaneous singletons, model differences from
prior power-flow hardness, the novelty of the electrical realization, and
the weaker status of residual evidence. The separate rational and topological
universality statements are clear. The verification appendix appropriately
calls its eight instances illustrative and never treats finite tests as a
proof of quantified claims. I found no required readability or consistency
correction. Blank author metadata is the user's confirmed choice.

## Independent checks and limitations

- Symbolic identities and full-neighborhood rational interval enclosures:
  passed; output is in `final-review3-calculations.log`.
- Fresh execution of `check_arithmetic_exact.py`: passed all four reported
  groups, including the final 332-variable disk circuit and its outside-point
  and altered-coordinate regressions.
- Read all other checkers against the manuscript; did not redundantly execute
  their full suites or rerun the LaTeX build in this mathematical review.
- Fresh narrow web searches for existential-real power-flow classification,
  resistive universality, and rational/basic-closed equivalence yielded no
  matching contrary result. These searches do not prove priority. I did not
  independently revalidate every bibliographic claim against every cited
  publication. The paper's qualified and model-specific novelty wording is
  therefore preferable to an absolute priority claim.
- I reviewed source presentation, not every rendered PDF page. This review is
  a reasoned assessment, not a formal proof verification or a guarantee about
  future peer review.

**Optional preferences:** none that warrant delaying completion.
