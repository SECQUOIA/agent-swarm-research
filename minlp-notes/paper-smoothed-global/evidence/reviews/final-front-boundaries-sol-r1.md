# Final integrated front and boundary review, Sol, round 1

This independent review concerns only the immutable snapshot
`evidence/snapshots/integrated-mathematical-draft-r1/`, captured at
`2026-10-06T03:49:31.635993+00:00`. Scientific locators below are relative to
that snapshot. The live manuscript and author reports are not evidence that
its statements are correct. This report makes no decision about proofs
assigned to the other mathematical reviewers.

**Decision for the assigned scope:** no new substantive mathematical proof
defect was found. All six Appendix G lemmas, its three theorem/proposition
proofs, and the other Section 9 boundary arguments checked below support
their stated mathematical conclusions. The earlier boundary defects have
been repaired in the frozen text. Two minor prose qualifications remain.
The assigned scope is not yet ready for submission: the requested further
companion comparisons and final bibliography/source audit remain pending.
Those are separate from the mathematical status, and this report is not
approval of the completed paper.

## New findings in this snapshot

### F1. Minor: qualify the proof-record size by its actual work bound

**Location:** `sections/01-introduction.tex:309–313`, especially lines
311–312. The introduction says that the global proof record has
“polynomial length only in expectation.” The actual contracts bound its
expected size by the displayed structural and numerical work factor. For
example, `thm:sp:main` at `sections/05-sparse.tex:151–156` gives
`C_0^p[4+(1+n/2)Lw_max/(2 sigma)]^p poly_d(I)`, and `thm:rec:poly` at
`sections/07-recourse.tex:450–451` gives `8^k Q_ap poly_d(I)`. These are
not a uniform polynomial in input length when the structural parameters
vary or a binary-encoded numerical ratio is large. The model states the
correct contract at `sections/02-model.tex:342–349`.

**Repair:** replace the introduction's record clause with “the record's
expected length obeys the same structural and numerical bound as the
expected work.” Keep the polynomial descriptor and ordinary evaluation
claims. This is a scope clarification, not a counterexample to a theorem.

### F2. Minor: include quantified events and expected counts in the boundary overview

**Location:** `sections/09-boundaries.tex:10–13`. The opening dichotomy says
that each result is a mechanism limitation valid on every draw or a
conditional complexity implication. `thm:lim:ambient` instead bounds
expected count surrogates using a positive-probability event;
`prop:lim:flow` obstructs one-label certificates on an event of probability
`1/16`. Their theorem statements and the boundary table correctly give
these scopes.

**Repair:** say that the results are limitations of specified mechanisms
or counts, with the stated every-draw or probabilistic scope, or conditional
complexity implications. This avoids giving an all-draw reading to the
ambient and flow results. No proof change is needed.

## Known pending comparison and source work

These are publication-completeness items already communicated by root, not
new proof defects.

1. **The O1/O7/O8 companion comparisons need one further explicit paragraph.**
   The frozen manuscript compares exact-arithmetic point evaluation, cubic
   positive cases, convexification and the quartic obstruction at
   `sections/01-introduction.tex:447–472`,
   `sections/07-recourse.tex:514–526`, and
   `sections/10-discussion.tex:80–93`. It does not yet give the additional
   distinctions requested by the coverage reviewer: arbitrary point
   approximation versus exact active-label decisions
   (`prop:points-active`), the active-sign rectangle and expanded algebraic
   output barriers (`prop:points-rectangle`,
   `prop:points-algebraic-output`), and the joint-convex specialization.
   The decomposition-aware comparison likewise gives the main graded-grid
   approximation/exact bounds but not the separate conditioned polynomial
   Hessian-at-optimum and boundary-enclosure scopes. The exact local source
   contracts are with Luna; I did not infer them from their labels or do
   literature research. Natural placement is after the two companion
   comparisons in the introduction. A short pointer from the model's
   evaluation paragraph, `sections/02-model.tex:351–365`, would connect the
   active-label distinction to the current output contract. Avoid presenting
   a barrier to one output interface as a barrier to all point algorithms.

2. **The bibliography is not part of this freeze.** The manifest explicitly
   marks the bibliography as pending Luna final audit, and no `.bib` file is
   present in the snapshot. All assigned internal theorem references
   resolve, but this does not resolve citation keys or verify bibliography
   metadata. Final source identity, edition/year/version, theorem/page
   locators, and priority language must be checked against Luna's final
   deliverable. In particular the preliminary evidence marks the
   Pardalos–Vavasis one-negative-eigenvalue source and several classical
   book locators as unfinished. I did not turn that preliminary evidence
   into a final literature verdict.

3. **The worked Del Pia–Khajavirad family is a cited-source instantiation.**
   `rem:lim:dk`, `sections/09-boundaries.tex:564–582`, now correctly
   distinguishes the nonnegative binary penalties `x_i(1-x_i)` from the
   squared recurrence residuals. It attributes the construction and states
   the particular NO family, witness and gap. Luna's supplied preliminary
   primary-source comparison supports those details. The generic threshold
   inequality is proved here; the exact bit-serial construction and its
   `2^(-2r-4)` witness value rely on that cited construction. Final citation
   identity and locator still belong to the final source audit. This is not
   a missing proof of a new hardness theorem in this paper.

## Earlier findings and integration decisions checked in the actual text

| Issue or required distinction | Frozen location | Status |
|---|---|---|
| Amplifier requires a strictly positive supplied base modulus | `appendices/G-boundaries.tex:211–224` | Fixed: `mu_0>0` is explicit; both reductions supply positive constants |
| Exponentially many atoms must enter via logarithmic format bounds | `sections/03-counting.tex:728–740`; `appendices/A-finite-noise.tex:727–738` | Fixed: `log(s+1)` and format/height separation are explicit |
| SRS width two and bounded coefficients do not extend to PosSLP | `sections/09-boundaries.tex:702–713,737–743`; introduction table | Fixed: distinct theorem parts and prose |
| All three point reductions/consequences are companion prior results | `sections/09-boundaries.tex:737–741`; `appendices/G-boundaries.tex:179–182` | Fixed: explicit attribution; proofs remain self-contained |
| Core-only cubic positive cases must survive the quartic obstruction | `sections/01-introduction.tex:447–472`; `sections/09-boundaries.tex:584–601`; `sections/10-discussion.tex:48–56` | Fixed: residual-convex cubic selector and supplied-convexifier scopes are retained |
| An all-precision finite law is already present in the companion | `sections/01-introduction.tex:451–459,469–472`; `sections/10-discussion.tex:88–93` | Fixed: descriptor/proof interface is distinguished from an optimization-time improvement |
| Uniform residual modulus implies a small-core quadratic convexifier | `sections/07-recourse.tex:556–566`; `sections/09-boundaries.tex:804–816` | Fixed: Schur-complement scale is stated; direct `L/sigma` remains the comparison |
| Retention lower bound is rule-specific, not a lower bound for all sparse algorithms | `sections/09-boundaries.tex:67–97,207–214`; `sections/10-discussion.tex:105–117` | Fixed: easy binary DP and other possible methods are stated |
| A conditional-value oracle is sufficient, not necessary for every possible FPT method | `sections/09-boundaries.tex:289–329`; `sections/05-sparse.tex:675–692` | Fixed, with a proved current-level incumbent interface |
| DA Euclidean `kappa` and weighted `bar kappa`; graded counts and rETH scope | `sections/01-introduction.tex:474–499`; `sections/05-sparse.tex:694–742` | Fixed; see comparison checks below |
| SI indicator-penalty-only noise, exact dictionary and numerical magnitudes | `sections/01-introduction.tex:501–514` | Fixed in the frozen comparison; final source metadata pending |
| FPT must include numerical ratios | `sections/00-abstract.tex:8–15`; introduction table caption; `sections/02-model.tex:387–406`; `sections/10-discussion.tex:60–65` | Fixed throughout checked front claims, apart from F1's record wording |
| Applications require the constructed law; two-stage feasibility stays fixed | `sections/10-discussion.tex:5–17,39–47` | Fixed; no arbitrary-distribution or cost-to-constraint extrapolation |
| Strong-noise sufficient constants are large, with no performance evidence | `sections/10-discussion.tex:95–102`; `sections/08-integer.tex:584–611,634–650` | Fixed: effective nonquadratic constant and quadratic exception are stated |
| Rational singleton-hull fixing and zero-dimensional evaluation | `sections/02-model.tex:309–319,366–368` | Fixed and mathematically legitimate |
| Implicit graph lifts can be algebraic; rational full feasibility is not promised | `sections/02-model.tex:357–363`; `sections/06-constraints.tex:244–255` | Fixed: rational retained coordinates, exact dependent roots and separate rational approximations |
| Gaussian calibration charges actual support and noise-coordinate widths | `sections/02-model.tex:469–514` | Fixed; dyadic existence and reciprocal-scale bounds checked below |
| Nonlinear boundary flow/TU common law uses a supplied `K>=k` | `sections/02-model.tex:174–225`; `sections/03-counting.tex:689–720`; `appendices/A-finite-noise.tex:802–813` | Fixed; taking `K=I` does not preserve the actual-small-core budget |
| B10, A0 and X16 must be retained | `prop:sp:conditional`; `cor:qp:conditioned-mixed`; `cor:int:grid` | Present with manuscript proofs, not private-note promises |

## Appendix G: complete proof and statement audit

### `thm:lim:ambient` and `app:lim:ambient`

**Statement:** `sections/09-boundaries.tex:361–394`.
**Proof:** `appendices/G-boundaries.tex:5–175`.
**Status:** checked; no mathematical defect found.

I rederived the block spectrum, auxiliary objective, probability event,
flatness estimates and both product counts. On the orthonormal range basis
the original block matrix has eigenvalues
`alpha(1 +/- sqrt(17/8))`; the convexified block has positive determinant
`7 alpha^2/8`. The row factor has unit norm, and its projected range is
exactly `[-4,4]`. The simplex masses give the stated coefficient
`S=(m/2)(min B_+ gamma-min B_- gamma)` and square completion shifts the
auxiliary argument by `xi/alpha`; it does not assume independence of the
factor and residual noise.

For either law, the two independent minima events have the claimed lower
bounds. The grid atom mass is at least `19/(10n)`. Subtracting the
Chebyshev bound `3/32` gives at least `41/160>1/4`; no independence of
`xi` and those minima is used. On this event, `|S|<=2/m`, `|t|<=1` and
`|xi|<=2`. The interior minimization in `y` is justified on
`|a|<=3/2`; it gives `|V'(a)|<3/m`. The trial `(a+xi/alpha,0)` and the
global lower bound on `G` give `V(a)-min V<15/m` on `|a|<=1`.

Products have event probability greater than `4^(-k)` and allowance
`2E_h=alpha k h^2/4`. The specified two ranges of meshes respectively
give the near-optimal and coordinate-neighbor counts
`(sqrt(alpha m)/64)^k` and `(alpha m/128)^k`. The lower bounds on the
number of nodes allow an arbitrary grid phase, not only a grid centered
at zero. The auxiliary search meshes meet both dyadic intervals. For
`alpha=1`, fixing `k>8c` defeats an `f(k,R) I^c` bound using the stated
dense upper bound `I<=C_0 N^2 log N`. This is a count-surrogate result;
the proof and following discussion do not infer algorithm work. The ambient
diameter grows with `m` and is explicitly excluded from the fixed list `R`.

### `lem:lim:signs`

**Statement/proof:** `appendices/G-boundaries.tex:184–209`.
**Status:** checked.

The bilinear Hessian block has operator norm at most
`epsilon ||grad zeta||<=kappa/4`; since `kappa<=1`, the base Hessian is
at least `kappa I` including the theta coordinate. Thus the claimed
`3kappa/4` modulus holds on the box. The first-order conditions at the
face theta=0 prove theta=0 exactly when `zeta(z^0)>=0`; when the value
is negative, a feasible positive-theta direction strictly decreases the
objective. This handles constrained base minimizers, not just interior ones.

### `lem:lim:amplifier`

**Statement/proof:** `appendices/G-boundaries.tex:211–246`.
**Status:** checked; the earlier zero-modulus counterexample is excluded.

The identity
`2(theta varsigma+2(y-c)pi)^2-6(y-c)^2 pi^2` is correct. With
`eta=mu_0/12` and `|y-c|<=1`, the negative part is absorbed by half the
strictly positive base modulus. This proves convexity, not a positive
modulus in y everywhere; the manuscript makes only the former claim.
The nonnegative amplifier attains zero at the two unique base minimizers
and the selected endpoint of y. Equality in the lower bound fixes the base
coordinates and the positive activation then fixes y. This proves
uniqueness without dividing by an activation coordinate.

### `lem:lim:tree`

**Statement/proof:** `appendices/G-boundaries.tex:263–290`.
**Status:** checked, including its dimension-independent modulus.

For a direction, the leaf coordinates and averaging residuals are exactly
`(I-P)d`. Every child has at most one parent, so distinct rows of P have
disjoint supports; each row's squared norm is at most `1/2`. Hence
`||P||<=1/sqrt(2)`. The leaf diagonal second derivatives are at least 2,
and the residual-square Hessians give
`2||(I-P)d||^2>=2(1-1/sqrt(2))^2||d||^2>=||d||^2/8`.
No estimate grows with tree height. Minimizing every leaf term and then
setting all residuals to zero gives the root
`sum sqrt(a_i)/(KR)`. Padded zero leaves cause no missing variables or
feasibility problem. Parent/children bags have at most three variables,
cover every term and satisfy connected occurrence.

### `lem:lim:trace`

**Statement/proof:** `appendices/G-boundaries.tex:292–308`.
**Status:** checked.

Trace transitivity gives zero trace for each nonsquare radical, and a
rational radical has trace equal to its value times the field degree.
If the total is an integer, the sum over positive nonsquare radicals would
therefore be zero. This is impossible unless there are none. The reduction
uses integer square roots only; it does not construct the multiquadratic
field or factor radicands. The all-square and negative/large B cases are
preprocessed, so equality is absent from the constructed instances.

### Square Root Sum construction, structural restrictions and output

**Locations:** `appendices/G-boundaries.tex:248–261,310–334`;
`sections/09-boundaries.tex:702–709`.
**Status:** checked.

The powers of two `R_i`, weights `w_i`, the power-of-two leaf count K and
`b=B/(KR)` have polynomial encoding length. The two sign tests use
`kappa=1/8`, so `epsilon=1/32` and `mu_0=3/32`; the amplifier uses
`eta=1/128`. Their output y is 1 for a strict NO comparison and 0 for
a strict YES comparison. This reversed encoding still decides the stated
decision problem, and the equality preprocessing is essential and present.

The root/theta and theta/y bags can be joined without violating connected
occurrence; their maximum bag size remains three. Leaf diagonal Hessian
entries are at most `9/2`, internal entries at most `5/2`, theta entries
at most `2+2eta`, and the y entry at most `4eta`. Mapping interval widths
at most two onto unit coordinates multiplies diagonal entries by at most
four, so 20 is valid. Each summand has bounded coefficients and at most
three variables; bounded variable incidence bounds accumulation into each
nonconstant expanded monomial. An accumulating constant can be deleted.
The coefficient restriction concerns magnitude, not a bounded denominator
or a lower bound on the tiny activation at the optimum.

### `lem:lim:pairs` and the gate bounds

**Locations:** `appendices/G-boundaries.tex:343–380`.
**Status:** checked.

The inductive ratios equal the program integers, all denominators stay
positive, and both coordinates remain in `[-1/4,1/4]`. The addition and
product numerators have the claimed smaller bounds. Thus
`t=v_s(2A-1)/4` is nonzero, has the sign of positive integer A, and has
absolute value at most `3/16`. The affine final gate stays in the box.
The derivative and Hessian bounds remain valid when the two input indices
coincide; merged monomials do not invalidate the norm bounds. Listing
`u_j` before `v_j` still gives triangular rules because both use only
earlier program indices. Exponentially long program integers are never
computed or supplied to the reduction.

### `lem:lim:gates`

**Statement/proof:** `appendices/G-boundaries.tex:382–409`.
**Status:** checked.

For `a_i=64^(N-i)`, conjugating the strictly lower-triangular derivative
matrix by `D=diag(sqrt(a_i))` gives entries `8^(j-i)L_ij`. Its row
and column absolute sums are at most `1/8` and `1/7`, so its operator
norm is below `1/4`. The positive Hessian term is therefore at least
`9||Dh||^2/8`. With residual absolute value at most `1/2` and dependence
only on earlier coordinates, the adverse term is bounded below by
`-sum_j h_j^2 sum_(i>j) a_i >= -||Dh||^2/63`. This proves the stated
modulus 1. The exact triangular assignment is the unique zero of G and
lies in the box. No unit-cost arithmetic on enormous integers is hidden
in this construction.

### PosSLP construction and part (c)

**Locations:** `appendices/G-boundaries.tex:411–438`;
`sections/09-boundaries.tex:710–735`.
**Status:** checked.

The PosSLP sign tests use `kappa=1`, `epsilon=1/4` and
`mu_0=3/4`, followed by `eta=1/16`. The designated coordinate is 1
exactly when A is positive. Weights have O(N) bits and O(N) residual
squares expand to O(N) fixed-degree monomials, so the explicit rational
quartic has polynomial description length. Numerical coefficients and
interaction width need not be bounded; no such claim is made for this part.

For either reduction the noisy core separates completely, has optimum
`(1-gamma)/2` in `[1/4,3/4]`, and has projected growth one and second
derivative two. The residual optimizer is unchanged on every draw.
Computing a point within Euclidean distance `1/4` determines its y bit by
comparison with `1/2`. The theorem assumes expected polynomial total work,
including law construction, sampling and point evaluation, so this is an
all-draw-correct Las Vegas decision reduction. Its deterministic variant
also follows directly. No lower bound on ordinary convex value
approximation is claimed. The final public PosSLP-oracle relation is a
cited classical result, pending the final source audit.

### `prop:lim:flow` and `app:lim:flow`

**Statement:** `sections/09-boundaries.tex:760–792`.
**Proof:** `appendices/G-boundaries.tex:440–481`.
**Status:** checked.

For a power-of-two endpoint grid with `M>=4`, exactly M/4 atoms are at
least `1/2`, hence the event has probability exactly `1/16` independently
of resolution. On that event, `v_i>=v_i^2` gives projected growth at least
one at the unique core optimum zero; both labels tie there. The labels
strictly reverse order at `(a,0)` and `(0,b)`, so no positive-width
rectangle admits one label optimal throughout. The corrected-grid bound
of `[0,h]^2` is at most `V(0)-h^2/4<=U_j`, so induction from level zero
retains it. Adding zero-cost parallel stages produces `2^m` distinct flows
without changing the conditional value. The exponential work conclusion
explicitly concerns a strategy that enumerates all flows when its one-label
certificate fails. It does not concern a general min-cost-flow oracle or
the optimal-face certificate used by the positive theorem.

## Other Section 9 statements and dependent examples

| Statement and frozen proof | Checks and status |
|---|---|
| `thm:lim:width`, `sections/09-boundaries.tex:99–205` | Checked the graph/treewidth, encoding `O((n+p^2)log n)`, diagonal curvature 2, vertex optimality, completion bound `3p/40`, induction of all-cell retention, both derivative signs, negative midpoint Hessian, last-level cell count and fixed-p exponent argument. Noise is arbitrary in the stated box, so the expected-work consequence is all-draw. The premise specifies this retention/closure rule and stopping depth. No unrestricted optimization lower bound follows. |
| `prop:lim:local`, lines 227–285, with `ex:rec:star` at `sections/07-recourse.tex:153` | Checked m=32, the uniform `33 sigma` perturbation bound, optimizer location `v>1/2,z_1<1/2`, level-zero nonclosure and level-one grid min-marginal gap. The bag allowance is `1/8`, the global allowance `33/16`. The `23/32` star grid value and both robust inequalities agree with the source example. This now proves that the algorithm reaches the erroneous pruning step. |
| `prop:lim:conditional`, lines 296–316; `prop:sp:conditional`, `sections/05-sparse.tex:598–673` | Checked the actual referenced proof: minimum over a fixed outside domain preserves coordinate upper curvature, feasible mean-preserving rounding retains every optimizer, current-level upper answers give `U_j<=f*+e_j+eta_j`, and retained cells have a true-value witness within `2(e_j+eta_j)`. The envelope `eta_j<=a e_j` need not be independent of the draw. Finite-grid coefficient intervals use the fixed envelope and `M>=2^J`. The count is joint FPT in bag size and numerical ratios; oracle work is explicitly not supplied by this corollary. |
| `thm:lim:constraints`, lines 419–474 | Checked positive Subset Sum input, continuous recurrence coordinates, native binary labels, the all-zero feasible point, bag size four and coefficient magnitudes. Only t=0 is possible for NO inputs; YES inputs have a strict value advantage on every noise draw in the stated box. `1/sigma=O(n)` and encoding is polynomial. The complexity hypothesis includes computing and sampling a polynomial-bit base-chosen law. Reading t decides every draw, giving the stated conditional NP-in-ZPP implication. Bounded magnitudes do not imply a bounded Hoffman or denominator parameter. |
| `ex:lim:coupled`, lines 488–512 | Checked the TU single row, positive residual slope, conditional kink, all four coordinate increments, event probability `1/4` for each stated law and `(r-1)/4` expected passing count. This concerns coordinate-neighbor candidates, not truly near-optimal nodes. |
| `prop:lim:threshold`, lines 530–555 | Checked symmetry including atoms, the required `delta>=0`, interval length `2delta/|y_i|`, continuous/grid mass bounds and the strict-negative event. Other coordinate laws need only independence and symmetry. The result addresses direct threshold reading, and the following text preserves other possible reductions or repeated scale queries. |
| `rem:lim:dk`, lines 564–582 | Generic probability substitution is correct. The claimed witness coordinate equals one and the quoted gap gives the displayed `1/2-2^(-2r-5)/sigma-1/(2M)` lower bound. The underlying worked family is source-dependent as recorded above. |
| `prop:lim:value`, lines 614–685 | Checked tridiagonal Hessian/Gershgorin modulus 10, convex quartic amplifier identity, interior KKT induction, `x_n*<=4^(-2^n)`, distance-one point and doubly exponential gap. The regularized KKT denominator includes the final y term and yields the same upper bound. `y_lambda>=1/2` forces `lambda<=x_n,lambda^2`. The resulting bit requirement is superpolynomial in `I=O(n log n)`; it is explicitly a value-to-point/Tikhonov limitation, with an easy direct solution acknowledged. |
| `ex:rec:fiber`, `sections/07-recourse.tex:673–689` | Checked projected growth and the rotating residual fiber. With residual error nonzero, a direction in the residual-square gradient kernel exposes the mixed indefinite Hessian. In the strict-convex variant, points with shifted `z_2=0` and nonzero residual error occur arbitrarily near the unique optimizer and still have an indefinite Hessian. This limits full-dimensional convex patches; it does not establish residual hardness. |
| `prop:rec:rank`, `sections/07-recourse.tex:480–503`, proof `appendices/E-recourse.tex:460–484`; discussion `sections/09-boundaries.tex:795–824` | Checked PSD kernel reasoning at t=0 and the spanning gradients `grad P(e_i)=4(e_i+1)`, forcing `K_zz` positive definite and rank at least m. The family has merely convex recourse. Uniformly strongly convex recourse is separately given the rank-k Schur-complement convexifier. Direct core curvature remains lambda; T enters coefficient bit length. The nonquadratic `Ct log t` correction is correctly excluded from the quadratic-rank conclusion. |

## Front, model and results-table audit

I read all of Sections 00, 01, 02, 09 and 10. I compared every substantive
row of `tab:intro:results` (`sections/01-introduction.tex:130–199`) with
the frozen route statements below. This comparison checks the front-facing
contract; it does not replace the other reviewers' full route-proof audits.

| Table route | Actual theorem/contract checked | Result |
|---|---|---|
| General low-rank Gaussian, aligned and uniform QP | `sections/04-quadratic.tex:559–638`, `thm:qp:gauss`, `thm:qp:aligned`, `thm:qp:uniform` | Matches ambient versus factor laws, mixed versus continuous domains, rational outputs, polynomial-bit samplers, joint numerical factors and uniform dimension exponent |
| At most two negative directions | `sections/04-quadratic.tex:261–282`, `thm:qp:two` | Matches continuous-only scope, both finite law families and linear `1+nu S/sigma` factor |
| Separable quadratic recourse | `sections/04-quadratic.tex:815–881`, `thm:qp:sep`, `thm:qp:sep-gauss` and model at lines 759–761 | Matches piecewise quadratics with rational knots, unrestricted integer count, supplied concave factor scale and rational outputs |
| Separable integer lattice route | `sections/08-integer.tex:659–696`, `thm:int:lowrank` | Matches fixed-degree explicit piecewise polynomials, native integer intervals, row-aligned law, rational exact output, `8^k H_rat`, no fallback |
| Sparse mixed polynomials and sparse QP | `sections/05-sparse.tex:138–169,1071–1098`, `thm:sp:main`, `cor:sp:qp` | Matches patch/fallback versus rational QP outputs, dimension-dependent count and fixed-degree polynomial-bit laws |
| Graphs, actuators, simplices and orders | `sections/06-constraints.tex:223–255,491–513,587–605,700–731` | Matches actual charted/relative formats and displayed fixed-width factors; algebraic implicit lifts are correctly qualified elsewhere in the front |
| Quadratic, certified polynomial and modulus-based core-only recourse | `sections/07-recourse.tex:337–351,432–457,528–554` | Matches exact versus certified oracles, all required subboxes, ambient versus core-only laws, `Q_ex` versus `Q_ap`, rational versus implicit/fallback outputs |
| Native integer recourse | `sections/08-integer.tex:175–193`, `thm:int:native` | Matches polynomial-bit ambient law, every-draw `c_d^k` algebraic output length, label output and expected work |
| Interior and bilinear flow | `sections/08-integer.tex:370–384,489–496` | Matches core-only laws, interiority premise in the first case, polynomial sampling precision and `c_d^k` output/refinement factors |
| General boundary flow and TU | `sections/08-integer.tex:460–473,514–530` | Matches `f_d(k)poly_d(I)` sampler/output lengths and `f_d(k)Q_ex poly_d(I)` work; no claim of polynomial-bit resolution independent of k |
| Strong fields | `sections/08-integer.tex:568–650`, `thm:int:strong-field` | Matches arbitrary actual grid resolution, subcritical branch denominator, component algebraic format, common-root components and symbolic total value, quadratic rational case |

The statement that all QP outputs are rational has the actual rational
polyhedral/piecewise-quadratic domain scope. It is not applied to implicit
graph equations. Component outputs share a root within each component and
give a symbolic sum across components; the front does not promise cheap
exact sign tests for unrelated algebraic sums.

**Finite-law and original-objective interfaces.** I checked
`prop:model:uniform` and its scientific proof dependencies at
`cor:count:universal-law`, `sections/03-counting.tex:642–751`, and
`appendices/A-finite-noise.tex:675–822`. The fixed effective envelope
argument uses logarithmic atom counts, separates combinatorial format from
coefficient height, and fixes the oracle implementation. Increasing M
preserves the applicable grid budgets; the lattice cap is reset to log M.
Gaussian accuracy is increased only after jointly recomputing its support
box and cap. For `H=A+D+21`, `t=ceil(4log_2 H)`, `b=A+Dt`, the bound
`b+20<=H+4H^2<=H^4<=2^t` is valid. Arbitrary strong-field q_i are not
monotone under refinement; only the sufficient regime transfers after
recomputation. Nonlinear boundary flow/TU uses the supplied K budget and
does not quietly impose its sampling cost on a small actual core while
claiming the old f_d(k) bound.

I also checked the regret inequality and exactly feasible lift interface
at `sections/02-model.tex:420–514`. Calibration uses W_noise in the
perturbation coordinates, including factor-row ranges and row-specific
scales. W_noise=0 is handled directly. The Gaussian scale takes the least
nonnegative integer t satisfying
`2R(P(I_0+t)+20)<=2^t`, with `R=max(1,W_noise/epsilon)`.
Exponential growth guarantees `t=O(I_0+log R+1)`; failure at the previous
integer gives the reciprocal-scale estimate, and t=0 has its own valid
bound. This charges the exact `b+20` support multiplier. Numerical factors
remain after substitution, and the strong-field route is excluded from
arbitrary prescribed-accuracy calibration. Implicit graphs return exact
algebraic dependent lifts, not nonexistent rational full feasible points.

**Companion numerical comparisons.** The frozen DA paragraph correctly
distinguishes Euclidean point growth from weighted growth, gives the
explicit `f(p,bar kappa)(I+q+1)^5` form, states that the condition parameter
is not an algorithm input, and separates the exact theorem's uniqueness
and point-growth hypotheses. Graded counts are logarithmic in n per
coordinate, while the quoted uniform-grid retained family is rule-specific.
The rETH claim stays in the companion's specified product-time model and
does not claim a matching p/2 exponent. The truncated moment formula in
`sections/05-sparse.tex:729–737` follows by layer-cake integration and
retains the cutoff power; `sections/10-discussion.tex:111–117` limits the
integration argument instead of declaring all algorithms impossible.
The SI paragraph names indicator-penalty noise, exact dictionaries and
numeric C,H,mu^-1,R,sigma^-1 dependence, keeping its encoding-only
NP-in-ZPP implication separate from this paper's affine feasibility
reduction. Final primary source verification is still Luna's task.

**Retained inventory items.** B10 has a full in-manuscript proof at
`sections/05-sparse.tex:633–673`; its oracle interface and count were
rechecked above. X15 has the direct width-two bounded-coefficient SRS proof
audited in G above. X16 is `cor:int:grid` at
`sections/08-integer.tex:324–341`, with proof at
`appendices/F-integer.tex:559–572`: fixed outside feasibility gives the
`kL/(8m^2)` corner allowance, the least upper answer is at most the least
lower answer plus eta, and no residual variable is rounded. A0's mixed
conditioned counterpart is `cor:qp:conditioned-mixed` at
`sections/04-quadratic.tex:228–237`, with proof at
`appendices/B-quadratic.tex:262–280`. That proof keeps the full auxiliary
embedding, removes only singleton mesh ranges, uses LP bounds for integer
labels and denominator heights, and charges the exact mixed oracle factor.
These items are present rather than silently excluded or outsourced to
private notes. This is not an independent recertification of all 69 IDs;
the final complete coverage record is a separate root task.

## Source integrity and checks actually performed

The following six directly assigned scientific files were read in full:

| File | Lines | SHA-256 |
|---|---:|---|
| `sections/00-abstract.tex` | 27 | `2b1dd7bfef41dd05d68d527afcba9c1526ce5b4ca243d96d926f63b2236bfbc2` |
| `sections/01-introduction.tex` | 524 | `c3b27472e13d0c6a94d1cb6693d264d6ac0f6137c7e64d039bc613eb3d35ba56` |
| `sections/02-model.tex` | 559 | `0a9267cd7a893497d212e5ccb0fbb6433b6428c4784793dd9fc79ec4f4e38a63` |
| `sections/09-boundaries.tex` | 824 | `1acb7217806f6e53e27a653e9ca36df3adfa3d37cc25a428b45c4770cb8e7bf8` |
| `sections/10-discussion.tex` | 144 | `d1e176dc2598a40d80d9bc6e13773cd634a713cd6f8e236d5b6e992ebfc49c56` |
| `appendices/G-boundaries.tex` | 481 | `163333352717c3b090f62924f8a8b90eea63cf7c4fc50bf1da0dafd4556f1553` |

I used scoped `rg`, `sed` and Python text reads of the frozen files. The
read-only Python metadata check computed SHA-256 and line counts for all
20 TeX files and compared them with the manifest; all matched. A label
catalogue of those frozen files found no duplicate labels. Internal
references in the six assigned files all had frozen targets. These are
snapshot-integrity and assigned-reference checks, not a build or a
project-wide verification run.

Evidence consulted included BRIEF, the independent review brief,
integration decisions and contract, my two earlier boundary reports and
coverage draft, root model/introduction/integration-scope findings and final
mathematical handoff, the universal-law budget report, front-r1 and the
four final author reports, the Opus editorial interim and root disposition,
the explicitly incomplete Opus mathematical report, and Luna's preliminary
source audit. Author reports were used to identify claimed repairs, which
were then checked against the immutable scientific text. No approval was
inferred from those reports or an earlier build.

After writing this report, its final newline, whitespace, heading structure
and named frozen locators were checked, together with a second manifest
comparison. No mathematical experiments, optimization reruns, literature
searches, TeX edits, delegation, project-wide tests or CI inspection were
performed. Only this review report was written.
