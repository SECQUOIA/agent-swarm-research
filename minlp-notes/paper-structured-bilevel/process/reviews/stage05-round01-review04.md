# Stage 5 independent review 04

Recommendation: accept after the minor coverage correction below. I found no
major mathematical defect in the frozen stage 5 statements or proofs.

## Snapshot and independence

Reviewed `process/snapshots/stage05-round01`. The SHA256.json digest is
`c25d5edb69e64647034e54fea863d4637e410b2a22461e8d3d378741d67fd6b5`.
I verified this digest and all 13 listed file digests before copying the files
to `verification/reviewer04/stage05/`. I read all of
`sections/05-boundaries.tex` and `appendices/d-path-geometry.tex`, the main-file
integration, README, coverage inventory, and added bibliography entries. I
revisited the accepted fixed-dimensional algebraic tools and accuracy/output
dependencies used here. Historical acceptance labels were not proof evidence.

I did not read another current stage 5 report, edit manuscript sources, or
delegate. The build, source-PDF text extracts, and diagnostics are isolated
under `verification/reviewer04/stage05/`.

## Major issues

None found.

## Minor issue: retain the positive-objective multiplicative consequence

Location: `sections/05-boundaries.tex:119–138`, following the dense scalar
hardness proof; `process/coverage.md:205`. Source:
`notes/bilevel-dense-box-hardness-investigation.md:305–327`, Section 8.

The source note contains a distinct approximation consequence of the final
no-upper-row construction that is absent from the manuscript and has no
explicit later-stage assignment. The displayed theorem retains the
zero-versus-two gap, but the source also treats strictly positive objectives
and multiplicative guarantees under exact bilevel feasibility. This matters
under the requested comprehensive coverage of note-only developments. It is
an immediate supporting corollary, not a missing premise or a defect in the
hardness proof.

Remedy: add a short paragraph or corollary after the proof, and update its
coverage row. With the proof's nonnegative response objective H, the objective
1+H has optimum one versus at least three, excluding a polynomial algorithm
returning an exactly bilevel-feasible solution with ratio strictly less than
three unless P=NP. With s=n+m, the objective 1+2^s H has optimum one versus
at least 1+2^(s+1). Its encoded instance length remains polynomial in s, so
every fixed polynomial approximation ratio is eventually smaller than the
gap; the finitely many smaller source sizes can be handled separately.
State that the latter scaling loses the bounded upper-coefficient restriction,
retains polynomial binary encoding, and proves neither strong hardness nor a
claim about relaxed follower optimality. This closes the note-only coverage
gap without expanding the main construction.

## Mathematical checks

1. **Dense scalar construction, lines 39–138.** A guessed weak active status
   gives an affine rational response through a positive definite principal
   system, and the resulting nonempty rational polyhedron has a polynomial-bit
   witness. The ternary residual's smallest signed leading term is at least
   3w_i/(2*3^n), so subtracting the displayed tail still gives the claimed
   w_i/3^n margin. The combined auxiliary feedback is below 4 eta and hence
   below every base margin. Conditional clipping gives the minority-distance
   identity and clause shortfall. A false rounded clause establishes the gap
   for every continuous response. The square residual matrix is nonsingular;
   the text correctly distinguishes joint convexity of the square
   representation from the normalized objective after deleting a leader-only
   term. The removed symmetric auxiliary block supplies no lost theorem.

2. **Near-identity reduction, lines 163–243.** The ternary recurrence keeps
   its state in [0,1]; every ReLU state and inactive residual has the stated
   bound. The scaled point is a box fixed point for the feedforward equation.
   Subtracting the actual KKT fixed point yields the relative-coordinate
   inequality, and the nonnegative finite Neumann series may multiply it
   without changing its direction. The backward matrix contains theta squared,
   not theta, after division by the local amplitude. The contraction estimate
   and readout scaling give delta/8 error and the stated separating threshold.
   Decreasing theta for zeta preserves all estimates. The row and column norm
   bounds imply strict diagonal dominance and all three near-identity norms.
   Polynomial-bit scaling does not imply polynomial numerical inverse gap;
   the statement and discussion keep this distinction.

3. **Conditioned grid and exact oracle, lines 272–350.** Both endpoint
   saturation tests hold at equality. Responses in one closed cell agree
   outside J, so the VI sensitivity estimate uses only D_J. Selecting a
   maximum row minor in independent columns bounds every full-row expansion
   coefficient by one. The grid covers intervals of width at most K, including
   large rational offsets; minimizing the direct leader term over each inverse
   grid cell avoids a numerical bound on b. The response error is at most
   epsilon times the one-norm of the upper follower weights. Constant ranks,
   empty follower dimension, zero leader dimension and zero upper follower
   weights are handled. For exact recovery, clearing Q and t denominators
   makes every free principal determinant at most N!H^N. The displayed
   contraction iteration count puts coordinates strictly within the rational
   reconstruction radius. Continued fractions and exact KKT verification
   recover the unique rational optimum with polynomial time in numerical K
   and input length, as required by this theorem.

4. **Growing leaders and the mixed-radix alternative, lines 378–452.** The
   attributed source gives a gap throughout the continuous input domain, not
   merely at label points. Bounded ReLU range permits the first scaling;
   integer duplication is polynomial because the source coefficient
   magnitudes are polynomial, not just their bit lengths. The mixed-radix
   table includes repeated labels as bad pairs. Its interpolation is
   nonnegative and 1-Lipschitz, and nearest-label rounding gives the claimed
   2nD+2 max(0,1-nD) lower bound. The difference of two scaled ReLUs preserves
   saturation, which a single scaled clipped argument would not do.

5. **Bounded leader core, lines 464–501.** For every fixed core point, a
   minimum of a signed clipped-affine component occurs at a vertex of a
   closed arrangement cell in its bounded box. A full independent set of
   component normals defines that vertex, even for lower-dimensional cells;
   the coefficients are constant in the component variables. Enumerating
   these bases gives all affine candidates. Box feasibility alone suffices
   for candidate soundness. The first core arrangement fixes feasibility and
   all clipping formulas, and the second fixes pairwise value order. Each
   selected candidate remains feasible on a cell closure and its continuous
   clipped value agrees there with the LP objective. Newly feasible boundary
   candidates do not invalidate this returned feasible value; completeness
   follows from the relative cell containing the true optimum. The number of
   both arrangements and rational bit lengths is polynomial for fixed c,h.

6. **Leader path and messages, lines 524–583.** The four-piece formula for
   rho holds over the entire increment range. Nearest-option telescoping and
   cumulative subset paths establish the exact normalized subset-distance
   optimum, with gap 1/W. Replacing only the last state establishes the exact
   terminal message while preserving every box constraint. Weighted
   telescoping also establishes the identical-factor message; its final tail
   explains the count 2^(n+1)-1. The text properly separates this unconditional
   representation lower bound, whose family has trivial optimum zero, from
   NP-hardness and from implicit representations.

7. **Sparse shadow and vertex polynomial, Appendix D lines 9–170.** One
   active bound per coordinate describes all vertices, with triangular
   nonsingularity and distinct terminal coordinates. I checked the indexed
   edge cancellation against the primary source's Definition 11/Lemma 12.
   Strict incident-edge loss gives global unique exposure, and the backward
   absolute-value recurrence evaluates the support in linear arithmetic time.
   Every projected point lies on the upper boundary and is uniquely exposed,
   giving the terminal-message count. The bounded epigraph's open boundary
   pieces force distinct linear factors in the product of the describing
   nonzero polynomials; only unextended two-variable descriptions are covered.
   Expanding the product terms proves the telescoping identity, vertex-only
   zero set, and parabolic exposing formula. Padding forces zero bits at every
   padding coordinate and decreases free-coordinate bit error by the required
   power, with polynomial dimension and a fixed local coefficient alphabet.

8. **Path-follower hardness and the new padded strengthening, lines 629–698.**
   The linear vertex score gap is a squared terminal difference at the
   exposing price. Its extension to an arbitrary convex combination bounds
   both terminal and quadratic perturbations using the off-vertex weight a,
   so it proves global QP optimality rather than only comparison with vertices.
   The entire follower objective may be rescaled to identity Hessian. For the
   padded family the proof explicitly uses the full N-dimensional cube's
   F,c,D and tau. Every desired zero-padding vertex is already strictly optimal
   on that full cube; restricting to the padded subset preserves optimality.
   Conversely F<=0 still forces an original cube vertex, so a new vertex of
   the cut polytope cannot introduce a false yes witness. Polynomial-bit free
   bits and the exposing leader prove NP membership for the stated restricted
   family. Continuity and the endpoint totals prove the slab-only feasibility
   and attainment claims. The nonconvex quadratic upper row, variable slab
   weights and rescaled linear costs remain explicitly qualified.

9. **Equal-gain projection, Appendix D lines 192–269.** Nonzero oriented
   gains admit consistent tree normalization, using reciprocal gains when
   traversed backwards. Consistent difference intervals make all backtracks
   nonnegative, so unique simple paths are shortest. The all-pairs lower/
   propagated-upper tests and their minimum witness prove necessity and
   sufficiency. Original state bounds are retained when a state is prescribed.
   A zero gain creates bounds at its original head before deletion; it must
   not be reversed. Multiple bounds can be propagated without choosing an
   active maximum or minimum symbolically. Removing c nonforest edges adds at
   most 2c retained states, so fixed total cycle rank, rather than a bound
   separately in arbitrarily many blocks, keeps the final dimension fixed.
   Rational gain products and path sums have polynomial degree/bit growth in
   fixed parameter dimension. Sign strata include zeros. Recovery requires
   only comparisons and rational arithmetic in the retained solution's field.
   Dense objectives on eliminated states and an automatic attainment claim
   from merely pointwise bounded states are expressly excluded.

10. **Curvature and arithmetic, lines 718–800.** Both Boolean constructions
    are optimistic restricted-family NP-completeness statements. The new
    one-power examples force 0<x<=(5/8)^P at constant requested accuracy, so a
    positive reduced rational x has denominator at least (8/5)^P. The second
    example really has the convex reduced row 1/2-x^(1/P) and a strict anchor
    at one. Neither example purports to settle the one-power affine-objective
    unconstrained subclass. Eisenstein proves the sparse upper degree example.
    The multiquadratic induction is not circular: an element squaring to the
    next prime would be a common sign-character eigenvector and thus a rational
    multiple of one existing basis radical, contrary to prime valuations.
    Distinct signed sums then give degree 2^N. The singleton local sets are
    convex as sets; their equality descriptions need not be convex constraints.
    Exact Square Root Sum comparison is separated from both an NP-hardness
    claim and the common-field output lower bound.

## Coverage, source checks, build and limitations

I compared the four canonical stage 5 result files (dense scalar hardness,
near-identity hardness, conditioned additive algorithm, and leader vertex
integrity) with the complete new text. I also checked the growing-leader and
parameterized-source notes; dense no-upper-row extension and earlier symmetric
construction; Klee–Minty diagonal-follower and rank-one-slab notes; parametric
path obstruction/investigation; affine-strip tree/cycle-rank extension; and
convex-leaf arithmetic note. The sole unaccounted distinct consequence found
is the minor issue above. Physical blending realizations remain explicitly
outside scope. Stage 6 computation/contact reconstruction and stage 7 synthesis
are assigned later and are not omissions in this review.

After reading `literature/AGENTS.md`, I checked the local primary Froese et al.
v3 statement and node/edge construction (PDF pp.10–12, Theorem 5.3 and Corollary
5.5 in extracted text), Gärtner et al. Definition 11/Lemma 12 (PDF pp.8–9), and
Mairal–Yu Proposition 2/equation (4) (PDF p.4). Original-PDF text extracts are
retained in the isolated directory for the formulas omitted by the literature
Markdown extraction. These support the precise attributed consequences. I did
not perform a new exhaustive priority search or claim all historical sources
were re-audited in full.

The isolated command
`latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`
succeeded, producing 63 pages. The final log contains no undefined references,
citations, or overfull/underfull warnings. The README and main inputs agree on
the current staged status.

Fresh independent exact checks in `check_review04.py` passed:

- 58 strict identity-Hessian KKT certificates over the full cube for padded
  target vertices, including shifted prices; 31 exact padded slab/Subset Sum
  target comparisons.
- 120 oriented-tree projection comparisons with an independent enumeration of
  original-coordinate polyhedron vertices. These include negative/zero gains,
  reversed original orientations, prescribed states and inconsistent combined
  bounds; all 58 feasible cases supplied rational original-coordinate witnesses.
- 30 projected-gradient exact rational reconstructions, using 1,548 rational
  updates and independent exhaustive active-status optima. The stated
  denominator/error bounds and continued-fraction recovery passed.

I also reran the existing exact structural/path checker (521 path arrangement
vertices and three core-versus-full-arrangement comparisons), conditioned-grid
checker (60 maximum-minor cases; seven grid cases with 25 exact response pieces
and 299 candidates), and dense-box checker (510 Boolean KKT certificates, 1,008
clause-feedback certificates, and its separate readout/gap controls). Their
logs are retained separately. These are finite diagnostics with different
purposes; their counts do not establish a formal verification of the general
algorithms. I did not implement a new general quantifier-elimination engine or
make a performance claim.

Optional editorial preferences: none required at this stage.
