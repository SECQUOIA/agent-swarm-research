# Second independent review: discrete resistance hardness

Date: 2026-09-05. Reviewer: `benders_property`, independent of the author and first reviewer. Reviewed [the discrete-resistance reduction](potential-flow-discrete-resistance-hardness.md).

**Verdict: pass.** The reduction proves NP-hardness of maximizing a prescribed terminal potential difference under independent two-point resistance choices, for the common quadratic law, on the stated degree-three graph class with a single cycle-rank-two block and one bridge. Its rational gap also rules out a polynomial algorithm in input length and requested precision bits unless `P=NP`. Common resistance scaling additionally proves fixed absolute-error hardness on the unnormalized integer-data class, as corrected below. It does not establish strong NP-hardness or fixed relative-error hardness. Literature priority is a separate question.

## 1. Graph, nominations, and series aggregation

Use the outflow-minus-inflow convention for nominations. On the theta graph, put `a=(q+1)/2` and `b=(7-q)/2`. The four fixed-edge flows are `a,b,b,a` in the listed order. At vertex 0, net outflow is `a+b=4`; at vertex 1 it is `-4`; at vertex 2 it is `b+q-a=3`; at vertex 3 it is `a-b-q=-3`. These identities hold for every `q`.

All internal cross-path nominations vanish, so conservation forces the same signed flow on each cross-path edge. Summing the quadratic drops yields exactly `tau*q*|q|`, with `tau` the sum of its independently selected resistances. Hence replacing the edge by a path implements the desired Subset-Sum encoding without adding nonlinear degrees of freedom.

The theta endpoints are vertices 2 and 3. Their three internally disjoint paths run through vertex 0, through vertex 1, and along the uncertain cross path. Subdivision preserves biconnectivity and cycle rank two. The four fixed edges plus `n` cross edges have `n+3` vertices, so their cycle rank is `(n+4)-(n+3)+1=2`. The added leaf edge is a bridge. Vertices 2 and 3 have degree three, vertex 1 gains degree three from the bridge, and all other vertices have degree at most two except the degree-one leaf. The graph is simple for every `n>=1`.

The reduction can restrict to nontrivial Subset-Sum instances with positive item weights and `1<=K<=S`. Empty or immediately decided instances can be handled before constructing the graph. The full nomination vector is balanced and uses only `4,-5,3,-3,1` and zeros.

## 2. Physical law and pressure objective

The two routes from vertex 0 give the cross-endpoint difference

```
pi_2-pi_3 = b^2/6-a^2/2 = (23-10q-q^2)/12.
```

Equating this with `tau*q^2` produces the stated polynomial. For `tau>=1/2`, it is negative at zero and positive at two, and its derivative is positive for `q>=0`; hence it has a unique root in `(0,2)`. All four fixed-edge flows are positive there. Thus the equations use the correct sign branch of every quadratic law. The constructed flows satisfy conservation and both independent cycle equations, so potentials exist; uniqueness of passive physical flow identifies the solution.

Summing drops along `0->2->1` gives exactly

```
pi_0-pi_1 = a^2/2+b^2/6 = 2+(q-1)^2/6.
```

The added leaf has nomination one, so its edge `4->1` carries flow one and yields `pi_4-pi_1=3`. Changing vertex 1's nomination to `-5` leaves its theta-block net nomination at `-4`. The theta state is therefore unchanged, and the final objective is exactly `1-(q-1)^2/6`.

The objective never exceeds one. Equality is equivalent to `q=1`, which in the cycle equation is equivalent to `tau=1`, and therefore to a subset sum of `K`. The threshold direction is maximization with a yes instance attaining one, not a minimum or a strict inequality at one.

## 3. Gap and input encoding

Subtracting the cycle polynomial at one from its value at the physical root gives

```
(q-1)[(12tau+1)(q+1)+10] = 12(1-tau).
```

The bracket is positive. In a no instance, `|tau-1|>=1/(2K)` follows from integral subset sums. Since `q+1<3` and `tau<=(K+S)/(2K)`, the bracket is at most `31+18S/K`. This proves `|q-1|>=6/(31K+18S)` and the pressure gap `Delta=6/(31K+18S)^2` with the stated inequality direction.

The graph has linear size in the item count. Each resistance option has polynomial binary encoding length, as do `S`, `Delta`, and the threshold. Requesting a certified interval of width below `Delta/3` takes only `O(log(K+S))` precision bits. Comparing that interval with `1-Delta/2` distinguishes both cases: a yes interval lies above this separator at its lower endpoint, while a no interval lies below it at its upper endpoint. The same conclusion holds for an approximation with absolute error below `Delta/3`.

The unscaled gap is polynomially encoded, but need not be inverse polynomial in the input length. It directly rules out polynomial dependence on precision bits. Common resistance scaling can amplify its absolute size, so the unscaled gap alone must not be used to exclude a fixed absolute-error hardness consequence. No strong-hardness conclusion follows.

Multiplication of every resistance by `6nK` changes neither conservation nor the unique physical flow and scales all potentials. The four fixed resistances become `3nK,nK,nK,3nK`; each uncertain pair becomes `{3K,3K+3n*a_i}`; the bridge resistance becomes `18nK`. The threshold and gap receive the same factor. All are positive integers or positive rational gaps with polynomial encoding lengths.

## 4. Continuous hull and cactus comparison

For this specific reduction, independent interval hulls make the effective cross resistance range over the entire interval `[1/2,(K+S)/(2K)]`. Since `K<=S`, that interval contains one. Every hull instance therefore attains objective one, even when the discrete instance is separated from one by the proved gap. This directly checks the failure of hull replacement on the constructed theta graph.

The cactus tractability comparison imports the separately reviewed cactus hull theorem. Its use here should remain within that theorem's uncertainty and physical-model scope. The present reduction independently establishes the rank-two obstruction; it does not prove hardness for every noncactus graph or for arbitrary network-design objectives. It imposes no extra pressure bounds, flow capacities, or feasibility conditioning on physical states.

## 5. Independent checks

The [second-review checker](../code/potential_flow_mpd/discrete_resistance_second_review_checks.py) verifies four graph identities symbolically. It also enumerates 2,550 scenarios across 40 deterministic small Subset-Sum instances, checking exact series aggregation and integer scaling, then root location, objective threshold, and the no-instance gap with 70-digit arithmetic. All passed. These numerical checks supplement the exact gap proof and do not replace it.

Run with `python code/potential_flow_mpd/discrete_resistance_second_review_checks.py` in an environment containing SymPy.

## 6. Correction: common scaling gives fixed absolute-error hardness

The original version of this review incorrectly ruled out a fixed-error
hardness conclusion without accounting for unnormalized resistance scaling.
Let `A=31K+18S`, so `Delta=6/A^2`. After the integer scaling by `6nK`,
multiply every resistance by the additional positive integer `A^2`.
Conservation and all physical flows remain unchanged; each potential
difference is multiplied by `6nK A^2`. The yes objective is therefore
`6nK A^2`, while every no objective is at most
`6nK A^2-36nK`.

All resistances are positive integers of polynomial binary encoding length.
The nominations remain the same fixed small integers. An absolute-error-one
objective approximation distinguishes the cases by the midpoint of this
gap, since `36nK>=36`. Thus fixed absolute-error-one pressure optimization
is NP-hard on this unnormalized integer-data class. This scaling does not
give a fixed relative gap, polynomially bounded numerical data, or strong
NP-hardness. The physical-state and original gap proofs above are unchanged.
