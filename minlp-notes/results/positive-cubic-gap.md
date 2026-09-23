# Positive cubic polynomials can have a relaxation-gap ratio above two

The [focused cubic paper and Lean package](../paper-cubic-gap/README.md)
collects the universal upper bound, optimality among fixed mixtures of the
three stated rounding laws for uniform termwise guarantees, the analytic lower
family, and exact finite witnesses. Its [coverage map](../paper-cubic-gap/formal/COVERAGE.md)
and [verification record](../paper-cubic-gap/formal/VERIFICATION.md) identify
the formal statements and completed checks.

Date: 2026-09-04. Status: exact certificates, upper-bound argument, and full written result independently checked; no unresolved mathematical issue identified. See `notes/review-positive-cubic.md`. Literature novelty remains subject to a separate source check.

## Result

There is an explicit polynomial in 52 variables with 4,320 distinct cubic monomials, every coefficient equal to one, whose term-by-term/convex-hull gap ratio at a strictly interior point is at least

\[
\frac{2700}{1343}>2.
\]

The [two-marginal construction](positive-cubic-two-level-family.md) gives the polynomial and proof. Its simpler 32-variable predecessor has exact ratio 135/67. The examples below include an 18-variable witness with ratio 20891/10411, a 24-variable witness with exact ratio 6601/3225, and a 192-variable witness with exact ratio 7443345/3445256>2.16.

Thus degree three already permits a ratio above two, even with homogeneous unit-coefficient polynomials and interior evaluation points. Degree two does not, by the known positive-bilinear factor-two theorem of Luedtke–Namazifar–Linderoth. This identifies the smallest possible degree, not the smallest possible number of variables.

The independently audited [three-distribution coupling](positive-cubic-rounding-upper-bound.md) shows that every positive multilinear polynomial of degree at most three satisfies

\[
\operatorname{tbtgap}(x)\le\frac{31}{12}\operatorname{chgap}(x)
\]

on every finite nonnegative box. Consequently the worst positive cubic ratio R(3) satisfies

\[
\frac{1610000}{743033}\le R(3)\le\frac{31}{12}.
\]

The lower bound follows from the [analytic cubic family](positive-cubic-analytic-family.md), including its positive Bernstein slack; omitting that slack gives the simpler bound 483/223. The two-sided bound is proved in Lean by [`cubic_boxDegreeSupremum_sandwich`](../formal/Formal/CubicGap/AnalyticResults.lean). The examples below have exact finite-dimensional hull gaps. The exact value of R(3) remains open in this investigation. The upper-bound coupling below is elementary, but its novelty has not been established; it is included as a useful verified companion to the new counterexamples.

The earlier [finite-witness package](../formal/topics/04-cubic-gaps/COVERAGE.md) also proves the 52-variable homogeneous unit-coefficient bound. The 25-variable homogenization and general coefficient-removal arguments below are outside the two cubic Lean packages.

## An explicit 24-variable polynomial

Let U,V,W be three disjoint groups, each containing eight variables. Write

\[
A=\sum_{i\in U}x_i,\qquad B=\sum_{i\in V}x_i,\qquad C=\sum_{i\in W}x_i,
\]

and let E_k(Q)=Σ_{S⊆Q, |S|=k}∏_{i∈S}x_i denote the elementary symmetric multilinear polynomial on group Q. Define

\[
f(x)=2E_3(W)+3B E_2(W)+13E_2(V)+12AC+8AB+7E_2(U).
\tag{1}
\]

Every monomial is squarefree and has a positive integer coefficient. There are 464 monomials, of degrees two and three. Evaluate at

\[
x_i=1/4\ (i\in U),\qquad x_i=1/2\ (i\in V),\qquad x_i=3/4\ (i\in W).
\tag{2}
\]

The term-by-term upper bound, which equals the concave envelope, is 971. The only positive termwise convex-envelope contributions come from E_3(W), giving the total lower bound 28. Thus the term-by-term gap is 943.

At a binary vertex, A,B,C are success counts in {0,...,8}, and (1) equals

\[
F(A,B,C)=2\binom C3+3B\binom C2+13\binom B2+12AC+8AB+7\binom A2.
\tag{3}
\]

Equation (3) is a vertex identity only: the original multilinear polynomial is (1), not the expression obtained by substituting continuous group sums into binomial polynomials.

## Exact lower-envelope certificate

For every integer A,B,C∈{0,...,8},

\[
7F(A,B,C)\ge793A+770B+798C-5882.
\tag{4}
\]

This is a finite certificate checked in exact integer arithmetic at all 729 count states. The minimum residual 7F−793A−770B−798C+5882 for each fixed C is:

| C | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Minimum residual | 168 | 42 | 0 | 30 | 22 | 0 | 0 | 16 | 0 |

Every binary vertex has one of these count states, so (4) is a valid affine minorant on the binary vertices and hence a lower bound on the convex envelope. At (2), the means of A,B,C are 2,4,6. The affine bound therefore gives

\[
\operatorname{vex}f(x)\ge\frac{3572}{7}.
\]

The matching feasible distribution has count states

| (A,B,C) | Probability | F(A,B,C) |
|---|---:|---:|
| (1,2,8) | 2/7 | 405 |
| (1,5,6) | 4/7 | 507 |
| (8,4,2) | 1/7 | 734 |

Its count means are exactly (2,4,6). Conditional on a count state, choose the successful variables uniformly within each group. Each individual variable then has its prescribed mean in (2). Its expected polynomial value is 3572/7, matching the affine lower bound. Thus

\[
\operatorname{vex}f(x)=3572/7,\qquad
\operatorname{chgap}(x)=971-3572/7=3225/7,
\]

and the claimed ratio is 943/(3225/7)=6601/3225.

No floating-point optimization is needed to verify this certificate. The complete check, including every vertex-count inequality, all means, and primal–dual equality, is in `code/multilinear_ratio/verify_cubic_bounds.py`, which uses only Python integer and rational arithmetic. An independent agent checked the 729 inequalities and the distribution separately.

## A smaller 18-variable certificate

Use three groups of six variables with the same respective marginals 1/4,1/2,3/4, and define

\[
f_{18}(x)=2E_3(W)+3B E_2(W)+9E_2(V)+10AC+7AB+7E_2(U).
\]

This has 212 monomials. The exact values are

\[
\operatorname{cav}f_{18}=1647/4,\qquad
\operatorname{tbt}_{\rm lower}=10,\qquad
\operatorname{vex}f_{18}=2750/13.
\]

An affine minorant on all integer counts 0≤A,B,C≤6 is

\[
F_{18}(A,B,C)\ge74A+\frac{778}{13}B+\frac{842}{13}C-\frac{4816}{13}.
\]

It is attained in expectation by count states (1,4,4), (2,1,6), and (6,2,1), with respective probabilities 17/26, 4/13, and 1/26. Their means are (3/2,3,9/2). Uniform subsets within each group again realize the individual marginals. Therefore its hull gap is 10411/52, and its ratio is 20891/10411>2. The pure rational verifier checks all 343 count inequalities and the matching distribution.

## A stronger 192-variable certificate

A larger example improves the certified lower bound on R(3). Use three groups of 64 variables at the same marginals 1/4,1/2,3/4 and define

\[
f_{192}(x)=2E_3(W)+3B E_2(W)+120E_2(V)+105AC+70AB+63E_2(U).
\]

Its exact values are

\[
\operatorname{cav}f_{192}=587944,\quad
\operatorname{tbt}_{\rm lower}=20832,\quad
\operatorname{vex}f_{192}=34172072/105.
\]

On every integer count state 0≤A,B,C≤64, the affine minorant is

\[
F_{192}(A,B,C)\ge
\frac{871710A+900446B+899046C-51743768}{105}.
\]

A matching primal count distribution is:

| (A,B,C) | Probability |
|---|---:|
| (4,19,64) | 241/735 |
| (5,19,64) | 12/735 |
| (16,40,43) | 419/735 |
| (64,31,17) | 63/735 |

Its means are (16,32,48). Therefore

\[
\operatorname{chgap}_{f_{192}}=27562048/105,\qquad
\frac{\operatorname{tbtgap}_{f_{192}}}{\operatorname{chgap}_{f_{192}}}
=\frac{7443345}{3445256}>2.16.
\]

The pure verifier checks the affine inequality at all 65³=274625 count states using integer arithmetic, then checks exact equality of the primal and dual values. This larger certificate was derived after the smaller examples; its independent review is recorded separately in the cubic review note.

## A homogeneous cubic example at a strictly interior point

The 24-variable construction can be made purely cubic without evaluating an extra variable at the boundary. Write f=P+Q, where P=2E_3(W)+3B E_2(W) contains its cubic terms and Q contains its quadratic terms. Introduce one variable z and define

\[
g(x,z)=P(x)+zQ(x),\qquad z=999/1000.
\]

Every monomial of g has degree exactly three, retains a positive integer coefficient, and is squarefree. All 25 coordinates are strictly between zero and one. Since z exceeds every original coordinate, the concave envelope at this point remains 971. The original quadratic terms had zero termwise lower envelopes and still do after multiplication by z. The cubic terms are unchanged, so the term-by-term lower bound remains 28 and the term-by-term gap is exactly 943.

The sum of the quadratic coefficients, counting individual monomials, is

\[
13\binom82+12\cdot8^2+8\cdot8^2+7\binom82=1840.
\]

Thus 0≤Q≤1840 on binary vertices. Any joint binary vector (X,Z) with the specified x,z means satisfies

\[
\mathbb E g(X,Z)=\mathbb E f(X)-\mathbb E[(1-Z)Q(X)]
\ge3572/7-1840/1000.
\]

The padding variable Z has failure probability 1/1000. The marginal distribution on the original variables is feasible for the already certified envelope of f. Consequently

\[
\operatorname{chgap}_g\le3225/7+46/25=80947/175,
\]

and hence

\[
\frac{\operatorname{tbtgap}_g}{\operatorname{chgap}_g}
\ge\frac{165025}{80947}>2.
\]

This is a certified lower bound on the new ratio, not a claim of its exact envelope. It shows that the failure of factor two persists for homogeneous cubic polynomials at strictly interior points.

## Unit coefficients by a probabilistic existence argument

The [coefficient-removal lemma](positive-multilinear-coefficient-removal.md) shows that, for fixed degree and unrestricted dimension, restricting to unit coefficients and homogeneous polynomials at interior points does not change the supremum of the gap ratio. Its explicit application to the preceding 25-variable example proves the existence of a unit-coefficient homogeneous cubic counterexample with 25,000 variables. This is a finite but nonconstructive bound: no particular random sample is claimed to have been generated. The small integer-coefficient examples above remain the explicit certificates.

## A common endpoint-orientation coupling

For arbitrary x∈[0,1]^n, draw T uniformly on [0,1], and independently assign each coordinate a fair left/right orientation. For left orientation, set X_i=1[T≤x_i]; for right orientation, set X_i=1[T≥1−x_i]. Every coordinate has mean x_i.

For a monomial e of degree k+1≥2, choose an anchor with minimum marginal u. Conditional on its orientation, same-oriented coordinates impose no further restriction inside the anchor's interval. Each oppositely oriented other coordinate excludes an interval of length

\[
a_j=\min\{u,1-x_j\}
\]

from one end of the anchor interval. The excluded intervals are nested. Thus the monomial deficiency is the largest a_j among independently selected coordinates, each selected with probability one half. If a_(1)≥...≥a_(k) denote these lengths in descending order, its expected deficiency is exactly

\[
\sum_{j=1}^k2^{-j}a_{(j)}.
\]

Since both sequences 2^{-j} and a_(j) are nonincreasing, the rearrangement or Chebyshev sum inequality gives

\[
\sum_{j=1}^k2^{-j}a_{(j)}
\ge\frac{1-2^{-k}}{k}\sum_{j=1}^ka_j
\ge\frac{1-2^{-k}}{k}\min\left\{u,\sum_j(1-x_j)\right\}.
\]

The last quantity is the stated fraction of the monomial's term-by-term gap. The same joint distribution works for every monomial. Multiplying by positive coefficients and summing proves the general bound

\[
\frac{\operatorname{tbtgap}}{\operatorname{chgap}}
\le\max_{1\le k\le d-1}\frac{k}{1-2^{-k}}
=\frac{d-1}{1-2^{-(d-1)}}.
\]

The expression increases with k: equivalently (1−2^{-k})/k is the average of the first k terms of the decreasing sequence 1/2,1/4,... and therefore decreases. For degree three this is 8/3; for degree two it is two. Affine terms have zero gap. The [positive-expansion argument](positive-multilinear-degree-upper-bound.md) extends the bound to the original term-by-term relaxation on every finite nonnegative box.

This bound is weaker asymptotically than the [sharp harmonic bound](positive-multilinear-sharp-degree-growth.md), but much smaller at degree three.
