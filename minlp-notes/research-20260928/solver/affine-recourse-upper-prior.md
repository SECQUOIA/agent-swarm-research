# Prior-work audit for the affine-recourse hierarchy

Date: 2026-09-28. Independent literature and significance audit of
[the affine-recourse upper theorem](affine-recourse-kernel-upper.md), read
together with [its sharpness example](affine-recourse-rate-boundary.md).
This supplements the existing [boundary audit](affine-recourse-prior.md)
and [fixed-polytope audit](partial-kernel-prior.md). It does not establish
publication priority or replace the separate proof reviews.

The defensible distinction is the combined theorem for a specific sparse
moment hierarchy: shared degree increases, private degree stays two, and
affine complete recourse permits an explicit inverse-order gap and feasible
rounding. Neither polynomial recourse approximation, low-degree treatment
of convex variables, nor repair of moment means through linear-program
sensitivity is a new general principle. A recent Wasserstein optimization
paper is particularly close to the last mechanism.

## The exact claim being compared

Shared bags `S_b` satisfy running intersection. Each private vector is
continuous and belongs to exactly one bag. The feasible fibers are

\[
 P_b(u)=\{y\in[-1,1]^{p_b}:A_by\le a_b+B_bu\},
 \qquad u\in[-1,1]^{S_b},
\]

with fixed `A_b` and nonempty fibers at every shared box point. The local
objective is polynomial in `u` and convex quadratic in `y`; its private
Hessian need only be pointwise PSD, rather than SOS, on the shared box.

The local functional is defined on
`R[u]_{<=2r} tensor R[y]_{<=2}`. It is positive on shared box-preordering
weights times squares affine in `y`, on scalar-square localizers for the
affine recourse inequalities, and on redundant private quadratic bounds.
Separator moments agree through shared degree `2r`. The theorem proves

\[
 0\le f^*-\rho_r\le C_2/r^2+C_1/r,
\]

with explicit coefficient, width, and Hoffman constants. No Slater
condition, full-dimensional fiber, SDP attainment, or SDP strong duality
is used for this primal inequality. This does not by itself establish
attainment or equality of a sparse SOS dual.

The largest matrix has `(p_b+1) binom(r+|S_b|,|S_b|)` rows. Thus private
dimension does not enter the exponent of `r` in the shared monomial count.
Matrix size, scalar moments, row counts, coefficient norms, and Hoffman
constants still depend on private dimension. This is not a dimension-free
accuracy or running-time bound.

## Strong recourse and moment precedents

[Zhong, Cui, and Nie (2024), *Towards Global Solutions for Nonconvex
Two-Stage Stochastic Programs: A Polynomial Lower Approximation
Approach*](https://doi.org/10.1137/23M1615516),
[open manuscript](https://arxiv.org/html/2310.04243v2), is a direct modeling
and approximation precedent. Theorem 4.1 gives convergence in `L1(nu)`
of polynomial recourse lower bounds under an Archimedean joint quadratic
module and continuity of the value function. Their algorithm then uses
these bounds in first-stage optimization. Equation (4.7) gives separate
degree limits for master and uncertainty variables in the approximating
polynomial. Its SOS certificate still has growing joint total degree in
master, private, and uncertainty variables. It is not a private-degree-two
relaxation, and the inspected theorem supplies no explicit degree rate or
sparse gluing. The example before Theorem 2.2 already uses `xy=0` to show
discontinuous recourse. The upper note's variable-matrix warning has this
close precedent; it should not be advertised as a new counterexample.

[Zhang and Zhong (2025 preprint), *Moment Relaxations for Data-Driven
Wasserstein Distributionally Robust
Optimization*](https://arxiv.org/html/2505.19278v2), Section 4.1,
Theorem 4.4, provides the closest proof mechanism found. For fixed-matrix
linear recourse, bounded master decisions, a sample moment bound, an
explicit quadratic-module bound on private dual second moments, and
specified degree conditions, its fixed-order moment relaxation has
`O(epsilon)` error as the Wasserstein radius `epsilon` tends to zero.
In the proof, private first moments satisfy a perturbed right-hand side;
equation (4.9) applies fixed-matrix LP sensitivity, and moment PSD plus
Cauchy--Schwarz controls mixed terms. Thus moment means followed by
recourse sensitivity are established precedent. The parameter is shrinking
distributional uncertainty, not increasing polynomial order. Their joint
total-degree moment hierarchy does not establish the present shared-only
degree restriction or overlapping-bag conclusion. Example 4.6 also warns
that absent private bounds, a moment relaxation can remain unbounded at
every order. Its half-strip construction differs from the fixed-polytope
note's bounded-domain example with omitted quadratic localizers.

[Bampou and Kuhn (2011), *Scenario-Free Stochastic Programming with
Polynomial Decision Rules*](https://www.nt.ntnu.no/users/skoge/prost/proceedings/cdc-ecc-2011/data/papers/1691.pdf),
Sections II--III, constructs upper and lower bounds for fixed-recourse
stochastic linear programs using polynomial decision rules and moment/SOS
constraints. It includes multistage programs and a prescribed uncertainty
distribution on a compact semialgebraic support. Theorems 2.2, 2.5, 3.1,
and 3.4 give bounding and SDP formulations. Growing polynomial complexity
only in parameter functions is therefore an established modeling idea.
No increasing-degree convergence theorem or explicit order rate was found
in the inspected seven-page paper. The present theorem minimizes over
shared decisions and proves a gap for specified finite pseudomoments;
it does not solve a stochastic policy problem or automatically cover its
nonanticipativity constraints.

[Lasserre (2010), *A joint+marginal approach to parametric polynomial
optimization*](https://arxiv.org/pdf/0905.2497), Theorems 3.3 and 3.5,
is an earlier foundational comparison. Joint decision/parameter moments
with a prescribed parameter marginal yield integral approximation of
value functions. The prescribed marginal and increasing joint degree are
different from the optimized, overlapping shared laws and fixed private
degree here. The existing fixed-polytope audit discusses this source in
more detail; the present audit reopened the manuscript.

## Fixed private degree, sparse rates, and repair

[Guo and Wang, *A Moment-SOS Hierarchy for Robust Polynomial Matrix
Inequality Optimization with
SOS-Convexity*](https://arxiv.org/html/2304.12628v3), Section 4.2,
equations (21)--(22), already keeps the convex decision-variable degree
fixed while increasing matrix moments in uncertain variables. Proposition
27 is the matrix pseudomoment Jensen statement; Theorem 29 proves
convergence under the paper's assumptions, including its Slater condition.
Its robust universal quantifier is different from joint minimization with
private recourse. The present theorem adds a rate for a different sparse
hierarchy and permits degenerate fibers. This comparison does not make
the low private degree or the Jensen step new. The fixed-polytope audit
also records the earlier Kahl--Henrion partial lifts and Fang--Fawzi
matrix-kernel rates, which further limit such claims.

[Weisser, Lasserre, and Toh, *Sparse-BSOS: a bounded degree SOS hierarchy
for large scale polynomial optimization with
sparsity*](https://arxiv.org/pdf/1607.01151) proves convergence with fixed
PSD degree and growing scalar products of constraints. Theorem 3 gives
first-step exactness for its SOS-convex subclass. Its convexity concerns
all variables of each local objective and constraint. Arbitrary nonconvex
shared dependence is outside that exactness argument. Nevertheless,
fixed PSD block size is already possible in other convergent hierarchies;
comparison must count scalar multipliers, coefficient equations, and
accuracy dependence, rather than only the largest matrix.

[Korda, Magron, and Ríos-Zertuche, *Convergence rates for sums-of-squares
hierarchies with correlative
sparsity*](https://d-nb.info/1330825241/34), Theorem 8, treats broader
constrained sparse polynomial problems through quantitative quadratic
module certificates. Degree grows in all variables of a bag. Applying
that result to the joint recourse formulation does not keep private degree
two. Conversely, the current theorem depends on affine fixed-matrix
recourse and private convexity, so it is not a replacement for that general
result. The earlier sparse-box inverse-square announcement is recorded in
[the independent prior audit](prior-independent.md); no novelty of the
box rate is being asserted here.

[Peña, Vera, and Zuluaga, *New characterizations of Hoffman constants for
systems of linear constraints*](https://arxiv.org/html/1905.02894),
Introduction (1)--(2) and Proposition 1, states the classical fixed-matrix
error bound uniformly over every consistent right-hand side. Its relative
version handles a fixed reference polyhedron such as the private box.
This directly supplies the repair constant without Slater. The paper also
explicitly notes earlier applications of Hoffman bounds to rounding
continuous relaxations of mixed-integer linear or quadratic problems.
The candidate's contribution cannot be described as introducing Hoffman
rounding. Its use after polynomial-kernel conditioning is the particular
combination under study.

[Tran and Toh, *Convergence rates of SoS hierarchies for polynomial
semidefinite programs*](https://arxiv.org/html/2406.12013v3), combines
polynomial penalties, approximation kernels, and geometric error bounds
for general matrix-defined domains. This is further precedent for
combining kernel approximation and feasibility geometry. It does not
give the present private-degree-two sparse hierarchy. The inspected
Section 2.4 describes the penalty reduction; its scope is materially
broader in constraint geometry and different in degree structure.

## Sharpness applies to the same anisotropic hierarchy

This paragraph is an independent deduction from the two repository
theorems, not a result attributed to an external source. It avoids an
unjustified comparison of total-degree and rectangular-degree cones.

Take one shared coordinate `u`, with private coordinates `x` and `z` in
two bags, and write

\[
 P_1(u)=[-1,1],\qquad
 P_2(u)=\{z\in[-1,1]:-z\le-u,\ -z\le u\},
 \qquad f=-ux+z.
\]

Both fibers are nonempty for every `u`. In fact
`P_2(u)=[|u|,1]`. Both objectives are linear in their private coordinate,
so all hypotheses of the upper theorem hold. The true minimum is zero.

The boundary theorem provides probability measures `alpha,beta` on
`[-1,1]` matching moments through degree `2r` with
`int |u| d(alpha-beta)=2E_(2r)(|u|)`. Lift them to
`x=sign(u)` and `z=|u|`, respectively. Evaluation against these actual
local measures satisfies every positivity condition of the rectangular
hierarchy, including the redundant private quadratic localizers. Hence,
writing its value as `rho_r^aniso`,

\[
 -\rho_r^{\rm aniso}\ge 2E_{2r}(|u|)
       \ge\frac{1}{9\pi(r+1)}.
\]

For this formulation, `s=1`, `m=r`, and `A=1` in the upper theorem.
The first bag needs no repair. In the second bag, `Lambda=1`,
`||B||_2=sqrt(2)`, and Hoffman constant one is valid: the stacked matrix
has only scalar rows `1` and `-1`, and the distance to any consistent
interval is at most the Euclidean norm of its violated inequalities.
Consequently,

\[
 \frac{1}{9\pi(r+1)}\le-\rho_r^{\rm aniso}
 \le\frac{3}{2r^2+1}+\sqrt{2V_r}
 \le\frac{3}{2r^2}+\frac{\sqrt6}{r},\qquad r\ge2.
\]

Thus the exponent one is sharp for this exact anisotropic hierarchy.
No inclusion between it and the boundary note's full total-degree
preordering is needed. The boundary note separately establishes an
inverse-order sparse certificate gap for that other cone. Its certificate
bound should not be transferred between the cones without checking each
term's degree and generator structure.

The lower-bound identity, the inverse-degree approximation of absolute
value, and the qualitative nonpolynomial-separator obstruction have
substantial prior work detailed in [the boundary audit](affine-recourse-prior.md).
The present combination is an exact-order boundary for a restricted
hierarchy, rather than a new approximation-duality theorem.

## A simple competing algorithm and significance

There is a direct grid/QP baseline with the same inverse-order exponent.
The following derivation is included to make the practical comparison
explicit. Let

\[
 F_b(u)=\min_{y\in P_b(u)}f_b(u,y),\qquad
 M_b=\max_{u,y}\|\nabla_u f_b(u,y)\|_2.
\]

The maxima are over the shared and private boxes. Hoffman repair gives
Hausdorff distance at most `h_b^H ||B_b||_2 ||u-v||_2` between fibers.
Choose an optimizer at `u`, repair it into the fiber at `v`, and apply
the two gradient bounds. Reverse `u,v` to conclude

\[
 |F_b(u)-F_b(v)|
 \le(M_b+\Lambda_bh_b^H\|B_b\|_2)\|u-v\|_2.
\]

The `N` Gauss--Chebyshev nodes cover each coordinate interval with radius
at most `pi/(2N)`. Rounding a global optimizer coordinatewise therefore
gives a grid upper value `U_N` with

\[
 0\le U_N-f^*\le\frac{\pi}{2N}
 \sum_b(M_b+\Lambda_bh_b^H\|B_b\|_2)\sqrt{|S_b|}.
\]

Local table entries are convex QP values, and junction-tree dynamic
programming uses `O(t N^s)` operations after those entries are computed.
This argument does not use moment relaxations. In an exact local-QP
oracle model it already gives an approximation procedure whose grid
exponent depends on shared width, rather than private dimension.
Numerical certification and bit complexity still need separate work.

The upper theorem adds a comparison with *every feasible pseudomoment
point* of a specified finite SDP. That is useful mathematical information
about lower relaxations, not a new justification for the simpler grid
algorithm. Its possible benefits include using inexpensive private
convexity inside global polynomial lower bounds, extracting feasible
decisions with an explicit error, and supporting branch-and-bound.
Practical advantage over QP grids, parametric elimination, Benders-type
methods, or other sparse relaxations remains unproved.

This is a coherent structural theorem with a matching obstruction. The
combined result is more consequential than the isolated example, because
it identifies a model class, a finite hierarchy, its dependence on shared
width, and an optimal general exponent. On the evidence examined, it is
best presented as a quantitative sparse convex-recourse contribution
whose priority is still qualified. It does not yet establish a major
general advance for MINLP. Complete recourse on the entire shared box,
fixed private constraint matrices, continuous private decisions, and
pointwise private convexity substantially restrict applications.

## Search and verification record

Primary sources were inspected at the sections identified above. A fresh
independent search agent inspected the Zhong--Cui--Nie,
Bampou--Kuhn, and Zhang--Zhong papers; the latter two recourse comparisons
and their degree distinctions were then checked against the primary text.
The existing fixed-polytope and boundary audits were read first to avoid
mistaking their established ingredients for new results.

Searches combined `polynomial optimization recourse moment relaxation`,
`two-stage sum-of-squares`, `partial convex moment hierarchy`,
`Hoffman sum-of-squares hierarchy`, and `polynomial decision rules`.
No equivalent complete theorem was found in this search. That absence
does not establish novelty; citation descendants and application-specific
terminology remain important targets before a publication-priority claim.

Targeted local actions were `cat`, `sed`, and `rg` reads of the two
candidate theorems, their reviews, the existing prior audits, and
`AGENTS.md`. The new file received a targeted whitespace and local-link
check. The hierarchy-transfer and grid arguments above were checked
mathematically; no computational proof test or Lean formalization was
performed for this audit. No project-wide verification or CI inspection
was run.
