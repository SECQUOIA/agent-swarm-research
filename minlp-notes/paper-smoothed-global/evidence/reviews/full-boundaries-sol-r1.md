# Independent full front/boundary review, r1

Reviewed 2026-10-05 local time (completion checks on 2026-10-06 UTC).
The reviewed artifact is the immutable
`evidence/snapshots/front-boundaries-r1/`, not the active r2 author files.
All seven files match the bytes and SHA-256 hashes in its manifest.

**Decision:** the main boundary constructions pass this proof review. I found
no new defect that defeats the subject, the direct Square Root Sum reduction,
the PosSLP reduction, or either ambient-count construction. The frozen scope
is not submission ready: the general amplifier lemma has a false literal
statement without a positive modulus, the uniform-resolution proof misstates
its format bound, and several front-matter sentences extend restrictions or
necessity claims beyond their proofs. These are local repairs. The actual
positive-modulus amplifier instances are sound.

This is separate from `early-boundaries-sol-r1.md`. I rederived the actual
r1 arguments, including the newly integrated direct width-two Square Root
Sum proof and quantitative conditional-recourse bridge. I read the brief,
independent-review brief, previous review and relevant coverage-draft rows,
root model/introduction findings, current integration decisions/contract,
the universal-law report, and the front-r1 author response. The accepted
interface corrections still visible in the frozen source are separated
below from new findings. Existing reviews and companion proofs were
context, not a substitute for checking this manuscript.

**Location convention**

S0 = `sections/00-abstract.tex` (30 lines); S1 =
`sections/01-introduction.tex` (426); S2 =
`sections/02-model.tex` (545); S9 =
`sections/09-boundaries.tex` (845); S10 =
`sections/10-discussion.tex` (149); G =
`appendices/G-boundaries.tex` (480). All these paths and line numbers refer
to `evidence/snapshots/front-boundaries-r1/`.

## New findings and newly exposed wording errors

1. **Medium; false general lemma, simple repair.**
   `lem:lim:amplifier`, G:211–222, does not assume `mu_0>0`.
   The two unique base minima and a lower Hessian bound `mu_0 I` do not
   imply it. Take boxes with only the activation coordinates,
   `H_+=(theta_+-1)^2`, `H_-=theta_-^2`, and `mu_0=0`.
   Each base minimum is unique and exactly one amplitude is positive,
   but `eta=0` makes the combined objective independent of `y`.
   Every `y in [0,1]` is optimal, contradicting the claimed uniqueness
   and designated coordinate. Add the explicit hypothesis `mu_0>0`.
   No proof change is needed. The applications at G:314 and G:415 use
   `mu_0=3/32` and `3/4`, respectively, so this does not invalidate
   `thm:lim:posslp`.

2. **Medium; wrong proof premise, supported theorem after repair.**
   In the proof of `prop:model:uniform`, S2:203–206 says that the
   numbers of variables and atoms and the degrees are bounded by fixed
   polynomials in `I`. The atom count of a native-label disjunction can
   be exponential in `I`. The effective algebraic degree/format of a
   fallback proof can also be exponential; it is its logarithm that
   receives the base polynomial bound. For example, a single native
   interval `[0,2^r]` has a description of length `O(r)` and
   `2^r+1` label atoms.
   Use the actual routewise format argument:
   dimensions are polynomially bounded, `log(s+1)<=poly_d(I)` for
   the explicitly bounded atom universe, and the logarithms of the
   relevant effective degree/format multipliers are polynomial.
   Separate those base multipliers from the polynomial dependence of
   coefficient height and fallback work on added sampled bits.
   This is the argument in the universal-law report and the shared
   finite-tail/fallback interfaces, and it supports the proposition.
   Make `P,A,D` integer-valued positive envelopes so the displayed
   resolutions are permitted power-of-two laws.

3. **Medium; overstatement of a mechanism limitation.**
   S10:110–115 says the width and local-allowance barriers show that an
   arbitrary width-FPT algorithm “needs certified conditional values.”
   They prove that the specified global-error retention rule has an
   unavoidable width-dependent exponent and that a naive bag-local
   substitution is unsound. They do not prove that every different
   algorithm must use this conditional-value interface.
   Replace the necessity claim with: “Certified conditional values are
   one sufficient way to remove the ambient dimension from the count
   for this search; current grid min-marginals do not supply them.”
   Keep the general width-FPT question open. S9:350–360 already makes
   the sufficient-interface scope correctly.

4. **Medium; structural restriction applied to the wrong consequence.**
   S1:336–340 says both Square Root Sum and PosSLP have the point
   consequence “even when the residual problems have treewidth two and
   bounded coefficients.” The corresponding row of
   `tab:lim:summary`, S9:44–46, has the same ambiguity.
   Only `thm:lim:posslp`(a) proves those restrictions, for Square Root
   Sum. Part (b) has neither restriction, as S9:762–764 itself explains.
   Split the sentences/row or say that the restricted consequence is for
   Square Root Sum. This is an existing integration decision whose
   violation is newly visible in the finished front matter, not a new
   failure of the reduction.

5. **Low; incorrect description of the cited threshold construction.**
   `rem:lim:dk`, S9:597–600, calls the nonnegative box quadratic a
   sum of squared residuals of binary indicators and recurrences.
   The binary-enforcement terms must be described as binary penalties
   such as `b(1-b)`, together with squared affine recurrence residuals.
   They are nonnegative on the unit box but are not squares of affine
   residuals. A sum consisting only of such squares would be a convex
   quadratic; its zero question on a box is linear feasibility and could
   not furnish the stated nonconvex hardness construction.
   Change this to “a sum of nonnegative binary penalties and squared
   recurrence residuals.” The local already-read mathematical note uses
   that distinction. Luna must still verify the exact published
   construction and source locator. The displayed witness gap and
   threshold calculation are not affected by this wording repair.

Items 1–4 and the aligned-calibration reminder below were sent promptly
to the root for r2 integration. There is no major new proof blocker.

## Accepted interface corrections still requiring final verification

These are not counted as new mathematical findings.

- **Aligned calibration remains too broad.** S2:467–469 correctly gives
  the aligned perturbation width using
  `sum_i omega_X(T_{i.})`, but S2:477–489 again gives
  `sigma=epsilon/(2 sum_i w_i)` as the general small-noise recipe.
  The author response says this has been fixed; the frozen paragraph
  still needs an explicit model-specific width quantity.
  Write `W_noise=sum_{perturbed original i}w_i` for ambient/core box
  noise and `W_noise=sum_i omega_X(T_{i.})` for aligned noise, with
  row-specific scales when applicable. Use that quantity in the grid
  recipe and Gaussian support condition.

  This is not merely a preference for a sharper bound. For
  `T=H_16/4`, where `H_16` is a Hadamard matrix whose first column
  is all ones, `TT^T=I` and `||T||=1`. An allowed aligned draw with
  every `xi_i=sigma` has `gamma_1=4sigma`.
  On a box with one width 1 and fifteen widths `delta=1/1000`,
  the original-width recipe underestimates the maximum perturbation
  width. For a concrete ordinary rational instance, take
  `F_0=-3 epsilon x_1/2-tau sum_j x_j^2`, `tau=epsilon/100`.
  It has sixteen negative directions and admits the stated normalized
  factor with convexifier scale `2tau`.
  The recipe gives `sigma=epsilon/[2(1+15delta)]`; on this draw
  `gamma_1=2epsilon/(1+15delta)`.
  The sampled first-coordinate derivative is positive throughout
  `[0,1]`, so an exact sampled optimizer has `x_1=0`, whereas the
  original optimizer has `x_1=1`. Its original gap is at least
  `3epsilon/2+tau>epsilon`.
  Thus the unqualified recipe fails even for a normalized factor and
  an all-draw exact sampled solve.

- **Output and fixed-feasibility scope.** S1:194–195 still says every
  quadratic output is rational, contrary to the implicit graph example
  with `y^2=2`; scope it to the proved rational polyhedral/box quadratic
  classes. S1:260–264 states literal search-independent outside
  feasibility as a common premise of all three routes; graph/chart and
  order transport use proved replacement invariants. Both corrections
  are already in the integration contract. The graph row at S1:164–166
  should distinguish charted output from an original-coordinate
  implicit box patch.

- **Original approximation scope and fallback exceptions.**
  S1:313–319 and S2:490–499 now preserve the other numerical factors
  and exclude strong-noise calibration; this is a real improvement.
  S10:16–25 still introduces prescribed-accuracy approximation without
  the small-noise qualification. Add it there. S0:21–23 and S10:75–77
  describe exact fallback as the common treatment without the lattice
  and strong-field exceptions that S2:301–306 and S1:264–269 correctly
  state. Keep the exception consistent across the front matter.

- **Literature identity and contribution scope.** S1:401–413 now names
  the three companions and acknowledges reproduced constructions;
  G:179–182 and S9:758–764 explicitly acknowledge the exact-arithmetic
  overlap. This repairs the earlier unnamed-companion problem.
  The exact public sources, primary theorem locators, and O1–O8
  comparisons remain Luna's responsibility. I make no approval of
  publication priority or of the cited DK/genericity/PosSLP-to-SRS
  literature identities.

## Appendix G: complete mathematical proof coverage

### Sign test and amplifier

**Sign test, `lem:lim:signs`, G:184–209: passes.**
The block-diagonal Hessian of `Phi(z)+theta^2` is at least
`kappa I` because `0<kappa<=1`. The off-diagonal bilinear block has
operator norm exactly `epsilon ||grad zeta||<=kappa/4`.
Thus `H''>=3kappa I/4`. On the face `theta=0`, only the unique
base minimizer can minimize. At that point the base first-order condition
continues to hold even if it lies on a box boundary; the remaining
one-sided derivative is `epsilon zeta(z^0)`.
Its nonnegative sign certifies the whole-box minimum, while its negative
sign supplies a feasible descent direction. No interiority of the base
optimizer is assumed. This proves the activation equivalence.

**Amplifier, `lem:lim:amplifier`, G:211–245: passes after item 1.**
I rederived the displayed Hessian identity:
`2(theta varsigma+2(y-c)pi)^2-6(y-c)^2pi^2`.
On the stated box each negative contribution is at least
`-6eta pi^2=-mu_0 pi^2/2`.
The base curvature therefore leaves at least
`mu_0 ||base direction||^2/2`, plus nonnegative squares.
There is no division by an activation amplitude, so convexity holds also
on their zero face. Nonnegativity of the amplifier bounds the objective
below by the sum of base minima; the appropriate endpoint attains this
bound. Every optimizer must minimize both bases and make the amplifier
zero, which fixes all coordinates and its endpoint. This proves uniqueness
without asserting a uniform modulus in the designated coordinate.

### Direct Square Root Sum construction

**Averaging tree, `lem:lim:tree`, G:247–289: passes.**
The normalization uses only integer square roots/powers of two of
polynomial bit length. Each leaf uniquely minimizes
`u_i^3/3-c_i u_i` at `sqrt(c_i) in [1,2)`, and all internal residuals
can simultaneously be set to zero. The root equals
`sum_i sqrt(a_i)/(KR)`, including padded zero leaves.

The dimension-independent Hessian bound is valid. In the full direction
matrix `P`, distinct internal rows have disjoint supports because a
variable has only one parent. Leaf rows are zero. Thus
`PP^T` is diagonal with entries at most `1/2`;
`||P||<=1/sqrt(2)<3/4`.
The leaf diagonal curvature is at least 2 and each residual square
contributes twice its squared linear directional residual. Therefore
`d^T F_tree'' d>=2||(I-P)d||^2>=2(1-1/sqrt(2))^2||d||^2>=||d||^2/8`.
The last inequality also follows directly from `1/sqrt(2)<3/4`.
No depth-dependent condition number is hidden here.
The internal-variable/child bags cover each factor, and a variable occurs
only in its own and its parent's adjacent bags. For a real leaf its
parent bag also covers the unary leaf factor; the padded slots create no
missing variables.

**Integral trace, `lem:lim:trace`, G:291–305: passes.**
Every nonsquare positive radicand yields a quadratic subfield with zero
trace of its square root; trace transitivity in the common multiquadratic
field preserves zero. Square radicands have rational integer roots and
full field trace. An integral sum must therefore equal the contribution
of the square radicands alone. Positivity forces the nonsquare contribution
to be empty. Constructing that potentially huge field is unnecessary:
the algorithm tests the individual radicands using integer square roots.

**Part (a), G:307–333 / S9:725–732: passes.**
The cases `B<0`, all-square inputs, and `B>=2KR` are handled by
polynomial integer arithmetic. Otherwise `b in [0,2)` and the trace
lemma guarantees `s^0!=b`. Opposite affine tests have gradient norm one.
With `kappa=1/8`, the sign-test modulus is `3/32`;
the amplifier uses `mu_0=3/32`, hence `eta=1/128`.
Exactly one amplitude is positive and the unique designated coordinate
encodes the strict comparison. A no/equality answer is returned directly
when preprocessing finds equality; no equality is silently mapped to an
undefined amplified output.

I checked the changed constants against the structural conclusion rather
than inheriting the companion's smaller amplifier constant.
Before unit-box rescaling the tree leaf diagonal is at most
`4+1/2=9/2`, an internal diagonal is at most `2+1/2=5/2`,
the activation diagonal is at most `2+2eta=129/64`, and the designated
diagonal is at most `4eta=1/32`. All are at most 5.
Every interval has width at most 2, so the diagonal after affine rescaling
is multiplied by at most 4 and is at most 20. Convexity is preserved by
this invertible diagonal affine map.

The two root/activation bags and the two activation/designated bags form
one chain connecting the disjoint averaging trees. The designated variable
occurs in two adjacent bags; all others retain connected occurrences.
Every bag has at most three variables, so the expanded interaction graph
has treewidth at most two.
After rescaling, each constant-degree factor has a constant-size expansion
with bounded coefficient magnitudes. Every variable belongs to at most
four such factors (in fact the construction usually gives fewer), so a
nonconstant monomial can receive only a constant number of contributions.
This justifies bounded expanded nonconstant coefficients, not merely
bounded factor coefficients. The accumulated constant term is allowed to
grow and can be deleted. The normalizations have polynomial bit length,
the tree has `O(n)` nodes, and the total explicit encoding is polynomial.

### PosSLP construction

**Pairs, `lem:lim:pairs`, G:342–361: passes.**
Positivity of the denominators, the exact integer ratio, and the box bound
are all inductive. Addition/subtraction numerator magnitude is at most
`1/32`; multiplication gives at most `1/64`.
Repeated operands do not change these bounds.
The final `t=v_s(2A-1)/4` is nonzero for every integer output, including
zero and negative outputs, and has magnitude at most `3/16`.
Its sign correctly tests `A>0`. The potentially enormous exact rational
pair values are proof witnesses, not numbers materialized by the reduction.

**Uniform local gate bounds, G:363–379: pass.**
For distinct operands the four gradient contributions of a numerator
rule are at most `1/16` each; its Hessian rows have at most two entries
of magnitude `1/4`. Identical operands give either cancellation, a
bilinear coefficient `1/2`, or a square with second derivative
`1/2`; their gradient sum remains at most `1/4` on the entire box.
The final affine rule has gradient sum `3/4`.
Thus the displayed magnitude, gradient-one-norm, and Hessian-two-norm
bounds hold uniformly even at assignments that do not satisfy the rules.
Every rule depends only on preceding coordinates.

**Weighted Hessian, `lem:lim:gates`, G:381–411: passes.**
With weights `a_i=64^(N-i)`, conjugation by their square-root diagonal
gives `Ehat_ij=8^(j-i)L_ij`.
Row absolute sum is at most `1/8`; column absolute sum is at most
`sum_{l>=1}8^(-l)=1/7`. Hence `||Ehat||_2<1/4`, and the positive
residual Hessian term is at least `9||Dh||^2/8`.
Because `|rho_i|<=1/2` and the nonlinear rule uses only earlier
coordinates, the negative term is bounded below by
`-sum_i a_i ||h_<i||^2`.
Interchanging the sums and using the geometric weight ratio gives
`sum_{i>j}a_i<=a_j/63`.
The total lower coefficient is `9/8-1/63=559/504>1`.
Since every weight is at least one, `G''>=I`.
This is a full-box estimate, not just a Hessian estimate on the exact
gate trajectory. Triangularity gives one zero-residual assignment; its
box feasibility follows from the pair bounds, and it uniquely minimizes
the nonnegative objective.

**Part (b), G:413–421 / S9:733–736: passes.**
The sign-test choice `kappa=1` yields modulus `3/4`; the amplifier
uses `eta=1/16`. Nonzero `t` guarantees exactly one positive amplitude
and a unique 0/1 designated coordinate with the required zero-output
convention. Each squared residual has a constant-size degree-four
expansion and each weight has `O(N)` bits, so there are `O(N)`
written monomials/factors and polynomial total coefficient length.
No bound on treewidth or coefficient magnitudes follows or is needed.

**Part (c), G:423–437 / S9:737–754: passes.**
Completing the separate core square gives
`v_gamma=(1-gamma)/2 in [1/4,3/4]`, projected growth one and curvature 2.
The residual problem is unchanged on every draw.
Euclidean distance at most `1/4` implies a designated coordinate
separated from `1/2`; no exact comparison of a tiny activation or an
irrational value is needed. The construction, law computation, sampling,
optimizer construction and requested evaluation are included in the
hypothesized expected polynomial total work. The resulting decision is
always correct. The deterministic conclusion applies directly to the
residual polynomial. The direct SRS construction suffices independently
of the cited PosSLP-oracle relation; Luna owns verification of that extra
literature consequence. This is a conditional arithmetic implication,
not an established NP-hardness result or separation from P/ZPP.

### Ambient barrier and boundary flow

**Ambient block construction, G:7–81: passes.**
The `(u,q/sqrt(2))` matrices have the claimed eigenvalues and determinants.
The convexified determinant is `7alpha^2/8>0`; the original has one
negative eigenvalue per block. The factor rows are exactly rational
orthonormal. The two simplex masses realize every projected
`y in [-4,4]`; the thin signed coordinate realizes every
`z in [-m^(-3),m^(-3)]`.
Minimizing residual noise on each simplex gives the coefficients
`S-xi` and `t`. Completing the auxiliary square gives exactly
`a+xi/alpha-y` and the constant offset in G:74–75.
The projected two-variable inner Hessian is
`alpha[[1,c],[c,1]]`, positive definite. Thus its unique projected
optimizer justifies Danskin differentiation even when the simplex
minimizer itself is tied under a finite law.

**Good event and flatness, G:83–130: pass.**
The finite endpoint-grid count gives
`pi>=(2/n)(1-1/M)>=19/(10n)` for `M>=32`.
The two disjoint minimum events are independent; `xi` is not assumed
independent of either. Their lower probabilities and the Chebyshev loss
give `41/160>1/4`. The variance formula
`(M+1)/(3(M-1))<=3/8` is valid at every allowed `M`.
On this event `|S|<=2/m`, `|t|<=1`, and `|xi|<=2`.
The unconstrained y-minimum stays strictly inside its bounds for
`|a|<=3/2`; hence `|V'(a)|<3/m`.
For `|a|<=1`, the displayed feasible witness gives an upper value
`6/m`, while the global lower bound for G gives the gap strictly
below `15/m`. These estimates use `1<=alpha<=m`, valid for both
choices in the theorem.

**Product counts and complexity conclusion, G:132–175 /
S9:392–438: pass.**
The independent block event has probability greater than `4^(-k)`.
At the first mesh range, `2E_h>=16k/m`, exceeding the witness gap.
The node count `2/h-1>=sqrt(alpha m)/16` is valid for
`alpha m>=256`. At the second range, neighbors stay in the
differentiability interval and `3h/m<=alpha h^2/4<=2E_h`;
the node count is at least `alpha m/32`.
This gives precisely the constants 64 and 128 after multiplying by
the event probability.
For `alpha=1` all quantities in R are fixed while
`I<=C N^2 log N`. Fixing `k>8c` defeats any `f(k,R)I^c`
bound on either count.

The proof is honest that these are full-grid count surrogates, not
algorithm-work lower bounds. The auxiliary boxes contain the stated
central intervals. I also checked the caller's terminal mesh in the
immutable complete-proof r1 quadratic schedule: it is at most
`1/[2B N k K(alpha+Theta)]`, hence below the smaller relevant
`16/(alpha m)` scale. Thus the finite dyadic mesh sequence really
reaches both ranges; it is not just an infinite-grid assertion.
The growing ambient diameter is explicitly retained as an escape from
the count obstruction.

**Flow proposition, G:439–480 / S9:784–817: passes.**
Exactly `M/4` endpoint-grid atoms lie in the upper quarter for every
power-of-two `M>=4`, yielding probability `1/16).
Core curvature is one. On the event, linear positive costs dominate
`min gamma_i ||v||^2`, proving the stated projected growth and the
unique core origin while both labels tie there.
The two positive axis points force different first-stage arcs on
every adjacent full-dimensional box. The origin corner keeps its cell
under the corrected value test at each level.
Chaining the zero-cost parallel stages yields exactly `2^m`
feasible flows and input length `O(m log m)`.
Only a strategy that enumerates all flows after the specified
one-label certificate fails receives the exponential expected-work
lower bound. The proof does not infer hardness of flow recourse.

## Other main-text proofs and model interfaces

| Result / frozen location | Independent check and status |
| --- | --- |
| `thm:lim:width`, S9:99–218 | Passes. The clique/path has actual width p−1; quartic endpoint penalties have upper coordinate curvature 2. A minimizing vertex supplies a completion of every bag corner with gap at most 3p/40. Induction retains the full grid whenever h^2>=3p/(10n). Every derivative has both signs on the full hull and its midpoint Hessian is negative definite. The last dyadic level gives the strict state-count lower bound, and fixing p>2c defeats f(p)I^c for the explicit search. All draws obey the bound. |
| `prop:lim:local`, S9:227–286 | Passes. I rederived the conditional optimizer location and noisy value bounds. The new level-zero sign and negative-Hessian argument closes the early reachability gap. At level one the local rule deletes every projected optimizer; the global allowance retains it. No favorable random event is used. |
| `prop:lim:conditional`, S9:296–348 | Passes. Fixed outside feasibility and upper coordinate semiconcavity give a corner within e_j of the optimum. The oracle's feasible completions update U before retention, giving U<=f*+(1+a)e_j. Every retained cell has a corner within 2(1+a)e_j. Independent bag-noise comparison intervals have length at most La_i[1+(1+a)p/2], yielding the displayed product. The error includes all outside optimization; the result does not assume efficient general recourse or independence of adaptive cells. |
| `thm:lim:constraints`, S9:450–509 | Passes. Native binary t/z/w and continuous s have a polynomial rational encoding and bag-size-four decomposition. The zero point is the only t=0 feasible point; t=1 exists exactly for a Subset Sum yes-instance. Every such point is strictly better on every support vector. Exact native-label output decides t in polynomial expected total work. This is not continuous-LP hardness. |
| `ex:lim:coupled`, S9:519–550 | Passes. The signed row plus bounds is TU. Conditional kappa stays positive. The four coordinate-neighbor increments and the exactly 1/4 opposite-sign event give the lower count (r−1)/4. The example explicitly separates coordinatewise passing nodes from truly near-optimal nodes. |
| `prop:lim:threshold`, S9:561–593 | Passes. The early delta>=0 omission is repaired. Independence and symmetry give the exact strict-tail identity even with atoms; conditioning on a deterministic witness coordinate gives the interval bound and atomic loss 1/(2M). The conclusion now correctly limits direct reading of original threshold answers. |
| `rem:lim:dk`, S9:595–612 | Local arithmetic/probability check passes, subject to item 5 and Luna's primary-source check. A=2^r, target A+1 and the first-item trajectory yield D=2^(r+2), final square D^−2, and a deterministic coordinate one. The generic threshold bound therefore gives the displayed crossing probability. No claim that every possible use of a smoothed solver fails is made. |
| `prop:lim:value`, S9:637–709 | Passes. Gershgorin gives G_n''>=10I; the quartic Hessian square identity leaves a nonnegative quadratic form. Boundary derivatives and induction put all x coordinates strictly inside the box. Stationarity gives x_n<=14·28^(−2^n)<=4^(−2^n), the distance-one witness and squared gap. Adding lambda preserves the interior argument and gives y_lambda=x_n,lambda^2/(x_n,lambda^2+lambda), forcing the displayed doubly-exponential-small parameter. In ordinary rational binary encoding the parameter needs exponentially many bits. The text correctly calls this a value-conversion/Tikhonov limitation and gives an easy alternative point method. |
| `prop:model:regret`, S2:428–475 | Passes. The two endpoints follow directly from a lower sampled value and exactly feasible y; the width bound is delta+omega_X(gamma). The frozen text now distinguishes irrational exact endpoints from rational enclosures and refuses to substitute infeasible rational graph approximations. A continuous relaxation maximum gives a valid lower endpoint on mixed polytopes. Calibration needs the model-specific width correction above. |
| `ex:model:tie`, S2:511–539 | Passes. Equality of independent grid coefficients has probability 1/M. The shifted bilinear objective is nonnegative in both halfspaces x1+x2<=1 and >1, with equality exactly at the two endpoints. A strongly convex convex patch containing both cannot close. The point-growth modulus is zero on that event, so an atomic growth-tail remainder must be at least 1/M. |
| `prop:model:uniform`, S2:169–242 | Supported after item 2. Larger endpoint grids improve the needed interval/transfer inequalities while preserving support; lattice closure resets J to log2M. Gaussian support must be recomputed jointly with its cap. With H=A+D+21, t=ceil(4log2H), b=A+Dt, the displayed bound b+20<=H^4<=2^t is valid for positive envelopes. This preserves the weighted count factors, not a count based on the enlarged support box. General nonlinear flow/TU keeps its supplied-K precision/output/work factor. Strong-field q_i are recomputed because endpoint grids are not nested. |
| Cross-referenced rotating fibers and rank separation, S9:625–630,819–836 | The implication/scope text is correct. The duplicated formal proofs have been removed. S9 now names the merely-convex recourse theorem and expressly preserves the uniform-modulus core-supported rank-at-most-k convexifier caveat. Their Appendix E proofs are outside this seven-file review; the earlier mathematical audit and the separate recourse reviewer cover them. I do not claim to have re-reviewed the finished E proof here. |

## Coverage and remaining integration

The old coverage draft's missing B10 statement is now filled by
`prop:lim:conditional`, with a complete proof.
Its missing X8 worked threshold family is filled by `rem:lim:dk`, with
the source qualification recorded above.
Its missing direct structural X15 boundary is filled by
`thm:lim:posslp`(a) and G's averaging-tree/trace construction.
The full mathematical proof chain is in the submission source and does not
depend on private notes. It explicitly acknowledges companion overlap.

The frozen front report still assigns X16's deterministic flow-core baseline
to Section 8; I did not independently review that other author's completed
integration in this task. The root must finalize the 69-ID coverage against
the complete reviewed manuscript. The exact-active-label versus approximate
point distinction and the detailed O1–O8 source comparison remain useful
related-work qualifications; this report does not certify that the shortened
companion paragraph fully satisfies every overlap inventory item.

## Checks actually performed

1. Read and analytically rederived all six G lemmas, all three G result
   proofs, the new B10 bridge, the regularization/precision proof, and the
   other main-text results listed above. The constants and all-draw versus
   positive-probability contracts were checked from the frozen manuscript.
   No random examples or experiment reruns were used.
2. Ran a scoped `python3 - <<'PY' ... PY` check of all seven manifest
   byte counts and SHA-256 hashes: all matched. It also extracted labels:
   92 unique snapshot labels, no duplicate, and all 15 specifically audited
   result labels present. This was metadata verification, not compilation
   or proof validation.
3. Ran scoped `rg -n` searches over the frozen sections and appendix for
   research paths, Markdown dependencies, evidence paths and unfinished
   placeholder words. There were no matches (normal rg exit 1).
4. Used only scoped `cat`, `rg`, and `nl -ba`/`sed`/`tail` reads.
   Supplemental mathematical comparison used the already local
   exact-arithmetic points construction, the local threshold/interface
   notes, and the immutable complete-proof r1 quadratic terminal schedule.
   Reading those local proofs was not treated as literature verification.

No literature research, manuscript/source-note edit, optimization experiment,
project-wide check, CI inspection, compilation, new numerical proof
diagnostic, or delegation was performed. A final report-only check is recorded
below after materialization. Source identity/priority approval remains with
Luna; approval of the completed r2 manuscript requires checking its actual
revised files.

Final report-only verification passed: final newline and no trailing
whitespace; every frozen S/G locator within its source's line count;
every named snapshot label resolves; all six G lemmas explicitly covered;
all seven snapshot hashes and byte counts still match. The targeted command
was an inline `python3 - <<'PY' ... PY` metadata/report check.
