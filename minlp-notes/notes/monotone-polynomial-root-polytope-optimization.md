# Exact optimization of a monotone polynomial root over a polytope

Date: 2026-09-05. Status: reviewed supporting arithmetic lemma. Two
independent full proof audits passed; a focused source assessment is linked
below. This abstracts the vertex-root recovery argument in the
[correlated-cycle design note](potential-flow-cycle-polytope-resistance-design.md).
All constituent LP and root-isolation tools are classical.

## 1. Statement

Let P={theta in R^t:A theta<=b} be a nonempty bounded rational polytope.
The dimension t is unrestricted. Let

```
H(q,theta)=h_0(q)+sum_(j=1)^t theta_j h_j(q)
```

have densely encoded rational univariate polynomial coefficients h_j of
degree at most D. A rational bracket a<b is supplied. Assume that, for
every theta in P, H(.,theta) is strictly increasing on [a,b] and

```
H(a,theta)<=0<=H(b,theta).
```

Thus H has a unique root q(theta) in the bracket. Under these promises,
both extrema of q(theta) over P can be computed exactly in polynomial
rational bit time. The algorithm returns a rational optimizing vertex of
P and a real-algebraic encoding of its root, of degree at most D and
polynomial coefficient bit length. D need not be fixed under dense encoding.
The algorithm neither enumerates the vertices nor assumes a derivative
lower bound. It does not validate the uniform strict-monotonicity promise.

A nonempty bracket rules out D=0. The case t=0 is ordinary univariate root
isolation; below assume t>=1. Lower-dimensional polytopes are permitted.

## 2. Threshold tests and attainment at a vertex

For rational z in [a,b], monotonicity gives

```
max_(theta in P) q(theta)>=z  iff min_(theta in P) H(z,theta)<=0,
min_(theta in P) q(theta)<=z  iff max_(theta in P) H(z,theta)>=0.       (1)
```

These are exact rational LPs. Moreover, all extremal roots occur at
vertices. Indeed, express any theta as a convex combination of vertices.
At q(theta), the same combination of their H-values is zero, so some
vertex has H<=0 and some has H>=0 there. Their roots bracket q(theta).
There are finitely many vertices, so their smallest and largest roots
are the global extrema. No continuity-of-argmin or compactness-of-lifts
argument is required.

## 3. Uniform coefficient bit bounds

Clear the denominators in every row of A theta<=b. Let C>=1 bound the
absolute values of all resulting integer row entries, including the RHS,
and put Delta=t! C^t. Every vertex has t independent active rows, including
when P is lower dimensional. Cramer's rule represents all its coordinates
with one nonzero integer denominator d and integer numerators n_j satisfying

```
|d|<=Delta, |n_j|<=Delta.
```

Clear all h_j coefficient denominators using one positive integer R, and
let P_0>=1 bound the resulting integer coefficient magnitudes. Substituting
a vertex and multiplying H by R d yields a nonzero integer polynomial of
degree at most D and height at most

```
H_0=(t+1) Delta P_0.
```

This polynomial is nonzero by strict monotonicity. The logarithms of
Delta, R, P_0, and H_0 are polynomially bounded by the input length.
The bounds are explicitly computable with polynomial-bit arithmetic.

## 4. A conservative separation bound for all possible vertex roots

Take any two of the integer polynomials from Section 3, allowing them to
be identical, and form their product Q. Its degree is at most 2D and
height at most (D+1)H_0^2. Let S be the primitive squarefree part of Q.
It is an integer factor after removing content. The classical
Landau--Mignotte factor bound gives

```
height(S) <= 2^(2D) sqrt(2D+1) (D+1)H_0^2
          <= H_s := 2^(2D)(2D+1)(D+1)H_0^2.
```

This use is deliberately loose. If S has degree n>=2, all its roots have
absolute value at most 1+H_s by the Cauchy bound. Its discriminant is a
nonzero integer, hence has absolute value at least one. For any distinct
two roots with distance delta, the discriminant product formula gives

```
1 <= H_s^(2n-2) delta^2 [2(1+H_s)]^(n(n-1)-2).
```

Since n<=2D, the smaller rational number

```
sigma=[2(1+H_s)]^(-4D^2)                                      (2)
```

is a valid lower bound on the distance between any two distinct roots
appearing in any pair of vertex polynomials. If S has degree one there
are no distinct roots to separate. Common factors and repeated roots
of Q cause no problem because S is squarefree. The encoding length of
sigma is polynomial in D and the input bit length.

The factor bound is established mathematics: see Mignotte, *An Inequality
About Factors of Polynomials*, Mathematics of Computation 28 (1974),
1153--1157, [primary publication](https://www.jstor.org/stable/2005373).
Its precise inequality is also stated as Theorem 1.2 in the primary
research paper [A new bound on cofactors of sparse polynomials](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/new-bound-on-cofactors-of-sparse-polynomials/2CADDB77D2E5CBFB7B803CCCAC49D2FD).
The remainder of this separation argument follows directly from the
Cauchy and discriminant formulas; no sharp bound is needed.

## 5. Recover one exact maximizing vertex from LP bisection

Maintain a rational bracket [l,u] containing q_max, initially [a,b].
At its midpoint z, use the first LP test in (1): if the test is true,
set l=z; otherwise set u=z. Stop when u-l<sigma. Only polynomially many
bisections are needed because log(1/sigma) and the input bracket length
have polynomial encoding length. Every LP has polynomial rational data.
Equality cases are included in the true branch.

Now minimize H(l,theta) over P and return a VERTEX optimizer theta_v.
Such a vertex can be extracted in polynomial bit time: first impose the
optimal objective equality, then successively minimize coordinates on
the remaining face, imposing each optimal value. After t steps the face
is a singleton and therefore a vertex of the original polytope.
Each successive optimal set is a face of the original P. Its coordinate
minimum is attained at an original vertex, so every newly imposed value
has the original Cramer bit bound from Section 3. Thus all intermediate
LP inputs and optima have a common polynomial encoding bound; the proof
does not iterate an unspecified polynomial size bound t times.

Since q_max>=l, the attained objective is at most zero. Hence

```
l <= q(theta_v) <= q_max <= u.
```

Both q(theta_v) and q_max are vertex roots. By (2) and u-l<sigma they
must be identical. Isolate the unique root of H(.,theta_v) in [a,b]
using a polynomial-bit univariate root-isolation algorithm and return
it with theta_v. Endpoints a,b are included. For minimization, use the
second test in (1) and take a maximizing LP vertex at the final upper
bracket u; its root lies between q_min and u, giving the same argument.

## 6. Fixed-breakpoint piecewise-polynomial extension

The same theorem holds when H is continuous and piecewise polynomial in q,
with an explicitly supplied rational breakpoint partition independent of
theta. On each piece, H is affine in theta and has densely encoded rational
polynomial coefficients. Strict increase and the endpoint bracket remain
uniform promises over P. Remove empty pieces and duplicate breakpoints.

The threshold oracle selects the polynomial piece containing its rational
test point; continuity makes a breakpoint unambiguous. Vertex attainment
is unchanged because H remains affine in theta at every fixed q. Use one
common denominator and coefficient bound over all pieces in Section 3.
Every positive-width piece is nonconstant at every profile by strict
increase. A vertex root belongs to a nonzero polynomial piece; continuity
also gives this property at a breakpoint through an adjacent closed piece.
Thus the separation proof applies to all vertex-piece polynomials with
the same degree and height bounds. No vertex or piece combinations need
be enumerated.

After recovering the optimizing vertex, evaluate H at the ordered rational
breakpoints. Equality returns an exact rational root. Otherwise binary
search identifies the unique adjacent pair with negative and positive
values. Its polynomial, squarefree part if required, and this interval
encode the unique root exactly. All work remains polynomial in the total
dense piecewise input. Both independent reviewers checked this extension, including breakpoint
roots, common coefficient bounds, and exact recovery from piece signs.

## 7. Scope, applications, and source assessment

This statement applies to a scalar strictly monotone balance equation
whose coefficients depend affinely on arbitrary correlated polyhedral
data. A passive single cycle with fixed nominations and polynomial laws
can have this form. Integer power laws with shifted-flow sign changes
fit the fixed-breakpoint extension when their numerical degree is included
in the dense input length.

This does not optimize arbitrary roots of a polynomial family, complex
root locations, multiple branches, or nonmonotone balances. The crucial
LP threshold equivalence and vertex attainment use a unique monotone
root. Sparse binary exponents are excluded: the separation precision
and root-isolation time can depend polynomially on the numerical degree.

The [focused source assessment](monotone-polynomial-root-polytope-novelty.md)
identifies quasilinear optimization, Megiddo's exact ratio optimization,
and real interval-polynomial root bounds as direct antecedents. No exact
matching variable-degree H-polytope statement was located, but the proper
positioning is a supporting arithmetic refinement, not a new general
optimization paradigm. The explicit recovery of a rational vertex below
a uniform algebraic separation bound is the useful feature for subsequent
passive-flow algorithms.

Independent proof reviews:
[first full audit](review-monotone-polynomial-root-polytope-optimization.md),
[second full audit](review-monotone-polynomial-root-polytope-optimization-second.md).
Both verified the classical factor bound directly in the cited primary
research paper. They corrected the distinction between numerical height
and its encoding length and clarified the original-face bit bound during
lexicographic vertex extraction.
