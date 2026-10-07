# Independent review of exact smoothed mixed separable recourse

Date: 2026-10-02. Reviewed the mathematical sections of
[the mixed separable closure note](../new-direction/smoothed-mixed-separable-closure.md),
including its references to the
[aligned closure proof](../new-direction/smoothed-exact-cell-closure.md)
and [ambient extension](../new-direction/smoothed-ambient-cell-closure.md).

**Verdict: pass under the stated rational-breakpoint model.** I found no
substantive gap in the scalar oracle, critical regions, nonsmooth closure
argument, fixed sampling laws, fallback, or expected bit-work conclusion.
The author clarified the breakpoint requirement during review. A delegated
independent scalar review reached the same conclusion.

The input must specify rational polynomial coefficients **and rational
breakpoints**, with pieces covering each coordinate interval. This is
essential to the rational-witness contract. For example,
\(\phi(x)=\max\{0,x^2-2\}\) on \([0,2]\) has rational polynomial
pieces, but \(\phi(x)-x\) uniquely minimizes at \(\sqrt2\). Its
irrational breakpoint would invalidate rational knot witnesses. The current
model explicitly excludes this case. Continuity, nonnegative curvature on
each positive-length piece, and the ordering of one-sided derivatives can
all be checked exactly using the supplied rational data.

The scalar recourse construction is complete. For an integer coordinate,
convexity makes the forward differences nondecreasing, and the two available
neighbor inequalities are necessary and sufficient for global optimality.
Binary search takes logarithmically many comparisons in the interval
cardinality. Endpoints, singleton domains, affine pieces, and long ties do
not require enumeration. Evaluating a listed quadratic at a binary-encoded
integer has polynomial bit cost.

For a continuous coordinate, positive-curvature pieces give rational affine
responses. Knots and endpoints give constant responses on closed derivative
intervals or half-lines. A zero-curvature interval needs no free response:
at its slope, an endpoint is also optimal. Thus at most \(2s_i+1\) states
cover every scalar tilt. Overlapping regions are appropriate at ties; no
disjoint arrangement or tie-breaking refinement is needed. Rational knots
also ensure exact continuous witnesses have polynomial encoding length.

Combining one state per coordinate produces a region with at most \(2n\)
linear inequalities. Those inequalities certify global scalar optimality,
so the resulting formula is valid on the entire region, including regions
with empty interior. Substitution gives

\[
 H_J=\alpha I-\alpha^2\sum_{i\in\mathcal F_J}
                t_it_i^T/p_{i,J},\qquad
 \nabla q_J(a;r)=\alpha(a-Tx_J(a,r)).
\]

The second identity is an identity of the quadratic extension, including
outside a lower-dimensional region; it is not an assertion that the full
value function is differentiable. Region normals and Hessians depend only
on the base data. Region offsets and the linear gradient term are affine
in the residual tilt. These facts are exactly what the ambient argument
needs.

The use of nonsmooth recourse is sound. Every active witness gives the
global upper model

\[
 V(v+h)\le V(v)+g_v^Th+\alpha\|h\|^2/2.
\]

Substitution of \(h=-g_v/\alpha\), followed by comparison with the
whole-space minimum, proves
\(\|g_v\|^2\le2\alpha(V(v)-V^*)\) for **every** active witness.
There is no averaging or favorable selection at integer ties. Compactness
of the original product domain gives attained recourse minima, and square
completion gives attained whole-space auxiliary minima inside the fixed
enlarged box. The trial point need not lie in that box. Consequently an
arbitrarily selected optimal scalar-state combination has the small branch
gradient required at a retained near-optimal corner.

The exceptional-hyperplane step then carries over. For an invertible
branch Hessian, a violated nonzero region row crosses the cell, and its
image under the affine negative-gradient map is a fixed hyperplane. For a
singular Hessian, the affine gradient image lies in a fixed hyperplane.
The tube radius \(\sqrt{k}(\alpha+H_0)h_j\) safely combines the
cell diameter and active-vector bounds. A region row with zero auxiliary
normal cannot be violated elsewhere in a cell containing the query.

The counts do not hide enumeration inside a query. There are at most

\[
 R=\prod_{i\in\mathcal I}N_i
      \prod_{i\in\mathcal C}(2s_i+1)
\]

state combinations, but a query obtains its combination by independent
scalar optimization. Integer labels may be exponentially numerous; their
encoding lengths and \(\log R\) remain polynomial in the base input.
The stated rational \(H_0\) bounds every branch Hessian by the triangle
inequality and the norm of a rank-one matrix. Small positive curvatures
affect its encoding length and the cutoff logarithm, rather than the
numerical multiplier in the expected cell count.

The fallback is valid. Enumerate integer assignments and continuous piece
choices; their product domains cover the original domain. Within each
resulting continuous box, the objective is rational quadratic. A minimum
on a smallest-dimensional optimal face has positive definite tangent
Hessian, unless the face is a vertex: a null direction would preserve the
quadratic value until a smaller face is reached. Nonsingular stationary
systems and vertices therefore include an exact optimizer. The number of
candidates is bounded by
\(B=\max\{2,\prod N_i\prod 3s_i\}\), and
\(2s_i+1\le3s_i\) gives \(R\le B\). Exact linear algebra gives
polynomial bit work per candidate and polynomial-length rational outputs.

Both sampling rules are determined before sampling. The counts \(R,B,K\),
the curvature bound, and the auxiliary widths use only base data and the
specified noise scale. Their logarithms have polynomial size. No sampled
denominator enters a new recovery threshold or changes the mesh cutoff.
Local exact closure and the fallback remain correct for every draw. The
exceptional-event probability is at most \(1/B\), canceling the
fallback's exponential multiplier in expectation on that same draw.

For ambient noise, the residual linear term preserves separability.
Semiconcavity suffices for the neighboring-value comparisons and the
volume bound; differentiability is unnecessary. On an ambient-coordinate
line, each state's region is an interval and its value is quadratic.
Closed overlaps have equal values, so at most \(2R\) finite endpoints
per auxiliary query suffice for the inherited section bound. The residual
offsets are affine, and fixed factor hyperplanes lift to fixed ambient
hyperplanes exactly as in the reviewed ambient proof. Full row rank and
\(\|T\|_2\le1\) are explicitly imposed where that proof needs them.

The scope statements are accurate. The parameter is the dimension of the
**supplied separable decomposition**, not automatically the negative inertia
of an arbitrary quadratic objective. General spectral normalization can
destroy separability. The aligned bound is FPT in that dimension and the
displayed numerical width ratios. The ambient bound contains powers of the
ambient dimension depending on the factor dimension and is not the same
FPT result. Arbitrarily many integer coordinates are allowed because the
product-domain scalar oracle handles them in polynomial work per query.
Coupling constraints or a dense convex residual are outside this argument.

The note's counterexample correctly distinguishes a certified global
region from matching integer winners at cell corners. Direct substitution
gives \(q_0=0\) and \(q_1=a^2/2-a/2+1/16\): the latter loses at
both endpoints and wins at the midpoint. The rescaled example preserves
this failure while satisfying \(\|T\|_2<1\).

For distinct executable confidence, I wrote and ran

```sh
python research-20261002/reviews/check_mixed_separable_sections.py
```

The [diagnostic](check_mixed_separable_sections.py) uses exact fractions
on a mixed fixture with a dense two-row factor, an integer piecewise
quadratic coordinate with a long tie, a continuous flat interval next to
curved pieces and a derivative jump, and a continuous absolute-value term.
It checks all state-boundary points and intervening intervals on 24
ambient-coordinate lines. An independent scalar candidate enumeration
supplies the reference value; exact central differences check gradients
of each active quadratic extension, including boundary overlaps.

It passed 204 boundary queries, 228 open-interval checks, 780 active branch
checks, 1,560 gradient identities, and 912 quadratic value identities.
There were 204 queries with overlapping active regions. This adds coverage
of entire parameter-line decompositions to the author's separate cell
diagnostic. It is not an implementation of the full optimization algorithm,
an empirical expectation estimate, or a substitute for the probability
proof. No external research, project-wide verification, or CI inspection
was performed.

A scoped inline `python - <<'PY'` check also passed: both new files had
final newlines and no trailing whitespace, the review's mathematical
delimiters balanced, and all four local Markdown links resolved.
