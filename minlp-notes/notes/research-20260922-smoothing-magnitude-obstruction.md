# Bounded penalty noise does not remove coefficient-magnitude hardness

Date: 2026-09-22. Status: supporting consequence checked by an
[independent review](review-20260922-smoothing-magnitude-obstruction.md).
This explains why the numerical coefficient dependence in the smoothed
indicator-QP algorithms cannot simply be replaced by dependence on encoding
length. It is a scaling consequence of the existing hardness construction,
not a separate claim of a new hardness mechanism.

## Statement

Fix rational `theta` in `(0,1/10]` and a rational noise radius `sigma>0`.
The [fixed-Hessian hardness family](../results/indicator-quadratic-treewidth-two-hardness.md)
has `N=2n` variables, a matrix depending only on `n,theta`, and the promise

```
YES: v <= Delta/4,
NO:  v > Delta,
Delta=theta^2(1-theta^2)/(1+theta^4)>0.
```

The graph is a chain of triangles. Its matrix is uniformly strictly
diagonally dominant and arbitrarily close to identity when `theta` is small.
Its linear coefficients and positive indicator costs can be large.

For every such instance, a polynomial-time rational scaling produces an
instance with the same quadratic matrix and graph whose YES/NO promise
remains separated for **every** indicator-penalty perturbation satisfying
`|xi_i|<=sigma`. All perturbed penalties can also be kept positive.

Consequently, an exact expected-polynomial Turing algorithm for the prescribed
finite-grid noise model, uniform over arbitrary binary-encoded linear
coefficients and penalties, would put SUBSET SUM in ZPP. In particular, a general theorem
polynomial only in the coefficient encoding lengths cannot follow merely
from constant conditioning, width two, and bounded independent penalty noise,
unless NP is contained in ZPP.

## Scaling proof

Write the old objective, including its displayed constant, as

```
F(x,z)=x'Qx+c'x+lambda'z+c0.
```

Choose an integer `s>=1` large enough that

```
3s^2 Delta/4 > 2N sigma,
s^2 Delta/(4n) > sigma.
```

For fixed `theta,sigma`, `s` can be chosen polynomial in `n` and computed
by exact rational comparisons. For example,
`s=1+ceil(8N(1+sigma)/Delta)` is more than sufficient. Form

```
F_s(y,z)=y'Qy+s c'y+s^2 lambda'z+s^2 c0.
```

The indicator constraint is preserved by `y=sx`, and
`F_s(sx,z)=s^2 F(x,z)`. Thus the new unperturbed optimum is `s^2 v`.
Adding `xi'z` changes every feasible objective, and hence the optimum, by
at most `N sigma`. Therefore

```
YES: v_xi <= a := s^2 Delta/4 + N sigma,
NO:  v_xi >  b := s^2 Delta - N sigma,
a < b.
```

Comparison with `(a+b)/2` decides the original promise for every allowed
noise realization. The constant objective term can be subtracted from this
threshold if the input convention omits constants. The matrix `Q` is
unchanged; only linear costs, penalties, and the threshold are scaled.
All resulting data have polynomial binary encoding length.

The old state penalties are `Delta/(4n)`, and its decision penalties are
`A_i^2`, with positive integer SUBSET SUM data and
`A_i=a_i theta^(-(n-i+1))`. They are at least `Delta/(4n)`.
The second condition on `s` consequently keeps every perturbed penalty
strictly positive, even at `xi_i=-sigma`.

For the complexity conclusion, draw the rational finite-grid perturbation
using the proposed solver's specified polynomial random-bit procedure and
run that solver. Its exact answer always decides the original promise by
the preceding disjoint thresholds. If its expected bit time were polynomial
in encoded input length for arbitrary `c`, this would be a zero-error
expected-polynomial algorithm for SUBSET SUM. Its NP-completeness gives the
stated consequence. This argument is a Turing statement about finite rational
noise; it does not turn an exact real-arithmetic oracle into a Turing machine.

## Scope

This does not contradict the smoothed positive results, whose complexity
depends polynomially on numerical coefficient and spectral bounds. The
hardness family uses exponentially large linear coefficients and penalties
in the original SUBSET SUM encoding; it does not establish this obstruction
under bounded penalties. The result also does not rule out alternative structural
assumptions, instance-dependent bounds, or successful practical algorithms.
Its role is to retain an explicit obstruction to an otherwise tempting
overstatement of the smoothing theorem.

No new external hardness theorem is needed beyond the reviewed local
SUBSET SUM reduction and the standard definition of ZPP. The scaling
identities are exact algebraic identities. The independent reviewer also
reports 60 exact rational checks of scaling, threshold separation, and
positivity; those finite checks support the calculations without proving the
general complexity implication. No formal verification is claimed here.
