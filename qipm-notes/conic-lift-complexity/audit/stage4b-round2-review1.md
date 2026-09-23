# Stage 4B second independent review 1

Reviewer: `/root/stage4b_round2_review1`.

I read all of `09a-whole-rows.tex`, `09b-face-sharing.tex`,
`09c-balance-slices.tex`, `09d-lp-power.tex`, and
`09e-spectral-chordal.tex`, the first-round root assessment and correction
record, and the necessary reduction, curvature, joint-cover, and
bounded-fiber projection dependencies. I did not read the other second-round
review reports or edit the manuscript.

**Result: no major or minor issue identified.** The substantive revisions
are valid, and I found no regression requiring correction.

## Revised sharing arguments

- In Theorem `thm:face-sharing-local`, the cross-contact identities make
  the primal ray and the rank-detecting subspaces a direct sum. A fixed
  nonzero active dual vector annihilates every primal derivative because
  its pairing has a minimum at the contact. Thus the entire direct sum
  lies in one hyperplane, proving the revised total bound
  `sum_a t_i^a <= m_i-2`. The proof uses only the stated first derivatives;
  it does not silently assume symmetric individual mixed forms. The
  zero-factor argument and the complementary-face bound are also valid.
- The aggregate dual map in Theorem `thm:face-sharing-global` is cone
  valued, globally C1, and factors the product-sphere contact kernel.
  Its contact pairing is the nondegenerate product metric. At capacity
  equality, the joint-cover theorem therefore applies with simply
  connected source `(S^p)^k`, since `p>=2`. Its capacity multiset conclusion
  excludes equality under `c<p`. The resulting integer premium is exactly
  the claimed necessary bound `R>=kp+1`; no stronger per-source premium
  is being inferred from this argument.
- The retained compact active-label pieces and proper source neighborhoods
  justify the separate face-incidence and face-weighted capacity budgets.
  Positive integer capacities make new activity increase the capacity
  count, which is the needed closedness and separation argument.
- The combined `R_*` and `L_*` bounds follow independently from those
  budgets, the aggregate bound, and `R<=cL`. They imply the displayed
  dimension and arbitrary ambient-barrier bounds. At face cap one they
  reduce to the exact previously established ray-exposed values. For
  general face caps the text correctly refrains from asserting attainment.
- Proposition `prop:spectral-contact` has the same valid hyperplane
  argument even when the two contact manifolds have different dimensions
  or the full mixed pairing is degenerate. The unweighted capacity bound
  and its integer factor-count consequence are correctly propagated.

## Whole rows and normalization

The whole-row rank proof detects the constant and every coordinate without
regularity assumptions. Its restriction to a contact cylinder detects the
claimed affine-face dimension. The shared homogenization attains both
bounds: arbitrary polar boundary contacts cannot produce a larger face
than the extreme polar contacts used to define the codimensions.

The minimum-dimension rigidity proof correctly eliminates free variables,
uses compactness to force a strictly positive hyperplane normalization,
and obtains a linear cone isomorphism. The separate slack-factorization
proof is valid without a regular factor choice. The connected-extreme-set
corollary excludes equality at total dimension `N+1`; it does not mistake
this for an additive per-factor bound. The stronger normalized-base bound
has precisely the additional single-base hypothesis needed for its finite
connected-cover argument.

The recession normalization criterion uses a functional positive on the
pointed recession cone, which makes all finite sublevels bounded. The
fiber minima are attained, recession translation reaches all larger
levels, and a sufficiently high level intersects the relative interior.
These facts justify barrier restriction and bounded-fiber projection.
The escaping-disk counterexample and the simple-vertex polytope transfer
are consistent with the criterion and do not assert unsupported
monotonicity for arbitrary unbounded fibers.

## Other scientific checks

- The balance-slice extremality criterion limits each extreme point to
  one or two primitive rays in distinct blocks. The stated sign geometry,
  including the explicit Albert chart, supports the connectivity proof.
  The diagonal orthant/simplex sections give the lower barrier parameters,
  and the restricted-gradient calculation gives the matching `rho-1`
  normalized upper bound. The comparison of classical and spin families
  clearly concerns different bodies. I independently recalculated the
  failed cancellation example's derivatives `13/4` and `25`.
- The generic norm-ball frontier follows from the positive-curvature patch
  and is attained by the displayed norm tree. The minimum-count capacity
  excesses, half-cone nonrigidity example, and globally C1 Young maps are
  consistent. The global proof differentiates primal and polar charts
  independently, avoiding a hidden C2 assumption at coordinate zeros.
  All relevant exact cap statements now explicitly require an integer
  cap. The two-dimensional power-cone obstruction separates non-C2 rays
  from zero-curvature rays correctly.
- The generalized power-cone Hessian is a positive weighted variance on
  the simplex tangent plus the Euclidean tangential term. Their common
  kernel is zero, giving the claimed capacity `m+k-2`. The discussion
  distinguishes this bound from denominator-sensitive representation
  results and makes no unsupported scalar priority claim.
- The spectral mixed rank includes the complex or quaternionic phase
  channels and is `delta*c-1`, rather than the polar manifold dimension.
  The whole-row spectral face codimension is
  `delta*(r+c-1)`. The shared spectral ambient lower bound uses one
  tensorized recession certificate, so it applies to coupled arbitrary
  barriers. The slice gradient norm and cube section give the exact slice
  parameter.
- The completion-cone closure argument, signed Legendre barrier,
  clique-separator formula, and diagonal-section optimality proof are
  coherent. The block-star certificate is invariant under the rank-one
  polar representative's simultaneous phase. Equality of reduced Newton
  systems is stated only after matching coordinates, constraints, and
  objectives, with no unwarranted ambient-oracle or runtime conclusion.

The classical barrier and completion constructions are attributed as such;
the new resource statements retain their full-row, regularity, dictionary,
and cap hypotheses. The final LaTeX/BibTeX logs inspected contain no
unresolved-reference, citation, overfull, or underfull warnings. No further
correction is requested by this review.
