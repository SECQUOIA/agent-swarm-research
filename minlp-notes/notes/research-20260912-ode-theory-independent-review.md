# Independent review of supporting flows for extended RPD

Reviewed 12 September 2026 by the fresh `ode_theory_review` subagent. This review is independent of the author derivation and does not modify the author draft or literature knowledge base.

The primary draft is [Supporting flows for polynomial extended RPD relaxations](../results/extended-rpd-supporting-flow.md). I also read [the opportunity note](research-20260912-second-opportunities.md), Ye–Scott (2023), Definitions 5–14 and its composition results, and Ye–Scott (2025), Algorithm 1 and the relevant construction and regularity statements. Equations missing from the Markdown extraction were checked in a separate `pdftotext -layout` extraction of the local original PDFs.

At review time the primary draft had SHA-256 `831a93bc19e5058deff0d6de24536877c4159caefc428b7ba6a8de149446ef97`, and the opportunity note had `59ea8ad8bcfea368f7e54f55451b3040cddfe7b3a4730aa177abc1007daf2843`. The author incorporated the priority warning below while the review was in progress. Subsequent edits should be distinguished from these reviewed versions.

## Verdict

I found no mathematical defect in Theorems 1–3 or Proposition 4 under the explicit fixed-interval, globally defined refinement assumptions. In particular, joint parameter dependence, inconsistent endpoint data, own-coordinate substitutions, direct comparison with physical states, and domination of an existing refined RPD field are handled correctly. The matrix comparison argument does justify true supporting rows without computing classical sensitivities.

The positive verdict is conditional on the actual construction satisfying the stated assumptions. It does not cover arbitrary McCormick implementations, adaptive interval computations, generic automatic differentiation, a hard infeasible refinement LP, or floating-point integration without an error certificate. It is a proof review, not a verification of any experimental implementation or a claim of publishable novelty.

The main contribution warning is stronger than merely saying that the tools are classical: **fixed-interval local Lipschitz continuity is already an immediate consequence of Ye–Scott's finite convexity on coherence fibers**. The polynomial proof additionally establishes global Lipschitz continuity, linear growth and finite affine structure. That is useful implementation information, but local regularity alone should not be presented as a substantial new theorem. The author has incorporated this warning. The closest sensitivity and affine-enclosure comparisons remain necessary.

## 1. Signed arithmetic, including empty inputs

For a scalar interval `[l,u]`, write the signed endpoints as `(a,b)=(c,-C)`. The cut map is exactly

\[
(a,b)\longmapsto (\max(l,a),\max(-u,b)).
\]

It is finite, convex in each output, nondecreasing in both inputs, piecewise affine and globally Lipschitz on all of `R²`. There is no assumption that `c≤C`, that the relaxation endpoints are within `[l,u]`, or that the two intervals intersect.

Let `D_α(a,b)=αa` for `α≥0` and `D_α(a,b)=(-α)b` for `α<0`. This is the signed form of the lower selector in Ye–Scott (2023), equation (29), and has nonnegative coefficients. The signed upper selector is `D_α(b,a)`. Thus the signed lower product is

\[
\max\{D_{y^L}(\bar a,\bar b)+D_{x^L}(\bar d,\bar e)-x^Ly^L,
D_{y^U}(\bar a,\bar b)+D_{x^U}(\bar d,\bar e)-x^Uy^U\},
\]

where bars denote the cut endpoints and `(d,e)` are the signed endpoints of the second operand. The negative of the upper product is a maximum of the two corresponding signed upper selectors and their negated constants. All coefficients on cut signed endpoints are nonnegative, for every combination of interval signs. Addition has the same property after the cuts.

This directly proves the primitive properties. Nonnegative monotone convex composition preserves convexity, isotonicity and global Lipschitz continuity. Composition of finitely many piecewise-affine functions is piecewise affine with finitely many pieces. Since the result is convex and finite on the full input space, it can also be represented as the maximum of finitely many affine functions. The number of pieces may be large; the theorem does not imply an efficient explicit enumeration.

An independent exact counterexample confirms why the alternate selector must be excluded. Take both operand intervals `[0,1]`, and fix the second operand's endpoints to `(1,1)`. The endpoint-minimum variant gives the lower output

\[
\widehat g(c,C)=\max(0,\min(\max(0,c),\min(1,C))).
\]

At `(c,C)=(0,2)` and `(2,0)` it is zero, but at their midpoint `(1,1)` it is one. It is therefore not convex on the extended endpoint domain. The correct sign-selected rule gives `max(0,c)` in this example and passes the convexity inequality. This is an illustration of the distinction already established in Ye–Scott (2023), not a new counterexample claim.

Exact parameter channels `(p,-p)` are an affine substitution into this global signed arithmetic. Their opposite signs do not jeopardize joint convexity in parameters. Monotonicity in parameters is not required anywhere in the comparison argument. The state endpoint channels retain their isotonicity.

## 2. Refinement and the own-coordinate substitution

Let the pre-substitution signed right-hand side be

\[
K_j(p,w)=G_j(p,H_i(p,w)).
\]

The composition is jointly convex in `(p,w)`: the inner map `(p,w)↦(p,H_i(p,w))` has an affine parameter channel and convex refinement channels; the outer `G_j` is jointly convex and nondecreasing in every refinement channel. A direct Jensen proof first bounds `H_i` by the convex combination of its endpoint values, uses monotonicity in those channels, and then uses joint convexity of `G_j`. This avoids incorrectly demanding parameter monotonicity.

For the lower equation of physical coordinate `i`, `E_i^-` overwrites coordinate `n+i` by `-v_i`. Consequently the only negative input coefficient introduced by this substitution belongs to the equation's own signed state coordinate `i`. The overwritten coordinate `n+i` disappears completely. All other state dependencies remain nonnegative. The upper equation has the analogous property, with own signed coordinate `n+i`. Affine precomposition also preserves joint convexity and global Lipschitz continuity.

Therefore the field is cooperative in the exact sense needed: every output is nondecreasing in every *other* signed state coordinate. Its own-coordinate dependence can have either sign. There is no hidden requirement that the full Jacobian be nonnegative.

Finite row refinement with fixed matrices and fixed interval data satisfies the required convex and isotone structure. In Ye–Scott (2025), Algorithm 1, any interval-part updates depend only on fixed input interval parts and fixed invariant coefficients, not on the trial relaxation endpoints. They can therefore be regarded as precomputed constants on the fixed interval fiber. Source algorithms that change the interval data as a function of the trial parameter or endpoint values require a separate argument; this review does not authorize those changes.

The self-exclusion observation is correct. With the physical interval `[0,1]` and substituted own pair `(-1,-1)`, initial clipping changes that pair to `(0,-1)`. Skipping only the invariant-row updates does not literally preserve the own pair on the global extended domain. Replacing both own output components by their unmodified inputs does preserve the required structural assumptions. This is a precise distinction between two maps; it does not demonstrate failure of the source's tested integration trajectories or establish stability of either version.

## 3. Global existence and physical bounds

With fixed `p`, a globally Lipschitz field obeys

\[
\|F(p,v)\|\le \|F(p,0)\|+L\|v\|.
\]

The ordinary Picard–Lindelöf and Gronwall arguments therefore give uniqueness and exclude finite-time blow-up for every finite initial state. This applies even if intermediate endpoint objects are empty or the relaxation trajectory leaves the physical state box. Only the physical trajectory must remain in the valid fixed box.

For validity define `z=(x,-x)`. Every own-coordinate equality substitution fixes `z` exactly. By refinement bound preservation, `H_i(p,z)` encloses the physical state. Since the interval data are valid and the arithmetic is a valid extension on nonempty enclosures, its lower output is at most `f_i(p,x)` and its negative upper output is at most `-f_i(p,x)`. Thus

\[
\dot z\ge F(p,z).
\]

The initial relaxation satisfies `v₀≤z₀`. Cooperative comparison gives `v≤z`, proving both lower and upper state bounds. This proof does not assume that the computed relaxation itself stays within the interval box or remains an exact enclosure before the theorem has been established.

For convexity in parameters, the convex combination of the trajectories at two parameter points is a supersolution at the convexly combined parameter. Initial componentwise convexity and the same comparison theorem give the stated convexity. Since `P` is a box, the convexly combined parameter remains in `P`.

The phrase “globally locally Lipschitz” for the initial map in the primary draft is awkward. A precise version is “defined on the parameter domain, finite and componentwise convex, with a valid supporting affine row at each reference point where Theorem 2 is used.” Local Lipschitz continuity on a neighborhood is a convenient sufficient condition. Initial-map Lipschitz continuity is not needed for state existence at one fixed parameter. This wording issue does not invalidate the stated conclusions, because Theorem 2 separately assumes valid initial supporting rows.

## 4. Supporting rows and arbitrary references

If `g` is finite convex on all of `R^d` and nondecreasing in input `k`, every global subgradient `s` has `s_k≥0`. Indeed, if `s_k<0`, the support inequality at `u-te_k` gives `g(u-te_k)≥g(u)-ts_k>g(u)`, contradicting monotonicity. The unbounded negative test direction is available here because the field is globally defined. For a function defined only on a restricted state box, boundary subgradients of the restricted function would need more care.

Applying this fact row by row makes the selected state-gradient matrix Metzler. Bounded measurable coefficients suffice: shifting the diagonal by a common constant makes the matrix entrywise nonnegative almost everywhere, and the Peano–Baker expansion shows that the associated fundamental matrix has nonnegative entries. This justifies the comparison argument without smooth switching assumptions.

For Theorem 2, set

\[
w(t)=v(t,p)-v(t,p_0)-S(t)(p-p_0).
\]

Substitution of the *joint* subgradient inequality and the equation `S'=A+BS` gives `w'≥Bw` almost everywhere. The initial supporting rows give `w(0)≥0`. Variation of constants with the nonnegative transition matrix proves `w≥0` for every parameter. Equality at `p=p₀`, together with the global inequality, makes each row a genuine convex supporting row. The row need not be a classical sensitivity or a selected directional derivative. This distinction is correct and useful.

Theorem 3 is the same argument with `w=v-ell` and a global affine minorant of the field. Reference points can be arbitrary, can differ between rows, and can be empty endpoint objects. A reference trajectory need not satisfy either the physical or relaxed ODE. The support coefficients, however, must be fixed functions of time for a single resulting affine cut; choosing a different coefficient family separately for each candidate parameter does not define the affine function asserted by the theorem.

For an autonomous field, a global affine support remains a global support throughout a time slab. Exact matrix-exponential propagation of the resulting affine ODE is mathematically valid. The draft correctly distinguishes this from certified numerical propagation. Its final coefficient-error correction has the right sign: if the slope error is bounded componentwise by `epsilon_q`, then its worst possible contribution over the box is at most `epsilon_qᵀ max(|pᴸ|,|pᵁ|)`.

Generic AD is not enough to implement these proofs. At a finite maximum, any active affine row or convex combination of active rows is a valid subgradient. Through convex isotone compositions, nonnegative outer weights preserve valid inner supporting rows. Through the own-coordinate affine substitution, the complete transpose map must be applied. These rules construct actual joint subgradients and do not depend on claiming that an arbitrary algebraically equivalent program has valid AD derivatives.

## 5. A complete held-support recovery estimate

The draft states an `O(h)` recovery sketch. It can be completed under its uniform bounds without an additional differentiability assumption.

Fix `p₀`. Let `v` be the exact relaxation solution and select a supporting affine field at `y_j=ell(t_j,p₀)` on each slab. Let `L` bound the Lipschitz constant of `F(p₀,·)`, `K` bound the norms of the selected matrices `B_j`, and `M` bound `||v'||`. Use compatible vector and operator norms, put `C=L+K`, and let `h_j=t_{j+1}-t_j≤h`.

The nonnegative support deficit at the true state has norm at most

\[
\|F(p_0,v(t))-F(p_0,y_j)-B_j(v(t)-y_j)\|
\le C(\|e(t_j)\|+M(t-t_j)),
\]

where `e=v-ell`. Since `e'=B_j e+deficit`, variation of constants gives

\[
E_{j+1}\le e^{Kh_j}\left[(1+Ch_j)E_j+\frac{CM}{2}h_j^2\right],
\qquad E_j=\|e(t_j)\|.
\]

Using `1+Ch_j≤e^{Ch_j}` and iterating yields, also for a partial final slab,

\[
\|e(t)\|\le e^{(K+C)t}\left[\|e(0)\|+\frac{CM}{2}th\right].
\]

Thus exact initial contact gives uniform first-order recovery at the chosen parameter point. For a globally Lipschitz finite piecewise-affine field, the global `L,K` exist and `M` is finite on the finite true trajectory, even when the approximate references are outside the physical box. For merely locally bounded coefficients, all references and true states must lie in a common region where the constants apply, or an additional bootstrap argument is necessary. This is a consistency estimate for an established supporting-flow idea, not evidence of research priority.

## 6. Penalty refinement and its dual

The penalty refinement is a valid finite extension. The minimization domain `X` is nonempty and compact, and the objective is finite for every finite parameter and endpoint input. It is jointly convex in `(z,p,c,-C)`. Projection of its convex polyhedral epigraph gives a finite convex piecewise-affine value function. Increasing any signed endpoint increases or leaves unchanged the objective at every `z`, so it does the same to the minimum.

The Lipschitz estimate in the draft follows from the 1-Lipschitz positive-part and absolute-value maps by comparing objective values at an optimizer of either problem. Taking a maximum with the input endpoint and a box bound preserves global Lipschitz continuity; the Lipschitz constant of that final maximum also includes the identity input channel.

At a physical point enclosed by the supplied endpoints and satisfying the invariants, every penalty term vanishes. Evaluating there shows `h_{k,+}≤x_k` and `h_{k,-}≤-x_k`, including when `rho=0`. The final maxima therefore preserve the enclosure. Inconsistent endpoint inputs simply produce finite values that may be mutually inconsistent; the theorem needs exactly this behavior.

For the dual, use

\[
\rho(c_j-z_j)_+=\max_{0\le\alpha_j\le\rho}\alpha_j(c_j-z_j),
\quad
\rho(z_j-C_j)_+=\max_{0\le\beta_j\le\rho}\beta_j(z_j-C_j),
\]

and the analogous bounded dual representation of the residual 1-norm. The resulting function is affine in `z` and in the dual variables, over two compact convex domains. Minimax is applicable. Minimizing over each box coordinate gives `min(l_j a_j,u_j a_j)` with `a=s e_k-alpha+beta+Aᵀq`, exactly as in equation (8). All dual signs are correct.

A fixed feasible dual tuple is a global affine minorant of the value function, with nonnegative signed endpoint slopes `(alpha,beta)`. At an optimum it touches the value function and therefore supplies a genuine joint subgradient. A nonoptimal feasible tuple remains valid for Theorem 3 but need not be a subgradient or preserve contact for Theorem 2.

A finite fixed bundle, followed by the existing signed-bound maxima, preserves convexity, isotonicity, finiteness and bound preservation. Adaptive selection of pieces is safe if it merely evaluates the maximum of a fixed bundle. A parameter-dependent decision to omit pieces need not be convex. Similarly, arbitrary parameter-dependent penalty weights are outside the proof.

The exact-penalty statement in the opportunity note is sound on *nonempty hard feasible sets*. The hard constraint matrix is fixed, so a Hoffman constant can be chosen uniformly over varying right-hand sides for which the hard set is nonempty. Within `X`, box residuals vanish and the endpoint/invariant residual in the note controls the distance to the hard feasible set. A coefficient at least the appropriate distance constant times the coordinate objective's Lipschitz constant gives equality of the hard and penalized optimum. This is standard LP exact-penalty reasoning. It says nothing about a finite hard optimum on empty RPD input sets.

## 7. Integrated domination

Suppose the actual signed maps satisfy `H_new(p,w)≥H_old(p,w)` for every input, with the same own-coordinate substitution and base arithmetic. Then isotonicity gives `F_new(p,v)≥F_old(p,v)` for every `v`, including empty endpoint states. With the same initial condition, comparison of the cooperative fields gives `v_new≥v_old`. This is the correct direction: larger signed states mean tighter lower bounds and tighter upper bounds simultaneously.

The componentwise maximum of two admissible refinements is admissible and dominates each. Therefore `max(H_row,H_penalty)` gives the claimed no-loss extension of the source map. It must be the maximum of the maps actually used, with identical self-exclusion conventions and common base interval data. A statement that the coupled LP is tighter only on physically feasible input sets is insufficient, because the RPD field evaluates empty substituted inputs. The draft explicitly avoids that erroneous inference.

For fixed `rho₂≥rho₁`, the nonnegative residual gives `h(rho₂)≥h(rho₁)` pointwise on all inputs; the same argument proves integrated monotonicity in the fixed penalty weight. It does not compare independently chosen finite dual bundles that fail to preserve pointwise domination.

## 8. Exact independent check of the four-variable example

I enumerated the vertices with exact SymPy rational arithmetic and independently iterated individual-row bound propagation to a fixed point. The calculation used SymPy in the repository's isolated research environment and did not call the proposed refinement implementation.

For `0≤z≤1`, `sum(z)=1`, and `z₁+2z₂+3z₃+4z₄=5/2`, all vertices are

\[
(0,\tfrac12,\tfrac12,0),\quad
(0,\tfrac34,0,\tfrac14),\quad
(\tfrac14,0,\tfrac34,0),\quad
(\tfrac12,0,0,\tfrac12).
\]

Thus the exact upper bounds are `(1/2,3/4,3/4,1/2)`, as claimed. The original two rows reach the fixed upper bounds `(1,1,5/6,5/8)`. Reduced row echelon form gives

\[
z_1-z_3-2z_4=-\tfrac12,\qquad z_2+2z_3+3z_4=\tfrac32,
\]

whose row propagation reaches `(1,1,3/4,1/2)`. Lower bounds remain zero in each row-propagation calculation. Both fixed points were reached after the first sweep and confirmed unchanged by the second. This verifies the stated separation from those two particular row systems. It does not show a separation from all redundant-row generation or from variable elimination.

## 9. Priority and remaining limits

Ye–Scott (2023), Definitions 5–9, already supplies the most important abstract facts behind fixed-interval joint convexity. Closedness under coherence means that all finite signed endpoint pairs are in a fixed fiber's domain. Coherent concavity is precisely componentwise convexity after negating the upper output, and coherent inclusion monotonicity is isotonicity of the signed channels. A finite convex function on the entire finite-dimensional endpoint space is locally Lipschitz. Consequently the fixed-box local regularity implication is inherited from their theory even for other covered finite primitives. It does not by itself give uniform regularity while interval bounds vary in time or approach singular primitive domains.

Polynomial finite affine structure provides a stronger global growth statement and a finite support representation. Nevertheless, those conclusions are short deductions from the elementary rules, so practical value and genuinely additional capability will matter more than theorem count. The no-interiority support theorem and coupled finite refinement deserve exact comparison with Song–Khan's work. The author has also identified direct affine-enclosure prior art in Harwood–Barton (2018). I have not independently completed those full-text priority comparisons and do not certify novelty.

No new missing literature was identified during this review beyond sources already routed to the shared literature agent. No knowledge-base additions or retrieval checks were run by this reviewer. The review is complete for the mathematical statements above; implementation correctness, numerical certification, comparative reactor results and priority remain separate tasks.

## 10. Independent prototype audit and a corrected exactness defect

Root subsequently requested a review of [extended_rpd.py](../code/research_20260912/extended_rpd.py). I reviewed its sign-selected multiplication, signed row updates, own-coordinate substitutions, finite dual bundles, penalty-dual LP, and the two physical model factories. The audited post-fix source has SHA-256 `7b0cd7a109d71624bd5e4709cc68cd53f558bc9fb0f009e2b88f525c794724a3`.

**A real exactness bug was found and fixed.** Before normalization of model metadata, ordinary integer invariant coefficients could undergo Python division and become floating-point numbers. For the two-state system `x₀'=x₁`, `x₁'=0`, box `[0,1]²` and invariant `3x₁=1`, supply integer metadata and reference signed endpoints `(0,0,0,-1)`. One row sweep produced the constant signed-upper support

\[
-\frac{6004799503160661}{18014398509481984}
=-\frac13+\frac1{54043195528445952}.
\]

This exceeds the true signed derivative `-1/3`. Its small numerical size does not excuse it in a purported exact certificate. Root fixed the defect by converting every model metadata entry to `Fraction` before arithmetic, rejecting implicit floating-point model constants, and checking dimensions and box order. Re-running the same example now returns the exact valid bound `-1/3`.

I also found that a constant-only RHS component raised `AttributeError` when the compiler attempted to read its `.cv` member. Root fixed it by converting scalar RHS outputs into constant McCormick objects. The same exact regression example now uses a literal zero RHS component and passes.

The multiplication coefficients and the signs in the penalty-support/dual implementation are correct. For the code's invariant convention `Ax=b+Dp`, the dual contains `-qᵀ(b+Dp)`; its LP minimizes the negative of that dual objective. The inequalities representing the box minimum have the correct signs. Repaired dual multipliers are clamped to exact rational bounds and the intercept is recomputed with exact arithmetic, so solver objective values and approximate optimality are unnecessary for validity. Feasible nonoptimal tuples can weaken a cut but cannot invalidate it.

The bundle implementation applies its finite supports to the row-refined endpoints, retains the row-refined endpoints in each maximum, and evaluates all coordinate bundles against the same pre-bundle input. Thus it implements a fixed sequential composition of two admissible refinements. This preserves the structural guarantees and dominates the row-refined map. It should be described as that particular composition when reporting comparisons, rather than silently identifying it with a different simultaneous update. The row propagation also uses fixed interval data; equivalence to every detail of a source implementation is not established by this review.

Floating-point values are used to choose among exact affine minorants. Every such choice remains a global minorant, including if rounding picks an inactive piece. Therefore the compiler is suitable for the validity assertion in Theorem 3. Contact or exact subgradient assertions in Theorem 2 need genuinely active choices; they must not be inferred from an approximate floating comparison near a tie. The nominal numerical RHS can differ from the ideal finite-max field by selection roundoff. The draft's separate exact-support certificate construction does not need to assume otherwise.

The model tubes have direct proofs. For dimerization, each species derivative is nonnegative on its zero boundary, and `A+2B=1` is conserved; hence `0≤A≤1`, `0≤B≤1/2`. For shift/methanation, mass-action positivity gives nonnegative derivatives on each species' zero boundary. The conserved inventories are carbon `CO+CO₂+CH₄=p_CO`, oxygen `CO+H₂O+2CO₂=p_CO+p_H₂O`, and hydrogen `2H₂O+2H₂+4CH₄=4+2p_H₂O`. With both feeds in `[1/2,3/2]`, these imply exactly the declared respective upper bounds `(3/2,3,3/2,7/2,3/2)`. Polynomial local existence, positivity and these compact bounds give global physical existence. These are stylized kinetic models; the tube proof does not turn their chosen rates into fitted process data.

I wrote a separate value-only arithmetic implementation in [verify_extended_rpd_independent.py](../code/research_20260912/verify_extended_rpd_independent.py). It uses ordinary lower/upper channels, exact rational max/min values and independent row/bundle evaluation, and does not reuse the compiler's `Affine` or `MC` arithmetic. The test covers both physical factories and an artificial mixed-sign polynomial model; zero, one and two invariant sweeps; both self-exclusion settings; fixed bundles present and absent; and rational endpoint values well outside the physical boxes, including inconsistent pairs. The two exact regressions above are retained.

The [saved validation report](../code/research_20260912/extended-rpd-independent-validation.json) records all checks passing:

- 8,640 exact global affine support inequalities at independent query points;
- 1,080 exact Metzler and rational-coefficient row checks;
- 216 exact contact checks at selected integer reference points;
- 4,320 exact pointwise field-domination comparisons for adding bundles;
- 18 repaired bounded rational dual tuples;
- 140 exact physical zero-boundary checks, supplemented by exact conservation checks and the analytic tube proof above;
- both discovered regressions.

Reproduction command:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/verify_extended_rpd_independent.py
```

No remaining defect was found for the documented exact-input prototype scope. This audit does not verify the separate rational linear-flow integrator, certify an ordinary floating-point ODE solve, validate arbitrary user-supplied invariant/tube claims, or establish computational advantage. The author also incorporated the explicit held-support rate bound above as equation (9); I rechecked that transcription and its recurrence and found them correct.
