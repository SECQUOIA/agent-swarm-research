# Standards lane citation ledger

Reviewed 6 October 2026. This ledger covers the 12 keys in
`standards-keys.txt` and the claims that use them in Sections 01, 02, 03, 05,
06, 08 and 09. Appendix B has no citations. Bibliographic identities were
checked against the read source, Crossref records, or the publisher record as
specified below. Page numbers refer to printed pages unless marked as PDF
pages.

`standards.bib` contains the verified entries expected to remain cited after
the root's planned edits. The Rockafellar entry is replaced by Ben-Tal and
Nemirovski for separation; the Lauritzen entry is removed because the
manuscript gives the dynamic program and already cites Bienstock. These
decisions and all 12 key mappings are retained in `standards-map.json`.

## Claim checks and locators

| Manuscript use | Source evidence and status |
|---|---|
| Section 01: moment/SOS hierarchies and convergence under Archimedean assumptions | Lasserre, Theorem 4.2, pp. 14–16, gives convergence for the compact semialgebraic hierarchy under its Archimedean certificate assumption. Parrilo, pp. 14–19, supports the general SOS/SDP and Positivstellensatz optimization framework. The claims are supported; neither source is evidence for the paper's sparse quantitative rate. |
| Section 02: finite SDP strong duality and dual attainment | Ben-Tal and Nemirovski, *Lectures on Modern Convex Optimization*, Theorem 2.4.1, p. 57: a strictly feasible primal conic problem bounded below has equal primal/dual values and a solvable dual. The moment problem is finite-valued, and its affine equalities can be eliminated by parameterizing the feasible affine plane before applying the theorem. The product PSD cone has nonempty interior, and the arcsine moment family is strictly feasible for every PSD block. This supports the manuscript's finite-SDP claim. |
| Section 02: even/odd Markov–Lukács interval forms, including zeros and degree caps | Powers and Reznick, p. 4681 (author PDF p. 5), reports Lukács's degree-preserving representation, citing Pólya–Szegő, *Problems and Theorems in Analysis II*, VI.47. For even degree $n$, the displayed representation is $p=f_1^2+(1-x^2)f_4^2$; for odd degree $n$, it is $p=(1-x)f_2^2+(1+x)f_3^2$. It states that each summand has degree at most $n$, and parity removes the other two terms. Replacing each square by an SOS block gives the manuscript's stated forms. The representation is stated for nonnegative polynomials, so zeros are allowed. |
| Section 02: conditional distributions on standard Borel spaces | Kallenberg, 2nd ed., Chapter 6, “Conditioning and Disintegration,” pp. 103–118; the publisher chapter record points to Theorem 6.4. The Springer text is not lawfully available in this lane, so the theorem statement and exact standard-Borel hypotheses were not checked from full text. Keep the citation without a pinpoint page; if a text-verified locator is required, use a readable standard-Borel disintegration source. The manuscript's junction-tree proof itself is complete once a regular conditional distribution exists. |
| Section 02: gluing local laws | The manuscript proves the running-intersection gluing construction in full. Its Lasserre 2006 citation (outside this lane's 12 keys) is the direct readable sparse-polynomial-optimization precedent: Theorem 3.6, pp. 6–12, glues local representing measures under the stated sparse assumptions. Vorob'ev's publisher abstract supports a general consistent-family extension result for regular finite complexes, but the article text was unavailable; applying that abstract-level result to the manuscript's finite junction-tree setting is an inference. Keep that limitation clear, or rely on the proof and Lasserre citation alone. |
| Section 03: tree-decomposition dynamic programming | Lauritzen's identity is correct (Oxford University Press/Clarendon Press, 1996; DOI 10.1093/oso/9780198522195.001.0001), but the full text and a precise algorithm locator were unavailable. The manuscript explicitly proves the bottom-up table recurrence and already cites Bienstock for the bounded-treewidth algorithmic context. Drop the Lauritzen citation; no bibliography entry is needed. |
| Section 05: Riesz representation for the signed moment-matching measure | Rudin, *Real and Complex Analysis*, 3rd ed. (McGraw-Hill, 1987) is the intended standard source identity. No lawful full text was available here, so the exact theorem locator and the signed-measure formulation were not verified from the book. The proof's use of Hahn–Banach followed by Riesz representation is mathematically standard, but do not add a page or theorem number. If a text-verified locator is required, substitute an accessible source stating the Riesz–Markov representation for $C(I)^*$. |
| Section 06: finite-dimensional separation | The old Rockafellar key points to *Convex Analysis* (Princeton University Press, 1970; DOI 10.1515/9781400873173), but the source text was not read. Replace it with Ben-Tal and Nemirovski, Theorem 2.4.2, p. 58. That theorem separates any two nonempty disjoint convex subsets of finite-dimensional Euclidean space by a nonzero linear functional; apply it to the singleton containing $p$ and the nonempty certificate cone $C_r$. This gives the exact separation claim used in the proof. |
| Section 08: Heijmans lift and comparison rate | The official arXiv v2 text was read. Theorem 2, pp. 8–9, constructs $F_\epsilon(x,u)=q_\epsilon(x)+\widehat c_\epsilon\lVert u-g(x)\rVert^2$, with $q_\epsilon(x)=F_\epsilon(x,g(x))$, a positive lower bound on the lifted compact box, and an upper bound controlled by the condition number of $q_\epsilon$. The lift degree is $\max\{\deg q_\epsilon,2\deg g\}$. Section 3 states that substitution back into the original variables gives certificate degree $r=aR+b$, with $a,b$ depending only on fixed generators. Theorem 4 (pp. 10–11) and Theorem 6 (pp. 12–13) give the corresponding effective Putinar and Schmüdgen degree bounds. |
| Section 08: dense $O((\log^{3/2} r/r)^\alpha)$ comparison | Section 08 explicitly limits this comparison to a dense formulation and certificate cone. The official arXiv v2 text, Theorem 2, pp. 8–9, constructs a fixed-degree lift with $F_\epsilon(x,g(x))=q_\epsilon(x)$, minimum at least $\epsilon/2$, and maximum controlled by the condition number of $q_\epsilon$; Section 3, p. 9, gives the substitution degree relation $r=aR+b$, where $a,b$ depend only on the fixed normalized generators. For $q_\epsilon=f-f^*+\epsilon$ and fixed data, $\kappa(q_\epsilon)=O(\epsilon^{-1})$. With the global error bound, the associated Łojasiewicz exponent may be taken as $L_g=1/\alpha$, so Theorem 2's graph-distance penalty coefficient is $O(\epsilon\,\kappa(q_\epsilon)^{2L_g})=O(\epsilon^{1-2L_g})$ and the lifted condition ratio is $O(\epsilon^{-2L_g})$. Combining this with the manuscript's dense ordinary-box rate yields the displayed $O((\log^{3/2}R/R)^{1/L_g})$ in lifted degree and, by $r=aR+b$, the stated rate in $r$. This rate is an inference from the lift and dense box bound, not a rate stated by Heijmans et al. The earlier sparse-lift bookkeeping is not used to assert membership in the paper's sparse certificate cone; the lift does not itself establish such membership. The direct displacement result and the manuscript's sparse conclusions are supported by their separate proofs and compatible constructions. |
| Section 09: rational SOS recovery under strict feasibility | Peyrl and Parrilo's title page and Crossref identify the first author as **Helfried Peyrl**, not “Tobias Peyrl” as in the current knowledge-base metadata. Their pp. 1–4 and 7–10 support numerical-symbolic rational rounding/projection and exact PSD/identity verification under strict feasibility. Correct the author in the final bibliography; do not edit the knowledge base in this lane. |
| Section 09: rational WSOS bit size and algorithm | Davis and Papp, Theorem 2.9, p. 15, bounds integer-certificate bit size using representation, interior-margin, and conditioning parameters. Algorithm 1, pp. 25–26, and Theorem 4.1, pp. 26–27, support rational Newton/rounding and global q-linear convergence under the stated WSOS interior conditions. Section 5, p. 32, notes that symmetry or term/correlative sparsity may reduce parameters. That is a discussion of sparse structure, not a theorem establishing the manuscript's expanded sparse-basis bound. The current attribution is accurate if kept at that level. |
| Appendix B | No citation commands occur in `appendices/B-recourse.tex`; its argument is self-contained. |

## Key-by-key identity and reading status

| Assigned key | Canonical identity / mapping | Identity and source status |
|---|---|---|
| `bental2001-lectures-modern-convex` | Aharon Ben-Tal and Arkadi Nemirovski, *Lectures on Modern Convex Optimization: Analysis, Algorithms, and Engineering Applications*, SIAM, 2001, DOI 10.1137/1.9780898718829. | Crossref metadata and legal author-hosted full PDF checked and read. Theorems 2.4.1–2.4.2, pp. 57–58, verified. |
| `davis2024-rational-dual-certificates-for-weighted` | Maria M. Davis and Dávid Papp, “Rational Dual Certificates for Weighted Sums-of-Squares Polynomials with Boundable Bit Size,” *Journal of Symbolic Computation* 121 (2024), article 102254, DOI 10.1016/j.jsc.2023.102254. | Crossref metadata and local original/full text checked and read. |
| `heijmans2026-degree-bounds` | Olga Heijmans-Kuryatnikova, Juan C. Vera, and Luis F. Zuluaga, “Degree Bounds for Positivstellensätze of General Semialgebraic Sets,” arXiv:2605.15821v2 (2026), DOI 10.48550/arXiv.2605.15821. | Official arXiv v2 original/full text checked and read. |
| `kallenberg2002-foundations` | Olav Kallenberg, *Foundations of Modern Probability*, 2nd ed., Springer, 2002, DOI 10.1007/978-1-4757-4015-8. | Crossref and Springer chapter metadata checked. Full text unavailable; no theorem statement or exact locator verified. |
| `lasserre2001-global-optimization` | Jean B. Lasserre, “Global Optimization with Polynomials and the Problem of Moments,” *SIAM Journal on Optimization* 11(3) (2001), 796–817, DOI 10.1137/S1052623400366802. | Canonical knowledge-base key is `lasserre2001-global-optimization-with-polynomials-and`; Crossref and local original/full text checked and read. |
| `lauritzen1996-graphical-models` | Steffen L. Lauritzen, *Graphical Models*, Oxford University Press/Clarendon Press, 1996, DOI 10.1093/oso/9780198522195.001.0001. | Publisher identity checked; full text and exact locator unavailable. Citation removed, so no final bibliography entry or ingest request. |
| `parrilo2003-semidefinite-programming` | Pablo A. Parrilo, “Semidefinite Programming Relaxations for Semialgebraic Problems,” *Mathematical Programming* 96(2) (2003), 293–320, DOI 10.1007/s10107-003-0387-5. | Canonical knowledge-base key is `parrilo2003-semidefinite-programming-relaxations-for-semialgebraic`; Crossref and local original/full text checked and read. |
| `peyrl2008-computing-sum-of-squares-decompositions` | **Helfried** Peyrl and Pablo A. Parrilo, “Computing Sum of Squares Decompositions with Rational Coefficients,” *Theoretical Computer Science* 409(2) (2008), 269–281, DOI 10.1016/j.tcs.2008.09.025. | Crossref and local original/full text checked and read. Existing knowledge-base frontmatter and generated reference have incorrect first name “Tobias”; use Helfried in the final bibliography. |
| `powers2000-univariate-interval` | Victoria Powers and Bruce Reznick, “Polynomials That Are Positive on an Interval,” *Transactions of the American Mathematical Society* 352(10) (2000), 4677–4692, DOI 10.1090/S0002-9947-00-02595-2. | Crossref and the author-hosted university PDF checked. Relevant Lukács degree/parity statement verified at p. 4681 (PDF p. 5). Earlier publisher/repository retrievals were unavailable; the lawful author copy closed the gap. |
| `rockafellar1970-convex-analysis` | R. Tyrrell Rockafellar, *Convex Analysis*, Princeton University Press, 1970, DOI 10.1515/9781400873173. | Crossref identity checked, but source text was not read. Replaced for this manuscript use by the verified Ben-Tal–Nemirovski separation theorem; no Rockafellar bibliography entry or ingest request. |
| `rudin1987-real-complex-analysis` | Walter Rudin, *Real and Complex Analysis*, 3rd ed., McGraw-Hill, 1987. | Bibliographic identity retained; no lawful full text or exact Riesz-representation locator was available in this lane. No page or theorem number asserted. |
| `vorobev1962-consistent-families` | N. N. Vorob'ev, “Consistent Families of Measures and Their Extensions,” *Theory of Probability and Its Applications* 7(2) (1962), 147–163, DOI 10.1137/1107014. | Crossref metadata and SIAM publisher abstract checked. Article full text unavailable; abstract-level extension result supports the broad historical attribution, while the junction-tree specialization is not text-verified. |

## Deduplicated unread or unavailable full text

These are the only distinct assigned works whose complete text was not read.
The first three remain cited; the last two have been removed/replaced and need
no owner action.

1. **Kallenberg (2002).** Publisher chapter metadata is available at
   <https://link.springer.com/chapter/10.1007/978-1-4757-4015-8_6>; the book
   record is <https://doi.org/10.1007/978-1-4757-4015-8>. The chapter text is
   paywalled. No access control was bypassed.
2. **Rudin (1987).** Bibliographic metadata only; no lawful full text or
   publisher page URL was verified in this lane. No access control was
   bypassed.
3. **Vorob'ev (1962).** SIAM publisher page and abstract:
   <https://epubs.siam.org/doi/abs/10.1137/1107014>. The article text was not
   available; no page or theorem locator is claimed.
4. **Lauritzen (1996), uncited after repair.** Publisher record:
   <https://academic.oup.com/book/53988>. Full text was not read; the citation
   was removed because the algorithm is proved in the manuscript.
5. **Rockafellar (1970), replaced.** DOI record:
   <https://doi.org/10.1515/9781400873173>. Full text was not read; the
   manuscript uses the verified Ben-Tal–Nemirovski separator instead.

## Serialized owner handoff

No knowledge-base files were changed in this lane. Sources absent from the
local knowledge base but still cited, and their lawful records/copies for the
shared owner to ingest serially if useful:

- **Ben-Tal–Nemirovski (2001):** DOI
  <https://doi.org/10.1137/1.9780898718829>; author-hosted full PDF
  <https://www2.isye.gatech.edu/~nemirovs/LMCOBookSIAM.pdf> (read here).
- **Heijmans-Kuryatnikova, Vera, and Zuluaga (2026):** official arXiv record
  <https://arxiv.org/abs/2605.15821> and full PDF
  <https://arxiv.org/pdf/2605.15821> (v2 read here).
- **Powers–Reznick (2000):** DOI
  <https://doi.org/10.1090/S0002-9947-00-02595-2>; author-hosted full PDF
  <https://reznick.web.illinois.edu/pos.pdf> (read here).
- **Kallenberg (2002):** DOI
  <https://doi.org/10.1007/978-1-4757-4015-8>; publisher chapter page
  <https://link.springer.com/chapter/10.1007/978-1-4757-4015-8_6> (metadata
  only; text paywalled).
- **Rudin (1987):** *Real and Complex Analysis*, 3rd ed., McGraw-Hill. No
  lawful full-text URL was verified here; keep metadata-only unless the owner
  has an authorized catalog/source URL.
- **Vorob'ev (1962):** DOI
  <https://doi.org/10.1137/1107014>; SIAM publisher record
  <https://epubs.siam.org/doi/abs/10.1137/1107014> (abstract only).

The owner was already notified of the absent-source set and author-hosted
Powers–Reznick locator. Lauritzen and Rockafellar are excluded from the ingest
request because their manuscript citations are removed or replaced.

## Targeted checks

- Read the cited passages in local original/full-text packages for Davis,
  Lasserre, Parrilo, and Peyrl; read the retrieved Ben-Tal–Nemirovski,
  Heijmans et al., and Powers–Reznick originals.
- `rg -n '\\cite|\\citep|\\citet' paper-sparse-sos/sections paper-sparse-sos/appendices`
  inventoried manuscript citations; Appendix B had none.
- `jq empty paper-sparse-sos/evidence/literature-lanes/standards-map.json`
  passed. A static key scan found 10 bibliography entries and no duplicate
  keys.
- No manuscript TeX or BibTeX build, knowledge-base check, CI, or experiment
  was run by this lane. The root owns final citation edits and manuscript
  build.
