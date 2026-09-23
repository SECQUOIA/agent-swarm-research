# Second independent review of series-parallel envelope optimization

Date: 2026-09-05. Reviewer: independent `spatial_sdp_review` agent.
Reviewed: `notes/potential-flow-series-parallel-envelope-optimization.md`.

**Verdict: PASS.** The single-envelope comparison and attainment proof,
convex cubic/SOCP representation, polynomial bit-time additive algorithm,
energy-to-flow bound, and endpoint recovery are correct. The primary
sources supporting the graph and weak-optimization ingredients were
read directly. No substantive correction is required. This is not a
novelty clearance, particularly against unread nonlinear circuit
tolerance literature.

## Graph signs and source verification

The `K4`-minor-free convention permits applying the electrical sign
argument separately to the target edge's block. The equivalence with
series-parallel biconnected components is stated in the primary
[Cosme Llópez–Pous paper abstract](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2017.76).
[Eppstein's Lemma 9](https://www.ics.uci.edu/~eppstein/pubs/Epp-IC-92.pdf),
printed page 9, permits taking the endpoints of any existing edge
as the two terminals of a biconnected series-parallel graph.

Inducting over that two-terminal decomposition gives a fixed current
orientation: series components carry the same signed through-current,
while positive parallel conductances split it without reversing any
component's direction. Blocks not containing the target have zero
adjoint current, because they attach to the source/sink block through
single articulation vertices and contain no adjoint source. The target
bridge case has unit target current and zero current elsewhere.

[Duffin's Theorems 0 and 1](https://sites.math.washington.edu/~reu/papers/current/jim/duffin.pdf),
printed pages 306–307, independently support the confluence/current-sign
interpretation. The note correctly treats these as established graph
theory. Adjacency of the objective terminals is essential to the route
used here.

With all electrical resistances one, the reduced Laplacian is a
rational positive-definite linear system. Exact rational solution
has polynomial bit complexity and determines zero/nonzero signs
without numerical tolerance. The graph sign invariance then makes
these signs valid for all positive differential resistances.

## Simultaneous envelope comparison

For `q(x)=x|x|`, the pointwise maximum of `L q(x)` and `U q(x)`
uses `U` at positive flows and `L` at negative flows; the minimum
uses the opposite endpoints. Both resulting laws are C1 and strictly
increasing, with positive quadratic coefficients on each half-line.
Their pointwise comparison with every admissible original law is
valid on the whole real line, not merely at the eventual optimizer.

Along the interpolated law family, include the common smoothing term
`rho x`. Write `R_e=(g_e^t)'(x_e)+rho>0` before absorbing that term
into the law notation. Differentiating conservation and constitutive
equations gives

```
d(pi_tail(a)-pi_head(a))/dt = sum_e j_e d_e(x_e),
R_a dx_a/dt = sum_e j_e d_e(x_e)-d_a(x_a).
```

This is exactly the displayed numerator with the distinct own-edge
factor `-(1-j_a)`. Since `0<=j_a<=1`, all its terms are nonnegative
for the maximizing choices and nonpositive for the minimizing choices.
The signs of the other adjoint currents are invariant throughout the
interpolation. Thus the comparison holds simultaneously for all
edge-law changes; it is not an unsupported coordinatewise-extremum
argument.

The physical flows of every interpolated smoothed network are bounded
by total positive nomination, because the laws are increasing and
zero at zero. Their normalized potentials are also uniformly bounded.
Compactness, passage to the limiting equations, and uniqueness justify
the zero-smoothing limit even when some original flows vanish.

At the envelope solution, choose each allowed resistance endpoint
according to its exact flow sign. Its original quadratic law then
agrees with the envelope law on that edge. Zero flows permit either
endpoint. The complete state satisfies conservation and all selected
original laws, so physical uniqueness proves exact attainment by an
allowed scenario. Finite resistance sets cause no difficulty because
their extrema are actually members of those sets.

## Convex energy and the SOCP lift

Integrating the asymmetric envelope law gives exactly

```
H_e(x)=[c_e^+(x^+)^3+c_e^-(x^-)^3]/3.
```

This is strictly convex and coercive. Its unique minimizer on the
affine conservation space is the physical flow. In the split-variable
formulation, simultaneous positivity of `p_e,n_e` can be reduced
without changing `p_e-n_e`, and strictly lowers the positive cubic
cost; hence that formulation is exact.

For `z,u,w>=0`, the proposed two rotated-cone inequalities imply
`z^4<=w^2<=uz`. If `z>0`, this gives `z^3<=u`; if `z=0`, they force
`w=0` and allow every `u>=0`, as required. Conversely `w=z^2` works
whenever `z^3<=u`. The first cone uses the fixed rational factor one,
and both have rational rotated-cone normalizations. Thus the conic
representation has linear size. Its mere existence is not used as
a substitute for the following conditioning and bit-complexity proof.

## Explicit weak optimization and bit complexity

When nominations are nonzero, `B=sum_v |b_v|>0` and total positive
nomination is exactly `B/2`. Both the physical flow and a tree-routed
particular flow obey the stated `B/2` bound. With tree routing zero
on chords and an identity chord submatrix in the fundamental-cycle
matrix, the physical circulation coordinate equals its chord flow.
Therefore the minimizer lies in `[-B/2,B/2]^k`, strictly inside the
optimization cube `[-B,B]^k`.

For every point in that cube,

```
|x_e| <= B/2+kB <= (m+1)B=R.
```

Each circulation gradient coordinate is a sum of at most `m`
signed edge laws of magnitude at most `beta_U R^2`. Its absolute
value is bounded by `G0=m beta_U R^2`. Since `k<=m`, its Euclidean
gradient norm is at most `sqrt(k)G0<=mG0<G`. All these rational
constants have polynomial binary encoding length.

Function and gradient evaluations at rational circulation vectors
require fixed-degree rational arithmetic and sign tests on affine
edge flows. Their output encoding is polynomial in the input and
query lengths. Cubic energy pieces have exact rational values,
including at zero flows.

For a sublevel at least `delta` above optimum, the proposed radius
`min(B/4,delta/(2G))` keeps the whole ball inside the cube and gives
objective variation at most `delta/2`. The containing radius `mB`
is valid, and the logarithmic radius ratio has polynomial encoding
dependence. This supports the described weak-feasibility/bisection
argument without requiring exact feasibility at the optimum itself.

The cited optimization theorem can also be applied directly to the
cube, avoiding any ambiguity about bisection near a thin sublevel.
[Dadush, Theorem 2.5.9](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf),
printed page 48, returns a feasible rational point and an additive
objective enclosure for a centered convex body with a rational
evaluation oracle for a globally Lipschitz convex function. His
preceding encoding convention defines polynomial time in the lengths
of all rational parameters. These passages were checked directly.

For that application the cube is centered at zero, with inner radius
`B` and outer radius `mB`. Extend each scalar energy outside `[-R,R]`
by its tangent affine function. The extension is convex and C1, has
rational values and slopes at its rational breakpoints, and agrees
with the original energy on every queried feasible flow. Its scalar
derivative is globally bounded by `beta_U R^2`, so composition with
the circulation map has the same global bound `G`. This supplies
all the cited theorem's hypotheses. Consequently an energy error
`delta` is obtained in time polynomial in input length and
`log(1/delta)`, even with unbounded cycle rank.

The zero-nomination and zero-cycle-rank cases are correctly handled
directly. Neither requires the full-dimensional optimization call.

## Energy error to certified flow error

The function `g_e^*(x)-beta_L x|x|` is nondecreasing on both half-lines
and continuous at zero. The scalar signed-quadratic inequality gives

```
(g_e^*(u)-g_e^*(v))(u-v)
>= (beta_L/2)|u-v|^3.
```

Apply this with `u=v+t h`, divide by `t>0`, and integrate `t` from
zero to one. The resulting scalar Bregman divergence is at least
`beta_L |h|^3/6`. Summing over edges, its linear term vanishes
because the physical energy gradient is a potential vector in the
incidence-transpose range, orthogonal to every feasible circulation.
This proves the stated energy-gap inequality with constant `1/6`.

Thus an energy gap at most `beta_L eta^3/6` bounds every physical-flow
coordinate error by `eta`. The rational interval around the returned
target coordinate has width `2eta` and encloses the exact requested
extremum. A weak-optimization energy enclosure supplies the required
rigorous gap guarantee; no exact algebraic flow representation is
being assumed.

As supplementary verification, 10,000 independently generated rational
scalar cases, with asymmetric positive coefficients and both same-sign
and opposite-sign arguments, passed the monotonicity inequality and
the cubic Bregman bound in exact rational arithmetic.

## Endpoint recovery from approximate signs

If the approximate sign selects the wrong endpoint relative to the
envelope's exact nonzero flow, that exact flow has magnitude at most
`eta`. The same conclusion holds if the approximate flow is zero
and its arbitrary endpoint choice is wrong. Therefore the selected
original law's residual at the envelope state has magnitude at most
`beta_U eta^2` on every edge.

Let `h=x'-x*` and let `r` denote this residual. Both physical states
have the same nomination, so `Ah=0`. Subtracting their potential
equations and taking the scalar product with `h` gives exactly

```
sum_e beta_e [q(x'_e)-q(x*_e)] h_e = -sum_e r_e h_e.
```

Its left-hand side is at least `beta_L sum_e |h_e|^3/2`, hence at
least `beta_L D^3/2` for `D=||h||_infinity`. Its right-hand side
is bounded above by `m beta_U eta^2 D`. The displayed perturbation
bound follows, including the separate zero case.

For `alpha=2m beta_U/beta_L`, the rational factor `C0=1+alpha`
dominates `sqrt(alpha)`. Thus the proposed
`eta=min(epsilon/2,epsilon/C0)` simultaneously ensures the extremum
interval width and the selected endpoint scenario's target-flow
accuracy. The rational energy tolerance then has only polynomially
many extra bits. This resolves the otherwise delicate need to decide
the exact sign of a potentially zero algebraic envelope flow.

## Scope

The fixed-nomination assumption is used in the law comparison and
in endpoint recovery. No side constraints may remove intermediate
physical scenarios. The method gives additive extrema and endpoint
scenarios on this graph class with unbounded cycle rank; it does not
give exact threshold comparison or a polynomial-size exact physical
state. The comparison with nonlinear circuit tolerance literature
remains qualified as stated in the candidate.
