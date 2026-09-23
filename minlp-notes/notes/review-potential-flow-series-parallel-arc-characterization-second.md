# Second independent review: the topology of quadratic arc uncertainty hulls

Date: 2026-09-05. Reviewer: `potential_flow_review`.

**Verdict: PASS**, including the quantitative restoration addendum in [the candidate](potential-flow-series-parallel-arc-characterization.md). I independently checked the four-node identities, probe orientation, strict endpoint comparison, subdivision construction, extra-edge restoration, encoding bounds, and the stated equivalence. This is a correctness review, not a novelty clearance.

## 1. The four-node obstruction

With cross flow `q`, write the four outer flows as `x,y,y,x`, where

```
x=(q+1)/2,
y=(7-q)/2.
```

Their conservation residuals are exactly `(4,-4,3,-3)` when the cross flow is included. The cross pressure condition is

```
y^2/6-x^2/2=(23-10q-q^2)/12=theta*q^2.
```

The reverse terminal pressure is

```
-x^2/2-y^2/6=-2-(q-1)^2/6.
```

The specified three settings give positive flows, so these formulas use the correct branches of the quadratic law. Substitution gives `q=3/2,1,1/2` at `theta=23/108,1,71/12`, respectively. The reverse pressures are `-49/24,-2,-49/24`. All these identities were also checked with exact rational arithmetic.

## 2. The probe edge and its signs

The target probe points from node `1` to node `0`. If its signed flow is `t`, subtracting its incidence contribution leaves the old graph with nomination

```
b(t)=b+t*e_0-t*e_1.
```

This sign is essential and is correct. For distinct `s,t`, the old graph's constitutive monotonicity identity gives

```
-(t-s)(F_theta(t)-F_theta(s))>0.
```

The strict inequality holds because different nominations cannot have identical flows, and the scalar laws are strictly increasing. Thus `F_theta` decreases strictly.

The full network has a unique physical state. At its probe flow,

```
F_theta(t)=M*t*abs(t).
```

Since `F_theta(0)<0`, monotonicity forces `t<0`. It then gives `F_theta(0)<F_theta(t)<0` and `|t|<2/sqrt(M)`. For `M=10^8`, this is less than one, so the candidate's nomination bound `B=18` is conservative and valid.

The fixed two-edge path from node `1` to node `0` has resistance sum `2/3`, independent of the uncertain cross resistance. The nomination sensitivity estimate therefore gives

```
|F_theta(t)-F_theta(0)| <=48|t|<96/10000<1/96.
```

The interior setting has pressure greater than `-2`, whereas either endpoint has pressure less than `-49/24+1/96=-65/32`. Their pressure gap is greater than `1/32`. The probe law is fixed and strictly increasing, so its signed flow at the interior setting exceeds its flow at both resistance endpoints. This proves both nonmonotonicity on the interval and failure of maximum preservation for the two-point uncertainty set. It does not need to locate the exact interval maximizer.

For the later explicit gap, both probe flows are negative and have magnitude less than `2/sqrt(M)`. Hence

```
F_I-F_E=M*(t_I-t_E)*(abs(t_I)+abs(t_E)),
t_I-t_E>1/(128*sqrt(M))=1/1280000=:g.
```

The algebra and orientation in this conversion are correct.

## 3. Passing to a subdivision

The graph step is established: a minor of maximum degree at most three occurs as a topological minor. I checked [Diestel, Proposition 1.7.2(ii), third edition, printed page 20](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/diestel1.pdf). Applied to `K4`, this gives six internally disjoint branch paths. One can also see it directly by reducing each minor branch set to a tree joining its three external incidences and retaining their median vertex.

At a zero-nomination internal vertex, all edges on an oriented series path carry the same signed flow. Quadratic resistances therefore add exactly along that path. Distributing each fixed original resistance into positive rational summands realizes the five fixed branch laws. On the cross path, assigning fixed total resistance `d<theta_L` to all but one edge and using `theta-d` on the remaining edge preserves the effective resistance and positivity at both endpoints and the interior test value. For a path of one edge, `d=0` handles the case directly.

Any edge on the subdivided probe path has the original probe flow before the other graph edges are restored. Thus the strict gap does not shrink under subdivision. Orientations can be chosen along these paths; if a fixed external orientation reverses the target, the same construction instead witnesses a minimum discrepancy. The property quantifies over both extrema.

## 4. Restoring extra edges qualitatively

The old subdivision flow, extended by zero on every extra edge, satisfies conservation on the full graph when every extra vertex has zero nomination. It need not satisfy the extra-edge potential laws; it is used only as a feasible comparison point for the energy minimization.

Giving all extra edges resistance `R` bounds their physical flows by a constant times `R^(-1/3)`. The full physical flow is uniformly bounded by the total positive nomination. Potentials on the connected subdivision, normalized at one subdivision vertex, are then bounded through its fixed laws. Any subsequential limit restricted to the subdivision satisfies its original conservation and potential equations, since all extra-edge flows vanish. Uniqueness identifies the limit. No bound on potentials at extra vertices is needed.

The same sufficiently large finite integer `R` preserves both comparisons among the three fixed scenarios. This establishes rational counterexample existence independently of the quantitative addendum.

## 5. Explicit restoration and polynomial encoding

The quantitative argument also passes. The comparison point with old outer flows `1,3,3,1`, cross flow one, and zero probe and extra-edge flows has energy `(10+theta)/3<6` in each of the three scenarios. Series subdivision preserves that energy exactly. Thus every extra-edge physical flow is at most

```
u=(18/R)^(1/3)
```

in absolute value.

The full network's total positive nomination is seven. Its passive flow has acyclic directed support, so each edge has magnitude at most seven. Restricting the physical state to subdivision `H` yields a physical state on `H` with induced balanced nomination `b'=A_H x_H`. In particular,

```
|b'_v|<=7*deg_H(v),
||b'-b||_1<=2*m*u.
```

The second bound follows by counting each extra-edge incidence at most twice. The original nomination also belongs to the symmetric box `|b_v|<=7*deg_H(v)`. That box has total absolute-coordinate bound at most `14m`. These facts justify applying the nomination Lipschitz estimate to the original and induced states of the *same subdivision network*.

For the actual target edge, its one-edge path gives

```
|Delta pressure|<=2*(14m)*beta_a*||b'-b||_1.
```

The scalar inverse inequality

```
|x'-x|^2<=2*|x'*abs(x')-x*abs(x)|
```

cancels `beta_a`, yielding

```
|x'_a-x_a|^2<=56m*||b'-b||_1<=112m^2*u.
```

This bound remains valid if restoring extra edges changes internal path flows; it compares the chosen actual edge through the induced nomination, not through an assumed series reduction of the restored graph.

With the proposed integer

```
R=18*(2000*m^2/g^2)^3,
```

we have `u=g^2/(2000m^2)`, and `112/2000<1/16`. Each target flow therefore changes by less than `g/4`. The interior flow still exceeds both endpoint flows by more than `g/2`.

Here `1/g` is the fixed integer `1280000`. Hence `R` is an integer with `O(1+log m)` bits. Equal splitting of fixed branch resistances adds only path-length denominators; using `d=theta_L/2` on a longer uncertain path has the same property. All nonzero nominations are the four fixed integers. Thus the constructed resistance and nomination data have polynomial encoding length in the graph size. This assertion concerns encoding size; finding a subdivision need not be implicitly justified by an unrelated numerical procedure.

## 6. The equivalence and its scope

The reviewed positive theorem supplies coordinatewise monotonicity on every `K4`-minor-free graph. On a compact product, continuous dependence gives attained extrema. Moving one coordinate of an optimizer at a time to a suitable allowed interval endpoint proves equality with the hull extrema; the monotonicity direction may depend on the other fixed coordinates.

Conversely, the construction above violates both properties on every connected simple graph with a `K4` minor. It uses only one uncertain positive resistance, a two-point set for that coordinate, fixed positive rational resistances on all other edges, and fixed rational nominations. Thus the universal quantifiers in the proposed characterization are satisfied in the positive direction and refuted by a valid special case in the negative direction.

The characterization does not assert that every data set on a non-series-parallel graph has a nonmonotone target flow, nor that the interval optimum occurs at the exhibited interior test value. It asserts the existence of a violating instance, which is exactly what the proof supplies. No scenario side constraints are admitted.

## Checks and conclusion

I reran the 80-digit K4 checker: all conservation, cycle, probe, and strict-gap checks passed. It reported an interior target-flow advantage of `1.4652094018745436428e-6` and pressure advantage of `0.041655598867117783696`, both exceeding the proof's conservative bounds. Separate exact-rational checks passed for all theta identities, the comparison energy bound, and the constants `96/10000<1/96` and `112/2000<1/16`.

No mathematical correction is required. The source PDF first linked in the candidate could not be opened through the browsing tool; the alternate copy cited above directly verifies the same proposition, with edition-dependent pagination. Novelty remains separate from this audit, particularly because the positive sign mechanism and broader nonlinear circuit tolerance theory predate this construction.
