# Literature investigation

Search date: 2026-09-22. This record distinguishes read evidence from search
leads. The manuscript must cite publications, not repository notes.

## Primary sources and comparison

- Gilyén, Su, Low, Wiebe, *Quantum singular value transformation and beyond*,
  STOC 2019, arXiv:1806.01838. Local package
  `andras2019-quantum-singular-value-transformation-beyond` has full text.
  Relevant prior tools: bounded definite-parity polynomial implementation,
  sign approximation, uniform amplification, and Theorem 73's pairwise
  eigenvalue-transformation lower bound. Neither generic polynomial synthesis
  nor the square-root pairwise obstruction should be claimed as new.
- Motlagh and Wiebe, *Generalized Quantum Signal Processing*, PRX Quantum 5,
  020368 (2024), doi:10.1103/PRXQuantum.5.020368, arXiv:2308.01501.
  Local full text inspected at Theorems 3--4 and Corollary 5. The bounded
  unit-circle polynomial characterization removes definite-parity constraints.
  Centering a Laurent polynomial is an application of this prior theorem.
  The potential new result is the particular optimal shift staircase and its
  comparison to single-sequence definite-parity transforms.
- Low and Chuang, *Hamiltonian Simulation by Uniform Spectral Amplification*,
  arXiv:1707.05391. Local full text available. Spectral amplification and
  its normalization accounting precede this work. Our high-accuracy upper
  bound is comparable to standard amplification; the new claim should focus
  on the matching continuum lower and the accuracy thresholds.
- Bessen, *The power of various real-valued quantum queries*, Journal of
  Complexity 20(5), 699--712 (2004), doi:10.1016/j.jco.2003.07.001;
  preprint *Approximation of Various Quantum Query Types*,
  arXiv:quant-ph/0308140. Publisher abstract and arXiv page confirm the
  trigonometric-polynomial query method and non-equivalence of query types.
  This is a direct methodological antecedent, not a new technique here.
- Laneve, *An adversary bound for quantum signal processing*, Quantum 10,
  2025 (2026), doi:10.22331/q-2026-03-13-2025, arXiv:2506.20484.
  Local package is named `laneve2025-an-adversary-bound-for-quantum`, but
  the published metadata is now 2026. Publisher abstract and references
  checked online. It characterizes QSP through state conversion/adversary
  feasibility; do not imply that this general viewpoint is new.
- Dong, Larsen, Lin, Sarkar, *Constrained minimax approximation for quantum
  signal processing*, arXiv:2608.30937 (2026). Local full text and online
  metadata available. It treats prescribed-parity minimax fitting with global
  boundedness, numerical Remez methods, and Fourier retraction. Its continuum
  feasibility warnings require our constructions to be proved contractive,
  rather than certified by a sampled plot.
- King, Low, Babbush, Somma, Rubin, *Quantum simulation with sum-of-squares
  spectral amplification*, arXiv:2505.01528 (2025); local package records
  a 2026 PRL publication doi:10.1103/m3fj-m4rm, requiring publisher metadata
  verification before using the journal entry. The arXiv abstract was checked.
  SOS factor access and low-energy amplification are prior art, distinct from
  unit-normalized complement conversion from a plain matrix block encoding.
- Orsucci and Dunjko, *On solving classes of positive-definite quantum linear
  systems with quadratically improved runtime in the condition number*,
  Quantum 5, 573 (2021), doi:10.22331/q-2021-11-08-573.
  Local full text inspected for factor access, rectangular pseudoinverses,
  and the good-subspace amplitude caveat. A generic square-root condition
  improvement is not new. The proposed application needs its explicit
  exact-central LP, matched oracle contracts and complement-conversion transfer.

## Approximation-theory antecedents

- Bos, Ma'u, Waldron, *Extremal growth of polynomials*, Analysis Mathematica
  (2020), doi:10.1007/s10476-020-0028-8. Local package lacked full text.
  An author-hosted open copy was located at
  https://www.math.auckland.ac.nz/~waldron/Preprints/Extremal-growth/BosMauWaldron1.pdf .
  Proposition 2.1 states the classical exterior Chebyshev inequality and
  attributes it to the established theory. Give a short proof or cite this
  precise proposition. The inequality itself is not original.
- Lewis, *Approximation with Convex Constraints*, SIAM Review 15(1), 193--217 (1973),
  doi:10.1137/1015006. Publisher abstract inspected: general finite-dimensional
  convex constrained approximation, including positive polynomial problems.
  Do not claim positivity-constrained approximation itself is new. Full text
  was not available in the local corpus.
- Taylor, *On Approximation by Polynomials Having Restricted Ranges*,
  SIAM Journal on Numerical Analysis (1968), doi:10.1137/0705022.
  Local package has metadata only. Treat as historical context; do not claim
  a theorem-by-theorem exclusion based on unread full text.
- Campos Pinto, Charles, Després, *Algorithms for Positive Polynomial
  Approximation*, SIAM Journal on Numerical Analysis 57(1), 148--172 (2019),
  doi:10.1137/17M1131891. An author-provided full-text search result gives
  the problem explicitly: nonnegative interpolation on [0,1] using Lukács
  representations. Obtain a primary-hosted copy if a detailed comparison
  becomes necessary. The local package's retrieval failed.
- Boundary Carathéodory--Schur interpolation and Fejér--Riesz factorization
  are classical. Local Agler--Lykova--Young and Bolotnikov packages are
  candidate references for background, not evidence that our precise
  constrained extremizer is absent from all older literature.

Additional primary-source checks: the publisher pages for Lewis, Taylor,
and Campos Pinto--Charles--Després were opened on 2026-09-22. The latter's
abstract describes algorithms for nonnegative interpolation using Lukács
representations, consistent with the author-provided excerpt. The Bos author
PDF was opened and Proposition 2.1 was read. The QSVT local full text was
checked at Corollary 18 (real bounded definite-parity synthesis, PDF pp.19--20),
Theorem 30 (uniform singular value amplification, p.29), and Theorem 73
(pairwise eigenvalue-transformation lower, pp.60--61). The real-polynomial
construction uses coherent averaging of conjugate phase sequences and
preserves unit normalization; an arbitrary-parity polynomial needs a
different synthesis route. Dong et al.'s local full-text introduction and
Sections 2.3--3 were read, including the distinction between numerical
sampled feasibility and global boundedness.

## Search record and scope of originality

Searches included combinations of unit-normalized spectral shift,
block-encoding complement normalization lower bounds, globally nonnegative
polynomial Chebyshev linear approximation, generalized QSP parity advantage,
and the cited authors/titles. The apparent title collision *Optimal lower
bound for lossless quantum block encoding*, arXiv:2305.18748, concerns quantum
source coding into Fock space, not matrix block encodings, and was excluded.

No direct match to the exact nonnegative thresholds and optimal fixed-relative-
accuracy staircase was located in this targeted investigation. That supports
a qualified, precisely scoped originality statement, not guaranteed priority.
The paper must separate established synthesis/approximation tools from its
specific extremizers, continuum query lower bounds, threshold-attaining
constructions, joint accuracy law, and LP realization. Exact threshold boundary
cases and the degenerate high band need especially careful checking.

## Root numerical cross-check

For rho=2, independently solving the hyperbolic stationary equation with
SciPy brentq gives G1=0.0211310131443374, G2=0.000260467264289756,
G3=4.85706271525714e-6 and G4=1.04651760368159e-7. G1 agrees with the
closed quadratic expression to floating-point precision, and the ratio to
the asymptotic sqrt(rho)/(e*r)*R0^(-2r) decreases toward one. This is a
numerical diagnostic, not a proof or certified error enclosure.

The publisher page confirms Lewis (1973), volume 15(1), pp.193--217;
its 2006 online posting is not the publication year. The King et al. DOI
resolver returned an internal retrieval error in this run, so the verified
arXiv metadata is the safe bibliographic form unless later checked.

Later primary-publisher verification during Stage 3 succeeded: King et al.
is Physical Review Letters 136, 110601 (17 March 2026), DOI
10.1103/m3fj-m4rm, at
https://journals.aps.org/prl/abstract/10.1103/m3fj-m4rm . The journal entry
can now replace the provisional arXiv-only citation. Bos--Ma'u--Waldron is
Analysis Mathematica 46, 195--224 (2020), directly verified at
https://link.springer.com/article/10.1007/s10476-020-0028-8 .

## Additional parity and state-preparation antecedents

- Essential motivation: Orsucci--Dunjko Section 4.3 (PDF pp.13--14, local
  fulltext lines 369--387) already explicitly asks how to obtain normalized
  B=I-eta*A, explains why LCU only gives a subnormalized block, and invokes
  QSVT Theorem 73 against generic black-box amplification. They give
  specialized sparse-value constructions for diagonally dominant matrices
  and sums of local PSD Hamiltonians. Our contribution must be described as
  a promise- and accuracy-dependent plain-block conversion analysis, not
  discovery of the normalization problem, and not resolution of their
  general sparse-value-oracle question. Root read this passage directly.

- QSVT Lemma 25 (local full text, PDF p.26) explicitly supplies a bounded odd
  sign approximant of degree O(delta^-1 log(1/epsilon)); it cites Low--Chuang
  and the optimal approximation work of Eremenko--Yuditskii. The sign
  approximation order itself is not new in the present paper.
- Eremenko and Yuditskii, *Uniform approximation of sgn(x) by polynomials and
  entire functions*, Journal d'Analyse Mathématique 101 (2007), 313--324,
  arXiv:math/0604324. Author publication list checked online at
  https://www.math.purdue.edu/~eremenko/papers.html; primary full text linked
  at https://www.math.purdue.edu/~eremenko/dvi/petia4.pdf . Their later
  *Polynomials of the best uniform approximation to sgn(x) on two intervals*,
  Journal d'Analyse Mathématique 114 (2011), 285--315, arXiv:1008.3765,
  DOI 10.1007/s11854-011-0018-7, is at
  https://www.math.purdue.edu/~eremenko/dvi/sgn2.pdf . Include the 2007
  antecedent in the literature comparison if asserting the odd-parity order;
  the specific shrinking-window shift comparison is the present application.
  Root opened and read the author-hosted 2006 manuscript of the 2007 paper:
  Theorem 1 gives fixed-gap minimax asymptotics on symmetric intervals;
  Theorems 2 and 5 concern entire-function and shrinking transition/Hausdorff
  limits. Do not assert that a gap-times-log-error phenomenon first appears
  here. Our odd lower is elementary and needs correctness only on the short
  positive low window, with global boundedness supplied by QSVT.
- Brassard, Høyer, Mosca, Tapp, *Quantum amplitude amplification and estimation*,
  Contemporary Mathematics 305 (2002), 53--74, DOI 10.1090/conm/305/05215,
  arXiv:quant-ph/0005055. Local full text inspected at Theorems 11--12;
  Theorem 12 gives the amplitude-probability estimation bound needed for
  sharp fixed-error state upper bounds in the LP example. No new amplitude
  estimation algorithm is claimed.

- A further direct approximation antecedent found during final presentation:
  Sarkar and Yoder, *Density theorems with applications in quantum signal
  processing*, Journal of Computational and Applied Mathematics 430, 115243
  (2023), DOI 10.1016/j.cam.2023.115243, arXiv:2111.07182. Primary publisher
  abstract and arXiv PDF were opened; root read the introduction and Definitions
  1.1--1.2. It proves density for QSP-related polynomial families constrained
  on and outside [0,1], with appropriate endpoint matching, and studies step
  approximation. This is important prior work on exterior constraints. The
  comparison here is quantitative shrinking-window query thresholds versus
  those density and step-approximation questions, not a first claim for
  outside-domain constraints. Primary URLs:
  https://www.sciencedirect.com/science/article/abs/pii/S0377042723001875
  and https://arxiv.org/pdf/2111.07182 .

## Stage 4 presentation checks (2026-09-22)

The Stage 4 author read the complete manuscript and the relevant local full-text
passages of Dong–Larsen–Lin–Sarkar (introduction, constrained feasible set and
numerical formulation), Orsucci–Dunjko Section 4.3, Haah's introduction and
complexity statement, and Laneve's introduction/state-conversion framing.
Primary metadata/abstract pages were independently rechecked for Bessen,
Laneve, Dong, King, Bos, Haah, Taylor, Campos-Pinto–Charles–Després, and
Eremenko–Yuditskii (author publication list). Taylor is 5(2), 258–268 (1968),
not the later online-posting year. The publisher spells the compound surname
Campos-Pinto; that spelling is used in the manuscript bibliography. The
historical Lewis/Taylor/Campos paragraph stays at the broad subject level;
no exclusion or theorem comparison is inferred from unavailable full texts.

The root suggested two additional direct comparisons, now included:

- Somma and de Wolf, *Optimal Lower Bound for Ground-State Energy Estimation
  with a Guiding State*, arXiv:2608.24493 (2026). The primary abstract was read
  at https://arxiv.org/abs/2608.24493 . Its joint ground-state bounds have
  guide-overlap and dimension hypotheses and include a sum-of-squares access
  variant. The manuscript distinguishes their energy/state output tasks from
  reusable complement conversion and does not transfer their bound.
- Sarkar and Yoder, *Density theorems with applications in quantum signal
  processing*, J. Comput. Appl. Math. 430, 115243 (2023), DOI
  10.1016/j.cam.2023.115243, arXiv:2111.07182. Root verified publisher metadata.
  Author independently read the primary abstract and HTML introduction,
  Definition 1.1, and the stated density conclusion at
  https://arxiv.org/html/2111.07182 . Their classes impose different range
  restrictions inside/outside [0,1], with endpoint compatibility; they also
  study a step approximant. The paper compares their qualitative density
  result with the present quantitative shrinking-window threshold problem.

The final originality statement is qualified by the cited literature and
scoped to the combination of exact thresholds, equality-attaining bounded
constructions and optimal shift-query exponents. No universal priority claim
or claim of new polynomial synthesis, sign approximation, Fejer–Riesz,
exterior Chebyshev, generic factor advantage, or amplitude estimation is made.

## Final review addition: supporting tangents (2026-09-22)

Fawzi, Saunderson, and Parrilo, *Equivariant Semidefinite Lifts of Regular
Polygons*, Mathematics of Operations Research 42(2), 472–494 (2017), DOI
10.1287/moor.2016.0813. The [publisher page](https://pubsonline.informs.org/doi/10.1287/moor.2016.0813)
confirms the May 2017 issue and November 16, 2016 online publication; the
bibliography uses the issue year and records the online date separately.

The [accepted manuscript](https://api.repository.cam.ac.uk/server/api/core/bitstreams/ccc24100-4e06-460d-b2fb-ccf567a429c3/content)
was inspected at Sections 3.1–3.2 and Appendix A, Lemma 1. It treats globally
nonnegative affine interpolation at finite nodes and proves the global
supporting-tangent inequality for even Chebyshev polynomials. The stable
section/appendix locators avoid the differing theorem numbers in arXiv v1.

The introduction now distinguishes that antecedent from this paper's
continuum minimax and query results. The note following `thm:thresholds`
credits the tangent inequality: with `z=(m_rho-y)/h_rho`, stationarity gives
`P_r^*(y)=G_r[T_{2r}(z)-T_{2r}(z_*)-T_{2r}'(z_*)(z-z_*)]`.
The existing self-contained proof and scoped originality statement remain.
