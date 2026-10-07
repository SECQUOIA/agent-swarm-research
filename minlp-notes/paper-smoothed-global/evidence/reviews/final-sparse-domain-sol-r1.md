# Final integrated mathematical review: sparse and feasible-domain routes, r1

Reviewer: Sol. Date: 2026-10-06 UTC.

All manuscript locators in this report refer to the immutable directory
`evidence/snapshots/integrated-mathematical-draft-r1/`. Abbreviations `05`,
`06`, `C`, `D`, `02`, `03`, and `A` mean the corresponding section or
appendix files in that snapshot. Historical reports and author responses
were context, not substitutes for reading the proofs.

## Decision

The assigned mathematical block passes this review under its explicit
curvature, chart, and oracle premises and the classical theorems it cites.
I found no new mathematical blocker or unresolved S1–S5 defect. I verified
the actual proofs of the sparse mixed polynomial and quadratic results,
explicit and implicit graph results, actuator reduction, simplex theorem,
mixed-order theorem, and the new conditional-recourse count. General TU
rounding remains a preliminary lemma, not an optimization theorem.

This is approval of the mathematical proof chain in the assigned scope,
not final publication approval. Final primary-source identities, classical
theorem locators, companion metadata, and bibliography completeness remain
with Luna and the root. I checked the revised companion paragraph against
Luna's current preliminary evidence; I did not independently research its
sources. I did not review the other routes or the boundary appendices as
complete proofs.

## Snapshot integrity and review scope

The manifest was captured at `2026-10-06T03:49:31.635993+00:00` and describes
20 TeX files. Its SHA256 is
`c439935acba1b1adeb5d883e3718b1416f71ca45839ab672f5545060343d92cf`.
I computed SHA256 and line counts for all 20 listed files: every entry
matched. This is the requested frozen-corpus integrity check, not
project-wide verification.

| File | Lines | SHA256 |
| --- | ---: | --- |
| `sections/05-sparse.tex` | 1145 | `df3ef7c7f7c08d415044d9d93e3f9daa9b8a5d6c301954b950c3130c6718f047` |
| `sections/06-constraints.tex` | 818 | `9467eb72e20f355b3afb70d844bfedcf0a7fe52ba8f53d2483327162ad9db898` |
| `appendices/C-sparse.tex` | 278 | `a93e0493bd253e24e72b5fa1d903f360f8422a84222ec04d80eed069ca9b2974` |
| `appendices/D-constraints.tex` | 1080 | `c0b90de5054e469a278c2d09f560ce39a746c5b1025c79ecf4aee75ca0f4e66b` |
| `sections/02-model.tex` | 559 | `0a9267cd7a893497d212e5ccb0fbb6433b6428c4784793dd9fc79ec4f4e38a63` |
| `sections/03-counting.tex` | 754 | `9818728f37864c878ab2e7d0bb1690bb79e8d53f3a338e2f316e31787692b049` |
| `appendices/A-finite-noise.tex` | 822 | `4ff3fe30e76466dcc744389e88deaa9759fc19a2709c1104cba89612379c39cd` |

I read Sections 05/06 and Appendices C/D in full. The dependency review
covered model preprocessing, grid law, output and parameter contracts;
the point-growth and finite-tail statements; Appendix A's growth proof,
grid transfer, two-block section proof, active-root count, shared-root
construction and exact fallback. The Gaussian sampler and all other
routes are outside this verdict. The model's universal-resolution result
was read as an interface; its entire routewise proof was not re-audited.
The ordinary sparse/domain proofs use their own explicit schedules and do
not depend on that universalization.

Required context consulted: `BRIEF.md`, `independent-review-brief.md`,
`integration-contract.md`, `integration-decisions.md`, `notation.md`,
`reviews/root-integration-to-final-math.md`, the three earlier Sol sparse
reports, the Opus editorial interim findings and root disposition,
`reviews/opus-math-partial-r1.md`, both sparse author reports, and
`literature-preliminary.md`. The partial Opus record has no adjudicated
minor-gap list or final verdict; it is not treated as approval.

## Disposition of previous findings

| Finding | Status in the integrated snapshot | Actual locations |
| --- | --- | --- |
| S1: equality-budget multipliers | Resolved. Only active inequalities enter the simplex margin event. Equality-budget multipliers are unrestricted; their common value cancels in zero-coordinate derivative differences. The stopping proof's negative-anchor argument concerns inequality budgets only. | `06:637–658`; `D:522–528`, `D:570–585`, `D:594–625` |
| S2: coarse simplex vertices and fine cube indices | Resolved. Coarse grids and corners are original simplex vertices for every `h>=1`. Fine indices are `0,...,m-1`, excluding exterior cubes. The count has a separate coarse branch. | `06:609–623`; `D:388–395`, `D:399–435`, `D:449–453` |
| S3: empty/fixed block division | Resolved. Empty free-coordinate blocks are removed; an equality block with one free coordinate is fixed to its residual budget; forced endpoint blocks are substituted; tangent dimension zero returns before center formulas. Remaining width sums are positive. | `D:543–560` |
| S4: point outputs before GLS | Resolved for boxes, explicit graphs, implicit graphs, simplices and orders. A fixed retained implicit chart still refines its dependent roots and objective. | `05:1039–1043`; `C:180–190`; `D:74–76`, `D:301–309`, `D:669–671`, `D:1047–1049` |
| S5: ambient parent count | Resolved with `min{n,k^{D_g}}`; no false comparison of ambient parent count with retained dimension remains. | `D:45–53` |
| S5: irrational constant implicit roots | Resolved. Only explicit rational constants and rational singleton brackets are substituted; other constant implicit roots remain in the original rational chart/fallback formula. | `06:188–196`; `D:9–15` |
| S5: best incumbent and associated point | Resolved. Exact and certified incumbents initialize to infinity, keep the point associated with the best bound, and update before pruning. | `05:382–387`, `05:606–611`; `06:351–356`; `D:166–178` |
| S5: zero-dimensional stationary tuples | Resolved. The implicit, simplex and order counts explicitly use one empty tuple rather than invoking the positive-dimensional root lemma. | `D:238–241`, `D:615–618`, `D:990–993` |
| Early: Appendix D absent | Resolved. All required domain proofs are present and were read. | `D:9–1080` |
| Early: actuator curvature can be negative | Resolved by `L=max{1,L_q+Lambda G_2}`. This also bounds the initial-state curvature when `L_q` is negative. | `06:474–483`; `D:352–357` |
| Early: literal coefficient length `I+b` | Resolved by fixed polynomial coefficient-length and production-cost premises. Explicit substitution and actuator production prove both. | `06:78–83`, `06:295–300`, `06:485–489`; `D:45–53`, `D:358–361` |
| Early: shared-root fallback and output length | Resolved. The common-root conversion, designated-tuple selection and its base-only budget are now proved. Heights/work retain polynomial dependence on added bits and requested precision. | `02:328–332`, `02:370–375`; `03:539–598`; `A:439–562`, `A:632–654` |
| Early: all-fixed inputs | Resolved before maxima and schedule divisions. Graph point charts and fixed actuator trajectories are evaluated directly. | `05:61–68`, `05:968–986`; `06:193–196`, `06:450–454`; `D:347–350` |
| Early: continuous singleton-hull descriptor | Resolved in both local and common contracts. Original-bound gradient forcing and singleton fixing have separate soundness arguments. | `02:309–319`; `05:114–132`, `05:825–835` |
| Early: order transport does not satisfy box P1 | Resolved. The introduction and proof expressly use transport as a replacement, without claiming a fixed or exhausted outside fiber. | `06:24–32`, `06:745–757`; `D:753–807` |
| Early: blanket hardness/noise explanation | Resolved within this block by the specific worked NO-family witness and finite-law threshold probability, with no claim about every reduction. Verification of the boundary construction itself belongs to its assigned reviewer. | `05:1099–1111` |
| Editorial P2: deterministic companion and high moments | Resolved at the current preliminary source-evidence level. See the detailed check below; bibliography/source identities remain pending. | `05:694–746`, `05:1131–1145` |
| Integration B10: missing explicit bridge | Resolved by an actual oracle contract, deterministic pruning/witness proof and finite-law count. No efficient outside oracle is claimed. | `05:583–692`, `prop:sp:conditional` |

## Verified proof coverage

| Result or interface | Decision and exact proof locations |
| --- | --- |
| Mixed polynomial box theorem, `thm:sp:main` | Verified: setting `05:32–189`; grid/whitelist/DP/rounding/pruning `05:193–439`; count `05:443–547`; closure and stopping `05:754–889`; law, fallback and work `05:897–1025`; evaluation `C:186–222`. |
| Conditional-recourse count, `prop:sp:conditional` | Verified as a count under an assumed oracle, not an unconditional algorithm: `05:598–673`. |
| Nonsingular zeros, `lem:sp:bezout` | Application verified: `C:13–34`. It counts nonsingular isolated zeros only, including when other components are positive-dimensional. The refined Bezout citation remains subject to Luna's source check. |
| Convex-patch evaluator, `lem:sp:gls` | Verified: `C:61–178`, with point branches `C:180–184`. Approximate separation, erosion comparison, rational feasibility repair, and physical distance are all included. The GLS source statement is used as transcribed. |
| Quadratic/MIQP rational output, `cor:sp:qp` | Verified: `05:1071–1097`; `C:226–278`. The scope is mixed boxes, not arbitrary quadratic objectives on nonlinear graphs. |
| Uniform conditioned schedules, `lem:con:uniform` | Verified: `06:72–133`; coefficients and production cost may be `poly(I+b)`, while format counts and schedule factors remain base-only. |
| Expanded chart decomposition, `lem:con:expand` | Verified: `06:208–221`; `D:9–43`. Constraint scopes connect ancestor occurrence subtrees. Empty ancestor sets are harmless. |
| Explicit graphs, `thm:con:graph`(E) | Verified: `06:293–310`; `D:45–90`. Fixed depth/degree makes expanded lists polynomial and preserves conditional retained-noise independence. |
| Implicit chart roots and derivative oracle, `lem:con:chart` | Verified: `06:319–344`; `D:92–155`. Premises hold on the whole real retained hull and dependent brackets. |
| Implicit lower-cost DP and closure | Verified: `06:346–388`; `D:157–214`. Rational lower costs, feasible stored lift, witness tolerance `4E_j`, operator-norm Hessian error and conservative margins agree. |
| Implicit active-root tail, `lem:con:kkt` | Verified: `D:216–266`. The polynomial system's degree is bounded by `max{2,d,e}` and its Jacobian is nonsingular at a positive-growth optimizer. |
| Implicit graph law, exact lift and evaluation | Verified: `D:268–331`. Ordinary, point and fallback outputs meet the distinct feasible-lift/rational-approximation contracts. |
| Actuator theorem, `thm:con:actuator` | Verified: `06:426–513`; `D:335–384`. Full-hull invariance, adjoints, unary reduced terms, uniform bounds and trajectory precision are proved for arbitrary horizon. |
| Simplex rounding and count | Verified: `D:388–493`. Coarse and fine cases, common feasible rounding across all whitelists, face directions and finite atoms are handled. |
| Simplex closure and multiplier tail | Verified: `D:495–642`. Active inequalities only; rational strict centers after fixed-block elimination; weighted tangent metric; transformed-tuple counting rather than independence. |
| Simplex schedule and feasible evaluation | Verified: `D:644–698`. Zero tangent dimension, exact projection, objective gap and physical distance are included. |
| Order vertices, rounding and sharp count | Verified: `D:708–850`. Endpoint-preserving transport and disjoint direction supports give the sharper continuous-coordinate count. |
| Order exposure, weighted closure and finite tail | Verified: `D:852–1024`. Binary labels precede exposure; opposite faces are in the original fixed-binary slice; sum-fiber counting pays for correlated coefficients. |
| Order schedule and feasible evaluation | Verified: `D:1026–1080`. Propagation precedes fallback repair; point branch and physical metric are explicit. |
| General TU scope paragraph | Verified only for aligned continuous rounding and sound pruning: `06:789–806`. It does not supply general TU count, closure, margins or expected optimization work. |

## Re-derivations and boundary checks

### Sparse pruning, deterministic domination and work

At `05:333–371`, a non-grid coordinate has one containing interval;
a coordinate on a grid boundary remains fixed. One global independent
rounding therefore stays inside every chosen incident cell across all
bags, not merely one bag. Sequential Taylor bounds use the full continuous
hull, including between native integer labels, and give
`E_j=nLh_j^2/8`. With separator consistency, the two-pass DP computes one
globally feasible allowed-grid assignment. Missing separator entries have
infinite cost and outgoing sums are recomputed, avoiding infinity
subtraction (`05:290–318`).

Fixed-cell rounding gives `q_C-E_j<=F(x)`. The current grid contains a
point of value at most `f*+E_j`, so `f*<=U_j<=m_j<=f*+E_j`. A retained cell
has one complete allowed-grid witness of value at most `f*+2E_j`;
deleted points have value strictly above `U_j`. These statements remain
valid for ties and old incumbents outside the current physical domain
(`05:397–439`).

The outside domain in `V_beta` is the original product domain. Given
outside noise and a fixed full-grid tuple, a regular coordinate is confined
to an interval of length `L a_i+4E_j/a_i`, with `a_i>=h_j`; at most three
clipped/boundary nodes are exceptional. Summing the product of interval
probabilities gives
`prod_i[4+(1+n/2)L w_i/(2 sigma)]`. The atomic term is bounded by
`w_i/(a_i M)<=2^j/M<=1`. Every adaptive retained cell is charged to this
deterministic full-grid count on every draw (`05:498–547`).

Generating children, corner rows, dictionary messages and hulls costs a
constant to the power `p` times the sum of retained list sizes, with a
polynomial bit factor. No product of random neighboring tables is needed.
Taking first moments over all base-selected levels proves the displayed
expectation (`05:997–1023`).

### Closure, finite law and fallback

All hulls contain every optimizer. Gradient signs use original continuous
bounds; singleton fixing separately uses containment; native integer
coordinates must all be fixed before a continuous patch is accepted
(`05:794–836`). Hessian variation is at most `kappa_3 r^P` in spectral norm
by symmetric row sums. The matrix certificate therefore proves curvature
on the entire patch, not only at its midpoint.

The witness gap and point growth localize retained projections within
`A h_j`, where `A=2+nL/g_0`. Under active-bound margins and the stated cap,
integer labels become exact, active bounds are removed, and two-sided
growth on the remaining interior directions yields Hessian at least
`2g_0 I`. The certificate has a positive slack (`05:853–883`). There is
no premise on the distance to inactive bounds.

Every schedule selects `B` first, then `rho,g_0,tau,J`, and finally `M`.
The growth and margin events each cost at most `rho=1/(4B)`; late fallback
costs probability at most `1/(2B)`. Degree and atom-format counts have
polynomial logarithms even for binary-encoded native ranges. Sampled
coefficient height enters the separate polynomial factor, never `B` or
the base-selected law (`05:897–960`; `03:416–507`; `A:356–435`).

I checked the shared-root construction used by these callers. A separating
integer linear form distinguishes every Cartesian scalar-root tuple;
the derivative of the multiplication-matrix characteristic polynomial
recovers each coordinate modulo that polynomial; refined scalar isolators
select the designated compatible tuple. Conversion is polynomial in the
product of scalar degrees, whose logarithm is polynomial in base input
length. Thus it fits in an enlarged base-only `B`, with fixed polynomial
dependence on coefficient height and requested precision
(`A:439–562`, `A:632–654`). Every-draw ties, singular stationary sets and
continua of minimizers are handled by the canonical singleton formulas,
not a nonsingularity premise (`A:565–630`).

### B10: actual oracle and finite expected count

At `05:603–611`, the oracle returns both a certified rational interval for
the true conditional minimum and an actual feasible completion whose
value is at most its upper endpoint. Merely returning a lower number or
separate incompatible bag witnesses would not meet this interface.

The conditional value is upper coordinate semiconcave on the full hull:
subtracting `L theta^2/2` leaves a minimum of concave functions over the
fixed original outside domain. Bag-only mean-preserving rounding gives a
queried corner with `W_beta(v)<=f*+e_j`. Hence
`f*<=U_j<=f*+e_j+eta_j`. The lower endpoint of a retained corner is at most
`U_j+e_j`; its returned feasible completion has value at most
`f*+2(e_j+eta_j)` (`05:633–660`). This proves the claimed witness factor.

For counting, replace any draw-dependent error by
`delta=2(1+a)e_j`. The comparison interval is then determined by outside
noise and the fixed tuple, not by queried errors or retention. Its length
is at most `L a_i(1+(1+a)p/2)`, and the same clipped-node and atomic-term
sum gives exactly `eq:sp:conditional` (`05:662–672`). The proposition
does not claim an efficient outside solver or full width-FPT algorithm
(`05:594–596`, `05:675–692`).

### Graphs and actuator lifting

For explicit charts, bounded depth and fixed degrees give polynomial
expanded monomial lists. The ancestor-union decomposition is connected
because each constraint scope contains a parent and its child. Conditioning
on dependent noise leaves independent retained ambient coefficients; all
curvature and fallback factors are chosen uniformly first. Algebraic
constants are not inserted into rational fallback input (`D:9–90`).

For implicit charts, monotonicity and endpoint signs on the whole hull
give one root per bracket. Local implicit-function extensions cover hull
boundaries. The first three derivative bounds and rational expressions for
value/gradient/Hessian have denominators bounded below by powers of the
given `mu_j`; rational bisection and explicit derivative bounds give the
claimed polynomial-bit oracle (`D:92–155`). Entry precision `epsilon_H/n`
and symmetrization give the needed operator error (`06:379–386`).

Summed lower-cost error is `D_j=E_j`. A lower-cost grid minimizer supplies
a feasible exact implicit lift of value at most its certified upper
bound, while a retained-cell witness has gap at most `4E_j`. This accounts
for the factor `1+n` and for the larger localization radius; the closure
test pays for both oracle errors (`D:157–214`). The implicit KKT system has
`k+2m` equations of degree at most `max{2,d,e}` independent of the tested
active coefficient. Invertible diagonal `q_y` gives full constraint rank,
and positive reduced tangent Hessian makes the bordered Jacobian
invertible. Thus the finite active-root tail counts the actual optimizer
even if other stationary components are singular (`D:225–266`).

Implicit point patches still refine roots and the objective. On a
positive-dimensional patch, value tolerance pays for `K_psi` and the
strong-convexity conversion; root brackets pay separately for ambient
coordinate error. On fallback draws, clipped retained coordinates preserve
native labels, the reduced gradient bound controls the feasible lift's
objective gap, and root refinement supplies the rational ambient
approximation. The exact lift satisfies all graph equations; the separate
rational ambient approximation is not claimed feasible (`D:301–330`).

For actuators, full-hull invariance makes every free point feasible.
Backward adjoints produce exactly one initial-state linear term and unary
control terms, preserving free-variable bags for every horizon. The
corrected positive `L` and derivative row-sum bounds are uniform in state
noise; affine recursion adds bit lengths. The trajectory map has Lipschitz
bound `1+(1+G_1)/(1-a)`, obtained from bounded convolution row and column
sums. Extra encoded precision therefore yields the stated physical
trajectory accuracy, with an exactly rational feasible trajectory
(`06:456–489`; `D:335–384`).

### Simplex and order geometry

Fine simplex cells are integral cube-budget polytopes after scaling.
Their convex combinations preserve means and fix grid-boundary
coordinates across every incident cell. Independent block rounding uses
the block Hessian bound, not diagonal bounds alone (`D:408–435`). Slack
faces use `e_i`; tight faces use `e_i-e_anchor`, of squared norm two.
Positive support and slack are grid multiples, so both comparison signs
are feasible. Conditioning on anchors leaves independent distinct tested
coefficients; relative-interior face counts cancel the powers of `h`.
Coarse vertex bounds and corner incidence finish the count (`D:449–493`).

Simplex margin counting does not assume independent transformed noise.
The map from original coefficients to tangent differences and undifferenced
normal coefficients is injective. Enumerating at most
`(2M-1)^k M^(n-k-1)` fixed transformed tuples and then the normal interval
gives `2^k D^k(tau/sigma+1/M)`. Only active inequalities enter the union.
The repaired fixed-block center has positive remaining width sums, and
the Hessian test uses `Z^T Z`, preserving physical curvature
(`D:543–642`). Blockwise Euclidean projection is rational and nonexpansive,
so ordinary and fallback evaluations are feasible and control physical
distance and value gap (`D:669–697`).

Order rounding uses one common monotone threshold, fixes binary labels
and grid nodes, and has total variance at most `n_c h^2/4`; it needs the
full Hessian bound on the cube. Conditional transport fixes endpoints and
all binary values, is affine in the target face tuple, and moves each
continuous coordinate at rate in `[0,1]` along a face direction. It provides
an attaining upper support, not equality of fibers. The comparison
interval length is `3 n_c bar L h/2`. Disjoint direction supports permit
independent tested coefficients after conditioning. Summing
`binom(c+1,k+1) A^k/k!` gives
`c!(c+1)[2+3 n_c bar L/(4 sigma)]^c`, with the separate binary-row factor.
This verifies the sharper mixed count and its continuous specialization
(`D:721–850`; `06:715–730`).

Binary hulls are fixed before any exposure test. In the original fixed
slice, a true gradient exposes a face containing an optimizer. If a
proposed equality fails, that face has a zero-one vertex in the opposite
face, so its computed gap cannot exceed `n_c kappa_2 r`. The gap is
`n_c`-Lipschitz, rather than paying twice that factor, because the
comparison uses differences of zero-one vertices (`D:852–894`). For an
edge margin, varying `gamma_i=t, gamma_l=s-t` leaves face stationarity
unchanged at fixed `s`, and the exposure gap is affine with slope minus
one on the optimizer event. Summing over at most `2M-1` fibers gives the
atomic term `2/M` without a false conditional independence assertion
(`D:986–1024`).

Merging, cycle contraction, bound propagation and singleton fixing
preserve containment. With strict propagated intervals and an acyclic
remaining graph, a finite average of feasible points strict for each
remaining row gives an interior point. Disjoint copy columns make
physical infinity distances equal to block infinity distances and require
the weighted curvature matrix `D^T D`; the stopping and evaluation proofs
retain that metric. Fallback propagation prevents a repaired predecessor
from changing a binary zero (`D:896–970`, `D:1047–1080`).

### Convex evaluation and source comparison

The GLS proof constructs a capped epigraph with a known inner ball.
Approximate gradients pay for their error over the entire affine domain.
Weak optimization compares with an eroded body; moving a true optimizer
toward the known ball gives an explicit feasible erosion competitor.
The repaired rational point has objective upper error controlled in the
chosen norm, and a fresh interval gives total gap at most `eta`.
Strong convexity on physical tangent directions then gives distance
`sqrt(2 eta/g)`, including boundary minimizers (`C:96–172`). The simplex
and order applications supply actual rational repair maps and radii; no
point patch is sent to this positive-dimensional interface.

The root's Section 05 update agrees with the latest preliminary Luna
comparison: Euclidean `kappa` and weighted `bar-kappa` are distinct,
point growth implies `bar-kappa<=kappa`, the stated approximation work has
the explicit function `f`, the condition parameter is not supplied to the
algorithm, and exact output has separate point-growth/uniqueness premises.
The uniform-grid limitation and the rETH statement are scoped to the
specified filtering/product-time models; no matching `p/2` lower exponent
or general width lower bound is claimed (`05:694–721`). This integrated
passage supersedes the sparse final author's conservative single-parameter
handoff, as the root's integration record expressly states.

For the moment paragraph, integrate
`Pr(Z>t)<=A_0/t+epsilon_M` using
`E min{K,Z^r}=integral_0^K Pr(Z^r>u) du`. The range below one contributes
at most one; above one the bound contributes
`r A_0/(r-1)(K^(1-1/r)-1)+epsilon_M(K-1)`, bounded by the displayed
formula with `epsilon_M K`. This includes ties and finite atoms. It says
the linear tail alone is insufficient for high moments; it does not infer
an impossibility theorem for another algorithm (`05:723–746`).

## Coverage and source supersession

The source-development map in the prior sparse author report remains
coherent after actual proof review. The mixed polynomial theorem contains
the continuous and mixed quadratic bag routes; the rational specialization
retains their distinct output claim. Appendix A's canonical shared-root
fallback is the common proof interface; the older constructive box
fallback is an alternative development, not a missing second constrained
fallback. The graph oracle, uniform conditioning, simplex and actuator
notes are covered by the proved interfaces above. The mixed-order
transport count supersedes the earlier continuous chamber count and
specializes directly to continuous orders. The original order face-closure
development is retained through exposure and the weighted metric. B10 now
has a proved statement; global/local-error barriers remain narrowly
described comparisons with proofs assigned to the boundary block.

At `06:789–806`, the TU statement assumes continuous `[0,1]^n`, integral
TU `A`, integral `b`, and aligned dyadic cells. Appending cube bounds
preserves TU; `b/h-Ak` is integral; feasible cell vertices are cube corners.
Their convex combination preserves means and boundary coordinates,
allowing a global full-Hessian rounding allowance and sound bag pruning.
This gives no unrestricted expected-time TU optimizer, no general
finite-tail/closure theorem, and no extension to arbitrary unfixed native
integer ranges or arbitrary nonaligned rational right-hand sides.

## Checks actually performed and remaining limits

Read-only commands used `cat`, scoped `rg --files`/`rg -n`, and
`nl -ba ... | sed -n ...p` on the assigned snapshot and required evidence.
A short Python script loaded the frozen manifest, computed SHA256 and
line counts for its 20 files, and reported zero mismatches. The
inequalities, root-system dimensions, probability constants, physical
metrics and precision allowances above were rederived analytically.
The final report check verified its final newline, absence of trailing
whitespace, and unchanged snapshot hashes. Only this review report was
written.

No optimization experiment, saved diagnostic, literature search, delegation,
manuscript edit, TeX build, project-wide check, CI inspection, commit or
publication was performed. Final literature attribution and bibliography
completion remain unverified here. Those limits do not conceal a known
mathematical defect in the assigned proof block.
