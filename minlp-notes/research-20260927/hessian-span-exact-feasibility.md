# From a positive value gap to exact convex-quadratic feasibility

Date: 2026-09-27. Status: proof, primary-source check, and independent
adversarial review for the algorithmic consequence of
`hessian-span-reduction.md`. It is conditional on the value-height theorem
proved and reviewed in that note. The ellipsoid method is established prior
work; the proposed addition is the Hessian-span-dependent value gap that
makes it decide exact feasibility without a Slater promise.

## 1. Precise conclusion

Consider finitely many rational convex quadratic inequalities and rational
affine equalities on an explicit finite rational box in `R^n`. Let `N`
be the total binary input length, and let `h` be the dimension of the
linear span of the quadratic Hessians. Exact feasibility can be decided in

```
N^{O(h+1)} bit operations.
```

The hidden constant is absolute. This is polynomial time for every fixed
`h`, and is an XP bound in parameterized-complexity terminology. There
is no Slater or nonempty-interior assumption on the original feasible
set. The algorithm decides existence; its returned point need only
satisfy a small relaxation and is not asserted to be exactly feasible
for the original inequalities.

There is now a second proof using ordinary rational linear programming:
set the number of integer variables to zero in the subsequently proved
[exact integer-projection reduction](mixed-integer-span-frontier.md).
The resulting compact rational LP is feasible exactly when the original
system is feasible. That reduction depends on the value-height theorem,
not on the ellipsoid argument below, so there is no circular dependency.
The present note retains the independently checked ellipsoid proof as an
alternative.

## 2. Normalization and the positive gap

An inconsistent coordinate box is immediately infeasible. Substitute any
coordinates whose lower and upper bounds coincide, and map each remaining
interval affinely onto `[-1,1]`. Both transformations preserve rational
polynomial coefficient bit lengths. Restriction cannot increase the
Hessian-span dimension, and an invertible affine coordinate change
preserves it. If no variables remain, evaluate the input constraints
exactly and stop. Write `d>=1` for the remaining dimension.

Replace each affine equality by its two affine inequalities. Let the
resulting functions on `[-1,1]^d` be `q_1,...,q_s`, all convex quadratics
or affine, and define

```
phi(x)=max(0,q_1(x),...,q_s(x)),
theta=min_{x in [-1,1]^d} phi(x).
```

Then `theta>=0`, and the original problem is feasible exactly when
`theta=0`. A rational bound `U_0>=1` of polynomial bit length bounds
`phi` on the cube. The epigraph formulation

```
min t
subject to x in [-1,1]^d,
           0<=t<=U_0,
           q_i(x)-t<=0 for all i
```

is a nonempty boxed convex QCQP. Its native Hessian span is still at
most `h`; the new variable occurs only affinely. The value theorem gives
a universal integer constant `c` such that, after accounting for the
polynomial-size normalization, one can choose

```
delta=2^{-N^{c(h+1)}} in (0,1]
```

with the following dichotomy:

```
theta=0, or theta>=delta.                                  (1)
```

As elsewhere in these notes, universal constants can be chosen large
enough from the effective elimination theorem. Their existence gives an
algorithmic complexity statement, not a numerically calibrated rule.

## 3. A relaxed set is either empty or contains a known-size ball

Consider the closed convex set

```
K_delta={x in [-1,1]^d:phi(x)<=delta/2}.
```

If the original problem is infeasible, (1) makes `K_delta` empty.
Suppose instead that a point `x*` of the original feasible set exists.
Choose rational bounds

```
U>=max(1,phi(0)),
G>=max(1, max_i sup_{[-1,1]^d} ||gradient q_i||_2).
```

Both have polynomial bit length; summing absolute coefficients supplies
such bounds. The maximum function `phi` is `G`-Lipschitz on the cube.
Set

```
alpha=delta/(8U),
y=(1-alpha)x*,
r=min(alpha/2,delta/(8G)).
```

Every coordinate of `y` has absolute value at most `1-alpha`, so the
Euclidean ball of radius `r` about `y` is inside the cube. Convexity gives

```
phi(y)<=alpha phi(0)<=delta/8.
```

For every point `z` of that ball, the Lipschitz bound gives
`phi(z)<=delta/8+G r<=delta/4`. Thus the whole ball lies in `K_delta`.
Its center need not be known. The bound `log(1/r)=N^{O(h+1)}` is
available from the input.

We have reduced exact feasibility to a promised convex-feasibility
problem: the set is either empty or contains a Euclidean ball of radius
the supplied rational `r`, while it is contained in the known outer
ball of radius `d` about the origin.

## 4. Exact rational separation and finite-precision ellipsoids

There is a polynomial-bit exact separation oracle for `K_delta`.
For a rational query outside the cube, use a violated coordinate bound.
Inside the cube, test each inequality `q_i(x)<=delta/2` exactly. If all
hold, accept the query as an actual member. Otherwise take a violated
row. Convexity implies that every `z in K_delta` satisfies

```
gradient q_i(x)^T(z-x) <= delta/2-q_i(x) < 0.
```

The gradient is rational, with bit length polynomial in the input and
query lengths, and so supplies the separator after normalization by its
infinity norm. If this gradient is zero, convexity says the violated
value is the row's global minimum; declare `K_delta` empty immediately.

The specific primary source used is Grötschel, Lovász and Schrijver,
*Geometric Algorithms and Combinatorial Optimization* (1988),
[author-hosted book](https://www.zib.de/groetschel/pubnew/paper/groetschellovaszschrijver1988.pdf),
Theorem 3.2.1, printed pp. 87–88. Its finite-precision central-cut method
returns an approximate member or an enclosing ellipsoid of arbitrarily
small supplied volume, in oracle-polynomial bit time. Definition 2.1.16,
p. 53, explicitly allows an inner-radius guarantee without knowing the
ball's center.

Use that algorithm with

```
epsilon_vol=min(1/2, (r/d)^d/2).
```

The proof's acceptance step calls the oracle at the ellipsoid center.
Our oracle accepts only actual members, so this use of the algorithm
returns an actual point of `K_delta` if it takes the membership branch.
Otherwise it returns an enclosing ellipsoid of volume less than
`epsilon_vol`. A Euclidean ball of radius `r` contains the cube of
side `2r/sqrt(d)`, and hence has volume greater than `(r/d)^d`.
The enclosing-ellipsoid branch is therefore impossible under the
nonempty side of the promise. Under the empty side, the oracle cannot
accept a member. This distinguishes the two cases exactly.

For `d=1`, interval bisection gives the same conclusion directly: each
separator chooses a half-interval, and an interval of length below `2r`
cannot still contain a promised radius-`r` ball. This also avoids any
dimension convention in the ellipsoid theorem.

The binary length of `epsilon_vol` is
`O(d(log d+log(1/r)))=N^{O(h+1)}`. The cited theorem controls all
intermediate bit lengths, not just the number of real-arithmetic steps.
The exact oracle has polynomial bit complexity at those query lengths.
This proves the stated bit-time bound.

## 5. Consequences and limits

A feasible original set can be lower-dimensional and need not contain any
rational point; `hessian-span-reduction.md` gives an explicit singleton
example. That does not affect the
decision proof: its membership query concerns `K_delta`, whose interior
is certified by the interpolation argument. A returned relaxed point
plus (1) certifies that an exact original point exists.

For a mixed-integer model with explicitly encoded rational polynomials
of total degree at most two, finite rational boxes, and convex
continuous slices, fixing a polynomial-bit integer assignment leaves a
continuous instance of polynomial size. Therefore, when its continuous
native Hessian span is bounded by a fixed constant, feasibility belongs
to NP: the certificate is the boxed integer assignment, and the
deterministic verifier runs the exact continuous decision algorithm.
The claim does not require a rational certificate for the continuous
feasible point. Convex-quadratic objective threshold decision adds one
convex quadratic inequality and raises the span bound by at most one.

This is not a statement about arbitrary nonconvex quadratic feasibility
or general existential real formulas. It also does not make the number
of integer variables irrelevant to deterministic complexity. Whether
fixed integer dimension together with fixed `h` permits a polynomial
algorithm requires additional mixed-integer convex-oracle theory and is
not established here.

## 6. Source and verification record

The openly available author-hosted GLS book was downloaded to
`/tmp/penalty-gls1988.pdf`; `pdftotext -layout` produced
`/tmp/penalty-gls1988.txt`. Theorem 3.2.1, its acceptance step, the
finite-precision discussion on printed p. 88, and Definition 2.1.16
were read. The earlier [1981 GLS paper](https://ir.cwi.nl/pub/10046/10046D.pdf)
was also examined, but its main setup supplies an explicit center;
the 1988 statement is the cleaner source for this reduction.

An independent reviewer read this entire argument and the cited
finite-precision algorithm, and found no gap. The review requested that
the mixed-integer consequence explicitly retain rational total-degree-two
input; the statement above includes that restriction. The review is
recorded in `hessian-span-review.md`.

This note contains a proof and a source audit, not an implemented
ellipsoid solver. No computational checks of the algorithm or Lean
formalization have been performed. No project-wide verification or CI
inspection was run.
