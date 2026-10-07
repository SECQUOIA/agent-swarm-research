# Attribution and contribution assessment

Checked on 2026-10-02. The continuation develops a reproducible solver
component from established convexification methods. The literature does
not support presenting simultaneous convexification, exact low-dimensional
quadratic hulls, or rigorous Bernstein bounds as discoveries of this work.
The contribution to assess is the complete implemented contract: supported
block discovery, bounded separation work, exact final-cut validation,
replay, and measured solver behavior.

This is a focused comparison against the actual additions. It is not an
exhaustive literature review and does not establish publication priority.
Links below are primary articles, author manuscripts, institutional
records, or official solver documentation. Earlier repository notes are
identified separately when their underlying source could not be recovered.

## Closest sources and their implications

| Addition being assessed | Closest established result | Claim permitted here |
| --- | --- | --- |
| Scalar and vector univariate support cuts | Ballerstein; Liers et al.; He and Tawarmalani; Li et al. | Concrete supported expression class, numerical contract, and implementation results |
| Polynomial cuts from Bernstein bounds | Garloff, Jansson and Smith; Garloff and Smith; polynomial RLT | Checked coefficients and complete domain coverage in the implemented certificate format |
| Simultaneous quadratic graph on a polygon | Anstreicher and Burer, Theorem 7 | Exact rational support implementation and use in automatically extracted blocks |
| Combining overlapping block hulls | Tawarmalani's common inclusion certificates; Lasserre's consistent marginal measures | Explicit obstruction for the proposed weak interface and a demonstrated remedy for a specified class |
| Choosing when to separate | Existing solver cut management; RLT filtering; recent axis-aligned relaxation implementation | A stated activation heuristic and its measured costs and outcomes |
| Improved solver performance | Native nonlinear handlers, projected bilinear envelopes, RLT and SDP cuts | Only the improvements actually established by the frozen comparative experiments |

### Simultaneous support separation

[Liers et al. (2021)](https://optimization-online.org/wp-content/uploads/2020/02/7628.pdf),
*Solving mixed-integer nonlinear optimization problems using simultaneous
convexification: a case study for gas networks*, Journal of Global
Optimization 80(2), 307–340, DOI 10.1007/s10898-020-00974-0. Proposition 1
attributes the linear-combination characterization of the simultaneous
graph hull to Ballerstein (2013); Section 3 develops separation from those
combinations. Their application uses bivariate quadratic absolute-value
functions. The report's direction search plus a scalar support oracle is
therefore an implementation of established simultaneous separation.
The retained author version is dated September 16, 2020; its Section 3,
pp. 6–9, was inspected in the existing local full text.

[Tawarmalani (2010)](https://optimization-online.org/wp-content/uploads/2010/09/2722.pdf),
*Inclusion Certificates and Simultaneous Convexification of Functions*,
Optimization Online manuscript. Corollary 2.7 handles simultaneous
multilinear functions using extreme domain points. Definition 3.4 and
Corollary 3.9 explain compatibility through measures realizing individual
envelopes. Individual hulls do not automatically combine to the joint
hull. These passages were inspected in the retained local full text,
pp. 5–6 and 12–16. Here an inclusion certificate is a mathematical
representing measure; it is distinct from this implementation's serialized
cut-validation artifact.

[Ballerstein (2013)](https://doi.org/10.3929/ethz-a-009959194),
*Convex Relaxations for Mixed-Integer Nonlinear Programs*, ETH dissertation
21024, is the principal older univariate-vector reference. The
[earlier audit](../../notes/shared-variable-terms-literature.md) records
Chapter 5 hulls, separators, and experiments. Its original PDF was not
retained. The institutional download returned HTTP 429 in this
continuation; that failure is recorded in
[the source manifest](sources/MANIFEST.md). The historical
details should retain that provenance. Liers et al. independently
corroborates the general hull characterization, but does not verify every
Chapter 5 algorithm or computational claim.

The [composition audit](composition-audit.md) inspects the primary texts
of He and Tawarmalani (2021, 2022, 2024), Zhu, He and Tawarmalani (2026),
and Li et al. (2026). These sources already cover vector outer functions,
simultaneous graph or hypograph relaxations, shared discretization,
coupled-domain approximation, and exact scalar polynomial envelopes under
their respective hypotheses. They preclude a broad first-method claim.

### Bernstein bounds and validated coefficients

[Garloff and Smith (2008)](https://www-home.htwg-konstanz.de/~garloff/rigorous.pdf),
*Rigorous Affine Lower Bound Functions for Multivariate Polynomials and
Their Use in Global Optimisation*, Lecture Notes in Management Science 1,
199–211. Section 2 states the Bernstein control-point enclosure; Section
5, manuscript pp. 8–9, computes interval coefficients, chooses an affine
candidate in ordinary floating point, and shifts it rigorously using the
coefficient lower bounds. Thus both Bernstein affine bounds and the
separation of numerical proposal from rigorous validation are prior art.
The present tree-based, model-bound replay format is an implementation
contract to demonstrate, not evidence of a new general validated-bounds
principle. [Source manifest](sources/MANIFEST.md).

[Garloff, Jansson and Smith (2003)](https://tore.tuhh.de/entities/publication/c91b3a23-8be6-40a5-8633-afae480ee8ae),
*Inclusion isotonicity of convex-concave extensions for polynomials based
on Bernstein expansion*, Computing 70(2), 111–119, DOI
10.1007/s00607-003-1471-7. The institutional abstract explicitly states
that shrinking the domain shrinks the Bernstein control hull, including
multivariate polynomials on boxes. This entry was checked at
abstract/metadata level only. It supports attribution of monotone
subdivision; the implementation's precise tree-coverage and rational
arithmetic claims require its own proofs and checks.

[Sherali and Tuncbilek (1997)](https://doi.org/10.1016/S0167-6377(97)00013-8),
*New reformulation linearization/convexification relaxations for
univariate and multivariate polynomial programming problems*, Operations
Research Letters 21(1), 1–9. Sections 2–3 include relations between powers,
linearized bound-factor products, constraint-factor products, and
selection based on coefficients. The retained user-supplied full text was
inspected. Polynomial dependencies and selective generation are already
established ideas. A Bernstein support bound should be compared with
applicable RLT constraints; a cut cap or sign-based trigger alone is not a
new mathematical selection result.

[Johansson (2017)](https://fredrikj.net/math/arbpaper.pdf),
*Arb: Efficient Arbitrary-Precision Midpoint-Radius Interval Arithmetic*,
IEEE Transactions on Computers 66(8), 1281–1292, DOI
10.1109/TC.2017.2690633, is the numerical-library reference for the
elementary-function path. The author abstract and official citation
metadata were checked. Using ball arithmetic is established practice;
the continuation must still verify its input conversion, domain handling,
full interval coverage, and export of the final coefficients.

### Exact quadratic graphs and overlap

[Anstreicher and Burer (2010)](https://optimization-online.org/wp-content/uploads/2007/02/1586.pdf),
*Computable representations for convex hulls of low-dimensional quadratic
forms*, Mathematical Programming 124, 33–43, DOI
10.1007/s10107-010-0355-9. The inspected February 6, 2007 preprint gives
the simplex hull in Theorem 3 (p. 4), triangles/tetrahedra in Corollary 4
(p. 5), the two-dimensional box hull as PSD plus RLT in Theorem 6
(p. 7), and triangulated polytopes of dimension at most three in Theorem
7 (p. 9). Its pp. 3–4 state the equality of completely positive and doubly
nonnegative cones through order four. The proposed polygon/DNN hull is a
direct specialization, including its vector-quadratic projection.
Exact stationary-point enumeration is the simpler support implementation;
it does not create a new hull theorem. [Source manifest](sources/MANIFEST.md).

[Lasserre (2006)](https://optimization-online.org/wp-content/uploads/2006/04/1367.pdf),
*Convergent SDP-Relaxations in Polynomial Optimization with Sparsity*,
SIAM Journal on Optimization 17(3), 822–843, DOI 10.1137/05064504X.
Lemmas 6.3–6.4 glue measures with matching overlap marginals under the
running intersection condition. The convergence proof uses moment
determinacy on compact sets to obtain this agreement. Matching a finite
list of overlap moments is not the same condition. Theorem 3.7 gives
additional rank conditions for finite extraction. The continuation's
example is an explicit regression against a weaker proposed interface,
not a refutation of sparse moment convergence. [Source manifest](sources/MANIFEST.md).

[Lasserre (2001)](https://doi.org/10.1137/S1052623400366802),
*Global Optimization with Polynomials and the Problem of Moments*, SIAM
Journal on Optimization 11(3), 796–817, supplies the general moment/SOS
comparison. Its Theorem 4.2 gives hierarchy convergence under its
Archimedean condition; finite exactness needs additional structure.
The retained primary full text was inspected. Local polynomial support
cuts offer a smaller LP interface, while higher-order moment relaxations
retain relationships that the chosen finite blocks may miss. No general
dominance between the implemented bounded cut loop and all such
relaxations is established.

The [star support audit](star-overlap.md) records the direct relationship
to forest quadratic programming and the distinction between box-only and
row-coupled leaf domains. Its attribution applies to the promising star
extension as well as the initial pairwise blocks.

### Baselines already available in solvers

[Bestuzheva et al. (2025)](https://arxiv.org/abs/2301.00587),
*Global optimization of mixed-integer nonlinear programs with SCIP 8*,
Journal of Global Optimization 91(2), 287–310, DOI
10.1007/s10898-023-01345-1. The inspected longer arXiv v1 is from January
2023. Section 2.1.3 defines nonlinear handlers; Sections 2.3.2–2.3.4
describe projected-domain bilinear estimates, RLT, and detected 3-by-3
moment-matrix minors. Other handlers recognize convexity, SOC forms, and
special quotients. Automatic structure recognition is therefore an
existing solver capability. In particular, improvement over independent
McCormick inequalities can reproduce strength already available from
native SDP/RLT separation. [Source manifest](sources/MANIFEST.md).

[Müller, Serrano and Gleixner (2020)](https://arxiv.org/abs/1903.05521),
*Using Two-Dimensional Projections for Stronger Separation and Propagation
of Bilinear Terms*, SIAM Journal on Optimization 30(2), 1339–1365, DOI
10.1137/19M1249825. The primary abstract and SCIP's detailed account were
checked. Their method obtains valid two-variable inequalities through LP
projections and uses them for stronger bilinear envelopes and bound
propagation inside SCIP. This directly anticipates automatic exploitation
of linear coupling for an individual product. The continuation's full
quadratic vector must be distinguished from that individual-product
scope; comparisons should preserve the native baseline.

[Locatelli (2018)](https://doi.org/10.1007/s10898-018-0626-1),
*Convex envelopes of bivariate functions through the solution of KKT
systems*, Journal of Global Optimization 72(2), 277–303, is the envelope
source cited by SCIP's bilinear handler. The paper's full text was not
downloaded in this continuation; the attribution is independently visible
in [official SCIP documentation](https://scipopt.org/scip/doc/html/group__NLHDLRS.php).
We do not infer a new bivariate-envelope theory from using a different
support implementation.

## Corrections and precise contribution language

The earlier shared-variable audit's Section 2.4 incorrectly said that the
He–Tawarmalani 2021/2022 abstracts omit vectors of outer functions. Both
explicitly cover them, and the full texts contain substantive vector
results. The [composition audit](composition-audit.md) supplies the exact
locations. That historical paragraph was corrected in this continuation.
Any remaining older first-method wording should be replaced by a claim
about the implemented function class and evidence.

For the integrated document, use the following distinctions:

- A mathematically exact support oracle does not mean that a budgeted
  numerical direction search separates every point outside the hull.
- A certificate for a cut proves that cut's validity on its stated model
  and domain. It does not certify the solver's whole search or final
  optimality gap.
- A replay routine sharing the producer's exact geometry is independently
  callable, but is not an independently implemented or formally verified
  checker.
- A deterministic activation rule controls work. A guarantee that it
  improves total runtime needs separate evidence and is not supplied by
  validity or convergence proofs.
- Report new experimental outcomes separately from inherited historical
  curves, synthetic examples, source-paper experiments, and native solver
  guarantees.

The [bibliography](references.bib) records exact citation identities and
version caveats. The local source ledger records file hashes and read
scope. Primary PDF retrieval, `pdftotext -layout` extraction, passage
inspection, bibliography-key checking, and hash checking are targeted
literature checks. No project-wide verification or CI inspection is part
of this audit.
