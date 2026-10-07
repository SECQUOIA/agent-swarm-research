# An independent constructive polynomial-box fallback

Date: 2026-10-02. Status: constructive proof; passed
[independent completed-text review](../reviews/polynomial-exact-fallback-review.md).
No literature-priority claim.

This note supplies an independent constructive proof of the
[exact fallback interface](polynomial-exact-fallback.md) used by the
[smoothed sparse polynomial theorem](smoothed-sparse-polynomial.md).
It handles every rational draw, including nonunique optima and
positive-dimensional stationary sets. Its exponential factor depends on
the base problem, while additional coefficient bits enter polynomially.
The construction uses symbolic polynomial arithmetic and univariate real
root isolation; it does not require generic input or multivariate
cylindrical decomposition.

## 1. Statement and output convention

Fix a degree bound `d>=1`. The base input consists of an explicitly
represented rational polynomial `F_0` of degree at most `d`, a nonempty
bounded product of closed rational continuous intervals and native-integer
intervals, and its variable types. Let `I` be its binary length. Additional
base data, such as a noise width or tree decomposition, may be counted in
`I` without affecting the result. Integer bounds are rounded inward;
reject any resulting empty domain. The theorem assumes the remaining
mixed domain is nonempty, and fixed coordinates may be substituted first.

For arbitrary rational linear coefficients `gamma_i`, put

\[
 F_\gamma(x)=F_0(x)+\sum_i\gamma_i x_i.
\]

Let `b` bound the binary length of each added coefficient. There is an
exact deterministic algorithm and a base-computable integer

\[
 B=2^{\operatorname{poly}_d(I)}
\]

such that the algorithm returns one global optimizer and its exact value
within

\[
 B(I+b+1)^{c_d}
 \tag{1}
\]

bit operations, for a fixed exponent `c_d`. It then supplies point and
value enclosures of error at most `2^(-q)` within

\[
 B(I+b+q+1)^{c_d}
 \tag{2}
\]

bit operations after enlarging the same `B` and exponent if necessary.
Neither depends on the realized coefficients or on `b` or `q`.

Each nonrational output coordinate is specified by a nonzero integer
univariate polynomial and a rational interval containing exactly its
selected real root. Rational coordinates may use the same format or an
ordinary fraction. The exact value is `F_gamma` evaluated at this tuple;
this polynomial expression is an exact real-algebraic value representation.
Equation (2) supplies numerical access to it. A common primitive element
or an expanded minimal polynomial is not part of the output requirement.

The output and its isolating intervals can have exponential length in
`I`. The polynomial dependence on new coefficient bits is the point of
(1), rather than a small-output assertion for arbitrary polynomial
optimization. Sparsity or interaction width is not used by this fallback.

## 2. Integer assignments and continuous faces

Let `n` be the total number of remaining variables and `n_c` the continuous
dimension. The number of integer assignments is at most `2^{poly(I)}`:
the logarithm of each finite integer interval's cardinality is bounded
by its endpoint encoding, and these encodings are part of `I`.

Enumerate those assignments. In each assignment, substitute the integer
values and minimize the resulting polynomial `f` on its continuous box.
The degree stays at most `d`. For fixed `d`, substitution and combining
monomials leave a polynomial number of terms and coefficient encoding
length polynomial in `I+b`. In particular, for a base-computable
polynomial `A_d`, we can clear coefficient denominators and write

\[
 f(x)=Q^{-1}\sum_{\alpha\in S}c_\alpha x^\alpha,
 \qquad
 1\le Q\le2^J,\quad |c_\alpha|\le2^J,
 \quad J\le A_d(I)(b+1).
 \tag{3}
\]

The same bound, enlarged if necessary, applies to the unsubstituted
objective and all rational interval bounds. There are at most
`s=poly_d(I)` monomials; the additional linear terms do not change this.

Enumerate all `3^n_c` continuous faces: each coordinate is fixed to its
lower bound, fixed to its upper bound, or left free. Repeated faces from
degenerate intervals can instead be removed during preprocessing. A
zero-dimensional face contributes its rational vertex immediately.
For a face with `r>0` free coordinates, the construction below gives a
finite list of real-algebraic candidates in its closed box.

## 3. A symbolic perturbation makes every face quotient finite

Choose a fixed even integer `D>d`, and write `a=D-1`. For a positive
parameter `epsilon`, perturb the continuous objective by

\[
 f_\varepsilon(x)=f(x)+\varepsilon\sum_{i=1}^{n_c}x_i^D.
 \tag{4}
\]

The parameter is symbolic. The algorithm never chooses a sufficiently
small numerical value for it. Fixed coordinates on a face contribute
only a constant to the perturbation. In the following equations, `f`
denotes its restriction to that face. Its free stationary equations are

\[
 x_i^a+\frac{1}{D\varepsilon}\partial_i f(x)=0,
 \qquad i=1,\ldots,r.
 \tag{5}
\]

Work over the field `Q(epsilon)`, and use a monomial order that compares
total degree first. Each derivative in (5) has degree at most `d-1<a`.
The leading monomials are consequently `x_1^a,...,x_r^a`. They are
pairwise relatively prime, so the equations are a Groebner basis: their
pairwise S-polynomials reduce to zero by the product criterion. This is
a deterministic algebraic fact about (5), not a genericity assumption.

The quotient therefore has the monomial basis

\[
 \mathcal M=\{x_1^{e_1}\cdots x_r^{e_r}:0\le e_i<a\},
 \qquad N_r=|\mathcal M|=a^r.
 \tag{6}
\]

This remains a basis after every specialization `epsilon!=0`, since the
same leading monomials and reduction rules remain valid. The ideal may
be nonradical; nothing below requires simple roots.

Let `M_i(epsilon)` be the matrix of multiplication by `x_i` in this
quotient, obtained by reducing `x_i m` for every `m` in (6). Its entries
are rational Laurent polynomials in `epsilon` with only nonpositive
powers. Form

\[
 \chi_i(\varepsilon,T)=\det(TI-M_i(\varepsilon)).
 \tag{7}
\]

Cayley--Hamilton in the quotient implies that every complex solution of
(5), for every nonzero real `epsilon`, satisfies
`chi_i(epsilon,x_i)=0`. This assertion includes multiple roots.

Multiply (7) by the smallest power of `epsilon` that removes all its
negative exponents. Then specialize `epsilon=0` and clear rational
denominators. This produces a nonzero integer polynomial `p_i(T)` of
degree at most `N_r`. It is nonzero because the chosen exponent leaves
at least one nonzero coefficient at power zero. Equivalently, one may
clear all powers first, divide out the largest common power of `epsilon`,
and then specialize.

The polynomial `p_i` may be a nonzero constant. In that case this face
has no bounded stationary limit in that coordinate, and supplies no
candidate tuples. Otherwise isolate all distinct real roots of each
`p_i` and enumerate their Cartesian products. Keep the tuples belonging
to the face's closed box. Spurious combinations of coordinate roots are
allowed: every retained tuple is an actual feasible point.

## 4. The candidate list contains an original optimizer

Fix an integer assignment. For every `epsilon>0`, choose a global
minimizer `x(epsilon)` of (4) on its continuous box. Compactness supplies
one. Along a sequence `epsilon_j` decreasing to zero, pass to a convergent
subsequence. The perturbation in (4) converges uniformly to zero on the
bounded box, so its limit `x*` minimizes the original `f`.

There are finitely many faces. Pass to a further subsequence on which
`x(epsilon_j)` lies in the relative interior of the same face. On each
member of this subsequence its free gradient vanishes. A vertex face was
already included directly. Otherwise (7) vanishes at every free
coordinate of every member of the subsequence.

After the normalization preceding `p_i`, (7) is an ordinary polynomial
in `epsilon` and `T`. Passing to the limit proves

\[
 p_i(x_i^*)=0\qquad(i=1,\ldots,r).
 \tag{8}
\]

The limit may move to the boundary of that face; this is why the candidate
test uses its closed box. Thus one enumerated coordinate-root tuple is
an original global optimizer. This argument does not require isolated
stationary points or a unique optimum of either objective.

Repeating over integer assignments includes a global optimizer of the
mixed problem. Compare the original `F_gamma` values of all feasible
candidates and return a least one, with any deterministic tie rule.
Additional feasible candidates cannot lower this minimum below the true
optimum. Sections 6--7 explain exact comparisons, including ties.

## 5. Degrees, heights, and candidate counts

All dimension-dependent bounds in this section are functions of the base
input. They do not place new coefficient bits inside an exponential.

A monomial `x_i m` reduced to construct `M_i` has total degree at most
`r(a-1)+1=O_d(n)`. Every application of (5) lowers total degree by at
least one. Thus a branch of the reduction uses `O_d(n)` replacements.
Each replacement multiplies coefficients by a derivative coefficient
and by `1/(D epsilon)`. With (3), every matrix entry has Laurent degree
`O_d(n)` and rational coefficient bit length
`poly_d(I)(b+1)`. The number of reduction branches is at most
`s^{O_d(n)}`, which is absorbed into `2^{poly_d(I)}`. Adding their
contributions increases coefficient bit length by their logarithmic count.

There are `N_r<=N=a^n_c=2^{O_d(I)}` rows in each multiplication matrix.
In (7), the degree in `T` is `N_r`, the Laurent exponent range is
`O_d(n N_r)`, and determinant expansion bounds coefficient bit lengths
by

\[
 H\le C_d(I)(b+1),\qquad C_d(I)=2^{\operatorname{poly}_d(I)}.
 \tag{9}
\]

The same bound covers the final integer `p_i`, after clearing rational
denominators. Polynomial-time exact determinant algorithms over the
polynomial ring compute these objects within a singly exponential base
factor times a fixed polynomial in `b+1`. The ring has only the two
symbolic variables `epsilon,T`; its explicit degree and coefficient
bounds above are singly exponential in base size. Division-free
characteristic-polynomial computation is one option.

Each face supplies at most `N_r^r<=a^(n_c^2)` coordinate-root tuples.
Including faces and integer assignments, the total candidate count is
at most

\[
 2^{\operatorname{poly}_d(I)}.
 \tag{10}
\]

Every output coordinate satisfies an integer polynomial of degree at
most `N` and coefficient bit length at most `H`, after enlarging `H` to
cover fixed rational coordinates as well. Reducible polynomials and
repeated roots are permitted. Taking a squarefree part for root isolation
only changes the displayed height bound by a polynomial in `N`.

## 6. An explicit nonzero-value separation bound

The following elementary bound makes exact comparisons possible without
assuming algebraic independence or constructing a common primitive
element. Suppose two candidate tuples `alpha,beta` have `n` coordinates.
Every coordinate satisfies a nonzero integer polynomial of degree at most
`N`, with coefficients of absolute value at most `2^H`. Write the common
objective as in (3), with at most `s` monomials, and define

\[
 E=N^{2n},\qquad
 R=1+\lceil\log_2\max\{1,s\}\rceil+J+2ndH+d(H+1).
 \tag{11}
\]

Then

\[
 \Delta=F_\gamma(\alpha)-F_\gamma(\beta)
 \quad\Longrightarrow\quad
 \Delta=0\ \text{or}\ |\Delta|\ge2^{-ER}.
 \tag{12}
\]

To prove it, let `a_i,b_i` be the nonzero leading coefficients of the
coordinate polynomials. The numbers `a_i alpha_i` and `b_i beta_i` are
algebraic integers: substituting them into their defining polynomials
produces monic integer equations. Put

\[
 A=\prod_i|a_i b_i|^d.
\]

Because every monomial has total degree at most `d`, the number
`z=Q A Delta` is an algebraic integer. Its field degree is at most
`E`. Every conjugate of every coordinate is a root of its integer
polynomial, so Cauchy's bound gives magnitude at most `2^(H+1)`.
It follows that every conjugate of `z` has magnitude at most `2^R`.

If `z!=0`, its field norm is a nonzero integer. All conjugates except
the chosen one therefore give `|z|>=2^(-R(E-1))`. Finally
`QA<=2^(J+2ndH)<=2^R`, proving (12). Reducible defining polynomials,
repeated coordinates, and coinciding candidate values cause no difficulty.

Feasibility against a rational endpoint `u/v`, whose numerator and positive
denominator have at most `J_0` bits, has the analogous bound

\[
 \alpha_i-u/v=0\quad\text{or}\quad
 |\alpha_i-u/v|\ge2^{-N(2H+J_0+2)}.
 \tag{13}
\]

Indeed, multiply the difference by `v|a_i|`, use algebraic integrality,
the same conjugate bound, and the integer norm. This decides inclusive
boundary membership exactly, including a coordinate equal to a box bound.

## 7. Exact comparisons and requested-precision evaluation

Integer univariate polynomials of degree at most `N` and coefficient
length `H` admit real-root isolation and refinement with bit work polynomial
in `N`, `H`, and the requested precision, with an absolute exponent.
One elementary implementation uses a squarefree subresultant Sturm
sequence, its exact rational sign tests, and interval bisection with
root-count pruning. Univariate root-separation bounds control isolation
depth. Subresultant determinant bounds control intermediate coefficient
lengths. These univariate procedures also handle rational roots and
multiple roots after taking the squarefree part.

For a known gap `eta`, compute a rational approximation to the compared
quantity with error at most `eta/4`. An approximate magnitude at most
`eta/2` then certifies exact equality; otherwise the approximate sign is
the exact sign. This is valid because every nonzero quantity has magnitude
at least `eta`. Apply it with (13) for feasibility and with (12) for
objective comparisons.

For example, refining each coordinate to absolute error at most `2^(-T)`
suffices for comparing two objective values when

\[
 T\ge ER+J+d(H+2)
       +\lceil\log_2\max\{1,2sd\}\rceil+3.
 \tag{14}
\]

On the root-bound box, the sum of absolute first derivatives of a monomial
is at most its degree times the appropriate power of the coordinate
bound. Summing the monomials and treating both candidates proves the
error estimate behind (14). Rational midpoint evaluation therefore
provides the required certified approximations. Exact ties are detected
by the gap, rather than by waiting indefinitely for disjoint intervals.

By (9)--(11), all precision lengths in (13)--(14) are bounded by
`2^{poly_d(I)}(b+1)`. The degree, number of polynomials, number of
candidates, and all arithmetic dimensions depend only on the base input.
Univariate algorithms and rational evaluation have absolute polynomial
bit exponents. Combining these bounds proves (1), with all exponential
factors absorbed into a base-computable `B`.

Once a minimizing tuple has been selected, refine its coordinate roots
to the requested accuracy. The same derivative bound gives a rational
enclosure of its objective value. An additional `O(log(n+1))` coordinate
precision gives Euclidean point error at most `2^(-q)`; objective
precision adds `q` to bounds such as (14). This proves (2). Rational
boxes and all defining polynomials have already been stored, so no
optimization or draw selection is repeated during refinement.

All bounds are effective: counts, degree bounds, coefficient bounds,
and precision lengths above are obtained from finite integer arithmetic
on base dimensions and sizes, multiplied by fixed powers of `I+b+q+1`.
A sufficiently large integer `2^((I+1)^C_d)`, with a fixed computable
`C_d`, bounds the remaining base factors. It can therefore be chosen
before any perturbation coefficient is drawn.

## 8. Why sampling precision does not enter the exponential budget

For a rational `M`-point linear-noise grid with base rational half-width,
each sampled coefficient has `poly(I)+O(log M)` bits. Substitution into
(1)--(2) gives

\[
 B\,\operatorname{poly}_d(I+\log M+q),
 \qquad \log B=\operatorname{poly}_d(I).
\]

Thus a failure probability chosen as `O(1/B)` before selecting `M`
can pay for this fallback's expected work and output length. Its remaining
polynomial factor uses the subsequently chosen precision, but does not
change the exponential budget or require an implicit equation for `M`.
The guarantee holds for the same sampled objective on every draw.

This proof uses a symbolic perturbation only to obtain a finite superset
of exact candidates for the original objective. It does not replace the
objective by a fixed perturbed approximation. It also does not bound the
cost of a practical polynomial solver or imply a small exact certificate
on every draw.

## 9. Verification status

The construction, specialization argument, and norm-based separation bound
were independently derived and checked before this draft. The
[completed-text review](../reviews/polynomial-exact-fallback-review.md)
and a separate reader approved the full proof, including the arithmetic
bounds and all-draw completeness. The review's explicit closed-domain,
post-rounding nonemptiness and face-restriction clarifications are included.
A targeted inline Python document check passed local links, whitespace,
paired math delimiters and sequential equation tags. No executable general
optimization solver, project-wide verification, CI inspection, or literature
search was used to establish this construction.
