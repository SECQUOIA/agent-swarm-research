# Publication assessment: encoding and calibration of exact norm penalties

Date: 2026-09-25. Scope: the September 25 penalty results. This is a
research handoff and claim audit, not a manuscript or a guarantee of
publication priority. It distinguishes the completed mathematical claims
from questions that would require new research.

The most coherent contribution is an **encoding boundary for exact norm
penalties in compact convex mixed-integer quadratic models**. The explicit
one-binary lower bound is the main construction. The general encoding
upper bound and its fixed-quadratic-count refinement explain how far that
obstruction can extend. The minimum-penalty hardness result addresses a
different question: even when a small sufficient penalty is obvious,
finding a nearly smallest sufficient penalty can be hard. The perturbation
theorem is a useful companion with a different input model.

The primary proofs are complete within their stated assumptions. Earlier
independent reviews, the fresh audits linked below, and the targeted
reproduction checks found no unresolved correctness blocker. This does
not certify exhaustive novelty or efficient solver performance.

## Claims suitable for further publication development

| Result and proof | Exact claim | Necessary scope |
| --- | --- | --- |
| [One-binary encoding obstruction](parametric-exploration.md), Theorem 1 | With a chain of length \(n\), the least optimized-dual penalty is \(2^{2^n-1}\), with exactly \(2^n\) ordinary binary digits. The sparse instance length is \(O(n\log n)\). The obstruction persists for fixed additive dual accuracy below one. | Compact native set; linear objective; one binary; one dualized scalar affine equality; convex quadratic native constraints with fixed coefficients. The feasible binary slice has a uniform strict point. The lower bound is exponential in continuous dimension and superpolynomial in ordinary input length; it is not asserted to be exponential in the full sparse input length. |
| [General upper bound](penalty-upper-bound.md), equations (3)–(14) | An integer zero-multiplier penalty giving equality of values and minimizer sets has bit length at most \((N+1)2^{O(n)}\). | Explicit rational quadratic input of length \(N\), \(n\) continuous variables, finite boxes, convex continuous slices, and refined Slater on equality-feasible slices. The norm is \(\ell_\infty\) or \(\ell_1\). No Slater condition is needed on equality-infeasible slices. |
| [Fixed-quadratic-count refinement](penalty-upper-bound.md), equations (15)–(25) | With at most \(k\) native inequalities nonlinear in the continuous variables, a sufficient zero-multiplier penalty has bit length \(N^{O(k+1)}\). Arbitrarily many affine rows and continuous variables are allowed. | The preceding assumptions remain in force. The bound counts nonlinear native inequalities, not all constraints or the quadratic objective. Degenerate affine geometry and singular Hessians are allowed. The proof gives an encoding existence theorem, without a practical coefficient-selection algorithm. |
| [Calibration hardness](minimum-penalty-hardness.md), Theorems 3–4 | For a binary box, linear objective, and one scalar equality, fixed-penalty dual exactness is coNP-complete on the specified family. Unless P = NP, no polynomial-time method always returns a sufficient penalty within any fixed polynomial factor of the smallest one. | The primal has the supplied unique feasible point zero. All thresholds are positive. Multiplier optimization is unrestricted. The hardness uses growing binary dimension and ordinary binary data; it is not strong hardness for this binary-box family. A universal conservative penalty of one is already sufficient. |
| [Finite-grid perturbation bound](smoothed-penalty.md), Theorem 3 | With at most \(K\) compact convex slices, objective range \(M\), and an explicit rational grid in a cube of radius \(\sigma\), the zero-multiplier coefficient \(4mKM/(\sigma\epsilon)\) is value-exact with probability at least \(1-\epsilon\), or the sampled instance is infeasible. Its encoding is polynomial in the supplied data and \(\log K\). | The residual maps are affine and fixed before sampling. The objective is convex on every slice. The sampled problem can differ in optimal value and assignment from the original one. Conditioning on feasibility needs a feasibility-probability bound or a robust feasible slice. Numerical penalty magnitudes can be large and their continuous-noise expectation can be infinite. |

The general upper and lower bounds agree at the scale of exponential
dependence on continuous dimension; their bases and their dependence on
the full input length are not proved sharp. The fixed-count refinement
shows that a growing number of nonlinear quadratic inequalities is
necessary for the worst-case superpolynomial encoding phenomenon within
this model. It is not a statement that every family with growing count
has large penalties.

## Definitions that must remain explicit

The lower-bound and calibration statements use

\[
 D_\rho=\sup_{\lambda\in\mathbb R^m}
   \min_{x\in X}\{f(x)+\lambda^Tr(x)+\rho\|r(x)\|\},
 \qquad v=\min\{f(x):x\in X,\ r(x)=0\}.
\]

Their least penalty means the least \(\rho\ge0\) with \(D_\rho=v\).
This must be distinguished from exactness at a specified multiplier,
existence of a finite maximizing multiplier, and equality of primal and
penalized minimizer sets. The constructed lower-bound duals attain their
suprema, so they do not depend on nonattainment. At the least penalty,
infeasible native points tie with feasible optima. Strictly larger
penalties with the specified multipliers give minimizer-set exactness.

The upper bounds prove the stronger zero-multiplier and minimizer-set
conclusion directly. The perturbation theorem proves value exactness at
its displayed coefficient and minimizer-set exactness at any strictly
larger coefficient. These differences are intentional.

All encoding statements refer to ordinary explicit rational input and
ordinary binary representations of penalty coefficients. Succinct
arithmetic expressions, unbounded exponent formats, instance-dependent
fractional penalties, and reformulations that change the dualized
constraint are outside the lower-bound claim. The easy primal solutions
in the negative constructions are also intentional: encoding and
calibration difficulty do not imply hardness of those primal problems.

## Strongest primary comparisons and defensible contribution

| Primary source examined | Relevant antecedent | Addition that remains defensible |
| --- | --- | --- |
| Gu, Ahmed, and Dey, [*Exact Augmented Lagrangian Duality for Mixed Integer Quadratic Programming*](https://arxiv.org/abs/1907.00920), Definition 8 and Theorem 11 | Polynomial binary encoding for exact norm penalties with rational positive semidefinite quadratic objectives and linear native constraints. | The one-binary construction prevents extension of that guarantee to all compact convex quadratically constrained models. |
| Lefebvre and Schmidt, [December 15, 2025 manuscript](https://optimization-online.org/wp-content/uploads/2024/07/exact-penalty-for-minlp-1.pdf), Definition 1, Assumption 5, Theorems 14–15, and conclusion | Finite exactness for compact convex continuous slices with refined Slater; efficient sufficient MILP penalties; explicit questions about quadratic-constraint encoding and the smallest penalty. | The construction gives a negative instance for the unrestricted encoding extension. The binary-box reduction answers the smallest-penalty question in growing dimension, including a relative approximation obstruction. Claims must identify this source version. |
| Bienstock, Del Pia, and Hildebrand, [*Complexity, Exactness, and Rationality in Polynomial Optimization*](https://arxiv.org/abs/2011.08347), §6; Beck, Bienstock, Schmidt, and Thürauf, [*On a Computationally Ill-Behaved Bilevel Problem with a Continuous and Nonconvex Lower Level*](https://optimization-online.org/wp-content/uploads/2022/02/nearly-feasible-bilevel-preprint.pdf), §2 and Result 4 | Repeated-squaring precision obstructions, including bounded convex chains with Slater regularity. | The contribution is the explicit optimized-multiplier norm-dual obstruction and its restricted model, not discovery of repeated squaring or a general QCQP precision pathology. |
| Basu and Roy, [final author manuscript](https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf), Theorems 3–4; Basu, [survey, September 4, 2014](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf), Theorem 2.27 | Effective bounds for weak sign conditions and quantifier elimination, including coefficient heights. | The general upper bound and fixed-count refinement are applications of established algebraic geometry. The package supplies the sparse KKT/reciprocal construction, convex affine-face reduction, degenerate limiting argument, and their penalty consequences. |
| Grigoriev and Pasechnik, [*Polynomial-Time Computing over Quadratic Maps I: Sampling in Real Algebraic Sets*](https://arxiv.org/abs/cs/0403008); Kamminga and Rudolph, [full arXiv version 2411.03096v2](https://arxiv.org/html/2411.03096v2), §§6.3–7.2 and §8.5, Corollary 8.14 | Polynomial sampling for a fixed number of quadratic-map components, proved small-variable formulas and coefficient bounds, and an explicit fixed-total-constraint QCQP application without convexity assumptions. The older optimization theorem's unavailable proof does not erase these later results. | The fixed-count penalty theorem uses a convex affine-face reduction to handle arbitrarily many affine rows and a direct KKT derivation. Neither the underlying small-variable method nor the fixed-count value lemma is asserted to be new. Priority of the particular penalty consequence remains qualified. |
| Alessandroni et al., [*Alleviating the Quantum Big-M Problem*](https://arxiv.org/abs/2307.10379), v4 §IV.A, Lemma 1 | Optimal QUBO penalty hardness already holds with a known trivial original optimizer. | The proposed distinction is a scalar residual, linear objective, binary-box native set, optimized unrestricted multiplier, and polynomial-factor calibration obstruction. Generic penalty hardness and a known primal optimum are not new. |
| Dunagan, Spielman, and Teng, [*Smoothed Analysis of Condition Numbers and Complexity Implications for Linear Programming*](https://www.cs.yale.edu/homes/spielman/Research/lpcond.pdf); Bürgisser and Amelunxen, [*Robust Smoothed Analysis of a Condition Number for Linear Programming*](https://arxiv.org/abs/0803.0925), v3 | Convex-boundary anti-concentration and smoothed conditioning. Convex sensitivity and exact-penalty multiplier estimates also predate this work. | The finite-grid finite-union penalty statement combines those principles with explicit rounding and feasibility qualifications. It should be a companion result, not presented as a new conditioning principle. |

The precise source-by-source audits are
[the encoding review](parametric-penalty-literature-review.md),
[the calibration review](minimum-penalty-novelty.md),
[the smoothing review](smoothed-penalty-novelty.md),
[the fresh priority audit](publication-penalty-priority-audit.md), and
[the fresh fixed-count audit](publication-penalty-fixed-k-audit.md), with
its [separate primary-source comparison](publication-penalty-fixed-k-prior-audit.md).
The searches recorded there are bounded searches, not evidence that an
equivalent statement cannot exist elsewhere.

One source correction is relevant to the definitions but should remain
supporting material: Lefebvre–Schmidt Example 13 has exact supremum-defined
dual value at every finite penalty, but no finite maximizing multiplier.
The calculation is documented in
[the independent geometry review](penalty-geometry-review.md) and
rechecked in the fresh priority audit. It does not invalidate that paper's
sufficient theorem or the stated encoding question. The present negative
examples avoid this distinction by giving exact attained dual formulas.

## Proof and reproduction evidence

The one-binary and symmetric lower-bound dual identities have targeted
[Lean coverage](formal/penalty-encoding-coverage.md) from their actual
native constraints. The current source SHA-256 is
`f42d98e8997e65f77a5573886673b00d823bd0aa1aa3f08d560ee4b5b780d72d`,
matching the independently reviewed version. Its infinite sequence storage
and the finite model have manually checked restriction/extension
correspondence; that correspondence is not a separate Lean theorem.
Convexity, Slater, input encoding, digit counts, significance, and novelty
remain mathematical and literature audits, not formalized conclusions.

The upper bounds were independently reviewed against the final Basu–Roy
source and the coefficient-height clause in effective quantifier
elimination. The final-source weak-sign-condition restriction and a
conservative factorial term are incorporated. The fixed-count proof was
reviewed separately for affine-face deletion, positive-definite
regularization, the two-block limit formula, and multiplier recovery.
Neither upper-bound theorem is Lean formalized. The proofs use published
algebraic-geometric theorems rather than a reproof of those sources.

The following targeted commands were rerun for this publication-readiness
audit; all exited successfully:

```sh
python research-20260925/check_parametric_penalty.py
python research-20260925/check_minimum_penalty_hardness.py
python research-20260925/check_smoothed_penalty_review_second.py
sha256sum research-20260925/formal/PenaltyEncoding.lean
```

They checked 72 exact lower-bound envelope cases; 976 binary-box and 75
unit-data calibration cases; and 363 penalty, 150 grid/tube, and 1,216
sharpness cases. These are arithmetic regression checks on finite
instances, not proofs of the quantified theorems. Existing independent
checks and formal compilation are recorded in the linked notes. No
project-wide checks or CI inspection were performed.

A targeted check of the seven penalty publication notes and edited main
notes found no trailing whitespace or missing local Markdown targets.

## Publication boundary and remaining work

No further theorem is required to make the scoped encoding-and-calibration
package self-contained. The general balanced-mixture geometry, symmetric
companion, unit-data hardness example, and smoothing theorem serve as
explanation or supporting results. They should not be counted as unrelated
major discoveries.

Before selecting a submission, an author should choose the central claim
and appropriate breadth, keep the source versions and distinctions above,
and decide whether the fixed-count consequence offers enough independent
novelty to feature as a principal theorem. External expert and journal
review remain valuable, but they are not evidence of an unfinished proof.
The package contains no solver experiment and makes no speedup claim.

Efficient coefficient-selection algorithms, numerically moderate penalties,
more informative perturbation models, and applications to decomposition
are possible future research. They are not prerequisites for the stated
theoretical claims, and none was pursued in this publication-readiness
pass.
