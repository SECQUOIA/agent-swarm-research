# Stage 5 independent mathematics and primary-source review

**MAJOR: 0. MINOR: 1. Recommendation: accept after the scope correction below.**

I reviewed all new mathematics in `sections/fourier-identification.tex` and `appendices/observation-design.tex`, the abstract/introduction/discussion, `main.tex`, added bibliography, README, coverage map, and author handoff. I checked the Fourier argument against the accepted normalized log equation and half-moment estimate. Every file recorded in the frozen Stage 5 snapshot matched its SHA-256 digest when checked. I did not read other current reports, contact reviewers, edit shared manuscript sources, run a shared build, or rerun the unchanged numerical supplement.

## Numbered findings

### 1. S5-SRC-001 — MINOR: the claimed necessity of strictly smaller daughters is too strong

**Location:** `sections/fourier-identification.tex:211–212`, immediately before the complex mass identity. The same interpretation appears in the development handoff under proof decisions.

**Claim:** “Strictly smaller daughters are essential: a daughter atom at one would produce an invisible jump at zero.”

The second clause is correct for an unconstrained jump measure. The first clause is not correct as an identification boundary with the two known daughter constraints in this manuscript. Those constraints determine the invisible atom once the visible jump measure has been identified. This does not invalidate the structural-identification theorem as stated, which assumes support in `(0,1)` throughout.

To see the distinction, hypothetically allow a finite daughter measure on `(0,1]` with `B((0,1])=2` and `integral theta B(dtheta)=1`, retaining positive selection rate. Write

\[
 \nu_-=\sigma(\log)_\#(B|_{(0,1)}),\qquad
 a=\nu_-(( -\infty,0)),\qquad
 c=\int e^y\nu_-(dy),\qquad z=\sigma B(\{1\}).
\]

The local exponent identifies `nu_-` by the same one-sided lemma. The two constraints give `a+z=2 sigma` and `c+z=sigma`. Consequently

\[
 \sigma=a-c,\qquad z=a-2c,
 \qquad
 B=\sigma^{-1}\big((\exp)_\#\nu_-+z\delta_1\big).
\]

Thus the selection rate and the atom at one are uniquely determined. Equivalently, the very next displayed identity in the manuscript, `psi(-i)=-sigma`, still holds with that atom present. A private exact-rational check used `sigma=3` and `B=(1/2)delta_1+(3/2)delta_(1/3)` and recovered both correctly; the general algebra above is the evidence, not that numerical example.

**Proposed correction:** Delete the two-sentence necessity claim, or replace it by: “The strict support assumption excludes zero log jumps. Such an atom is invisible to the exponent alone; with the prescribed daughter count and mass, its weight could instead be recovered from those constraints.” No extension of the theorem or forward framework is required for this correction. Update the handoff's corresponding claimed boundary if that record is maintained.

## Mathematics checked without further findings

1. **Factorization (`fourier-identification.tex:41–95`).** The bounded real/imaginary tests give the stated source. Its paired increment is bounded by `|k| lambda H(t)^2/N(t)`, so the accepted half-moment estimate gives exactly `omega=kappa(b+sigma)`. Variation of constants has the correct damping condition `delta=omega+Re psi>0`, physical error `D exp(-omega t)`, and rescaled error `D exp(-delta t)`. Uniform local convergence proves amplitude continuity and nonvanishing without source smoothness or log moments. No positive-definiteness interpretation of the limiting amplitude is assumed.
2. **Quotients and uniqueness (`:104–209`).** The denominator threshold, the two tail errors, and the factor `exp(h Re psi)(1+exp(-delta h))` are correct. The anchored logarithm is uniquely chosen on a sufficiently small interval. For the one-sided lemma the lower half-plane has the correct sign: its exponential damps the negative support. Finite total variation gives boundary continuity and compact interior derivative domination. Schwarz reflection across a zero boundary interval, the identity theorem, and Fourier uniqueness justify the conclusion. Intersecting candidate-model neighborhoods handles unknown model-specific intervals. Selection, daughter, and coagulation recovery use exactly the stated observations; zero selection leaves the unused daughter measure unidentified.
3. **Instability and sampling (`:214–333`).** The complementary two-atom example preserves both daughter constraints, has variation distance four, and has uniformly convergent exponents on every bounded frequency interval. Hoeffding's bound gives `8 exp(-n epsilon^2/4)` after the four-component union bound. Both quotient identities and both denominator estimates are correct. The stronger signal condition avoids an unnecessary second attenuation factor. At the proposed time, `epsilon exp(dt)=epsilon^(delta/omega)`, which verifies the signal condition eventually and balances the two proved bounds, also when `d=0`. The interpretation correctly limits this to predetermined pointwise observations and relevant known constants, with no adaptation, minimax, full noisy inversion, or reactor-independence assertion.
4. **Preparation shell (`observation-design.tex:21–79`).** Relative interior permits polynomial extension to the full affine shell. The Hessian argument gives `Q K Q=0`; the proposed `A_0` reconstructs the symmetric kernel. The skew correction has the correct sign, `L^T h=gamma`, and adjusts the linear term without changing the kernel. Nonzero `h`, full row rank, and positivity/interior assumptions are used. The continuum two-constraint family is stated only as sufficient, and its trajectory conclusion follows from the scalar count equation with an integrable coefficient.
5. **Dilution and tomography (`:97–204`).** Monodisperse and two-atom tests give the complete known-source and unknown-source gauges. The residual polynomial is exactly `zeta(1-c/c_1)(1-c/c_2)`. Both reconstruction formulas, the additional source observation, and the finite-grid parameter count are correct, including repeated-size mixtures. Deterministic noise coefficients are `3/c^2`, `5/(2c)`, and seven for the source estimate. The finite-difference remainder, positive minimizing time, and minimum bound are correct with the stated curvature and measurement-error assumptions. Physical positivity and coefficient preservation are appropriately distinguished from algebraic identification.

## Primary-source and bibliography audit

**Garnier (2024).** [Version-one Section 2.2](https://arxiv.org/html/2405.10588v1#S2.SS2) explicitly displays the multiplicative noise factor, divides characteristic functions at two times to cancel it, and applies the distinguished logarithm. This is a direct antecedent, and the manuscript names it in both introduction and Fourier section. The nonlinear exponentially small remainder and non-probabilistic limiting amplitude are accurately distinguished. The [arXiv submission record](https://arxiv.org/abs/2405.10588v1) dates v1 to May 17, 2024; the dynamically generated HTML date is not the bibliography year. The bibliography follows the actual HTML article title (“independent”), while the abstract-page metadata has “independents”; I do not regard that source-internal discrepancy as a manuscript error.

**Doumic–Escobedo (2016).** I checked [equations (12)–(14), printed pages 4–5 of the linked preprint](https://arxiv.org/pdf/1510.03588): the Mellin transform solves the scalar equation and has the exact exponential factor claimed as the pure-fragmentation antecedent. Normalizing at Mellin argument one gives the number-law version relevant here. The current paper proves its own bounded-test extension and does not import the source's detailed density asymptotics into the larger daughter class.

**Doumic–Escobedo–Tournus (2018, 2024).** I checked the local primary texts and the [2018 publisher PDF](https://ems.press/content/serial-article-files/16864). The 2018 work identifies division parameters and daughter kernel from an asymptotic profile under positive power-law selection and additional hypotheses. The manuscript cites this as context without saying those hypotheses cover its constant-selection setting. The [2024 journal record](https://www.numdam.org/articles/10.5802/ahl.207/) and primary text describe short-time reconstruction, near-Dirac initial data, and Mellin estimates. Authors, titles, years, volumes, pages, and DOIs in both entries agree with the primary records.

**Mirzaev–Byrne–Bortz (2016).** The [author preprint](https://arxiv.org/pdf/1510.01355), particularly its introduction and flocculation application, supports the stated daughter-distribution estimation antecedent in an aggregation–fragmentation model. It has a different title and author order from the published article. The [indexed primary PMC manuscript header](https://pmc.ncbi.nlm.nih.gov/articles/PMC5352987/) explicitly gives the final singular title, Mirzaev–Byrne–Bortz order, volume 32(9), article 095005, 2016, and the DOI, as used in the bibliography. The manuscript does not claim this work proves its structural uniqueness theorem. Direct PMC navigation returned a browser challenge; the preprint itself was accessible and read.

**Hoang and coauthors (2022).** The [author-hosted published article](https://www.math.univ-paris13.fr/~phamngoc/HoangPhamRivoirardTran.pdf) confirms the bibliography on its first page. Sections 3.1.1–3.1.4, printed pages 9–12, give the log transformation, iid sampling from an asymptotic profile, Fourier division formula, and truncated denominator estimator. Its process has size growth and division, with no coagulation. The manuscript's attribution and model distinction are accurate. The [author's publication list](https://www.math.univ-paris13.fr/~phamngoc/Publications.php) independently confirms the 2022 issue year and pages; the earlier acceptance/copyright year is not a bibliography defect.

**Patil–Andrews, Lage, and McCoy–Madras.** The [publisher's indexed McCoy–Madras introduction](https://www.sciencedirect.com/science/article/abs/pii/S0009250903001593) explicitly credits the first two works with simultaneous aggregation/fragmentation examples having constant count, then discusses the variable-count case. The [Patil publisher record](https://www.sciencedirect.com/science/article/abs/pii/S000925099700314X) confirms its title, 1998 volume/issue/pages/DOI and links the Lage comment with its title, 2002 volume/issue/pages and author. These support the deliberately narrow introductory statement. Direct ScienceDirect fetches returned 403 responses; I did not examine the full older proofs or certify their complete parameter scope. No stronger statement about them is used by this manuscript.

**D'Orsogna–Lei–Chou (2015).** I read the [author-hosted published PDF](https://www.math.ucla.edu/~tchou/pdffiles/JCP_LEI.pdf), including the mean-field comparison in Section II and Figure 2. It supports existing discrepancies in finite-cluster assembly with total-mass and maximal-cluster constraints. It is not the current logarithmic-time additive theorem. The title, author order, volume, article number, year, and DOI `10.1063/1.4923002` agree.

**Ramkrishna (2000).** The user-supplied local original/text supports the Chapter 2 modeling, Chapter 6 inverse, and Chapter 7 stochastic references. In particular, Chapter 6's opening, printed pages 221–223, explicitly discusses extracting particle mechanisms from dynamic size distributions and the inverse problem's instability. The [publisher record](https://shop.elsevier.com/books/population-balances/ramkrishna/978-0-12-576970-9) confirms the title, author, original edition year, and contents. No redistribution of the local book was made.

**Brown–Donev–Bissett (2015).** The [indexed primary Section 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC4673519/) states the mixture-simplex constraint and classical quadratic Scheffé models. This supports the modest context citation; the exact preparation-shell proposition is proved in the current manuscript rather than falsely attributed to Brown et al. The [publisher article record](https://www.tandfonline.com/doi/pdf/10.1080/00401706.2014.947003) and [PubMed metadata](https://pubmed.ncbi.nlm.nih.gov/26681812/) agree with all bibliographic fields. Direct PMC navigation and publisher fetches were restricted; the indexed primary text and metadata were available.

**Hoeffding (1963).** I downloaded the openly available [RPI-hosted original article](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf) into a private temporary path and visually checked printed page 16. Theorem 2, equation (2.6), is exactly the independent bounded-summand inequality required. Applying both tails with component range two and threshold `epsilon/sqrt(2)` yields the manuscript's constant. The [publisher record](https://www.tandfonline.com/doi/abs/10.1080/01621459.1963.10500830) confirms the 1963 volume/issue/pages and DOI; its later online date is not the publication year.

## Integration, limitations, and preferences

Except for S5-SRC-001, the abstract, introduction, assumptions roadmap, discussion, README, and coverage map accurately distinguish proved statements from open questions. In particular, they preserve the differences among the auxiliary number process, physical finite particles, and independent continuum sampling. They do not promote classical transform cancellation, compound-Poisson limits, Borel/product formulas, or mixture algebra to new methods. Sharp instantaneous constants are not advertised as exact calendar-time exponents.

This bounded source audit supports the stated attribution; it does not certify priority for every model-specific theorem. Access limits above are accepted limits of this review, not additional numbered defects. None affects the self-contained proof of a new theorem. I have no additional editorial preference that needs to be resolved before Stage 5 acceptance.

**Final counts: MAJOR 0; MINOR 1. Accept after correcting the claimed strict-daughter identifiability boundary.**
