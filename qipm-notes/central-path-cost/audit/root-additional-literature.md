# Additional primary-source screen during staged writing

Root search on 2026-09-07: central path / Riemannian distance / logarithmic
box barrier / spectral geodesic / Lorentz length. Search results do not
establish absence of prior work.

- Ohara, Atsumi; Ishi, Hideyuki; Tsuchiya, Takashi. *Doubly autoparallel
  structure and curvature integrals: Applications to iteration complexity
  for solving convex programs*. Information Geometry 7 (2024), 555–586;
  first online 27 July 2023. DOI 10.1007/s41884-023-00116-x.
  Primary publisher full text inspected, especially sections 4–5:
  https://link.springer.com/article/10.1007/s41884-023-00116-x
  Their section 4.2 defines conjugate Hessian metrics and the gradient-map
  isometry; section 4.3 explicitly gives metric-orthogonal projections onto
  primal/dual affine tangent spaces. Section 5 develops a geometric
  predictor-corrector algorithm and curvature-integral complexity.
  These are additional antecedents for projection calculus and geometric
  algorithm claims, not evidence of the present ordered-profile endpoint
  ratio or target-allocation constant. Do not present metric projections
  or Hessian-gradient isometry as new. The paper also characterizes Jordan
  doubly autoparallel submanifolds, a different geometric question from
  the bounded-interval real Hessian distance here.
- Iusem, Alfredo N.; Svaiter, B. F.; da Cruz Neto, João Xavier.
  *Central Paths, Generalized Proximal Point Methods, and Cauchy
  Trajectories in Riemannian Manifolds*. DOI 10.1137/S0363012995290744.
  Publisher abstract inspected:
  https://epubs.siam.org/doi/10.1137/S0363012995290744
  Establishes relationships among barrier central paths, Bregman proximal
  sequences, and Riemannian gradient trajectories. Do not rely on search
  engine publication dates; verify bibliographic year/volume before citing.
  Abstract-level use only until full text is inspected.

Potential relevant citation chain from the Ohara–Ishi–Tsuchiya full text:
Kakihara–Ohara–Tsuchiya, JOTA 157 (2013), 749–780; COAP 57 (2014),
623–665; Monteiro–Tsuchiya, Math. Program. 115 (2008), 105–149.
These concern curvature integrals and predictor-corrector iteration
complexity. They require primary-text review before detailed comparison.

## Direct prior result requiring explicit credit in stage 4

Nesterov–Todd (2002), Theorem 5.1(c) and Corollary 5.1, already pass from
same-central-endpoint comparison to the **entire feasible small-gap set**.
Corollary 5.1 expressly states short-step optimality for traveling to that
set. The text also allows intermediate points to violate the affine
equations. Thus the general gap-set lower bound and endpoint-set inference
must be presented as a quantitative restatement/consequence of their work,
not as a new extension. The paper's contribution in that part must rest on
the explicit same-LP three-scale comparison, primal speed allocation, and
any separately verified support-rank formulation result.

Lorentz's original primary article is available at
https://msp.org/pjm/1951/1-3/pjm-v1-n3-p07-s.pdf
(Pacific J. Math. 1(3), 411–429, DOI 10.2140/pjm.1951.1.411).
Its weighted decreasing-rearrangement norm is the appropriate classical
antecedent of the prefix inequality. Sharpness as a central-path ratio is
a separate claim requiring the present translated-profile construction.

## Barrier and finite-sequence literature found during stage 3

- The cube lower bound `nu >= dimension` is NN1994, Proposition 2.3.6.
  Its precise attribution is confirmed in the primary Lee–Yue paper
  https://optimization-online.org/wp-content/uploads/2018/09/6810.pdf
  and Bubeck–Eldan preprint
  https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/1412.1587.pdf.
  Verify the book text if a detailed formulation is quoted.
- Lévy, Lucas; Valeau, Jean-Lou; Akhavan, Arya; Rebeschini, Patrick.
  *Self-Concordant Perturbations for Linear Bandits*, arXiv:2510.24187v3,
  revised 26 June 2026. Primary section 6.1 explicitly uses the cube entropic
  barrier's separable gradient `coth(t)-1/t` and its optimal parameter.
  https://arxiv.org/html/2510.24187v3
  This is additional evidence against claiming the factorization itself
  as new. Their problem is adversarial linear-bandit regret, not the
  central-path/shortest-route ratio considered here.
- Allamigeon, Xavier; Dadush, Daniel; Loho, Georg; Natura, Bento;
  Végh, László A. *Interior point methods are not worse than Simplex*.
  arXiv:2206.08810v4, revised 19 February 2025.
  https://arxiv.org/html/2206.08810v4
  Primary introduction, Definition 1.3, Theorem 1.7 and section 10 inspected.
  They compare their algorithm with piecewise-linear paths in wide
  neighborhoods for arbitrary self-concordant barriers, within a factor
  `O(n^(3/2) log(n theta_f/(1-theta)))`. Their straight-line complexity
  counts affine segments and is not the same resource as bounded local
  Hessian moves or Riemannian distance. This is essential context for the
  manuscript's finite-sequence and barrier-choice discussion. Do not claim
  generic first comparisons against other path-following methods.
  Their reference [3] is Allamigeon–Gaubert–Vandame, STOC2022, pp515–528,
  *No self-concordant barrier interior point method is strongly polynomial*.
  Their reference [15] gives Chewi's published exact-n entropic chapter:
  *Geometric Aspects of Functional Analysis: Israel Seminar (GAFA)
  2020–2022*, pp209–222, Springer2023 (verify publisher DOI for bibliography).
# Additional targeted screen during stages 3--4

**Published-version metadata update:** *Interior Point Methods Are Not Worse than Simplex* is now published: Xavier Allamigeon, Daniel Dadush, Georg Loho, Bento Natura and László A. Végh, SIAM Journal on Computing **54(5)** (2025), **FOCS22-178--FOCS22-264**, DOI **10.1137/23M1554588**. Primary publisher https://epubs.siam.org/doi/abs/10.1137/23M1554588 confirms online publication March 3, 2025, issue October 2025. Prefer this article entry over the earlier arXiv-only entry; the inspected arXiv v4 remains the open full-text locator. Its straight-line complexity comparison is essential related work, with a different counted resource from this paper's fixed-radius local-Hessian movement.

Primary author PDF https://www.cas.mcmaster.ca/~deza/mp2008.pdf verifies Deza--Nematollahi--Terlaky, *How good are interior point methods? Klee--Minty cubes tighten iteration-complexity bounds*, Mathematical Programming **113** (2008), **1--14**, DOI **10.1007/s10107-006-0044-x**. The published Allamigeon et al. 2025 article's references also verify Allamigeon--Gaubert--Vandame, STOC2022 pp515--528; DOI10.1145/3519935.3519997 can be checked against its arXiv primary record. Use those works for prior path-following lower-bound mechanisms, not as sources for the new Hessian-distance ratio.

Root searched the exact combinations `central path` / `subgeodesic` / `Lorentz space` / `sqrt(log` / `Riemannian cube`, and `Busemann principal minor`, `Riemannian exposed rank`, and `log determinant distance duality gap`. These searches again returned NT2002, NN2008, Papa Quiroz--Oliveira2007, Permenter2023 and Ohara--Ishi--Tsuchiya2024 as the closest inspected optimization sources. They did not locate a primary theorem identical to the manuscript's exact Gamma constant, full dyadic finite-sequence synthesis, or explicit radial-family comparison. This is a targeted negative search, not a priority certificate.

The search also surfaced Yukun Du's *Completeness of partial domains* manuscript on an institutional site, with classical Busemann functions expressed through principal minors in its Proposition 3.1, citing Hattori1995. Direct full-document web access failed, so this search excerpt is not used as a supporting citation. It reinforces the conservative decision to avoid claiming the support-minor/Busemann identity as original and to give a self-contained Jordan proof of the optimization consequence. No assertion from that inaccessible document is used in a theorem.
