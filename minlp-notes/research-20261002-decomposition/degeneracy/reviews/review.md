# Independent review of the degeneracy extensions

Date: 2026-10-02. This review checks the actual saved derivations and their
stated dependencies. It does not establish external priority or competitive
solver performance. Only checks targeted to these notes were performed.

## Unknown growth on the diagonal-certificate class

The argument in [the diagonal-class note](../unknown-growth-diagonal-class.md)
correctly combines the existing proximal-grid and exact-recovery theorems
with an acceptance test that is valid even for an incorrect growth guess.
The distinction between the candidate search and the acceptance test is
essential.

The following points were checked directly.

1. The diagonal identity has the correct boundary-gradient signs and
   Hessian. Box KKT makes every diagonal entry nonnegative; positive
   semidefiniteness makes the remaining quadratic term nonnegative.
2. At any other optimizer, every nonnegative term vanishes. Kernel
   membership yields the gradient identity, and positive diagonal entries
   force endpoint coordinates. These facts recover the identical maximal
   diagonal at every optimizer. Thus an arbitrary rational optimum returned
   by the recovery LP passes whenever one optimum admits this certificate.
3. An invalid growth trial still has finite work. Its radius and geometric
   grading bound the coordinate grids independently of optimality, its
   explicitly imposed stage budget bounds refinement, and the dyadic
   denominator argument does not use growth. Each fresh box contains its
   feasible center even if it contains no global optimizer.
4. At the first valid doubled guess, the objective-gap bound gives distance
   at most half the recovery threshold. The recovery LP uses only original
   coefficients and selected original bounds. The earlier stationary-polytope
   argument therefore supplies a global optimizer of polynomial rational
   length without enumerating optimal components.
5. The full-set output uses a rational kernel equation and endpoint
   polynomials. It does not require matrix square roots or expanded
   components. Positive semidefiniteness is essential when replacing zero
   quadratic form by kernel membership.

One precision issue was reported to the author: choosing an *arbitrary*
dyadic accuracy below the trial threshold permits arbitrarily many bits and
does not prove the displayed runtime. Choosing the largest dyadic at most
that threshold, or one within a fixed constant factor, resolves the issue.
The saved note now specifies the largest dyadic, so this issue is resolved.

The earlier invalid-growth fixture gives a useful independent check of the
acceptance gate. For

\[
 F(x,y)=x^2+y^2-3xy+\frac{63}{128}(x+y),\qquad (x,y)\in[0,1]^2,
\]

the false narrow interval approaches the nonglobal KKT point \((0,0)\).
At that point the shifted Hessian has diagonal \(191/64\), off-diagonal
\(-3\), and eigenvalue \(-1/64\), so the new verifier rejects it. At the
true optimum \((1,1)\), its diagonal is \(193/64\) and its smallest
eigenvalue is \(1/64\), so the verifier accepts. Merely checking KKT would
not make this distinction.

The claimed theorem remains restricted to continuous box QPs admitting
the diagonal certificate. It neither decides membership in that class nor
establishes termination outside it. Those limitations are explicit.

## Every optimizer of a coordinatewise concave quadratic

No mathematical gap was found in
[the endpoint full-set note](../endpoint-optimal-set.md). Independent
endpoint rounding preserves linear and off-diagonal terms and adds
\(Q_{ii}(x_i-\ell_i)(u_i-x_i)\) to each diagonal term. This verifies the
sign of the variance correction in the full-set identity.

The Bellman residuals are nonnegative for every local endpoint assignment.
Running intersection and the standard parent-separator recurrence make
their global sum telescope to the endpoint objective minus its optimum.
Taking independent-rounding expectations therefore gives an identity whose
summands are all nonnegative when \(Q_{ii}\le0\). Their simultaneous
vanishing is both necessary and sufficient for optimality.

The strict-negative-diagonal endpoint condition is required, including for
interior integer labels. When the diagonal is zero, the residual products
correctly test the full independent-rounding support. They do not confuse
coordinate projections of optimal corners with optimal Cartesian products.
The two-corner example in the note demonstrates this distinction.

The factored equations have at most one product per positive residual
entry, so their size obeys the claimed \(2^{O(p)}\operatorname{poly}(I)\)
bound. Messages share the original rational endpoint-evaluation
denominator; table elimination does not multiply denominators. For mixed
boxes, the descriptor retains the original integrality requirements and
does not enumerate long integer intervals.

## Boundary-face extension

No mathematical gap was found in
[the saved active-face note](../boundary-active-face.md). Its explicit
active-gradient precision parameter is necessary. Strict complementarity
alone does not bound this precision by input length and the point-growth
ratio, as the existing nearby-minimum construction demonstrates.

The proof correctly distinguishes two consequences of derivative signs.
A weak sign preserves the minimum value and at least one minimizer under
endpoint substitution. A strict sign also forces every minimizer onto that
endpoint. The final certificate therefore claims an exact selected global
optimizer and uniqueness within the strongly convex restricted problem,
without claiming uniqueness in the original box after weak reductions.

Once the integer labels have been fixed, the continuous-Hessian row-sum
bound controls the midpoint derivative error. When the current half-width
is at most one quarter of the active margin divided by that bound, the
strict sign test detects every active continuous coordinate. Sequential
substitution keeps the unique optimizer under the theorem's promise and
does not enlarge the half-width. Every remaining coordinate is interior;
two-sided second-order limits of point growth give the stated free-Hessian
lower bound. No numerical distance from those coordinates to their bounds
is required.

The patch inequality includes both the midpoint-to-point Hessian variation
and the positive certified curvature. Its displayed thresholds make the
inequality strict. The needed number of refinement stages has additive
dependence on the active-gradient precision term. Generating independent
Bernstein bounds for the original factors respects the width parameter and
does not require a dense tensor basis over the full variable set.

The bit-step dovetail is a sound way to combine unknown conditioning and
unknown precision. In phase \(q\), the total allotted simulation time is
less than \(2^{q-1}\); restarting from scratch is harmless. A successful
trial of index \(\mu_*\) and runtime \(A\) completes by a phase with
\(q\le\mu_*+\lceil\log_2\max\{1,A\}\rceil\), giving the claimed
parameterized runtime after simulation overhead. Interleaving whole
unbounded stages instead would need a separate work bound, and increasing
the grading parameter once per precision stage would lose this result.

An early accepted patch may have poor certified curvature. The note does
not assume otherwise: its favorable approximation bound uses the original
certified enclosure algorithm under unique point growth. The restricted
strongly convex problem still provides an unambiguous exact descriptor
without that promise; only the favorable evaluation cost uses it.

## Targeted verification

An independent inline `python3 - <<'PY'` check using `fractions.Fraction`
passed 18 diagonal identities, including rejection of the nonglobal KKT
point above and acceptance at its global optimizer. A second part passed
162 endpoint-interpolation identities on a branching decomposition with
overlapping bags, once with zero diagonals and once with negative and zero
diagonals. These are exact small diagnostics of the certificate algebra,
not an implementation or performance test of either search algorithm.

An inline Python document check inspected this review's local links and
trailing whitespace and checked paired display delimiters in the three
reviewed derivations. It passed. No project-wide verification or CI
inspection was performed.

### Review of the final diagnostic and scope claims

The final [diagnostic script](../check_extensions.py) and
[README](../README.md) were also inspected. Running
`python3 -B research-20261002-decomposition/degeneracy/check_extensions.py`
passed the reported 256 diagonal/full-set cases, 135 mixed endpoint cases,
the 21-stage proximal/recovery fixture with 1,158 exact local evaluations,
and 34 boundary/precision cases. The recovery fixture correctly permits
either optimal mode and movement along the free coordinate. Its direct
solution of the free stationary equation is valid for that fixture; the
README does not claim a general LP implementation or full boundary search.

One diagnostic coverage issue was identified and fixed: sampled derivative
signs alone did not justify describing a full-box weak-sign certificate as
checked. The saved script now verifies exact derivative identities and
their complete Bernstein coefficient lists, respectively
\((1,1,1,3/2)\) and \((1,0)\). These nonnegative coefficients certify
the claimed signs over the full example boxes. A targeted rerun of
`check_boundary()` through an inline `python3 -B`/`runpy` command passed
after this change. No unresolved coverage issue was found.

A final inline Python check of links and trailing whitespace passed for
the four top-level Markdown files and this review. These checks remain
separate from the mathematical diagnostics and from CI.
