# Focused prior-art audit: strong-field component optimization for mixed box QPs

Date: 2026-10-02. This audit compares the reviewed
[strong-field component theorem](../new-direction/strong-field-component-qp.md)
with random-field Ising algorithms, percolation and correlation-decay methods,
and smoothed discrete optimization. It also checks the component-oracle
interface for a possible fixed-degree polynomial extension. The comparison is
focused; it is not a priority clearance.

## Main assessment

The reviewed theorem solves a different problem from the closest random-field
Ising results. It exactly optimizes a rational mixed continuous/integer
quadratic over a product of boxes, including indefinite and frustrated
quadratic interactions. Independent linear perturbations expose coordinates
whose derivative has a fixed sign across the entire original box; fixing
those coordinates splits the problem into components of the original
interaction graph. The algorithm then exhaustively solves each component,
including all integer labels and continuous box faces. It returns an exact
rational optimizer for every finite-noise draw and has expected polynomial
bit work under an explicit strong-noise condition, with no treewidth or
curvature promise.

The proof's persistence step, connected-set count, and exhaustive component
solver are elementary ingredients. Their composition is also the familiar
subcritical-percolation pattern. The technical result is the explicit
coordinate test and weighted finite-grid bound for arbitrary mixed box QPs,
together with an all-draw exact solver whose component work accounts for
binary-encoded integer ranges. I found close analogues for Ising systems and
finite-action decision networks, but none of the reviewed sources proves this
full mixed continuous exact-optimization guarantee. This is a scoped search
finding, not evidence of novelty.

## Closest random-field and percolation comparisons

- **Exact RFIM ground states are already polynomial for ferromagnetic
  interactions and arbitrary fields.** Esser, Nowak, and Usadel write the
  random-field Ising Hamiltonian with nearest-neighbor ferromagnetic couplings
  and Gaussian or bimodal random fields, and calculate ground states by
  mapping the Ising problem to a transport network and running maximum flow.
  Their strong-field conclusion is about ground-state domain statistics:
  as field magnitude increases, the domains approach clusters of the
  percolation model induced by field signs. This is a physics/numerical study
  on two- and three-dimensional lattices; it does not prove an expected
  component-enumeration runtime. The Ising variables are binary and the
  ferromagnetic structure is essential to the cut reduction. The mixed-QP
  theorem allows continuous variables and arbitrary signed quadratic
  couplings. See Esser, Nowak, and Usadel, [“Exact Ground State Properties of
  Disordered Ising-Systems”](https://arxiv.org/abs/cond-mat/9612022), §§I–II
  and IV (especially the flow mapping and strong-field cluster discussion).
- **The min-cut capability does not need strong noise.** Hartmann and Usadel's
  1995 paper is titled [“Exact determination of all ground states of random
  field systems in polynomial time”](https://doi.org/10.1016/0378-4371(94)00259-V).
  Its publisher abstract says that ferromagnetic and unfrustrated
  antiferromagnetic Ising systems with arbitrary site fields are transformed
  to a network-flow problem. The project KB has a matching metadata-only,
  unread package at
  [`hartmann1995-exact-determination-of-all-ground`](../../literature/papers/hartmann1995-exact-determination-of-all-ground/paper.md);
  no full article text was available in that package. I therefore use this
  only as an abstract-level solver boundary, not for page-specific claims.
- **High-disorder RFIM algorithms use percolation, but target approximate
  counting and sampling.** Helmuth, Lee, Perkins, Ravichandran, and Wu prove
  that for bounded-degree graphs, sufficiently high-variance iid Gaussian
  external fields give an FPTAS for the ferromagnetic Ising partition
  function and a sampler with high probability over the field realization.
  Their analysis uses percolation on a self-avoiding-walk tree and handles
  connected regions of small fields. This is the nearest formal
  high-disorder/percolation guarantee, but its output is an approximation or
  sample, not an exact ground state, and it is still the ferromagnetic Ising
  model. The source is read in the local KB:
  [[helmuth2021-approximation-algorithms-for-the-random]] p.1-3, p.8-10;
  see also the [arXiv record](https://arxiv.org/abs/2108.11889).
- **Random finite-action optimization has correlation-decay precedents.**
  Gamarnik, Goldberg, and Weber's Cavity Expansion algorithm truncates an
  exact cavity recursion on a computation tree. Under decay assumptions, it
  gives high-probability near-optimal decentralized decisions for finite
  action sets with random rewards, including bounded-degree examples. It is
  approximate and finite-action, rather than an exact solver for continuous
  mixed box quadratics. The read source is
  [[gamarnik2014-correlation-decay-in-random-decision]] p.1-4, p.8-18;
  see also [arXiv:0912.0338](https://arxiv.org/abs/0912.0338).

Thus “high disorder makes components small” is established motivation and a
standard algorithmic pattern. It does not by itself solve arbitrary
continuous-spin interactions. In the RFIM studies above, high-field
percolation describes field-sign domains, often at occupation probability
one half; it is not a proof that the optimizer of a general signed quadratic
has only small unresolved components.

## Smoothed discrete optimization

Beier and Vöcking's accessible primary source is the 2004 STOC paper
[“Typical Properties of Winners and Losers in Discrete Optimization”](https://doi.org/10.1145/1007352.1007409)
(local package:
[[beier2006-typical-properties-of-winners-and]]). For a fixed feasible subset
of binary vectors and independent bounded-density random linear objective
coefficients, its generalized Isolating Lemma bounds the density of the
winner-versus-runner-up objective gap by a quantity proportional to the
number of variables. Their adaptive-precision construction characterizes
polynomial smoothed complexity through randomized pseudopolynomial
solvability of the unary problem. This explains why random objective
coefficients can make an exact finite-action problem easier, while also
showing that the perturbation alone is not an optimizer. The theorem here
uses derivative-sign persistence to reduce the feasible search graph, not
just objective-gap isolation, and it has continuous coordinates and an
explicit expected-time bound.

Röglin and Vöcking's [“Smoothed Analysis of Integer Programming”]
(https://doi.org/10.1007/s10107-006-0055-7) extends related winner/loser-gap
and adaptive-rounding ideas to integer linear programs. Its tractability
characterization relies on pseudopolynomial solvability and concerns
linear-integer models; it does not provide the derivative-persistence
decomposition or exact optimization of indefinite mixed continuous
components. The source is available in the local package
[[roglin2007-smoothed-analysis-of-integer-programming]].

These works are relevant anti-concentration and output-refinement baselines.
They do not subsume a structural solver that makes most coordinates
provably endpoint-valued for the sampled objective, then solves only the
remaining connected components. The new theorem's randomization is a
chosen **large** finite perturbation of the objective; it returns the
optimizer of that perturbed problem. It is not a guarantee for the optimizer
of the unperturbed objective, and its high-noise threshold can be large.

## Component-oracle question for polynomial objectives

The QP theorem avoids algebraic degeneracy entirely. For each component it
enumerates integer labels and continuous lower/free/upper states. On a free
face, a singular Hessian would permit a nontrivial optimal line, so an
optimizer with a minimal free set has a nonsingular rational stationary
system. This gives exact rational output with polynomial bit length on every
draw.

For fixed-degree polynomial components, generic finite stationary systems
may admit a component solver with cost `c_d^k poly(I+b)`, where `k` is the
component dimension, `d` is the fixed degree, and `b` is coefficient-bit
length. This is materially different from a loose `2^poly(k)` fallback,
which subcritical component tails do not pay for. Two primary sources bound
what can be claimed:

- Greuet and Safey El Din, [“Probabilistic Algorithm for Polynomial
  Optimization over a Real Algebraic Set”](https://arxiv.org/abs/1307.8281v2),
  SIAM Journal on Optimization 24(3), 2014, give exact global infimum and
  attainment/minimizer outputs under regularity assumptions. The abstract's
  coarse bound is essentially cubic in `(sD)^n`; Theorem 22 gives a more
  detailed arithmetic-operation expression. This is not itself a Turing-bit
  bound of the desired form, and with a number `s` of equations growing with
  `n`, the abstract expression alone does not certify a `c_d^k` bound.
- Gimenez and Matera, [“On the bit complexity of polynomial system
  solving”](https://arxiv.org/abs/1612.07786), Theorems 1.2–1.3 and 6.8,
  give a probabilistic Turing algorithm computing a Kronecker
  representation for a zero-dimensional fiber of a reduced regular
  polynomial sequence. The bit bound is polynomial in system size and
  coefficient height, with a quadratic dependence on the Bézout degree
  `δ` (Theorem 6.8 gives
  `O~(r(nL+n^5) δ(dδ + ndrh))`). For `r=n=k` fixed-degree equations,
  Bézout gives `δ≤d^k`; thus the stated bit bound can be `c_d^k poly(I+b)`.
  This is a real generic-face solver lead. Its reduced-regular-sequence
  premise is essential: it does not, as stated, handle positive-dimensional
  or otherwise degenerate systems on every finite-grid noise draw, nor does
  it supply the needed rare-failure budget and same-draw exact fallback.

The remaining polynomial-extension question is therefore narrower than
“does exact real algebraic geometry have singly-exponential algorithms?”
One needs: (i) a fixed-degree bit bound with a constant base in `k` for the
generic stationary systems actually arising on faces; (ii) an effective
bound on the finite-grid perturbations for which these systems fail the
required regularity; and (iii) a fallback whose expected cost is paid by a
single finite rational noise law without resampling. The current mixed-QP
theorem does not assert this extension.

## Solver boundary and scope

For a finite graph with bounded maximum degree, a direct connected-set
enumeration bounds the number of connected size-`k` vertex sets containing a
fixed root by `(4Δ)^(k-1)`. Under the theorem's independent bad-site tests,
the weighted sum is a geometric series whenever `4Δ max_i(a_i q_i)<1`.
This is an elementary weighted subcritical condition, not a treewidth
condition and not an appeal to a lattice percolation threshold. For the
quadratic component, the exact work is bounded by
`A(C)=∏_{i∈C} a_i`, where `a_i=3` for a continuous variable and is its number
of native integer labels otherwise. The explicit noise condition must
therefore pay for large integer ranges. Its proof counts a component as
degenerate only when necessary: equality atoms are retained as bad sites,
so the finite perturbation law preserves exact all-draw correctness.

The closest complete statement remains the reviewed theorem in
[`strong-field-component-qp.md`](../new-direction/strong-field-component-qp.md).
The current solver claim is an exact optimizer of the sampled objective
with expected polynomial bit work under strong noise. It does not assert an
algorithm for arbitrary perturbation strengths, a global treewidth-free
solver for the unperturbed mixed QP, or a fixed-degree polynomial extension.

## Retrieval and scope note

The primary Esser–Nowak–Usadel preprint was read through the official arXiv
HTML/PDF; its flow mapping and percolation comparison are in §§I–II and its
numerical scope is explicit. The Helmuth et al. and Gamarnik et al. sources
were read from local primary-text packages. Hartmann–Usadel is present as a
metadata-only package and only its publisher abstract was checked. Greuet–
Safey El Din and Gimenez–Matera are being routed through the sole literature
writer for local promotion/read; the mathematical comparison above was
checked against their openly accessible primary texts. No literature KB
files or generated indexes were changed by this audit.
