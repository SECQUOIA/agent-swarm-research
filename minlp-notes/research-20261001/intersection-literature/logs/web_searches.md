# WebSearch / WebFetch queries run on 2026-10-01 (stream intersection-literature)

Mode in brackets. "New relevant" lists hits not already in the sfree note's Section 10.

| # | Query | Mode | New relevant hits |
|---|---|---|---|
| 1 | maximal quadratic-free sets intersection cuts choice of set best cut 2025 | extended | none (MS 2022, MPS 2025/2026, Chmiela, BCM) |
| 2 | "intersection cuts" QCQP "S-free" 2026 arXiv | extended | Pathy-Rahimian arXiv:2609.33946 (chance constraints); Xu-Pokutta arXiv:2608.03318 (joint-range inequalities) |
| 3 | strongest intersection cut nonconvex quadratic corner relaxation optimal S-free set selection | extended | none |
| 4 | "intersection cuts" "nonconvex quadratic" 2025 OR 2026 paper choosing maximal S-free set deepest cut | extended | none new |
| 5 | "SCIP Optimization Suite 10.0" arXiv report | standard | arXiv:2511.18580 |
| 6 | CCDLM "Cut-generating functions and S-free sets" pdf hal | standard | UAB preprint p05_13 (open copy) |
| 7 | Cornuejols Wolsey Yildiz "Sufficiency of cut-generating functions" pdf | standard + extended | CORE DP 2013/27 (host unreachable); Basu-Conforti-Di Summa survey arXiv:1701.06692 |
| 8 | Sercan Yildiz dissertation ... sufficiency | standard | thesis on figshare (Ch. 4 = CWY) |
| 9 | Kilinc-Karzan Yang "sufficiency of cut-generating functions" published journal | standard | author draft (revised Oct 2017); no journal version found |
| 10 | Glover "convexity cuts" "cut search" DTIC report pdf | extended | author-hosted copy (leeds-faculty.colorado.edu); Eckstein-Nediak "Depth-optimized convexity cuts" (Ann. OR 2005) |
| 11 | Konno 1976 cutting plane bilinear IIASA research memorandum pdf; pure.iiasa.ac.at Konno ... | extended / standard | IIASA WP-74-075 and RM-75-061 (open) |
| 12 | Sherali Shetty 1980 polar cuts disjunctive face cuts ... | extended | only Springer landing page (no open copy) |
| 13 | "Depth-Optimized Convexity Cuts" Annals of OR 2005 authors abstract | standard | Eckstein-Nediak; RUTCOR RRR 23-2003 (archived copy) |
| 14 | Eckstein Nediak "convexity cuts" RUTCOR research report pdf deepest cut | extended | RUTCOR 2003 list page |
| 15 | Porembski "How to extend the concept of convexity cuts ..." abstract | extended | Springer page only; a pirate-host copy was ignored |
| 16 | Balas Margot "generalized intersection cuts" pdf ... | standard | Kazachkov-Nadarajah-Balas-Margot arXiv:1703.02221 (describes GICs) |
| 17 | Chmiela Munoz Serrano "Monoidal strengthening ..." arXiv OR optimization-online pdf | standard | ZIB OPUS 8959/8913 (file access "not granted"); IPCO slides URL returned HTML |
| 18 | Antonia Chmiela dissertation TU Berlin intersection cuts ... | extended | master's thesis 2020 listed (no file) |
| 19 | local minimizer indefinite QP lies on face of dimension at most number of nonnegative eigenvalues ... | extended | none citable |
| 20 | Hager Pardalos "Active constraints, indefinite quadratic test problems, and complexity" ... | standard | JOTA 68 (1991) 499-511 (paywalled; not read) |
| 21 | "standard quadratic" local solution support size bounded by number of positive eigenvalues plus one Bomze lemma | extended | no exact statement found |
| 22 | NP-hard compute strongest intersection cut corner relaxation deepest cut complexity quadratic | extended | none |
| 23 | "outer-product-free" sets 2023-2026 maximal classification optimal cuts follow-up | extended | none beyond MPS papers |
| 24 | "optimal intersection cut" OR "best intersection cut" OR "deepest intersection cut" nonconvex quadratic | extended | none |
| 25 | intersection cuts quadratic constraints SCIP computational study 2025 dense cuts disabled by default nlhdlr quadratic | extended | SCIP 9 report; SCIP docs |
| 26 | Lorentz group transformations maximal S-free sets second-order cone complement intersection cuts all maximal sets orbit | extended | none |
| 27 | maximal "bilinear-free" sets OR "xy-free" sets intersection cuts bilinear constraint w = xy 2024-2026 | extended | none |
| 28 | "Nonconvex optimization problems involving the Euclidean norm" ... | standard | Kuznetsov-Sahinidis 2024 survey (cites MS 2022; not about set choice) |

WebFetch calls: Springer article pages (redirect to idp.springer.com; not followed), Semantic Scholar
API citation endpoints (see `s2_citations_via_webfetch.md`), arXiv abs pages 2604.00932 and 2605.30602
(only v1 exists), ideas.repec.org record of Eckstein-Nediak, ScienceDirect Fischetti-Monaci (HTTP 403),
alfresco.uclouvain.be (DNS failure).

## Revision round 1 (2026-10-02)

| # | Mode | Query | Result |
|---|---|---|---|
| R1 | standard | `Kılınç-Karzan Steffy "On sublinear inequalities for mixed integer conic programs" arXiv` | Author draft at andrew.cmu.edu (downloaded, `sources/kilinc-steffy-sublinear-draft-web.pdf`); Optimization Online 2015/07/5002; Springer DOI 10.1007/s10107-015-0968-0 |
| R2 | extended | `Chmiela Muñoz Serrano "monoidal strengthening" MIQCP computational results branch-and-bound arXiv pdf` | Springer pages only (login; not followed); Muñoz publications page (WebFetch: Springer links only, no preprint); MIP 2022 slides by Serrano (downloaded; no computations) |

WebFetch: https://gonzalomunoz.org/publications/ (no open copy of the monoidal paper or of the Math. Program. 197 version).
curl: OpenCitations v2 for 7 DOIs (`code/opencitations.py`, `opencitations.log`); Crossref for 3 citing DOIs (`opencitations_r1_titles.log`).
