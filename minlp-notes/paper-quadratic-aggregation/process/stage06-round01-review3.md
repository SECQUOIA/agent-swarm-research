# Stage 6, round 1, independent review 3

Date: 2026-09-22. Verdict: **no major issue; one minor wording correction.**

I independently reviewed the full four-aggregation section, author and
literature records, bibliography addition, coverage, exact checker, and
snapshot. I checked the relevant accepted negative-direction lemma and
read the canonical result's development map. I did not read other current
review reports, coordinate findings, edit manuscript sources, or run
global verification.

## Required correction

**Minor M1 — exclude the zero multiplier in the witness statement.**
In `sections/08-four-aggregation.tex:349–351`, the text says that any
multiplier in the displayed four-ray cone is strictly negative at the
witness unless it is a positive multiple of the designated ray. That
cone includes zero, whose aggregate is zero and which is not a positive
multiple. Change “any multiplier” to **“any nonzero multiplier”** (or
“any good multiplier”). The surrounding necessity argument concerns
nonzero good multipliers and is correct. This is a local quantifier
clarification, not a defect in the theorem or sharpness proof.

No other minor correction and no major issue was identified.

## Mathematical audit

- **External-input hypotheses and perturbation.** The statement includes
  independence of the homogeneous matrices, signed homogeneous PDLC,
  nonempty interior, closure of the interior, and the simultaneous
  nonstrict condition at infinity. The three displayed positive definite
  perturbations are independent even for `n=1`: their off-diagonal and
  two diagonal entries establish the claimed independence. A nonzero
  cubic coordinate minor has only finitely many exceptional parameters.
  Strict feasibility and PDLC persist for all sufficiently small
  parameters, including when the original PDLC vector has mixed signs.

- **Bounded inward systems.** A nonzero direction satisfying all perturbed
  nonpositive leading inequalities would make all original leading forms
  strictly negative. The accepted midpoint lemma excludes this for a
  proper hull. Normalizing an unbounded feasible sequence then proves
  boundedness of each inward nonstrict system. Their closedness gives
  compactness without assuming original boundedness or changing charts.

- **Regular levels.** For an exceptional level of a continuous function,
  a basic neighborhood witnessing failure of strict-sublevel density has
  infimum equal to that level. A countable base therefore gives only
  countably many exceptional real levels. Applying this to the maximum
  of the three ratios, whose denominators are strictly positive, gives
  exactly the stated inward sets. Avoiding the exceptional values of
  `-epsilon`, the finite dependence set, and parameters outside the
  strict-feasibility/PDLC range is possible along a decreasing sequence
  tending to zero. Density of the strict sublevel implies the required
  closure-of-interior equality. Every fixed finite feasible subset is
  eventually included; uniform inclusion of all of `S` is neither used
  nor claimed.

- **Strictification.** Deleting globally nonpositive quadratics preserves
  the nonstrict intersection. A retained quadratic cannot vanish at an
  interior point of its own nonpositive sublevel: the local maximum
  forces zero gradient and negative semidefinite Hessian, and the exact
  Taylor formula would make it globally nonpositive. Finite intersections
  commute with interiors, and the nonempty open convex hull equals the
  interior of its closure. Boundedness ensures that some cut remains.
  Thus the external nonstrict representation yields one to four strict
  good aggregations, without accidentally deleting interior hull points.

- **Fixed-cardinality limit.** Duplication to four indices and simplex
  normalization are valid. Compactness yields a common subsequence, and
  the perturbation matrices vanish uniformly in the normalized weights.
  Eigenvalue continuity preserves at most one negative eigenvalue; strict
  negativity at the fixed feasible point ensures exactly one in each
  limit. Normalized eigenvectors can be oriented at that point and passed
  to a further common subsequence. For any fixed original feasible point,
  eventual inclusion in the inward sets forces its lift onto the same
  side of the negative eigenvector. Strict negativity of the original
  simplex aggregate rules out equality in the limiting orientation.
  The displayed convex negative components, including singular and
  rank-one cases, therefore preserve strict validity on every finite
  convex combination. Conversely, four strictly negative limiting
  values remain negative for all sufficiently large indices. This proves
  ordinary hull equality without a closure interchange.

- **Dependent triples.** Evaluation at a feasible lift is a strictly
  negative functional on the finitely generated matrix cone. Its slice
  at value `-1` is the convex hull of the normalized original generators,
  hence compact. When the span has dimension at most two, this slice is
  a segment or a point, with extreme rays among the original rows. The
  corresponding one or two inequalities define the same strict set.
  Yildiran's result then supplies at most two good aggregations with
  the manuscript's sign convention reversed. Translating weights back
  to the original rows preserves the matrix, strict validity, and inertia.
  This optional improvement is not needed by the main proof.

- **Sharpness.** The signed PDLC identity and strict feasible point are
  correct. Every feasible `s` lies below `-1`; the additional sum
  inequality restricts it below the negative root `alpha`, so the chosen
  negative components establish goodness of all four displayed rays.
  If `c>a+b`, the repeated rho coefficient gives at least two negative
  eigenvalues exactly when `n>=3`, which explains the sharpness scope.
  The interval for the decomposition parameter is nonempty, and its
  four coefficients are nonnegative. All four witness slack vectors and
  their off-designated strict signs check out. With M1's explicit nonzero
  qualification, each ray is indispensable. Combining necessity with
  the already proved upper bound justifies exactness of those four
  specific inequalities without assuming the source example's claim.

- **SOC closure and counterexample.** The spectral decomposition absorbs
  the square root of the negative eigenvalue into the oriented vector
  correctly. The open components give the ordinary hull. Mixing any
  point satisfying the closed SOC constraints with one common strict
  point makes all conic slacks strictly positive, proving the closure
  formula. The half-ball example has `-Q3=I`, its strict set is the open
  left half-ball, and naive nonstrict replacement adds precisely `e1`
  outside its closure. It also demonstrates why the original nonstrict
  hull is a different object.

## Primary-source and priority audit

- Independently opened [Blekherman–Dunbar arXiv v1](https://arxiv.org/html/2405.18282v1)
  and inspected its local primary extraction. The introduction's standing
  independence assumption and Theorem 1.4 agree with the manuscript's
  input. Section 8 expressly drops spectral smoothness. Proposition 8.7
  covers `n=1,2`; the final proof combines Propositions 8.6, 8.7, and 8.10,
  so the claimed positive-dimensional scope is supported. Proposition
  3.15 supplies the credited fixed-set eigenvector-limit antecedent.
  A fresh opening of the publisher's author eprint failed; I therefore
  verified these locators in the explicitly cited preprint rather than
  claiming an independent inspection of the journal layout.

- Independently opened [BDS arXiv v2](https://arxiv.org/html/2210.01722v2)
  and read the relevant local primary passages. Corollary 2.20 gives six;
  Example 2.21 is exactly the credited four-necessary system; Section 2.5
  after that example contains the dependent-cone reduction. Remark 2.19
  records the SOC principle. The half-ball example is indeed 2.23 in
  this version. Conjecture 3.2 asks for a six-necessary strict PDLC
  example, so the manuscript's four-bound rules it out. The manuscript
  gives appropriate antecedent credit rather than claiming the number
  four or the lower-bound example as new.

- Read the saved primary dissertation extraction at
  `/tmp/dunbar-thesis-priority.txt`, including Theorem 5.0.5 (printed
  page 97), the cited propositions, and its proof. Its statement omits
  the infinity hypothesis, while the propositions used in the retrieved
  proof include it. The extraction has damaged mathematical glyphs.
  Fresh direct openings of the official record and original PDF failed;
  the [official indexed Emory record](https://etd.library.emory.edu/concern/etds/vq27zq10w)
  and indexed PDF corroborate author, title, and 2025 date. I did not
  visually verify the original PDF or establish an error in it. The
  manuscript correctly acknowledges the stronger prior statement and
  does not rely on it or allege a definitive error.

- Independently opened the accepted author text of
  [Yildiran (2009)](https://www.researchgate.net/publication/220386378_Convex_hull_of_two_quadratic_constraints_is_an_LMI_set)
  and checked Section 3.2, Assumption 1, and Theorem 1. The theorem
  assumes nonemptiness and gives two endpoint aggregations for the proper
  hull, using positive strict inequalities and one positive eigenvalue.
  Thus its use in the dependent-triple remark is accurately scoped.

Bounded searches for the exact dissertation title, strict four-aggregation
PDLC statements, and inward aggregation transfers did not establish a
prior universal strict transfer. That is not proof of priority. The
qualified manuscript claim concerns the complete transfer to arbitrary
strict systems, including dependence; it avoids claiming the first
four-bound or first statement without an infinity condition. I found
that qualification consistent with the inspected evidence.

## Targeted checks and limits

- Ran `python3 paper-quadratic-aggregation/supplement/check_four_aggregation.py`:
  PASS for the PDLC polynomial identity, strict point, all four exact
  rational/radical witness vectors, and coefficient decomposition.
  I read the exact radical arithmetic and sign routine; the sign rule
  handles the opposite-sign cases correctly. These finite checks do not
  certify perturbation, topology, limiting arguments, or novelty.
- Recomputed every file hash in `stage06-author-snapshot.json`: all 18
  entries matched at review time.
- Searched the existing `build/stage06/main.log` and `main.blg` for
  `Warning`, `Overfull`, `Underfull`, and `undefined`: no matches. I did
  not rebuild LaTeX or independently inspect all rendered pages, and do
  not claim a fresh build.

No CI, project-wide tests, Lean rerun, or subagent work was performed.
Only this report was written in the repository.
