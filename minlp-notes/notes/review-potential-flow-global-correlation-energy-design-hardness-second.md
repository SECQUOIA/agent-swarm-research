# Second independent audit of minimum dissipation and pressure-drop hardness

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-global-correlation-energy-design-hardness.md) correctly modifies the reviewed globally correlated cactus gadget to prove strong NP-hardness of minimizing total dissipation, equivalently the unit source-to-sink potential drop. The paired bridges, curvature sign, cut constants, rational threshold gap, restricted NP membership, and rational approximate-design reduction are sound. No correction is required.

## 1. Paired bridges and topology

Each parameter coordinate is now stored in two actual serial bridge resistances `r_i=1+theta_i` and `s_i=2-theta_i`. Their equality `r_i+s_i=3` has bounded integer coefficients, and both resistances lie in `[1,2]`. Because every bridge carries unit flow, their combined dissipation is exactly three. This removes the variable bridge term rather than assuming it away.

The original bridge coordinate r_i still makes the full actual-resistance polytope an injective affine image of the cube. All triangle correlations remain unchanged, and every remaining resistance is in `[1,3]`. Replacing n prefix bridges by 2n adds n edges and n vertices to the previous gadget. Thus `V=6m+2n`, `E=8m-1+2n`, and cycle rank 2m are correct. Subdividing this prefix does not change maximum degree three, simplicity, cactus structure, or the directed acyclic orientation. Its flows remain one, and every triangle flow remains strictly positive.

## 2. Triangle dissipation and curvature

For path-edge resistance s, the path flow is `f=1/(1+sqrt(s))`. Let P be the common terminal drop. Then

```
P=2s f^2=2(1-f)^2,
triangle dissipation=2s f^3+2(1-f)^3=P[f+(1-f)]=P.
```

This proves `e(s)=2s/(1+sqrt(s))^2` for both terminal drop and actual dissipation. The latter is not the variational energy primitive, which differs by a factor of three; the candidate uses the actual dissipation consistently.

Differentiating gives

```
e'(s)=2/(1+sqrt(s))^3,
e''(s)=-3/(sqrt(s)(1+sqrt(s))^4)<0.
```

Hence the paired comparison contribution is concave and even. Its uncut and cut values are exactly `AE=24-16sqrt(2)` and `BE=13/2-3sqrt(3)`. Using the strict rational square-root bounds from the preceding review gives

```
kappaE=35/2-16sqrt(2)+3sqrt(3)
       >35/2-16(283/200)+3(173/100)=1/20>1/32.
```

In particular, a cut strictly decreases this objective, as needed for minimization.

## 3. The global minimum and prescribed potential drop

The prefix bridges contribute 3n and the joining bridges contribute `2(2m-1)=4m-2`. A binary parameter profile therefore has value

```
E(theta)=3n+4m-2+m AE-kappaE cut(theta).
```

For arbitrary theta, each triangle-pair term is a concave function of an affine parameter difference. The bridge contribution is constant. The total is thus concave on the cube and has a minimizing vertex: its value at a convex combination is at least that combination of the vertex values, which is at least their minimum. This proves the exact identity with maximum cut and the stated CE.

For any physical conserved state, the incidence identity gives

```
sum_e x_e(pi_u-pi_v)=pi^T b.
```

The signed quadratic law makes each summand `beta_e |x_e|^3`. With precisely unit source and sink nominations, the right side is the source potential minus the sink potential. Therefore minimizing this prescribed drop is exactly the same task as minimizing total dissipation on the constructed family. Potential normalization has no effect.

## 4. Rational thresholds and approximation

The center threshold is

```
3n+4m-2+(m-K+1/2)AE+(K-1/2)BE.
```

For the nontrivial source cases, both displayed coefficients lie between zero and m. Square-root enclosures of width `1/(65536(m+1))` give total substitution error at most `19m/(65536(m+1))`, which is below 1/512. Common dyadic denominators within a constant factor of the requested precision, and the fixed halves in BE and K, yield denominator O(m+1). Numerators are polynomial in m+n. Together with bounded network and polytope data this justifies strong numerical hardness, including polynomial unary encoding of rational thresholds.

In a yes instance the minimum lies below the center by at least `kappaE/2`; in a no instance it lies above by that amount. The rational threshold error gives the strict margins

```
yes: OPT<tau-7/512,
no:  OPT>tau+7/512,
```

using `kappaE>1/32`. These directions are correctly reversed from the earlier total-flow maximization. The one-edge comparison graph with target one supplies a fixed yes case, and a comparison triangle with target three supplies a fixed no case, so preprocessing trivial inputs remains inside the same physical family.

A minimizing cube vertex gives integer resistances and an objective in the fixed field `Q(sqrt(2),sqrt(3))`. Exact comparison with a rational threshold is polynomial-time, proving NP membership for the restricted weak upper-threshold design problem. No membership claim for arbitrary global-correlation families is inferred.

A value error at most 1/256 is smaller than the threshold margins. A rational design with objective at most `OPT+1/256` has value below `tau-5/512` in a yes instance, while every feasible design exceeds `tau+7/512` in a no instance. Enclosing the separate triangle roots and summing their energy values to error 1/512 distinguishes the cases. All queried resistances have polynomial output encoding in a polynomial-time rational-output algorithm, and remain uniformly bounded and positive, so this additive evaluation has polynomial bit cost. No exact arbitrary radical-sum comparison is required.

## Verification and limits

Independently checked both derivative identities and both radical endpoint identities symbolically, and checked the rational lower bound on kappaE exactly. Reused the actual-network constructor from the [previous independent checker](../code/potential_flow_mpd/global_correlation_total_flow_second_review.py) with a 2n-edge prefix. It verified the modified graph counts and the constant paired-bridge energy over 1,068 binary profiles across all 71 nonempty simple comparison graphs on two through four vertices. The triangle physics and complete node balances are inherited unchanged from that check.

The proof concerns fixed absolute accuracy and does not establish normalized or fixed relative-error hardness. Concave minimization over cube vertices and Max-Cut are classical mechanisms; this audit confirms the specific bounded passive-network realization and objective equivalence, not priority.
