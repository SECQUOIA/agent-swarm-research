# Independent review of the certified integer-recourse value corollary

Date: 2026-10-02. Verdict: **PASS** on the actual saved
[certified-recourse corollary](core-value-certified-recourse.md).
The review followed completion of the independent
[main grid and cap review](core-only-noise-value-grid-review.md).
The separate all-core-dimensions extension in Section 4 also passed the
additional actual-file review recorded below.
No new mathematical fixtures or external searches were needed.

## The fixed-domain oracle interface is sufficient

The residual domain is a finite integer set fixed before choosing the
core. Holding a feasible residual label fixed while rounding only the
core therefore preserves feasibility at every corner. The supplied
coordinate upper-curvature bound is needed only on this fixed domain;
residual convexity, uniqueness, and label stability are not used.

For fixed rational core coordinates, the sampled linear core objective
is a rational constant. Adding it to both certified conditional endpoints
preserves their width and feasible upper witness. Thus the inherited
cell lower bounds, final-incumbent filtering, retained-corner estimate,
generated-cell cap, and ordinary-branch global certificates remain valid.

The statement correctly assumes a conditional solver whose bit work and
certificate verification are already proved polynomial for the specified
residual class. The existence of a bounded rational integer polytope does
not supply this solver. The explicit qualifications concerning TU and
nonlinear objectives are necessary and are present.

## The finite-format tail remains uniform

After rounding rational integer-coordinate bounds inward, let
\(N_i=u_i-\ell_i+1\). Each label has polynomial input bit length, and
both \(\sum_iN_i\) and \(\prod_iN_i\) are bounded by
\(2^{\operatorname{poly}(I)}\). Membership is the conjunction of the
finite coordinate-label disjunctions and the linear inequalities.

The projected growth predicate therefore still has exactly two quantified
blocks. Existential membership is conjoined with the formula, and
universal membership guards its growth inequality. Integer membership
does not add quantifier alternations. The threshold and fixed sampled
coefficients affect polynomial coefficients, not the atom-count or
degree bound. Fixed-block elimination consequently gives the required
scalar-section complexity \(2^{\operatorname{poly}(I)}\), uniformly in
coefficient heights and thresholds.

The core value is the minimum of finitely many continuous polynomials,
so it is continuous. Its proximal growth tail uses the core width sum
\(k\), independent of the number of residual labels. Tied residual
minimizers at a single core do not invalidate this projected-growth
argument. Finite-law atoms are handled by the main theorem's common
choice of sampling precision.

## The fallback separates base format from coefficient height

Enumerating the residual bounding box costs a base-only exponential
factor. Testing its linear constraints and substituting each feasible
label into the fixed-degree objective use polynomial bit work. The
substituted polynomial has only \(k\le2\) continuous variables and fixed
degree, with coefficient lengths polynomial in the base input and sampled
noise length.

Exact real-algebraic optimization for each such fixed-dimensional core
problem therefore has polynomial coefficient-height cost, including tied
or positive-dimensional core optimal sets. Comparing the resulting
algebraic values pairwise selects a best label. One keeps one current best
value; there is no need to build a common field for every enumerated
candidate or to expand a sum of algebraic values. Alternatively, the
already reviewed two-block exact fallback applies to the full finite
membership formula.

After selecting a label, rational approximation and coordinatewise
clipping of the core preserve that label's feasibility. Polynomial
coefficient bounds control objective variation, so a polynomial number
of additional accuracy bits gives the promised feasible upper value.
Refining the exact global value gives the matching lower bound. Hence
the whole fallback fits
\(B_0\operatorname{poly}(I+b+q)\), with
\(B_0=2^{\operatorname{poly}(I)}\) independent of noise length \(b\)
and requested precision \(q\).

These are exactly the height and format separations needed by the
inherited cap-and-moment proof. The one base law works at every accuracy.
The explicit \(L\ge0\) assumption and its separate zero-curvature branch
are also correct.

## All core dimensions: separate extension review

The new Section 4 was reviewed after the preceding \(k\le2\) corollary.
Verdict: **PASS** for arbitrary \(k\ge1\), conditional on the same
uniform polynomial-time certified recourse interface. Its expected work
and proof/output bound is
\(f_d(k)(1+L/\sigma)^k\operatorname{poly}_d(I+q)\), with an absolute
polynomial exponent at fixed degree. The sharper linear numerical-ratio
bound for \(k\le2\) remains a separate valid conclusion.

The [reviewed all-scale theorem](all-scale-core-value-oracle.md) uses only
continuity of the projected objective in its geometric argument. A finite
fixed residual domain gives that continuity, and holding a residual label
fixed preserves the corrected-corner witnesses. Neither residual convexity
nor a topological property of the residual set is needed by this part of
the composition.

I read the actual two-block event formula in Section 5 of that theorem.
It uses \((k+1)^2\) near-optimal core points, their residual witnesses,
Caratheodory weights, padding vectors, and the quadratic QR and scalar
product-chain variables. Replacing each residual box witness by a feasible
integer witness changes only its membership formula. The total number of
real quantified variables is
\(O(k^2(k+m)+k^2)\), hence polynomial in the base input. There is one
existential block and one shared universal competitor block.

Finite conditional attainment supplies each existential residual witness
when its core point is near-optimal. Conversely, comparison with every
feasible competitor, including a global optimum, proves that core point
is near-optimal. Conjoining the comparisons for all witnesses permits the
same universal competitor variables; it does not introduce another
quantifier alternation or assume independence of those witnesses.

Every witness membership copy has at most exponential-in-polynomial base
size after expanding allowed integer labels. Polynomially many copies
still have atom-count logarithm polynomial in \(I\). The explicit QR
orthogonality/factorization equations and scalar product chains retain
degree at most two; the objective and free noise coordinate bring the
overall degree to at most \(\max(d,2)\). Thus fixed-block elimination
still gives scalar-section complexity \(2^{\operatorname{poly}_d(I)}\),
uniform in the threshold and coefficient heights. No volume predicate,
extra optimization quantifier, or residual-witness independence is hidden
in this substitution.

For fallback, the fixed-dimensional argument in the original review is
replaced explicitly. After any integer label is substituted, the core
instance has encoding length \(\operatorname{poly}_d(I)\). The generic
polynomial-box fallback permits arbitrary \(k\), with a base factor
\(2^{\operatorname{poly}_d(I)}\) and a fixed polynomial exponent in
added coefficient bits and requested accuracy. The exponential number of
labels multiplies only that base factor.

Each candidate value has a univariate representation with base-exponential
degree and coefficient length equal to a base-exponential factor times a
polynomial in noise bit length. Pairwise real-algebraic comparison has
polynomial dependence on these degrees and heights, with an absolute
exponent. Multiplying by the number of candidates therefore preserves a
single base factor \(B_0=2^{\operatorname{poly}_d(I)}\); keeping one best
candidate does not accumulate a common field or increase algebraic degree
through repeated arithmetic. Refinement of the selected core point and
coordinatewise clipping preserve the selected integer label's feasibility.

These format and height bounds are precisely what the inherited all-scale
cap proof requires. The same finite noise law and random work factor
control all requested accuracies. The \(L=0\) case uses \(2^k\)
conditional vertex calls and fits the stated parameter dependence.
No optimal-label stability or new integer solver is implied. No numerical
fixtures or source searches were duplicated for this extension review.

## Scope and verification record

The corollary returns a feasible integer label supporting a certified
objective gap. It does not claim a stable or exactly optimal label, a
coordinate-distance guarantee, or a new integer optimization algorithm.
A residual domain depending on the core would require another feasible
rounding argument and is correctly excluded.

The initial read identified two minor input clarifications: rounding
rational integer-coordinate bounds inward and stating \(L\ge0\).
Both are present in the final actual file reviewed here. No substantive
proof gap remains.

This was a direct mathematical actual-file review. No new fixtures,
project-wide tests, CI inspection, external searches, or index edits were
performed. The main algorithm's existing exact grid diagnostic and the
separate probability review remain the applicable recorded checks; they
were not duplicated for this interface substitution.

A scoped inline Python check passed this review's math delimiters,
whitespace, and local links, together with the companion grid review and
saved checker syntax. A `git diff --check` restricted to those three files
also passed. Neither command reran mathematical fixtures.

After adding the all-dimensional review, an inline Python command checked
this file's math delimiters, whitespace, and local links again. The command
`git diff --check -- research-20261002/new-direction/core-value-certified-recourse-independent-review.md`
also passed. No numerical fixtures were run for that addendum.
