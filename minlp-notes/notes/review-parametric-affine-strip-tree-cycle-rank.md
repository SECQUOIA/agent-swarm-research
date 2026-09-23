# Independent review: affine strips on trees and fixed total cycle rank

Date: 2026-09-05. Reviewer: `benders_property`. Status: mathematical PASS. The author applied the orientation and optimization-output clarifications below; I verified the final integrated text.

Reviewed the new final section of [the affine-strip projection note](parametric-affine-strip-path-projection.md) and the [earlier full path audit](review-parametric-affine-strip-path-projection.md). This is a bounded audit of the tree and fixed-total-cycle-rank extensions, not a new review or priority claim for difference constraints and real-algebraic elimination.

## Arbitrary tree branching and original edge directions

For an original nonzero-gain transition directed u→v, choose scaling factors satisfying `A_v=a_e*A_u`. On a rooted forest this determines every A from the root value one: traversing an edge in its original direction multiplies by its gain, and traversing against that direction divides by it. Thus A_v is a product of gains and reciprocal gains on the root path. Division of the original row by A_v gives a difference interval for `y_v-y_u`, with the bounds reversed when A_v is negative. Original input directions therefore need not point away from the chosen root.

The initial tree paragraph described an orientation away from the root. For its use on a general spanning forest, the reciprocal rule above should be explicit; merely reversing an original strip row without changing its gain would be incorrect. This clarification was sent to the author.

If an original gain is zero, its row becomes a coordinate interval at the original head v and imposes no relation to u. Delete that edge and keep the new bounds at v, regardless of the chosen rooting direction. Restart normalizers on the resulting components. This also handles several zero-gain rows meeting at one vertex and isolated components.

For each nonzero component, the transformed bidirected tree has one arc upper bound in each direction per edge. The sum of the two lengths is nonnegative. A closed walk traverses each tree edge equally many times in each direction and consequently has nonnegative total length. Removing closed excursions from any walk leaves the unique simple path. Its sum is therefore the exact directed distance, even with negative individual lengths.

The same all-pairs lower-versus-propagated-upper inequalities are necessary and sufficient. The minimum formula supplies all upper bounds, all lower bounds by those inequalities, and adjacent transitions by the directed triangle inequality. It does not rely on degree two. Branching creates additional pairs, but no alternative paths, shortest-path choices, or exponential disjunctions.

## Multiple retained states and denominator control

At a retained state, use its prospective normalized value as both a lower and upper bound, while keeping its original coordinate restrictions separately. The recovered state then equals that value. All retained vertices can be handled simultaneously. Multiple lower and upper bounds from zero transitions are kept as candidates; feasibility uses all relevant candidate pairs and recovery takes the minimum over the upper candidates. Their total number is linear in the input, so the all-pairs description remains polynomial.

A single denominator makes the bit bound explicit even for arbitrary original directions. Within a nonzero component write `A_v=N_v/D_v`, where N_v and D_v are products over disjoint subsets of gains on its root path. Let G be the product of every nonzero gain in the component. Then N_v divides G as a polynomial product. Every normalized bound `b/A_v=b*D_v/N_v`, and every retained value divided by A_v, can be represented over denominator G by multiplication with G/N_v. The degrees of these numerators are at most the input bound degree plus twice the sum of gain degrees. Every distance is a sum of such expressions with that same denominator.

The sign of G is fixed and nonzero on the current sign cell. Clearing it, or using its square, therefore yields equivalent polynomial inequalities. Fixed parameter dimension makes the number of dense monomials polynomial in these degree bounds. Product coefficient bit lengths and rational coefficient-denominator clearing also remain polynomial. The extra retained variables appear only linearly before any separately supplied retained-coordinate constraints are added.

After solving for the retained coordinates and parameters, recovery uses rational functions and finite minima in their common real-algebraic field. Choosing a minimum selects an existing value rather than adjoining a new root. Polynomially many comparisons and arithmetic operations suffice; no algebraic tower is formed along branches.

## Fixed total cycle rank

Removing c nonforest edges leaves a spanning forest. Retaining every endpoint of those removed edges adds at most 2c distinct state variables. Forest projection removes all other nonretained states, and each removed original strip is then a polynomial constraint on the retained endpoints and parameters. There is no need to normalize a removed strip or divide by its gain. Its zero and negative cases remain valid directly in the original inequalities.

When the parameter dimension, c, and the number of additional objective or constraint states are fixed, this produces a fixed-dimensional semialgebraic problem of polynomial description length, degree, and coefficient bit length. Sign-cell enumeration depends only on the fixed parameter dimension. Components without retained states contribute parameter-feasibility conditions; components with retained states contribute the corresponding projected inequalities. Having arbitrarily many forest components does not increase the remaining dimension.

The parameter is **total** cycle rank. A graph with many rank-one blocks may have unbounded total rank, and this construction can retain arbitrarily many cycle endpoints on it. The explicit exclusion of a fixed-maximum-block-rank interpretation is correct. The common gain in both sides of each strip remains essential; an arbitrary two-variable polygon does not inherit the argument.

## Optimization output scope

Projection and fixed-dimensional real-algebraic methods give exact feasibility, infimum analysis, and attainment decisions. A witness optimizer can be returned when the infimum is attained. Finite state intervals depending on t do not themselves make the t-domain compact, so an unconditional optimizer claim would be too strong. For example, a strict parameter domain can have an unattained objective infimum even when every state is fixed to zero. I requested that the final text either state this infimum/attainment distinction or impose an appropriate closed compact feasible-domain hypothesis when promising an optimizer.

No algorithmic or algebraic gap was found after these two scope clarifications. No new general numerical test was needed: the new confidence comes from the unique-path proof, the explicit reciprocal-gain denominator construction, and the fixed retained-dimension count.
