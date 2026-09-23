# Independent audit of the universal arc-hull characterization

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`, independent of
the author and the other characterization reviewer.

Reviewed: [the characterization](potential-flow-series-parallel-arc-characterization.md),
including its quantitative restoration. The positive direction was checked
separately in [the series-parallel arc-hull review](review-potential-flow-series-parallel-arc-hulls-second.md).

**Verdict: PASS.** The four-node signed-quadratic obstruction, subdivision,
qualitative restoration, and polynomially encoded quantitative restoration
are correct. They establish the proposed universal graph equivalence.
This audit verifies correctness, not novelty relative to earlier nonlinear
tolerance theory.

## Reference states and probe orientation

The theta identities agree with the previously reviewed construction.
Its root polynomial is strictly increasing for nonnegative `q`, negative
at zero, and positive at two. Substituting the three specified resistances
gives `q=3/2,1,1/2`, respectively, and reverse pressures
`-49/24,-2,-49/24`. The outer flows are positive and satisfy conservation
and the signed-quadratic potential laws.

The edge `1->0` is the unique missing edge of this four-node theta, so
adding it produces exactly `K4`. With its signed flow denoted `t`, the
restricted theta nominations are correctly

```
b(t)=b+t*e_0-t*e_1.
```

The restricted state is the unique theta state for those nominations.
Its reverse pressure `F_theta(t)` therefore obeys the new-edge equation
`F_theta(t)=M*t*|t|`.

For distinct `s,t`, the constitutive monotonicity identity has a strictly
positive right side: every edge contribution is nonnegative and distinct
nominations force some flow difference. Its left side is
`-(t-s)*(F_theta(t)-F_theta(s))`. Thus `F_theta` is strictly decreasing,
without requiring differentiability of the physical solution map.

For each of the three reference resistances, `F_theta(0)<0`. A solution
with `t>=0` would have a negative left side and nonnegative right side in
the new-edge equation, so `t<0`. Strict decrease gives

```
F_theta(0)<F_theta(t)<0,
M*t^2=-F_theta(t)<-F_theta(0)<=49/24<4.
```

Consequently `|t|<2/sqrt(M)<1`. The stated nomination-box magnitude
bound `B=18` is conservative and valid. The fixed path from `1` to `0`
through vertex `2` has resistance sum `2/3`. The quadratic nomination
Lipschitz estimate therefore gives

```
|F_theta(t)-F_theta(0)|<=2*18*(2/3)*2|t|
                     =48|t|<96/10000<1/96.
```

All signs and constants check. The path avoids the uncertain cross edge,
so its sensitivity bound is uniform across the three scenarios.

The interior new pressure exceeds `-2`. Either endpoint pressure is less
than `-49/24+1/96=-65/32`. Its interior advantage is therefore greater
than `1/32`. Inverting the same fixed target law preserves this strict
order, even though all three target flows are negative.

## Exact rational flow gap

For the interior flow `t_I` and either endpoint flow `t_E`, negativity
gives the exact factorization

```
F_I-F_E=M*(t_I-t_E)*(|t_I|+|t_E|).
```

The sum of magnitudes is less than `4/sqrt(M)`. Since the pressure
advantage exceeds `1/32`, the target-flow advantage exceeds

```
g=1/(128sqrt(M))=1/1280000.
```

This rational bound follows from exact inequalities, independently of
the numerical experiment.

## Subdivision and the graph import

I directly inspected [Diestel's third-edition text](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/diestel1.pdf),
Proposition 1.7.2(ii), printed page 20 (PDF index 30). It states that a
minor of maximum degree at most three is also a topological minor.
The candidate's printed page 18 refers to a different edition; the
mathematical statement is the required one.

For `K4`, the fact also follows directly from its minor branch sets.
Inside each branch set, take a tree joining its three incident-edge
attachments. Their tree median supplies a branch vertex and internally
disjoint arms. Joining these arms along the six inter-branch edges
produces a subdivision of `K4`.

Zero internal nominations make every branch path carry one signed flow.
Its quadratic drops therefore add with the sum of its positive
resistances. Equal positive rational splits of the fixed branch
resistances preserve the three states exactly. On a cross path of more
than one edge, splitting `d=theta_L/2` among all but one edge and placing
`theta-d` on the remaining edge preserves positivity and the effective
resistance `theta`. The one-edge case correctly uses `d=0`.

Any actual edge of the subdivided probe path can be the target. Before
restoration, it has exactly the reference target flow and gap `g`.

## Qualitative restoration

Extending a subdivision physical flow by zero on extra edges is
conservation-feasible; extra vertices have zero nomination. Such a
comparison state need not satisfy the extra potential laws. Its finite
energy bounds each extra physical flow by a constant times `R^(-1/3)`.

Every full physical flow also has magnitude at most the total positive
nomination, seven. On the connected subdivision, normalized potentials
are bounded by fixed-resistance path sums. Any subsequential restricted
limit consequently satisfies the original subdivision conservation and
potential laws. Uniqueness identifies it with the corresponding reference
state. With only three scenarios, one sufficiently large integer `R`
preserves both comparisons. This establishes qualitative necessity.

## Quantitative restoration

For each scenario, the theta flow with `q=1`, zero probe flow, and zero
extra-edge flow is a valid conservation comparison point. Its energy is

```
(10+theta)/3 <=(10+71/12)/3=191/36<6.
```

It need not be the endpoint scenario's physical state. Series subdivision
preserves this energy. Hence every extra physical edge has magnitude
less than `u=(18/R)^(1/3)`.

Let `H` be the subdivision and `m` the full edge count. Restrict the full
physical flow to `H` and define its induced nomination by `b'=A_H*x_H`.
The bound of seven per edge gives `|b'_v|<=7*deg_H(v)`. The original
nomination belongs to the same box. Both vectors are balanced on `H`,
whose box has total absolute magnitude `14|E(H)|<=14m`.
Full-graph conservation gives `||b'-b||_1<=2m*u`, because extra edges
incident to subdivision vertices are counted at most twice.

The restricted state is exactly the physical state of `H` for `b'`.
Extra edges may create nonzero induced nominations at internal probe-path
vertices, so its edges need not still have equal flows. The proof
correctly compares the chosen actual target edge directly.

For its fixed positive resistance `beta_a`, its own one-edge path gives
endpoint-pressure sensitivity at most `2*(14m)*beta_a`. The global
quadratic inverse inequality, valid even across a sign change, then gives

```
|x'_a-x_a|^2 <=2*|Delta pressure|/beta_a
             <=56m*||b'-b||_1
             <=112m^2*u.
```

Thus the target resistance cancels; its subdivision-dependent magnitude
causes no loss. The proposed value

```
R=18*(2000m^2/g^2)^3
```

makes `u=g^2/(2000m^2)`, and
`|x'_a-x_a|^2<=112g^2/2000<g^2/16`. Every target-flow perturbation is
less than `g/4`. The original interior advantage exceeds `g`, so its
restored advantage exceeds `g/2` against both endpoints.

Since `1/g=1280000` is an integer, `R` is an integer with binary length
`O(log m)`. Equal path splits and the cross-path offset also have
polynomial rational encoding length. The uniform quantitative claim
therefore passes, not merely the qualitative limiting argument.

## Universal quantifiers and reproducible check

For a `K4`-minor-free graph, the already-reviewed positive theorem gives
monotonicity for every fixed balanced nomination, every admissible
independent resistance family, and every target edge. Endpoint replacement
then gives hull equality.

For a graph with a `K4` minor, the construction assigns rational positive
coefficients to every edge, integer nominations at four branch vertices,
one uncertain resistance with two positive rational endpoints, and an
actual target edge. An interior interval value has flow greater than
both endpoint values. This refutes both universal monotonicity and
universal hull equality. It does not claim failure for every nomination
or every target edge on such a graph.

I reran the existing 80-digit obstruction check. All three complete `K4`
states passed conservation, cycle, probe-law, and strict-gap assertions.
The observed target-flow advantage was approximately
`1.46520940187454e-6`, and the pressure advantage approximately
`0.0416555988671`. These support the explicit-state mechanism; the proof
and restoration above use exact identities and inequalities.

No additional operating constraints belong in the universal property.
This characterization does not itself create a new complexity result.
The electrical confluence mechanism is prior work, and novelty relative
to historical nonlinear endpoint tolerance analysis remains qualified.
