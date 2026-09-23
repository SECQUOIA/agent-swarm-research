# Independent review: NP membership for fixed-parameter linear fibers

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: the lemma and fixed-pool/fixed-quality pooling consequence are
correct as stated.** This reviews
[the candidate proof](fixed-parameter-lp-np-membership.md). The argument uses
standard ingredients, and no novelty claim is made for the general lemma.

A nonempty bounded closed polyhedral fiber has a vertex, including when its
affine dimension is smaller than the number of flow variables. At a vertex,
the active row normals span the whole flow-variable space. Otherwise a nonzero
orthogonal direction gives a sufficiently short feasible segment because all
inactive inequalities have positive slack. Thus a square nonsingular active
row basis exists. Its row indices form a polynomial-length certificate.

For a guessed basis, write `D=det B` and `N=adj(B)d`. The proposed verifier
requires `D^2>0` and `(A_j N-b_j D)D<=0` for every original row, together with
the parameter-domain conditions. These signs are correct for both determinant
signs: they multiply the reconstructed inequality by `D^2`. Acceptance yields
an actual feasible point `N/D`; completeness follows from a vertex basis at any
feasible parameter. No rationality assumption about that parameter is needed.

With entry degree at most `d`, determinant and Cramer-numerator degrees are at
most `nd`; the verifier degree is at most `(2n+1)d`. Fixed parameter dimension
makes the dense monomial count polynomial. Clearing rational coefficient
denominators has polynomial bit cost. Each determinant coefficient is a sum
of at most `n! M^n` signed products if `M` bounds the entry monomial count, so
its bit length is bounded polynomially by input coefficient sizes, `n`, and
`log M`. Exact evaluation on a tensor grid of side `nd+1`, followed by rational
interpolation, computes all determinant polynomials in polynomial bit time.
The integer evaluation points and determinant values also have polynomial bit
length. There are only `n+1` determinants to construct by Cramer's rule.

Fixed-dimensional real-algebraic feasibility therefore verifies the guessed
basis in deterministic polynomial bit time, even though the list of possible
bases can be exponential. I checked the cited
[Basu survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf),
Theorem 2.18, which supplies quantifier-elimination operation counts and
coefficient bit bounds. For a single fixed-size quantified block, both are
polynomial. Strict determinant nonvanishing is allowed by the sign-formula
framework. No compactness assumption on the parameter set is needed for this
feasibility argument. The `n=0` case is direct fixed-dimensional feasibility.

For pooling with fixed pool and quality counts, fixing all pool qualities
leaves a linear system in every flow, including arbitrary bypasses, lower flow
bounds, conservation, quality specifications, and an objective threshold.
Finite flow bounds give bounded fibers. The usual input-quality ranges suffice
as a rational parameter box, with arbitrary in-range assignments at inactive
pools. The model here has no unmodeled recirculating source-free components.

Consequently the independently reviewed
[one-pool bypass-copy construction](review-pooling-one-pool-bypass-copy.md),
combined with this upper bound, gives NP-completeness for its precise model:
one pool and one physical quality with upper/lower specifications, or two
upper-only quality coordinates, arbitrary bypasses, and exact supply/demand
contracts. This does not prove strong NP-completeness or NP membership when
both the pool and quality counts are unrestricted.

## Added parameterizations reviewed on 2026-09-05

The promoted [result](../results/fixed-parameter-linear-fibers-np-membership.md)
also has two valid pooling consequences.

First, fixed pool count and fixed affine rank of input-quality vectors
suffice for NP membership with unrestricted attribute count and bypass
graph. The exact rational affine-coordinate construction was independently
checked in the [structural pooling audit](review-pooling-bypass-structure-second.md).
It gives a fixed-dimensional core and affine coefficient dependence in
the entire flow LP without needing any bypass decomposition for this
nondeterministic upper bound.

Second, fixed pool count and fixed output count suffice, even with
unrestricted input count, attribute count, affine quality rank, and
bypasses. Use each pool's outgoing fractions as the fixed-dimensional
core. For total intake `T_l=sum_i y_il`, substitute output flow
`v_lj=theta_lj T_l` and output attribute mass
`theta_lj sum_i C_ik y_il`. Once fractions are fixed, every original
capacity, quality specification, and cost is linear in intakes and direct
bypass flows. Fractions lie in a rational simplex, with missing arcs
excluded. Positive-throughput physical pools determine these fractions;
inactive pools can choose any split. Conversely the substituted flows
and source-weighted pool quality reconstruct the physical model.

A pool without an outgoing arc forces all its intakes to zero. Before
removing it, its pool and incident-arc lower bounds must be checked for
compatibility with zero. I requested this explicit preprocessing
clarification because the statement permits lower bounds. Subject to
that routine check, no defect remains. All remaining flow fibers are
bounded by the assumed finite capacities, and the general NP lemma
applies. This upper bound upgrades the reviewed two-pool/two-output
hardness construction to ordinary NP-completeness, without claiming a
polynomial optimization algorithm.
