# Latent separators and block-pattern design: priority audit

Date: 2026-09-12. This is a bounded primary-source audit, not a proof of novelty. It concerns exact discrete measurement selection with known correlated Gaussian errors and a fixed mean-sensitivity matrix. Root and the independent separator reviewer own the construction and its correctness review; this note does not replace their proofs or numerical validation.

The proposed method has a plausible useful role as a strengthening of correlated-noise design relaxations. Its individual ingredients are established. In particular, generalized D-optimal design already covers the target Schur-complement criterion and arbitrary finite positive-semidefinite experiment atoms; correlated-noise design already uses simplicial decomposition over complete designs; and nuisance-aware sensor selection already augments a target with latent variables to recover conditional independence. I did not find a source explicitly combining exact Markov separators, within-bridge observation patterns, and a hierarchy of target-information bounds. That limited search result does not establish priority for the combination.

## 1. Construction being audited

Suppose that conditioning a Gaussian error process on latent separator variables \(u\sim N(0,K)\) gives

\[
 y=F\theta+Hu+e,\qquad \operatorname{Cov}(e)=D,
\]

where \(D\) is block diagonal over disjoint candidate groups \(B_j\). Here \(K\) and the residual covariance blocks are positive definite; a positive-definite \(J_0\) is sufficient to keep every target criterion finite. A Markov process supplies such a representation by conditioning on selected latent states; the conditional covariance inside a bridge is generally dense. No observation is actually made of a separator. The variables are retained in the statistical representation and subsequently marginalized.

For pattern \(T\subseteq B_j\), define the joint information atom

\[
 Q_{jT}=[F_T,H_T]^\top D_{TT}^{-1}[F_T,H_T],\qquad Q_{j\varnothing}=0.
\]

For a schedule selecting one pattern per group,

\[
 M(S)=\operatorname{diag}(J_0,K^{-1})+\sum_j Q_{j,S\cap B_j}.
\]

Its target information is the Schur complement \(J(S)=M_{\theta\theta}-M_{\theta u}M_{uu}^{-1}M_{u\theta}\). A finite convex hull of these **joint** matrices, restricted to allowed complete schedules, gives a relaxation when maximizing \(\log\det J\). The Schur complement is taken after mixing. This differs from first computing every complete schedule's target information and then taking its convex hull.

If each group has at most \(b\) selectable packets, there are at most \(2^b\) group patterns. Exact total cardinality can be enforced in a count-layered multiple-choice path. Linear optimization over that path is a standard dynamic program with \(O(q(k+1)2^b)\) transitions for \(q\) groups. This cardinality hull is stronger than simply imposing an expected count on independent group probability vectors. The claim is only about pricing complexity; joint-matrix factorization, atom construction, memory, and numerical conditioning also contribute to the solver's cost.

## 2. Direct equivalences and established ingredients

### Generalized D-optimal design already supplies the conic formulation

Sagnol and Harman (2015), *Computing exact D-optimal designs by mixed integer second-order cone programming*, defines information \(M(w)=\sum_iw_iA_iA_i^\top\) for arbitrary multiresponse experiment matrices. Its Introduction, pp. 2–6, permits parameter subsystems and general linear constraints on integer weights. Theorem 4.3 and Corollary 4.4 establish SOC representability of

\[
 \Phi_{D\mid E}(M)=\det\{(E^\top M^{-1}E)^{-1}\}^{1/p}.
\]

Set \(E=[I_p,0]^\top\), take one atom for each separator pattern, and add the fixed prior as a fixed-weight atom. Then \((E^\top M^{-1}E)^{-1}\) is precisely the target Schur complement. Pattern selection and count-flow constraints are linear integer constraints, so the resulting exact design problem is an instance of their framework. Log determinant has the same maximizers as the determinant root. This does **not** mean their paper constructs Markov separators or proves the proposed hierarchy; it does rule out claiming a new generalized D criterion or new generic conic representation. [Primary paper, arXiv:1307.4953](https://arxiv.org/abs/1307.4953), DOI [10.1214/15-AOS1339](https://doi.org/10.1214/15-AOS1339).

The continuous version of this atom formulation is a natural competing implementation, even if the specialized rank-\(p\) support oracle is substantially faster. Factorizing rational PSD atoms to obtain conic coefficients can introduce irrational entries; this is a numerical modeling consideration, not an obstacle to the mathematical equivalence.

### Full latent augmentation recovers a virtual-noise split

Liu et al. (2016), §II.B, equations (8)–(11), splits a covariance as \(R=S+aI\) and derives an exact binary Fisher-information expression with a concave continuous extension. If all latent process states are retained and the remaining observation noise is \(aI\), the separator formulation gives this same extension. A nonconstant diagonal residual gives its diagonal-split counterpart. [Primary paper, arXiv:1508.03690](https://arxiv.org/abs/1508.03690), DOI [10.1109/TSP.2016.2550005](https://doi.org/10.1109/TSP.2016.2550005).

The implementation's label `b=1` must not automatically be called exactly the scalar Liu baseline. The independent reviewer reports that its last latent state is omitted from the anchor list. That leaves a larger last diagonal residual variance, giving a diagonal-split improvement over a literal all-anchor model. The equivalence is exact for the actual covariance split, with boundary handling stated explicitly.

There is a second comparison issue. The physical nugget \(a=r\) need not be the strongest admissible virtual-noise split: \(a\) can approach \(\lambda_{\min}(R)\), and diagonal choices can improve further. A hierarchy that strengthens the physical latent split is not thereby proved to dominate every Liu/virtual-noise relaxation.

### Complete-design mixtures and support searches are direct prior

Hainy, Müller, and Pázman (2025), §3, proves the Liu/virtual-noise equivalence. Its §4.4 explicitly uses simplicial decomposition: maintain extreme complete designs, optimize over their convex hull, and add an extreme point by solving the linearized design problem. Projected Newton or multiplicative algorithms solve the restricted master; Appendix D supplies stopping conditions. Thus fully corrective design mixtures and tangent pricing are already a practical correlated-noise design algorithm. [Primary paper, arXiv:2504.17651](https://arxiv.org/abs/2504.17651).

Pázman, Hainy, and Müller (2022) is the earlier convex virtual-noise and upper-bound reference. [Primary paper, arXiv:2103.02989](https://arxiv.org/abs/2103.02989), DOI [10.1214/22-EJS2071](https://doi.org/10.1214/22-EJS2071). Uciński and Patan (2024), *Sensor Selection with Correlated Observations via Convex Relaxation*, also reports simplicial decomposition, a multiplicative restricted master, and linear pricing for correlated-noise A-optimal PDE sensor selection. Its primary abstract was available in search, but the conference PDF returned HTTP404 and remains unread here. It is a particularly relevant comparator, not evidence of the separator hierarchy.

### Targeted inference in the presence of latent nuisance parameters is established

Alexanderian, Petra, Stadler, and Sunseri (2021), *Optimal Design of Large-scale Bayesian Linear Inverse Problems Under Reducible Model Uncertainty*, gives the linear model \(y=Fm+Gb+\eta\), a joint Gaussian prior, and the full block posterior precision. Equation (2.4), PDF p. 6, gives the same target Schur complement. Section 3.2, Theorem 3.3 and Corollary 3.4, proves convexity of the marginalized A criterion over continuous sensor weights. Their objective and numerical method differ, but retaining latent variables and accounting for their uncertainty in a focused design criterion is direct prior. [Primary paper, arXiv:2006.11939](https://arxiv.org/abs/2006.11939), DOI [10.1137/20M1347292](https://doi.org/10.1137/20M1347292).

Levine and How (2013), *Sensor Selection in High-Dimensional Gaussian Trees with Nuisances*, §7 and Proposition 7, augments a relevant latent set until observations become conditionally independent, then uses a greedy augmented-target mutual-information problem to bound focused information. Section 2 already states precision marginalization by Schur complement. Their bound values the augmented target, with a submodularity-based efficiency factor. The proposed separator relaxation retains the original target through a Schur complement and can use conditionally independent groups with alternative patterns. This is a distinction between bounds, not a claim that nuisance augmentation is new. [Primary NeurIPS paper](https://proceedings.neurips.cc/paper_files/paper/2013/file/8a1e808b55fde9455cb3d8857ed88389-Paper.pdf).

### Grouping discrete alternatives before convexification is established

Balas (1985), Theorem 4.3, orders hull relaxations obtained by distributing intersections across disjunctions. Papageorgiou and Trespalacios (2025), Proposition 4 and Corollary 2, studies the bound gains and computational costs of grouping convex disjunctions. These are the relevant MINLP/GDP antecedents for increasing a group's pattern size. They do not by themselves prove the exact separator hierarchy: removing a latent separator also changes the matrix representation and performs statistical marginalization. The comparison across representations needs its own correct projection/Schur argument. [Balas DOI10.1137/0606047](https://doi.org/10.1137/0606047), [Papageorgiou–Trespalacios arXiv:2501.15345](https://arxiv.org/abs/2501.15345).

The repository itself already noted enumeration of all within-time measurement patterns for the independent six-channel blocks in Wang et al.'s kinetics example. See [measurement source audit](research-20260912-measurement-source-audit.md). Enumeration for independent correlated blocks must not be presented as a new result of the separator work.

## 3. Additional correlated-block and random-effects prior

The following sources help delimit the remaining scope. The reading status matters: an abstract or a search extract is insufficient to exclude an exact construction hidden in the full paper.

| Source | Read scope and relevance |
|---|---|
| Ankenman, Avilés, Pinheiro2003, *Optimal designs for mixed-effects models with two random nested factors*, Statistica Sinica13:385–401 | Full author PDF retrieved; §§2–5 inspected. Enumerates assembled nested batch/sample designs. Equations (3)–(6) and Theorems1–4 derive information and balanced designs for fixed effects and two variance components. It concerns independent nested structures at treatment points, not an arbitrary temporal bridge hierarchy. [Primary journal](https://www3.stat.sinica.edu.tw/statistica/j13n2/j13n27/j13n27.html). |
| Holland-Letz, Dette, Pepelyshev2011, *A geometric characterization of optimal designs for regression models with correlated observations* | Primary abstract and equation/Theorem2.1–2.2 search extracts inspected; direct page retrieval hit a browser challenge. Uses independent individuals with correlated multiresponse observation schedules and generalized information atoms. This is strong prior for treating an entire within-group schedule as one design point, but full-text priority remains incompletely checked. [Primary PMC article](https://pmc.ncbi.nlm.nih.gov/articles/PMC3106301/). |
| Holland-Letz, Dette, Renard2012, *Efficient Algorithms for Optimal Designs with Correlated Observations in Pharmacokinetics and Dose-Finding Studies* | Abstract inspected. Multiplicative algorithms and efficiency bounds for within-patient correlation, random effects, and treatment-allocation constraints. Full text still needed. DOI [10.1111/j.1541-0420.2011.01657.x](https://doi.org/10.1111/j.1541-0420.2011.01657.x). |
| Harman and Trnovská2009, *Approximate D-optimal designs of experiments on the convex hull of a finite set of information matrices* | Primary bibliographic page inspected; full text not read. Direct finite-PSD-atom convex-hull and multiplicative-algorithm precedent. Mathematica Slovaca59(6):693–704. DOI [10.2478/s12175-009-0157-9](https://doi.org/10.2478/s12175-009-0157-9). |
| Rodríguez-Díaz2017, *Computation of c-optimal designs for models with correlated observations* | Primary abstract and author-text extracts inspected. Covariance whitening and independent correlated blocks; no separator-pattern formulation identified in that inspected material. DOI [10.1016/j.csda.2016.10.019](https://doi.org/10.1016/j.csda.2016.10.019). |
| Aretz, Chen, Degen, Veroy2024, *A greedy sensor selection algorithm for hyperparameterized linear Bayesian inverse problems with correlated noise models* | Published PDF retrieved; Introduction and §§3–4 inspected. Optimizes a worst-configuration observability coefficient with greedy matching pursuit and correlated-noise updates. The paper explicitly says the iterative procedure does not guarantee the best sensor combination. Its geothermal PDE example is useful practical context, but it is not a D-optimal separator upper bound. DOI [10.1016/j.jcp.2023.112599](https://doi.org/10.1016/j.jcp.2023.112599). |
| Yamada et al.2021, *Fast greedy optimization of sensor selection in measurement with correlated noise* | Primary abstract inspected. Bayesian D-optimal sensor selection, modal covariance modeling, and low-rank noise acceleration. Strong feasible-design comparator; no bound-hierarchy claim checked. DOI [10.1016/j.ymssp.2021.107619](https://doi.org/10.1016/j.ymssp.2021.107619), [arXiv:1912.01776](https://arxiv.org/abs/1912.01776). |

The 2026 López-Fidalgo–Wong review has an accessible primary abstract and indexed excerpts, but repeated direct full-PDF retrieval remains unsuccessful. Its broad discussion of certification difficulty should not be quoted as proof that no certificates exist: the virtual-noise papers already give relevant bounds, with clearly delimited assumptions. The review explicitly says it is not comprehensive. DOI [10.1146/annurev-statistics-042324-012947](https://doi.org/10.1146/annurev-statistics-042324-012947).

## 4. What could still be useful

The defensible candidate is a specialized, exact statistical reformulation that strengthens an existing relaxation by changing the retained latent separators and enumerating small conditional blocks. It needs evidence at the complete solver level. The following comparisons determine whether this is a meaningful contribution rather than an illustrative application of established machinery.

1. **Bound strength:** compare each separator level against the strongest scalar or diagonal virtual-noise split used by the existing baseline, not only the physical-nugget split. Prove only the order that the actual nested anchor sets support. Arbitrary partitions or shifted grids need not be comparable.
2. **Computational tradeoff:** report atom construction, joint-matrix factorization, support pricing, restricted-master work, memory, and certified upper-bound quality. A fixed number of candidates per bridge avoids a calendar-memory \(2^L\) explosion as correlation grows, but the retained nuisance dimension increases with grid size. It is not a grid-independent algorithm.
3. **Generic conic comparison:** run a Sagnol-style continuous or mixed-integer model on the same atoms at a manageable size. A specialized support certificate is useful if it materially improves bound-versus-time behavior or permits a substantially larger instance.
4. **Feasible schedules:** compare greedy and exchange designs under the exact same selected covariance. A much tighter relaxation can still have an integrality gap. An integer pattern schedule is exact for the original model; a fractional optimum is only an upper bound.
5. **Scope:** known covariance, fixed/local mean sensitivities, and complete selectable packets are the initial claims. Unknown covariance-parameter Fisher information, nonlinear Bayesian expected information, arbitrary latent approximation, or off-grid time optimization require additional analysis.

A strong outcome would be a verified hierarchy that closes difficult correlated-noise design gaps at modest bridge sizes and provides useful certificates on a motivated kinetic or process model. A new formula for Gaussian marginalization, a new name for simplicial decomposition, or a pure pattern-enumeration example would not be sufficient.

## 5. Search and retrieval record

All searches in this audit were made on 2026-09-12. Query families included `optimal design latent Schur complement correlated`, `optimal designs mixed-effects assembled`, `sensor selection separator Gaussian`, `sensor selection Markov bridge`, `experimental design Markov separators`, `optimal design correlated block convex hull`, `sensor selection nuisance integer`, `optimal design virtual noise block`, and exact-title searches for the papers above. No exact separator-pattern design method appeared in the returned material. This is a bounded negative search, not an exhaustive search of all graphical-model, mixed-model, or disjunctive-optimization literature.

Existing KB full texts inspected: Sagnol–Harman2015; Liu et al.2016; Hainy et al.2025; Pázman et al.2022; Levine–How2013. Balas1985 and Papageorgiou–Trespalacios2025 were mapped using their existing source-grounded KB notes. Their full proofs were not re-audited here.

New PDFs retrieved directly through the prescribed `lit.py get` source path, followed by `pdftotext -layout`:

- `/tmp/research-20260912-alexanderian-reducible.pdf` and `.txt`: arXiv2006.11939, v1 dated2020-06-21 in the retrieved text; relevant pp6–10 read.
- `/tmp/research-20260912-ankenman2003.pdf` and `.txt`: author-hosted published paper; §§2–5 inspected. PDF color-profile warnings did not prevent text extraction.
- `/tmp/research-20260912-aretz2024.pdf` and `.txt`: author-institution-hosted published JCP paper; Introduction and §§3–4 inspected.

Unsuccessful retrievals: Uciński–Patan2024 conference PDF HTTP404; López-Fidalgo–Wong2026 signed primary PDF HTTP302 without a body; Holland-Letz et al. geometric preprint CiteSeerX PDF HTTP301 without a body, and PMC direct page browser challenge. These are access results from this audit, not claims that no lawful full text exists.

All newly identified relevant works and the available full texts were sent to the sole `/root/literature` maintenance agent in sequential batches. That agent owns deduplication, bibliographic verification, source retrieval, KB additions, and the final missing-source record. Other adjacent sources routed include the 2023 exact-factorial MISDP paper, Nagata et al.'s proximal correlated-noise selection paper, Koval et al.2020 on irreducible uncertainty, the Huan–Jagalur–Marzouk2024 OED survey, the Liu–Yin–Liu2023 CO2-capture sensor-design paper, and Zhong et al.2024 on sparse distributed sensor selection. None was used to infer an unexamined theorem.
