**Independent Sol review of the frozen early boundary draft**

Reviewed 2026-10-05. The reviewed snapshot is
`evidence/snapshots/early-boundaries-r1/`, whose five files match every hash
in its `manifest.json`. Locations below refer to that snapshot unless a
different location is named. This is a partial-draft review, not approval
of the completed paper.

The substantive constructions checked here are sound. I found no defect
that defeats the subject or its main boundary results. The scope is not
submission ready as written: the threshold proposition has a false literal
statement because it omits a sign assumption, and its surrounding prose
overstates what the crossing calculation excludes. Both repairs are local.
The bag-local counterexample also needs a short argument that the search
reaches its first refinement level. The final integrated paper still needs
review of the relevant theorem interfaces and literature attribution.

I read the brief, independent-review brief, integration decisions, frozen
model and recourse sections, and both frozen boundary files. I also read
the root's early model/recourse reports to avoid treating their already
reported issues as new findings. No manuscript or research-note file was
edited. No literature research, experiment rerun, project-wide check, or
CI inspection was performed.

**Findings requiring correction**

1. **Medium severity; false statement with a simple repair.**
   `sections/09-boundaries.tex:403–412`, especially line 405, does not assume
   `delta >= 0` in the small-gap proposition. The proof at lines 416–420
   uses the interval `[-delta,delta]` and an interval length `2 delta`, so
   it requires this assumption. The statement is false without it. Set
   `X={1}`, `sigma=1`, `Psi(1)=-2`, and `delta=-2`. Under continuous
   uniform noise, the sampled minimum is always negative, but the claimed
   lower bound is `1/2-delta/(2 sigma)=3/2`. Add `delta >= 0` to the
   hypotheses. With that addition, the continuous and finite-law bounds
   are correct, including their strict threshold and interval-endpoint
   treatment. No change to the proof or atomic term is otherwise needed.

2. **Medium severity; scope overstatement, not a failed reduction.**
   `sections/09-boundaries.tex:395–401` and `425–430` say that sampled exact
   optimization does not answer original threshold questions when their
   gap is below the noise, and conclude that the sampled guarantees
   “give no algorithm for those questions.” The proposition proves a
   threshold-crossing probability for a specified family. It does not
   exclude a different reduction with a robust gap, repeated queries at
   chosen scales, or a more elaborate use of sampled outputs. The local
   source note makes this distinction expressly. Replace the conclusion
   with: “These guarantees do not by themselves provide a polynomial-time
   algorithm for the original threshold questions.” Phrase the preceding
   paragraph in terms of directly reading the original answer from the
   sampled optimum. The crossing probability is a useful compatibility
   explanation, but is not an impossibility theorem for every possible
   use of a smoothed solver.

3. **Low severity; missing short reachability argument.**
   `sections/09-boundaries.tex:230–234` and `255–260` assert a deletion at
   level 1 and prove that the level-0 cells survive. Survival alone does
   not rule out the level-0 closure attempt. For this example it is easy
   to rule out closure: every leaf derivative takes both signs, since
   `partial_yi F_gamma=2 yi-x/2+gamma_i`; the core derivative also takes
   both signs, using `(x,y)=(0,1)` and `(1,0)`. The constant Hessian has
   block form `[[2,-1/2 1^T],[-1/2 1,2 I]]`; its quadratic form on
   `(1,(1/4)1)` is `-2` when there are 32 leaves. Thus no sound whole-hull
   sign or convexity test closes at level 0. Add these observations and
   explicitly use the supplied schedule with `J >= 1` (or condition the
   level-1 statement on reaching that level). The deletion inequalities
   themselves are correct and robust for every permitted perturbation.

**Result-by-result mathematical coverage**

| Result and locations | Checked conclusion and qualifications |
| --- | --- |
| Global-error width barrier, `sections/09-boundaries.tex:63–214` | The construction has actual treewidth `p-1`, degree four, and coordinate upper curvature 2. A minimizing vertex exists for every noise vector; the positive quartic terms also show every optimizer is a vertex. Completing a bag tuple by a minimizing vertex outside the bag gives the stated `3p/40` bound. This proves retention by induction while `h_j^2 >= 3p/(10n)`. The full hull remains the original box; exact derivative ranges have both signs; the midpoint Hessian is negative definite. The dyadic last-level inequality gives strictly more than `(5n/(6p))^(p/2)` cells. Fixing `p>2c` correctly disproves `f(p) I^c` work for the explicit-list search. |
| Bag-local counterexample, `sections/09-boundaries.tex:222–286` | Diagonal curvature 2 is exact. The conditional minimizers satisfy `y_i<1/2`; the lower bound on `V_gamma` for `x<=1/2` and the witness at `x=1` place every optimizer in the asserted bag cell. All four unperturbed min-marginal values are correct. Uniform objective perturbation by at most `33 sigma` gives the stated deletion and global-allowance retention margins. The added reachability argument above completes the mechanism claim. |
| Sparse affine feasibility reduction, `sections/09-boundaries.tex:296–354` | This is a mixed-domain construction: `t,z,w` are native binary variables and `s` are continuous. The zero point is the unique feasible point with `t=0`; `t=1` is feasible exactly for a Subset Sum yes-instance. State variables stay in the unit interval. Every constraint has at most three variables; the supplied decomposition has bag size at most four. The objective separation is uniform over every coefficient vector in the noise box. It does not rely on independence or a favorable event. |
| TU diagonal count, `sections/09-boundaries.tex:362–393` | The single signed constraint row plus coordinate bounds is TU. Conditioning on residual noise leaves the two core coefficients independent, and `kappa` stays positive. The four neighbor increments are correct. Under either continuous uniform noise or the defined power-of-two finite grid, the strict opposite-sign event has probability exactly `1/4`; its `r-1` passing diagonal nodes give the expected-count lower bound. The draft correctly limits this result to coordinate-neighbor counting and explains why diagonal comparisons remove the spurious candidates. |
| Threshold crossing, `sections/09-boundaries.tex:403–430` | Correct after adding `delta>=0` and narrowing the prose. Conditional anti-concentration uses a deterministic witness `y`, not an adaptive sampled point. Symmetry gives exactly `Pr(Z<-delta)=(1-Pr(|Z|<=delta))/2`, including atoms at both endpoints. The finite bound loses `1/(2M)`, not `1/M`. |
| Rotating fiber and strictly convex variant, `sections/09-boundaries.tex:448–482`; `appendices/G-boundaries.tex:5–60` | The conditional value, interior core optimizer, projected growth, and full optimal segment are correct. The null-quadratic-form vector has a nonzero Hessian image off the fiber, which proves indefiniteness. The explicit negative direction is correct. The strictly convex residual variant has a unique interior residual minimizer, but its full Hessian is indefinite arbitrarily close to the optimizer. Neither example is an optimization hardness claim. |
| Value-to-point and Tikhonov precision, `sections/09-boundaries.tex:489–559` | Gershgorin gives `H_G>=10 I`. The quartic Hessian square identity proves joint convexity without dividing by the tiny last coordinate. Boundary derivatives put all `x_i` strictly inside their bounds. The stationary chain gives `x_n<=14*28^(-2^n)<=2^(-2^(n+1))`; therefore the distance-one witness has the claimed gap. The regularized stationarity equations and the exact formula for `y_lambda` give the same chain bound uniformly in positive `lambda`. A positive rational parameter small enough to reach `y_lambda>=1/2` really needs exponentially many ordinary binary numerator/denominator bits. This is a limitation of value conversion and this regularization path. The draft correctly supplies an easy alternative point method. |
| PosSLP residual point implication, `sections/09-boundaries.tex:570–606`; `appendices/G-boundaries.tex:64–222` | The bounded pair rules preserve the integer ratio and positive denominator, including repeated operands. The final affine gate is nonzero for every integer output, including zero and negative outputs. The local derivative bounds support the weighted triangular Hessian argument. All weights have polynomial encoding length; the exact, possibly huge gate values are never written. The two sign tests handle active bound coordinates by valid convex first-order conditions. The paired quartic amplifier is jointly convex and forces the designated coordinate to 0 or 1. It has a unique minimizer. The added core is independent of the residual program. Constant point accuracy decides the original circuit on every draw. |
| Boundary one-flow obstruction, `sections/09-boundaries.tex:613–645`; `appendices/G-boundaries.tex:224–265` | The upper-quarter event contains exactly `M/4` atoms per coefficient for every allowed `M>=4`, so its probability is exactly `1/16`. The projected growth lower bound is valid on that event. The two axis points require different first-stage arcs on every positive-width adjacent box. The origin corner retains its cell at every level. Adding zero-cost stages gives exactly `2^m` feasible flows. The exponential expected-work conclusion explicitly concerns a strategy that enumerates all flows after this specific certificate fails. It is not a lower bound for flow optimization or for the later certificate fixing the core face. |
| Fixed quadratic rank separation, `sections/09-boundaries.tex:657–688`; `appendices/G-boundaries.tex:267–323` | The example has total degree five, with an explicit expansion of polynomial size (`O(m^4)` monomials). Its residual Hessian is positive semidefinite for every core value, and core curvature is exactly `lambda`. The boundary kernel argument is valid because convexity in the interior extends Hessian positivity to the boundary by continuity. Positive semidefiniteness of `K` is used correctly to get `Kw=0`. The gradients `4(e_i+1)` span the residual space, forcing `K_zz` positive definite. The strict endpoint/interior witness separation persists under small linear perturbations. The entropy correction follows from the homogeneous Euler identity and the generalized Schur complement, including singular residual Hessians. The separation is from fixed positive semidefinite quadratic corrections on the whole box. |

**Encoding, output, and probability contracts**

The width-family input bound is justified by the explicit factor encoding
allowed in the model: singleton quartic factors and two-variable edge
factors require `O((n+p^2) log n)` bits. It should not be interpreted as a
dense length-`n` exponent vector for every monomial. The PosSLP reduction
also has constant-size factor scopes and polynomial total coefficient
length. The dense rank example must be expanded as a degree-five explicit
polynomial when it is supplied to the polynomial recourse theorem; the
expansion is polynomial in `m`.

The no-FPT work conclusion for width uses the explicit cell and row lists
of the stated sparse search. I checked the current, separately authored
`sections/05-sparse.tex:224–232`, which expressly stores those lists, and
its schedule at `651–657` and `728–740`, which gives the inequalities used
in the frozen boundary proof. That file is not part of this frozen
snapshot. The final integrated review must check that these interfaces
still agree. The lower bound is a list/state-count lower bound for this
search; a hypothetical compressed representation or a specialized vertex
solver is a different implementation mechanism and is not ruled out.

The sparse feasibility consequence correctly reads the explicit native
integer label `t`. It does not require exact comparison of an irrational
optimal value. Its always-correct Las Vegas conclusion is valid in the
bit model because the frozen definition of an exact smoothed algorithm
(`sections/02-model.tex:166–182`) charges computing the law, sampling, and
running the algorithm to its expected work. The reduction's instance
length and `1/sigma=O(n)` are polynomial in the source input. Dropping the
native binary domains would destroy this reduction; it is not a claim of
hardness for continuous linear programming.

The PosSLP consequence deliberately requires efficient point evaluation,
with expected polynomial **total** work, rather than merely a short
unevaluated `argmin` description. Only the designated coordinate must be
accurate, and the distance-`1/4` contract ensures its comparison with
`1/2` is separated on every draw. Rational feasibility of the approximate
point is unnecessary for this decision reduction. The signed gate boxes
can be mapped affinely to unit boxes with polynomial encoding length and
unchanged degree, while leaving the designated `y` coordinate unchanged,
if a unit-box formulation is desired. The draft does not promise that
the complete exact optimizer is rational. These boundary examples have
box or native-flow domains; they do not supply rational feasible lifts
for the manuscript's separate graph-constraint models.

The PosSLP theorem gives an unconditional reduction and conditional
complexity implications, not an established separation from P or ZPP.
Its deterministic Square Root Sum consequence is correct conditional on
the cited polynomial-time oracle reduction. The same oracle reduction
would give Square Root Sum in ZPP under conclusion (a), since a
polynomial number of always-correct expected-polynomial-time oracle
queries can be simulated with polynomial expected total time. I did not
independently research that literature claim; it belongs to Luna's
primary-source attribution check. The local construction and its proof
are self-contained and agree with the relevant companion-paper proof.

There is one coverage distinction to record for inventory X15. The frozen
section includes Square Root Sum only through its reduction to PosSLP.
The companion's `sections/02-points.tex:502–524` states a direct quartic
point reduction for Square Root Sum whose residual interaction graph has
treewidth at most two, whose nonconstant coefficient magnitudes are
bounded, and whose diagonal Hessian entries are at most 20 on a unit box.
The PosSLP construction here does not retain those extra structural
restrictions. If the complete manuscript intends to cover that stronger
boundary too, state and cite it explicitly; otherwise record that the
present broader-class implication deliberately replaces only the general
point-output limitation. I have not independently re-audited the full
direct Square Root Sum construction in this assigned review.

For precision wording, the PosSLP amplifier is even less uniformly
conditioned than the commentary at `sections/09-boundaries.tex:601–604`
might suggest: on the feasible face `a_+=a_-=0`, its pure `y` curvature is
zero, so it has no positive uniform strong-convexity modulus on the whole
box. Its unique optimum can still have positive, extremely small local
curvature. This is consistent with the continuous core-only theorem's
uniform-modulus premise. The rank family similarly belongs to the
ambient certified polynomial-recourse theorem; the final sentence already
correctly excludes attributing it to the uniform-modulus core-only class.
Calling the applicable theorem by its precise name would improve the
plural “recourse theorems apply” at line 679.

The whole section distinguishes the three probability contracts correctly:
the width, sparse feasibility, and residual constructions are pointwise on
every permitted draw; the TU count uses a fixed probability-`1/4` event;
and the boundary flow strategy fails on a fixed probability-`1/16` event
that persists as the finite grid is refined. No counting proof here treats
adaptive survival as independent of noise.

**Checks actually performed**

I manually derived the inequalities and Hessian arguments listed in the
coverage table from the frozen manuscript, rather than accepting the
source notes' review status. Local corroborating proofs read were
`global-error-cell-barrier.md`, `constrained-smoothing-barrier.md`,
`sparse-smoothed-hardness-sanity.md`,
`regularization-point-precision-obstruction.md`,
`posslp-convex-point-extraction.md`,
`core-only-flow-boundary-obstruction.md`, and
`polynomial-recourse-rank-separation.md` under
`research-20261002/new-direction/`, plus the relevant portions of
`paper-exact-arithmetic/appendices/C-points.tex:1249–1415`.

Targeted computational commands actually run were inline
`python3 - <<'PY' ... PY` commands, with these results:

- SHA-256 verification against the frozen manifest: all five files matched.
- Exact SymPy identities for the rotating-fiber null vector, its Hessian
  image, the strictly convex variant's negative direction, and the quartic
  amplifier Hessian square decomposition: passed.
- Exact rational retention and precision-chain constants for `n=1,...,8`
  (with the width inequality for applicable `p>=2`), and upper-quarter
  atom counts for `M=4,8,16,32,64,128,256`: passed.
- Exact SymPy Euler identity and determinant of the spanning-gradient
  matrix for residual dimensions `m=1,...,4`: passed.
- The initial diagnostic stopped while summing SymPy Boolean atoms; a
  first coercion attempt also stopped on that API behavior. Replacing
  the rational scalar checks with Python `Fraction` completed them.
  Neither stop was a failed mathematical assertion. The symbolic
  identities and manifest checks had already passed before the first
  stop.

These are proof diagnostics, not optimization experiments or empirical
performance evidence. The finite ranges corroborate the symbolic
derivations; they do not replace the dimension-uniform arguments.
Read/search commands used `rg`, `nl`, `sed`, and `cat` only within the
assigned manuscript and local mathematical sources. No project-wide
verification or CI check was run, and no CI outcome is claimed.

The required remaining changes in this assigned scope are the
nonnegative-gap hypothesis, the narrower threshold conclusion, and the
short level-0 nonclosure argument. No fatal blocker remains in the
reviewed constructions. Previously reported model-output and duplicated
statement integration issues remain with the root and are not reopened
here.
