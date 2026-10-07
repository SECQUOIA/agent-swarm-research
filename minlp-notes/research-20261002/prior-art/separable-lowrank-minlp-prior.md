# Prior art for separable convex costs with a low-rank concave interaction

Date: 2026-10-02. This audit compares the proposed projected-grid method for
mixed product boxes with exact low-rank quadratic algorithms, separable
convex optimization, and indefinite-MIQP approximation. It is a focused
comparison, not a priority claim.

## Candidate class and the relevant distinction

The candidate objective is

$$
F(x)=\sum_{i=1}^n g_i(x_i)-\frac{\alpha}{2}\|Tx\|^2,
\qquad \operatorname{rank}(T)\le r,
$$

on a product of bounded rational intervals, with any subset of the
coordinates restricted to integers. Each $g_i$ is convex; the concrete
polynomial-bit oracle in the current derivation is for convex rational
quartics. The intended guarantee assumes a quadratic-growth bound in the
projected coordinate $Tx$, and uses a fixed-domain inner problem that
separates by coordinate. Its main complexity distinction is the number of
integer coordinates and their numerical range: neither is enumerated. The
candidate gives a certified $2^{-q}$ objective gap in
$f(r,\alpha/g_T)\operatorname{poly}(I+q)$ bit operations; when every
coordinate is integer, a rational objective lattice lets the same algorithm
return an exact optimum after polynomially many additional accuracy bits.
The whole Hessian of the quadratic specialization can have full rank because
of the separable convex terms, even though the concave interaction has rank
at most $r$.

## Special cases that already have stronger algorithms

Several elementary regimes should be kept outside any solver-advantage
claim.

- **Binary variables, rank one.** On $\{0,1\}^n$, each unary term is affine.
  If the single row of $T$ has mixed signs, complement every variable whose
  coefficient is negative. The transformed coefficients in the square are
  nonnegative, so expansion of $-\alpha(Tx)^2/2$ gives nonpositive pair
  coefficients. The resulting pairwise binary energy is submodular and is
  minimized by an $s$-$t$ minimum cut. This is exact and needs no growth
  promise. It relies on product binary domains without additional side
  constraints. The graph-representability characterization is due to
  Kolmogorov and Zabih ([author page and paper](https://pub.ista.ac.at/~vnk/papers/WHAT_ENERGIES.html),
  DOI [10.1109/TPAMI.2004.1262177]).
- **Binary variables, fixed rank.** Since every binary unary is affine,
  negating $F$ gives a convex PSD quadratic of rank at most $r$ plus a linear
  term. Ferrez, Fukuda, and Liebling reduce the no-linear-term case to
  maximizing a convex quadratic over a rank-$r$ zonotope and enumerate its
  vertices in $O(n^{r-1})$ time for fixed rank. Hladík, Černý, and Rada
  handle an arbitrary linear term and arbitrary-sign quadratic matrix of
  fixed rank over a continuous box, with a face-enumeration bound
  $O(n^{2r+1}\,\mathrm{lp})$ after their linear-term lift. Their theorem
  applies to the binary problem because a convex quadratic on $[0,1]^n$
  has an optimizer at a vertex. These are exact fixed-rank polynomial
  algorithms, but have an exponent depending on $r$ (XP form), rather than
  the candidate's proposed FPT dependence on $r$ under growth. The sources
  are already read in the local KB: [[liebling2005-solving-the-fixed-rank-convex]]
  pp.4-8 and [[rada2021-a-new-polynomially-solvable-class]] pp.1-8.
- **Continuous variables, affine $G$.** If every $g_i$ is affine, then
  $-F$ is a convex quadratic of rank at most $r$ plus a linear term.
  Hladík–Černý–Rada therefore solve the continuous box case exactly for fixed
  $r$, without quadratic growth. This includes mixed-sign $T$ and arbitrary
  linear coefficients.
- **Continuous variables, rank one and convex quadratic $G$.** There is a
  direct scalar exact algorithm even when $G$ has a diagonal quadratic part
  of full rank. Write $v^Tx$ for the scalar projection and use

  $$
  F(x)=\min_{a\in\mathbb R}\left\{G(x)-\alpha a v^Tx+
  \frac{\alpha}{2}a^2\right\}.
  $$

  The projection $a$ can be restricted to the interval $v^T X$. For fixed
  $a$, each continuous coordinate minimizer of its shifted convex quadratic
  is a clipped affine function of $a$ (or an endpoint choice for a linear
  coordinate). There are at most two breakpoints per coordinate. Between
  consecutive breakpoints the minimized value is quadratic, so its exact
  global minimum is among interval endpoints and any interior stationary
  point. Rational input yields rational breakpoints and stationary points.
  This gives polynomial-time exact optimization, without the candidate's
  growth hypothesis. It is a direct scalar reduction; it should not be
  presented as a new benefit of the proposed method.

These baselines mean that the candidate's useful regimes, if established,
are more specific: rank at least two with FPT rather than XP dependence,
nonlinear continuous separable recourse beyond quadratic coordinate
responses, or large binary-encoded integer ranges with arbitrarily many
integer coordinates.

## Separable optimization and coupling constraints

Hochbaum and Shanthikumar show that separable convex optimization over
linear constraints can be reduced to a sequence of linear or integer linear
optimization calls. Their guarantees make dependence on the largest
constraint subdeterminant explicit; the continuous accuracy dependence is
logarithmic, and the integer version is polynomial when the corresponding
integer-linear oracle is polynomial. This is a strong antecedent for the
coordinatewise convex recourse, but the method does not optimize a
nonseparable concave rank-$r$ interaction. In the candidate's product-box
subproblems, coordinatewise derivative bisection and discrete-convex
binary search give the needed oracle directly. [[hochbaum1990-convex-separable-optimization-is-not]]
pp.1-5, 9-17

Del Pia's separable concave integer-QP scheme has a different structure:
only $k$ coordinates carry separable concave quadratic terms, while the
others are linear, and the approximation cost depends on $k$ and the
constraint matrix's subdeterminants. Its subdeterminant-preserving
decomposition gives polynomially many ILPs for fixed $k$ and bounded
subdeterminants; the totally unimodular case uses LP calls. It does not cover
a dense low-rank concave interaction added to an arbitrary convex separable
base. [[pia2019-subdeterminants-and-concave-integer-quadratic]] pp.1-3,
17-20

Brand, Koutecký, Lassota, and Ordyniak show that extending important
structured-constraint classes such as $n$-fold and two-stage stochastic
programs from linear objectives to separable-convex mixed-integer objectives
can be harder than the linear versions. That result is a boundary warning
about adding coupling constraints; it does not cover a product box or the
candidate's objective. [Official paper page and open full text](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2024.32),
DOI [10.4230/LIPIcs.ESA.2024.32](https://doi.org/10.4230/LIPIcs.ESA.2024.32).

## Low-rank and indefinite quadratic predecessors

Mittal and Schulz give an FPTAS for objectives of the form
$f(x)=g(a_1^Tx,\ldots,a_k^Tx)$ over a polytope, by building an approximate
Pareto front for those $k$ linear forms. Under their positivity, monotonicity,
and scaling conditions, the number of LP calls is of order
$(\log(M/m)/\epsilon)^k$. This is not the same function class: the sum of
coordinate costs generally depends on all $n$ variables and does not factor
through $Tx$. Their guarantee is multiplicative with polynomial dependence
on $1/\epsilon$, not a QG-conditioned logarithmic-accuracy or exact-rational
bound. [[schulz2013-an-fptas-for-optimizing-a]] pp.1-10, 13-17

For quadratic costs, Del Pia's 2023 theorem gives objective-range-relative
$\epsilon$-approximation for bounded MIQP when the rank of the **whole
quadratic matrix** and the number $p$ of integer coordinates are both fixed.
It allows arbitrary linear constraints, but does not give an exact result
or a guarantee when $p$ grows. In a convex-quadratic separable base minus a
rank-$r$ square, the full Hessian may have rank $n$, and the number of
integer coordinates can be arbitrary, so the candidate is not a direct
special case. [[pia2023-an-approximation-algorithm-for-indefinite]] pp.1-3,
19-31

Del Pia's 2026 rational-Jacobi theorem instead parameterizes by negative
inertia and the number of integer variables. For fixed negative inertia
$k_-$ and fixed integer dimension $p$, it gives objective-range-relative
approximation in time polynomial in input length and $1/\epsilon$ on
bounded-below rational MIQP. In the quadratic specialization of the
candidate, convexity of the separable base ensures at most $r$ negative
eigenvalues. The existing theorem still fixes $p$ and is approximate; the
candidate instead uses the product-box oracle, projected quadratic growth,
and integrality of objective values to handle arbitrary $p$ and recover an
exact all-integer optimum. For a genuinely quartic base, the MIQP theorem
does not apply. The continuous low-inertia branch-and-bound predecessors
and their $\epsilon^{-r/2}$ cell counts are compared in
[the companion QP audit](convex-recourse-prior.md). [[pia2026-rational-jacobi-rotations-and-the]]
pp.1-2, 18-22

## Assessment and limitations

The low-rank lift, convex inner minimization, zonotope enumeration for
fixed-rank quadratic problems, and spatial partitioning in negative-curvature
coordinates all have close precedents. The possible contribution is the
combination of (i) an inner oracle for separable convex mixed recourse on
binary-encoded product boxes, (ii) active-cell packing from projected
quadratic growth, and (iii) FPT dependence on projected rank and
curvature-to-growth ratio with only logarithmic target-accuracy dependence;
the all-integer specialization may convert that certificate into exact
optimization by a rational value lattice. This is a focused distinction,
not a novelty conclusion from an absence search. The binary, rank-one
continuous quadratic, and affine-base fixed-rank cases above already have
exact algorithms with weaker assumptions or simpler reductions.

The proposed method is not a general solver improvement claim. It assumes a
product domain and a certified fixed-domain oracle; the polynomial-bit result
currently follows from explicit convex-quartic responses. General coupling
constraints can destroy this oracle. For mixed models with continuous
coordinates, the stated output is a certified approximation, not an exact
rational optimizer. A useful comparison must also separate the candidate's
FPT parameterized bound from the $n^{O(r)}$ exact algorithms in binary and
fixed-rank quadratic special cases.

## Source status

The read local packages are Hochbaum–Shanthikumar (1990), Del Pia (2019,
2023, 2026), Ferrez–Fukuda–Liebling (2005), Hladík–Černý–Rada (2021), and
Mittal–Schulz (2013). The separate 2026 indicator-MIQO decision-diagram
paper is already in the KB but concerns convex low-rank quadratic costs,
not this negative-curvature objective. I routed the missing Brand et al.
(2024) source and the Kolmogorov–Zabih graph-cut primary source to the sole
ingestion agent for serialized processing. No bibliography package was
modified here.
