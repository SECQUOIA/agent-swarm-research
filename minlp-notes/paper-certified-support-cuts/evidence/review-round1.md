# R1-math

I checked every statement and proof in Sections 2-7 and Appendix A (including A2-star-proof), plus the related-work claims in 02b-related.tex. I found no critical error. Every theorem, proposition, lemma and example I checked is correct as proved, and every numerical constant I recomputed matches.

**Exact checks done, with sympy/fractions scripts under /workspace/minlp-notes/paper-certified-support-cuts/verification/:**
- Examples 4.5 and 4.7, including the D=[0,2] example. The tangent point is -1/2, the envelope value at 0 is -1/4, and the cut v1-v2>=0 is violated by 1/4.
- The triangle example and its RLT identity.
- Proposition 6.1. Both measures give exactly v̄. The minimum is 1/128, attained only at (1,11/16,1). The cut has right-hand side -7/128 and violation 1/128. The reduced objective equals D at binary leaves and gives the same witness and gap.
- The (sdp-identity): its symbolic residual is 0.
- Proposition A.1. On three interleaving configurations the three p_xz formulas agree, they violate p_xz<=min(m_x,m_z), and the unique completion is PSD with determinant 0.
- Theorem 6.2(ii). A measure-LP check on 150 random two-point configurations matched 0 or δ²/2 (error below 1e-13). The certificate multipliers of Appendix A.2 were checked exactly on about 2000 random rational separated and nested instances.
- Theorem 6.3. Alternation versus moment-matching LP feasibility agreed on 7500 random cases.
- Proposition 6.4 for r=1,2,3. The sets A and C are as stated, the minimum is 1/2, the binomial weights match all moments up to k=2^{r+1}-2, and D_L has no x_j² terms.
- Theorem 5.4. On 177 random constrained stars the per-leaf and total breakpoint bounds held and the exact minimum agreed with a grid check. Concave leaves reach 2s_i-3 breakpoints for s_i=3,4.
- The Ben-Or star: V equals the sum of negative tents exactly.
- Remark 5.5. The conditional value is min{-1/8,-(1-t)²/4}, the switch point is 1-√2/2, and min f=-3/8 at (1,0,1/2).
- Theorem 5.1. On 60 random indefinite and degenerate polytopes the candidate minimum was never above a feasible value. The Hadamard bound B of Appendix A.1 was never exceeded.
- Lemma 7.1. LP duality with cone coordinates holds (gap below 1e-15).
- Theorem 7.2. Column generation stayed within the call bound and kept the pairwise direction separation.
- The Bernstein coefficient formula and the chord-lemma algebra.
- The ellipsoid appendix (GLS 3.2.1 iteration count, the post-hoc K* argument, and the box-of-side-ρ volume step), checked by hand against GLS in the local literature base.

**Cited results I confirmed in the local literature base:**
- Del Pia-Khajavirad: O(n²) on forests, the O(d_v m_v) root merge, and quartic strongly NP-hard on paths (Theorem 2).
- Burer-Natarajan-Willemsen Theorem 1.
- Padberg Proposition 8.
- Dey-Khajavirad Corollary 1, which assumes no plus loop on the separator.
- GLS (4.4.7) and (3.2.1).
- Lasserre 2006, Lemma 6.3 and Theorem 3.7.
- Chen-Luedtke Theorem 3.
- Anstreicher-Burer 2010. This one is cited too broadly in Related Work; see the findings.

**What remains:**
- One false-as-stated complexity bound in Theorem 5.4: rows in y alone are not counted. It is repeated in the abstract and introduction.
- A bookkeeping gap in the star bit-length appendix.
- Several imprecise summary sentences, where "δ²/2 exactly when interleave" fails in the touching case and "counts attained" is overstated.
- One unproved existence step in Appendix A.4.
- Small hypothesis gaps in Section 7 (initial W, rational F values, R>0) and in Proposition 4.1 (min versus inf).
- One overbroad citation of Anstreicher-Burer.
- A few suggestions on missing examples and notation.

None of these changes a result.

## [major] sections/05b-star.tex lines 31-39 (Theorem 5.4 statement); also sections/00-abstract.tex line 15 and sections/01-introduction.tex lines 73-75

**Issue.** The operation bound O((m+k)log(m+k)) is false as stated. The domain may contain rows in y alone: line 13 allows rows that involve y and *at most one* leaf, so zero leaves are allowed. But m counts only rows that involve a leaf. With k=1, m=0 and m_0 rows in y alone, any algorithm must read all m_0 rows to compute I, because each may be binding. That costs Omega(m_0) operations, while the claimed bound is O(1). The same bound is repeated in the abstract and the introduction.

**Fix.** State the bound with the center-only rows counted. Theorem: "Let m be the number of rows that involve a leaf and m_0 the number of rows that involve y alone ... with O(m_0+(m+k)\log(m+k)) arithmetic operations and comparisons." Add to the proof: "Intersecting the bounds of y with the m_0 rows in y alone costs O(m_0)." Alternatively, assume that rows in y alone have already been reduced to bounds on y. Update the abstract and the introduction the same way.

**Evidence.** The proof's operation count (lines 73-79) covers envelopes, sorting and the sweep only. Computing I (lines 26-28) also uses the rows in y alone, and these are not included in m.

## [minor] sections/A2-star-proof.tex lines 5-7 and 11-17

**Issue.** The definition "σ=max_i σ_i" comes after σ_i is defined for leaves and σ_0 separately for the center, so it reads as excluding σ_0. The candidates for the minimum include the endpoints of I that come from the bounds of y and from rows in y alone; these have η<=2σ_0. These endpoints are neither intersections of leaf lines nor zeros of the endpoint factor, so the bound "η<=12σ+4" does not cover them. The final bound "η<=4C+36σ+14" then fails to follow at those endpoints when σ_0 is much larger than σ. Evaluating c2 y² there gives about C+4σ_0, and 3C+6σ_0+2<=4C+36σ+14 is not implied. Polynomiality is unaffected.

**Fix.** Write "σ=\max_{0\le i\le k}\sigma_i". Add after the breakpoint bound: "Endpoints of I are bounds of y, zeros of rows in y alone (η<=2σ_0) or intersections of two lines of one leaf, so every breakpoint and every endpoint of I has η<=12σ+4."

**Evidence.** I recomputed each bound: lines η<=2σ_i; v_i η<=2σ_i+1; intersections η<=8σ+6; endpoint-factor zeros η<=12σ+4; piece coefficients η<=11σ_i+7; value at a breakpoint η<=3C+36σ+14; value at a stationary point η<=4C+3. Each holds only if σ also bounds the center data. development/M3.md (Theorem 5, item 2) makes the same implicit assumption.

## [minor] sections/06-composition.tex lines 93-95 (sentence after Theorem 6.2); sections/01-introduction.tex lines 83-84

**Issue.** The text says "it is δ²/2 exactly when A and C interleave". When A∩C≠∅, δ=0, so the gap is 0=δ²/2 without interleaving, because the definition of interleaving requires disjoint sets. As written, "exactly when" is false in that case.

**Fix.** Replace with: "The gap between H and R in the direction of D is therefore either 0 or δ²/2; it is positive exactly when A and C interleave, and then it equals δ²/2." Make the same change in the introduction: "... the gap is positive, and equal to δ²/2, exactly when two two-point sets interleave."

**Evidence.** Theorem 6.2(i)-(ii) with A∩C≠∅ gives box minimum 0 and minimum over R equal to 0.

## [minor] sections/A-proofs.tex lines 134-137 (remark after Proposition A.1)

**Issue.** The text says "The positive semidefinite completion in this proof is unique, so the dense moment matrix alone does not exclude the zero-value point." The proof shows only uniqueness: if M⪰0, then p_xz is forced. It does not show that a PSD completion exists. The claim that "neither ingredient alone suffices" needs existence.

**Fix.** Add: "A completion exists: on the two supports x=α+βy and z=α'+β'y, so with p_xz=E[(α+βy)(α'+β'y)] computed from (m_y,s_y), M=L^T M_y L, where M_y=[[1,m_y],[m_y,s_y]]⪰0 and L maps (1,y) to (1,x,y,z). Hence M⪰0."

**Evidence.** For the configurations (1/4,3/4,0,5/8), (0,2,1,3) and (1,3,0,2), the three formulas for p_xz agree (3/5, 3/8, 3/8). The completed M has all eigenvalues >=0 and det M=0 (verification/R1-math_algebra.py).

## [minor] sections/07-separation.tex lines 17-19, 61-73 and 78-80 (setup, column-generation procedure, Theorem 7.2)

**Issue.** Three hypotheses are missing.
(i) The initial set W is not specified. If W is empty, the master LP has value +infinity and there is no optimal direction.
(ii) F is only assumed continuous, but the procedure solves the master LP exactly over w=F(p)-z̄. That requires F(p) to be rational at rational p, as for polynomials with rational coefficients. For exp, log and similar functions this fails.
(iii) The bound 2k⌈2R/(ε-δ)⌉^{k-1} and the proof's division by R need R>0. The appendix assumes R>0; Theorem 7.2 does not.

**Fix.** Add: "Initialize W={F(p_0)-z̄} for some p_0∈P (for example a vertex); if F(p_0)=z̄, stop with a one-point certificate." Add to the setup: "for exact arithmetic we assume F(P∩Q^d)⊆Q^k, for example F polynomial with rational coefficients." Add to Theorem 7.2: "If R=0, then F≡z̄ on P and the procedure stops without an oracle call."

**Evidence.** development/M5.md (Theorem 5.2) has an initial point p_0 and the case T=0 if F(p_0)=q. The paper dropped both.

## [minor] sections/02b-related.tex lines 42-45

**Issue.** The text says the hull of {(x,xx^T)} "over a simplex, a box in dimension two, and small triangulated polytopes is described by semidefinite and RLT constraints [AnstreicherBurer2010]". Anstreicher-Burer prove the simplex result only for n<=4 in the standard simplex {x>=0, e^T x=1}, that is, simplices of dimension at most three; their abstract notes a counterexample for n>4. Their triangulated-polytope result holds for n<=3 and is an extended (disjunctive) formulation built from the simplex pieces, not the SDP+RLT system itself.

**Fix.** Replace with: "The convex hull of {(x,xx^T)} is described by semidefinite and RLT constraints over a simplex of dimension at most three and over a box in dimension two, and for polytopes of dimension at most three a triangulation gives an extended formulation [AnstreicherBurer2010]; for boxes in higher dimension the SDP+RLT description is not exact [BurerLetchford2009, Anstreicher2012]."

**Evidence.** literature/papers/anstreicher2010-computable-representations-for-convex-hulls/fulltext.md, abstract and introduction: "If n ≤ 4 and F is a simplex ...", "A known counterexample shows that the representation for C does not hold when n > 4", and "for n ≤ 3 a representation for C can be obtained when F is any triangulated polytope".

## [minor] sections/01-introduction.tex lines 73-75

**Issue.** The introduction calls the star algorithm "optimal for algebraic computation trees" without a condition. The lower bound (Section 5.3, lines 85-89, and Appendix A.3) is proved only for instances with m=Θ(k): the hard family has 3r leaves and r rows. No lower bound is given for box-only stars (m=0).

**Fix.** Write: "... with O((m+k)\log(m+k)) arithmetic operations for k leaves and m rows, which is optimal for algebraic computation trees on instances with m=Θ(k)."

**Evidence.** sections/A2-star-proof.tex lines 22-37 build the hard family with m=r and k=3r.

## [minor] sections/05b-star.tex lines 82-85

**Issue.** "The counts in the proof are attained" overstates. The per-leaf bound 2s_i-3 for concave leaves is attained. The bound s_i+2 for convex leaves is not attained when s_i=2: a box leaf with d_i>0 has at most 2 rule changes, not 4. So the total 2m+4k+1 is not attained, for example on box stars. What the paragraph actually shows is Θ(m+k).

**Fix.** Replace with: "The bound is tight up to a constant factor. A single concave leaf whose bounds zigzag attains 2s_i-3 rule changes, and k hinge leaves force k more, so the partition can have Θ(m+k) intervals."

**Evidence.** In verification/R1-math_star.py, a random search found concave leaves with 2s_i-3 breakpoints for s_i=3 and 4. Over 5000 random convex box leaves the maximum number of breakpoints was 2, against the bound s_i+2=4.

## [minor] sections/04-original-variables.tex lines 24-38 (Proposition 4.1 and its setup)

**Issue.** φ is defined as a minimum over D, but g and h are not assumed continuous there; continuity first appears in Theorem 4.2. For discontinuous g or h the minimum need not be attained. The proposition only needs β<=inf.

**Fix.** In (eq:agg-support), replace "\min_{u\in D}" by "\inf_{u\in D}". Alternatively, add "with g and h continuous on the compact set D" to the setup at line 24.

**Evidence.** The proof (lines 41-44) uses only a^T Sv+λ^T g(Sv)+μ^T h(Sv)>=β at the given point, so the infimum suffices.

## [minor] sections/03-certification.tex lines 100-106 (Proposition 3.3)

**Issue.** The proposition first concludes min_j L_j<=inf_B p. It then says cells with min_{B_j} α^T x>γ "may be omitted from the minimum". After omission the valid conclusion is about the infimum over the row-constrained domain D=B∩{α^T x<=γ}, not over B; the statement does not say so. The symbols α and β are also reused here and in Lemma 3.4, after serving as Bernstein multi-indices in (eq:bernstein).

**Fix.** Replace the second and third sentences with: "Let D=\{x\in B:\alpha_r^{T}x\le\gamma_r,\ r\in\mathcal R\} and let O be the set of cells with \min_{B_j}\alpha_r^{T}x>\gamma_r for some r. Then \min_{j\notin O}L_j\le\inf_Dp, and if O contains every cell, D=\emptyset." Rename the row vector, for example to g^T x<=γ.

**Evidence.** This follows directly from the definitions.

## [minor] sections/03-certification.tex lines 116-155 (elementary grammar and Lemma 3.4)

**Issue.** The grammar includes |·|, and the text after the lemma (lines 153-155) says verified enclosures of p'' on the cell "are enough". Lemma 3.4 needs p∈C²; on a cell that contains a kink of |·|, p'' does not exist. An endpoint-only bound would then be invalid: for p=-|t| on [-1,1] the endpoints give -1, the true minimum is -1, but variants with an interior kink pointing down give a false bound. The paper does not say when the correction is switched off.

**Fix.** Add after line 155: "The correction is used only on cells where p is C² and a finite upper bound on p'' is verified; on a cell that contains a nondifferentiable point of the expression (for example a zero of the argument of |·|), only the natural enclosure is used."

**Evidence.** evidence/issues-raised.md BERN-3 records that unsupported or singular derivatives disable the correction in the implementation, but the paper does not state it.

## [minor] sections/04-original-variables.tex lines 130-143 (Corollary 4.3) and line 163 (proof of Proposition 4.4)

**Issue.** Notation is used without definition. Corollary 4.3 uses the convex envelope breve-h without defining it; only breve-g and hat-h are defined. The proof uses hat-g, which is never defined. The proof of Proposition 4.4 says each preimage is the closure of its group "over D", but the group's block domain is D^i. The result is the same, but as written it mixes the two blocks.

**Fix.** In Corollary 4.3 write: "... where \breve h(x)=\min\{y:(x,y)\in K\} and \hat h(x)=\max\{y:(x,y)\in K\} are the convex and concave envelopes of h over D." In the proof write: "the fiber is the interval [\breve g(x),\hat g(x)] with \hat g(x)=\max\{y:(x,y)\in K\}." In Proposition 4.4 write: "each preimage is the closure of its group over D^i."

**Evidence.** Checked by reading the definitions; the mathematics is correct.

## [minor] figures/chords.tex lines 39-41 (caption of Figure 1(b))

**Issue.** The caption says "by Theorem 6.2 the glued relaxation is exact". The theorem shows only that the minimum of the linearization of D over R equals δ²/2, that is, R is exact in the direction of D. R is not equal to H.

**Fix.** Replace with: "(b) Nested sets: the chords do not meet, and by Theorem 6.2 the glued relaxation gives the exact bound δ²/2 in the direction of D."

**Evidence.** Statement of Theorem 6.2(ii).

## [suggestion] sections/04-original-variables.tex lines 232-238 (hierarchy conv Σ ⊆ ∩_λ conv Σ_λ ⊆ C)

**Issue.** The text says "both inclusions can be strict". Example 4.7 shows only the second inclusion: there ∩_λ conv Σ_λ={1/2}=conv Σ. No example is given for the first, although the paper's own D=[0,2] example already shows it.

**Fix.** Add after the D=[0,2] example: "This example also shows that the first inclusion can be strict: for every λ≥0 the aggregated row defines a convex function of x whose chord over [0,2] equals 1 at x=1, so (1,1)∈conv Σ_λ for all λ, whereas z≤1/2 on conv Σ."

**Evidence.** For λ=(λ1,λ2), the row reads z<=[λ1(x-2)²+λ2x²]/(2(λ1+λ2)). Its values at x=0 and x=2 are 2λ1/(λ1+λ2) and 2λ2/(λ1+λ2), so their mean is 1, and (1,1) is the midpoint of two points of Σ_λ. conv Σ = {z <= min(x/2, 1-x/2)}.

## [suggestion] sections/06-composition.tex lines 311-312 (after Corollary 6.5)

**Issue.** "Pairwise intersections of the projections are not enough: they can all be nonempty while Δ>0" is stated without an example. By Helly's theorem in dimension one this can happen only when the argmin projections are not intervals, which deserves a one-line instance.

**Fix.** Add: "For example, with y∈[0,2] and leaves whose zero sets project to {0,1}, {1,2} and {0,2} (members of the family (eq:family)), the projections intersect pairwise but have no common point, and Δ=2/3."

**Evidence.** With the three D_A-type leaves, β_i=0, and min_y Σ_i dist(y,A_i)²=2/3, attained at y=2/3 (and symmetrically at y=4/3).

## [suggestion] sections/07-separation.tex (Section 7.1-7.2): nothing on why ε>0 is needed

**Issue.** A referee will ask why the contract needs a positive tolerance beyond complexity. With ε=0 a within-tolerance answer may have no rational certificate even for exact queries in the hull. The development notes have such an example (M5, Example 5.8); the paper omits it.

**Fix.** Add after Theorem 7.2: "A positive tolerance is needed even for certification: for P=[-3,3], F(t)=(t,(t^2-2)^2) and z̄=(0,0), z̄=\tfrac12F(\sqrt2)+\tfrac12F(-\sqrt2) lies in the hull, but the valid inequality z_2\ge0 is tight at z̄, so every representing mixture uses only the irrational points t=\pm\sqrt2."

**Evidence.** Checked by hand: z_2=(t²-2)²>=0 on the graph, with equality only at t=±√2.

## [suggestion] sections/04-original-variables.tex lines 80-83

**Issue.** "the classical fact that the Lagrangian dual of a nonconvex problem equals the dual of its convexification" is a weak paraphrase. The fact used, and cited (Falk, Geoffrion, Lemaréchal-Renaud), is that the Lagrangian dual bound equals the optimal value of the convexified primal in the joint space. Section 2's related work (line 34) states it correctly.

**Fix.** Replace with: "It is the set version of the classical fact that the Lagrangian dual bound of a nonconvex problem equals the optimal value of its convexification in the joint space of variables and constraint values."

**Evidence.** Consistent with sections/02b-related.tex lines 33-36.

## [suggestion] Notation across sections 5-7 and Appendix A (A-proofs.tex lines 5-32, 149; A2-star-proof.tex line 3; 05-quadratic-support.tex lines 93-94)

**Issue.** Symbols are heavily reused.
- η means an encoding bound (A.1), a log-height function (A.3) and (ε-δ)/2 (A.5).
- σ means a product of denominators (A.1), size bounds (A.3) and divided-difference weights (Theorem 6.3).
- k means the number of features, |S| in A.1, the number of leaves, the number of moments and the number of pairs (Corollary 6.5).
- R means the glued relaxation and the radius bound; Δ means a gain, a coefficient change and a determinant.
- Section 5.1 states the bit bound with λ_q and λ_A, while Appendix A.1 proves it with η and α, which makes it hard to match the two.

**Fix.** Use the main text's λ_q and λ_A in Appendix A.1. Rename the A.3 height function, for example to ht(·), and the A.5 constant, for example to τ. Use r or ℓ for the number of moments in Section 6.3, or say explicitly that k changes meaning there.

**Evidence.** Found by reading; it does not affect correctness.

# R2-math

No result in Sections 4-7 or Appendix A is wrong. The problems are overstatement, positioning, precision and notation.

**What I checked**
- **Section 4:** the proof of Theorem 4.2. Corollary 4.3, Propositions 4.4, 4.6 and 4.8, and Examples 4.5 and 4.7, including the envelope value -1/4 and the D=[0,2] example. Theorem 4.2 is correctly presented as the set version of "Lagrangian dual = convexified problem", with Chen–Luedtke credited for the argument.
- **Section 5:** the face-minimality argument of Theorem 5.1 and the Hadamard/Cramer bounds of App. A.1. The breakpoint and piece counts of Theorem 5.4, the bit-length argument, the Ben-Or construction including the tent identity, and the depth-two example. The comparison with Del Pia–Khajavirad is accurate: their O(k^2) root merge, box-only model and concave value functions.
- **Section 6:** every number in Prop. 6.1 and cut (14). The proof of Theorem 6.2 and the separated and nested multipliers in A.2. The run construction and divided-difference weights of Theorem 6.3 and A.3, and Prop. 6.4. Identity (16), checked symbolically, and Prop. A.1.
- **Section 7:** Lemma 7.1, the packing argument of Theorem 7.2, the ellipsoid argument in A.5 (GLS Theorem 3.2.1 confirmed in the KB), Lemma 7.3 and the grid fallback.

**Main issues**
1. Section 6's opening and the conclusions claim that Theorem 6.3 tells exactly when k-moment gluing fails. It only tells when the glued bound is zero. An exact k=3 instance has a positive glued bound below the true minimum.
2. The dense-SDP + McCormick(xz) closure is presented as a contribution "consistent with" Burer–Natarajan–Willemsen (2025). In fact their Theorem 1 implies it, for every objective on the three-variable box path. Dey–Khajavirad's stable-set theorem (their Theorem 2) also covers the reduced 1/128 instance exactly.
3. In Corollary 6.5, Delta depends on how the center terms are split among the pairs. Its minimum over re-splittings is the gap to R, a link the paper does not state.
4. An existence lemma for the PSD completion (chordal completion, Grone et al. 1984) is used but not stated.
5. Column generation is Kelley's method, and Brierley et al. (2016) already state the same output contract; the paper cites neither as such.
6. Smaller points: W is never initialized, Theorem 5.4's optimality claim needs its m = Theta(k) qualifier in the introduction, and one coNP-reduction sentence needs rewording.
7. Notation: k (five meanings), R, C, S, T, h, delta and r are reused across, and sometimes within, sections that refer to each other.

Theorem 6.3 could also note that, by Gordan's alternative, it amounts to the classical fact that the least degree of a polynomial that is positive on A and negative on C equals the number of alternations. Its Karlin–Studden attribution is otherwise appropriate.

**Checks run** (my own, all single-threaded; no project-wide tests or CI checks were run)
- `/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python /workspace/minlp-notes/paper-certified-support-cuts/verification/R2-math_checks.py`: witness PSD completion, cut arithmetic, and the exact k=3 counterexample to exactness.
- `/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python /workspace/minlp-notes/paper-certified-support-cuts/verification/R2-math_identity.py`: identity (16), and the re-split duality on the nested example.

Both scripts exited normally and every exact check passed.

## [major] sections/06-composition.tex lines 10-12 (Section 6 opening); sections/10-conclusions.tex lines 17-20; missing remark after Theorem 6.3 / Proposition 6.4 (06-composition.tex lines 183-217)

**Issue.** The text claims more than Theorem 6.3 proves. Section 6 says it 'determines precisely when gluing on a fixed number of shared moments fails', and the conclusions say glued pair hulls 'accept distributions that no joint distribution reproduces, exactly when the local zero sets alternate often enough'. Theorem 6.3 only says when the glued bound in the direction D_L+D_R is zero (a zero witness exists). When alt(A,C) <= k the bound is positive, but it can still be strictly below the true minimum. The 0-or-delta^2/2 dichotomy of Theorem 6.2 holds only for k=2 and two-point sets. The paper never says this, so readers will take 'detects' to mean 'closes'.

**Fix.** Line 11-12: replace 'and determines precisely when gluing on a fixed number of shared moments fails' with 'and determines exactly when gluing on k shared moments gives no positive bound at all'. Conclusions lines 17-20: replace with 'pair hulls glued on k moments of a shared variable give the trivial bound zero for a positive objective exactly when the local zero sets alternate at least k+1 times'. After Theorem 6.3, add: 'Theorem 6.3 characterizes zero glued bounds, not exactness. For k>=3 the glued bound can lie strictly between 0 and the minimum: for D_A=(y-2x)^2+4x(1-x), D_C=(y-1-2z)^2+4z(1-z) on y in [0,3] (A={0,2}, C={1,3}, alt(A,C)=3) and k=3, the measures 57/112 d_{15/32}+55/112 d_{57/32} and 22/117 d_0+1045/1456 d_{39/32}+95/1008 d_{81/32} have equal moments up to order three and give a glued value of at most 6103/16128 < 1/2 = min D. The dichotomy of Theorem 6.2 is specific to two shared moments.'

**Evidence.** Exact check in verification/R2-math_checks.py (sympy): the weights are nonnegative, the moments of orders 0..3 match exactly, and the value is 6103/16128 ≈ 0.378. The development note M4.md Section 3, Remark (iii) already reports this numerically (≈0.378 on [0,3], ≈0.238 on [-2,5], so the gap also depends on [l,u]). The paper omits it.

## [major] sections/06-composition.tex lines 241-267 (dense-relaxation paragraph); sections/01-introduction.tex lines 87-91; sections/10-conclusions.tex lines 20-23

**Issue.** This misstates what is new relative to Burer–Natarajan–Willemsen (2025). The paper calls the dense-SDP + McCormick(xz) closure of the family 'consistent with' their Theorem 1, and the introduction lists it as a contribution ('We also show ...'). Their Theorem 1 (local KB burer2025-on-the-semidefinite-representability-of) says: for n<=3, the Shor SDP with the RLT upper bounds X <= x e^T is tight for every submodular box QP. On a three-variable path, complementing x and/or z can always make the coefficients of xy and yz nonpositive, and the xz coefficient is zero. So the theorem gives exactness for every objective in the path coordinates, not just for the family D. The 'representation, not strength' conclusion therefore holds for every three-variable box path and follows from the published theorem. Identity (16) is an explicit certificate for a special case.

**Fix.** Replace 'This is consistent with a theorem of BNW...: ...a semidefinite relaxation with part of the RLT inequalities is exact. After an affine change ... has this sign pattern.' with: 'This is a special case of [BNW, Theorem 1]. On a three-variable path, complementing x or z makes the coefficients of xy and yz nonpositive, so the semidefinite relaxation with the RLT upper bounds (including those of the nonedge product xz) is exact for every objective on the path coordinates over the box. Identity (16) is an explicit certificate for the family.' In the introduction, change 'We also show that a dense semidefinite relaxation ... closes the whole family' to 'We also give an explicit certificate that a dense semidefinite relaxation with the McCormick inequalities of the missing product closes the whole family, a special case of a theorem of Burer, Natarajan and Willemsen'.

**Evidence.** BNW fulltext: 'Our main result in Theorem 1 states that this relaxation is tight when n <= 3, for every submodular (Q, c)'. The relaxation (2) is Y(x,X) PSD with X <= x e^T. The paper itself notes the sign pattern after complementing (06-composition.tex lines 260-262).

## [major] sections/06-composition.tex lines 286-319 (Corollary 6.5 and the text after it)

**Issue.** Corollary 6.5 is correct for the given q_i, but it is not precise enough to support its title and its use as a 'diagnostic for a proposed merge'. (a) Delta depends on how the center-only terms (in y, y^2 and constants) are split among the q_i. Replacing q_i by q_i+alpha_i y+gamma_i y^2 with sum alpha_i = sum gamma_i = 0 leaves sum q_i and beta* unchanged but changes sum beta_i. So Delta is not intrinsic to the merged direction. (b) The relaxation R is defined only for the three-variable path (Section 6.1), yet the following text compares Delta with 'the glued relaxation R' for k leaves. (c) The exact relation is missing. Let R be the pair hulls of the P_i glued on (m_y, s_y). The pair hulls are compact, so Sion's minimax theorem gives: gap to R = beta* - sup over re-splits of sum_i min_{P_i}(q_i+alpha_i y+gamma_i y^2) = inf over re-splits of Delta. This makes 'lies in [0,Delta] and can be smaller' exact. It also identifies the multipliers p of Appendix A.2 as optimal re-splits. (d) 'Pairwise intersections ... can all be nonempty while Delta>0' gives no example and needs k>=3. With convex argmin sets, Helly's theorem in R gives the converse. (e) Exact computability needs rational data, which is not stated. 'Compact polytopes' is redundant. The result does not follow from any stated result, so it is not a corollary.

**Fix.** Restate as 'Proposition (Gain over separate pair cuts). Let P_i ⊂ R^2 be rational polytopes in (y,x_i), i=1..k, with S={(y,x):(y,x_i) in P_i for all i} nonempty, and let q_i be rational quadratics. For this decomposition put beta_i, beta*, Delta as above. Then Delta>=0 is the largest c such that sum_i q_i >= sum_i beta_i + c on S, and Delta>0 iff the projections onto y of argmin_{P_i} q_i have empty common intersection.' Then add: 'Delta depends on the decomposition. Let R be the relaxation in which the pair hulls conv{(y,x_i,y^2,yx_i,x_i^2):(y,x_i) in P_i} share m_y and s_y. Then beta* - min_R sum_i lin(q_i) = inf Delta over all re-splittings q_i -> q_i+alpha_i y+gamma_i y^2 with sum alpha_i = sum gamma_i = 0. For A={0,3}, C={1,2}, the re-splitting by p(y)=-(1/2)(y-3/2)^2 gives pair minima 3/4 and -1/4, so Delta=0 = gap to R.' For (d), give an example such as projections {0,1},{1,2},{0,2} (k=3).

**Evidence.** verification/R2-math_identity.py: re-split pair minima 3/4 and -1/4, sum 1/2 = beta*, for the nested example (original split: Delta = 1/2). M4.md Section 7 also notes that Delta compares with separately added pair cuts, not with R.

## [minor] sections/A-proofs.tex lines 134-137; sections/06-composition.tex lines 255-256 ('neither ingredient alone suffices')

**Issue.** A lemma is used implicitly. The text says 'The positive semidefinite completion in this proof is unique, so the dense moment matrix alone does not exclude the zero-value point'. Proposition A.1 shows only that any PSD completion must have the forced value of p_xz; it does not show that one exists. Existence follows from the PSD completion theorem for chordal patterns: K4 minus the edge x–z is chordal, and the two specified blocks (1,x,y) and (1,y,z) are moment matrices, hence PSD. Without it, 'neither ingredient alone suffices' is not proved. The same theorem also explains the general fact behind this (for quadratic data, sparse and dense first-order moment relaxations coincide; Laurent 2009, Lemma 8.6/Cor. 8.7).

**Fix.** Replace the sentence with: 'The specified entries of M form a chordal pattern whose two maximal blocks are pair moment matrices, so M has a positive semidefinite completion [Grone, Johnson, Sá, Wolkowicz 1984]. By the argument above it is unique. Hence the dense moment matrix alone does not exclude the zero-value point.' Add GroneEtAl1984 (and optionally Laurent 2009) to references.bib and cite it in Section 6.4.

**Evidence.** verification/R2-math_checks.py: for the witness, det M(w) = -(5w-3)^2/400, so the only PSD completion has w = 3/5 = p_xz; the eigenvalues of M(3/5) are 0, 0, (209 ± sqrt(30161))/160 >= 0; and 3/5 > m_x = 1/2.

## [minor] sections/06-composition.tex lines 227-235 (positioning against Dey–Khajavirad)

**Issue.** The positioning is incomplete. The text says Prop. 6.1 shows the no-plus-loop hypothesis of Dey–Khajavirad Corollary 1 cannot be dropped. It does not mention their Theorem 2: if the plus-loop nodes form a stable set, PP(G) is SOC-representable, by adding the products among the neighbors of each plus-loop node. The reduced instance has a single plus loop at y, which is a stable set. So their Theorem 2 describes its hull exactly, by adding exactly the nonedge product xz. The example shows that their decomposition into pairs fails without the hypothesis, not that the instance is outside their exact results.

**Fix.** After '... has the same witness and the same gap 1/128.' add: 'Their Theorem 2 still gives an exact extended formulation for this sign pattern, since the plus-loop node y forms a stable set, but it adds the products among the neighbors of y, here the nonedge product xz. This matches the dense-relaxation remark below.'

**Evidence.** KB dey2025-a-second-order-cone-representable: Corollary 1 (decomposability when G1 ∩ G2 is complete with no plus loops), and the stable-set theorem whose proof adds the hyperedges p ⊆ N'(i), |p| >= 2. M4.md Section 8 records the same.

## [minor] sections/07-separation.tex lines 73-76, 110-111, 120-134 (Theorem 7.2 and its positioning)

**Issue.** Theorem 7.2 is not positioned against two closer precedents. (a) In direction space the procedure is Kelley's (Cheney–Goldstein) cutting-plane method for maximizing the concave Lipschitz function psi on C_J: the master LP is the cutting-plane model and the oracle point is a supergradient. The packing argument is the standard finite-epsilon convergence proof. The worst-case behavior of Kelley's method is known to be poor in high dimension (Nemirovski–Yudin 1983, as cited by Drori–Teboulle 2016). So 'The bound is exponential in k, but this is a property of the analysis, not of the problem' is misleading about the method. (b) Brierley–Navascués–Vértesi (2016) already define and solve the same output contract: an exactly valid strictly separating hyperplane, or a point of the set within delta, for arbitrary, possibly lower-dimensional convex sets, using a linear optimization oracle and Gilbert's method. The 'Relation to the ellipsoid method' paragraph contrasts only with GLS and reads as if this contract were new.

**Fix.** At line 76 add: 'In direction space this is Kelley's cutting-plane method [Kelley 1960; Cheney and Goldstein 1959] for maximizing psi over C_J, and the termination proof below is its standard convergence argument.' Replace lines 110-111 with: 'The bound is exponential in k, as is the known worst case of Kelley-type cutting-plane methods; it is not a property of the problem.' At lines 120-123 replace 'gives yet another variant' with '... Brierley et al. state and solve the same contract for arbitrary convex sets by Gilbert's method'. Add 'the same contract appears in [BNV2016]' to the last sentence of the ellipsoid paragraph.

**Evidence.** evidence/literature-L5.md: Chvátal–Cook–Espinoza Algorithm 1; BNV p. 2 definition of WSEP and pp. 9-10 oracle counts; A16–A17 (Kelley, Drori–Teboulle introduction). references.bib has no Kelley or Cheney–Goldstein entry.

## [minor] sections/07-separation.tex lines 61-73 (procedure) and Theorem 7.2 (lines 78-86)

**Issue.** The procedure is underspecified, and the returned cut has no guaranteed depth. (a) W is never initialized. With W empty, the master LP (17) is unbounded/infeasible and the direction c-bar is undefined. (b) A returned cut is only guaranteed L_c - c^T z-bar > 0. Even when dist_1 > epsilon its violation can be arbitrarily small, which matters for binary64 export (Section 7.4 notes that tiny violations can be lost).

**Fix.** Add: 'Initialize W={F(p_0)-z-bar} for some rational p_0 in P, for example a vertex.' Optionally add a remark: 'If a cut is returned only when L_c - c^T z-bar > eta for a fixed eta in [0, epsilon-delta), the same proof gives termination after at most 2k ceil(2R/(epsilon-delta-eta))^(k-1) oracle calls, and every returned cut is violated by more than eta.' (Proof: a call without a cut gives c_s^T w_s <= eta+delta.)

**Evidence.** 07-separation.tex lines 61-73 define W only as 'a finite set'. Checked the modified packing argument by hand: c_t^T w_s > epsilon and c_s^T w_s <= eta+delta give ||c_t-c_s||_inf > (epsilon-delta-eta)/R.

## [minor] sections/07-separation.tex lines 25-26

**Issue.** Section 7.1 says that with F=(x,g(x)) and query (x-bar, b-A v-bar), U_J 'is the set K+Q of Theorem 4.2'. This ignores the equality rows h of Theorem 4.2 (p > 0), for which K = conv{(u,g(u),h(u))} and T(v) has a third block.

**Fix.** Replace with: 'For F=(x,g(x),h(x)), the query (S v-bar, b-A v-bar, e-C v-bar) and J equal to the coordinates of g, this is the set K+Q of Theorem 4.2; the coordinates of h are free.'

**Evidence.** Theorem 4.2 defines K = conv{(u,g(u),h(u)) : u in D}, Q = {0}×R^m_{>=0}×{0}, T(v)=(Sv, b-Av, e-Cv).

## [minor] sections/01-introduction.tex line 75 and sections/00-abstract.tex lines 14-16; Theorem 5.4 (sections/05b-star.tex lines 31-39) and lines 82-89

**Issue.** The complexity statement for stars is slightly stronger than what is proved. (a) The introduction calls the O((m+k)log(m+k)) algorithm 'optimal for algebraic computation trees'. Appendix A.6 proves the Omega((m+k)log(m+k)) lower bound only for a family with m=r leaf rows and k=3r leaves, i.e. m = Theta(k), and only for the decision version. Section 5.3 (line 85) states this qualifier, but the introduction drops it. For box stars (m=0) no lower bound is given. (b) Theorem 5.4 lets m count only rows that involve a leaf. Rows in y alone are not counted, yet they enter the interval I, so the count should include their number m_0.

**Fix.** Introduction line 75: 'worst-case optimal for algebraic computation trees on instances with m = Theta(k)'. Theorem 5.4: 'with O((m+k)log(m+k) + m_0) arithmetic operations and comparisons, where m_0 is the number of rows in y alone'. Alternatively, let m count all rows.

**Evidence.** A2-star-proof.tex lines 22-37: 'The instance has 3r leaves and r leaf rows'. 05b-star.tex lines 25-29: I includes 'the rows in y alone'.

## [minor] sections/05-quadratic-support.tex lines 119-121 (proof of Proposition 5.3)

**Issue.** The coNP-hardness step reads 'with integer data, min q <= -W holds if and only if q >= -W+1/2 fails'. This is true only because the MAX CUT quadratic has an integer minimum, attained at a binary point. For general integer data it is false: x^2-x on [0,1] has minimum -1/4.

**Fix.** Replace with: 'For the quadratic q of the reduction, min q is an integer because q has integer coefficients and a binary minimizer; hence min q <= -W holds if and only if q >= -W+1/2 fails.'

**Evidence.** Direct check of the proof text; counterexample x^2-x.

## [minor] sections/04-original-variables.tex lines 131-142 (Corollary 4.3) and Prop. 4.8 (lines 248-257)

**Issue.** Notation in Section 4. The proof of Corollary 4.3 uses the concave envelope \hat g, which is never defined. The statement uses \breve h without defining it; only \breve g and \hat h are defined. The hat also marks binary64 values (\hat a, \hat c, \hat r) in Prop. 4.8 of the same section.

**Fix.** Define both envelopes once, e.g. 'let vex f and cav f denote the convex and concave envelopes of f over D, vex f(x)=min{y:(x,y) in conv graph f}'. Use vex g, vex h, cav g, cav h throughout Corollary 4.3 and its proof, and keep hats for binary64 data only.

**Evidence.** 04-original-variables.tex line 140: 'the interval [\breve g(x),\hat g(x)]'; line 134: '\breve h(Sv)\le e-Cv\le\hat h(Sv)'.

## [minor] Notation across Sections 1, 2, 4-7 and Appendix A

**Issue.** Several symbols carry different meanings in sections that refer to each other, and some collide within one section. k: the number of features (Sec. 2; intro line 16), the number of leaves (Sec. 5.3; intro line 75; Cor. 6.5), the number of shared moments (Sec. 6.3, same section as Cor. 6.5), the lifted dimension including x (Sec. 7; intro line 95 'k+1 graph points'), and |S| in App. A.1. In the introduction, the 'k' of the separation bound is undefined. h: the support value (Sec. 2, Sec. 7 h(c)) and also the equality-row functions (Sec. 4), while Sec. 7 identifies its set with Theorem 4.2. R: the screening radii (Sec. 3), the glued relaxation (Sec. 6) and the l1 bound (Sec. 7). C: the matrix and the closure \mathcal C (Sec. 4), the two-point set (Sec. 6), C_J (Sec. 7), and a constant (App. A.6). Within Sec. 5, S denotes both row subsets and the star domain, T both a linear space and the triangle, m both polytope rows and leaf rows, and f_i, e_i, a_0..a_2, d_i are coefficients while f_j, e, a, d denote features, the RHS, the direction and the dimension. Within Sec. 6, r denotes the alternation number, the binary length (Prop. 6.4) and a number of values (Sec. 6.5). delta is the set distance in Sec. 6 and the oracle accuracy in Sec. 7. The main text writes lambda_q, lambda_A for encoding lengths (lambda also denotes the KKT multipliers), while App. A.1 uses eta, alpha. App. A.3 uses an undefined label function lambda(s_0). The intro/abstract bound O(k^2 log(kR/epsilon)) omits the -delta of App. A.5.

**Fix.** Fix one letter per object for objects that cross-reference. Suggested: n_F (or q) for the lifted dimension in Sec. 7, k only for the number of features (Sec. 2/5.2), ell or L for the number of leaves, s or k for moments. Rename the equality rows to e.g. h->g^= or eta(u), and the right-hand side e -> d. Use R only for the glued relaxation and write rho_1, rho_inf and B_1 for the other two. Use Omega (or X) for the star domain and I_S for row subsets. Rename the star coefficients in (10) (e.g. alpha_i, beta_i, gamma_i). Use the same encoding-length symbols in Sec. 5.1 and App. A.1. Define the label function in A.3 ('let lambda(t)=+1 on A, -1 on C'). In the introduction, say 'with at most dim+1 graph points' or define k, and write epsilon-delta (or delta=0) in the ellipsoid bound.

**Evidence.** Line references: 01-introduction.tex lines 16, 75, 85, 95-96; 04-original-variables.tex lines 21-24; 05-quadratic-support.tex lines 14-23, 86, 92-95, 140; 05b-star.tex lines 10-14; 06-composition.tex lines 145-155, 189-192, 274-276, 289-293; 07-separation.tex lines 17-31; A-proofs.tex lines 9-14, 75-84, 149.

## [suggestion] sections/04-original-variables.tex lines 232-238 (hierarchy conv Σ ⊆ ∩_λ conv Σ_λ ⊆ \mathcal C)

**Issue.** The text says 'both inclusions can be strict' but does not say which example shows which. Example 4.7 shows only the second: there the aggregated sets are [0,1/2] and [1/2,1], whose intersection {1/2} equals conv Σ. The D=[0,2] example shows the first: every aggregated row is z <= q_lambda(x) with q_lambda convex and q_lambda(0)+q_lambda(2)=2, so the chord gives (1,1) in conv Σ_lambda for all lambda, while z <= 1/2 on Σ at x=1. Σ_lambda should also be defined with Sv ∈ D.

**Fix.** Replace with: '...where Σ_lambda={v: Sv in D, lambda^T(g(Sv)+Av-b)+mu^T(h(Sv)+Cv-e) <= 0}. Example 4.7 shows that the second inclusion can be strict. In the following example the first is strict as well: ...'

**Evidence.** Hand computation: q_lambda(x)=[lambda_1(x-2)^2+lambda_2 x^2]/(2(lambda_1+lambda_2)), so q(0)=2lambda_1/s and q(2)=2lambda_2/s, and the chord value at x=1 is 1.

## [suggestion] sections/06-composition.tex lines 189-199 (Proposition 6.4)

**Issue.** Proposition 6.4 is correct, but several conventions are implicit. The statement does not require k >= 1. It does not say that x_i x_j means i<j, or that x_j^2 is not a feature (its coefficient cancels). It does not name the domain of the minimum, K=[0,1]^r×[0,2^{r+1}-1]×[0,1]^r, or how r is chosen for a given k. The proof also cites Theorem 6.2(i), which is stated for two-point sets.

**Fix.** Restate: 'Let k>=1 and choose r>=1 with k<=2^{r+1}-2 (e.g. r=ceil(log2(k+2))-1). Let H_L be the convex hull of (y,...,y^{max{k,2}}, (x_j), (y x_j), (x_i x_j)_{i<j}) over [0,1]^r×[0,2^{r+1}-1], and H_R analogously. Then min over K of D_L+D_R = 1/2, while R_k contains a point at which the linearization of D_L+D_R vanishes, so the glued bound is 0.' In the proof, write 'by the argument of Theorem 6.2(i)'.

**Evidence.** The x_j^2 coefficient is 4^j-4^j=0. The chain 0,...,k+1 needs k+1 <= 2^{r+1}-1. Both checked by hand and recorded in M4.md Theorem C3.

## [suggestion] sections/05b-star.tex lines 91-127 (Relation to forest algorithms; Remark 5.5)

**Issue.** The positioning against Del Pia–Khajavirad is accurate. Their root merge is a linear scan over d_v heads costing O(d_v m_v), i.e. O(k^2) at a star center, so a heap or sort gives the O(k log k) count, as the paper concedes. Two smaller points would help. (a) The example in Remark 5.5 is itself a star rooted at x_2, so Theorem 5.4 applies to it. Only Appendix A.6 says this, and a reader may otherwise think Theorem 5.4 fails on this path. (b) The leaf subproblems are one-parameter parametric QPs (classical multiparametric QP, e.g. Bemporad et al. 2002). Parametric dynamic programming over trees for convex QP with indicators (Bhathena et al. 2025) is a natural comparator for the open tree question in Section 10.

**Fix.** In Remark 5.5 add: 'Rooted at x_2, the same path is a star, and Theorem 5.4 gives a rational partition; the obstruction concerns nesting conditional values along a tree of depth two.' In the forest paragraph, cite multiparametric QP for the leaf subproblems and Bhathena et al. (2025) for tree DP.

**Evidence.** KB pia2026-treewidth-and-the-complexity-of, proof of Theorem 1 ('O(d_v m_v) comparisons'); A2-star-proof.tex line 46; evidence/issues-raised.md STAR-9, STAR-12.

# R3-lit

I checked all 117 citation commands (91 keys) in sections/*.tex. The sources were local KB full texts, primary PDFs downloaded for this audit (Murty Ch. 2, Nie–Demmel v3, Nie–Qu–Tang–Zhang v3, Fantuzzi–Fuentes v3, the report version of Garloff–Jansson–Smith 2003, Anstreicher 2012, Boyd–Vandenberghe, and SCIP lp.c at v10.0.0 and v10.0.2), and, only where full text was unavailable, abstracts or lane reports.

Almost all attributions and locators are accurate. Verified locators include Neumaier–Shcherbina p. 294; GJS 2003 §5; Murty §2.9; Chen–Luedtke Thm. 3; Lasserre Lemma 6.3 and Thm. 3.7; Nie–Demmel Ex. 3.5; NQTZ Ex. 6.7; Dey–Khajavirad Cor. 1; Burer–Natarajan–Willemsen Thm. 1; Padberg Prop. 8; GLS Thms. 3.2.1 and 4.4.7; Neumaier 2004 §20; and the rounding lines in SCIP's lp.c. Problems found:
- one wrong attribution: Liers et al. as 'the objective alone' (04:211-213);
- several imprecise ones: Schichl–Neumaier, SCIP 8 'negative effect', Boyd–Vandenberghe locator, Rikun, Anstreicher–Burer n=3, the folklore MAX CUT proposition;
- one major novelty overstatement: the 'exact characterizations' of Theorems 6.2–6.3, whose combinatorial core is the classical moment-curve Radon-partition criterion (Breen 1973). The witness, the δ²/2 value and the interface application remain new.

The other novelty claims (certification contract; exact stars with center–leaf rows) survive targeted searches and the lane reports. The introduction's star claim should match the hedged wording of Section 5.

Missing references that a referee would require:
- Tawarmalani 2010, Ex. 3.8 and Cor. 3.10 (already in the bibliography), in Section 6;
- Müller et al. 2022 on surrogate duality in MINLP, for the Section 4.3 hierarchy;
- Davarnia–Richard–Tawarmalani 2017 and Bao–Sahinidis–Tawarmalani 2009, in related work;
- Breen 1973.
Standard RLT, SDP and sparse-SDP citations (Sherali–Adams, Shor, Waki et al., Laurent/Grone) are also absent.

Bibliography: all 76 DOI entries match Crossref; the 12 arXiv entries match the arXiv API. Remaining defects:
- Dey–Khajavirad is now published (Math. Program. 2026, DOI 10.1007/s10107-026-02364-y);
- the SCIP source is cited at v10.0.0 while the runs use 10.0.2 (the cited code is identical);
- some entries render badly: SCIP10 as 'Technical Report ... arXiv', three preprints with no arXiv number, Ballerstein without DOI;
- eight entries lack issue numbers.

The full table is in /workspace/minlp-notes/paper-certified-support-cuts/evidence/review1-citation-audit.md. Scratch scripts: verification/R3-lit_crossref.py with its R3-lit_crossref.json output, and verification/R3-lit_radon_check.py (0 mismatches in 3000 instances).

## [major] sections/06-composition.tex:236-239 (also 06:183-187; Theorems 6.2(ii), 6.3)

**Issue.** The novelty claim overstates. It says that 'the exact characterizations of Theorems 6.2 and 6.3 have not been given before'. For finite A and C, the criterion of Theorem 6.3 is the classical description of Radon partitions of points on the moment curve: conv{(t,...,t^k): t in A} and conv{(t,...,t^k): t in C} meet iff A and C alternate at least k+1 times (Breen 1973; alternating oriented matroids). The zero case of Theorem 6.2(ii) is its k=2 instance (two parabola chords cross iff the endpoints interleave). Only the use of the criterion for gluing interfaces, the delta^2/2 value and the witness/cut are new.

**Fix.** Replace the sentence with: 'For finite sets, the criterion of Theorem 6.3 is equivalent to the classical description of Radon partitions of points on the moment curve: the hulls of {(t,...,t^k): t in A} and {(t,...,t^k): t in C} meet exactly when A and C alternate at least k+1 times [Breen 1973]; Theorem 6.2(ii) is its case k=2. What we add is its use to decide when a k-moment interface misses a gap. To our knowledge, a degree-two example with exact pair hulls, an exact rational gap and a separating cut in the existing coordinates, and the value delta^2/2 of the gap in Theorem 6.2, have not been given before.' At 06:185 cite Karlin–Studden together with Breen (1973), Israel J. Math. 15:156–157, DOI 10.1007/BF02764601, and optionally Björner et al., Oriented Matroids (CUP 1999).

**Evidence.** Breen 1973 (Crossref metadata; the standard statement is that a (d+2)-subset of the moment curve has as its Radon partition exactly the alternating split). verification/R3-lit_radon_check.py: 3000 random instances, k=1..4; LP feasibility of equal-moment measures on A and C agrees with alt(A,C) >= k+1 every time (0 mismatches).

## [major] sections/06-composition.tex:6-9, 219-239, 271-284

**Issue.** Section 6 omits the closest MINLP precedent, although it is in the bibliography. Tawarmalani (2010), Example 3.8 (pp. 14–15), shows that separate envelopes are weaker than the simultaneous hull because they represent the same point by two different convex combinations: the same mechanism as the pair-hull gap. Corollary 3.10 (p. 16) glues two functions h1(u,v), h2(u,w) when their inclusion certificates have equal marginal distributions of u: the full-marginal gluing statement of Section 6.5, stated for MINLP hulls. Section 6 cites only moment-SOS sources (Vorob'ev, Lasserre, Nie–Demmel, Fantuzzi–Fuentes).

**Fix.** At 06:9 add: 'In the MINLP literature, [Tawarmalani 2010, Example 3.8] shows that separate envelopes are weaker than the simultaneous hull because they represent the same point by different convex combinations, and [Tawarmalani 2010, Corollary 3.10] glues two functions that share a variable when their inclusion certificates have equal marginals of that variable.' At 06:274 cite Tawarmalani2010 (Cor. 3.10) next to Vorobev1962 and Lasserre2006.

**Evidence.** KB tawarmalani2010-inclusion-certificates-and-simultaneous-convexification/fulltext.md: Example 3.8 (pp. 14–15: 'the overestimators of f1 and f2 were obtained by expressing (x',y') as a convex combination in two different ways'), Corollary 3.10 (p. 16, condition Pr(u in A) equal for all A ⊆ U). grep finds no Tawarmalani2010 citation in 06-composition.tex. Lane L1 §1 item 5 flags the same point.

## [major] sections/04-original-variables.tex:223-238; sections/02b-related.tex:89-91

**Issue.** A directly relevant SCIP-based reference is missing: Müller, Muñoz, Gasse, Gleixner, Lodi, Serrano (2022), 'On generalized surrogate duality in mixed-integer nonlinear programming', Math. Program. 192:89–118, DOI 10.1007/s10107-021-01691-6. It studies the relaxation obtained by aggregating nonlinear constraints and keeping the aggregated set nonconvex, and its multi-aggregation generalization. Section 4.3's hierarchy conv Σ ⊆ ∩_λ conv Σ_λ ⊆ C and the remark 'closed by convexifying aggregated sets instead of aggregated functions' are surrogate-versus-Lagrangian statements. A referee will ask for this citation.

**Fix.** After the hierarchy at 04:233, add: 'The middle set is the convexified closure of the surrogate relaxations of [Müller et al. 2022]; the gap to C is the surrogate–Lagrangian gap.' At 02b:91 extend the citation to '\citep{DeyMunozSerrano2022,BlekhermanDeySun2024,MullerEtAl2022}'.

**Evidence.** KB muller2022-on-generalized-surrogate-duality-in/fulltext.md, abstract ('nonconvex relaxation obtained via aggregation of constraints: a surrogate relaxation ... generalization ... multiple aggregations'). Lane L1 §1 item 3 and lane L4's must-cite list both include it. It is not in references.bib.

## [major] sections/02b-related.tex:55-77; sections/01-introduction.tex:23

**Issue.** Two core references on joint relaxation of several terms are missing. (a) Davarnia, Richard, Tawarmalani (2017), 'Simultaneous convexification of bilinear functions over polytopes with application to network interdiction', SIAM J. Optim. 27(3):1801–1833, DOI 10.1137/16M1066166: simultaneous convex hulls of vectors of bilinear functions over polytopes, i.e. joint graphs with linear rows, which is the paper's setting. (b) Bao, Sahinidis, Tawarmalani (2009), 'Multiterm polyhedral relaxations for nonconvex, quadratically constrained quadratic programs', OMS 24(4–5):485–504: the BARON reference for relaxing groups of quadratic terms jointly. 02b:20-21 cites only Misener–Floudas for this.

**Fix.** After 'Zhu, He and Tawarmalani treat simultaneous factorable graphs with coupling constraints' add ', and \citet{DavarniaRichardTawarmalani2017} convexify vectors of bilinear functions simultaneously over polytopes'. Change 02b:21 to '\citep{BaoSahinidisTawarmalani2009,MisenerFloudas2012}'. Optionally add DRT2017 to the list at 01:23.

**Evidence.** Both are in the local KB (davarnia2017-simultaneous-convexification-of-bilinear-functions, bao2009-multiterm-polyhedral-relaxations-for-nonconvex) and in lane L1's must-cite list. Neither is in references.bib.

## [minor] sections/04-original-variables.tex:211-213

**Issue.** Misattribution. The text says that 'for the objective alone the closure is the hull of the epigraph over D; this is the case studied by Liers et al. (2021)'. Liers et al. study problem (OP): min c^T(x,z) s.t. z=g(x), x in D. That is the hull of the graph of a vector of constraint functions, each row with its own variable z_j, which is the free-remainder case of Proposition 4.6. It is not the objective epigraph.

**Fix.** Replace with: 'The objective row always contains −t, so for the objective alone the closure is the hull of the epigraph over D. The setting of \citet{LiersEtAl2021}, rows z_j=g_j(x) with a separate variable z_j for each row, is also covered by Proposition~\ref{prop:free-remainders}. Without free remainders the gap can be strict.'

**Evidence.** KB liers2021-solving-mixed-integer-nonlinear-optimization/fulltext.md §2 (problem (OP) and feasible set X with z = g(x)) and §3.1 (Y_g = conv of the feasible set).

## [minor] sections/08-implementation.tex:249-251

**Issue.** Over-attribution. The text attributes to Schichl and Neumaier (2005) the observation that modeling systems introduce uncontrolled rounding. Only Neumaier (2004, §20, 'Rounding in the problem definition') says this. Schichl–Neumaier (2005, §3.1) say that constant folding during DAG simplification must not introduce roundoff in a validated context.

**Fix.** Replace with: '... of the model import. It addresses the observation of \citet[Section~20]{Neumaier2004} that modeling systems introduce uncontrolled rounding, and the requirement of \citet[Section~3.1]{SchichlNeumaier2005} that simplification of the expression graph introduce no roundoff.'

**Evidence.** KB neumaier2004-complete-search-in-continuous-global §20; KB schichl2005-interval-analysis-on-directed-acyclic §3.1 l.138 ('In a validated computation context, however, you have to make very sure that no roundoff errors are introduced in this step').

## [minor] sections/02b-related.tex:94-95

**Issue.** 'Several valid cut families ... remain disabled by default because their overall effect is negative' overstates the SCIP 8 source. SCIP 8 disables intersection cuts ('not clear yet how to decide when it will be beneficial'), edge-concave cuts ('has not shown to be particularly useful') and gradient-cut tightening ('require more tuning to be efficient'). Only SCIP 10 reports a performance loss, for flower cuts on continuous products.

**Fix.** Replace with: 'Several valid cut families for nonconvex problems remain disabled by default because they have not been found to pay off in general \citep{BestuzhevaEtAl2025,SCIP10}.'

**Evidence.** KB bestuzheva2025-global-optimization-of-mixed-integer l.323, 335, 391; KB hojny2025-the-scip-optimization-suite-10 l.495.

## [minor] sections/05-quadratic-support.tex:104-122 and 132-134

**Issue.** Proposition 5.3 (strong NP-hardness of box QP via MAX CUT; coNP-completeness) is folklore, but it is presented without saying so. Lines 132–134 support 'restricting the interaction graph alone is not enough' only with the quartic path result. For quadratic blocks, the subject of the section, Del Pia–Khajavirad (2026) prove the stronger and directly relevant result in Theorem 3: box QP is strongly NP-hard at treewidth two.

**Fix.** Before Proposition 5.3 add: 'The following facts are folklore \citep[Section~2.3]{BurerLetchford2009}; we include the proof because the coNP statement is used below.' Replace 05:132-134 with: 'Restricting the interaction graph alone is not enough: box-constrained quadratic minimization is strongly NP-hard already at treewidth two, and quartic minimization already on paths \citep[Theorems~2 and~3]{DelPiaKhajavirad2026}.'

**Evidence.** KB burer2009-on-nonconvex-quadratic-programming-with §2.3 p.4 ('Another folklore result ... max-cut ... NP-hard in the strong sense ... so is QPB, even in the concave case'); KB pia2026-treewidth-and-the-complexity-of Theorem 3 (l.559) and Theorem 2 (l.471).

## [minor] sections/05-quadratic-support.tex:152-154

**Issue.** Rikun (1997) is weak support for 'factorable relaxations ignore linking constraints, and convexifying over the constrained domain repairs this'. Rikun gives polyhedrality conditions for envelopes of multilinear functions over polytopes; at most a footnote relates. The direct source, already in the bibliography, is Anstreicher (2012), Thm. 1 and Cor. 1: convexifying the quadratic form over the linear-constraint region dominates separate envelopes.

**Fix.** Use '\citep{Anstreicher2012,ZhuHeTawarmalani2026,WuMutsNowakHendrix2025}', or keep Rikun only with a page locator for the specific statement used.

**Evidence.** Anstreicher 2012 Optimization Online preprint (abstract: 'replacing ... with their convex lower envelopes on F is dominated by ... convexifying the range of the quadratic form for x in F'). KB rikun1997 abstract and §1.

## [minor] sections/02b-related.tex:43-45

**Issue.** Two attribution problems. (1) The n=3 box counterexample (−53 versus about −53.004) is due to Anstreicher–Burer (2010). Burer–Letchford (2009, §2.2 p. 4) and Anstreicher (2012, p. 8) only report it, yet only they are cited for 'for boxes in higher dimension it is not'. (2) For triangulated polytopes, AB2010 (Thm. 7) give a disjunctive extended formulation built from DNN descriptions of the simplices, not SDP+RLT constraints on the polytope.

**Fix.** Replace with: 'The convex hull of {(x,xx^T)} is described by semidefinite and RLT (doubly nonnegative) constraints over a simplex of dimension at most four and over a box in dimension two, and polytopes of dimension at most three admit such descriptions through a triangulation \citep{AnstreicherBurer2010}; for the box in dimension three these constraints are not enough \citep{AnstreicherBurer2010,BurerLetchford2009,Anstreicher2012}.'

**Evidence.** KB anstreicher2010-computable-representations-for-convex-hulls (abstract; Thm. 6; l.163–167 n=3 example; Thm. 7 via Cor. 4); KB burer2009 l.131; Anstreicher 2012 preprint p. 8.

## [minor] sections/01-introduction.tex:76-78

**Issue.** The introduction says that 'to our knowledge, the case with center–leaf rows has not been solved exactly before'. This is stronger than the hedged 05b-star.tex:276-279 ('We know of no earlier exact algorithm ...; the construction itself ... is elementary'). The lanes and my own search found no exact algorithm, so the claim survives. The construction, however, is nonserial dynamic programming with parametric scalar minimization, and a referee will want those ingredients credited.

**Fix.** Replace with: '...; to our knowledge, no exact algorithm for the case with center--leaf rows has been published, although its construction, conditioning on the center as in nonserial dynamic programming \citep{BerteleBrioschi1972}, is elementary.' In 05b, optionally cite Bemporad et al. (2002) and Bhathena et al. (2026) for parametric and tree dynamic programming.

**Evidence.** Lane L2 §4.1; web searches for nonconvex star QPs with coupling rows and TVPI-type QPs found nothing. Khajavirad (Aug 2026, Optimization Online, 'A polynomial-time solvable class of sparse box-constrained polynomial optimization problems') is box-only.

## [minor] sections/04-original-variables.tex:47

**Issue.** Wrong locator. 'This is weak Lagrangian duality [Boyd–Vandenberghe, Section 5.1]'. §5.1.3 gives the lower-bound property; 'weak duality' is named and stated in §5.2.2.

**Fix.** Use '\citep[Sections~5.1.3 and~5.2.2]{BoydVandenberghe2004}'.

**Evidence.** Boyd–Vandenberghe PDF (bib URL): 5.1.3 'Lower bounds on optimal value'; 5.2.2 'Weak duality'.

## [minor] sections/06-composition.tex:219-227; 02b-related.tex:104-107; 05-quadratic-support.tex:156; 06:25

**Issue.** Standard references are missing for tools used throughout. (1) RLT is used repeatedly with no citation (Sherali–Adams 1990; Sherali–Tuncbilek 1992); the SDP relaxation is used without citing Shor. (2) The discussion of sparse relaxations on paths lacks the basic sparse-SDP references: Waki–Kim–Kojima–Muramatsu (2006); Grimm–Netzer–Schweighofer (2007); Laurent (2009, Cor. 8.7) / Grone et al. (1984), which show that sparse equals dense for quadratic Shor relaxations via PSD completion. That explains why the gap needs box RLT, as the paper's own Appendix shows. Also missing: Kojima–Kim–Arima (2026, §3.3) on overlaps that carry off-diagonal entries.

**Fix.** Cite Sherali–Adams/Sherali–Tuncbilek at the first use of RLT (02b:44) and Shor at the first SDP use. In 06:219-227 add: 'For quadratic objectives, sparse and dense Shor relaxations coincide under chordality \citep{Waki2006,Laurent2009}; the gap of Proposition 6.1 therefore comes from the RLT constraints of the pairs, which have no nonedge counterpart.'

**Evidence.** KB waki2006-sums-of-squares-and-semidefinite; KB sherali1990-a-hierarchy-of-relaxations-between; KB sherali1992-a-global-optimization-algorithm-for; KB kojima2026-local-to-global-exactness-of; lane L2 §3.1 and its must-cite list. BL2009 §2.2 attributes the SDP relaxation to Shor.

## [minor] sections/05b-star.tex:19

**Issue.** Moré–Vavasis (1990) is cited for 'minimizing a concave separable quadratic over a box and a single row ... is already NP-hard'. The accessible record (abstract) says 'separable concave' with bounds and one equality; the full text is closed access and could not be checked for the quadratic case.

**Fix.** Add the one-line reduction (subset sum: min Σ x_i(1−x_i) s.t. Σ a_i x_i = b, 0 ≤ x ≤ 1 has value 0 iff the instance is feasible), or cite a source that proves the quadratic case. Alternatively write 'a separable concave function'.

**Evidence.** Publisher abstract via search; Unpaywall reports no open-access copy. Lane L2 also read only the abstract.

## [minor] references.bib DeyKhajavirad2025 (cited 02b:50, 05b:108, 06:228 with 'Corollary 1')

**Issue.** Cited as arXiv:2508.18435 (2025), but it is now published in Mathematical Programming (online 2026-05-26). The locator 'Corollary 1' was verified only in the arXiv version.

**Fix.** Change to @article, journal Mathematical Programming, year 2026, DOI 10.1007/s10107-026-02364-y (add volume and pages when assigned), and recheck the corollary number in the journal version.

**Evidence.** Crossref works/10.1007/s10107-026-02364-y: title and authors Dey, Khajavirad match; published-online 2026-05-26.

## [minor] references.bib SCIPsource10; sections/03-certification.tex:45-48

**Issue.** The source citation is tag v10.0.0, but all runs use SCIP 10.0.2. The cited behavior (rowAddCoef and rowChgCoefPos round near-integral coefficients when not in exact mode, without changing the sides) is present and identical in both tags.

**Fix.** Cite tag v10.0.2, or state that the cited lines are unchanged between 10.0.0 and 10.0.2.

**Evidence.** src/scip/lp.c fetched at v10.0.0 and v10.0.2: 'if( !set->exact_enable ) val = SCIPsetIsIntegral(set, val) ? SCIPsetRound(set, val) : val;' at l.2223–2225 (rowAddCoef) and l.2401–2403 (rowChgCoefPos); no side adjustment follows.

## [minor] references.bib (rendering in main.bbl)

**Issue.** Several entries render badly with plainnat. (a) SCIP10 renders as 'Technical Report 2511.18580, arXiv, 2025'. (b) DelPiaKhajavirad2026, Khajavirad2026 and ZhuHeTawarmalani2026 print no arXiv identifier, only an HTML URL, because plainnat ignores eprint/archivePrefix. (c) Ballerstein2013 loses its DOI and 'Diss. ETH No. 21024'. (d) Issue numbers are missing for AnstreicherBurer2010 (1–2), GleixnerEtAl2017 (4), HeTawarmalani2021 (1–2), MisenerFloudas2012 (1), MoreVavasis1990 (1–3), NieQuTangZhang2026 (1–2), Rabinowitsch1930 (1) and WuMutsNowakHendrix2025 (2). Apart from these, all 76 DOI entries match Crossref in title, authors, venue, volume, pages and year.

**Fix.** Use @misc with howpublished = {arXiv:2511.18580} (and likewise arXiv:2609.35595, arXiv:2601.18545, arXiv:2603.18458). Add note = {Diss. ETH No. 21024, doi:10.3929/ethz-a-009959194} to Ballerstein2013. Add the issue numbers.

**Evidence.** verification/R3-lit_crossref.py and R3-lit_crossref.json (76 DOIs; Ballerstein's DataCite DOI resolves via doi.org); arXiv API checks for 12 preprints; main.bbl lines 223–227, 399–400, 439–443, 708–712, 33–36.

## [minor] sections/09-computations.tex:21

**Issue.** The experiments use the current MINLPLib (OSiL files and library metadata), but the only citation is the 2003 MINLPLib paper, which describes the original GAMS-format collection.

**Fix.** Also cite the current library, e.g. 'S. Vigerske, MINLPLib: A library of mixed-integer and continuous nonlinear programming instances, https://www.minlplib.org (accessed <date>)', with the snapshot date.

**Evidence.** KB vigerske2026-minlplib-a-library-of-mixed; lane L5 ('cite the snapshot or version used').

## [minor] sections/02b-related.tex:12; 01-introduction.tex:23

**Issue.** No lane accessed Ballerstein (2013); the ETH copy was access-restricted. The attribution of the vector-hull characterization is secondary, via Liers et al. (2021, Prop. 1) and Mertens (2019, Prop. 3.13, citing 'Cor. 5.25'). The introduction's 'vectors of univariate functions' rests on the same secondary report.

**Fix.** Either obtain the thesis and add the locator (\citealp[Cor.~5.25]{Ballerstein2013}), or write 'Ballerstein (2013), as stated in Liers et al. (2021, Prop. 1), characterizes ...'.

**Evidence.** Lane L1 entry [Ballerstein2013] ('not accessed'); KB record status 'unread'; issues-raised.md SUP-10 (Open).

## [suggestion] sections/00-abstract.tex:16-20

**Issue.** 'We show that exact pair hulls glued on shared moments do not compose' reads as a discovery claim, while Section 6 states that the phenomenon and its reason are known.

**Fix.** Replace with: 'We quantify how exact pair hulls glued on shared moments fail to compose: on a path of three variables ...'.

**Evidence.** 06-composition.tex:6-9 ('That gluing local convex hulls along shared variables can fail is known, and the reason is known as well').

## [suggestion] sections/04-original-variables.tex:80-83; 03-certification.tex:132-134

**Issue.** Two wording issues. (1) 'the Lagrangian dual of a nonconvex problem equals the dual of its convexification' should state the primal characterization: the dual value equals the optimal value of the convexified problem, under a constraint qualification. (2) With p'' ≤ M, the αBB quantity M(β−α)²/8 is the maximal separation of the αBB underestimator of −p (the concave overestimator of p) with α=M/2, not of p.

**Fix.** (1) Use: '... that the Lagrangian dual value of a nonconvex problem equals the optimal value of its convexification in the joint space of variables and constraint values (under a constraint qualification) ...'. (2) Use: '... the maximal separation of the αBB underestimator of −p with α=M/2'.

**Evidence.** Lanes L1/L4 (Nowak Lemma 3.3 needs a CQ); KB adjiman1998 l.201 (d_max formula).

## [suggestion] various (05b, 09, 03:132, 02:18)

**Issue.** Optional references a referee may ask for: Margot (2009, Math. Program. Comput. 1:69–95) on testing cut generators, as a contrast to the replay validity test; Xu–Pokutta (2026, arXiv) on joint-range inequalities for QCQPs; Khajavirad (Aug 2026, Optimization Online) on polynomial-time sparse box-constrained POP; a numerical-analysis source for the linear-interpolation remainder in Lemma 3.4; Rockafellar (1970, Cor. 11.5.1) for Proposition 2.1.

**Fix.** Add where relevant; none of these is required for correctness.

**Evidence.** KB xu2026-joint-range-inequalities-for-nonconvex; optimization-online.org/wp-content/uploads/2026/04/mainRevised.pdf; lane L5 C10 (Margot).

# R4-numbers

I recomputed every number in Section 9, the abstract, the introduction and Appendix B (Tables 2, 3, 6, the Part B table and the path-family table) from the raw records, using my own standard-library script /workspace/minlp-notes/paper-certified-support-cuts/verification/R4_recompute.py. The script reads campaign-v1, campaign-v2, the repair cohort, v3 Parts A, B and C, the scan, the selection files and the v3d diagnostic. It imports no producer code and makes 209 checks: 200 pass and 9 are real mismatches.

**What matches exactly:**
- every cell of Table 2, Table 3, Table 6 (limits, checked against the configs in the records), the Part B table and the path-family table;
- all campaign-2 numbers, all scan counts except the maximum discovery time, the hash selections, the incumbent counts, and the replay counts (7,498 cuts, 14/14 tamper rejections per mode).

**Mismatches:**
1. Campaign 1 shows that the claim 'the cuts never changed which models SCIP solved', made in the abstract, introduction and Sec. 9.7, is false: genpooling_lee2 was lost in both cut modes (critical).
2. Campaign-1 timing: the baseline (0.38 s) and control (0.52 s) values are over 19 models. On the 18 models solved in every mode they are 0.26 s and 0.41 s.
3. Part A slowdown is 15-20%, not 15-21%.
4. Part B: mode auto was slower on 43 of 52 runs, not 44.
5. The scan's maximum discovery time is 4.0 s, not 4.2 s.
6. The per-copy root-bound range -0.031 to -0.022 is not reproducible.
7. The row-direction variant changed cut counts in 10 of 180 runs, not 8.
8. The host load during the timed runs was 14-21, not 10-17.

**Replay of v3d/runs/partC-rowdir:** it finished at 12:00 today, after the PDF was built, and passed: 30,000 of 30,000 cuts. Together with 469 and 529 cuts in the Part A and B rowdir runs, the diagnostic contributes 30,998 replayed cuts, which the paper does not report.

**Methodology:**
- Section 9.6 labels the post hoc diagnostic correctly. The abstract and introduction do not: they present it as the headline result and credit the row direction alone. In fact the row direction alone gave 43-46% closure and 10 of 20 solved; full closure and 20/20 also needed fourfold cut limits.
- The 2x2 design behind that attribution is missing a cell (remainder-only directions with wide limits).
- Two pre-run steps are not disclosed: hand tests of the wide limits on 2 of the 20 evaluation instances, and a native pilot that came before the random family design.
- The slowdown claims are directionally sound but understated by the shift-1 SGM. In Part B the median per-run factor is 2.6 against '40%'.
- The bound claims hold at 1e-4.
- The conclusions contradict Section 9: they blame frozen limits and discovery cost, while the paper's own all-diag runs and the campaign-3 cost breakdown say otherwise.

**What a referee would require:**
- a prospective sample of structure-containing models that SCIP finds hard;
- counts of certified cuts rejected at the stored-row check (up to 36% in all-diag);
- a definition of the time measure and the tolerance floor;
- uncertainty estimates for the timing comparisons.

**Commands run (targeted, local only, no CI):** `/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python /workspace/minlp-notes/paper-certified-support-cuts/verification/R4_recompute.py` (single-threaded, about 20 s), plus short read-only inspection scripts over the same records.

## [critical] /workspace/minlp-notes/paper-certified-support-cuts/sections/00-abstract.tex:23-24; /workspace/minlp-notes/paper-certified-support-cuts/sections/01-introduction.tex:107-110; /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:285-287

**Issue.** The abstract, the introduction and Sec. 9.7 say the cuts never changed which MINLPLib models SCIP solved, 'in any campaign, mode or seed'. The paper's own campaign-1 data, which Sec. 9.2 (l.53-55) reports correctly, contradict this. Both cut modes lost genpooling_lee2: the baseline and control solved it in 5.61 s and 4.89 s, while all and auto hit the 6 s limit. So the headline computational claim is false as stated.

**Fix.** Abstract: 'Every recorded cut passed replay. In campaigns 2 and 3 the cuts did not change which models SCIP solved, and in campaign 1 they lost one model at the 6-second limit; in all campaigns they made the solves slower.' Introduction l.107-110: '... the cuts never changed which models SCIP solved in campaigns 2 and 3; in campaign 1 both cut modes lost genpooling_lee2 at the 6-second limit.' Sec. 9.7: 'On benchmark models the cuts did not change which models SCIP solved in campaigns 2 and 3, in any mode or seed; in campaign 1 both cut modes lost genpooling_lee2 at the 6-second limit.'

**Evidence.** R4_recompute.py check C1.solved_set_unchanged gives ['genpooling_lee2']. Scanning every non-root MINLPLib group of campaign-v1, campaign-v2 and the repair cohort finds that this is the only group whose solved status differs between baseline and a cut mode. Campaign 1 solved counts: baseline 19, control 19, all 18, auto 18 (of 20 admitted).

## [major] /workspace/minlp-notes/paper-certified-support-cuts/sections/00-abstract.tex:25-27; /workspace/minlp-notes/paper-certified-support-cuts/sections/01-introduction.tex:112-116; /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:291-292

**Issue.** The abstract and introduction present the post hoc diagnostic as the main positive result: complete root closure and 20/20 solved 'once the direction search tried each row's own direction'. This is overstated and attributed to the wrong cause. (i) The text does not say it is a post hoc variant designed after Part C was seen. (ii) The row direction alone, under the protocol limits, closed only 43-46% (median) and solved 10/20 against 9 for the baseline. Full closure and 20/20 also required 4x cuts per callback, 4x total cuts and 2x support calls. (iii) The prospective result is not mentioned: 19-35% median closure, and the same 9 instances solved as native SCIP. Sec. 9.7 l.291-292 repeats the attribution.

**Fix.** Abstract: 'On a constructed family with the path structure, the prospective runs closed a median of 19-35% of SCIP's root gap and solved the same 9 of 20 instances as native SCIP within 300 seconds. In a post hoc diagnostic that first tried each row's own direction and raised the cut limits fourfold, the cuts closed the root gap and solved all 20 instances; the row direction alone closed 43-46% and solved 10.' Make the same change in the introduction (l.112-116) and in Sec. 9.7 (l.291-292).

**Evidence.** Table 3 and my recomputation agree. Row dir. medians are 0.44/0.44/0.43/0.46, with 5/5/0/0 solved (10 of 20). Row dir. wide gives 1.00 with 20/20 solved. Frozen gives 0.35/0.25/0.19/0.22, with the same 9 solved as the baseline. In v3d/runs/partC-rowdir the configs are all-diag-mech (max_cuts_per_round n, max_cuts 4n, max_support_calls 20n) and all-diag-mech-wide (4n, 16n, 40n).

## [major] /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:250-270 (and mechanism design, l.201-215)

**Issue.** The post hoc diagnostic is not fully disclosed, and its design cannot support the stated attribution. (a) The design is incomplete: frozen directions combined with wide limits were never run, so the paper cannot tell whether the row direction or the wider limits is decisive. (b) experiments/v3d/README-diagnostic.md l.39-40 records hand tests of the wide mode on n=10 seed 4 and n=40 seed 0 before the run. These are 2 of the 20 evaluation instances, and the paper does not mention the tests. (c) The randomized family was adopted after a native-SCIP pilot (experiments/pilot-native.md) showed that the deterministic family was easy: n=160 solved in 18.6 s. The paper does not mention the pilot either. (d) The variant was evaluated only on the instances that motivated it.

**Fix.** Run the missing cell (remainder-only directions with wide limits; 40 runs) and the row-direction variant on fresh seeds (for example 5-9 per n), both prospectively. In Sec. 9.6 add: 'Before this run we checked the wide limits by hand on two of the 20 instances (n=10 seed 4, n=40 seed 0). The random family itself was adopted after a pilot showed that native SCIP solves the deterministic family (all triples equal to Proposition 6.1) up to n=160 in 19 s.'

**Evidence.** v3d partC-rowdir contains only the modes baseline, all-diag-mech (row direction, protocol limits) and all-diag-mech-wide (row direction, wide limits). There is no record with remainder-only directions and wide limits. Pilot table: deterministic n=80 solved in 9.16 s and n=160 in 18.63 s, whereas the random family at n=40 and n=80 is unsolved in 300 s.

## [major] /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:55-58

**Issue.** The campaign-1 timing numbers do not refer to the model set the text names. The baseline value 0.38 s and the control value 0.52 s are shifted geometric means over 19 models (those solved by baseline or control). The values 0.57 s and 0.46 s for the cut modes are over 18 models. On the 18 models solved in every mode, as the sentence claims, baseline and control are much faster. The text therefore understates the overhead of both the reformulation and the cuts (all is 2.2x the baseline, not 1.5x).

**Fix.** Replace with: 'On the 18 models solved in every mode, the shifted geometric mean time was 0.26 s for the baseline, 0.41 s for the control, and 0.57 s and 0.46 s for the two cut modes.'

**Evidence.** Time is total_seconds + source_read_seconds, with shift 1. Over the 18 common models: baseline 0.262, control 0.407, all 0.574, auto 0.464. Over the pairwise sets: baseline 0.377 (19), control 0.517 (19), all 0.574 (18), auto 0.464 (18). These are checks C1.sgm.* and the corresponding details.

## [major] /workspace/minlp-notes/paper-certified-support-cuts/sections/01-introduction.tex:111-112; /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:148-150, 167-169, 288-290

**Issue.** Slowdown is quantified mainly by a shifted geometric mean with a 1 s shift. Most baseline runs take under 1 s (56 of 80 in Part A, 38 of 52 in Part B), so this statistic compresses the per-run cost. Part A does report a median per-run factor of 1.3, but Part B reports only 'about 40%' and omits its median per-run factor of 2.6. The introduction's '15-40%' therefore understates the typical per-run slowdown on the structure-selected models by a large factor.

**Fix.** Report both statistics wherever slowdown is quantified. Sec. 9.4, Part B: '... the cut modes were 37% (auto) and 41% (all) slower in shifted geometric mean, and by median factors of 2.5 and 2.7 per run.' Introduction: '... made the solves slower, by 15-41% in shifted geometric mean and by median per-run factors of 1.3 on the campaign-2 models and 2.5-2.7 on the structure-selected models.' Add per-run ratio quartiles to Table 2.

**Evidence.** Per-run time ratios on commonly solved runs (time = total+preparation). Part A: median 1.336 (all) and 1.290 (auto); unshifted geometric mean 1.607 and 1.374. Part B: median 2.655 (all) and 2.547 (auto); unshifted geometric mean 2.783 and 2.646; quartiles [1.14, 2.65, 5.87] for all.

## [major] /workspace/minlp-notes/paper-certified-support-cuts/sections/10-conclusions.tex:25-34

**Issue.** The conclusions contradict Section 9 in three places. (1) 'The frozen work limits allow few cuts' is offered as a reason for the null result, but the all-diag test that Section 9 designed for this question found that raised limits improved the root bound on only one more model per part. (2) 'Discovery in Python costs more than the cuts return' contradicts Sec. 9.5: 'In campaign 3, discovery is fast and exact certification dominates' (Part B: discovery 4.4 s of 32.9 callback seconds, certification 23.0 s). (3) 'The cuts close part of the root gap' contradicts the abstract's claim of complete closure. Part only is correct for the prospective runs.

**Fix.** Replace the second reason with: 'Second, where the structure occurs, SCIP solves these models in about a second, and the separator's Python cost (in the final implementation mostly exact certification) exceeds what the cuts return; raising the work limits did not change this.' Replace the family sentence with: 'On the constructed family, the prospective separator closed part of the root gap and reduced the number of nodes; a post hoc variant that tried each row's own direction first, with wider limits, closed the gap at the root.'

**Evidence.** Raised-limit (all-diag) root runs: Part A improved 1 model (cvxnonsep_psig20r), Part B improved 4 against 3 for all (the extra one is pooling_bental4pq). Part B callback breakdown recomputed: 32.90 / 22.97 / 3.85 / 4.39 s.

## [major] /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:152-169, 188-191

**Issue.** A computational referee would ask for a missing experiment. The structure-selected sample can hardly show a benefit because SCIP solves nearly all of it at once: 21 of the 26 solved models take under 3 s, and the baseline median is 0.16 s. The sample is also clustered: 9 pooling, 8 kall and 3 bayes2 models among the 30. Even so, the paper generalizes to 'what is rare is a model in which it is decisive for SCIP'. The scan already identifies 111 qualifying models, but no sample of qualifying models that are hard for SCIP was evaluated.

**Fix.** Add a prospective Part D: qualifying models from the 111 (or from a larger size class) that native SCIP does not solve within, say, 10-60 s, selected by a rule fixed in advance. Otherwise restrict the claim, for example: 'The structure is common in MINLPLib; on the 30 sampled models, which SCIP mostly solves in under a second, it was never decisive.'

**Evidence.** In Part B baseline seed-0 runs (Table tab:partB), 4 models time out at 300 s and only 5 solved models take 8-191 s; on these the cuts changed nothing beyond noise (for example 191.4 vs 190.7 s, 23.2 vs 19.7 s). Baseline time on commonly solved runs: median 0.159 s, with 38 of 52 under 1 s.

## [minor] /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:267-269

**Issue.** The number of cut-mode root runs whose cut count the row-direction variant changed is wrong. The text says 8 of 180; the records give 10.

**Fix.** '... the variant changed the number of cuts in 10 of 180 cut-mode runs (2 in Part A, 8 in Part B) and no bound.'

**Evidence.** Changed runs, as (model, mode, old count, new count). Part A: kall_congruentcircles_c51 all 6->8 and auto 6->8. Part B: c61 all 6->7 and auto 5->7; c63 all 5->6 and auto 5->6; c71 all 5->6; c72 all 4->6 and auto 4->5; nvs02 auto 10->9. Root bounds were unchanged at 1e-4 in all modes for all 60 models, which confirms the text.

## [minor] /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:239

**Issue.** The range 'between -0.031 and -0.022 per copy on average' for the baseline root bound cannot be reproduced under any reading I tried: per instance, per-n mean, per-n median, or gap per copy.

**Fix.** 'SCIP's root bound on these instances is weak: between -0.035 and -0.013 per copy (mean -0.027), while each copy contributes at least 1/8192 to the optimum ...'

**Evidence.** Baseline root dual divided by n: per instance -0.0354 to -0.0131; per-n means -0.0273, -0.0250, -0.0290, -0.0249 (overall -0.027); per-n medians -0.0252, -0.0290, -0.0306, -0.0227.

## [minor] /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:148-150, 168-169, 189

**Issue.** Small numerical mismatches. (1) Part A: '15-21%' should be 15-20%; Sec. 9.7 itself says 'about 15-20%'. (2) Part B: 'slower on 44 of 52 runs' holds only for mode all; auto is slower on 43. (3) Scan: 'at most 4.2 s' should be 4.0 s.

**Fix.** 'slower by 15-20% in shifted geometric mean'; 'slower on 44 (all) and 43 (auto) of 52 runs'; 'at most 4.0 s per model'.

**Evidence.** SGM ratios are 1.2673/1.0535 = 1.203 (all) and 1.2134/1.0535 = 1.152 (auto). Ratios above 1 occur in 44 (all) and 43 (auto) of 52 runs. The maximum discovery_seconds over the 389 admitted scan records is 4.008 (median 0.0424).

## [minor] /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:16-19, 30-34

**Issue.** The setup is described inaccurately or incompletely. (1) The load range is wrong: the campaign-3 timed runs saw a one-minute load of 14.1-20.7 (Part A full: median 19.9, maximum 20.6). (2) The host has 18 physical cores (36 hardware threads) and runs under WSL2, not '36-core'. (3) The time measure is never defined: Table 2 uses total_seconds + preparation_seconds (in-process, excluding about 0.6-0.7 s of interpreter/import and the primal check), while Tables tab:partB and tab:mechanism-detail use total_seconds. (4) The bound tolerance is rtol*max(1,|a|,|b|), which is absolute for |bound| < 1 (all kall_* models and the path family).

**Fix.** '... on a Linux host (WSL2) with 18 cores and 36 hardware threads, shared with unrelated jobs (one-minute load average between about 10 and 21 during timed runs). Times are in-process wall times charged to the soft budget (model build, discovery, separation and solve), excluding interpreter start-up and the primal check. Bounds a and b are compared with tolerance 1e-4 max{1,|a|,|b|}.'

**Evidence.** load_start/load_end over v3 records: Part A full 15.3-20.6, Part A root 15.0-16.9, Part B 16.0-17.0, Part C 14.1-16.9, v3d C 14.1-20.7; v3d A/B root 2.1-5.8 (quiet host). Campaign-2 environment: 10.8-12.5. lscpu: 18 cores per socket, 2 threads per core. The outer-wall SGM of the Part A baseline is 2.23 s, against 1.05 s in-process.

## [minor] /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:175-179; /workspace/minlp-notes/paper-certified-support-cuts/sections/01-introduction.tex:117-118

**Issue.** (1) The replay of the diagnostic's cuts is not reported, although the abstract's 'every recorded cut passed replay' must cover them. That replay (v3d/runs/partC-rowdir) finished at 12:00 today, after the PDF was built (11:48); it passed. (2) 'Independent replay' overstates what replay does. It re-executes the same exact support module (snapshot solver/support.py, shared with generation), as Sec. 8.3 states.

**Fix.** Add to Sec. 9.4: 'The 30,998 cuts of the post hoc diagnostic (469 and 529 in the root runs of Parts A and B, 30,000 in the path family) also passed replay, and all 14 corrupted records were rejected in each mode.' Introduction l.117: 'Every recorded cut passed a fresh-process replay, which re-executes the exact support routines, against the source model and the stored solver row.'

**Evidence.** v3d replay.json: partA-root-rowdir 469/469, partB-root-rowdir 529/529 and partC-rowdir 30,000/30,000, all passed; 14/14 tamper rejections per cut mode, with no config failures.

## [minor] /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:154-180, 239-249

**Issue.** Separator statistics that matter for interpretation are missing. (1) How often a certified, violated cut was rejected because SCIP's stored row differed from the certified row; Sec. 8.3 describes this check but the paper gives no counts. (2) That the cut caps were binding: every prospective Part C run reached exactly 4n cuts, every wide run reached 16n, and the budget or caps were exhausted in 36 of 60 Part B full runs of mode all.

**Fix.** Add a short table or paragraph: certification calls, certification failures, row-check rejections and runs that hit each cap, per part and mode. In Sec. 9.6 state that every run reached its total cut cap.

**Evidence.** row_binding_rejections against cuts added: Part B full all 45 vs 179, auto 31 vs 145; Part B root all-diag 202 vs 358; Part A root all-diag 41 vs 403; Part C 71 vs 3,000 per phase; wide 308 vs 12,000. budget_exhausted: Part B full all 36/60, auto 30/60; Part A full all 25/90; all 20 runs in every Part C mode.

## [minor] /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:11-12, 79-81, 96-99

**Issue.** The text says all campaigns are 'reported in full, including failures', but some unfavorable outcomes are left out. (1) The campaign-1 historical suite of 4 models is not mentioned. On waterno2_06 the 6 s final bound was 26.59 for the baseline against 7.05 (all) and 2.41 (auto). (2) In the campaign-2 diagnostic suite, btest14 had a bound of -72.30 for the baseline against -115.60 in both cut modes before the repair. (3) The repair cohort still had worse cut-mode bounds at 1e-4, yet the text cites only the case that improved (graphpart_clique-40). On waterno2_06 the bound went from 81.64 to 76.75 with no cut added, and waterx was also worse. (4) In campaign 2, graphpart_clique-40 also had a worse root bound in both cut modes at 1e-4, which is not mentioned.

**Fix.** Either remove 'reported in full' or add one sentence per item, for example: 'In the repair cohort, the cut modes still had worse final bounds on two time-limited models (waterno2_06, 81.6 vs 76.8, with no cut added; waterx), which reflects the separator's time, not the cuts.'

**Evidence.** Raw records of campaign-v1 (suite historical), campaign-v2 (suite diagnostic) and repair-discovery-v1. The repair comparisons at 1e-4 that are not ties are waterno2_06 full (worse in all and auto) and waterx full (worse in all and auto).

## [minor] /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:219-224, 243; /workspace/minlp-notes/paper-certified-support-cuts/sections/B-tables.tex:96-99

**Issue.** The caption calls the prospective Part C mode 'Frozen ... the separator as used in all campaigns'. Its code was frozen, but its limits were not the frozen defaults of Table tab:limits: Part C used n-proportional raised limits.

**Fix.** Rename the column 'prospective' and write in the caption: '"Prospective" is the separator code used in all campaigns, with the n-proportional limits of the protocol; "row direction" is the post hoc variant ...'.

**Evidence.** Record configs. all-diag-mech: max_blocks n, max_cuts 4n, max_cuts_per_round n, max_rounds 10, max_support_calls 20n, 60 s, fraction 0.5. Frozen defaults: 32, 12, 4, 3, 24, 1 s, 0.05.

## [minor] /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:163-167

**Issue.** The worse root bound of auto on pooling_haverly2pq is large, but it is described only as 'a worse root bound'. More generally, cut strength is measured by the bound at the end of a one-node SCIP run, which SCIP's own separation and cut selection confound.

**Fix.** Quantify the effects as fractions of the root gap closed. Add an isolated measurement of cut strength, for example re-solving the final root LP with SCIP's cuts fixed, with and without the certified cuts. This separates cut strength from SCIP's separation dynamics.

**Evidence.** pooling_haverly2pq root runs: baseline -617.70, auto -857.14 with 1 cut, all and all-diag -617.70 with 2 cuts; optimum -600. The root gap grew 14.5-fold. Root gap closed elsewhere: ex3_1_4 0.105 (all/auto) and 0.154 (all-diag); pointpack04 0.078 (all), -0.026 (auto), 0.335 (all-diag).

## [minor] /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:197-199

**Issue.** 'About half a second per run, which is of the same order as SCIP's whole solving time on most of these models' understates the overhead. It is about 3.4 times the median SCIP time.

**Fix.** 'Over the 60 full runs this is about 0.55 s per run, more than SCIP's whole solving time on most of these models (median 0.16 s).'

**Evidence.** Part B mode all: 32.90 callback seconds over 60 full runs = 0.548 s per run. Median baseline scip_solve_seconds in Part B full runs: 0.160 s.

## [minor] /workspace/minlp-notes/paper-certified-support-cuts/sections/B-instances.tex:35-45

**Issue.** The selection description is incomplete. It omits (1) the parser-support filter, which removed 7 otherwise eligible models (tanh, log10, signpower, gammaFn, erf); (2) campaign 1's other criteria (at most 150,000 bytes, a quadratic or general nonlinear constraint, at least two nonfixed bounded variables, 123 excluded names, 279 eligible); (3) the MINLPLib snapshot version or date; (4) the hash prefixes ('convexification-holdout-v2:', 'convexification-structure-v3:').

**Fix.** Add these four items to the 'Selection' paragraph and archive the instance SHA-256 list with the supplement.

**Evidence.** research-20261003-convexification/experiments/holdout-selection.json lists 7 parser_errors, none of them among the 422 eligible models. research-20261002-convexification/experiments/protocol.md gives the campaign-1 filters. I recomputed the hash orderings from these prefixes and they match the frozen selections.

## [suggestion] /workspace/minlp-notes/paper-certified-support-cuts/sections/09-computations.tex:118-150, 295-309; /workspace/minlp-notes/paper-certified-support-cuts/sections/B-tables.tex:92

**Issue.** Some reporting a referee would expect is missing. (1) Uncertainty for time ratios, such as bootstrap confidence intervals or a paired signed-rank test over the 80 and 52 paired runs, and per-seed SGMs. Per-seed SGMs differ: the Part A baseline is 0.85, 1.13 and 1.19 s over different common sets. (2) A per-model table for Part A; only the names are listed. (3) Sec. 9.7 says timing differences are reported 'with the variation between baseline seeds for comparison', but only the bound variation is reported; the A/A time variation is not. (4) On the path family, a comparison with the dense SDP + McCormick relaxation that Section 6 says closes the family, or with SCIP at higher nonlinear-separation effort.

**Fix.** Add confidence intervals and per-seed SGMs to Table 2, the A/A time ratios to Sec. 9.4, and a per-model Part A table to Appendix B. Optionally add a dense-relaxation or SCIP-emphasis comparator for Part C.

**Evidence.** A/A baseline time ratio, seed 1 vs seed 0 in Part A: median 1.03, range 0.61-1.92; SGM 0.822 vs 0.852 over the 26 models solved by the baseline in both seeds.

# R5-impl

I checked the implementation statements in Sections 3.2, 3.3, 4.4, 5.3, 7.4, 8, 9 and Appendix B against the code and records. Sources: B = research-20261003-convexification/solver and theory, A = research-20261002-convexification/solver and theory, the v3 and v3d snapshots, records and replay files, and evidence/implementation-facts.md. I also checked SCIP's own source, using a download of v10.0.0 lp.c (SHA-256 3fab5cca…, matching the hash recorded in literature-L3.md) and the local 10.0.2 tree.

**Confirmed, no action needed:**
- **Work limits:** every Config value and limit (32/6/16/3/12/4/24/3, 2,000 subsets, 128 cells, depth 16), the 1e-5 and 5e-4 thresholds, the min{1 s, 0.05 T} allowance, and the auto rule (`integration.py:40-60, 251-265`).
- **Model builder:** the domain witnesses, the variable-power rule, the affine bound propagation, and the objective epigraph sides.
- **Export:** elimination plus the conservative two-bound rounding rule (`row_certificate.py:213-223`).
- **Polytope subset counts:** m includes the 2d box rows; 1,941 subsets for 7 sides at d=4, 2,517 for 8.
- **Separation routine:** the grid and export claims of Section 7.4.
- **Screening:** 2 skips out of 506 screen queries in campaign 1.
- **Campaign-2 timing:** 24.4 of 27.6 s, from the 30 holdout full runs.
- **Part B timing:** 23.0 / 3.9 / 4.4 of 32.9 s.
- **Replay totals:** 7,498 cuts with 14/14 corruptions rejected per mode; v3 snapshot integration.py = 128fe10b.
- **SCIP coefficient rounding:** lp.c rounds near-integral coefficients in rowAddCoef, rowChgCoefPos and also rowMerge (lp.c is identical in 10.0.2 apart from the copyright line). In a rerun of pooling_haverly3pq, the stored-row check caught SCIP storing −0.9999999999999998 as −1.
- **Exact mode is MILP only:** SCIP 10 report, Section 3.1.
- **Implicit discreteness:** presolveSingleLockedVars / checkvarlocks in SCIP 10.0.2. The n=10 path instance has 20 binaries after presolve.

**Main problems:**
- **Trust base (major):** it is incomplete, and the sentence "replay does not share SCIP" is wrong.
- **"Independent replay" (major):** the introduction calls the replay independent, which overstates it.
- **Diagnostic replay not reported (major):** the post hoc diagnostic behind the headline result has 30,000 cuts. Their replay finished after the PDF was built and is not in the paper.
- **Conclusions (major):** the second stated reason is contradicted by Section 9's own campaign-3 data.

The minor items are wording mismatches between Section 8 and the code, plus missing reports: stored-row rejection counts, the frozen campaign-2 code differences, and the size of the star-certificate partition.

Scratch scripts (read-only scans) are in paper-certified-support-cuts/verification/: R5-impl_scan_records.py, R5-impl_single_column_cuts.py, R5-impl_star_pieces.py and R5-impl_row_rejections.py.

## [major] sections/08-implementation.tex:136-144 (trusted base); also :27-31 and :38-39

**Issue.** The trust-base paragraph is incomplete, and one sentence contradicts the code.

(1) "It does not share ... SCIP" is wrong. Replay calls build_model, which creates a SCIP model through PySCIPOpt (addVar, addCons, and getLhs/getRhs for the stored guard sides). It only does not solve it.

(2) Replay re-executes the generator's own code, not just "the exact support routines": the model builder, bound replay, support kernels and row elimination/export.

(3) The trusted base omits several components:
- SymPy symbolic differentiation, which the chord bound uses.
- SymPy's automatic canonicalization when expressions are built (e.g. x/x→1, 0·log x→0).
- The OSiL reader's parsing of the expression structure; the text lists only its token-to-binary64 conversion, but replay re-reads the pinned file with the same reader.
- PySCIPOpt's translation of the checked expression object and of the unchanged row sides into SCIP constraints.

(4) "Reads back the expression submitted to SCIP" is imprecise. The check reads the Python-side PySCIPOpt Expr/GenExpr object before addCons; nothing is read from SCIP.

**Fix.** Replace lines 136-144 with: "Replay re-executes the generator's exact code: the model builder (which constructs, but does not solve, a SCIP model through PySCIPOpt), the bound replay, the support kernels, and the elimination and export routine. It has its own affine splitter and does not run the direction search, the LP solver or SCIP's solving process. The trusted base therefore consists of: Python's rational arithmetic; SymPy's expression construction (including its automatic canonicalization), expansion, polynomial conversion and differentiation; Arb through python-flint; the OSiL reader, both its parsing and its conversion of decimal tokens to binary64; PySCIPOpt's translation of the checked expression objects and row sides into SCIP constraints, and its accessors for stored rows; and the code shared by generation and replay. None of these is formally verified, and replay is a re-execution, not an independent checker. The certificates say nothing about ..."

At :28 say "reads back the PySCIPOpt expression object that it passes to SCIP". At :38-39 say "Its boundary is this expression object; PySCIPOpt's translation of it into SCIP's internal expression, and SCIP's later simplification, presolve and floating-point LP, are outside it."

**Evidence.** - `A/solver/model_binding.py:115-165`: native_expression reads `.terms`, `.children`, `.coefs`, `.constant`, `.expo` of the Python object.
- `B/reviews/model_binding_audit.py:74`: `rebuilt = build_model(original)`, called from `replay.py:316-317`.
- `A/solver/certified.py:338-345`: `_elementary_data` uses `sp.diff(scalar, symbols[0], 2)` for the chord bound (lines 363-373).
- `replay.py:378-386`: `load_expected_model` uses `uenv.osil.read_osil`.
- `model.py:386-391`: row sides go to `ExprCons` unchanged and are not read back.
- `issues-raised.md` SUP-5 and IMPL-12 already ask for this paragraph.

## [major] sections/01-introduction.tex:117-118

**Issue.** "Every recorded cut passed an independent replay" overstates the evidence. Replay shares the exact kernels, the bound replay, the model builder and the elimination code with the generator. Only the affine splitter is separate. Section 8.3 itself says replay "re-executes the exact support routines". The code's own docstrings and issues-raised SUP-5 ("Do not call replay an independent proof checker") say the same.

**Fix.** Replace with: "Every recorded cut passed replay in a fresh process against the source model and the recorded solver row; the replay re-executes the exact routines that produced the cut (Section 8.3)."

**Evidence.** - `B/experiments/replay.py:1-7`: "The support and affine-bound checkers share exact primitives with producers; this is an implementation audit, not formal or complete solver verification."
- `B/theory/quadratic_polytope.py:10-12` and `B/solver/row_certificate.py:249-256`: replay calls `certify_row_combination` itself.

## [major] sections/09-computations.tex:259-270 and :175-179; abstract 00-abstract.tex:23-27; 01-introduction.tex:113-118

**Issue.** The abstract and introduction headline (the root gap closed on all 20 path instances, all solved) comes from the post hoc row-direction diagnostic. The paper never reports a replay for those runs. The 7,498 cuts listed in Section 9.3 are Parts A-C only.

The diagnostic Part C runs recorded 30,000 cuts; the Part A and Part B root diagnostics recorded 469 and 529. The Part C replay.json was written at 12:00 on 2026-10-03, after main.pdf was built at 11:48. The current text therefore cannot support "every recorded cut passed replay" for the result it puts in the abstract.

**Fix.** In Section 9.6, after the diagnostic results, add: "Replay passed for all 30,000 cuts of the diagnostic runs on the path family and for the 469 and 529 cuts of the Part A and Part B root diagnostics; in each cut mode all 14 corrupted records were rejected." In Section 9.7, say that the replay statement covers the diagnostic runs.

**Evidence.** - `experiments/v3d/runs/partC-rowdir/replay.json`: passed, 30000/30000 cuts, 0 missing logs, tamper controls for all-diag-mech and all-diag-mech-wide.
- `partA-root-rowdir/replay.json`: 469/469; `partB-root-rowdir/replay.json`: 529/529.
- `v3d/runs/replay-partC-rowdir.log` was empty while the replay was running.

## [major] sections/10-conclusions.tex:30-33

**Issue.** The second stated reason for the negative result ("the frozen work limits allow few cuts, and discovery in Python costs more than the cuts return") contradicts Section 9's campaign-3 data.
- Section 9.5: "In campaign 3, discovery is fast and exact certification dominates." In Part B (all, full runs), certification took 22.97 s, LPs 3.85 s and discovery 4.39 s of 32.9 s; in Part A, discovery took 6.3 of 19.1 s.
- Section 9.3: raising the limits (all-diag) added cuts but improved the root bound on only one more model per part, so the limits were not the binding factor on MINLPLib.
- Discovery dominated only in the frozen campaign-2 code (24.4 of 27.6 s).

**Fix.** Replace with: "Second, where the structure occurs, the cuts the separator finds rarely move SCIP's bounds: raising the work limits added cuts but improved the root bound on only one more model per part. The separator's Python-level work, which in the final implementation is mostly exact certification (discovery before the repair), costs more than the cuts return on small models." Adjust "with discovery done once, at negligible cost" accordingly.

**Evidence.** - Scan of `v3/runs/partB/records.jsonl` (full, all): callback 32.90 s, certification 22.97 s, candidate 3.85 s, discovery 4.39 s over 60 runs.
- `v3/runs/partA-full`: callback 19.14 s, certification 8.57 s, discovery 6.33 s over 90 runs.
- `campaign-v2` holdout full runs (all): 27.63 s, of which discovery 24.41 s.

## [minor] sections/03-certification.tex:43-50; sections/08-implementation.tex:117-121

**Issue.** The text says the implementation reads back "the row that SCIP stores" and covers "a row that the solver changes after it has been submitted". The audit actually runs after SCIP has built the row and before addCut. SCIP's handling after addCut is not checked; for example, sepastore.c converts a single-variable cut into a bound change using a floating-point division lhs/vals[0].

The runs contain 2,150 such single-column cuts in the diagnostic Part C runs (the decisive cuts t_i ≥ min D_i) and 34 in Parts A/B. All have coefficient ±1, so no rounding occurred, but the stated scope is broader than the check.

The cuts are also added with removable=True and forcecut=True; the paper does not say so, although this matters for the root-bound discussion in Section 9.3.

On the lp.c claim: it is correct. The separator path (cacheRowExtensions → addVarToRow → flushRowExtensions) goes through rowAddCoef and rowMerge, which also rounds. The paper cites tag v10.0.0; the runs used 10.0.2, whose lp.c is identical apart from the copyright line.

**Fix.** At 03:43-50 write: "... and neither does a row that the solver changes while creating it: outside its exact mode, SCIP 10 rounds a row coefficient that is integral within its tolerance to that integer, without adjusting the sides (rowAddCoef, rowChgCoefPos and rowMerge in src/scip/lp.c). For this reason our implementation reads back the row that SCIP has created, before passing it to the separation storage, and compares it with the certified row. SCIP's later handling of the row, such as converting a single-variable cut into a bound change, is outside this check."

In Section 8.3 add: "Accepted rows are passed to SCIP as global, removable cuts with forcecut set."

**Evidence.** - `integration.py:509-523`: create row → audit → `addCut(row, forcecut=True)`; `removable=True` at line 510.
- SCIP 10.0.2 `sepastore.c:1016-1019` and `sepastoreApplyBdchg` (lhs/vals[0]).
- `lp.c:2223`, `2401`, `6319` (rounding comments); `scip_lp.c:1612` (flush → SCIProwForceSort → rowMerge).
- `verification/R5-impl_single_column_cuts.py` output.

## [minor] sections/09-computations.tex (Sections 9.3, 9.5); sections/08-implementation.tex:120-121

**Issue.** The paper never reports how often the stored-row check rejected a certified row, although it presents the check as a key component. The counts are substantial:

| Runs | Rejected | Accepted |
|---|---|---|
| Part A full, all / auto | 15 / 3 | 151 / 37 |
| Part B full, all / auto | 45 / 31 | 179 / 145 |
| Part B root, all-diag | 202 (127 on kall_circlespolygons_c1p12) | 358 |
| Part A root, all-diag | 41 | 403 |

Most rejections come from presolve-aggregated block variables, because the separator does not mark them do-not-aggregate. A rerun of pooling_haverly3pq (mode all, root) gave 6 rejections: 5 had aggregated columns with a nonzero row constant, and 1 had the coefficient −0.9999999999999998 rounded by SCIP to −1.0. That last case is direct evidence for the lp.c claim in Section 3.1.

**Fix.** Report the rejection counts per part and mode, together with the observed causes (aggregated variables, plus at least one coefficient rounded by SCIP). Note that protecting block variables from aggregation, or binding the aggregation exactly, would keep these rows. Mention this where Section 9.3 interprets all-diag as a test of whether the limits bound the effect.

**Evidence.** - `verification/R5-impl_scan_records.py` on `v3/runs/*/records.jsonl` (`separation.row_binding_rejections`).
- `verification/R5-impl_row_rejections.py . pooling_haverly3pq all` output: {'variable status AGGREGATED': 5, 'column set differs': 5, 'nonzero row constant': 5, 'coefficient changed (rounded to integer): -0.9999999999999998 -> -1.0': 1}.

## [minor] sections/08-implementation.tex:84-89

**Issue.** "The separator first tries, for each block, the support of each single source side" does not match the code. The first directions are (a, λ) = (0, e_j), which bound only the side's nonlinear remainder; Section 9.6 describes this correctly, so the two sections disagree.

Two further imprecisions:
- The LP separates the point from the convex hull of the samples plus the cone in the side coordinates (multipliers in [0,1]), not from the hull alone.
- Two work filters are omitted. An LP direction is used only if its scaled objective is below −1e-5 in both modes. For non-quadratic blocks, the support call must reach the target activity + threshold.

**Fix.** Replace with: "At an LP solution the separator first tries, for each block and each of its source sides j, the direction (a, λ) = (0, e_j), which bounds the side's nonlinear remainder alone (see Section 9.6). It then solves up to three LPs that separate the current point, after coordinate scaling, from the convex hull of sampled graph points plus the cone of the side coordinates; an LP direction is used only if its scaled violation exceeds 10^{-5}."

**Evidence.** - `integration.py:399-407` (`direction[d+j] = 1`, a = 0) and the code comment.
- `integration.py:325-331`: LP bounds and `result.fun >= -config.min_violation`.
- `integration.py:467-468`: target for non-quadratic blocks.

## [minor] sections/08-implementation.tex:90-95

**Issue.** The fallback description is imprecise in four ways.

(i) The "seven affine domain rows" are signed sides (an equality uses two), as are the 16 in line 79.

(ii) With at most 16 sides, the 2,000-subset budget is never exceeded for d ≤ 3 (N(22,3) = 1,794), so the fallback only happens for d = 4 with at least 8 sides.

(iii) For d = 4, only the star oracle can succeed: the Bernstein fallback is limited to 1-2 variables and the ball-arithmetic bound to one. Listing all three as alternatives misleads.

(iv) In campaigns 2-3 no cut carries `polytope_skipped`, and no star cut occurs (campaign 2: 91 polytope / 30 arb / 2 bernstein; campaign 3: only polytope, arb and bernstein). "The block yields no cut" should be "that direction yields no cut".

**Fix.** Replace with: "Quadratic blocks are certified with Theorem 5.1 when the number of row subsets is at most 2,000; for four variables this allows at most seven signed affine sides (an equality row counts twice), and with at most sixteen sides the budget is never exceeded in dimension three or less. Otherwise only the star oracle of Theorem 5.4 can apply, because the Bernstein bound is limited to two variables and the ball-arithmetic bound to one; if the block is not a star, that direction yields no cut. In campaigns 2 and 3 every quadratic cut came from the polytope enumeration."

**Evidence.** - `support.py:65-104`; `certified.py:342-345, 387-399`.
- `enumeration_size`: (4,7) = 1941, (4,8) = 2517, (3,16) = 1794.
- Method scan of v3 records: no `quadratic_star` and no `polytope_skipped`.

## [minor] sections/08-implementation.tex:75-77

**Issue.** Discovery admits polynomial remainders of total degree up to 8 in up to four variables, but no kernel certifies a non-quadratic polynomial in three or four variables. Bernstein handles 1-2 variables with at most 1,024 tensor coefficients and per-variable degree at most 32; Arb handles only one variable. Such blocks are admitted in mode all, always end as `unsupported`, and use up support calls and certification failures. The reader cannot see this from Section 8.2 or from Table B.

**Fix.** Add after line 77: "Polynomial remainders of degree three or more in three or four variables are admitted by discovery but are not certified by any kernel (Bernstein bounds need one or two variables and at most 1,024 tensor coefficients), so such blocks yield no cuts."

**Evidence.** - `integration.py:199-211` (admission).
- `certified.py:342-348` (`_leaf_bound`: Bernstein only for ≤ 2 variables and ≤ 1,024 coefficients; elementary only univariate).
- `implementation-facts.md` items 68 and 8.

## [minor] sections/09-computations.tex:68-69 and 90-94

**Issue.** "The second implementation is the one described in Section 8" is not accurate for campaign 2. The frozen campaign-2 integration.py (5620d3f2…) differs from the described code (128fe10b…) in four places:
- no discovery deadline;
- dense polynomial conversion without catching CoercionFailed or RecursionError;
- no rejection of a converted rhs or stored lhs at SCIP's infinity value;
- no catch for a failed exchange-sample evaluation.

The text names only the first two (as defects). issues-raised IMPL-15 asks the paper to say that the measured code is the frozen one.

**Fix.** Write: "The second implementation is, up to the repairs described below, the one of Section 8. Besides the two defects below, the repair added two guards: rows whose side reaches SCIP's infinity value are rejected, and a failed evaluation of an exchange sample is tolerated. A separate audit found all 123 recorded rows of campaign 2 below the infinity value."

**Evidence.** - `diff experiments/campaign-v2/snapshot/.../solver/integration.py solver/integration.py`: hunks at 125-158 (split), 187-263 (deadline), 357-358 (`abs(lhs) >= infinity`), 476-484 (exchange catch), 498-500 (`abs(converted.rhs)`).
- `implementation-facts.md` Section 4.

## [minor] sections/05b-star.tex:129-136

**Issue.** The implemented star oracle splits the center interval at all pairwise intersections of each leaf's bound lines, including lines that are not on the envelope, then recomputes every leaf rule per piece. Its certificate partition can therefore have Θ(Σ m_i²) pieces, more than the 2m+4k+1 intervals of Theorem 5.4. The certificate is still exact, and the O((m+k)³) cost bound holds.

Test: one leaf with 10 redundant tangent rows gave 43 pieces against the theorem's 25. "Intersects all pairs of envelope lines" should read "all pairs of a leaf's bound lines".

Also, "adequate for the blocks of Section 9, where k ≤ 4" holds for campaign 1 (125 star cuts). The star oracle certified no cut in campaigns 2 and 3.

**Fix.** Replace with: "Our implementation is simpler than the algorithm of the proof: it splits the center interval at all pairwise intersections of each leaf's bound lines and recomputes every leaf rule on every piece. This costs O((m+k)^3) operations, stores Θ(k) rules per piece, and can produce more pieces than Theorem 5.4 requires. This is adequate for the stars of campaign 1, which have at most four leaves; in campaigns 2 and 3 the polytope oracle certified every quadratic cut."

**Evidence.** - `A/theory/quadratic_star.py:97-116` (`combinations(lines, 2)`), `195-199`.
- `verification/R5-impl_star_pieces.py`: 'pieces 43 theorem bound 2m+4k+1 = 25'.

## [minor] sections/09-computations.tex:239-242; sections/10-conclusions.tex:28-30; sections/02b-related.tex:91-93

**Issue.** Section 9.6 says SCIP's presolve turns the leaves into binaries and refers to Section 6.1 for this, but Section 6.1 says nothing about SCIP, presolve or binaries; the reference dangles. The conclusions repeat the claim for the three-variable example ("strong branching closes the gap at the root") with no supporting evidence in the paper.

The claim itself is true:
- SCIP 10.0.2 `presolveSingleLockedVars`, parameter `constraints/nonlinear/checkvarlocks`: "fix a variable x_i to one of its bounds if the variable is only contained in a single nonlinear constraint g(x) ≤ rhs if g() is concave in x_i … with bounds [0,1] … changed to be binary".
- After presolve, the n=10 seed-0 Part C instance has 20 binaries out of 40 variables.
- experiments/pilot-native.md gives the root bounds 1/128 by default and −0.0559 without strong branching; L5 reports about −1.16e-4 with checkvarlocks=d.

The related-work wording "presolves variables that occur only concavely to binaries" omits the conditions: single constraint, no objective coefficient, and [0,1] bounds (otherwise a bound disjunction is added).

**Fix.** At 09:241-242 replace the reference with: "which its presolve turns into binaries, because each x_i and z_i occurs only in its own row, where D_i is concave in it (SCIP's implicit-discreteness reduction, constraint parameter checkvarlocks; \citealp[Section 4.2.7]{SCIP8report})."

In Section 6.1 or 9.6, report the pilot root bounds: 1/128 by default, −0.056 without strong branching, about −1e-4 with checkvarlocks disabled.

At 02b:91-93 write: "fixes a variable that occurs in a single nonlinear constraint, which is concave in it, to one of its bounds and makes it binary when its bounds are [0,1]".

**Evidence.** - SCIP 10.0.2 `cons_nonlinear.c:5654-5666, 5849, 12678-12680`.
- `R5-impl` presolve probe: `transformed types {'BINARY': 20, 'CONTINUOUS': 20}`.
- `experiments/pilot-native.md`; `evidence/literature-L5.md:115-135`.

## [minor] sections/08-implementation.tex:42-43

**Issue.** "0·log x, x/x, (√x)² and (log x)⁰ are each defined only for x>0 or x≠0" is wrong for (√x)², which is defined for x ≥ 0. The model builder records sqrt as a nonnegativity requirement.

**Fix.** Write: "... are defined only for x>0, x≠0, x≥0 and x>0, respectively."

**Evidence.** `B/solver/model.py:195-197`: sqrt → `require("nonnegative", ...)`.

## [minor] sections/03-certification.tex:157-163

**Issue.** The text says a bound computation has three outcomes. The kernels return four: complete, `empty`, unsupported and incomplete. `empty` occurs when every cell is excluded by a domain row, or when the polytope or star domain is empty. Proposition 3.3 already mentions this case, and the separator treats it as a certification failure. The quoted-out "no bound is returned" (lines 125-126) is fine at the level of the whole computation: an unresolved cell is subdivided until the depth budget, then the result is incomplete.

**Fix.** Write: "A bound computation returns one of four outcomes: a certified bound with its partition, empty (every cell is excluded by a domain row, so D = ∅), unsupported (an operation outside the grammar), or incomplete (a work limit was reached)."

**Evidence.** - `certified.py:441-443` (status "empty").
- `support.py:79-80`; `quadratic_star.py:189-191`; `quadratic_polytope.py:223-224`.

## [minor] sections/07-separation.tex:177-184

**Issue.** "within tolerance with a mixture certificate" describes only one of the two within-tolerance answers the routine gives. After the grid fallback, the answer is a finite normal net: one feasible support minimizer per grid direction, checked against the bound error + 2R/N ≤ ε. That answer is not a mixture of at most k+1 points as in Theorem 7.2. Both forms need only feasible points and exact arithmetic, so the following sentence remains correct.

**Fix.** Write: "... within tolerance, with either a mixture certificate or, after the grid fallback, one exactly feasible point per grid direction ..."

**Evidence.** - `B/solver/separation.py:404-421` (`finite_normal_net` witness).
- Replay at `separation.py:459-472`.

## [minor] sections/08-implementation.tex:133-134; sections/09-computations.tex:178-179

**Issue.** The "fourteen deliberately corrupted records" are fourteen single-field mutations of the first cut of one record, per part and cut mode. None alters a domain row or a source-side multiplier λ; the field `support_coefficient` changes a block-variable coefficient. Campaign 1 used a different checker with 12 controls. The text reads as if 14 independent records were corrupted.

**Fix.** Write: "For one recorded cut in each cut mode, fourteen single-field corruptions check that replay rejects altered inputs: model hash, support normal, source-side rhs and identity, feature, box, row rhs, scope, rounding correction, support identity, stored coefficient, stored side, column mapping and bound proof." Consider adding controls for a domain row and for a multiplier.

**Evidence.** - `replay.py:337-375`.
- v3 `replay.json` field `v3.tamper_scope`: 'archived mutations applied to the first cut of the record'.
- `implementation-facts.md` Section 5.2: campaign 1, 12/12.

## [minor] sections/B-instances.tex:4-7, 17-29 (Table tab:limits)

**Issue.** The limits table has several imprecisions and omissions.
- "16 affine rows" are 16 signed affine sides.
- "LP exchange rounds 3 per block and callback" omits that one remainder-only direction per source side comes first.
- "the diagnostic modes of campaign 3 raise only the limits named in Section 9.3": the Part C limits are named in Section 9.6, and all diagnostic modes also set separation_budget_fraction to 0.5.
- Missing settings that affect results: the sampling design (campaigns 2-3: 33-point 1D grid, 7×7 2D grid, 3^d for d = 3, 4, plus exact vertices and centroid for quadratic blocks within budget; HiGHS 0.05 s per LP, one thread; campaign 1: 65 / 13×13 / 128 Halton points plus corners, 0.1 s); nonpolynomial sides admitted only in one variable; Bernstein per-variable degree ≤ 32; Arb precision 128 bits; cut flags (global, removable, forcecut).

**Fix.** Change "16 affine rows" to "16 signed affine sides". Change the exchange row to "one direction per source side, then 3 LPs per block and callback". Change the paragraph to "raise the limits named in Sections 9.3 and 9.6 and set the budget fraction to 0.5". Add rows for sampling and the LP time limit, nonpolynomial admission, Bernstein degree, Arb precision and cut flags.

**Evidence.** - `integration.py:40-60, 225-250, 284-313, 325-329, 509-510`.
- `v3/v3_worker.py:24-41`; `v3d/v3_worker.py` (wide mode).
- `certified.py:111, 154`.
- `implementation-facts.md` Section 5.2.

## [minor] sections/08-implementation.tex:99

**Issue.** "Mode all attempts every admitted block" does not hold under the caps. Blocks are processed in a fixed order, largest first, and a callback stops after 4 cuts, 24 support calls in total, or the allowance. Later blocks may never be tried; Section 9.6 shows this matters for the path family.

**Fix.** Write: "Mode all tries the admitted blocks in a fixed order, largest first, until a cap is reached."

**Evidence.** - `integration.py:226` (order), `447-449`, `459-460` (per-callback cap), `387-392` (`_expired`).

## [suggestion] sections/08-implementation.tex:142-144

**Issue.** "SCIP's exact mode, which does certify complete solves, is limited to MILP" is correct on the MILP restriction (SCIP 10 report, Section 3.1). However, exact mode solves without tolerances; a certificate of the complete solve exists only if the optional VIPR output (certificate/filename) is written and then checked externally.

**Fix.** Write: "SCIP's exact mode, which solves MILPs without tolerances and can write VIPR certificates of complete solves for independent checking, is limited to MILP \citep{SCIP10}."

**Evidence.** `literature/papers/hojny2025-the-scip-optimization-suite-10/fulltext.md:207-209`.

## [suggestion] sections/03-certification.tex:126-128

**Issue.** The example "x log x/x still requires x>0" does not show where the guarantee is implemented. SymPy simplifies x·log(x)/x to log(x) as soon as the expression is built (and x/x to 1, 0·log x to 0), before any kernel sees it. The kernel only prevents cancellation across features (it evaluates every original feature on the whole cell). Requirements lost within a feature are kept by the model builder, which walks the raw OSiL tree (Section 8.1); issues-raised SEP-11 makes the same point.

**Fix.** Add: "In our implementation, requirements are collected from the raw source tree before any symbolic simplification (Section 8.1), and every original feature is enclosed on the whole cell before features are combined."

**Evidence.** - `certified.py:349-356` (zero-weight features evaluated).
- `model.py:138-219` (raw-tree traversal).
- `issues-raised.md` SEP-11.

## [suggestion] sections/08-implementation.tex:49-54

**Issue.** The existential witnesses describe strict domains exactly over the reals. SCIP, however, enforces du = 1 and u ≥ 0 only within its feasibility tolerance, so the strict domain holds only up to tolerance in the floating-point solve (issues-raised IMPL-9).

**Fix.** Add: "(exactly over the reals; SCIP enforces these constraints with its feasibility tolerance)".

**Evidence.** `issues-raised.md` IMPL-9; `model.py:343-361`.

## [suggestion] sections/09-computations.tex:87-88 and 193-195

**Issue.** "Discovery accounted for 24.4 of the 27.6 callback seconds of mode all" matches only the 30 holdout full runs with seed 0. Over all 92 campaign-2 runs in mode all, the figures are 81.9 of 88.5 s; the remainder comes from diagnostic models, seed-1 repeats and root runs. In the same runs, discovery alone exceeded the allowance in 23 runs per cut mode.

**Fix.** Write: "on the 30 holdout full runs, discovery accounted for 24.4 of the 27.6 callback seconds of mode all".

**Evidence.** Scan of `campaign-v2/records.jsonl`: ('all', holdout, full, seed 0) callback 27.63 s, discovery 24.41 s, candidate 0.67 s, certification 2.36 s; all runs of mode all 88.51 / 81.91 s.

# R6-writing

The paper is mostly written in the requested style: plain, direct and largely free of hype. Section openings orient the reader. The introduction states the problem as four questions and maps each answer to a section. The problems are mainly about consistency and precision.

(1) Three summary claims do not match the reported results:
- The path-family success is credited to the row direction alone, and the abstract does not say it was post hoc.
- "The cuts never changed which models SCIP solved" is contradicted by campaign 1.
- The conclusion's reasons for the negative result contradict Sections 9.4-9.6.

(2) Section 8.2 describes the first directions in a way that hides the defect found in Section 9.6.

(3) Notation is heavily overloaded. The worst case is Section 7, which reuses k and F with new meanings while the introduction states that section's results in terms of k.

(4) The conclusion restates the introduction. Limitations and novelty disclaimers are repeated across sections.

(5) Layout: Figure 2 has an arrow drawn through a box. There are four overfull lines, and two appendix tables and Figure 1 are never referenced.

Checks run (all read-only on the manuscript):
- pdftotext -layout and pdftoppm page renders of main.pdf.
- grep of main.log for Overfull and undefined references: four overfull boxes, no undefined references.
- grep counts of terms and label references.
- Python over experiments/v3/runs/partC/records.jsonl for per-copy root bounds, and over partB/records.jsonl for objective sense.
- Read of experiments/v3d/README-diagnostic.md and of RowSeparator._directions in research-20261003-convexification/solver/integration.py.
- A scratch compile of a corrected pipeline figure in /tmp/R6fig.

Scratch script written: /workspace/minlp-notes/paper-certified-support-cuts/verification/R6-writing_long_sentences.py. No CI or project-wide checks were run.

## [major] sections/00-abstract.tex:25-27; sections/01-introduction.tex:112-116; sections/09-computations.tex:290-292

**Issue.** The path-family result is credited to the direction search alone ('once the direction search tried each row's own direction'). Table 2 shows that the row direction with the original limits closed only 43-46% of the root gap and solved 10/20 instances (5,5,0,0), barely more than the 9 solved by baseline and frozen. Full closure and 20/20 solved also needed raised limits (4n cuts per callback, 16n cuts, 40n support calls; 09-computations.tex:261-263). The result is also a post hoc diagnostic (09:259-262, 09:306-309). The abstract does not say so, and the introduction says so only indirectly.

**Fix.** Abstract, replace the last sentence with: 'On a constructed family with the path structure, the separator as specified before the experiment closed a median of 19-35% of SCIP's root gap; a post hoc variant that tried each row's own direction first and allowed more cuts closed the gap and solved all 20 instances within 300 seconds, against 9 for native SCIP.'

Introduction 112-116, replace with: 'On a constructed family of path blocks, the separator as specified before the experiment closed a median of 19-35% of SCIP's root gap. A post hoc variant that tries each row's own direction first and allows more cuts closed the gap completely and solved all 20 instances within 300 seconds, against 9 for native SCIP; the row direction alone, with the original limits, closed 43-46%.'

Section 9.7, 291-292, replace with: 'On the constructed family, a post hoc variant that tried each row's own direction first and allowed more cuts turned time-outs into root solves.'

**Evidence.** Table 2 (09-computations.tex:231-234): row dir. columns 0.44/0.44/0.43/0.46 closure and 5/5/0/0 solved; only 'row dir., wide' reaches 1.00 and 5/5/5/5. experiments/v3d/README-diagnostic.md confirms that two separate changes were made: the direction order and the wide limits.

## [major] sections/00-abstract.tex:23-24; sections/01-introduction.tex:107-110; sections/09-computations.tex:285-286; sections/10-conclusions.tex:25-26

**Issue.** These passages say the cuts never changed which models SCIP solved 'in any campaign, mode or seed'. Section 9.2 reports the opposite for campaign 1: baseline and control solved 19 of 20 models, both cut modes only 18, and genpooling_lee2 was lost to the time limit in both cut modes (09-computations.tex:53-55).

**Fix.** State the exception wherever the claim appears, for example in Section 9.7: 'Apart from one model that both cut modes lost to the 6-second limit in campaign 1, the cuts never changed which benchmark models SCIP solved.' Abstract: '...but the cuts made the solves slower and, apart from one model lost at a 6-second limit, did not change which models SCIP solved.' Alternatively, restrict the claim explicitly to campaigns 2 and 3.

**Evidence.** research-20261002-convexification/experiments/campaign-v1/results.md: holdout baseline 19/24, control 19/24, all 18/24, auto 18/24.

## [major] sections/10-conclusions.tex:25-34

**Issue.** The conclusion's account of the computational results contradicts the body in five ways.
(a) 'on the path example its presolve turns the leaves into binaries and strong branching closes the gap at the root' relies on a pilot that is not reported in the paper (experiments/pilot-native.md). It also conflicts with Section 9.6: SCIP's root bound on the family is weak, and 11 of 20 instances time out.
(b) 'the frozen work limits allow few cuts' conflicts with Section 9.4 (09:169-173): raising the limits (all-diag) improved the root bound on only one more model per part.
(c) 'discovery in Python costs more than the cuts return' conflicts with Section 9.5 (09:195-197): in the final implementation certification takes 23.0 of 32.9 callback seconds and discovery only 4.4.
(d) 'the cuts close part of the root gap' omits the full closure reported in the abstract and introduction, so the three summaries tell different stories.
(e) 'SCIP's root relaxation is provably weak' is not proved anywhere; Theorem 6.2 concerns glued pair hulls, not SCIP's relaxation.

**Fix.** Replace lines 25-39 with: 'The computations show that this strength rarely matters on MINLPLib models. Apart from one model lost at a 6-second limit, the cuts did not change which models SCIP solved. Raising the work limits at the root improved the root bound on only one more model per part. In the final implementation the 15-40% slowdown is dominated by exact certification, not by discovery. On the constructed path family, where SCIP's root bound is far below the optimum, the cuts as specified closed 19-35% of the root gap, and a post hoc variant that tried each row's own direction first and allowed more cuts closed it completely. The components may be useful as the certified cut source of a solver that must justify each relaxation step, inside a native constraint handler that runs discovery once in compiled code, and for model classes such as pooling and networks with shared flows, whose blocks are stars with linking rows.' If the strong-branching observation is kept, report it in Section 9.6 together with its numbers: root bound 1/128 with defaults and -0.0559 with strong branching disabled, on the Proposition 6.1 instance.

**Evidence.** 09-computations.tex:239-248 (weak root bound, time-outs), 169-173 (all-diag), 195-197 (cost breakdown); experiments/pilot-native.md is the only source for the strong-branching claim.

## [major] sections/08-implementation.tex:84-85

**Issue.** 'At an LP solution the separator first tries, for each block, the support of each single source side.' A reader understands this as the support of the whole row, which is the 'row direction' of Section 9.6. The frozen code actually used a=0 with multiplier e_j, so it bounded only the nonlinear remainder. Section 9.6 identifies exactly this as the reason for the partial closure. As written, the implementation section hides the defect that the computational section diagnoses.

**Fix.** Replace with: 'At an LP solution the separator first tries, for each block and each of its source sides, the direction with $a=0$ and multiplier one on that side. This bounds only the side's nonlinear remainder; the side's affine terms in the block variables enter the cut only through the elimination (Section~\ref{sec:mechanism} shows the consequence).'

**Evidence.** research-20261003-convexification/solver/integration.py:399-407 (RowSeparator._directions yields direction[d+j]=1 with all block coefficients zero); 09-computations.tex:255-257.

## [major] sections/07-separation.tex:17-31 (also Theorem 7.2, Appendix A.6); sections/01-introduction.tex:92-98

**Issue.** Section 7 silently redefines F and k. In Section 2, F lists the k expressions and the graph is (x,F(x)). In Section 7, F:R^d->R^k lists all lifted coordinates, including x (F=(x,g(x))), so k is the lifted dimension (n+m). The introduction states the Section 7 results ('at most k+1 graph points', 'O(k^2 log(kR/eps))') where k still means the number of expressions, and R and eps are undefined there. The bounds are therefore misread. In addition, line 26 omits the equality rows: K in Theorem 4.2 includes h(u), so F=(x,g(x)) with query (x̄, b-Av̄) is not the set K+Q unless p=0.

**Fix.** 07-separation.tex:17-19: 'let $F:\R^d\to\R^r$ be continuous, where $F$ lists all lifted coordinates, including the variables themselves, and let $\bar z\in\Q^r$ be the query'. Rename k to r throughout Section 7 and Appendix A.6.

Line 26: 'For $F=(x,g(x),h(x))$, the query $(\bar x,b-A\bar v,e-C\bar v)$ and $J$ equal to the coordinates of $g$, this is the set $K+Q$ of Theorem~\ref{thm:closure}.'

Introduction 93-97: '...certifies, with at most $r+1$ graph points, where $r$ is the number of lifted coordinates, that the query is within a given distance of the hull; an ellipsoid variant needs $O(r^2\log(rR/(\epsilon-\delta)))$ oracle calls, where $R$ bounds the $\ell_1$ distance from the query to graph points and $\delta$ is the oracle accuracy, and does not require the hull to be full-dimensional.'

## [minor] sections/10-conclusions.tex:3-23

**Issue.** Paragraphs 1-2 of the conclusion restate contributions 1-4 of the introduction almost clause by clause: strongest inequalities, certificate scope, projection of the lifted relaxation, Lagrangian gap, two exact quadratic cases, path analysis, representation versus strength. They add no consequence the introduction does not already state.

**Fix.** Replace paragraphs 1-2 with two or three sentences on consequences for solver design, for example: 'Two consequences matter for solver design. Certification does not constrain how directions are found: only the final binary64 row, its whole-domain bound and the row the solver stores need to be checked. The advantage of joint quadratic blocks over their pairs is one of representation: dense moment relaxations with products absent from the model close the same gaps, and support cuts obtain that strength in the model's own coordinates.' Then continue with the corrected computational paragraph and the open questions.

## [minor] Global notation; worst cases at sections/06-composition.tex:39-46,77-81,150-152,242-249; sections/09-computations.tex:208,254; sections/A-proofs.tex:9-12,179

**Issue.** Many symbols carry several meanings:
- D: support domain (Sections 2-4, 8.2); the quadratic D, D_A, D_C, D_L, D_R (Section 6, A.4); the rows D_i (Section 9.6); the diameter D_inf (Lemma 7.3).
- u: the endpoint of [l,u] and u=y-a_1-(a_2-a_1)x in eq. (16), within the same family.
- S: selection matrix (4.1), row subset (5.1), star domain (5.3, Cor. 6.5), net S_M (7.3).
- T: affine map (4.2), tangent space (proof of Thm 5.1), triangle (5.2), A∪C (A.3).
- R: glued set (6), R_1/R_inf (3.3), l1 bound (7), R_0 (A.2).
- K: hull (4.2), K_S (5.1), K_L/K_R (6.3).
- h: support value h_D (2), equality functions (4), h(c) (7).
- delta: gap distance (6), oracle accuracy (7), shear (5.3).
- lambda: multipliers, KKT multipliers, encoding lengths lambda_q and lambda_A, convex weights.
- k: expressions, leaves, moments, lifted dimension, a summation index in N(m,d).
- Encoding lengths are lambda_q, lambda_A in 05-quadratic-support.tex:93-94 but eta, alpha in A.1, while A.5 uses eta(r) for something else.
- Lifted moment coordinates are (X,Y,Z) in 5.2 but (s_x, s_y, p_xy) in 6.1.
- 'separator' means both the SCIP plugin and a graph separator (06:229, 06:273-275).

**Fix.** At minimum:
- Rename the Section 6 quadratic D to \Phi (\Phi_A, \Phi_C, \Phi_L, \Phi_R) and the rows in 9.6 to \Phi_i(x_i,y_i,z_i)-t_i\le0.
- Rename u, v in eq. (16) to \xi_A, \xi_C.
- Use one notation for encoding lengths in Section 5.1 and A.1.
- Write (s_x, s_y, p_xy) in Section 5.2.
- Say 'separating variable' or 'clique separator' for the graph notion.
- Add a short notation paragraph at the start of Section 2 for the global symbols (D, F, k, n, H_D, h_D) and keep other letters local.

## [minor] sections/06-composition.tex:43,93; 02-background.tex:35; 05-quadratic-support.tex:3; 08-implementation.tex:73-103; 09-computations.tex:48,69,90,126; 02b-related.tex:43; 05b-star.tex:107; figures/pipeline.tex:10

**Issue.** Several terms are used without definition or before they are defined:
- 'linearization' of a quadratic (Prop. 6.1 and later).
- 'the gap between H and R in the direction of D' (Thm 6.2).
- 'block' (Section 2, defined only in 4.1).
- 'feature' (first in Section 5; Section 2 says 'expression' or 'function').
- 'side' versus 'row' (Section 8.2 and Table 3 mix 'nonlinear sides' and 'nonlinear rows').
- 'mechanism cases' (never described).
- 'frozen' (introduction l.115, Section 9.3) and 'prospective' (Section 9.3), never defined.
- Abbreviations: RLT (first at 02b-related.tex:43, expanded only at 05:156), SOC, DAG (Figure 2), SGM (Table 1 header), MINLP (introduction l.57).

**Fix.** Add definitions at first use:
- Section 6.1: 'The linearization of a quadratic is the linear function of $(m,s,p)$ obtained by replacing each monomial by its coordinate; the gap in a direction is the difference between the minima of the linearization over $H$ and over $R$.'
- Section 2: 'We call $x$ together with $F$ a block, and the $f_j$ its features.'
- Section 8.2: 'A ranged row $\ell\le g\le u$ has two sides, $g\le u$ and $-g\le-\ell$.'
- Section 9.2: one sentence describing the 13 mechanism cases, or a pointer to an appendix list.
- Section 9: 'Before each campaign the code and limits were frozen and the protocol fixed (prospective); analyses designed after seeing results are labeled post hoc.'
- Expand RLT, SOC, DAG and SGM at first use.

## [minor] sections/09-computations.tex:242

**Issue.** '(Section~\ref{sec:path-example})' is cited as the source for 'SCIP closes the gap by branching on the leaves, which its presolve turns into binaries'. Section 6.1 says nothing about SCIP's presolve or binaries. The fact appears in Section 2.1 ('presolves variables that occur only concavely to binaries').

**Fix.** Change the reference to Section~\ref{sec:related}, or to the pilot result if that is added to Section 9.6.

## [minor] sections/09-computations.tex:239 and 289

**Issue.** (1) 'between -0.031 and -0.022 per copy on average' matches no statistic of Table 5. Per instance, root/n ranges from -0.035 to -0.013. The per-n means range from -0.029 to -0.025, and the overall mean is -0.027. (2) Section 9.7 says 'about 15-20%' for the campaign-2 models, but Section 9.4 says 15-21%, which matches Table 1 (1.21/1.05 and 1.27/1.05).

**Fix.** (1) 'SCIP's root bound on these instances is weak: between $-0.035$ and $-0.013$ per copy (mean $-0.027$), while each copy contributes at least $1/8192$ to the optimum.' (2) Use '15--21\%' in Section 9.7.

**Evidence.** Computed from experiments/v3/runs/partC/records.jsonl (baseline, node_limit 1): per-n mean -0.0273/-0.0250/-0.0290/-0.0249; min -0.0354; max -0.0131.

## [minor] sections/01-introduction.tex:117

**Issue.** 'Every recorded cut passed an independent replay' overstates the check. Section 8.3 (08-implementation.tex:136-137) says replay re-executes the same exact support routines; it is independent only of the direction search, the LP solver and SCIP.

**Fix.** 'Every recorded cut passed replay in a fresh process against the archived source model and the stored solver row.'

## [minor] sections/B-tables.tex:1-43 (Table 4), 47-79 (Table 5); figures/chords.tex:41 (Figure 1); sections/09-computations.tex:120-123, 219-224

**Issue.** Table and figure problems:
- Table 4, Table 5 and Figure 1 are never referenced in the text.
- Table 4 does not give the objective sense. pointpack02 and pointpack04 are maximization models, so all-diag's 1.109 against the baseline's 1.164 is an improvement, and without the sense the reader cannot tell.
- The Table 2 caption says 'Frozen is the separator as used in all campaigns', but Part C used limits proportional to n (09:213-215), not the campaign defaults.
- The Table 1 caption does not explain the column 'Runs faster than baseline' or the abbreviation SGM.
- Table 5 packs status, nodes and seconds into one cell ('o 2562 3').
- Negative numbers in Tables 4-5 are typeset as hyphens ('-450.2').

**Fix.** - Reference Figure 1 in Section 6.2 (after Theorem 6.2), Table 4 in Section 9.4 (Part B paragraph) and Table 5 in Section 9.6.
- Add a sense column to Table 4, or the caption note 'pointpack02 and pointpack04 are maximization models; for them a smaller bound is stronger'.
- Table 2 caption: '"Frozen" is the campaign code with the Part C limits'.
- Table 1 caption: add 'SGM: shifted geometric mean (shift 1 s); last column: paired runs in which the cut mode was faster'.
- Split the status, nodes and seconds columns in Table 5.
- Write negative numbers as $-450.2$.

**Evidence.** experiments/v3/runs/partB/records.jsonl: sense='max' only for pointpack02 and pointpack04.

## [minor] main.log; sections/06-composition.tex:51-55 (PDF p.16); sections/07-separation.tex:142-148 (PDF p.22); sections/B-tables.tex:45 (PDF p.41)

**Issue.** main.log reports four overfull lines:
- 12.9pt and 35.8pt in the proof of Proposition 6.1 (inline moment vectors run into the margin).
- 9.0pt in the statement of Lemma 7.3 (inline definition of Lambda).
- 19.9pt in the Appendix B list of model names (\code names cannot be hyphenated).

**Fix.** - Proof of Prop. 6.1: display the two moment vectors, e.g. \[ (m_x,m_y,s_x,s_y,p_{xy})=(\tfrac12,\tfrac12,\tfrac12,\tfrac5{16},\tfrac38),\quad (m_y,m_z,s_y,s_z,p_{yz})=(\tfrac12,\tfrac45,\tfrac5{16},\tfrac45,\tfrac12). \]
- Lemma 7.3: move $\Lambda\ge\sum_j\sum_i\max_B|\partial_iF_j|$ to a display.
- Appendix B: set the model-list paragraph in {\raggedright ...\par}, or as a three-column table.

## [minor] figures/pipeline.tex:12,23 (Figure 2, PDF p.23); figures/chords.tex:15 (Figure 1, PDF p.17)

**Issue.** Figure 2: the dotted 'LP point' arrow runs along the top edge of the 'exact support' box and strikes through its first line of text, and the label sits on the arrow. Figure 1(a): the label 5/8 lies on the solid chord of A near the crossing point.

**Fix.** pipeline.tex: change line 12 to \node[num,below=14mm of src] (disc) {block discovery}; and line 23 to \draw[->,dotted] ([xshift=2mm]scip.south west) -- ++(0,-8mm) -| node[pos=0.25,above,font=\small] {LP point} (lp.north); (a scratch compile in /tmp/R6fig showed no overlap). chords.tex:15: use node[below right] {$\tfrac58$}.

## [minor] 01-introduction.tex:106-130; 08-implementation.tex:38-39,133-134,141-144; figures/pipeline.tex:27-28; 09-computations.tex:16-20,35-37,87-88,178-179,193-195,283-303; 10-conclusions.tex:25-39; 02b-related.tex:51-55,64; 06-composition.tex:6-9,221-227,272-274

**Issue.** Several limitations and facts are stated three or four times instead of once where they matter:
- What the certificate does not cover: introduction 128-130, 8.1 end, 8.3 end, Figure 2 caption.
- The negative result and the recommendation: abstract, introduction 106-126 (a near duplicate of 9.7), 9.7, conclusion.
- Shared host: 9.1 and 9.7.
- SCIP's exact mode is MILP-only: 2.1, 8.3, conclusion.
- Fourteen corrupted records: 8.3, 9.1, 9.4.
- 'Discovery accounted for 24.4 of 27.6 callback seconds': 9.3 and 9.5, verbatim.
- 'Representation, not strength': introduction, 5.2, 6.4, conclusion.
- Gluing literature (Vorob'ev, Lasserre, Fantuzzi-Fuentes, Nie): 2.1, the Section 6 opening, 6.4, 6.5.

**Fix.** - Keep the certificate scope in Section 8.3 only (the Figure 2 caption may keep one clause), and delete 08:38-39 and the clause at 01:128-130.
- Cut introduction 106-126 to three sentences: the result, the path-family result with its post hoc status, and a pointer to Section 9.7.
- Delete the second '24.4 of 27.6' sentence (09:193-195) and the corrupted-records sentence in 9.1.
- Keep the detailed gluing comparison in 6.4; reduce 2.1 to a pointer and the Section 6 opening to one clause.

## [minor] 01-introduction.tex:56-59,71-72,77-78,97-98; 02b-related.tex:72-74; 03-certification.tex:30,96-98,108; 04-original-variables.tex:12-14,181-183; 05-quadratic-support.tex:100-102,152; 05b-star.tex:97-98,111-113; 06-composition.tex:6-9,183-186,236-239; 07-separation.tex:9-10

**Issue.** Positioning disclaimers recur throughout: 'classical' (9 times), 'elementary' (5), 'is known' (2), 'to our knowledge' (3), 'We know of no', 'we do not claim', 'our use of it is ordinary', 'The statement is elementary, and the principle behind it is established'. The novelty claim for the certification contract appears twice, almost word for word (introduction 56-59 and 2.1 at 72-74). The cumulative effect reads as defensive and makes it harder to find what is new.

**Fix.** State each novelty claim once, in the contribution list, and keep only the citation at the point of use. Delete 'our use of it is ordinary' (03:97-98) and 'the construction itself ... is elementary' (05b:111-113). Shorten 03:30 to 'The principle is established:'. Replace 06:6-9 with 'Gluing local convex hulls along shared variables can fail because finitely many shared moments do not determine the shared distribution [cites].' Remove the duplicate novelty sentence at 02b-related.tex:72-74.

## [minor] sections/00-abstract.tex:1-28

**Issue.** The abstract has 297 words, above the usual 150-250 for MP, JOGO and IJOC. It uses delta (line 18) without defining it. It packs three claims into one sentence (lines 10-13) and contains the misleading path-family sentence noted above.

**Fix.** Shorten to about 250 words. Replace 'the gap is either zero or $\delta^2/2$, depending only on whether two point sets interleave' with 'exact pair hulls glued on $k$ shared moments miss a gap exactly when the local zero sets alternate at least $k+1$ times; for two moments on three-variable paths this happens exactly when two point sets interleave'. Drop the sentence 'An exact finite procedure completes the separation to any positive tolerance.', or reword it as 'A finite exact procedure either finds a violated cut or certifies that the point is within any given distance of the hull.' Use the corrected computational sentences given above.

## [minor] sections/09-computations.tex:7-12,105-112; sections/01-introduction.tex:103; sections/00-abstract.tex:22-23

**Issue.** Section 9 says 'We report three campaigns on MINLPLib models and one on a constructed family', but the constructed family is Part C of campaign 3 (09:111-112), and the replay totals count it inside campaign 3 (09:177). Section 9.7 says 'three campaigns and the constructed family'. The count shifts between three and four. The sentence 'The first two campaigns were run with time budgets fixed in advance' also implies that campaign 3 was not, although campaign 3 had a fixed protocol.

**Fix.** 09:7-10: 'We report three campaigns. Each was run with code, limits and protocol fixed in advance; the third consists of a repeat of campaign 2 with longer budgets and seeds (Part A), a structure-selected sample (Part B) and a constructed family (Part C).' Use the same wording in the introduction and the abstract.

## [minor] 08-implementation.tex:42-43,16-19; 05b-star.tex:116,86-89; 04-original-variables.tex:107,140; figures/chords.tex:39-40; 02-background.tex:48-49; 03-certification.tex:3; 01-introduction.tex:19-20; 06-composition.tex:290

**Issue.** Local precision errors:
(a) '(√x)^2 ... defined only for x>0 or x≠0': (√x)^2 is defined for x≥0.
(b) 'The argument uses that every leaf is a leaf.' is a tautology.
(c) Corollary 4.3 proof uses ĝ, which is not defined (only ĥ is).
(d) Theorem 4.2 proof uses the coordinates (u,y,η) without introducing them.
(e) 'a family whose decision set has r! components': r is undefined in the main text.
(f) Figure 1 caption: 'the glued relaxation is exact' (it is exact only in the direction of D).
(g) 'Two ordinary steps of model loading ... We guard against both' is followed by three paragraphs; Bounds is not one of the two steps.
(h) 'we relax them to their bounds' is unclear.
(i) 'A separation routine for~\eqref{eq:joint-hull}' refers to an equation, not a set.
(j) w is used in the introduction (l.19-20) before it is defined (l.33).
(k) 'compact polytopes' (Cor. 6.5) is redundant.

**Fix.** (a) 'are defined only for $x>0$, $x\ne0$, $x\ge0$ and $x>0$, respectively.'
(b) 'The argument uses that every vertex other than the center is a leaf.'
(c) Add 'and $\hat g(x)=\max\{y:(x,y)\in K\}$'.
(d) Add 'Write points of $\R^n\times\R^m\times\R^p$ as $(u,y,\eta)$.'
(e) 'by Ben-Or's theorem applied to a family of instances with $3r$ leaves and $r$ rows whose decision set has $r!$ connected components'.
(f) '...the glued relaxation attains the true minimum $\delta^2/2$ in the direction of $D$.'
(g) Add 'The third paragraph describes the bounds that certificates use.'
(h) 'we drop their integrality and keep their bounds'.
(i) 'A separation routine for $H_D(F)$'.
(j) '..., where $w_j$ stands for $f_j(x)$,'.
(k) Drop 'compact'.

## [minor] 01-introduction.tex:8,106,117-123,71-72,96-97; 05b-star.tex:17; 09-computations.tex:295; 10-conclusions.tex:27,38

**Issue.** Filler and announcing phrases that the target style excludes:
- 'This is robust and general'
- 'and we report it as such'
- 'The certified cuts are therefore usable' (replay shows validity, not usefulness)
- 'whatever the cuts contribute, and our implementation's overhead outweighs the rest' (vague)
- 'made precise for certificates'
- 'needs ... no full-dimensionality'
- 'and for good reason:'
- 'The study has limitations that the reader should weigh.'
- 'Two reasons stand out.'
- 'at negligible cost' (unsupported)

**Fix.** - 01:8 -> 'This construction is general, but it relaxes expressions as if they were unrelated.'
- 01:106 -> 'The computational results are mostly negative.'
- 01:117-123 -> 'The cuts are therefore valid in practice. On instances with the structure of Section~\ref{sec:composition} they supply strength that SCIP's root relaxation lacks; on the benchmark models we tested, SCIP solves the models without them, and the separator's cost makes the solves slower.'
- 01:71-72 -> 'the method is classical face enumeration; we treat the degenerate cases that a certificate must cover.'
- 01:96-97 -> '...oracle calls and does not require the hull to be full-dimensional.'
- 05b:17 -> 'Rows or products that couple two leaves are excluded, because ...'
- 09:295 -> delete the sentence.
- 10:27 and 10:38 -> see the conclusion rewrite.

## [minor] sections/01-introduction.tex:50-67,75

**Issue.** Contribution bullets 1 and 2 are hard to parse. Bullet 1 is one 57-word sentence with four 'on ...' clauses. Bullet 2 nests two appositions ('..., the projection of the joint-graph relaxation, which is the set version of ...') and ends with the imprecise phrase 'the convex hull of the selected rows', which should be the convex hull of the set the rows define. Bullet 3 says 'optimal for algebraic computation trees' without the qualification m=Θ(k) that Section 5.3 (05b:85-86) requires.

**Fix.** Bullet 2: 'Minimizing a nonnegative combination of nonlinear rows over their common block domain and eliminating the rows gives linear cuts in the model variables, with no auxiliary variables. Together these cuts describe exactly the projection of the joint-graph relaxation, the set version of the primal characterization of the Lagrangian dual. We give conditions under which this projection is the convex hull of the set defined by the selected rows, and examples where it is not.'

Bullet 1: split after 'any numerical method.' and list the four checks as a short series.

Bullet 3: 'optimal up to a constant factor for algebraic computation trees when $m=\Theta(k)$'.

## [minor] sections/09-computations.tex:44,57-58,48,159-160; sections/03-certification.tex:209; sections/B-instances.tex:24

**Issue.** The campaign 1 description and Section 9.4 have small gaps:
- 'polygon and star oracles': no polygon oracle is defined in the paper.
- '0.57 s and 0.46 s for the two cut modes' does not name the modes.
- '13 constructed mechanism cases' are never described.
- Section 3.3 says 'the automatic mode' instead of \code{auto}.
- 'which were then solved at the root node' (09:159-160) could refer to the models or to the modes.

**Fix.** - 'the polytope oracle of Theorem~\ref{thm:polytope} in dimension two and the star oracle'.
- Name the modes: '0.57\,s (\code{all}) and 0.46\,s (\code{auto})', or the reverse, as recorded.
- Add one sentence or an appendix list for the mechanism cases.
- 03:209 -> 'mode \code{auto}'.
- 09:159-160 -> '...in modes \code{auto} and \code{all-diag}; in these modes both models were solved at the root node.'

**Evidence.** campaign-v1/results.md lists the modes as baseline, control, all and auto.

## [minor] main.tex:17-19; sections/07-separation.tex:202-204

**Issue.** Front matter a referee would expect is missing: authors and affiliations (\author{} is empty), keywords, MSC 2020 codes (required by Mathematical Programming and JOGO), and a code and data availability statement (required by IJOC). Section 7.4 cites 'the supplementary verification scripts' without saying where they are.

**Fix.** Add keywords (e.g. simultaneous convexification; support cuts; safe rounding; nonconvex quadratic programming; MINLP), MSC codes (90C26, 90C11, 90C20, 65G30), and a 'Code and data availability' paragraph that names the repository or archive containing the separator, the replay checker, the campaign records and the verification scripts.

## [minor] references.bib:134-141,356-363,558-565,712-715; sections/08-implementation.tex:3; sections/09-computations.tex:16

**Issue.** The arXiv entries use arxiv.org/html/...v1 URLs and eprint fields that plainnat does not print, so the references show an HTML URL instead of an arXiv identifier. The SCIP source used for the lp.c claim is cited as tag v10.0.0, while all runs used SCIP 10.0.2.

**Fix.** Cite the arXiv papers as 'arXiv:2609.35595' (and similarly for the others), via note or howpublished, with abs/ URLs. Cite tag v10.0.2, or add 'the behavior is unchanged in 10.0.2'.

## [suggestion] sections/03-certification.tex:165-211; sections/05-quadratic-support.tex:136-164; sections/02-background.tex:43-48; sections/A-proofs.tex (ordering)

**Issue.** Structure:
- Section 3.3 (Screening) introduces a theorem that the final implementation does not use and that nothing else references, and it reports campaign-1 numbers before the campaigns are introduced.
- Section 5.2 interrupts the two algorithms of Section 5 with a modeling point.
- The roadmap in Section 2 ('Three tasks remain...') omits Section 6.
- The appendix order (polytope, interleave, alternation, SDP, star, ellipsoid) does not follow the main-text order.

**Fix.** - Move Section 3.3 to an appendix, or cut it to one paragraph.
- Move Section 5.2 before 5.1, or into Section 4.
- Add Section 6 to the roadmap ('...and deciding when larger blocks are stronger than their pairs (Section~\ref{sec:composition})').
- Order the appendix as A.1 polytope, A.2 star, A.3 interleave, A.4 alternation, A.5 SDP, A.6 ellipsoid.

## [suggestion] 07-separation.tex:12; 05-quadratic-support.tex:159; 06-composition.tex:266; 09-computations.tex:60,250; 01-introduction.tex:90

**Issue.** The contrast pattern 'X, not Y' appears about a dozen times ('cost, not a missing case'; 'representation, not of strength'; 'the reformulation, not by the cuts'; 'in the direction search, not in the support computation'; 'a property of the analysis, not of the problem'). Each instance is defensible, but the frequency makes the prose formulaic.

**Fix.** Keep the pattern where the contrast is the claim (representation versus strength, once). Elsewhere state the positive fact, e.g. 07:11-12 -> 'and because it shows that what remains difficult in separation is its cost.'

# R7-editor

Handling-editor assessment.

Contribution and scope. The manuscript is honest and carefully attributed. Its new content, however, is narrow compared with its length. Three parts are genuinely new and worth publishing:
- The exact limits of composing pair hulls (Section 6): the 1/128 path witness, the interleaving theorem, the k-moment alternation criterion, and the SDP identity, which shows the advantage is one of representation.
- The exact O((m+k)log(m+k)) star algorithm with center-leaf rows and its matching lower bound (Theorem 5.4).
- An integrated certification and replay pipeline inside SCIP, with a careful negative computational study.

Most of the remaining theory restates classical results (support functions, Bernstein bounds, Lagrangian closure, safe rounding, face enumeration, oracle separation), as the authors themselves say. The theory and the computations are also poorly connected:
- The star oracle never certified a cut in the final implementation's campaigns; all quadratic cuts came from the polytope oracle.
- The only positive result, on the constructed path family, comes from a post hoc diagnostic.
- That result is measured against a SCIP root bound weakened by SCIP's own presolve. An exact pair relaxation would already close 82-96% of that gap, so the effect specific to Section 6 is the remaining delta^2/2 per copy.

Balance and length. About 20 of the 30 main-text pages are theory, 2 are implementation and 5 are computation. Roughly 8-10 pages can be removed or moved to appendices without losing anything new:
- the Bernstein, Arb and chord bounds;
- the screening certificate, which is unused by the final implementation;
- the complete-separation section, which the SCIP separator does not run;
- the proof of Theorem 5.1 and the hardness proposition;
- the superseded campaigns 1-2;
- repeated statements of the negative result.

Reordering so that the composition limits come right after the setting would lead with the strongest material and motivate the oracles.

Prior work. The attribution is fair and unusually careful. Missing are Locatelli-Schoen 2014 (supporting hyperplanes of envelopes over 2D polytopes), Bao-Sahinidis-Tawarmalani 2009 (multiterm relaxations) and Bhathena et al. 2025 (parametric DP on trees). Misener-Floudas 2012 (edge-concave relaxations) is cited only for grouping terms, and SCIP's own edge-concave separator should be named as the native counterpart.

Negative results. They are reported in full and honestly. They become useful only if the paper says what they mean:
- The records show SCIP's solving time unchanged once separator time is removed. The cuts are neutral, and the 15-40% slowdown is Python overhead, now dominated by certification.
- 20-36% of certified cuts in Part B were discarded by the stored-row check because presolve aggregated block variables. This is never reported.
- The baselines omit SCIP's disabled-by-default nonconvex separators and any other solver.

My checks also show that Gurobi 13 times out on the path family. That is favorable to the paper, which should report it.

What referees will most likely require, in priority order:
1. Shorten and refocus to about 22-24 pages with three contributions.
2. Redo the path-family analysis with a pair-hull reference, a relaxation-only SCIP comparator (checkvarlocks='d') and a second solver, and label the post hoc diagnostic in the abstract and introduction.
3. Fix the conclusions, which contradict Section 9 and call SCIP's root relaxation 'provably weak'.
4. Add the time decomposition and the certification funnel, and fix the loss of cuts to presolve aggregation.
5. Add comparators: SCIP's nondefault separators and BARON or Gurobi.
6. Add a root-strength study on harder structured instances (QPLIB, larger pooling models) or narrow the general negative claim.
7. Say that the star oracle was unused, or show where it matters.
8. Add the missing prior work.
9. Add a code and data availability statement.
10. Minor fixes: abstract scope and length, the Section 8.2 description, the Section 9.6 cross-reference and numbers, replay counts for the diagnostic, a per-model table for Part A, and typesetting.

Recommended but optional:
- A path-family variant with binding coupling.
- An uncertified ablation to measure what certification buys.

Journal fit. The best fit is the Journal of Global Optimization. Its scope covers convex relaxations, rigorous global MINLP and solver components, and it has published SCIP-internals work (Bestuzheva et al. 2025). Its readers can use all three parts of the paper, and it accepts long papers that mix theory and computation, including negative results.

The other venues fit less well as the paper stands:
- Mathematical Programming would need a theory-only paper with stronger new results, for example general directions on paths or trees, or the star algorithm extended to deeper trees.
- INFORMS Journal on Computing would need a much stronger computational contribution with public code; a Python prototype whose overhead dominates and whose cuts are neutral is unlikely to clear that bar.
- Mathematical Programming Computation would fit only if the certification and replay toolkit were released and reviewed as standalone software, with the paper reframed around it.

Recommendation: major revision, aimed at JOGO.

Verification scripts, all in /workspace/minlp-notes/paper-certified-support-cuts/verification/:
- R7-editor_mechanism.py: pair-hull closure fractions and per-copy root bounds.
- R7-editor_native_settings.py and R7-editor_native_full.py: SCIP nondefault settings, root runs and 100 s full runs.
- R7-editor_gurobi_family.py: Gurobi on the path family, 60 s.
- R7-editor_funnel_and_time.py: separator funnel, oracle usage and time decomposition from the archived records.

All SCIP and Gurobi checks ran single-threaded on three to four instances each. No project-wide tests were run and CI was not consulted.

## [major] sections/09-computations.tex lines 201-279 (Section 9.6), Table 2 (tab:mechanism), Table B.3 (tab:mechanism-detail); abstract lines 25-27; intro lines 112-116

**Issue.** The path-family study measures 'root gap closed' against a SCIP root bound that SCIP's own presolve weakens, and it does not separate the joint-versus-pair effect of Section 6 from the effect of having any exact low-dimensional relaxation. By Theorem 6.2(ii), exact pair hulls glued on (m_y,s_y) give value 0 for every interleaving copy, so the root bound is 0. The coupling row is nonbinding at that point because the chord intersections lie at most at 3/4. A bound of 0 already closes 82-96% of SCIP's default root gap on every instance; the median is 0.89-0.95 for each n. The gap that only the joint block closes, delta_i^2/2 per copy, is 4-18% of that root gap. Separately, turning off one presolve step (constraints/nonlinear/checkvarlocks='d', the implicit-discreteness step that turns x_i and z_i into binaries) brings SCIP's root bound to almost the pair-hull level. As it stands, Table 2 overstates what Section 6's mechanism contributes and understates native SCIP. The frozen separator (19-35%) closes less than an exact pair relaxation would.

**Fix.** (1) Add to Table 2 and Table B.3 a column with the analytic pair-hull bound (0) and the closure it implies. Add a native-SCIP root bound with constraints/nonlinear/checkvarlocks='d' as the relaxation-only comparator. Add a column for the closure of the residual gap: (root bound with cuts - 0)/(optimum - 0). (2) Add this sentence to Section 9.6: 'An exact pair relaxation glued on (m_y,s_y) has root bound 0 on every instance (Theorem 6.2(ii)) and would already close 82-96% of SCIP's default root gap; the part that only the joint block closes is sum_i delta_i^2/2.' (3) Report full runs of native SCIP with checkvarlocks='d', and of at least one other global solver (BARON or Gurobi), on the 20 instances. My checks suggest this strengthens the result for n>=40: the instances stay hard for both solvers.

**Evidence.** verification/R7-editor_mechanism.py (archived v3 Part C records plus the case files): the pair-hull closure fraction per instance ranges from 0.82 (n10 s4) to 0.96. The per-n medians are 0.95, 0.89, 0.93 and 0.92 for n = 10, 20, 40, 80. verification/R7-editor_native_settings.py, root runs, 1 thread. The default runs reproduce the archived baselines. n20 s0: default -0.580; checkvarlocks='d' -0.00236; intersection cuts -0.168; eccuts and RLT-hidden/interminor unchanged. n40 s0: -1.226 / -0.00517 / -0.323. n10 s4: -0.236 / -0.00110 / -0.093. verification/R7-editor_native_full.py (100 s, checkvarlocks='d'): n20 s0 solved in 39 s (the default baseline timed out at 300 s); n40 s0 and n80 s0 timed out. verification/R7-editor_gurobi_family.py (Gurobi 13.0.3, 1 thread, 60 s): n20, n40 and n80 s0 all timed out, with final bounds 0.0633, 0.0127 and -0.0374.

## [major] sections/00-abstract.tex lines 25-27; sections/01-introduction.tex lines 112-116

**Issue.** The only positive computational result (root gap closed, all 20 instances solved) comes from a post hoc diagnostic. That diagnostic was designed after the prospective Part C results were seen, and it changed the direction code and widened the limits. The abstract states this result without labeling it post hoc. The introduction mentions the frozen result only in a subordinate clause and never says 'post hoc'. Sections 9.6 and 9.7 label it correctly. Referees and readers judge a paper by its abstract, and presenting a post hoc result next to prospective ones without a label is a reporting-integrity issue.

**Fix.** Abstract, replace the last sentence with: 'On a constructed family with the path structure, the frozen separator closed 19-35% of SCIP's root gap (median), and both solved the same 9 of 20 instances within 300 seconds; in a post hoc diagnostic in which the direction search first tried each row's own direction, the cuts closed the root gap and solved all 20 instances.' Introduction lines 112-116, replace with: 'On a constructed family of path blocks, the frozen separator closed a median of 19-35% of SCIP's root gap and solved the same 9 of 20 instances as native SCIP within 300 seconds. In a post hoc diagnostic, designed after these results were seen, the direction search first tried each row's own direction; the cuts then closed the root gap on all 20 instances and solved all of them, mostly at the root node.'

**Evidence.** experiments/v3d/README-diagnostic.md: 'a diagnostic conceived after the Part C results of campaign v3 were seen'. The diagnostic changes RowSeparator._directions and adds the mode all-diag-mech-wide (4n cuts per callback, 16n cuts, 40n support calls). sections/09-computations.tex lines 259-261 and 306-309 label it post hoc; the abstract and introduction do not.

## [major] sections/10-conclusions.tex lines 25-34

**Issue.** The conclusions paragraph appears to predate campaign 3 and contradicts the paper's own results. (a) 'the cuts close part of the root gap and reduce the number of nodes' contradicts the abstract and Section 9.6, where the cuts close the whole gap and solve all 20 instances. (b) 'where SCIP's root relaxation is provably weak' is not proved anywhere: the paper proves weakness of the glued pair relaxation R, not of SCIP's relaxation. SCIP's weak root bound largely comes from a presolve step (see the first finding). (c) 'the frozen work limits allow few cuts' is contradicted by Section 9.4 lines 169-173: raising the limits (all-diag) improved the root bound beyond the gap tolerance on only one more model in each part. (d) 'discovery in Python costs more than the cuts return' contradicts Section 9.5 lines 195-197: in campaign 3, certification takes 23.0 of 32.9 callback seconds and discovery 4.4 s. (e) 'on the path example ... strong branching closes the gap at the root' refers to a pilot (experiments/pilot-native.md) that the paper never reports.

**Fix.** Replace lines 25-34 with: 'The computations temper these conclusions. On MINLPLib models the cuts were valid but did not change which models SCIP solved, and they left SCIP's own solving time essentially unchanged; the Python separator's overhead, now dominated by exact certification, made the runs slower. Raising the work limits improved the root bound beyond the gap tolerance on only one more model in each sample, so the limits are not the main reason. On the constructed path family, SCIP's default root bound is weak partly because its presolve turns the leaves into binaries; an exact pair relaxation would already close most of that gap, and the joint cuts close the remaining delta^2/2 per copy. With the direction search corrected post hoc, the cuts closed the root gap and solved all 20 instances.' Either report the single-instance pilot in Section 9.6, with the checkvarlocks control, or delete the 'path example' sentence.

**Evidence.** Compare 10-conclusions.tex lines 27-34 with 09-computations.tex lines 169-173, 193-199 and 263-266. verification/R7-editor_funnel_and_time.py and analyze_v3.py give, for Part B full in mode all: callback 32.9 s, certification 23.0 s, discovery 4.4 s, direction LPs 3.9 s.

## [major] Whole manuscript; contribution list sections/01-introduction.tex lines 49-104; Sections 3, 4, 5.1-5.2, 7, 9.2-9.3

**Issue.** The paper is too long for its new content, and the contribution is spread out. The main text runs 30 pages (11 pt, 1 in margins), plus 6 pages of references and 6 of appendix. About 20 pages are theory, and by the authors' own statements roughly 12 of them restate classical results 'in the form needed': Prop 2.1; Prop 3.1 ('elementary'); Lemma 3.2; Prop 3.3 ('immediate'); Lemma 3.4; Theorem 3.5 (Hölder; 2 of 506 skips; unused by the final implementation); Prop 4.1 (weak duality); Theorem 4.2 (Chen-Luedtke); Prop 4.8 (Neumaier-Shcherbina); Theorem 5.1 (Murty); Prop 5.2 (MAX CUT); and Section 7 ('we do not claim the principle as new'; not run by the SCIP separator). The introduction lists six contributions, three of them described as classical. The genuinely new material is Theorem 5.4 with its lower bound, Section 6, and the integrated certification pipeline. Superseded implementations (campaign 1, and campaign 2 with defective discovery) take about 1.5 pages of the main text, and the negative result is restated in the abstract, Section 1, Section 9.7 and Section 10. A referee for any of the target journals will ask for shortening and focus.

**Fix.** Target 21-24 pages of main text. (a) Reduce the introduction to three contributions: limits of pairwise composition (Section 6); exact quadratic support for constrained stars (Theorem 5.4); a certified original-variable separator with an honest computational evaluation. Mention the classical ingredients in one sentence. (b) Lead with the strongest new material: Setting and related work -> Limits of pair composition (current §6) -> Exact quadratic support (current §5, with the proof of Thm 5.1, its degenerate cases and Prop 5.2 moved to an appendix) -> Cuts in the original variables (current §4, condensed; keep Thm 4.2 short with its citations, the x^2 = 1/4 example and one sentence on free remainders) -> Certified export and replay (merge §3.1, §4.4 and §8.3) -> Implementation -> Computations -> Conclusions. (c) Move to appendices: Bernstein, Arb and chord bounds (§3.2, keep one paragraph); complete separation (§7, keep one paragraph saying the separator never treats a failed search as membership); Corollary 6.5 as a remark. Delete screening (§3.3), or move it to an appendix with the 2/506 statistic. (d) Make campaign 3 the main study and summarize campaigns 1-2 in one paragraph plus an appendix. (e) State the negative result once in full (Section 9) and briefly elsewhere.

**Evidence.** Page map from pdftotext: §1 pp. 1-3, §2 pp. 3-5, §3 pp. 5-8, §4 pp. 8-11, §5 pp. 11-15, §6 pp. 15-20, §7 pp. 20-23, §8 pp. 23-25, §9 pp. 25-30, §10 p. 30, references pp. 31-36, appendices pp. 37-42. The self-descriptions as classical are at 03-certification.tex lines 30-37, 108, 132-134 and 195-198; 04-original-variables.tex lines 12-14, 47 and 80-88; 05-quadratic-support.tex lines 99-102; 07-separation.tex lines 9-13. The literature lanes (evidence/literature-L1.md §1, L4 §1, L5 novelty table) reach the same conclusions.

## [major] sections/09-computations.tex Table 1 (lines 118-137), lines 145-150, 166-169, 286-293; sections/00-abstract.tex line 24

**Issue.** The text attributes the slowdown to the cuts ('made the solves slower'). The records show that SCIP's own time is unchanged once the separator callback time is removed. The cuts are therefore neutral, and the whole 15-40% slowdown is the Python separator's overhead. This is the most useful form of the negative result: it shows that a compiled implementation would at best break even on these models. The paper does not report it.

**Fix.** Add to Table 1 a column 'SGM time excluding separator callback' and the total node counts. Rephrase the abstract: 'the cuts did not change which models SCIP solved and left SCIP's own solving time unchanged; the separator's overhead made the runs 15-40% slower.' Rephrase Section 9.7 in the same way.

**Evidence.** verification/R7-editor_funnel_and_time.py, over runs solved by every mode. Part A full (80 runs): SGM total 1.052 / 1.265 / 1.212 (baseline / all / auto); total minus callback 1.052 / 1.055 / 1.055; node sums 695,712 / 695,959 / 694,230. Part B full (52 runs): SGM total 1.330 / 1.870 / 1.818; minus callback 1.330 / 1.311 / 1.288; node sums 771,221 / 791,603 / 762,375.

## [major] sections/08-implementation.tex lines 114-121 (Section 8.3); Section 9 (no counts reported)

**Issue.** The paper never reports what the certification pipeline accepted or rejected, although certification is its first claimed contribution. In the records, the stored-row check discards a large share of certified cuts, mostly because SCIP's presolve aggregated or substituted block variables. The implementation does not mark them do-not-aggregate (evidence/implementation-facts.md, row 83). This bears directly on the null result: certified cuts on up to 17 of the 30 Part B models never reach the LP. Rounding corrections never rejected a cut.

**Fix.** Add a funnel table per part and mode: certification calls; failed certifications by outcome (incomplete, unsupported); row-binding rejections by cause (presolve aggregation, coefficient change by SCIP, other); rounding rejections; cuts added. Then either mark block variables as not (multi-)aggregatable, or add the cuts in the original space before presolve. Rerun the affected root experiments (at least Part B, all-diag) so that the strength measurement is not reduced by the integration.

**Evidence.** verification/R7-editor_funnel_and_time.py: Part B full, all: 179 cuts added, 45 row-binding rejections (10 models), 14 certification failures. Part B root, all-diag: 358 added, 202 rejected (17 of 30 models). Part A root, all-diag: 403 added, 41 rejected. Part A full, all: 151 added, 15 rejected, 57 certification failures. Part C: 3000 added, 71 rejected per phase (13 instances). row_rounding_rejections = 0 everywhere.

## [major] sections/02b-related.tex lines 88-97 (Native SCIP); Section 9 (baselines); Section 9.7 lines 303-305

**Issue.** The only baseline is default SCIP. The paper itself notes that SCIP has nonconvex cut families that are disabled by default. In SCIP 10.0 these include edge-concave cuts on aggregated quadratic terms (separating/eccuts/freq = -1, maxaggrsize 4), intersection cuts (nlhdlr/quadratic/useintersectioncuts = False), interminor cuts (-1) and hidden-product RLT (separating/rlt/detecthidden = False). These target the same joint quadratic structure and are the natural comparators for a new separator of that kind. No second global solver is run. On the path family, intersection cuts already raise SCIP's root bound substantially. Gurobi also fails on the family, which would strengthen the paper's claim that the family is genuinely hard.

**Fix.** In Part B and Part C, add runs of SCIP with these separators enabled, one by one or together, and one other global solver (BARON or Gurobi with NonConvex = 2). Report root bounds and solved counts. In Section 2.1, name these separators explicitly as the native counterparts of joint block cuts.

**Evidence.** SCIP 10.0 default parameters queried through PySCIPOpt: separating/eccuts/freq -1, separating/interminor/freq -1, nlhdlr/quadratic/useintersectioncuts False, separating/rlt/detecthidden False. verification/R7-editor_native_settings.py: intersection cuts raise the root bound from -0.580 to -0.168 (n20 s0), -1.226 to -0.323 (n40 s0) and -0.236 to -0.093 (n10 s4); eccuts change nothing. verification/R7-editor_gurobi_family.py: Gurobi 13.0.3, 1 thread, 60 s, times out on n20, n40 and n80 s0.

## [major] sections/09-computations.tex lines 295-300 (limitations); Appendix B selection paragraph

**Issue.** The benchmark design cannot show usefulness. The models have at most 120 variables, and on the structure-selected sample SCIP solves the 26 solvable models 'in about a second regardless' (line 167), so the solved count and the time can only get worse. The strength question (do the cuts tighten the root relaxation where it matters?) does not depend on fast code. It could be tested on harder structured instances, such as larger pooling instances or QPLIB QCQPs with star or row-domain blocks, by root-only runs with raised limits. Referees will ask for this before accepting the general negative conclusion 'SCIP's own machinery already obtains whatever the cuts contribute' (intro lines 120-123).

**Fix.** Add a root-strength experiment on a structure-selected sample of harder instances (QPLIB, Furini et al. 2018 MPC; larger pooling models) without the size cap, with all-diag limits. Report the root gap closed relative to SCIP and to SCIP with its nondefault separators. Otherwise, narrow the general conclusion to 'on small MINLPLib models that SCIP solves in seconds'.

**Evidence.** Table B.2: 26 of 30 Part B models are solved by the baseline in at most 191 s, most in under 2 s. 09-computations.tex lines 166-169 and 295-298.

## [major] sections/05b-star.tex lines 129-136; sections/08-implementation.tex lines 90-95; intro lines 68-78

**Issue.** Theorem 5.4 is presented as a main contribution and as part of the implementation's oracle chain. Yet no cut in the experiments of the final implementation (campaigns 2 and 3) was certified by the star oracle: every quadratic cut came from the polytope enumeration of Theorem 5.1. Only campaign 1 (the superseded lifted implementation) used the star oracle. The paper says only that the simpler O((m+k)^3) implementation is 'adequate for the blocks of Section 9, where k<=4'. Readers will assume the star result mattered computationally.

**Fix.** State explicitly in Sections 8.2 and 9: 'In campaigns 2 and 3 every quadratic cut was certified by the polytope oracle of Theorem 5.1; the star oracle was not needed because all blocks had at most four variables.' Then either add an experiment in which stars with many leaves and center-leaf rows occur (e.g., pooling models with many outputs, run with a larger block cap), or present Theorem 5.4 as a theoretical result and keep it out of the claimed implementation contribution.

**Evidence.** verification/R7-editor_funnel_and_time.py, support methods of recorded cuts: v3 Part A full {quadratic_polytope 149, bernstein 3, arb 36}; Part A root {409, 3, 53}; Part B {quadratic_polytope 845}; Part C {quadratic_polytope 6000}. The same count over research-20261003-convexification/experiments/campaign-v2/records.jsonl gives {quadratic_polytope 182, bernstein 4, arb 60}, and repair-discovery-v1 gives {68, arb 16}. Campaign 1 records contain quadratic_star 250 times.

## [major] sections/02b-related.tex lines 3-25 and 41-56; references.bib

**Issue.** Attribution is generally careful, but four directly relevant lines of prior work are missing or understated. (1) Locatelli and Schoen (2014, Math. Program. 144) compute the convex envelope value and a supporting hyperplane of a bivariate function over a general two-dimensional polytope; this is the closest precedent for exact support oracles on low-dimensional polytopes. (2) Bao, Sahinidis and Tawarmalani (2009, OMS 24) give multiterm polyhedral relaxations of several bilinear and quadratic terms relaxed jointly. (3) Misener and Floudas (2012) is cited only for 'grouping quadratic terms', although its edge-concave relaxations of small quadratic blocks are joint relaxations, and SCIP's edge-concave separator implements this kind of cut. (4) Bhathena, Fattahi, Gómez and Küçükyavuz (2025, Math. Program.) solve tree-structured quadratic problems by a parametric dynamic program that conditions on the parent. This is relevant to Theorem 5.4 and to the open question of Remark 5.5. QPLIB (Furini et al. 2018) is not mentioned as a test set.

**Fix.** Add to the paragraph 'Exact low-dimensional and structured quadratic hulls': 'Convex envelopes and supporting hyperplanes of bivariate functions over general polygons are computed by Locatelli and Schoen (2014). Several bilinear terms are relaxed jointly by the multiterm relaxations of Bao, Sahinidis and Tawarmalani (2009) and by the edge-concave relaxations of Misener and Floudas (2012); SCIP contains an edge-concave cut separator that is disabled by default. Parametric dynamic programs over trees that condition on a parent variable, as our star algorithm does, are used by Bhathena et al. (2025) for convex quadratic problems with indicators.' Cite QPLIB in Section 9 if it is used.

**Evidence.** grep over references.bib finds no Locatelli, Schoen, Bao 2009, Bhathena or QPLIB entry. The local knowledge base has locatelli2014-on-convex-envelopes-for-bivariate (abstract: 'compute the value at some point of the convex envelope over a general two-dimensional polytope, together with a supporting hyperplane'), bao2009-multiterm-polyhedral-relaxations-for-nonconvex, bhathena2025-a-parametric-approach-for-solving and furini2018-qplib. MisenerFloudas2012 is cited only at 02b-related.tex line 21.

## [major] main.tex (no declarations); sections/07-separation.tex lines 201-205

**Issue.** There is no statement on code and data availability, although replayable certificates are a main selling point. Section 7.4 refers to 'supplementary verification scripts' without saying where they are. Springer journals (JOGO, MP, MPC) require a data-availability statement; INFORMS JoC requires a public repository; MPC requires the code for review.

**Fix.** Add a 'Code and data availability' section. Give an archival location (e.g., a Zenodo DOI) for the separator, the replay checker, the frozen snapshots with their SHA-256 manifests, the run records, the replay outputs and the verification scripts. Name the exact SCIP, PySCIPOpt and python-flint versions, and state what replay needs in order to run.

**Evidence.** grep -i for 'availab', 'repositor', 'supplement', 'github' and 'zenodo' in sections/*.tex finds only the phrase in 07-separation.tex line 204.

## [minor] sections/00-abstract.tex lines 16-21 and overall length

**Issue.** (a) 'on a path of three variables the gap is either zero or delta^2/2, depending only on whether two point sets interleave' reads as a general statement about paths. Theorem 6.2 is about the specific family (eq. family) of directions D_A + D_C; for other directions the gap can take other values (Corollary 6.5 gives only [0, Delta]). (b) The sentence on complete separation advertises a result the paper calls classical. (c) The abstract has about 290 words; JOGO and Math Programming ask for 150-250.

**Fix.** Replace lines 16-21 with: 'We show that exact pair hulls glued on shared moments do not compose: for a family of quadratic directions on a path of three variables, the gap between the glued pair hulls and the joint hull is either zero or delta^2/2, depending only on whether two point sets interleave, and an interface that shares k moments misses the gap exactly when the local zero sets alternate at least k+1 times.' Delete the separation sentence and trim to at most 250 words.

**Evidence.** 06-composition.tex lines 72-96 (statement of Theorem 6.2 for the family) and lines 309-318 (gap to R lies in [0, Delta]).

## [minor] sections/08-implementation.tex lines 84-85

**Issue.** 'the separator first tries, for each block, the support of each single source side' does not describe the code used in all campaigns. The frozen code uses a = 0 and lambda = e_j, so it bounds only the nonlinear remainder of the side; this is exactly the defect diagnosed in Section 9.6.

**Fix.** Replace with: 'At an LP solution the separator first tries, for each block and each source side j, the direction a = 0, lambda = e_j, which bounds the nonlinear remainder of side j over D; the side's affine terms in the block variables enter only through the elimination (Section 9.6 discusses the consequence).'

**Evidence.** research-20261003-convexification/solver/integration.py, RowSeparator._directions (lines 399-420): direction = [0.]*(d+len(sides)); direction[d+j] = 1. experiments/v3d/README-diagnostic.md item 1.

## [minor] sections/09-computations.tex lines 239-242

**Issue.** (a) The cross-reference '(Section~\ref{sec:path-example})' for 'its presolve turns [the leaves] into binaries' is wrong: Section 6.1 says nothing about SCIP. (b) 'between -0.031 and -0.022 per copy on average' matches neither the per-instance range nor the per-n means.

**Fix.** Replace with: 'SCIP's root bound on these instances is weak: per copy it lies between -0.035 and -0.013 (median per n between -0.031 and -0.023), while each copy contributes at least 1/8192 to the optimum. SCIP's implicit-discreteness presolve turns the leaves x_i and z_i into binaries \citep[Section~4.2.7]{SCIP8report} (Section~\ref{sec:related}), and SCIP then closes the gap by branching.'

**Evidence.** verification/R7-editor_mechanism.py: the per-copy baseline root bound ranges over [-0.0354, -0.0131]; per-n medians are -0.0252, -0.0290, -0.0306 and -0.0227; per-n means are -0.0273, -0.0250, -0.0290 and -0.0249.

## [minor] sections/09-computations.tex lines 175-179; sections/00-abstract.tex line 23; Section 9.7 lines 283-285

**Issue.** The replay counts cover only the prospective parts (7,498 cuts). The post hoc diagnostic, which supplies the headline positive result, produced 30,998 more cuts, and their replay is not reported. That replay was still running when the PDF was built (main.pdf 11:48; v3d/runs/partC-rowdir/replay.json written at 12:00). It has since passed.

**Fix.** Add: 'Replay also passed for all 30,998 cuts of the post hoc diagnostic (30,000 on the path family, 469 and 529 in the root runs of Parts A and B), and all 14 corrupted records were rejected in each part.'

**Evidence.** experiments/v3d/runs/replay-partC-rowdir.log: {"passed": true, "cuts": 30000, "replayed_cuts": 30000, ...}, tamper rejections 14/14. replay-partA-root-rowdir.log: 469/469. replay-partB-root-rowdir.log: 529/529.

## [minor] sections/B-instances.tex line 46 and sections/B-tables.tex

**Issue.** Part B has a per-model table (Table B.2), but Part A, the 30 campaign-2 models over 3 seeds, has only a list of names. Readers cannot see which 11 models received cuts or where the 2 better and 4 worse bounds occurred.

**Fix.** Add a Part A per-model table like Table B.2 (root bounds for baseline and all-diag; status, time and cuts for seed 0), or put it in an online supplement.

**Evidence.** sections/B-instances.tex line 46 lists only model names; 09-computations.tex lines 144-148 report aggregate counts.

## [minor] main.tex; sections/06-composition.tex lines 51-63; sections/07-separation.tex lines 142-148

**Issue.** Administrative and typesetting issues. The author block is empty, and the funding, competing-interest and data declarations required by Springer and INFORMS are missing. main.log reports four overfull hboxes (12.9 pt and 35.8 pt in the proof of Prop 6.1, 9.0 pt in Lemma 7.3, and 19.9 pt in a later part).

**Fix.** Add the declarations required by the target journal. Break the long inline moment vectors in the proof of Prop 6.1 into a display, and rewrap Lemma 7.3.

**Evidence.** main.log lines 959, 969, 981, 996.

## [suggestion] sections/09-computations.tex lines 203-215 (family design) and 272-279

**Issue.** The constructed family is fully separable: the objective is a sum of block functions and the coupling row is nonbinding by construction, so the n cuts t_i >= min D_i give the optimum directly. This is the most favorable case, as the paper says, and it shows little about whether joint cuts help when block minima are not the answer.

**Fix.** Add a variant with a binding or linking coupling (for example sum_i y_i <= c with c below the sum of the optimal y_i, or rows linking y_i across copies) and report root gap closure and solves. This would test whether joint support cuts in non-row directions, found by the LP search, add strength.

**Evidence.** experiments/mechanism-protocol.md: 'The coupling row is not binding because every optimal y_i is a midpoint of two values at most 3/4'; 09-computations.tex lines 251-254.

## [suggestion] Section 9 (certification value)

**Issue.** The value of the certification contract is argued but never measured. No run shows a proposed cut that would have been invalid, or a row that SCIP changed (e.g., the integer-snapping in rowAddCoef cited at 03-certification.tex lines 45-48). Rounding rejections are zero in all campaigns.

**Fix.** Add a small ablation. Use a floating-point-only variant (numerical support from the sample LP or a local solver, no certificate) and count how many exported cuts are invalid by exact check, and how many stored rows differ from the submitted rows and why. This would turn the certification from a design choice into a measured safeguard.

**Evidence.** row_rounding_rejections = 0 in every v3 part and mode (verification/R7-editor_funnel_and_time.py). The row-binding rejections are mostly caused by presolve aggregation (evidence/implementation-facts.md row 83), not by unsafe coefficients.

