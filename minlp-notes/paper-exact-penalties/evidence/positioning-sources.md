# Contribution and literature review

This revision starts from `b63317ab072109d74ba5e27ee74759374ee24be9`.
Its literature review was conducted on September 27, 2026. The purpose is
to identify the exact contribution relative to directly related work, not
to certify exhaustive priority. All mathematical results and proofs are
unchanged. The abstract and introduction now put encoding first, explain
why multiplier optimization does not avoid the lower bound, and separate
the calibration and perturbation contributions.

## Source-to-claim comparisons

| Claim in this paper | Closest inspected evidence | Scope of the retained claim |
| --- | --- | --- |
| Exponential penalty bits in continuous dimension | Gu–Ahmed–Dey, Theorem 11; Lefebvre–Schmidt, Theorem 14 and conclusion; Bienstock–Del Pia–Hildebrand, §6, Example 6.2; Beck et al., §§2 and 4, Result 4 | Polynomial encoding for polyhedral native sets and finite nonlinear exactness are prior. Repeated squaring, small violations, and nonconvex zero-multiplier large-penalty examples are prior. Qualified novelty is restricted to the exact optimized-dual formula in the compact, one-binary-variable convex-quadratic family with uniform strict points and its fixed-accuracy consequence. The lower bound is exponential in chain length/continuous dimension, only superpolynomial in total sparse input length; no matching rate in total input length is claimed. |
| Upper bounds in continuous dimension and nonlinear count | Basu–Roy, Theorems 3–4; Basu–Pollack–Roy, Theorem 14.16; Grigoriev–Pasechnik, Theorem 1.2; Kamminga–Rudolph, full-version §§6.3–7.2 and 8.5; Gu–Ahmed–Dey, Theorem 11; Lefebvre–Schmidt, Theorem 15 | Radius and elimination estimates, few-quadratic methods, and polyhedral-case conservative output are credited as existing results. Qualified novelty concerns the derived exact-penalty bounds for the explicitly boxed convex-slice model, including arbitrary affine rows with a bounded count of nonlinear native inequalities. There is no claim of a practical coefficient-selection algorithm. |
| Calibration inapproximability | Alessandroni et al. 2025, §IV.A, Lemma 1; Mirkarimi et al., §2.2; Alessandroni et al. 2026, Definition 1 and Theorem 2; EXPEDIS, §§5–6 | Generic penalty-choice hardness, including known constrained optima, and conservative upper bounds are prior. The restricted claim is polynomial-factor inapproximability of an always-positive optimized-dual norm threshold on a binary box with a linear objective, one equality, known unique primal optimizer and known sufficient coefficient. The zero-multiplier consequence is also stated. No strong-hardness claim is made for that binary-box reduction. |
| Finite-grid perturbation result | Dunagan–Spielman–Teng, Theorem 2.3.3 and Lemma 2.3.4; Bürgisser–Amelunxen, Theorem 3.3 and Corollary 3.4; Friedlander–Tseng, Theorem 4.2 | Convex-boundary avoidance, Gaussian tube bounds and multiplier/penalty relations are prior. The contribution is the stated finite-grid exact-penalty application with precision, encoding, feasibility and perturbed-problem qualifications. No separate priority claim is made for the geometry or convex repair. |
| Supporting residual geometry | Boland–Eberhard, primal characterization and Corollary 1; Feizollahi–Ahmed–Sun, Theorem 1 | These supply direct augmented-dual convexification precedents. The manuscript gives a compact residual-space proof without an attainment assumption and explicitly does not claim novelty for convexification. |

The original local PDFs for Gu, Bhardwaj and Beck were read during this
revision using `pdftotext -layout ... -`; the lead also checked the current
primary versions and the other direct comparisons above against the
sources documented in the existing stage source records. In particular,
Bhardwaj–Narayanan–Pathapati, arXiv:2209.13326v2 (February 7,
2024), Theorems 3.1–3.2 give existence proofs and data-dependent penalty
parameters for MILPs and MIQPs; their construction uses value functions.
Theorem 3.3 gives an explicit bound under strong convexity and smoothness
for a nonlinear objective with polyhedral constraints. The revised
introduction distinguishes these claims rather than describing all of
them as explicit analytic bounds. The bibliography identifies this
inspected version and the published DOI 10.1137/22M1526204. The inspected local Lefebvre–Schmidt text, conclusion on printed
p.24, explicitly asks both the smallest-penalty and quadratic-encoding
questions. The current online PDF remains dated December 15, 2025.

## Newly added primary references

- Boland–Eberhard, *On the Augmented Lagrangian Dual for Integer
  Programming*: author manuscript posted January 2013,
  <https://optimization-online.org/wp-content/uploads/2013/01/3738.pdf>.
  Corollary 1, printed p.6, gives finite-penalty exactness for finite X;
  Theorem 1 gives a primal characterization. Both the lead and writer
  opened the primary PDF. The writer verified published volume 150,
  pp.491–509 (2015) and DOI 10.1007/s10107-014-0763-3 at the publisher
  <https://link.springer.com/article/10.1007/s10107-014-0763-3>.
  The main-text citation deliberately claims no norm-specific extension
  beyond this source's assumptions.
- Feizollahi–Ahmed–Sun, *Exact Augmented Lagrangian Duality for Mixed
  Integer Linear Programming*: inspected author manuscript submitted
  August 13, 2015,
  <https://www2.isye.gatech.edu/~xsun84/publications/EALD_optimizationonline.pdf>.
  Theorem 1, printed p.10, uses a lifted convex hull under a
  relative-interior feasibility condition; Theorem 4, p.19, proves norm
  exactness for rational MILPs. Proposition 8, p.21, treats each fixed
  multiplier, and Remark 4, p.20, treats strict increases of the penalty.
  The lead read these statements and the writer independently read the
  lifted characterization. Publisher metadata at
  <https://link.springer.com/article/10.1007/s10107-016-1012-8> confirms
  Mathematical Programming 161, pp.365–387 (2017).
- Gusmeroli–Wiegele, *EXPEDIS: An Exact Penalty Method over Discrete Sets*:
  <https://arxiv.org/pdf/1912.09739v4>. The primary arXiv version record
  identifies v4 as posted January 3, 2021; the PDF title date is January
  5, 2021. Sections 5–6, especially Lemma 6 and Proposition 8 on printed
  pp.9–10, derive sufficient squared penalties from objective bounds
  and positive residual separation. The lead read the primary PDF;
  the writer independently checked Proposition 8 and its surrounding
  discussion. The claim is conservative sufficiency, not that this
  source computes the least norm-augmented dual threshold. Published
  metadata were verified through Crossref's primary DOI registration
  API, <https://api.crossref.org/works/10.1016/j.disopt.2021.100622>:
  Discrete Optimization 44, article 100622, May 2022. The API failed
  through the browser tool but succeeded through Python urllib. Direct
  ScienceDirect opens failed; no failed retrieval supported a claim.

Primary PDFs obtained through the browser were not redistributed or
added to the repository. Existing local literature packages were read
without modification.

## Search coverage and limits

The lead and writer searched online with combinations of:

- exact augmented Lagrangian / exact penalty + binary encoding, encoding
  length, quadratic constraints, bit complexity, double exponential;
- penalty + fixed number of quadratic constraints + encoding;
- penalty parameter / smallest penalty + NP-hard, coNP, polynomial
  factor, approximation, inapproximability;
- exact penalty + smoothed analysis, and penalty + smoothed + mixed integer.

These searches returned the direct sources compared above and adjacent
application papers, but no additional theorem establishing the same
restricted encoding or calibration conclusions. This is bounded search
evidence, not proof of absence. Consequently the manuscript uses two
explicit “To the best of our knowledge” qualifications for encoding
claims and a similarly bounded calibration comparison; it makes no
first-ever claim.

The local García–Ayodele–Moraglio 2022 package is metadata-only. The lead
tried the discovered Exeter primary URL
<https://ore.exeter.ac.uk/rest/bitstreams/185242/retrieve>; the browser
returned an error and urllib returned zero bytes. No full-text theorem
claim or absence claim relies on that unread source. New 2026 search
hits about double-integrator thresholds and slack-free HUBO penalties
address other models; only their primary abstracts were screened, and
no substantive comparison to their unread full texts is asserted.


## Comparisons clarified after review

The upper bounds are existential bounds on a sufficient integer
coefficient for the infinity and one-norm penalties. The nonlinear-count
bound is a second bound, not a uniformly smaller bound for all parameter
values. The finite-grid coefficient uses the infinity norm and requires
convex slice objectives and affine residuals. Its probability concerns
one sample, not a deterministic proportion in any finite run of samples.

Boland–Eberhard's author manuscript assumes a restricted augmentation
class (its condition (3), printed p.3, has superlinear growth). The
introduction therefore separates its bounded pure-integer exactness
result under those assumptions from Feizollahi–Ahmed–Sun's norm result.
The compact residual-space characterization here needs no
relative-interior hypothesis; the comparison does not claim that the
Feizollahi–Ahmed–Sun theorem assumes multiplier attainment.

The lead also screened Kleinert et al.'s primary Optimization Online
abstract, <https://optimization-online.org/2019/04/7172/>: its hardness
concerns two validity tests for big-M coefficients in bilevel KKT
reformulations. The local Ketkov–Prokopyev arXiv:2603.17107, pp.10–12,
uses exact penalization in a reduction and proves coNP-completeness of
posterior bilevel verification. These are adjacent coefficient or
verification questions, not results about the least optimized-dual norm
penalty studied here. Neither was added as a direct theorem predecessor;
the manuscript already credits generic penalty-choice hardness.

The Claude review automatically cached four fetched primary PDFs outside
the paper folder. The writer moved only those four identified files from
`/home/sgusev/.claude/projects/-home-sgusev-repo-minlp-notes/17600d7f-d70a-4712-994b-4c9bc9d9ac31/tool-results/`
into the ignored `paper-exact-penalties/evidence/sources/` directory:
`webfetch-1790546466829-wf7ohi.pdf`,
`webfetch-1790546469936-j63p5m.pdf`,
`webfetch-1790546474680-8io7mn.pdf`, and
`webfetch-1790546740446-qlld7d.pdf`.
No other cache files were changed, and these PDFs will not be committed.
