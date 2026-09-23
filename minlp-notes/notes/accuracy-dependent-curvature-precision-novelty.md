# Accuracy-dependent curvature density: source audit

Date: 2026-09-05. Bounded primary-source assessment of
[the scalar curvature candidate](accuracy-dependent-curvature-precision.md),
read in full. This is a literature assessment, not an independent proof audit.

No matching theorem was found for the explicit density

```
rho_epsilon(x) = min(sqrt(f''(x)/epsilon), (1-x)f''(x)/epsilon)
```

and its constant-factor characterization of the minimum number of admissible
chord intervals, uniformly over convex `C^2` functions with nondecreasing
second derivative and over all positive tolerances. The resulting comparison
against every convex lift with unrestricted integer coordinates was also not
found. These are qualified findings from a bounded search, not a priority
certification. Accuracy-dependent approximation densities, adaptive secant
partitions, and endpoint corrections are already established ideas.

## The closest function-specific approximation measure

Simchowitz, Jamieson, Suchow, and Griffiths,
[Adaptive Sampling for Convex Regression](https://arxiv.org/pdf/1808.04523)
(2018), is the closest checked source. Definition 1 and Equation (5), printed
page 4, define a secant-error modulus `omega(f,x,epsilon)` and integrate its
reciprocal, excluding endpoint intervals handled separately. Lemma 2.1,
printed page 3, proves that maximum chord error lies between midpoint error
and twice midpoint error. This lemma deserves direct attribution in the
candidate. Theorem 3.2, printed page 6, constructs adjacent intervals with
prescribed midpoint error and obtains a packing bound with denominator
`4(1+log(omega_max/omega_min))`. Proposition 3.4 gives an oracle allocation.
Section 2.1.2 connects the modulus to square-root curvature asymptotically.
Remark A.1, printed page 28, explains why the integrated modulus can exceed
the necessary number of intervals by a logarithmic factor for piecewise
linear functions. Their principal target is function-specific sampling
complexity, including noisy observations.

The proposed density is a different, explicit local formula. Its claimed
constant-factor comparison uses the extra monotonicity of `f''`. It therefore
does not establish constant-factor results for every convex function in the
sampling paper. Conversely, that paper does not state the proposed formula
or a minimum-integer comparison. Do not advertise the candidate as the first
accuracy-dependent or endpoint-corrected approximation complexity measure.

## Adaptive curvature estimates and asymptotic segment counts

Choi, Ding, Hickernell, and Tong,
[Local Adaption for Approximation and Minimization of Univariate Functions](https://arxiv.org/pdf/1606.02766)
(Journal of Complexity 40, 2017, 17–33;
DOI `10.1016/j.jco.2016.11.005`), gives guaranteed adaptive linear-spline
algorithms on a cone of functions whose curvature cannot change too sharply.
In the checked arXiv text, Equation (15), printed page 9, defines an
accuracy-dependent local refinement level using curvature bounds on enlarged
intervals. Theorem 2, printed page 10, integrates the reciprocal local mesh
width to bound sample cost. The following asymptotic calculation recovers
the integral of `sqrt(|f''|/epsilon)`. Their cone assumptions and local
supremum-based mesh differ from the candidate's monotone-curvature class and
pointwise minimum formula. A uniform comparison with arbitrary convex integer
lifts is not part of the checked result.

Rote's
[1992 Sandwich-algorithm paper](https://page.mi.fu-berlin.de/rote/Papers/pdf/The%2Bconvergence%2Brate%2Bof%2Bthe%2BSandwich%2Balgorithm%2Bfor%2Bapproximating%2Bconvex%2Bfunctions.pdf)
provides established adaptive chord upper and tangent lower approximations,
including optimal-order quadratic decay of error in the number of pieces.
This is a direct predecessor for adaptive convex-function bands. No matching
explicit truncated density was identified in the source checks associated
with this research.

Frenzen, Sasao, and Butler,
[On the number of segments needed in a piecewise linear approximation](https://www.sciencedirect.com/science/article/pii/S0377042709008528)
(2010, DOI `10.1016/j.cam.2009.12.035`), concerns optimal nonuniform segment
counts. Only its primary publisher abstract was accessible in these audits;
the full theorem was not checked. It should be cited as relevant asymptotic
segmentation work without asserting its exact uniformity hypotheses.

The local
[raw-curvature obstruction](curvature-arclength-precision-obstruction.md)
clarifies the order of quantifiers. It varies the positive polynomial while
holding tolerance fixed and keeps the necessary integer count bounded even
as the raw square-root curvature integral diverges. That does not contradict
small-error asymptotics for each fixed function. Retain this distinction in
any publication discussion.

## Integer-formulation attribution and contribution

The lower bound imports the known midpoint/parity obstruction for mixed-
integer convex representability. Credit Lubin, Zadik, and Vielma,
[Mixed-integer convex representability](https://arxiv.org/abs/1706.05135),
especially Lemma 4.1 in the locally checked final text. The finite upper
uses a logarithmic encoding of a disjunction, also established; see Vielma,
[Embedding formulations and complexity for unions of polyhedra](https://arxiv.org/abs/1506.01417).

The distinctive bridge is quantitative: contacts in each parity class give
an interval with controlled chord error; the new density estimate then
bounds how many such intervals are needed. The candidate states

```
M_epsilon/24 <= N_epsilon <= 2 M_epsilon+1,
log2(1+M_epsilon)-log2(49) <= p_conv
    <= p_bin <= log2(1+M_epsilon)+2.
```

Thus the asserted contribution has two separable parts: an explicit finite
approximation measure under monotone curvature, and its comparison with the
minimum integer dimension of any convex lift. The latter remains useful
even if further approximation literature supplies an equivalent density.
Neither parity nor logarithmic disjunction encoding should be claimed new.

## Limits and next source questions

The result is finite and geometric. The upper bound permits real coefficients
and unrestricted formulation size. No polynomial-time procedure for
integrating this density, locating its quantiles, or producing rational knots
has been proved here. Scalar and monotone-curvature restrictions matter.
No necessity result for any multivariate sum of these quantities follows
from this audit.

Searches covered adaptive convex approximation, endpoint-corrected local
moduli, curvature-based knot placement, free-knot approximation, and weighted
curvature/K-functional terminology. No precise matching K-functional theorem
was located; this should remain a possible follow-up, not an asserted
identification. The most valuable additional comparison would establish
whether the proposed density has an existing name or an equivalent formula
in finite free-knot spline approximation with monotone curvature. The checked
sources already rule out broad claims of novelty for adaptive complexity
measures in general.
