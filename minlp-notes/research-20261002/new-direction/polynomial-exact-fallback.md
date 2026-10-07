# Exact polynomial-box fallback with a base-only exponential budget

Date: 2026-10-02. Status: complete proof using a verified primary
quantifier-elimination theorem; passed
[independent completed-text review](../reviews/polynomial-exact-fallback-review.md).
No literature-priority claim.

This note supplies the exceptional exact branch needed by the
[smoothed sparse polynomial theorem](smoothed-sparse-polynomial.md).
It selects one global optimizer on every rational draw, including ties
and positive-dimensional optimizer sets. Its exponential factor depends
only on the base input; additional coefficient and evaluation bits enter
polynomially. An
[independent constructive proof](polynomial-exact-fallback-construction.md)
uses symbolic perturbations and univariate algebra instead of multivariate
quantifier elimination.

## 1. Exact output and bit work

Fix a degree bound `d>=1`. Let `F_0` be an explicitly represented rational
polynomial of degree at most `d` on a bounded product `X` of closed
rational continuous intervals and native-integer intervals. Let `I` be
the binary length of these base data. Additional base data, including
a noise half-width or tree decomposition, may be included in `I`.
Round integer bounds inward, reject empty domains, and substitute fixed
coordinates. The zero-variable case is direct evaluation. Otherwise
assume the remaining mixed domain is nonempty.

For arbitrary rational linear coefficients `gamma_i`, put

\[
 F_\gamma(x)=F_0(x)+\sum_i\gamma_i x_i.
 \tag{1}
\]

Let `b` bound the binary length of each added coefficient. There is a
deterministic exact algorithm, a base-computable integer

\[
 B=2^{\operatorname{poly}_d(I)},
 \tag{2}
\]

and a fixed exponent `c_d` with the following guarantees. The algorithm
returns one exact global optimizer and the exact optimal value within

\[
 B(I+b+1)^{c_d}
 \tag{3}
\]

bit operations. Its output supports point and value enclosures of error
at most `2^(-q)` in

\[
 B(I+b+q+1)^{c_d}
 \tag{4}
\]

bit operations, after enlarging the same base budget and exponent if
necessary. Neither `B` nor the exponent depends on the realized
coefficients, `b`, or `q`.

Within the same bound, it can also return a feasible rational point `y`
and a rational global lower bound `a` with
`F_gamma(y)-a<=2^(-q)`. This stronger approximation contract is proved
in Section 6.

Each coordinate and the value are represented by a nonzero integer
univariate polynomial and a rational interval containing exactly the
selected real root. Rational coordinates may instead use ordinary
fractions. No common primitive element, minimal polynomial, unique
optimizer assumption, or finite stationary-set assumption is required.
The representations may have exponential size in `I`, consistent with
(3). Sparsity and interaction width are not used by this fallback.

## 2. One canonical optimizer, including nonunique cases

The domain `X` is compact and `F_gamma` is continuous. Its global
optimizer set `S` is therefore nonempty and compact. Minimize the first
coordinate over `S`, restrict to that minimum, then minimize the second
coordinate, and continue. Each remaining set is compact and nonempty.
After all `n` coordinates have been fixed, exactly one point remains:
the lexicographically first global optimizer `x^lex`.

This argument supplies uniqueness of the selected point even when `S`
has positive dimension. It does not assume that lexicographic order is
continuous or that the original optimizer is unique.

Describe mixed-box membership by the quantifier-free formula

\[
 \mathcal D(z)=
 \bigwedge_{i\in C}\{\ell_i\le z_i\le u_i\}
 \ \wedge\!
 \bigwedge_{j\in Z}\ \bigvee_{k=\ell_j}^{u_j}\{z_j=k\},
 \tag{5}
\]

where integer endpoints have been rounded. If `N_j` is the number of
integer labels, its length is `O(n+sum_j N_j)`. This can be exponential
in the base input, but its logarithmic length is polynomial in `I`.
Every label has polynomial base bit length.

Define the linear-comparison formula

\[
 \operatorname{LexGE}(y,x)=
 (y=x)\ \vee\
 \bigvee_{j=1}^n
 \left[\left(\bigwedge_{i<j}y_i=x_i\right)\wedge y_j>x_j\right].
 \tag{6}
\]

It has `O(n^2)` atomic occurrences. A point is `x^lex` exactly when it
belongs to `X` and every feasible `y` has a larger objective, or the
same objective with `LexGE(y,x)` true. A point with larger-than-optimal
value fails at a better point; a noncanonical optimum fails at `x^lex`.

## 3. Scalar singleton formulas use only two quantified blocks

For coordinate `i`, introduce one free scalar `t` and use

\[
 \exists x\in\mathbb R^n\ \forall y\in\mathbb R^n:\quad
 \mathcal D(x)\wedge x_i=t\wedge
 \left[
 \neg\mathcal D(y)\vee F_\gamma(y)>F_\gamma(x)
 \vee\{F_\gamma(y)=F_\gamma(x)\wedge\operatorname{LexGE}(y,x)\}
 \right].
 \tag{7}
\]

Its satisfying set is `{x_i^lex}`. Replacing `x_i=t` by
`F_gamma(x)=t` gives the singleton consisting of the exact global value.
All `n+1` formulas refer to the same canonical point. Their independently
encoded coordinates cannot come from different optimizers.

Each formula has two blocks, both of size `n`, and one free scalar.
Its number `m` of atomic occurrences is at most
`O(n^2+sum_j N_j)`, its degree is at most `d_0=max(2,d)`, and
`log(m+1)=poly(I)`. Its Boolean evaluation cost is polynomial in its
explicit length, hence at most `2^{poly(I)}`.

Clear rational denominators using positive integer multipliers. Integer
coefficient lengths then satisfy

\[
 L\le\operatorname{poly}_d(I+b+1).
 \tag{8}
\]

Only polynomially many rational coefficients occur before integer-label
disjunctions are expanded. The expanded labels are integers of polynomial
base bit length. Thus denominator clearing does not put the label count
into an exponent of `b`.

## 4. The primary theorem separates coefficient height from dimension

Renegar's Theorem 1.1 gives quantifier elimination for `omega` blocks,
`ell>=1` free variables, block sizes `n_j`, `m` atoms and degree at most
`d_0`. Its sequential bit bound is

\[
 L\log L\log\log L\,
 (m d_0)^{2^{O(\omega)}\ell\prod_j n_j},
 \tag{9}
\]

plus `(m d_0)^{O(ell+sum_j n_j)}` evaluations of the input Boolean
formula. Logarithms of small lengths may be replaced by positive constants.
The numbers of output disjuncts and atoms per disjunct, and their
polynomial degrees, are bounded by the displayed dimension-dependent
power. Output integer coefficient lengths are at most

\[
 (L+1)(m d_0)^{2^{O(\omega)}\ell\prod_j n_j}.
 \tag{10}
\]

These are the bit and height assertions on printed page 330 of the
[primary paper](../../literature/papers/renegar1992-on-the-computational-complexity-and/original.pdf).
The scanned theorem was inspected directly; the local text extraction
omits parts of its displayed exponents.

For (7), `omega=2`, `ell=1`, and both block sizes are `n`. Therefore
the dimension-dependent factors, Boolean evaluation work, and `n+1`
repetitions are all at most `2^{poly_d(I)}`. The coefficient-height
factor has an absolute polynomial exponent, and the output coefficient
length is linear in `L` times the base factor. A general doubly
exponential cylindrical-decomposition bound would not suffice here.

Fix an effective implementation. Its bounds are computable from the
base atom count, degree, dimensions and Boolean formula length. A
sufficiently large `2^((I+1)^C_d)`, with fixed computable `C_d`, bounds
them. Elimination is run on the sampled coefficients; only its exponential
budget is selected beforehand.

## 5. Recover and refine each singleton by univariate algorithms

Let `Phi(t)` be one output formula. Replace constant and identically zero
polynomial atoms by their truth values. Form the product of the remaining
nonconstant integer polynomials and take its squarefree part `P(t)`.

The singleton must be a real root of `P`. Otherwise every polynomial
has locally constant sign there, and `Phi` would hold on a neighborhood.
In particular, the product is nonempty. Isolate all real roots of `P`;
determine the signs of the atom polynomials at each root and evaluate
`Phi`. Exactly one root satisfies it. Store `P` and an interval isolating
that root.

Standard subresultant Sturm methods perform real-root isolation, sign
determination at an algebraic root, and subsequent refinement in bit work
polynomial in degree, coefficient length, formula length and requested
precision, with an absolute exponent. These are univariate operations.
The squarefree step handles repeated input roots and requires no
stationary-point regularity for the original problem.

There are at most `2^{poly_d(I)}` output polynomial occurrences, with
degrees bounded by the same base factor and coefficient lengths at most
`(L+1)2^{poly_d(I)}`. Product construction, squarefree reduction, root
isolation and sign testing consequently cost

\[
 2^{\operatorname{poly}_d(I)}(I+b+1)^{c_d}
\]

bit operations, including output length. This proves (3). No
coefficient-height term is raised to an exponent depending on `n`.

Apply the procedure separately to the coordinates and value. Subsequent
refinement adds `q` to the precision work. Coordinate intervals of radius
at most `2^(-q)/(n+1)` give Euclidean point radius at most `2^(-q)`;
refine the separate value root to obtain its enclosure directly. The
extra `O(log(n+1))` coordinate bits and the base degree/height factors
fit in the same enlarged `B`, proving (4). No additional optimization
or quantifier elimination is needed during refinement.

## 6. Feasible rational approximations with a certified objective gap

Compute a rational bound

\[
 G\ge\max\{1,\sup_{x\in\operatorname{hull}(X)}
                         \|\nabla F_\gamma(x)\|_1\}.
\]

Termwise monomial bounds on the original bounded hull suffice. For fixed
degree their encoding length, including `log G`, is polynomial in
`I+b`. Given `delta=2^(-q)`, refine each continuous coordinate to error
at most `delta/(2G)` and clip its rational midpoint to the original
closed interval. Clipping cannot increase its distance to the exact
coordinate. Refine each integer coordinate until its isolating interval
contains exactly one integer and use that label exactly.

The resulting rational point `y` is feasible and shares the canonical
optimizer's integer labels. The segment between their continuous parts
stays feasible. The gradient bound gives
`0<=F_gamma(y)-F_gamma(x^lex)<=delta/2`. Independently refine the exact
value representation to a rational enclosure of width at most `delta/2`
and take its lower endpoint `a`. It is a global lower bound, and

\[
 0\le F_\gamma(y)-a\le\delta.
\]

These refinements require `q+poly_d(I+b)` bits. Exact rational evaluation
of `F_gamma(y)` has the same polynomial precision dependence. Therefore
the work remains (4), with the same enlarged base-only budget. No
algebraic coordinates are expanded to produce this rational approximation.

## 7. Sampling budget and verification

For an endpoint-inclusive rational `M`-point noise grid with a base
rational half-width, `b=poly(I)+O(log M)`. Equations (3)--(4) become

\[
 B\,\operatorname{poly}_d(I+\log M+q),
 \qquad \log B=\operatorname{poly}_d(I).
 \tag{11}
\]

A failure probability chosen as `O(1/B)` can pay for expected fallback
work and output length. The grid precision appears only in the remaining
polynomial factor, so the exponential budget need not be recomputed from
that precision.

The lexicographic selection and scalar projections were independently
derived by multiple reviewers. The primary theorem's bit, output-height,
block and free-variable dependencies were checked on a local rendering
of printed page 330. The
[constructive alternative](polynomial-exact-fallback-construction.md)
supplies a separate proof mechanism for every draw. The
[completed-text review](../reviews/polynomial-exact-fallback-review.md)
checked both proofs, the separated bit bounds, and the feasible rational
gap contract. Two additional readers independently approved the shorter
proof and its final approximation contract; one separately rendered the
primary theorem. A targeted inline Python check passed local links,
whitespace, paired math delimiters and sequential equation tags in both
proof notes. No executable general optimization solver, external search,
project-wide verification or CI inspection was used for this note.
