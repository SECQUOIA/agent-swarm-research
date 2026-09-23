# Well-conditioned box-follower hardness: source audit

Date: 2026-09-05. Bounded primary-source assessment of
[the promoted well-conditioned hardness result](../results/bilevel-well-conditioned-box-exact-hardness.md),
whose full investigation version was read. The author reports two passing
independent proof reviews before promotion; this note audits sources.

The candidate result has a precise potential contribution: scalar-leader
bilevel threshold decision remains NP-complete with one fixed unit-box
quadratic follower, a Hessian uniformly close to identity, bounded coefficient
magnitudes, an affine upper objective, and no follower-dependent upper
constraints. No theorem matching all these restrictions was found in this
bounded search. The SAT gap is exponentially small with polynomial encoding;
this is ordinary exact hardness, not strong hardness or constant-gap
inapproximability.

Several central construction ideas have unusually close predecessors.
Both diagonal scaling of feedforward ReLU networks and approximation by
convex quadratic network energies are known. Their use alone is not a new
representation theorem. The candidate's quantitative bit-size and
relative-coordinate estimates, and the resulting restricted bilevel hardness,
are the distinctions to assess.

## Diagonal scaling is established

El Ghaoui, Gu, Travacca, Askari and Tsai, *Implicit Deep Learning*, SIAM
Journal on Mathematics of Data Science (2021),
[author manuscript](https://arxiv.org/pdf/1908.06315), §2, equations (2.6)–(2.7),
uses positive diagonal similarity to preserve positively homogeneous network
predictions while making the recurrent matrix contractive in the infinity
norm. The transformed matrices are `SAS^-1`, `SB`, and `CS^-1`.
Their argument invokes the Collatz–Wielandt characterization of the
Perron–Frobenius eigenvalue. The discussion beginning §3 notes that strictly
triangular feedforward matrices have zero spectral radius. Thus arbitrarily
small scaled interaction weights in a feedforward representation are already
supported by this framework. The candidate gives an explicit rational choice
suited to a later complexity reduction.

## Convex squared-residual emulation is also established

Zach and Estellers, *Contrastive Learning for Lifted Networks*, BMVC 2019,
[primary full paper](https://arxiv.org/pdf/1905.02507), §2, equations (2)–(4),
uses a convex energy of the form

```
.5 ||z_1-W_0 x||^2 + .5 sum_k gamma^k ||z_(k+1)-W_k z_k||^2
```

over convex activation sets. Nonnegative orthants model ReLU activations.
They derive first-order terms describing feedback from later layers and
explain that feedforward computation is recovered as the feedback parameter
vanishes. Their introduction explicitly states approximation by strictly
convex energies to arbitrary accuracy. Diagonally normalizing this type of
energy produces the same general family of squared triangular residuals as
the candidate. The checked sections do not provide the candidate's uniform
relative-coordinate error with explicit polynomial rational bit lengths,
near-identity Hessian bounds on a unit box, or scalar bilevel hardness.

Høier and Zach, *Lifted Regression/Reconstruction Networks*, BMVC 2020,
[primary institutional manuscript](https://research.chalmers.se/publication/538335/file/538335_Fulltext.pdf),
§§2–3, further treats strictly convex quadratic network energies on convex
activation sets, with forward regression and reverse reconstruction terms.
It explicitly identifies weak feedback as the regime in which convex energy
models imitate feedforward networks. Its focus is Lipschitz control and
learning. This reinforces that convex-energy approximation of neural
computation has established foundations; it does not supply the candidate's
restricted exact-complexity result.

Amos and Kolter, *OptNet*, ICML 2017,
[primary full paper](https://proceedings.mlr.press/v70/amos17a/amos17a.pdf),
Theorem 2, gives optimization-layer representations of elementwise
piecewise-linear functions, including an affine map followed by ReLU. This
is an earlier direct QP/ReLU connection. A single ReLU layer has a simple
Euclidean projection interpretation; representing a whole deep computation
by one near-identity box QP with a certified error is a further step.

## Scalar hardness and representation directions

The [earlier scalar-box audit](bilevel-dense-box-hardness-novelty.md)
records Sugishita and Carvalho's
[one-leader linear-follower hardness](https://arxiv.org/abs/2510.21126),
including the importance of distinguishing coupled follower constraints from
a fixed box. That source remains a close complexity predecessor. The present
candidate strengthens the local SPD-box hardness result by controlling
absolute eigenvalues and coefficient magnitudes, while accepting a much
smaller gap. Its hardness is not a statement about the difficulty of solving
one fixed convex QP.

Bassan, Moshkovitz and Katz, *Additive Models Explained: A Computational
Complexity Approach*, NeurIPS 2025,
[primary proceedings paper](https://papers.neurips.cc/paper_files/paper/2025/file/1917f4feb7bab715645aa7b2476566f0-Paper-Conference.pdf),
Lemma 14, printed pp. 38–39, claims NP-hard verification for scalar-input,
scalar-output neural networks. This is relevant published prior for scalar
neural hardness. The displayed proof has issues: equations (24) and (25)
interchange the ReLU formulas for identity and absolute value, while (26)
contains an incorrect constant. These were checked in a rendered PDF page.
The later claim that a continuous ReLU map sends an entire interval exactly
onto Boolean vectors also needs justification: a nonconstant continuous map
from an interval cannot have finite image. This audit therefore records the
prior claim but does not import its proof or conclude that the theorem itself
is false. The candidate instead proves a continuous ternary construction and
penalizes fractional assignments explicitly.

Koeln, *Exact feedforward neural network representations of multi-parametric
quadratic programs with applications to explicit MPC*, Automatica 2026,
[publisher abstract and introduction](https://www.sciencedirect.com/science/article/pii/S0005109826003638),
DOI 10.1016/j.automatica.2026.113179, constructs networks representing QP
responses, including clipped-ReLU models for boxed QPs. The stated network
size can be exponential in the constraint count. This is the opposite
representation direction, with a different size target. Only the primary
abstract and introduction were accessible and checked here.

## Recommended claim and remaining limits

The key estimate to retain is the candidate's control of each scaled state
`u_i/s_i`, rather than only an absolute Euclidean error. Together with a
polynomially encoded scaling, it preserves the SAT readout despite extremely
small state amplitudes. The bounded upper coefficients are obtained by
shrinking the readout and consequently the hardness gap. This tradeoff is
central to the result.

The theorem is compatible with a runtime polynomial in inverse normalized
additive error for fixed leader dimension and bounded conditioning. It rules
out polynomial dependence on accuracy bit length for exact-scale global
optimization, unless `P=NP`; it does not rule out the proposed additive
scheme. Keep explicit the absence of follower-dependent upper constraints,
the fixed unit box, and the uniform absolute eigenvalue bounds.

The search covered well-conditioned quadratic bilevel hardness, scalar ReLU
verification, QP optimization layers, implicit-network scaling, and lifted
quadratic network energies. No exact matching hardness theorem was found.
The underlying emulation methods should be credited plainly, with novelty
qualified around the quantitative restriction-preserving reduction.
