# Independent review of the scalar noisy-design FPTAS

Date: 2026-09-12. Reviewed
[the FPTAS corollary and priority audit](research-20260912-scalar-noisy-design-fptas.md)
independently, using the previously reviewed uniform finite-history bound.
The approximation scheme is correct for the stated fixed-contraction,
fixed-noise-ratio input class. The PSD weighted-trace extension is also
correct, even when matrix dimension is part of the input. No FPTAS for a
multi-parameter logdet objective follows from this argument.

Two minor conventions should be explicit: the accuracy input `epsilon` is
rational, and the literal graph-size bound is `O(n(k+1)2^L)` when `k=0` is
allowed. Alternatively, immediately return the empty selection for `k=0`.
Neither affects the approximation or polynomial-time conclusion.

## Approximation and dynamic programming

Fix rational class constants `0<rho0<1` and `B0>0`. With
`C0=2B0/(1-rho0)^2`, choose the first nonnegative integer `L` satisfying
`C0 rho0^(L+1)<=epsilon/2`, capped at `n-1`. The cap means using exact full
selected history, so its true approximation error is zero even if the
geometric certificate still exceeds the target. The cases `n=0` and `n=1`
are correctly treated separately.

Every choose-arc weight depends only on the previous `L` selection bits.
The accumulated scalar reward is additive. Keeping only the largest
accumulated value at each time/mask/count state is therefore valid: all paths
reaching that state have exactly the same allowed future continuations and
future rewards. Mandatory and forbidden candidates can remove choose or
skip arcs. Terminal count `k` gives the exact surrogate optimum.

For the weighted trace, the relevant positivity is

```text
A<=B and W>=0  =>  tr(WA)<=tr(WB).
```

It follows because `tr[W(B-A)]` is the trace of a PSD congruence. Thus the
matrix precision sandwich gives the same scalar relative sandwich after
congruence by `F_S` and application of the trace functional. Also
`tr(WJ0)>=0`, even if `W` and `J0` do not commute. The direct arc calculation
`G W G^T/d` is rational and nonnegative; computing a possibly irrational
square-root factor of `W` is unnecessary.

The approximation ratio follows exactly as stated:

```text
I(S_hat) >= I_L(S_hat)/(1+delta)
         >= I_L(S_star)/(1+delta)
         >= (1-delta)/(1+delta) I(S_star).
```

For `delta<=epsilon/2`, the last factor is at least `1-epsilon`. A zero
optimum causes no division and is harmless. If the optimum is positive,
the positive ratio ensures the returned value is positive, so the subsequent
logarithmic inequality is defined. No positive sensitivity lower bound is
needed.

## Exact bit complexity and the cap

For the uncapped choice, let
`x=log(C0/(epsilon/2))/log(1/rho0)`. Its exact integer characterization is
`L=max(0,ceil(x)-1)`, giving

```text
2^L <= max(1,(2C0/epsilon)^a0),
a0=log(2)/log(1/rho0).
```

The implementation need not evaluate these logarithms. Incrementing `L`
and comparing rational powers obtains the same integer. Capping `L` can
only decrease `2^L`. In particular, choosing an exact, potentially
exponential-in-`n` full-history graph at very small `epsilon` does not
contradict the FPTAS bound: whenever that cap is reached, the same graph
size is bounded by the displayed polynomial in `1/epsilon`.

The rational arithmetic justification is sufficient. More explicitly:

- Each latent variance follows a rational affine recurrence in the preceding
  variance. A calendar covariance entry is that variance times a product of
  transitions, plus measurement noise on the diagonal. Their numerator and
  denominator bit lengths are polynomial in the rational input encoding.
- Each local covariance is SPD because measurement noise is strictly positive.
  Its dimension is at most `L`. Clearing its finitely many denominators and
  applying determinant/cofactor bounds gives polynomial bit lengths for
  every inverse entry; fraction-free elimination gives a polynomial-time
  computation. Poor numerical conditioning does not alter this exact
  arithmetic conclusion.
- Local weights use polynomially many rational products and sums, including
  the input matrices for weighted trace. Their bit lengths are polynomial
  in input size, `n`, `L`, and matrix dimension.
- A stored path value is the sum of at most `n` local weights. A common
  denominator can be the product of their denominators, whose bit length
  is at most the sum of their bit lengths. Maximization selects one path
  value rather than combining exponentially many values. Exact comparisons
  therefore retain polynomial bit complexity.

The graph has `O(n(k+1)2^L)` states and arcs, and local conditional
precomputation has `n2^L` possible time/history pairs with polynomial work
per pair. Combining these facts gives polynomial time in input encoding
length and `1/epsilon`. The exponent `a0` may depend on the fixed class
constant `rho0`, as permitted for an FPTAS on that class.

The input-class qualifications are essential. An arbitrarily input-dependent
`rho0` approaching one makes this exponent unbounded. An unbounded
binary-encoded noise ratio enters the size bound through its numerical value,
which need not be polynomial in its encoding length. A suitable polynomial
ratio promise could suffice, but the note correctly avoids claiming the
result for unrestricted binary input parameters.

## Closest-prior check

I independently read §4, Theorem 4.1 and Corollary 4.2, and §7 of Das and
Kempe's [primary author PDF](https://david-kempe.com/publications/regression.pdf),
*Algorithms for Subset Selection in Linear Regression*, STOC 2008. The local
full text used for the check is
`/tmp/research-20260912-das-kempe-regression.pdf` and its extracted text.

The note accurately reports their scalar quadratic objective, fixed-bandwidth
approximation scheme, displayed dependence on bandwidth and condition number,
and the covariance-entry perturbation corollary. For fixed positive
stationary correlation and nugget, choosing the perturbation error to be
`O(epsilon)` requires its displayed entry threshold to be `O(epsilon/k)`.
In the regime before the finite-horizon cap, the exponentially decaying tail
then gives bandwidth `beta=Theta(log(k/epsilon))`.

The displayed running-time term `(k/epsilon)^(beta^2)` becomes
`exp(Theta(log^3(k/epsilon)))` on this substitution. Thus that particular
published bound yields a quasi-polynomial estimate, not an FPTAS bound for
this dense noisy class. This is an audit of the displayed construction, not
a lower bound on its possible implementation or a claim that no other
algorithm in the literature supplies an FPTAS.

Section 7 assumes exact covariance entries `a^|y_i-y_j|`, including the
unit diagonal, and uses the selected covariance's tridiagonal inverse.
With positive stationary nugget, normalized correlations instead satisfy

```text
C_13=alpha rho^2,
C_12 C_23=alpha^2 rho^2,
0<alpha<1,
```

so the exact exponential-line identity fails. This verifies the stated
distinction. When describing the noiseless Markov subclass covered by that
prior, it is safest to say *nonsingular* noiseless covariances; zero process
innovations can otherwise produce singular adjacent observations outside
the inverse-based formulation.

The observation/target interpretation does not make the scalar quadratic
objective a new optimization problem. Conversely, the present weighted-trace
corollary is not a conclusion about an inverse-trace criterion or a
multi-parameter logdet objective: those are not additive scalar arc rewards.

## Outcome and remaining work

No substantive correctness blocker remains. The minor accuracy-encoding and
`k=0` conventions above should be recorded. This is a formal corollary review,
not an implementation benchmark or a completed publication-priority search.
The later structured-regression and latent-state approximation literature
remains important to the priority assessment. No production code or
knowledge-base entry was modified.
