# Independent Stage 3 review 1

Reviewed all Stage 3 manuscript additions, the extended scalar-certificate appendix, both relevant scripts, bibliography and main-file integration, and their dependence on the preceding sections. I did not read other reviewer reports or communicate with reviewers. Pending final front matter and future stages were excluded.

**Verdict: no major issues found.** The substantive Stage 3 arguments withstand independent rederivation. I found one small endpoint-scope omission.

## Required minor repair

**MINOR — state $r\geq2$ for the unused-coordinate example.** `sections/04a-coupled-barriers.tex:410–431`, Example `ex:vertex-singular`, introduces $\Gamma_{r-1}$ and a positive-rank construction with $n=r-1$ without imposing $r\geq2$. The section's initial setup does not impose this globally; the earlier $r\geq2$ is inside another theorem. At $r=1$, the exact-parameter assertion is valid ($F_0=2b$, parameter two), but the subsequent $\Gamma_0$ construction and division by its linear asymptotic are outside the stated positive-rank definitions. **Repair:** begin the example “For $r\geq2$, …”. There is no need to add a separate rank-one case, since the example's purpose is a regular unused coordinate.

No other mandatory mathematical, citation, or prose repair was identified. In particular, the new radial upper bound is supported by a complete proof, rather than inferred from its metric comparison alone.

## Independent mathematical checks

### Normalized scalar theorem and accurate endpoints

- Re-derived $v=f'/\sqrt{f''}$ and $v'=v(1-vf'''/[2(f'')^{3/2}])\geq v(1-v)$. The positive-branch normalization gives $0<v\leq1$; its limiting value is one. The integrable negative tail follows from the finite metric coordinate, and the positive tail follows from the differential inequality once $v\geq1/2$.
- Checked that $x'(t)=e^{-t}v(t)^2$ proves the right endpoint is finite and identifies it using full positive gradient range. The tail integral then gives both central gap bounds used later. These facts do not require an unproved symmetry of $f$.
- The fixed-profile sharpness argument has an $O_{f,r}(1)$ error, with the profile held fixed while the objective separation grows. It correctly gives an exact supremum for each fixed $f,r$.
- Re-derived $p_f'=\sqrt{f''}$ and $|p_f''|\leq p_f'$, $p_f\leq p_f'$. The accurate-endpoint problem need not be convex, and the manuscript does not assume that it is. A minimizing nonnegative metric vector exists; positivity follows from the first-order gap/second-order norm perturbation at a zero coordinate. Necessary Lagrange multiplier conditions suffice. The multiplier's factor is consistently absorbed into its definition, and choosing $\eta=\lambda/\log2$ gives the claimed coordinatewise accuracy comparison.
- Checked the general fixed-profile dyadic theorem against the same data, not a modified accuracy scale. A fixed shift in activation thresholds and the window $[T-\log8,T]$ suffice. Actual terminal accuracy forces the first coordinate's metric position, and the initial tube bounds the starting potential. The growing-tube powers and dependence of constants on the fixed profile are consistent.

### Relaxed envelope, its unique maximizer, and the nonmonotone example

- Independently integrated the envelope differential inequalities for $\upsilon=p/p'$. The initial range $1-e^{-a}\leq\upsilon(a)\leq\min(1,e^a-1)$ and safe scale $k=\log2$ are correct. The upper trajectory $\min(1,(1+u)e^q-1)$ gives the displayed two time formulas, both decreasing in the initial value $u$. Substituting its least feasible value yields the exact relaxed envelope.
- Checked the branch switch, matching first derivatives, both endpoint limits, and both proofs of strict $C(a)<2$. The polynomial lower bound on the second branch has the stated positive minimum.
- Checked uniqueness separately from attainment. On the first branch $B$ is strictly convex and $aB'-B>0$. On the second branch $B''<0$: the exponential inequality follows from the indicated Taylor bounds. Thus $aB'-B$ decreases from a positive value to $-\infty$ and has exactly one zero. This proves uniqueness of the maximizer of $C_{\mathrm{sc}}$, without making any claim about uniqueness for $c_\star$.
- The piecewise differentiable extremizer is admissible for the explicitly relaxed problem, and reconstructing $p$ gives the required behavior at zero. The manuscript appropriately avoids turning this into a stronger smooth-barrier or arclength minimax claim.
- Checked every derivative and endpoint claim for the globally smooth $P_A,X_A,Z_A$ construction. Its self-concordance follows directly from $|P_A'|<P_A$, its finite interval and two-sided blow-up are proved, and its gradient range is full. The stated parameter bounds are valid. For the sharpness argument, all translated windows lie before the terminal parameter, are disjoint for sufficiently large $A$, and each yields the claimed coordinate gain. The endpoint estimate is uniform with $r,\delta,B$ fixed before the limit in $A$. The subsequent limit in $\delta$ gives $\sqrt r$ and does not contradict a fixed-parameter bound.

### Canonical barriers and general spectral transfer

- Checked the polar-volume factorization for the universal cube barrier and the product integral/Fenchel conjugate factorization for the entropic barrier. The scalar entropic gradient norm tends to one and satisfies the positive-branch normalization. The global standard self-concordance input is explicitly attributed to Chewi's theorem.
- The trace-Hessian derivation by polynomial approximation is valid for $C^2$ functions on compact spectral intervals: approximating $f''$ and integrating twice controls divided differences and the diagonal derivatives. Positivity of off-frame terms gives spectral contraction, and fixed-frame interpolation attains the radial lower bound. The proof distinguishes metric conclusions from standard self-concordance of the lift, which is not a consequence asserted here.
- For non-even Jordan profiles, the objectives are expressly positive spectral support objectives; alignment and replacing below-center coordinates are valid in that scope. The rectangular transfer adds the necessary evenness and centered-domain hypotheses.

### Facet coupling and exact parameters

- The full-collar entry argument is sound: convexity in the first coordinate bounds its gradient outside the collar by its value at the collar boundary. Large first forcing therefore implies entry, irrespective of the other coordinates. A bound only near a vertex would not suffice, and the manuscript says so.
- Re-derived the restricted inverse-quadratic variational bound and its direction. Bounded gradient implies the activated scalar terms tend uniformly to one after a fixed threshold, giving the prefix arc lower bound. The comparison curve has finite initial cost, stays in the collar, and has bounded Euclidean total variation, so its additional coupling length is $O(1)$ in the separation parameter.
- The same-accuracy extension legitimately chooses the actual terminal gap. Strict monotonicity of the central objective makes that the first accurate center; target-set distance is no larger than its endpoint distance. No new geometric lower bound is needed for this implication.
- Re-derived the dense Sherman–Morrison expression, $|B|\leq m$, $A\leq m/2$, and the correction bound $17m/32$. For the radial barrier, the numerator/denominator difference factors exactly as written; its bracket decreases to a nonnegative value. The boundary directional gradient ratio proves the reverse parameter inequality. Neither exact-parameter conclusion relies only on the generic sum certificate.

### Uniform radial upper bound and full-family finite sequences

- Re-derived the global Hessian sandwich. The diagonal relative term is at most $1/4$, while the rank-one term is at most $2\lambda t/(4\lambda+t)^2\leq1/8$. This holds on the entire cube, including outside the active-coordinate subspace.
- Differentiating stationarity gives the stated formula for $a'$. The bound $K\leq t$ is valid coordinatewise, hence $0\leq a'\leq1/4$. The effective logarithmic velocities satisfy $7/10\leq\theta_i\leq5/4$, so all coordinates increase. The auxiliary $v_i$ are ordered even though the actual velocities need not be. The proof applies the prefix inequality to the auxiliary velocities and then uses both sides of the $\theta_i$ bounds; the resulting factor $\sqrt{11/8}\,25/14$ is correct.
- For same accuracy, $4z_i/5\leq q_i\leq z_i$ brackets the radial center against standard centers. The standard profile inequality $H(s+\log a)\leq aH(s)$ follows from $v'\leq v$ and integration. The extra $5/4$ and $c_\star$ factors appear exactly once, and the final comparison uses metric domination for the full accurate target set.
- Checked the full-family dyadic proof with parameters allowed to vary with $r$. All shifted thresholds and speed constants are absolute. The stopping label $T+\log(5/4)$ gives actual accuracy for the same $\varepsilon_r$. The unrestricted route is measured in $F$, using the global sandwich, while the target-distance lower bound follows from $F\succeq U$. The progress argument uses center-distance domination and monotone coordinates to clip arbitrary labels. Initialization and final coordinate accuracy force net progress; no monotonicity of labels or prescribed end labels is hidden in the proof.
- The vertex-singular example's bounded perturbation estimates hold along both required paths because the unused coordinate stays small. Its exact parameter and lower comparison are sound for the intended $r\geq2$ case.

### Every-maximizer localization for $c_\star$

Checked the logic of the three elasticity exclusions, the monotonic map $E=Y(v)/v$, the strict rational localization intervals, and the final radical conversion. Since a known witness has ratio strictly above $a_0$, every global maximizer is excluded from the regions where the scalar dilation by $a_0$ already succeeds. This does locate every maximizer without assuming uniqueness. Differentiating $P(W)=YA$ gives exactly the displayed stationary equation.

## Execution, literature, and build

Read and ran `verify_barrier_dependence.py` and the extended `verify_scalar_certificate.py` under `/workspace/local-home/miniconda3/envs/qipm/bin/python`; both passed. The former remains numerical evidence, while the latter proves the displayed finite rational arithmetic bounds.

Additional independently written checks, rather than only rerunning supplied code:

- Tested the dense parameter formula on 240 arbitrary signed points in dimensions 2, 5, and 20. Direct Hessian solves and the closed formula agreed within $5.33\times10^{-15}$; every parameter ratio was below one.
- Reconstructed the extremizing relaxed velocity and numerically integrated its hitting time at $a=0.05,0.3,0.65,1,3$. These agree with both branches of the formula; the value near $a=0.65$ was approximately $1.831856409$.
- Checked radial metric and parameter bounds near vertices for $(r,\lambda)=(2,1),(20,1),(20,10^4)$ and distances $10^{-2},10^{-4},10^{-6}$ from the vertex. The relative Hessians obeyed the sandwich, and the gradient ratios approached $r$ from below.

Read the literature README before corpus access. Independently checked Chewi's primary theorem and tensorization setup and Castro–Cuesta's primary diagonal regularization discussion and parameter conclusion. These support the manuscript's attribution and its narrower distinction for dense/radial couplings. The new formulas are not presented as new definitions of canonical barriers. The existing NT/NN comparison and the differing parameter regimes remain compatible. The broader final novelty synthesis is still appropriately deferred to the final stage.

Inspected the current final LaTeX log rather than causing a shared build race: it reports a 34-page PDF with no undefined-reference, undefined-citation, overfull-box, or warning matches. The substantive exposition is sufficient for the intended reader; I identified no additional mandatory editorial repair.
