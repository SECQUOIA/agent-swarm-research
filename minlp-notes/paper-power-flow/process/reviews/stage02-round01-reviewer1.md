# Stage 2, round 1 — independent reviewer 1

**Verdict: PASS. No major or minor issue requiring correction found.**

I independently reviewed the complete frozen stage-2 manuscript at `paper-power-flow/process/snapshots/stage02-round01`, concentrating on every statement and proof of `sections/03-ac.tex`, the updated abstract and bibliography, the AC checker, and dependencies on the accepted resistive section. I did not read other reviewers' reports. I verified every hash in the frozen manifest. My artifacts are confined to `paper-power-flow/verification/reviewer1/stage02-round01/`.

## Mathematical audit

1. **Rectangular power signs and model scope.** Directly expanding `U_i conjugate(s_i U_i + Σ y_ij(U_i−U_j))` gives the printed signs: `P=h r²+Σ[g(r²−H)−bD]` and `Q=−t r²+Σ[−b(r²−H)−gD]`, where `D=Im(U_i conjugate(U_j))`. The definition explicitly permits the pinned/interval combinations used in the hardness construction. Strictly positive magnitude lower bounds exclude zero phasors. The general membership theorem handles signed susceptances, nonnegative conductances including purely imaginary lines, and shunts; the hardness claims correctly restrict to positive purely resistive lines without shunts.

2. **Cosine test at all advertised endpoints.** `H≥c r_i r_j` is equivalent to the principal angle bound for every `−1<c≤1`. There is no invalid squaring when `c<0`. The strict lower exclusion `c>−1` rules out antipodal phasors, and `c=1` legitimately forces equal directions. The `r_i` variables have the positive magnitude bounds and squared-norm equality needed for this equivalence.

3. **Crossing lemma, including axes and long arcs.** I checked the argument cases `a<−π`, `|a|<π`, and `a>π` independently. On the first case the endpoint in the open lower half-plane is the start, the endpoint in the closed upper half-plane is the end, and `D>0`; the reverse case gives `−1`. The negative-real-axis endpoint does not cause a false positive because the determinant sign excludes it. Positive-real-axis arrivals/departures follow the half-open convention. Identical directions give zero; antipodal directions are excluded. The formula uses directions only, so unequal magnitudes cannot change its result. The proof works for short arcs longer than `π/2` as claimed.

4. **Cycle lift, orientations, and membership.** The choice `j→i`, `δ_ij=arg(U_i conjugate(U_j))`, and the orientation multiplier in the cycle sums are mutually consistent. The principal-difference sum equals `2π` times the integer crossing sum. If every fundamental sum vanishes, extending real arguments on a spanning forest gives the same differences on every non-tree edge. Conversely every admissible real lift has precisely the principal difference on each edge because both lie strictly between `−π` and `π`. Disconnected graphs, isolated vertices, and zero-angle limits introduce no missing case. The Boolean crossing encoding enforces `k∈{−1,0,1}` using real quantifiers and does not need hidden integer quantification. At most `|E|−|N|+κ` cycles, each of length at most `|N|`, suffice for a polynomial formula. No transcendental coefficient or equality enters the ETR instance.

5. **Equal-angle energy identity.** Pairing the terms in `−Σ θ_i Q_i` gives exactly the displayed positive weighted sum of `t sin t`. For real edge differences strictly below `π` in absolute value, this forces every difference to vanish. The converse and reduction to the original resistive injections are immediate substitutions. Thus the fixed choice `c=0`, together with the stage-1 reduction, proves the stated AC completeness and conditional NP consequence. The proof does not silently assume convexity, stability, positive cosine, or uniqueness for principal-angle profiles.

6. **One-sided reactive intervals.** In the specified shunt-free, purely resistive network, line antisymmetry gives `ΣQ_i=0` even before imposing angle bounds. A common weak sign then forces every reactive injection to zero. Hence replacing `[0,0]` by `[0,1]` preserves the feasible set in each of the three restricted formulations. The text accurately distinguishes this saturation identity from symmetric-tolerance robustness.

7. **Winding counterexamples and rational data.** On the regular `n`-cycle, neighbor sine terms cancel, active injections are `2(1−cos(2π/n))>0`, and the cyclic principal-difference sum is `2π`. For each fixed rational `c<1`, a sufficiently large `n` satisfies the angle limit. Rational positive enclosing injection endpoints exist even if the witness powers are irrational; the proposition claims existence, not a uniform fixed-alphabet reduction here. With all resistive voltages pinned to one, every resistive injection is zero, making the corresponding resistive instance infeasible. The explicit four-cycle has rational singleton power two and cosine zero. The one-edge `π` example correctly establishes the failure of the energy conclusion at that excluded endpoint.

8. **Small cycle budgets and strictly positive principal windows.** Every fundamental-cycle sum is an integer multiple of `2π`; its absolute value is less than `2π` under the stated strict budget, so it vanishes. The concavity inequality gives `γ_n≤π/(sqrt(2)n)` for `c_n=1−1/n²`. Every simple fundamental cycle has at most `n` edges. This proves the real lift needed for the transfer. The positive window, `O(log n)` cosine encoding, distinction from fixed numerical data, and harmless isolated-bus padding are all correct. Forests have the lift property vacuously; no unproved forest tractability claim is made.

9. **Rectangular bus-angle boxes.** Together with positive magnitude, `e≥|f|` implies `e>0` and uniquely gives an argument in `[-π/4,π/4]`. Real edge differences are within `[-π/2,π/2]`. The equal-angle lemma and one reference per component force every imaginary part to zero, and every resistive solution extends. This proves the exact feasible-set statement as well as completeness. No additional line-angle constraints are needed.

## Sources and clarity

The current abstract accurately summarizes the established stage-1 and stage-2 results. The distinctions among real angle limits, principal-only limits, and rectangular bus boxes are explicit and essential. The paper does not present the principal-only counterexample as a hardness classification for every fixed positive window.

I checked the Dörfler–Chertkov–Bullo primary source at [arXiv:1208.0045v1](https://arxiv.org/html/1208.0045v1). Equation (1) supplies the weighted sine-coupled equilibrium equation, and the phase-cohesiveness discussion supports the limited background attribution used in this manuscript. The paper does not import the source's stronger global uniqueness claims; its real-lift energy lemma is independently proved. No source-support repair is needed.

The stage-1 homeomorphism direction finding is corrected in the dependency section. I found no new consistency problem between the sections.

## Verification

- The frozen manuscript builds cleanly with `latexmk` in my own output directory; the final log contains no unresolved citations/references, overfull boxes, or underfull boxes.
- The AC exact checker passes: **2,112 scaled short-arc pairs**, including **768 arcs longer than `π/2`**; **14,784 rational cosine checks**; **177,168 closed cycles/walks compared against a rotated cut**, including **59,640 nonzero winding cases**; and **648 exact complex-power sign cases**. Explicit regressions cover unequal radii, antipodal exclusion, the rational four-cycle, reactive cancellation, and polynomial-bit cosine inputs.
- I additionally wrote and ran an independent integer-coordinate phasor diagnostic comparing the crossing formula with `atan2`. It uses exact integer signs and floating-point angle evaluation only as a diagnostic; its script and log are retained alongside the exact-check output. This is not presented as a proof or exact certificate.
- I read the checker itself. It tests finite residuals and cut invariance rather than proving the universal cycle criterion or a quantified complexity theorem. Its docstring and output state this limitation accurately. The universal statements above are supported by the mathematical proofs, which I checked separately.

I have no required revisions and no optional future-research request to attach to this stage.
