# Stage 6, round 1 — review 05

I reviewed the entire introduction and Section 6, with extra attention to the dense-slab reduction, fixed-coefficient padding, NP certificates, and the distinction between abstract and physical hardness. Both manuscript files matched the frozen round snapshots byte for byte at completion. I followed `process/reviewer-protocol.md` and `literature/AGENTS.md`. I did not inspect other reviewers' reports or edit the manuscript.

**Findings: none.** I found no major or minor defect requiring correction in the reviewed material. The following records the mathematical checks and their limits; it is not an inference from earlier PASS labels.

## Main proof checks

| Manuscript location | Assessment |
|---|---|
| `06-synthesis.tex:11–63`, endpoint certificate | Expanding the weighted products cancels every intermediate square and gives the stated coefficients. Positivity of each weight and separation of the conditional endpoints make the zero set exactly the endpoint vertices. The inverse terminal recursion proves distinct terminal values. The exposing inequality has the correct maximizing sign. |
| `06-synthesis.tex:66–182`, physical response | Capacity gives the lower strip inequality and midpoint upper quality gives its upper inequality. The scaling, relay reset equation, supply sequence, and objective coefficients are consistent. In the penalty argument the only relaxed violations are contract deficits; clearing the midpoint row gives coefficient bound one. The Section 3 error bound therefore gives `H=N^N`, and `M=3H+1` works uniformly over the whole price interval. The two revenue bonuses count source and reset throughputs exactly. |
| `06-synthesis.tex:184–241`, description and coordinate-port bounds | Every exposed vertex persists over an interval; distinct terminal values give distinct affine response slopes. The line-factor proof applies to both graph and epigraph boundaries and concerns total degree in price and value alone. Backward elimination has the stated absolute-value recurrence. Fourier–Motzkin elimination preserves two-variable row support, and the three-dimensional simplex counterexample correctly excludes individual coordinate-port universality. |
| `06-synthesis.tex:243–336`, nonlinear interface and strict local maxima | All interface flows and the active quality follow uniquely from terminal flow and clean flow. The remaining quality row is exactly `z >= t-t^2`. The economic shift preserves profit by total mass conservation. The perturbation adds exactly `delta*t`; the rational terminal spacing makes every directed edge derivative strictly negative. The tangent-cone argument then establishes strict local maximality, including transfer to the clean-flow direction. |
| `06-synthesis.tex:338–442`, parity, LP hull and extensions | Pairwise midpoint exclusion gives the parity lower bound even with unbounded integer coordinates. Binary labeling gives the matching upper bound without a formulation-size claim. The lower affine hull boundary is the convex combination of vertex graph points, and every hull vertex is physical. The relay economics and arbitrary strictly growing supply identity preserve this argument. The example after deleting the lower throughput bound is feasible and has profit `3/16`. |
| `06-synthesis.tex:452–491`, dense slab and padding | Both reduction directions, the nonempty-domain promise, endpoint certificates, and all encoding bounds are valid; details below. |
| `06-synthesis.tex:507–651`, interaction rank and specialization | Double centering gives the least residual cost rank. Projected-box enumeration retains original box witnesses and remains polynomial for fixed projected dimension. A slice vertex lies on an original edge or vertex, so enumerating all vertex pairs is sufficient; extra segments remain feasible. Candidate objectives have the stated `alpha*S+beta+gamma/S` form. Stationary-point signs, singleton totals, zero total, common-field recovery and comparison bounds are correct. The signed rank-one specialization correctly uses all four pairs of scalar extrema. |
| `06-synthesis.tex:653–737`, oracle and arithmetic boundaries | Quality multipliers add an interaction matrix of rank at most the attribute count, with row/column additive terms removed. The supplied approximation gives the stated twice-error bound. The rank-one matrix-perturbation sign disjunction is exact also at zero signal and gives rational recovery. The source rank-two columns have independent supports. Convex singleton leaves encode Square-Root Sum exactly; no NP-hardness conclusion is drawn. |

## Detailed slab and certificate audit

At `06-synthesis.tex:463–476`, positive integer weights give `W>=1` and hence an admissible rational `epsilon=1/(8W)`. At each endpoint vertex, `|x_i-u_i|<=epsilon`; consequently the weighted perturbation is at most `1/8`. A subset-sum solution is inside the slab, while any point of objective at most zero must be an endpoint vertex and yields an integer subset sum within `3/8` of `B`. This proves both directions without needing a gap estimate.

For the nonemptiness promise, the all-one-bit endpoint vertex has weighted sum at least `W-1/8`. If `B<W`, integrality gives `B<=W-1`, so the segment from zero to that vertex reaches `B`. If `B=W`, that endpoint itself meets the slab. Compactness follows from the path box. This reasoning also covers `B=0` and one-variable instances.

The direct NP witness consists of endpoint bits. Rational recursion has polynomial bit length, and slab membership is an exact rational check. This argument is stronger and simpler for this restricted problem than invoking general nonlinear certificates; it does not claim rational optimizers for unrelated pooling models.

At `06-synthesis.tex:478–490`, a padding coordinate cannot take the upper endpoint because that endpoint is at least `3/4`, whereas the new bound is `1/2`. Every assigned free-bit vector therefore has one admissible zero extension, obtained by lower branches at all padding coordinates. The effective predecessor factor between successive free coordinates is `4^{-(r+1)}`, including the step into the next free coordinate. The first free coordinate is its bit exactly. The same weighted error and nonemptiness arguments apply. Dimension `N=n+(n-1)r` is polynomial since `r=O(log W)`, and coefficients in the full certificate have `O(N)` bits. Only the local path coefficients are fixed: the slab and objective retain binary data. The statement properly withholds strong hardness and an inverse-polynomial gap.

At `06-synthesis.tex:493–503` and `859–927`, the interpretation preserves the dense slab and dense linear part of the nonlinear certificate. Fixing `x_n` does leave a bounded LP fiber, but the leaves remain coupled. The manuscript expressly lacks a physical realization of the slab. Its bare-path linearization is valid because a concave objective has a vertex minimizer and the certificate agrees with the square at all original vertices. Thus the abstract reduction does not contradict the physical family’s LP hull or establish the open degree-two physical classification.

## Introduction, adjacent results and sources

The abstract, contribution paragraphs, table and roadmap agree with the scoped statements checked in Sections 2–5. In particular, the certificate row uses basis indices rather than rational-optimum claims; product-degree hardness distinguishes threshold decision from feasibility with positive contracts; fixed exceptions retain redundant common bounds; the restrictive-capacity result remains fully contracted and of quality rank at most one; and the two-vector result remains a feasibility statement with its zero lower-bound restrictions. I checked the relevant accepted theorem statements and the Section 3 Hoffman proof, rather than re-proving all accepted stages.

For `06-synthesis.tex:739–857`, I compared the claims with the canonical rank-one margin, correlation-face, stability, approximate SDP, common-factor, reciprocal-anchor, integer-anchor, network–simplex, parallel-path, cycle/theta and power-flow result files. The margin theorem retains nonadditive matrix costs. The correlation face follows by trace equality, pair exclusion and then total-mass maximization. The approximate LP and SDP bounds retain their distinct source mechanisms, norms, constants and cone-size conventions. The common-factor summaries exclude extra original-point linking restrictions in the anchor hulls. The network summaries distinguish compact extended hulls from original-space coefficients, and parallel-path blocks from general series–parallel graphs. Power-flow scope retains real-angle semantics.

Primary-source checks included:

- `[[gartner2013-large-shadows-from-sparse-inequalities]] p.8-9`: checked the original PDF’s direction and exposing proof. Its parameter formula has absolute value bounded by the finite geometric sum below `1/15` at `epsilon=1/4`.
- `[[lubin2022-mixed-integer-convex-representability]] p.12`, Section 4.2: checked the midpoint/parity argument against the manuscript’s application.
- `[[punnen2015-the-bipartite-unconstrained-01-quadratic]] p.8-15`, Sections 3.2–3.3, and [Hladík, Černý and Rada’s author page](https://kam.mff.cuni.cz/~hladik/publ/b2hd-HlaCer2021c.html): the cited box and zonotope precedents support the qualified comparison.
- [Pardalos–Vavasis publisher abstract](https://link.springer.com/article/10.1007/BF00120662): confirms the prior concave quadratic hardness with one concave direction; I did not obtain its subscription full text.
- [Boveroux et al. preprint](https://orbi.uliege.be/bitstream/2268/345162/1/OntheComplexityofLinearProgramswithparametricConstraintMatrices.pdf), PDF pp.5–6 and 10–11: checked the two perturbation columns and one-column comparison. The manuscript uses its independently bounded positive-product source rather than relying on unqualified source claims.
- [Grothey–McKinnon preprint](https://arxiv.org/pdf/2002.10899), PDF pp.9–10: confirms the three-bin, two-nutrient geometric example used for the limited comparison.
- Original PDFs of `[[fawzi2013-exponential-lower-bounds-on-fixed]] p.3`, `[[lee2015-lower-bounds-on-the-size]] p.23` and p.32: checked the fixed-block/SOC transfer and the quantitative pseudo-density ingredients against the canonical notes.

## Reproducible finite checks

I reran the following existing scripts with `/home/sgusev/miniconda3/envs/minlp-notes/bin/python`. All exited successfully:

```text
code/parametric_path_lp/exact_rank_one_slab_check.py
PASS: 2246 exact identity/positivity/tangent checks through dimension10.
PASS: 661 subset-sum targets from 28 weighted instances through dimension7.
PASS: 1016 padded vertex identities and 661 fixed-coefficient slab targets.

code/parametric_path_lp/exact_fixed_alphabet_check.py
PASS: 252 exact positive dual certificates; two input qualities, upper flows/qualities only.

code/parametric_path_lp/exact_strict_local_check.py
PASS: 2044 distinct local-optimum values and 18432 exact negative directed-edge derivatives.
```

These are exact rational checks of finite families and corroborate the written arguments. They are not proofs for all dimensions, a new independent implementation, or a numerical global-optimization certificate.

**Verdict: no findings.** This is a complete reading of the new introduction and Section 6 with the proof and scope checks described above. Limits: I did not conduct a comprehensive novelty search, re-audit every theorem in accepted Sections 1–5, reproduce every adjacent standalone proof from first principles, or run a manuscript build. Root owns builds. No claim of exhaustive correctness or external-review acceptance is made.
