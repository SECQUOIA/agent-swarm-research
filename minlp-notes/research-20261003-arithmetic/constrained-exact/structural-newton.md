# Exact comparison from constrained Newton steps

Date: 2026-10-03. Status: proof complete and passed
[independent actual-file review](review-structural-newton.md).
Publication priority is not established. This note supplies a structural
extension of the [unconstrained exact-comparison theorem](../../research-20260927/strong-convex-quartic-posslp-upper.md).

Exact comparison at the minimizer of a strongly convex rational quartic
over a rational box is in `P^PosSLP` when Hessian interactions lie in a
forest or every Hessian has nonpositive off-diagonal entries. The
dimension and number of active
bounds are unrestricted. Zero multipliers and arbitrarily small nonzero
slacks are permitted. The result comes from a more general transfer
principle: an exact quadratic-programming subroutine with a polynomial
number of arithmetic operations makes constrained Newton refinement a
polynomial-size arithmetic computation.

The output is an exact sign or active-set decision. The high-precision
Newton iterates have rational arithmetic circuits. The generally
irrational optimizer itself does **not** have a rational arithmetic
circuit.

## 1. Input and structural theorem

Let `f` be an explicit rational polynomial of degree at most four, with
a supplied positive rational `mu` satisfying

```
H_f(x) >= mu I                    for every x in R^n.       (1)
```

Let `P` be a rational box, initially with finite endpoints. Empty
intervals are detected directly. Coordinates fixed by equal endpoints
are substituted out. Let `p` be the unique minimizer of `f` over the
remaining nonempty box. The input also specifies an explicit rational
polynomial `h` of degree at most four. All these encodings contribute
to the input length `I`.

Assume either of the following promises on every `x in P`:

1. A supplied forest on the variable indices contains every off-diagonal
   Hessian interaction: `H_f(x)_ij=0` whenever `ij` is not a forest edge.
   A tridiagonal Hessian is a special case.
2. Every off-diagonal entry of `H_f(x)` is nonpositive.

**Theorem.** Each comparison `h(p) bowtie 0`, for
`bowtie in {<,<=,=,!=,>=,>}`, is decidable in deterministic polynomial
time with a PosSLP oracle. The full set of active box bounds can be
computed in the same oracle class. The statement also holds for rational
boxes with some infinite endpoints, by the reduction in Section 7.

The structural and curvature promises are not recognition algorithms.
The supplied forest and absent Hessian interactions can be checked by
graph traversal and polynomial coefficient identities;
the nonpositive-sign promise and global strong-convexity promise require
their own verification if the chosen input language includes verification.
Supplying valid certificates does not change the algorithm below, but
their verification cost must be charged. The theorem does not assert
PosSLP-hardness for either structural subclass.

## 2. General transfer principle

For this section, let `P={x:Ax<=b}` be any nonempty bounded rational
polyhedron with a supplied rational bounding box. Suppose an exact
algorithm solves each quadratic program

```
minimize  (1/2) z' H_f(x) z + [grad f(x)-H_f(x)x]'z
subject to z in P                                         (2)
```

for rational `x in P` in a number of arithmetic operations and sign
comparisons polynomial in the original encoding `I`. Its allowed
operations are addition, subtraction, multiplication, division by a
nonzero quantity, and comparisons. The count must hold independently
of the expanded bit lengths of `x` and the resulting Hessian and linear
cost. A fixed polynomial operation bound in the dimensions is sufficient.
It is also sufficient that the operation count be polynomial in the
dimensions and the logarithms of supplied parameters, when those
logarithms are polynomial in `I`.

Under this subroutine assumption, all the exact comparisons in Section 1
are in `P^PosSLP`. This is a conditional transfer theorem, not a claim
that arbitrary convex QP has the needed arithmetic bound.

All coefficients of the derivatives of `f` on the supplied box have
computable rational magnitude bounds with polynomial bit length. Choose
a rational `L_H>=0` bounding the Lipschitz constant of the Hessian in
Euclidean operator norm on the box, a rational `M_h>=1` bounding
`||grad h||_2` there, and

```
K=max(1,L_H/(2 mu)).                                      (3)
```

Such bounds follow directly by summing absolute monomial coefficients
of the relevant derivatives, replacing each coordinate magnitude by the
largest endpoint magnitude or one, and bounding operator norms by entry
sums. No spectral root calculation is necessary.

Ordinary polynomial-time convex optimization produces a rational feasible
`x_0` with objective error at most `min(1,mu/(8K^2))`. In the present global
convexity setting, the convex Corollary 1.2 of
[Slot--Steurer--Wiedmer](https://arxiv.org/html/2511.03440v1)
supplies this point; the required precision has only polynomially many
bits. Strong convexity and constrained first-order optimality give

```
f(x)-f(p) >= (mu/2)||x-p||_2^2,   x in P,
||x_0-p||_2 <= 1/(2K).                                   (4)
```

This preliminary computation produces ordinary binary rational output
and needs no PosSLP oracle.

## 3. Quadratic convergence does not require identifying the optimal face

This is an established proximal Newton estimate: see Lee, Sun and
Saunders, [*Proximal Newton-Type Methods for Minimizing Composite
Functions*](https://stanford.edu/group/SOL/multiscale/papers/14siopt-proxNewton.pdf),
Theorem 3.4, printed page 1431, with the nonsmooth term equal to the
indicator function of `P`. The following specialized proof records the
constant and hypotheses used in the arithmetic composition.

Given `x in P`, let `y` solve (2) exactly. Strong convexity makes that
solution unique. Write `g=grad f(x)` and `H=H_f(x)`. The two constrained
optimality inequalities, tested against `p` and `y`, are

```
[g+H(y-x)]'(p-y) >= 0,
grad f(p)'(y-p) >= 0.
```

Subtracting gives

```
(y-p)'H(y-p)
  <= [grad f(p)-g-H(p-x)]'(y-p).
```

Taylor's integral formula bounds the norm of the bracket by
`(L_H/2)||x-p||_2^2`. If `y!=p`, division by `mu||y-p||_2`
therefore yields

```
||y-p||_2 <= (L_H/(2mu))||x-p||_2^2
           <= K||x-p||_2^2.                              (5)
```

The same conclusion is immediate for `y=p`. Define `x_(t+1)` to be the
exact solution of (2) at `x_t`. Every iterate is feasible. With
`e_t=||x_t-p||_2`, equations (4)--(5) imply

```
K e_t <= 2^(-2^t),   e_t <= 2^(-2^t).                    (6)
```

The derivative bound is valid along every segment used in the proof
because the box contains `P`, which is convex. There is no requirement
that the QP and the nonlinear problem have the same active set. In
particular, a tiny multiplier or a zero multiplier does not shrink the
quadratic-convergence neighborhood in this argument.

## 4. Circuit implementation and exact signs

Represent a rational circuit value as a pair of integer circuits for
its numerator and denominator. Arithmetic operations append a constant
number of gates to these pairs. Keep shared predecessor nodes rather
than expanding expressions. The subroutine's division promises ensure
that denominators are nonzero. A rational sign is the sign of the
product of its numerator and denominator, so a PosSLP oracle implements
every comparison; equality uses the two strict signs. Polynomially many
subroutine operations across polynomially many Newton steps give a
polynomial-size directed acyclic circuit, despite potentially enormous
expanded numerators and denominators.

Here is a uniform separation bound involving only the original rational
input. Put `alpha=h(p)` and consider the one-block existential formula

```
exists x,lambda:
  Ax<=b, lambda>=0,
  grad f(x)+A'lambda=0,
  lambda_i(b_i-a_i'x)=0 for every i,
  z=h(x).                                                (7)
```

Polyhedral first-order optimality, including lower-dimensional
polyhedra, makes its real `z`-projection exactly `{alpha}`. The proof
does not assume a strictly complementary multiplier or a bounded
multiplier set. After denominator clearing, the formula has polynomially
many variables and polynomials, fixed degree, and polynomial coefficient
bit length.

The one-block quantifier-elimination bound in Theorem 2.16 of
[Basu's survey](https://www.math.purdue.edu/~sbasu/raag_survey2011.pdf)
therefore gives a fixed effective polynomial `a(I)` such that some
nonzero integer polynomial vanishing at `alpha` has degree and
coefficient bit length at most `2^(a(I))`. This uses quantifier
elimination only as an existence and size bound, not as the algorithm.
A quantifier-free description of a singleton must contain a nonzero
polynomial vanishing there: otherwise all its signs would be locally
constant. Removing any power of `z` from that polynomial and comparing
its nonzero integer constant term with its other terms proves

```
alpha!=0  implies  |alpha|>=delta,
delta=2^(-2^(a(I)+1)).                                   (8)
```

Enlarge `a` to dominate `I`, a polynomial bound on `log_2 M_h`, and a
fixed constant. With `t=a(I)+4`, (6) gives

```
|h(x_t)-alpha| <= M_h e_t < delta/4.                     (9)
```

Repeated squaring constructs the rational circuit for `delta` in
`a(I)+1` squarings starting from `1/2`. Compare `h(x_t)` with `delta/2`
and `-delta/2`. The respective outcomes above, below, or between these
thresholds identify positive, negative, or zero `alpha` exactly.

Applying the same argument to each explicit slack observable recovers
the entire active mask with polynomially many queries. The method is a
polynomial-time **Turing** reduction to PosSLP: QP pivots depend on oracle
answers. No single-instance many-one reduction is established here.

An exact implicit optimizer description can then consist of the active
equalities and the stationary equations on their affine intersection.
Global strong convexity makes the latter have a unique real solution.
This is different from printing expanded algebraic coordinates.

## 5. Exact box QPs with the required arithmetic bound

For a positive definite matrix `H`, call `v>0` an admissible vector if

```
H_SS^(-1) v_S >= 0          for every nonempty S.         (10)
```

[Pang--Han](https://optimization-online.org/wp-content/uploads/2021/12/arxiv.pdf),
Algorithm I and Proposition 2.1, solve a box QP with such a vector in
at most `2n` pivots. Their displayed steps use linear-system solutions,
arithmetic, sign tests, and ratio comparisons. They allow degeneracy.
Solving each system afresh suffices for a polynomial operation count;
the sharper update bound is unnecessary here.

For a positive definite symmetric matrix with nonpositive off-diagonal
entries, every principal inverse is entrywise nonnegative. One proof:
write `H_SS=cI-N`, where `N>=0` and choose `c>=lambda_max(H_SS)`;
positive definiteness gives spectral radius `rho(N)<c`, so the inverse
is the entrywise nonnegative convergent Neumann series. This is an
existence proof, not a step of the algorithm. Thus `v=1` satisfies (10).
It is immediately available for the second class in Section 1.

For a positive definite `H` whose off-diagonal support is a forest, let
`B` have the same diagonal
and off-diagonal entries `-|H_ij|`. A diagonal sign matrix `S` can be
chosen successively from a root of each tree component so that `B=SHS`.
Consequently `B` is positive definite with nonpositive off-diagonal
entries. Compute

```
d=B^(-1)1,       v=(H+B)d/2.                             (11)
```

The inverse argument above gives `d>0`. Also
`v=1+(H-B)d/2>=1`. The comparison-matrix result preceding Section 4 of
Pang--Han gives (10) for this `v`. All computations in (11) are rational
linear algebra; absolute values require only sign queries. There are no
square roots. Principal systems in the pivot procedure are positive
definite and hence nonsingular. Ratios are formed only on the algorithm's
explicit positive-denominator branches.

The same argument proves a broader sufficient condition: the comparison
matrix `B(x)`, with diagonal `H_f(x)_ii` and off-diagonal
`-|H_f(x)_ij|`, is positive definite for every `x in P`. In that case
(11) directly supplies the required vector, even when the interaction
graph contains cycles and Hessian off-diagonal entries have mixed signs.
This is an additional promise, not a test performed over the entire box.
The two concrete classes above imply it without further assumptions.

Translate an arbitrary finite box by its lower endpoint to the source
form `0<=z<=u`. Its Hessian is unchanged and its linear cost is updated
by rational operations. Thus the operation bound applies even when `H`
and the cost are represented by the Newton circuits of Section 4.

## 6. Scope illustrated by explicit quartics

For any graph `G`, rational `mu>0`, rational `w_ij>=0`, and rational
linear cost `c`,

```
f(x)=(mu/2)sum_i x_i^2
     +sum_{ij in E(G)} w_ij(x_i-x_j)^4 + c'x             (12)
```

has Hessian equal to `mu I` plus a graph Laplacian with nonnegative
edge weights `12w_ij(x_i-x_j)^2`. It satisfies the second structural
promise on every box. The graph can be dense. The constraint-normal
rank of a full-dimensional box is `n`; this result therefore does not
rely on the previous low constraint-rank parameter.

For a path graph, replacing any difference by `x_i+x_(i+1)` still gives
a globally strongly convex tridiagonal Hessian. Its off-diagonal signs
need not satisfy the second promise, but the first promise applies.

The new component is the composition with exact arithmetic complexity.
The source QP algorithm is established prior work, and (5) is the
proximal Newton estimate of Lee--Sun--Saunders. No claim of novelty is made for
either ingredient. The [dedicated source comparison](../literature/constrained-prior.md)
distinguishes these ingredients from the exact-comparison consequence;
publication priority remains unestablished.

## 7. Infinite endpoints and further fixed degrees

For a nonempty rational box with infinite endpoints, choose a rational
feasible `x_bar` by clipping zero to its finite bounds. It has polynomial
bit length. Strong convexity gives coercivity, so the constrained
minimizer exists. Comparing its value with `f(x_bar)` gives

```
||p-x_bar||_2 <= 2||grad f(x_bar)||_2/mu
                <= 2||grad f(x_bar)||_1/mu.
```

Intersect the box with
`|x_i-x_bar_i|<=R`, where
`R=1+2||grad f(x_bar)||_1/mu`. This is a polynomial-bit finite box
containing `p` strictly inside its added bounds. The optimizer is
unchanged, and the preceding theorem applies. Original active bounds
are compared directly; added bounds introduce no active labels.

Nothing in the transfer proof relies specifically on degree four beyond
fixed-degree derivative encoding and the separation exponent. For every
fixed degree bound `D`, the same result holds for explicit globally
strongly convex polynomials of degree at most `D`, with explicit
fixed-degree observables and the same Hessian structural promises.
The constants and polynomial bounds may depend on `D`. This statement
does not cover variable-degree sparse or circuit representations without
additional encoding analysis.

## 8. Verification and remaining boundary

The independent reviewer reconstructed the proof and checked the source
algorithm. One overly loose sentence about the arithmetic-operation bound
was corrected to require polynomial dependence on logarithms of numerical
parameters. The reviewer then passed the revised actual file, including
the forest and comparison-matrix extensions, the infinite-endpoint
reduction, and the fixed-degree statement.

The reviewer ran:

```text
python3 research-20261003-arithmetic/constrained-exact/check_structural_newton_review.py
```

It passed 90 exact bounded-QP KKT checks, 714 principal-submatrix
admissible-vector checks, and four exact quartic Newton steps satisfying
the squared error bound. The quartic optimizer has an active lower bound
with zero multiplier while every tested iterate is interior, illustrating
why the proof does not require early face identification. All tested QP
pivot counts were at most twice the dimension. These finite checks
support the source interface and the identities; they do not implement
PosSLP or prove asymptotic complexity. The author read the review without
duplicating its mathematical diagnostic. A separate focused author check
passed local links and whitespace in this note and its source record.
No project-wide checks or CI inspection were performed.

The transfer theorem isolates the unresolved general step: arbitrary
polyhedra and arbitrary strongly convex quartics need exact Taylor-QP
solves with a polynomial operation count for circuit Hessians. The
Granot--Skorin-Kapov result removes right-hand-side and linear-cost bit
dependence while retaining dependence on the Hessian encoding. It does
not by itself provide this missing circuit-Hessian interface.
