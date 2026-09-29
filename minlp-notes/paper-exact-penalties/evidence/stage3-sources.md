# Calibration and perturbation sources

All paths below are relative to the repository root. Primary documents were
read directly from retained PDF text; mathematical claims were checked
against the stated models rather than accepted from the repository reviews.
The manuscript uses the following comparisons, not a claim of exhaustive
priority verification.

| Source and version | Inspected locators and retained claim |
| --- | --- |
| Alessandroni, Ramos-Calderer, Roth, Traversi and Aolita, *Alleviating the quantum Big-M problem*, arXiv:2307.10379v4, July 30, 2025; npj Quantum Information 11, article 125 (2025) | Section IV.A, Lemma 1, PDF pp.5–6; the supplied-penalty reduction has a known zero constrained optimizer, a quadratic objective after auxiliary encoding, and the vector constraint x=0 with a squared penalty. An unrestricted multiplier reproduces its binary penalty term, so that reduction does not establish the present positive optimized-dual threshold. |
| Alessandroni, Ramos-Calderer, Krispin, Schinkel, Walter, Kliesch, Aolita and Roth, *Scalable Determination of Penalization Weights for Constrained Optimizations on Approximate Solvers*, arXiv:2604.02416v1 | Definition 1 on PDF p.3 defines probabilistic feasibility and energy guarantees. Theorem 2 on p.4 treats exact Gibbs sampling used for approximate optimization under infinite sampling and full penalty-energy range; the discussion following Definition 1 says hardness of its new optimal probabilistic weight is not established. This is a different guarantee from the manuscript's least optimized-dual norm penalty. |
| Mirkarimi, Hoyle, Williams and Chancellor, *Experimental demonstration of improved quantum optimization with linear Ising penalties*, arXiv:2404.05476v2, December 16, 2024; New Journal of Physics 26, 103005 (2024) | Section 2.2 begins on PDF p.6; its knapsack observation is on p.9. If a successful linear penalty always existed and could be tuned in polynomial time, knapsack could be solved by linear optimization on a box. The passage permits nonexistence of a successful penalty. |
| Dunagan, Spielman and Teng, *Smoothed Analysis of Condition Numbers and Complexity Implications for Linear Programming*, author manuscript March 30, 2009; Mathematical Programming 126, 315–350 (2011) | Theorem 2.3.3 and Lemma 2.3.4, PDF p.10. The latter bounds each inner and outer Euclidean Gaussian convex-body tube by 4 m^(1/4) d/sigma. The manuscript adds the union bound and explicitly extends it to lower-dimensional compact images by parallel bodies. |

The cube/fiber proof, grid coupling, scalar threshold identities and the
calibration reductions are proved in the manuscript. The general Gaussian
surface-area theorem and the source's shell integration are cited results,
not claimed as independently reproved. Standard NP-completeness of positive
integer SUBSET SUM and STABLE SET is used as the starting point of the
complexity reductions.

The deterministic perturbation bound needs convex slice objectives; the
nonconvex square-root example shows why that hypothesis matters. The new
exceptional-atom example is different: its slices are compact convex
quadratic sets and its objectives are linear, but refined Slater fails at
right-hand side zero. Balanced mixtures prove an infinite optimized
threshold there. This completes the finite-grid expectation qualification
without extending the good-event theorem.

## Source artifacts

| Primary URL | Local PDF | SHA-256 |
| --- | --- | --- |
| <https://arxiv.org/pdf/2307.10379v4> | `research-20260925/publication-sources/alessandroni-2307.10379v4.pdf` | `b43f9e92fc087432440ca89b414f9d4d38a4f8e5ee04838c2ca1f65024e0074f` |
| <https://arxiv.org/pdf/2604.02416v1> | `research-20260925/publication-sources/alessandroni-2604.02416v1.pdf` | `c8ddabd7c1ae247f3f81114fc6188423c1f81215566ba6ee60566e6409870114` |
| <https://arxiv.org/pdf/2404.05476v2> | `research-20260925/publication-sources/mirkarimi-2404.05476v2.pdf` | `e9aaaa22661b1eb3e6de97c03a659c9af1167138a200d9b8443b2b6c045d51f3` |
| <https://www.cs.yale.edu/homes/spielman/Research/lpcond.pdf> | `research-20260925/smoothed-sources/dst-smoothed-conditioning-2009.pdf` | `8a7c36eaec7649d7a974e2f32734043d5cd16ff06197ec7b2df93493e598aa3c` |

Publisher metadata for Dunagan–Spielman–Teng was checked at
<https://link.springer.com/article/10.1007/s10107-009-0278-5>.
Mirkarimi et al.'s author-institution repository record
<https://durham-repository.worktribe.com/output/2954855> supplied the
published volume, article number and DOI; its search result was readable,
while a subsequent direct open returned an internal error. The local v2
primary text supplied the mathematical comparison. The lead independently
read the Alessandroni 2025 publisher page
<https://www.nature.com/articles/s41534-025-01067-0> and supplied its verified
journal metadata and Methods Lemma 1 comparison. The writer's subsequent
open returned an internal error, so the proof comparison uses the retained
v4 primary text. The 2026 arXiv primary version record was also opened.
No failed retrieval was treated as evidence for a mathematical or priority
claim.

The lead's supplementary September 27, 2026 search used combinations of
“augmented Lagrangian”, “smallest”, “penalty”, “NP-hard”, “encoding”,
“quadratic”, “Slater” and “polynomial factor”, followed by the named
Lefebvre–Schmidt and Alessandroni sources. No additional directly matching
theorem was found; this bounded search is not a priority certificate. The
writer's additional searches checked the publication metadata of the two
older Gaussian/Ising sources. The manuscript cites only the primary sources
needed for its comparisons and proofs.

## Classical context checked during final revision

- Friedlander–Tseng, *Exact Regularization of Convex Programs*, SIAM Journal
  on Optimization 18 (2007), 1326–1350, DOI
  <https://doi.org/10.1137/060675320>. The retained author manuscript is
  dated November 18, 2006. Section 4, Theorem 4.2 (PDF pp.11–12, extracted
  text lines 580 onward) relates minimizer-set exactness to polar-gauge
  multiplier size under a nonempty compact solution set. The writer read
  the theorem and proof directly and opened the SIAM publisher record.
  Primary URL: <https://optimization-online.org/wp-content/uploads/2006/11/1531.pdf>.
  Local PDF: `research-20260925/smoothed-sources/friedlander-tseng-2007.pdf`;
  SHA-256 `2830afa597c6bad6aaa597690e1f57788c3f15e761e7f5f3288736dee13a950d`.
- Gugat–Hante, *Lipschitz Continuity of the Value Function in Mixed-Integer
  Optimal Control Problems*, arXiv:1612.04639v2, January 10, 2017. The
  writer read Assumption 4 (CQ, PDF p.5) and Theorem 3 (PDF p.8, extracted
  text lines 473 onward). Its Lipschitz conclusion assumes Assumptions 1–3
  and a uniform Slater/boundedness condition across discrete controls.
  The manuscript cites this as context, not as its finite-slice proof.
  The primary arXiv record also identifies the published article as
  Mathematics of Control, Signals, and Systems 29, article 3 (2017),
  DOI 10.1007/s00498-016-0183-4; this metadata is retained in the bibliography.
  Primary URL: <https://arxiv.org/pdf/1612.04639v2>. Local PDF:
  `research-20260925/smoothed-sources/gugat-hante-2016.pdf`; SHA-256
  `c191d1b6b874574a05947680416383a915bf425a7a3a48f1a55df54526fae3d0`.
- Bürgisser–Amelunxen, *Robust Smoothed Analysis of a Condition Number for
  Linear Programming*, arXiv:0803.0925v3, posted January 22, 2010;
  Mathematical Programming 131(1), 221–251 (2012), as recorded on the
  primary arXiv page. The writer retrieved the v3 PDF and read Theorem 3.3
  (p.14) and Corollary 3.4 (p.15): inner and outer neighborhoods of
  properly spherical convex sets in spherical caps, with the latter
  bound 13m epsilon/(4 sigma) for epsilon <= sigma/(2m). The manuscript
  credits only the spherical uniform-noise antecedent; it does not identify
  this with the cube lemma. The regenerated PDF title date is November 3,
  2018, so the explicit arXiv version identifies the inspected source.
  Primary URL: <https://arxiv.org/pdf/0803.0925v3>. Local ignored PDF:
  `paper-exact-penalties/evidence/sources/buergisser-amelunxen-v3.pdf`; SHA-256
  `81d09ad28189e385b28c38cc8cad9502592a79d7ecb860eb53f674628888d4b0`.

The finite-grid tail statement added in the final revision is restricted
to K dividing q and q >= 2K, and gives probability at least 2(K-1)/q
at threshold q. It makes no lower bound on that probability independent
of q. The fixed-zero-multiplier calibration consequence follows from the
existing nearest-residual construction and is proved explicitly in §6.1.
