# Independent final review 5

Reviewed the complete standalone manuscript: `main.tex`, `macros.tex`, Sections 01–08, bibliography, figure scripts, build instructions, and submission archive. I read all eight source theorem notes under `notes/workbench/active/`, the allowed source map and literature record, and relevant primary-source passages. I did not read other peer reports, author/assessment/validation audits, or workflow outcomes. No manuscript or supplied artifact was modified.

**Findings: 0 major, 1 minor.** I found no mathematical error or missing hypothesis that invalidates a stated theorem. One close literature antecedent should be acknowledged before submission.

## Minor finding

**M1 — Add the Chebyshev-tangent/nonnegative-interpolation antecedent.** Locations: Section 1.2, paragraph beginning “Constrained polynomial approximation”; Section 4.1, Theorem 4.2 (`thm:thresholds`), admissibility of the extremizer; `bibliography.bib`.

Fawzi, Saunderson, and Parrilo, *Equivariant semidefinite lifts of regular polygons*, [arXiv:1409.4379](https://arxiv.org/pdf/1409.4379), Proposition 7 (PDF p.13) and Appendix A Lemma 1 (PDF p.26), give a close geometric antecedent. Proposition 7 constructs globally nonnegative polynomials agreeing with a linear target at finitely many nodes when a polynomial lies above its tangent. Lemma 1 proves that an even Chebyshev polynomial lies above its tangent globally when the tangency point is sufficiently far to the right.

The connection is exact at the level of the positivity construction. Write (n=2r), (x=(y-m_\rho)/h_\rho), and let (z_*) be the manuscript’s exterior stationary point. Its equations imply

\[
P_r^*(y)=G_r\{T_n(x)-T_n(-z_*)-T_n'(-z_*)(x+z_*)\}.
\]

Thus the proposed globally nonnegative extremizer is a positive multiple of a Chebyshev polynomial minus an exterior tangent; reflection of their even-polynomial lemma proves its nonnegativity. This is closer than the generic positive-approximation references currently discussed. It does **not** establish the present continuum minimax formula, threshold asymptotics, or quantum query staircase, and the existing self-contained proof is correct.

**Fix:** add this reference and one concise sentence distinguishing their finite-node interpolation/tangent construction from the present continuum minimax and query results. Optionally identify the tangent representation after Theorem 4.2. No weakening of the precisely scoped final novelty claim or change to the proofs is required.

## Mathematical verification

- **Sections 1–3:** The summary matches the theorem contracts. I checked the arbitrary-completion Hermitianization and walk reduction, centered Laurent polynomial implementation, scalar trigonometric degree induction, two-point polynomial range and error factorization, exact-impossibility continuation, and both pairwise constants and the formal normalization-slack derivative. The impossible exact tradeoff is not presented as achievable.
- **Section 4:** I checked the exterior Chebyshev bound, global positivity over all four real-axis regions, stationary-point uniqueness, strict threshold decrease, the quadratic formula, and the large-order asymptotic including integer rounding. The Taylor compactness argument obtains global nonnegativity only in the limit. The pinned gate is indeed an even algebraic polynomial, and its contact multiplicity and signed-error estimates establish error at most exactly (G_r\delta). The separate coarse constructions correctly distinguish (c<1) from (c=1).
- **Parity:** The even limit remains even and nonnegative; the same contact construction is applicable to an attained even minimizer. Convexity in (v=y^2) proves (F_1=F_2), while the degree-six witness gives the required strict inequality without claiming an exact value for (F_3). The odd lower proof’s Taylor/exterior argument supplies the logarithm; its upper construction remains globally bounded, including inside the small transition interval. The comparison is properly limited to one definite-parity transform.
- **Section 5:** The exact sine target avoids an uncontrolled (O(\delta^2)) error in the high-precision lower proof. Maximal index selection controls the sine remainder uniformly for arbitrarily large (\log(1/K)). The independent Fejér–Riesz argument uses a valid globally nonnegative squared Taylor polynomial, with the adaptive-radius and fixed-radius branches covering their claimed ranges. I recomputed the growing-index gate degree, leakage/slack ratio, explicit exponential tail factors, all three contractivity regions, and both high-band error powers. The intermediate comparison retains its required margin and does not claim a uniform multiplicative optimum.
- **Section 6:** I checked orthogonality, exact centrality, the bounded nontrivial feasible segment, predictor elimination, and the public primal direction. The full oracle completions are unitary. Endpoint hybrid distances count right-side access correctly; amplitude estimation gives the stated state orders and unconditional trace error. Compiler lower bounds properly omit the right-side oracle; the public-projector zero-query coarse exception and exact two-query factor construction are consistent. Digital access and whole-LP scope limitations are explicit.
- **Sections 7–8 and integration:** The conclusion preserves the precision-regime and access-model caveats. All eight source notes are represented or strengthened; their problematic coarse-band, rounding, pairwise-error, and growing-index constants are corrected. The exposition is readable and self-contained with the stated standard external ingredients.

## Source and reproduction checks

I checked QSVT Corollary 18, Lemma 25 and Theorem 30; GQSP’s completion/construction discussion; amplitude-estimation Theorem 12; Orsucci–Dunjko Section 4.3; and the recent constrained-minimax introduction. Primary arXiv records were also checked for GQSP, Dong et al., and Somma–de Wolf. The literature comparison does not transfer an unrelated output-task lower bound. Originality remains qualified: this is a targeted search, not an exhaustive historical priority certification.

I independently extracted `submission-source.zip` into `/tmp/shift-review5-jy5gomwp`. All 18 packaged files matched the corresponding supplied source bytes. `conda run -n qipm --live-stream make` generated a 31-page PDF with no unresolved-reference/citation or box warnings. Both figure scripts ran successfully through `make figures` in that isolated extraction. Their numerical thresholds, witness bound, and pinned-contact diagnostics agree with the manuscript; these computations are appropriately presented as illustrations rather than continuous-domain proof certificates.
