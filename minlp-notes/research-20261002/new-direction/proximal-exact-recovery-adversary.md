# Adversarial review of exact recovery from a nonunique optimal set

Date: 2026-10-02. Scope: a fresh review of
[proximal-exact-recovery.md](proximal-exact-recovery.md), including its
arithmetic separation argument and integration with the proximal grid
algorithm. No external literature search was performed. This review does
not establish originality.

## Verdict

No substantive gap was found. For a rational mixed-integer box QP, a
sufficiently close feasible point identifies a face on which a rational
linear-feasibility problem returns an exact optimizer. The optimal set may
be infinite. Neither enumerating its components nor knowing the optimum
value is required for the recovery lemma.

The integration remains conditional on a valid supplied growth bound. LP
feasibility, rational value reconstruction, and a final equality check do
not independently verify proximity to the global optimal set. They do not
make an invalid conditioning guess safe.

One minor precision choice was reported to the author: choose the largest
dyadic accuracy at or below the specified rational threshold, or a dyadic
within a constant factor of it. Merely choosing an arbitrarily smaller
accuracy does not imply the claimed polynomial bound on its exponent.

## 1. Constants and snapping are well defined

Use the main note's convention

```
F(x)=x^T Qx+b^T x+a,
B=DQ,
C0=max(1,max_ij |B_ij|),
H=(2nC0)^n,
tau=1/(4nDH).
```

Here `D` clears the rational data after fixed-coordinate substitution and
the original, unrefined box endpoints. It must not be defined using only
the later restricted boxes. Include the factors of two needed when
converting monomial coefficients to a symmetric matrix.

Assume a feasible point `y` has `dist(y,S)<=tau/2`, and choose a nearest
optimizer `s`. Such an optimizer exists by compactness. Both points have
integer values in the integer coordinates, and their distance is less than
one, so those coordinates agree exactly.

All positive original interval widths are at least `1/D`, while
`2tau<1/D`. Therefore the rule that snaps a continuous coordinate within
`tau` of an endpoint cannot select both endpoints. Every continuous
coordinate active at `s` is snapped to its correct endpoint. The rule can
also snap coordinates that are strictly interior at `s`; proving that these
extra snaps are harmless is the main issue.

## 2. The stationary polytope of the unknown optimizer

Let `A` be the continuous coordinates active at `s`, and let `J0` be the
strictly interior continuous coordinates. Consider, for analysis only,

```
P = {x in X : x_A=s_A, x_int=s_int, grad_J0 F(x)=0}.
```

After fixing the integer coordinates this is an ordinary bounded rational
polytope. It contains `s`, by first-order optimality within that fixed
integer slice and continuous face.

Every point of `P` is optimal. If `x in P` and `v=x-s`, then `v` is
supported on `J0`. Subtracting stationarity equations gives
`Q_J0J0 v_J0=0`. The exact quadratic expansion is therefore

```
F(x)-F(s)=grad F(s)^T v+v^T Qv=0.
```

This identity does not require an inverse Hessian or a positive-definite
free block. It is valid when the stationary polytope has positive dimension.
The algorithm does not need to know `s`, `A`, or `J0`.

## 3. A common vertex denominator is the decisive bound

Scale continuous coordinates by `u=Dx`. Fixed true bounds, fixed integer
values, and all box bounds have integral scaled values. The free
stationarity equations become

```
2 B_J0J0 u_J0 = -D^2 b_J0 - 2 B_J0,Aunionint u_Aunionint.
```

Both the coefficient matrix and the right-hand side are integral. At any
vertex, choose a full-rank square subsystem from these stationarity rows
and the active bound rows. A bound row is a signed unit row. Every matrix
entry has magnitude at most `2C0`, including those unit rows.

For a subsystem of size `m<=n`, its nonzero determinant `delta` satisfies

```
1<=|delta|<=m!(2C0)^m<=H.
```

Cramer's rule puts every free scaled coordinate over the same denominator
`|delta|`. Returning to the original coordinates gives the common
denominator `D|delta|<=DH`. Fixed coordinates and input bounds also have
denominators dividing this same integer. Rank-deficient stationarity rows
cause no problem: enough independent active bounds complete the vertex
system. For a zero-dimensional system use determinant one.

The common denominator matters. Separate coordinate-denominator bounds
alone would not give the same bound for a sum of slacks.

## 4. Extra snapped bounds have a common optimal intersection

Let `E` be the extra snapped coordinates, those in `J0`. Define `q(x)` as
the sum of their nonnegative slacks to the selected endpoints. Each slack
at `s` is at most `tau+tau/2`, so

```
0<=q(s)<=3n tau/2=3/(8DH)<1/(DH).
```

The linear function `q` attains a minimum at a vertex of the nonempty
compact polytope `P`. At such a vertex, its value has denominator dividing
the common integer `D|delta|`. If that minimum were positive, it would
therefore be at least `1/(DH)`, contradicting the displayed upper bound.
Thus the minimum is zero.

Because all component slacks are nonnegative, a zero sum makes every extra
snapped coordinate attain its selected endpoint simultaneously. There is
therefore an optimizer `s' in P` on the entire selected face. This proves
more than separate feasibility of each snap and is the step needed by the
algorithm. If there are no extra snaps, the argument simply uses `q=0`.

## 5. Why the final stationarity LP cannot return a saddle value

Let `J` be the continuous coordinates left free by the actual snapping rule.
All true active coordinates were snapped, so `J` is a subset of `J0`.
Fix the snapped coordinates and the integer coordinates, retain the original
box bounds, and impose

```
grad_J F(x)=0.
```

This rational linear-feasibility system contains `s'`: it satisfies the
stronger stationarity equations for `J0`. For any other feasible solution
`x`, the displacement `x-s'` is supported on `J`, and subtracting the two
stationarity equations gives `Q_JJ (x-s')_J=0`. The quadratic expansion
then proves

```
F(x)=F(s')=f*.
```

Stationarity alone would not ordinarily identify a global optimum. Here
the preceding separation argument proves that an actual global optimizer
belongs to this same stationary face, and all stationary points on that
face have the same value. Both ingredients are necessary.

The LP has at most `n` continuous variables, linear stationarity equations,
and box bounds. Its coefficients come from the original rational QP.
Fixed integer values have encoding length bounded by the original integer
interval endpoints. No approximate continuous grid coordinate is inserted
into the LP coefficients. Exact rational linear programming therefore has
polynomial bit complexity and returns a rational feasible point of
polynomial encoding length. Exhaustive face or vertex enumeration is not
part of the algorithm.

## 6. Integration and the role of the optimum value

Under the supplied promise

```
F(y)-f* >= (L/kappa) dist(y,S)^2,
```

a promise-valid interval of width at most
`L tau^2/(4kappa)` gives `dist(y,S)<=tau/2`. The inclusive endpoint is
sufficient for the lemma: the slack bound remains strictly below
`1/(DH)`. Thus the main note's target precision is valid.

The snapping and stationarity LP already recover an exact optimizer under
this hypothesis. They do not require `f*` as an input. The main note also
uses the standard value-height bound

```
R=DH,       V=D R^2
```

and an interval of width at most `1/(4V^2)` to reconstruct `f*` and check
the returned point's exact objective. This is a valid additional check,
not a hidden optimization oracle.

All constants have polynomial binary length. Choosing a dyadic precision
within a constant factor of the smaller threshold has polynomially many
accuracy bits. The proximal approximation theorem followed by this one LP
therefore gives `f(p,kappa) poly(I)` bit complexity for an exact optimizer
and exact value, with an absolute polynomial exponent.

If the supplied growth bound is false, the local interval can fail to
contain the true global value. Isolating a rational inside that invalid
interval and matching it with the LP candidate would not repair the
failure. The theorem remains a trusted-promise result.

## 7. Targeted verification

A second independent reviewer checked vertex heights, common slack
denominators, true-bound inclusion, simultaneous extra snapping, selected
face feasibility, the constant-objective identity, and polynomial LP
encoding. That reviewer found no gap.

An inline exact-`Fraction` Python check was run with `python3 -`. The final
run passed 37 snapping cases, 112 stationary-polytope vertices, and 20 extra
bound snaps. Families included an optimal diagonal segment, a rationally
shifted and sloped segment, a flat family with another coordinate fixed by
stationarity, disconnected optima, and mixed integer/continuous optima.
It tested lower and upper extra snaps, a selected face with remaining free
coordinates, vertex heights, positive slack gaps, zero joint slack, and
objective equality at both vertices and their averages.

The first test construction was rejected by its own proximity assertion
because some deliberately varied perturbations exceeded `tau/2`; the
perturbation range was corrected before the successful run. This was a
test-input failure, not a counterexample satisfying the recovery lemma.

These checks used exhaustive small stationary-polytope vertex enumeration
as an independent verification method. They do not claim an implementation
or benchmark of the polynomial-time LP step. No project-wide verification,
CI inspection, or external search was performed.
