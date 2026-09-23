# Independent audit: cacti and universal weighted arc-flow resistance hulls

Date: 2026-09-05. Reviewer: `benders_property`.

**PASS, with the explicit slice-wise monotonicity convention now present.**
I independently checked
[the cactus characterization](potential-flow-weighted-arc-cactus-characterization.md).
Both directions are valid for connected simple graphs, fixed balanced
nominations, common quadratic passive laws, and nonempty compact positive
scalar resistance sets. The noncactus construction uses the stated four
nominations, two objective coefficients, and one uncertain resistance.
The quantitative restoration preserves its gap. Arithmetic complexity
of optimizing many independent cycles and literature priority remain
separate questions.

## Cactus decomposition and the meaning of monotonicity

Fixed nominations determine every bridge flow and every cycle's effective
boundary nominations, independently of resistance choices. This follows
by summing conservation over the components attached at its articulation
vertices. Distinct cycle blocks therefore have independent circulation
equations with disjoint resistance sets. A linear arc-flow objective is
a bridge constant plus affine functions of those scalar circulations.

For one consistently oriented cycle, `H_beta(q)` is continuous and
strictly increasing from minus infinity to plus infinity. At
`q=-d_e`, its value does not depend on `beta_e`. The unique root's
position relative to this point, and hence the sign of `q+d_e`, cannot
change while only `beta_e` varies. If the flow is zero for one setting,
that same root satisfies every setting. Otherwise, changing `beta_e`
changes `H` at its previous root with a fixed sign, and comparison of
strictly increasing equations gives monotonicity of the root. Multiplying
by the cycle's objective coefficient preserves monotonicity, possibly
reversing its direction.

The direction is allowed to depend on the fixed values of the other
resistances. This qualification matters. For cycle offsets `(0,1,-1)`,
the sign of `H(0)=beta_2-beta_3` changes with those two resistances,
and so can the direction of the circulation's dependence on `beta_1`.
The proof establishes monotonicity on each one-coordinate section;
it does not give a common direction vector throughout an entire box.
The revised statement explicitly adopts the correct convention.

Physical states depend continuously on positive resistance parameters,
so products of nonempty compact sets and their interval hulls have
attained extrema. Starting from a hull optimizer, change one coordinate
at a time to an endpoint that does not worsen the objective. Section-wise
monotonicity is sufficient even if its direction changes after another
coordinate is moved. Each endpoint belongs to the corresponding original
compact set. This proves equality of maximum and minimum values and
establishes the cactus direction.

## Theta obstruction and embedding

The exact weighted-flow theta states have already passed the separate
full gadget audit. Their objective values are `-9/2` at the interior
resistance and `-37/8` at both endpoints, giving advantage `1/8`.
This violates section-wise monotonicity and hull equality on the theta.

Every noncactus connected simple graph contains the required theta
subgraph. In a biconnected block other than a cycle or edge, choose a
cycle. A chord gives three internally disjoint paths immediately. If
there is no chord, the block must contain off-cycle vertices. A connected
component of those vertices has at least two distinct neighbors on the
cycle, since a unique neighbor would be an articulation. A simple path
through that component together with the two cycle arcs gives the theta.

Simplicity ensures that at most one of the three paths has no internal
vertex. Internal vertices `0,1` can therefore be selected on two
different paths, with the remaining path designated for the cross
resistance. The four prescribed nonzero nominations are at distinct
vertices. Distributing fixed segment resistance totals preserves the
gadget because internal nominations are zero and segment flows coincide.
On a longer cross path, the fixed total `theta_L/2` and variable remaining
resistance `theta-theta_L/2` stay positive at both endpoints and throughout
their hull. Exactly one physical edge needs to be uncertain.

Choosing one consistently oriented edge on each of the two objective
segments gives coefficients `-9` and `5`. Under subdivision alone their
flows equal the original `a,q`. Additional edges may disturb those
equalities, which is why the separate restoration estimate is needed.

## Restoring all extra edges

The displayed comparison flow is conservation-feasible in the whole
graph at all three resistance settings. Every extra edge carries zero
in that comparison, and all extra vertices have zero nomination. Its
energy depends only on the selected resistance totals. I checked its
largest value exactly:

```
[(9/8)^3+3^3+(23/8)^3+2+12032*(9/8)^3]/3
=91657/16<6000.
```

The physical state minimizes the nonnegative energy. Thus an extra edge
of resistance `R` has `R|x_e|^3/3<6000`, giving the claimed bound
`|x_e|<=u=(18000/R)^(1/3)`. Independently, every physical edge flow is
bounded by total positive nomination, which is seven. This uses the
acyclic orientation induced by strictly decreasing physical potentials.

Restrict the physical state to the selected theta and define `b'` by
its selected-edge conservation. This is exactly a physical theta state
at `b'`: the restricted potentials still satisfy every selected law, and
uniqueness identifies the state. Its nominations are balanced. Selected
degree is at most three, so every coordinate has magnitude at most 21.
The original four nominations also obey this bound. The theta has
`n_theta=m_theta-1<=m` vertices, so a common balanced box can have total
absolute coordinate bound `B<=21m`. Conservation gives
`||b'-b||_1<=2m u` by charging each extra edge at most twice.

The single-edge nomination-to-pressure estimate is valid without any
flow-sign assumption. It can also be derived directly here. For the two
theta states form positive secant resistances

```
r_f=beta_f[phi(x'_f)-phi(x_f)]/(x'_f-x_f),
phi(t)=t|t|,
```

when the flows differ; when they agree choose any positive value up to
`2B beta_f`. In every case `r_f<=2B beta_f`, and the difference state is
an electrical flow with these resistances and nomination `b'-b`.
The unit endpoint adjoint for edge `e` has potential oscillation equal
to its effective resistance, at most the resistance `r_e` of that direct
edge. Therefore

```
|Delta(pi_tail-pi_head)|<=2B beta_e ||b'-b||_1.
```

The scalar inequality `|x'-x|^2<=2|phi(x')-phi(x)|` then gives

```
|x'_e-x_e|^2<=4B||b'-b||_1<=168m^2 u.
```

The resistance cancels exactly. This is essential for objective edges
inside long subdivisions and applies equally when their flows change
sign or vanish. The weighted objective error is bounded by
`14 sqrt(168m^2 u)`.

With the stated integer
`R=18000(10^9 m^2)^3`, one has `u=1/(10^9m^2)`. I verified the final
comparison with exact rational arithmetic:

```
14^2*168/10^9=1029/31250000<1/1024.
```

Every endpoint and interior objective therefore changes by less than
`1/32`. The interior advantage over either endpoint remains greater than
`1/16`. All restored resistances and subdivision data have polynomial
rational encoding length; no limiting infinite resistance is used.

## Equivalence and boundaries

On every noncactus, hold all restored resistance values fixed and allow
only the designated uncertain edge its two endpoints. Its hull contains
the interior setting with the strictly better value just proved. This
violates property 3. The same one-coordinate function exceeds both
endpoint values at an interior point, so it is not monotone and violates
property 2. Together with the cactus implications, this completes all
directions of the characterization.

If positive boxes in property 2 are taken to have nondegenerate intervals
in every coordinate, simply choose such intervals containing the fixed
values of the other resistances; their one-coordinate section already
violates the property. Property 3 permits singleton compact sets for
those fixed edges, as needed.

Equality of maxima for every linear flow functional is equivalently
equality of the closed convex hulls of the two compact attainable flow
sets. It is not equality of the underlying flow sets and does not by
itself supply an exact arithmetic algorithm for sums of many independent
cycle extrema. The result correctly keeps this structural statement
separate from both the larger series-parallel class for individual-arc
objectives and the separate fixed-rank complexity results.

No substantive defect remains after the explicit section-wise
monotonicity and nonempty-set clarifications.

## Positive-coefficient obstruction

The obstruction also works with positive coefficients `(9,5)`: choose
an objective edge on the `0->3` segment instead of the `0->2` segment.
Before restoration, conservation changes the objective to `F+36`, so
the interior advantage remains `1/8` and both selected flows are
positive. The restoration bound depends only on the coefficient
absolute sum, still `9+5=14`. Therefore the restored interior advantage
is still greater than `1/16`. Each selected flow stays positive as well:
the largest individual perturbation is less than `1/(32*14)`, whereas
the smallest selected theta flow at the three tested scenarios is
`1/32`. This positive-coefficient corollary passes independently.
