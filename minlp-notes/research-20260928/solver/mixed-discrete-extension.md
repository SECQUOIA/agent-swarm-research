# Finite-state variables in the sparse kernel construction

Date: 2026-09-28. Status: proved consequence of the explicit kernel in
[sparse-kernel-rounding.md](sparse-kernel-rounding.md), with an independent
[extension review](mixed-discrete-review.md). Publication priority is
unestablished. Finite-state junction-tree formulations are established;
this note does not claim them as new.

## 1. Model and purpose

Let a finite tree have bags `b=(C_b,D_b)` of continuous coordinates and
finite-state variables. The bags cover all variables and satisfy the
running-intersection property for each variable. Each continuous
coordinate has domain `[-1,1]`. Each finite-state variable has an explicitly
listed finite domain. In bag `b`, let `A_b` be a list of permitted assignments
to `D_b`. The globally feasible finite-state assignments form the set

\[
 \mathcal A=\{a:a_{D_b}\in A_b\text{ for every bag }b\}.
\]

Assume `A` is nonempty. The objective and its minimum are

\[
 f(a,x)=\sum_b f_{b,a_{D_b}}(x_{C_b}),\qquad
 f^*=\min_{a\in\mathcal A,\ x\in[-1,1]^n}f(a,x),
\]

where each local cost is a polynomial. There are no other continuous
constraints. Costs can be nonconvex and can couple continuous and
finite-state variables arbitrarily within a bag.

The extension keeps finite-state labels unchanged and smooths only the
continuous coordinates. It therefore covers bounded integer and binary
models with local combinatorial restrictions. Continuous domains that
depend on a label, including indicator bounds, are not covered.

## 2. Labelled moment relaxation

Write `w=max_b |C_b|` and `d=max_{b,a in A_b} deg(f_{b,a})`, taking degree
zero for zero or constant costs. Choose an integer `r>=max(w,d)`. For each
`b` and each `a in A_b`, introduce a real linear functional

\[
 L_{b,a}:\mathbb R[x_{C_b}]_{\le2r}\longrightarrow\mathbb R.
\]

Require

\[
 L_{b,a}\left(q^2\prod_{i\in I}(1-x_i^2)\right)\ge0
 \quad(I\subseteq C_b,\quad 2\deg q+2|I|\le2r),       \tag{1}
\]

and masses `tau_{b,a}=L_{b,a}(1)` with `sum_{a in A_b} tau_{b,a}=1`.
The nonnegativity `tau_{b,a}>=0` already follows from (1).

For a tree edge `(b,c)`, put `S_C=C_b intersect C_c` and
`S_D=D_b intersect D_c`. For every assignment `s` to `S_D` and every
polynomial `p in R[x_{S_C}]` of total degree at most `2r`, impose

\[
 \sum_{a\in A_b:a|_{S_D}=s}L_{b,a}(p)
 =\sum_{a\in A_c:a|_{S_D}=s}L_{c,a}(p).              \tag{2}
\]

An empty sum is zero, and an empty finite-state separator has one empty
assignment. These sums, rather than equality of individual labelled
functionals, are essential: labels may differ away from the separator.

Let `rho_r` be the infimum of `sum_{b,a} L_{b,a}(f_{b,a})` subject to
(1)--(2) and normalization. Every original feasible point gives such a
collection, so `rho_r<=f*`. An arbitrary feasible collection's objective
need not itself be a lower bound; the SDP optimum or a feasible dual
certificate supplies the lower bound.

## 3. Explicit theorem

Use the unnormalized tensor Chebyshev expansion

\[
 f_{b,a}(x)=\sum_\alpha c_{b,a,\alpha}T_\alpha(x),\qquad
 H_{b,a}=\sum_\alpha |c_{b,a,\alpha}|
                              \sum_{i\in C_b}\alpha_i^2,
 \qquad A_{\rm mix}=\sum_b\max_{a\in A_b}H_{b,a}.       \tag{3}
\]

For `w>=1`, set

\[
 m=\lfloor r/w\rfloor+1,\qquad
 \delta_r={3\over2m^2+1}.                             \tag{4}
\]

**Theorem.** From every feasible labelled moment collection one can define
a probability law `nu` on `A times [-1,1]^n` such that

\[
 \left|\mathbb E_\nu f-\sum_{b,a}L_{b,a}(f_{b,a})\right|
 \le\delta_r\sum_{b,a}\tau_{b,a}H_{b,a}
 \le\delta_r A_{\rm mix}.                            \tag{5}
\]

Consequently,

\[
 0\le f^*-\rho_r\le{3A_{\rm mix}\over2m^2+1}
                     \le{3w^2A_{\rm mix}\over2r^2}.  \tag{6}
\]

There is a globally feasible point with objective at most the given moment
objective plus the first error bound in (5). This is an inverse-square
rate in the *total-degree moment order* `r`, with explicit dependence on
continuous bag size and the displayed coefficient budget.

If `w=0`, all costs are constants for each label. Equations (1)--(2) reduce
to consistent finite-state bag probabilities, which admit a global law.
Then (5) holds with error zero and `rho_r=f*`, including `r=0`.
There is no division by `w` in this case.

## 4. Proof, including zero-mass labels

For `w>=1`, use exactly the rational squared-Fejer kernel `K_m` of the
[companion theorem](sparse-kernel-rounding.md#3-a-fully-explicit-positive-kernel).
It has degree `2(m-1)` in each argument, is nonnegative on the square,
preserves mass under normalized arcsine measure `mu`, and satisfies

\[
 \int T_k(y)K_m(x,y)\,d\mu(y)=g_kT_k(x),\qquad
 0\le g_k\le1,\qquad 1-g_k\le\delta_r k^2.             \tag{7}
\]

The same `m` and the same kernel are used in every bag. Define

\[
 h_{b,a}(y)=L_{b,a}\!\left(\prod_{i\in C_b}K_m(x_i,y_i)\right).
                                                                  \tag{8}
\]

The univariate interval positivity representation, multiplied across a
bag, expresses the kernel product in its full box preordering at degree
at most `2|C_b|(m-1)<=2r`. Thus (1) implies `h_{b,a}>=0`. Its integral
against `mu^{C_b}` is `tau_{b,a}`. For an empty continuous bag the empty
kernel product is one and this statement means `h_{b,a}=tau_{b,a}`.

Let the mixed bag law give label `a` and continuous coordinates in `dy`
weight `h_{b,a}(y) dmu^{C_b}(y)`. It is a probability measure. The density
of its marginal at separator label `s` is exactly

\[
 \sum_{a\in A_b:a|_{S_D}=s}
 L_{b,a}\!\left(\prod_{i\in S_C}K_m(x_i,y_i)\right).   \tag{9}
\]

Integrating an omitted continuous coordinate deletes its kernel factor;
summing an omitted finite-state coordinate gives the label sum in (9).
The remaining input polynomial has degree at most `2r`, so (2) makes
(9) identical on the two sides of each edge.

Junction-tree gluing now produces a global law with these bag marginals.
The spaces are finite products of finite sets and compact intervals, so
regular conditional laws exist. At a null separator event the conditional
law can be chosen arbitrarily. Inductively, this choice does not change any
bag marginal. Each bag marginal has zero probability of every forbidden
label. The union of these finitely many null events is null, so the global
law is supported on `A times [-1,1]^n`. No label is smoothed or rounded.

It remains to prove the objective bound without normalizing any possibly
zero mass. For `|alpha|<=r`, the identity

\[
 1-T_\alpha(x)^2
 =\sum_i(1-x_i^2)U_{\alpha_i-1}(x_i)^2
                       \prod_{j<i}T_{\alpha_j}(x_j)^2             \tag{10}
\]

has nonnegative preordering terms of degree at most `2r`; terms with
`alpha_i=0` are zero. Moment positivity and (10) give

\[
 0\le L_{b,a}(T_\alpha^2)\le\tau_{b,a},\qquad
 |L_{b,a}(T_\alpha)|^2
     \le L_{b,a}(1)L_{b,a}(T_\alpha^2)\le\tau_{b,a}^2.
                                                                  \tag{11}
\]

The middle inequality is Cauchy--Schwarz for the positive semidefinite
bilinear form `(p,q) -> L_{b,a}(pq)` on degree-at-most-`r` polynomials.
It remains valid when `tau_{b,a}=0`, and proves
`|L_{b,a}(T_alpha)|<=tau_{b,a}` in that case as well.

Kernel diagonalization gives

\[
 \int T_\alpha(y)h_{b,a}(y)\,d\mu^{C_b}(y)
       =\left(\prod_{i\in C_b}g_{\alpha_i}\right)L_{b,a}(T_\alpha).
                                                                  \tag{12}
\]

Since every objective index has `|alpha|<=d<=r`, (7), (11), and
`1-product_i g_i<=sum_i(1-g_i)` bound the absolute cost change for this
label by `delta_r tau_{b,a} H_{b,a}`. Summing proves (5). The law is
feasible, hence its mean is at least `f*`; taking the infimum over feasible
moment collections gives (6). Compactness and continuity give existence
of a feasible point with cost no greater than the mean. All integrals
and exchanges involve finite-degree polynomials on compact boxes.

## 5. Pruning and finite SDP duality

Local labels that extend to no assignment in `A` should be deleted before
claiming strict feasibility. Finite-state tree propagation can determine
these labels: pass compatibility messages in both directions along tree
edges, retaining a label precisely when it extends in every incident
component. The running-intersection property makes the component choices
compatible once the bag label is fixed.

This pruning does not change the moment optimum. Indeed (2) at `p=1`
makes the label masses consistent, so discrete junction-tree gluing alone
shows that an unextendable label has mass zero. For such a label (11)
shows `L(T_alpha^2)=0` for every `|alpha|<=r`. These polynomials form a
basis of the degree-at-most-`r` space. Positivity forces all entries of
its moment matrix to vanish. Every monomial of degree at most `2r`
factors into two monomials of degree at most `r`, so the entire functional
is zero. Removing these blocks, or reinserting them as zero, preserves
all constraints and objectives.

After pruning, take any probability distribution positive on every
assignment in the finite nonempty set `A`, independently of a continuous
product measure with positive density on the open box. Every retained
local label then has positive mass. For each nonzero polynomial `q`
occurring in a localizing matrix, the expectation of
`q^2 prod_{i in I}(1-x_i^2)` in this labelled block is strictly positive:
the weight is positive on the open box and a nonzero polynomial cannot
vanish there almost everywhere. The empty continuous bag gives a positive
one-by-one mass block. The resulting moments satisfy all equalities and
make every retained localizing matrix positive definite.

The pruned finite SDP therefore satisfies primal Slater. Its optimum is
finite by (11) and `d<=r`. Finite-dimensional SDP duality gives no duality
gap and attainment of its dual optimum. This is an exact real-arithmetic
statement about the pruned SDP; it is not a rational-certificate size
bound or a claim about strictly feasible unpruned blocks.

## 6. Finite rounding, scope, and novelty limits

For `w>=1`, the companion theorem's quadrature also retains the finite-state
labels. Let `d_infty` be the largest coordinate degree in any cost, taking zero
for constant costs, and put `N=m+floor(d_infty/2)`. Evaluating (8) at the
`N` Chebyshev quadrature nodes in each continuous coordinate, with weights
`N^{-|C_b|}`, gives nonnegative finite mixed bag tables. Quadrature exactly
preserves their masses, their separator marginals, and each bag's cost
expectation. Thus (5) also has a law supported on the original finite-state
assignments and this fixed continuous grid. Ordinary tree dynamic
programming on the tables of allowed labels and grid coordinates finds
a feasible point with at most that mean cost. This exact-arithmetic
consequence does not require constructing a density from the input SDP
point: the grid minimum satisfies (5) for every feasible moment point.

There are `sum_b |A_b|` labelled moment blocks. The finite grid has
`sum_b |A_b| N^{|C_b|}` local entries before compatibility messages.
Listing the labels can itself be exponential in the number of finite-state
variables per bag. This is not a general polynomial-time MINLP algorithm.
All kernel coefficients are rational; the extraction grid uses real
algebraic nodes. No rational-output or bit-complexity bound for extraction
from numerical SDP output is proved. Numerical SDP error and inexact
separator equality require a separate certified analysis.

The continuous domain must be the same product box for every label.
The full local preordering, including all products of box generators, is
required. No transfer to the usual quadratic module or to arbitrary local
continuous constraints is asserted. The theorem gives a quantitative gap
for the stated relaxation and exact label feasibility, without a
continuous feasibility repair step in this model.

Direct coordinate gridding followed by tree dynamic programming is an
essential comparator here as in the box-only case. Fix a globally optimal
finite-state assignment. At its continuous box minimizer, derivatives
in interior coordinates vanish. A grid containing the box endpoints can
keep boundary coordinates fixed; a uniform Hessian bound then gives a
quadratic objective error when the interior coordinates move to the grid.
Optimizing over labels and grid coordinates can only improve that candidate.
An inverse-square hierarchy rate alone therefore gives no new general
approximation-complexity exponent over elementary grid optimization.

The established ingredients and inspected rate comparisons are recorded in
the companion [prior-work audit](prior-independent.md) and
[parallel audit](kernel-prior.md). This finite-state extension is a direct
consequence of compatible box smoothing and standard finite-state tree
gluing. Its separate novelty has not been established. Its proved value is
that the sparse preordering guarantee covers this precisely stated mixed
model while preserving every discrete restriction. Faster practical
solving remains a possibility requiring separate numerical and complexity
analysis.
