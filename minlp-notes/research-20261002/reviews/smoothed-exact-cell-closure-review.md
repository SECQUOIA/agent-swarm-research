# Independent review of exact closure under fixed rational noise

Date: 2026-10-02. Scope: the complete
[smoothed exact cell-closure theorem](../new-direction/smoothed-exact-cell-closure.md),
including its active-basis extraction, probability estimate, fixed noise
law, and bit-complexity claim. No substantive gap was found in the stated
continuous-QP result. This review does not establish publication priority.

## Finding and essential scope

The proposed closure operation supplies the ingredient missing from the
approximate expected-cell theorem. Most samples finish after a base-data
number of refinement stages; exceptional samples, including noise atoms,
use the exact fallback on the same objective. The refinement cutoff and
noise resolution are chosen before sampling and have polynomial encoding
length. They do not use the sampled objective's rational recovery height.

The conclusions are for the specifically constructed rational noise law
in the supplied factor coordinates. They are not a theorem for arbitrary
coarse atomic noise, independent noise in every original coefficient, or
the unperturbed objective. The recourse feasible set is a continuous
rational polytope. General mixed-integer recourse would require a new
argument: its optimal set need not have the convex-polytope description
used below, and its envelope need not be continuously differentiable.

## Smoothness and active-basis extraction

The condition \(\ker P\subseteq\ker T\) is sufficient for the
claimed \(C^1\) envelope. Any two convex inner optimizers differ by
a vector in \(\ker P\), so their \(T\)-images agree. Compactness
then makes that image continuous in the parameter, and the attained-value
comparison proves
\(\nabla W(a)=\alpha(a-Tx(a))\). The global identity
\(W(a)-\alpha\|a\|^2/2=\inf_x\{\text{affine in }a\}\)
supplies the full quadratic upper model, not merely coordinatewise
curvature.

The kernel condition is substantive. With \(P=0\), \(T=1\),
\(\alpha=1\), \(F(x)=-x^2/2\), and \(X=[-1,1]\), the
envelope is \(W(a)=a^2/2-|a|\), which is not differentiable at
zero. The reviewed normalization removes this failure by putting every
residual null direction in \(\ker T\).

At a query, the written description of the entire convex optimal set is
correct: the quadratic objective gap is the sum of a nonnegative linear
first-order term and a nonnegative PSD quadratic term. Both vanish
exactly on the stated linear equalities. A vertex of this optimal polytope
can be found by polynomial rational LP, including in lower dimension.
Lexicographic optimization is valid here; each successive optimum is
attained at a vertex of the original optimal polytope, so it does not
cause uncontrolled recursive coefficient growth.

At that vertex, the residual Hessian is positive definite on the tangent
of its original active face. A null tangent would give two feasible
optimal displacements, contradicting vertexhood. Nonnegative multipliers
exist by the polyhedral normal-cone formula, without a Slater assumption.
Removing dependencies in their positive support preserves nonnegativity;
extending that support with zero multipliers gives an independent basis of
the full active row space. This proves nonsingularity of the displayed
KKT matrix. These operations are polynomial rational computations, not
an enumeration of all critical regions.

Lower-dimensional original polytopes, redundant rows, and nonunique inner
optimizers therefore do not obstruct the extraction. The global set of
possible row subsets remains bounded by \(2^m\), independently of
queries and noise.

## Lower-dimensional critical regions and exact cell solves

Agreement of \(W\) with a quadratic on a lower-dimensional critical
region would not, by itself, establish equality of their full gradients.
The written proof correctly uses the algebraic KKT envelope identity
instead. Differentiating the active equalities gives
\(M_Jx'_J=0\), so the multiplier term cancels and

\[
 \nabla q_J(a)=\alpha(a-Tx_J(a)).
\]

At a feasible KKT parameter this equals \(\nabla W(a)\), even
when the region has empty interior.

The algorithm tests regions extracted at every cell corner. Thus an
unclosed cell in particular failed the region test at its near-optimal
corner. Testing only an unrelated corner would not justify the later
gradient estimate; the completed algorithm avoids that error.

If one region contains the entire cell, its quadratic is the exact value
function there. Enumerating \(3^k\) box faces and solving nonsingular
free stationarity equations includes a global minimizer: choose a global
minimizer in a face of smallest dimension, whose tangent Hessian must be
positive definite or zero-dimensional. Feasible candidates from other
faces are harmless. The affine recourse witness at the chosen parameter
is valid because the entire cell is in its critical region.

Closing a cell and updating the incumbent preserves the global search
invariant. Its exact local minimum cannot fall below the updated incumbent.
Ordinary discarded cells retain valid lower bounds. Retention is refreshed
after all closure updates at a level. If no unresolved cells remain, the
stored auxiliary incumbent is exactly global; its recourse witness then
attains the original optimum by square completion.

## Hyperplane event and arithmetic constants

The global upper model gives
\(\|\nabla V_\xi(v)\|^2\le2\alpha(V_\xi(v)-\min V_\xi)\)
by testing the point \(v-\nabla V_\xi(v)/\alpha\). This point
may leave the auxiliary box, but the proof correctly uses the global
envelope on \(\mathbb R^k\), whose minimum equals the box minimum.

For a retained unclosed cell, the near-optimal corner has small gradient.
If its piece Hessian is invertible, some nonzero defining row of the
critical region is crossed inside that cell. Mapping that hyperplane by
the affine negative-gradient map gives a fixed hyperplane close to the
noise sample. If the Hessian is singular, its entire affine gradient image
already lies in a fixed hyperplane. This covers critical regions with
empty interior and does not require an irredundant facet description.

The Cramer bound includes the scaled KKT right-hand-side coefficients
\(b,d,\alpha T^T\), as required. Its numerator determinants have
order at most \(2n\), while a nonzero integral denominator determinant
has magnitude at least one. Consequently the stated \(U\) bounds
every affine optimizer coefficient, and
\(H_0=\alpha(1+nkU)\) safely bounds every piece Hessian. Large
values enter the cutoff through logarithms only.

There are at most \(K=2^m(m+n+1)\) needed hyperplanes. For each,
conditioning on the other noise coordinates leaves an interval of length
at most \(2\sqrt{k}\eta\) in a coordinate with sufficiently
large normal component. The finite-grid probability bound is therefore
\(\sqrt{k}\eta/\sigma+1/N\). Independence is used at this
step with a fixed base-data hyperplane; adaptively discovered regions are
covered by the finite base-data union.

The displayed choices of \(J\) and \(N\) make the union bound
at most \(1/B\), including its atomic term. They also ensure
\(N\ge m_{iJ}\), so the earlier finite-noise expected-cell bound
applies at every stage before the fallback. All their logarithms have
polynomial base-input length.

## The fallback closes the precision argument

The fallback factor \(B\) counts original active-row subsets; it
does not need to dominate the full bit cost. Exact face enumeration costs
\(B\operatorname{poly}(L)\) for perturbed input length \(L\).
Its probability at most \(1/B\) therefore contributes polynomial
expected work. The noise uses polynomially many bits, so \(L\) is
polynomial in the base input.

This avoids the earlier circular argument in which a rational recovery
threshold depends on the chosen noise precision, which in turn depends
on that recovery threshold. Here the cutoff depends on base critical-region
geometry, and remaining samples are solved directly. No rare sample is
discarded or resampled. Exact flatness at a grid atom is permitted and
covered by the fallback.

The additional critical-region extraction and local \(3^k\) face
solves multiply the expected cell work by a dimension factor and a
polynomial with an absolute exponent. No region enumeration, exponential
height, or denominator product is hidden in each query. The stated
expected bound is consistent with these costs.

## Targeted exact checks

The command
`python research-20261002/new-direction/check_exact_cell_closure_review.py`
passed four fixtures, with 208 corner queries, 34 closed cells, and 52
retained unresolved cells across their tested noise samples and levels.
They covered:

- a singular residual Hessian with a flat inner optimizer coordinate,
  while satisfying the kernel condition;
- a critical region consisting of one parameter point, alongside singular
  quadratic pieces;
- a lower-dimensional original polytope with redundant equality rows;
- a literal endpoint noise atom that leaves an unresolved cell and thus
  exercises the same-draw fallback case.

The last fixture uses \(X=[0,1]^2\),
\(T=(1/2,-1/2)\), \(\alpha=4\), base objective
\(F(x,y)=xy-T(x,y)\), and sample \(\xi=1\). This sample is
an endpoint of every specified symmetric finite grid. The perturbed
objective is \(xy\); its critical switch is at \(a=-1/4\),
which lies at relative position \(1/3\) in the auxiliary box
\([-3/4,3/4]\). The corresponding cell continues to cross that
switch under equal dyadic refinement. The test confirmed an unresolved
cell through its last level, while the exact fallback returned the known
global value on the same sample.

The checks verified the affine KKT gradient identity, agreement between
all feasible pieces at each queried parameter, exact recourse values,
coefficient and curvature height bounds, exact closed-cell minimization,
the incumbent error bound, and membership in the claimed bad-hyperplane
tube whenever a cell remained unresolved. They also checked the necessity
of the finite-grid atom term and the nondifferentiable example obtained
by dropping the kernel condition.

The diagnostic enumerates small KKT bases to provide an independent
reference; it does not claim to implement the polynomial extraction
procedure or to benchmark the full algorithm. A temporary run of the
final atom-count check required converting SymPy Boolean values to Python
integers before summing; the corrected final command passed.

The scoped command
`git diff --check -- research-20261002/reviews/smoothed-exact-cell-closure-review.md research-20261002/new-direction/check_exact_cell_closure_review.py`
passed. An inline `python - <<'PY'` check of whitespace, paired
mathematical delimiters, and local references also passed.

No project-wide checks, CI inspection, or external search were performed.
