# Many-leaf reciprocal-anchor hull: mathematical obligations

This inventory covers every mathematical and algorithmic assertion in
[the full-hull note](../../../results/common-factor-reciprocal-anchor-full-hull.md).
The note's theorem concerns the convex hull of the original graph, with an
arbitrary finite number of leaves. An assertion about a supplied feasible
distribution alone does not prove that theorem. Likewise, a sound formula
evaluated on supplied envelope data does not prove that such data can always
be constructed, or prove the advertised running time.

The inventory is the frozen obligation list, not a completion claim.
`COVERAGE.md` must map each identifier to actual Lean declarations and describe
any difference between the source statement and the proved statement.
Existing one-leaf results may discharge unchanged obligations, but their use
must be identified. Source proofs may be reorganized; an alternative proof
must still establish the same mathematical conclusion and boundary cases.

Use real variables for the hull theorem with `0 < a < b`; rationality is
required only for the rational algorithms and decompositions. Include zero
leaves, zero or unit leaf masses, duplicate lines, tied slopes, coincident
breakpoints, zero-probability atoms, and reciprocal endpoints that coincide.
Division in Lean is total, so denominator hypotheses must be stated where
the source uses genuine fractions. Finite sums may replace expectations
where finite convex representations suffice; a claim about arbitrary
probability distributions must retain its measure-theoretic scope or be
marked separately.

## Original hull and linear conditions

| ID | Required assertion | Source and material scope |
|---|---|---|
| MR01 | Define the actual graph `(X, 1/X, Y, X*Y)` and its convex hull, and prove equivalence to finite probability representations with all coordinates and products matched. | Section 1 and the final paragraph of Section 2. Arbitrary finite leaf types, including the empty type; no representing law is assumed as an unexplained premise. |
| MR02 | Every original graph point and every hull point satisfies the six leaf McCormick inequalities and the reciprocal secant bound. | Equation (3), necessity. Convex combinations preserve each affine inequality. |
| MR03 | For a nonempty leaf type the leaf inequalities imply `a <= m <= b`; with no leaves include this condition explicitly, as the source requests. | Section 1, zero-leaf qualification. This does not assert that the reciprocal bounds alone cannot imply the same mean bounds. |
| MR04 | The function `C_*` is exactly the maximum of the two base lines and both lines for every leaf; each line is affine in `s`, and in the hull coordinates for fixed `s`. | Equation (1). Include repeated lines and the empty leaf type. |
| MR05 | Under the linear conditions, `C_*` is convex, continuous, piecewise affine, and has slopes in `[-1,0]`. | Section 2, least feasible call function. The slope statement needs an actual mathematical interpretation, not an unconstrained input field. |
| MR06 | Under the linear conditions, `C_*(s)=m-s` for `s <= a` and `C_*(s)=0` for `s >= b`. | Section 2 exterior-piece argument. Prove domination of both leaf lines, including endpoint equality cases. |

## Call functions and leaf realization

| ID | Required assertion | Source and material scope |
|---|---|---|
| MR07 | The call function of a probability distribution supported on `[a,b]` is convex, equals `m-s` to the left and zero to the right, and has the stated slope bounds. | First paragraph of Section 2. A finite-distribution specialization suffices for the finite hull argument; the note also states the general probability-distribution fact. |
| MR08 | A convex piecewise affine function with those exterior pieces is the call function of the finite law given by its upward slope jumps; the jumps are nonnegative, sum to one, have locations in `[a,b]`, and give mean `m`. | Converse in the first paragraph of Section 2. Derive the representation, rather than assuming that a proposed law has the desired call function. |
| MR09 | Every selection `0 <= theta <= 1` of mass `q` satisfies `E[X theta] <= q*s + C_mu(s)` for every real threshold `s`. | Equation (4), pointwise selection inequality. Include `q=0` and `q=1`. |
| MR10 | An upper-tail selection with fractional threshold-atom selection attains the infimum over all thresholds in (4). | Equation (4), attainment assertion. Existence of a suitable threshold and exact mass must be proved; assuming an optimal selection does not discharge this entry. |
| MR11 | The minimum selectable first moment is `m-U_mu(1-q)`, and every value between the minimum and maximum is attained by convex interpolation of selection functions. | Paragraph following (4). Include coincident extremes without dividing by their zero difference. |
| MR12 | For `q` in `[0,1]`, a leaf pair `(q,w)` is realizable on a fixed law if and only if both inequalities in (5) hold for every real `s`. | Equation (5). Necessity and sufficiency, including mass zero and mass one. |
| MR13 | Every finite family of individually admissible selections on the same law can be realized simultaneously by deterministic leaf values in `[0,1]`, preserving all moments. | Paragraph following (5). No independence assumption and no enumeration of all binary leaf patterns. |
| MR14 | Every law with the specified mean that realizes all leaves has `C_mu >= C_*` pointwise. | Section 2, least feasible call function. Establish the two base-line inequalities as well as the leaf-line inequalities. |
| MR15 | Under the linear bounds there exists a law `mu_*` with call function exactly `C_*`, mean `m`, and all prescribed leaf moments. | Section 2 construction of `mu_*`. Compose the envelope representation and leaf-realization results; do not assume the desired representing law. |
| MR16 | An upper envelope of `2n+2` affine functions has at most `2n+2` nonempty affine pieces, so `mu_*` has at most `2n+1` support points. | Section 2 support count. Count distinct positive-mass support locations, with ties, redundant lines, and endpoint jumps covered. |

## Reciprocal extrema and exact hull

| ID | Required assertion | Source and material scope |
|---|---|---|
| MR17 | The stated second-derivative call-function identity holds for a twice continuously differentiable function on `[a,b]` and every `X` in that interval. | Section 2 identity preceding (6). State the regularity and endpoint hypotheses precisely. |
| MR18 | Substituting `f(X)=1/X` gives the reciprocal expectation identity (6), including existence of the integrals and the expectation/integration interchange. | Equation (6). A finite-sum proof suffices for the finite hull theorem; distinguish it from the note's general-law identity. |
| MR19 | The formula (2) is well-defined and convex as a function of the hull coordinates; call-function domination implies the reciprocal lower bound `E[1/X] >= T_*`. | Section 1 description of `T_*` and Section 2 reciprocal minimum. The weight `2/s^3` is positive on `[a,b]`. |
| MR20 | The law `mu_*` attains reciprocal moment exactly `T_*`; it is feasible for all leaves. | Section 2 reciprocal minimum. The lower bound is attained in the actual graph hull. |
| MR21 | The endpoint law with mean `m` has nonnegative probabilities summing to one and reciprocal moment exactly `(a+b-m)/(a*b)`. | Section 2 reciprocal maximum. Include `m=a` and `m=b`. |
| MR22 | The endpoint law's call function dominates every supported law of mean `m`, hence dominates `C_*` and realizes every leaf satisfying the linear bounds. | Section 2 maximum argument. A reciprocal secant bound alone does not establish simultaneous leaf feasibility. |
| MR23 | Every reciprocal moment between the minimum and maximum is attained by mixing the two laws; its call function remains above `C_*`, and the leaves remain simultaneously realizable. | Section 2 final sufficiency argument. Treat coincident extrema separately. |
| MR24 | The constructed original-graph convex representation for every feasible point uses at most `2n+3` support points. | Section 2 final support count. Transfer the scalar-law support bound to actual graph points. |
| MR25 | Membership in the actual graph hull is equivalent to the linear inequalities and both reciprocal bounds (3), for every finite number of leaves. | Main theorem. Assemble both directions and the zero-leaf mean qualification. |

## Normalization and boundary variants

| ID | Required assertion | Source and material scope |
|---|---|---|
| MR26 | A fixed positive anchor product `X*y0=p` gives `t=y0/p`; the coordinate transformation preserves the graph and its convex hull. | Section 1 anchor normalization. Positivity of `p` and the common-factor interval are explicit; do not silently add restrictions on the anchor variable. |
| MR27 | Each nonfixed leaf box `[l_j,u_j]` is transformed by the displayed affine coordinate map, with an inverse map, and hull membership is preserved. | Section 1 box normalization. The transformed product coordinate is `(w_j-l_j*m)/(u_j-l_j)`, not `w_j/(u_j-l_j)`. |
| MR28 | Fixed leaves are equivalent to the linear equations `y_j=l_j` and `w_j=l_j*m` and can be deleted and restored without changing the remaining hull problem. | Section 1 fixed-leaf statement. Include a mixture of fixed and nonfixed leaves and the all-fixed case. |
| MR29 | When `a=b>0`, the hull is exactly the linear set with `m=a`, `t=1/a`, arbitrary leaf means in their boxes, and products `w_j=a*q_j` in normalized coordinates. | Section 1 fixed-common-factor statement. This boundary is separate from formulas dividing by `b-a`. |

## Rational construction, evaluation, and separation

| ID | Required assertion | Source and material scope |
|---|---|---|
| MR30 | For rational candidate data satisfying the linear bounds, a terminating algorithm constructs the exact upper envelope on `[a,b]`, including parallel-line elimination, ordering, and endpoint clipping. | Section 3 first paragraph. The correctness theorem must connect the algorithm's output to `C_*` on every interval. |
| MR31 | Sorting slopes and constructing the envelope take `O(n log n)` rational arithmetic operations and produce `O(n)` segments. | Section 3 first paragraph. State an operation-count model and prove the bound for the actual algorithm; the existing all-pair-intersections Python routine does not establish this claim. |
| MR32 | For each positive interval `[alpha,beta]`, integration of an active line gives exactly formula (7). | Section 3 displayed formula. Include a zero-length interval; endpoint reciprocals must be defined. |
| MR33 | Summing the interval formulas with the affine initial term evaluates `T_*` exactly using rational arithmetic; exact membership is decided by these quantities and the linear inequalities. | Section 3 evaluation. Completeness depends on a correctly constructed envelope, not a supplied list of guessed active lines. |
| MR34 | Envelope intersections, endpoints, and integrated coefficients have polynomial bit length, and total evaluation has polynomial bit complexity in the rational input encoding. | Section 3 bit-complexity paragraph. Account for rational arithmetic, intermediate sums and comparison costs. An arithmetic-operation bound alone is insufficient. |
| MR35 | For any fixed finite interval partition of `[a,b]` and any choice of one allowed line on each interval, the integrated expression `L` is affine in the hull coordinates and satisfies `L <= T_*` globally. | Section 3 separator proof and cut-family paragraph. The chosen interval boundaries are constants when the candidate coordinates vary. |
| MR36 | At the candidate that supplied the active envelope, that fixed-boundary affine expression equals `T_*`; its inequality therefore strictly separates a candidate below the lower bound. | Equations (7)–(8). Includes tied active lines and empty or degenerate segments. |
| MR37 | Violated leaf/mean inequalities and the reciprocal upper secant provide the other separating cuts, so the resulting rational separation oracle is exact and has polynomial bit complexity. | Section 3 complete oracle. Include the explicit mean bounds when there are no leaves and membership acceptance when no cut is violated. |
| MR38 | The family of all rational-partition integrated-line cuts is valid and complete for the lower hull bound. | Last paragraph of Section 3. Candidate-envelope selection proves completeness at rational candidates; if completeness is claimed for arbitrary real points, prove the needed rational-partition approximation or equivalent extension. No polynomial-size explicit formulation is asserted. |
| MR39 | For rational feasible data, slope-jump probabilities and locations, endpoint probabilities, and the reciprocal interpolation weight are rational and give the stated scalar moments. | Section 3 rational decomposition. Handle zero jumps and equal reciprocal extrema without invalid division. |
| MR40 | On the resulting finite rational support, lower/upper-tail selection and fractional boundary-atom selection produce rational leaf values; interpolation gives every prescribed rational `(q_j,w_j)`. | Section 3 rational decomposition. Include zero/full mass and coincident selectable first moments. |
| MR41 | The construction yields an explicit rational convex decomposition into at most `2n+3` original graph points, in polynomial bit complexity and with polynomial output bit length. | Section 3 rational decomposition. Count all leaf coordinates in the output and prove the construction's complexity, not only existence of a rational witness. |

## One-leaf specialization and exact example

| ID | Required assertion | Source and material scope |
|---|---|---|
| MR42 | With one leaf, the least feasible law is the two conditional-mean atoms at `w/q` and `(m-w)/(1-q)`, with the stated masses, and its call function is `C_*`. | Section 4 first paragraph. Omit zero-mass atoms and allow coincident conditional means. |
| MR43 | The one-leaf value is `q^2/w+(1-q)^2/(m-w)`, with the zero-mass convention justified, and the resulting hull description agrees with the existing two-SOC hull. | Section 4 formula and link to the small-block note. Distinguish Lean's total division convention from genuine positive denominators in nonzero-mass terms. |
| MR44 | For the displayed two-leaf example, the three specified locations and probabilities form a law of mean two, with reciprocal moment `31/50`, and its call function equals the full envelope. | Section 4 exact example. Prove the envelope identity and hence optimality; merely exhibiting a law of reciprocal moment `31/50` gives only an upper bound on the minimum. |
| MR45 | That law realizes both stated leaf pairs; the point with reciprocal coordinate `3/5` is outside the joint hull and lies below its minimum by exactly `1/50`. | Section 4 exact example. Construct or prove the required simultaneous selections. |
| MR46 | Both individual one-leaf hull constraints admit the same candidate, while the joint hull excludes it; the individual equality laws are incompatible and the full-envelope lower bound is strictly larger. | Section 4 last paragraph. Reuse existing individual memberships and joint cut where applicable; identify whether the separate equality-law statement is proved. |

## Existing coverage and nonmathematical boundaries

The existing [one-leaf coverage](../05-reciprocal-anchor/COVERAGE.md) proves
the one-leaf graph-hull equivalence, inverse-moment bounds, and its fixed-anchor
case. Its `Joint` and `Separator` modules establish the two individual
memberships and joint nonmembership used in MR46. Those results do not by
themselves establish the many-leaf envelope theorem, the exact example's
minimum, general leaf-box normalization, support counts, or any complexity
claim. Generalizing a finite-law statement does not verify execution of the
Python implementation.

| ID | Assertion outside the mathematical completion claim | Evidence and limitation |
|---|---|---|
| MS01 | The existing Python verification script implements its exact rational envelope and moment checks correctly. | Source review and focused execution can support behavior. Lean theorems require a proved refinement connection before they verify this executable. Its current envelope construction enumerates pairwise intersections. |
| MS02 | The script passed the stated 150 seeded comparisons against an independent shared-measure LP using floating-point HiGHS. | Historical test evidence and reproducible execution; this is not a continuous-support proof or a Lean theorem about HiGHS. |
| MS03 | The written theorem passed the stated author/root reviews; the construction has the recorded provenance and related literature. | Review records and literature sources. Lean does not establish review history, attribution, novelty, or priority. |

The note explicitly excludes adding product bounds or linking constraints
without further convexification. This restriction is part of the theorem's
scope; no result for those stronger graph sets is claimed. The cut-family
description asserts no polynomial-size explicit linear formulation.

Local validation must use targeted checks for this topic. Project-wide
verification belongs to CI; do not run it locally or inspect CI status or logs.
