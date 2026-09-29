# Literature and significance review: large exact penalties for convex MIQCQP

Review date: 2026-09-25. This is an independent literature and scope review of the proposed one-binary construction and its symmetric two-binary companion. The main proof belongs in the research note; the calculations below identify the precise comparison and important qualifications.

The candidate appears to answer a specific open extension stated by Lefebvre and Schmidt: ordinary polynomial binary encoding length of exact norm penalties does not extend from MIQP to all quadratically constrained problems. The repeated-squaring precision mechanism itself is established prior art. The defensible contribution is its conversion into a sharp lower bound that survives optimization over every Lagrange multiplier, already for a compact convex MIQCQP with one binary variable, one dualized linear equality, and fixed rational coefficients. This is a potentially useful short theoretical result, rather than evidence of a new general precision phenomenon or a new solver method.

**Exact statement being compared.** Let

\[
 C_n=\{a\in[0,1]^n:a_1\ge1/4,\ a_{i+1}\ge a_i^2\ (i<n)\},
 \qquad \delta_n=2^{-2^n}.
\]

Its minimum last coordinate is exactly \(\delta_n\). With \(q\in\{0,1\}\), \(y\in[-1,1]\), retain the single linear constraint

\[
 y\ge a_n-2(1-q).
\]

Minimize \(-q\) and dualize only \(y=0\). The primal value is zero. Projection of the native set onto \((q,y)\) is exactly

\[
 (\{0\}\times[-1,1])\ \cup\ (\{1\}\times[\delta_n,1]).
\]

The exact identity established in the accompanying research note is

\[
 \sup_{\lambda\in\mathbb R}\inf_{(a,q,y)\in\widehat X_n}
 [-q+\lambda y+\rho|y|]
 =\min\left\{0,\frac{2\rho\delta_n-1}{1+\delta_n}\right\}.
\]

The two witness points \((q,y)=(0,-1)\) and \((1,\delta_n)\) bound the optimized multiplier and force \(\rho\ge1/(2\delta_n)=2^{2^n-1}\) for zero gap. The research note verifies attainment of the displayed bound. Equality of optimal values occurs at the threshold; equality of the entire primal and penalized optimal sets is available for a strictly larger penalty and an appropriate fixed multiplier. At the threshold, infeasible points tie with the primal optimum. Even a fixed additive gap such as \(1/2\) requires a penalty of the same asymptotic encoding size.

The symmetric companion adds one binary and has opposite objective-improving residuals \(\pm\delta_n\). Its optimized dual is \(\min\{0,-1+\rho\delta_n\}\), with threshold \(\delta_n^{-1}\). It is useful for explaining the multiplier cancellation but is no longer the strongest variable-count result.

The one-binary instance has sparse ordinary encoding length \(O(n\log n)\); every rational \(\rho\ge2^{2^n-1}\) requires at least \(2^n\) numerator bits. State this as failure of a polynomial encoding-size guarantee, with the chosen sparse/dense input convention specified. Do not automatically describe it as an exponential lower bound in the full input length: variable indices and dense zero coefficients affect that relation.

**Strongest directly relevant positive results and open question.**

| Inspected primary source | Assumptions and result relevant here | Precise comparison |
| --- | --- | --- |
| Gu, Ahmed, Dey, *Exact Augmented Lagrangian Duality for Mixed Integer Quadratic Programming*, SIAM J. Optim. 30 (2020), 781–797; [open preprint](https://arxiv.org/pdf/1907.00920), Definition 8 and Theorem 11 | Rational positive semidefinite quadratic objective, rational **linear** native constraints, feasible bounded optimum. Definition 8 uses standard binary encoding. Theorem 11 gives an exact norm penalty of polynomial encoding size, both for the optimized dual and for any fixed multiplier with that multiplier included in the size bound. | The candidate changes the native constraints from linear to convex quadratic. It keeps a linear objective, fixed integer dimension, compactness, and rational data. Thus it directly prevents extending this polynomial-size statement to all convex MIQCQPs. |
| Bhardwaj, Narayanan, Pathapati, *Exact Augmented Lagrangian Duality for Mixed Integer Convex Optimization*, SIAM J. Optim. 34 (2024), 1622–1645; [open preprint](https://arxiv.org/pdf/2209.13326), Theorem 3.3 and Remark 3.4 | Convex objectives over mixed-integer points of a rational polyhedron. Exactness under bounded integer variables or specified recession assumptions; further quantitative bounds for smooth strongly convex objectives. | Despite “mixed integer convex” in its title, the inspected theorem retains linear constraints. Its matrix inverse and polyhedral certificate bounds do not cover the squaring chain. |
| Lefebvre, Schmidt, *Exact Augmented Lagrangian Duality for Nonconvex Mixed-Integer Nonlinear Optimization*, [December 15, 2025 preprint](https://optimization-online.org/wp-content/uploads/2024/07/exact-penalty-for-minlp-1.pdf), Assumption 5, Theorem 14, conclusion p.24 | Compact native set; convex fixed-integer subproblems; each equality-feasible fixed-integer slice satisfies a Slater condition for nonlinear inequalities. Theorem 14 gives a finite exact penalty for every fixed multiplier. The conclusion expressly asks whether polynomial penalty encoding size extends to quadratically constrained quadratic problems. | The candidate satisfies the stated Slater condition and has finite exact penalties. It supplies a negative instance for the unrestricted polynomial-size extension raised in the conclusion. The relevant source version and its mixed-integer context must be stated, because the conclusion abbreviates the class name. |

No claim that Gu et al. bound the numerical magnitude of \(\rho\) by a polynomial is justified: their claim concerns encoding length. Likewise the candidate does not contradict existence of finite exact penalties.

The exact source language in Lefebvre–Schmidt's conclusion includes “existence of an exact penalty representation with a penalty parameter of polynomial size is limited to MIQPs” and names “quadratically constrained quadratic problems” as the proposed extension. These fragments should be read in the paper's mixed-integer setting and against its explicit definition of the optimized augmented dual.

**The precision mechanism is old.** In [Bienstock, Del Pia, Hildebrand, *Complexity, Exactness, and Rationality in Polynomial Optimization*](https://arxiv.org/pdf/2011.08347), inspected version v5 dated April 14, 2022, Section 6 gives two particularly close examples. Example 6.1 is the convex chain \(y_1\ge2, y_{i+1}\ge y_i^2\), whose last coordinate is doubly exponentially large. Example 6.2 uses a bounded squaring chain in a nonconvex QCQP to obtain constant superoptimality at doubly exponentially small additive constraint violation. The authors attribute the earlier large-coordinate chain to Ramana and Khachiyan, with further references to Alizadeh and Letchford–Parkes. Therefore neither repeated squaring nor bounded quadratic precision pathologies should be claimed as new. The displayed index convention in Example 6.2 should be checked before reproducing its precise exponent; the qualitative comparison does not depend on it.

[Beck, Bienstock, Schmidt, Thürauf, *On a Computationally Ill-Behaved Bilevel Problem with a Continuous and Nonconvex Lower Level*](https://optimization-online.org/wp-content/uploads/2022/02/nearly-feasible-bilevel-preprint.pdf), inspected May 3, 2023 preprint, provides an even closer regularity comparison. Section 2 uses the compact convex set \(y_1+y_n=1/2\), \(y_i^2\le y_{i+1}\). Result 4 exploits doubly exponentially small infeasibility to change the bilevel outcome drastically. Their lower-level feasible set satisfies Slater, and their exact problem has additional regularity and uniqueness properties. They explicitly credit Bienstock–Del Pia–Hildebrand for the chain. Their statement concerns approximate bilevel feasibility rather than the optimized sharp augmented-Lagrangian dual.

An independent subreview also inspected [Pataki and Touzov, *How do exponential size solutions arise in semidefinite programming?*](https://optimization-online.org/wp-content/uploads/2021/02/8263.pdf). It treats a much broader structural explanation of large solutions in strictly feasible SDPs, relates growth to dual singularity degree, and discusses compact symbolic representations. That paper reinforces both the classical status of the mechanism and the need to identify the encoding model. Its relevant statements were reported by the subreview; the author of this review directly inspected the two preceding primary papers. Original Ramana/Alizadeh examples were not independently rederived from their original publications here.

**Why the signs and quantifiers matter.** A one-sided tiny residual does not by itself force a large penalty in an augmented dual. An objective improvement of one at residual \(\delta>0\) only imposes \((\rho+\lambda)\delta\ge1\), which can be met with \(\rho=0\) by increasing \(\lambda\). In the one-binary construction, however, the native point \((q,y)=(0,-1)\) additionally forces \(\rho-\lambda\ge0\) whenever the relaxation value is zero. Together these inequalities imply \(2\rho\delta\ge1\). The residuals of the two witness points straddle zero, even though only one point improves the original objective. The symmetric companion gives an especially transparent cancellation through two opposite objective-improving residuals.

This is the essential addition to the classical chain. It distinguishes a lower bound on the supremum over multipliers from a lower bound only at a selected multiplier. The exact dual formula handles both attainment and supremum issues directly.

The lower bound does not arise from large equality multipliers of the feasible fixed-binary convex problems. On the feasible slice \(q=0\), the objective is constant and the zero multiplier is sufficient. The point \(a_i=3/8\), \(y=0\) satisfies all native inequalities strictly and the dualized equality. For the native slice \(q=1\), take \(a_i=3/8\), \(y=1/2\). In the displayed normalization, all native inequality slacks at both points are at least \(1/8\), independent of \(n\). The obstruction is the doubly exponentially small residual of an objective-improving integer assignment whose equality-constrained slice is empty. Bounding optimal multipliers on feasible slices alone cannot rule it out.

**Other formulations examined.**

- [Dolgopolik, *Augmented Lagrangian Functions for Cone Constrained Optimization: the Existence of Global Saddle Points and Exact Penalty Property*](https://arxiv.org/pdf/1707.05747), J. Global Optim. 71 (2018), 237–296, develops existence and localization results for global saddle points and exact augmented Lagrangians. The inspected definitions and results concern existence and local/global optimality conditions, not a polynomial rational encoding-size guarantee for the candidate mixed-integer family. This is relevant conceptual background, not an equivalent lower bound established by the parts examined.
- [Subramanyam, El Tonbari, Kim, *Data-driven two-stage conic optimization with zero-one uncertainties*](https://arxiv.org/pdf/2001.04934), inspected Theorems 3–4 and Appendix G, gives an exact penalty reformulation under complete/sufficiently expensive recourse and fixed recourse, using \(\|z-\xi\|_1\) for a fixed binary vector \(\xi\). Its threshold is related to conic multipliers; no ordinary encoding-size bound was established in the inspected result. Its complete-recourse framework differs from the candidate's infeasible integer slices.
- [Buchheim, *Bilevel linear optimization belongs to NP and admits polynomial-size KKT-based reformulations*](https://arxiv.org/pdf/2307.06639), Operations Research Letters 51 (2023), 618–622, gives a polynomially encoded sufficiently large big-M for linear bilevel KKT reformulations. Its lower-level feasible sets are polyhedral. This is relevant to the polyhedral/nonpolyhedral boundary but does not directly establish the proposed nonlinear penalty lower bound. The candidate does not, without another argument, prove a general lower bound for every nonlinear KKT reformulation.

**Source correction that affects interpretation.** Lefebvre–Schmidt Example 13 should not be used as evidence of a positive optimized duality gap for every finite penalty. In their example, write \(c=\lambda+\rho\), since the residual \(x_2\) is nonnegative. For \(c\ge1/2\), their branches give

\[
 z^{LR+}_\rho(\lambda)
 =\min\{c-3/2,-1/(4c)\}.
\]

As \(\lambda\to+\infty\), this tends to the primal value zero for every fixed \(\rho\ge0\). Weak duality then gives \(z^{LD+}_\rho=0\). No finite multiplier attains that value: taking a sufficiently small negative \(x_1\) with \(x_2=x_1^2\), \(x_3=0\), always gives a negative Lagrangian value. Thus the example separates attainment of an exact relaxation from zero gap for the supremum-defined dual. This calculation does not invalidate the explicit open encoding-size question, and the proposed one-binary and symmetric constructions avoid this distinction entirely. This correction was independently derived here and communicated for separate rechecking; it is not treated as an independently reviewed theorem in this file.

**Significance and limits.** A careful paper could present the construction as a negative resolution of the general extension posed in the inspected Lefebvre–Schmidt version. Its strongest restrictions are compactness, a linear objective, one binary, one scalar equality, constant coefficients, convex quadratic native constraints, and uniform native strict feasibility. These restrictions isolate a genuine boundary between polyhedral and quadratic native geometry. The argument is elementary after the classical chain is known; a publication claim should rest on the precise open question and restrictions, not on proof length or a broad novelty claim.

The theorem does not establish computational hardness of solving these instances: their primal solution is immediate. It does not exclude short arithmetic circuits, floating representations with unbounded binary-encoded exponents, reformulations, or presolve arguments that detect the bad assignments. Scaling the equality by an enormous factor can also move magnitude into its coefficient, so the model's original rational encoding is part of the statement. No claim of practical speedup follows. A useful further theory would quantify separation of equality-infeasible integer slices, in addition to multiplier bounds on feasible slices, and identify important model classes in which that separation has polynomial encoding size.

**Search and verification record.** Primary-source web searches covered the three exact-ALD papers, QCQP extensions through 2026, polynomial/bit-encoding penalty bounds, SOCP/SDP exponential-size solutions, conic exact penalties, and KKT big-M encodings. The most relevant titles and links are recorded above. Queries including “exact penalty doubly exponential”, “penalty parameter encoding length”, and “Exact Augmented Lagrangian quadratically 2026” did not expose an equivalent multiplier-independent statement. This is limited search evidence, not proof of novelty.

The following targeted work was performed: downloaded the linked open preprints into `parametric-sources/`; ran `pdftotext -layout` on each; inspected the cited portions with `rg` and `sed`; directly checked the residual-sign and threshold calculations; obtained an independent adversarial comparison from a separate conic-precision reviewer. A `python` script using `fractions.Fraction` checked the four strict native points of the symmetric companion and the two strict native points of the main one-binary construction (minimum slack exactly `1/8`) and the chain identity for `n=1,...,8` (all assertions passed). This finite calculation supports the indexing and displayed strict points; the general claims still rely on the algebraic arguments. `git diff --no-index --check /dev/null research-20260925/parametric-penalty-literature-review.md` checked the new note's whitespace. No project-wide checks or CI inspection were run. This review is not a formal proof verification or an exhaustive literature survey.
