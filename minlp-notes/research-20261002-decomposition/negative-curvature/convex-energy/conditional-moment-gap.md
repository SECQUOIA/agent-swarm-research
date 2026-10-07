# Exact convex energy does not supply conditional moment consistency

Date: 2026-10-02. Status: a proved limitation of one proposed relaxation
interface, with targeted exact checks and a completed
[independent research-agent review](../adversary/conditional-moment-gap-review.md).
No substantive issue remained in that review. This does not resolve the
general sparse negative-curvature algorithmic target.

The constructive idea is to retain the positive semidefinite part of the
quadratic exactly and discretize only its bounded negative curvature.
That idea has a useful general inequality. The missing step is stronger
than ordinary PSD completion: the completion must remain valid after
conditioning on a **global** choice of coordinate cells. Exact local
distributions and matching separator moments do not ensure this.

The example below has four continuous variables on the unit box, largest
bag size three, a unique optimizer, valid quadratic growth `g=1/22`, and
negative curvature exactly `nu=2`. Its local relaxation retains exact
convex energy and exact distributions within every bag. It matches
separator moments through degree three and even admits a global PSD
completion. Nevertheless its gap is at least `5/32` while every occupied
cell width tends to zero. This rules out a specific missing error bound,
not the use of PSD energy, selective filtering, or stronger consistency.

## 1. What exact PSD energy does prove

Let

\[
 F(x)=\tfrac12x^THx+b^Tx+c,\qquad H\succeq-\nu I,
 \qquad X=\prod_i[\ell_i,u_i].
\]

A lifted first/second moment pair `(m,Y)` with `m in X` and covariance
`Sigma=Y-mm^T` positive semidefinite has objective

\[
 L=\tfrac12\langle H,Y\rangle+b^Tm+c
   =F(m)+\tfrac12\langle H,\Sigma\rangle
   \ge F(m)-\tfrac\nu2\operatorname{tr}\Sigma.                 \tag{1}
\]

Thus large positive curvature causes no loss in (1). In a chordal sparse
moment formulation, compatible PSD bag matrices admit a PSD completion;
the objective uses only specified entries, so the same inequality applies.
PSD completion itself is classical; it is not a claim of this note.

If all moments refer to one box cell with coordinate widths `w_i`, the
valid interval moment inequalities give

\[
 \Sigma_{ii}\le(u_i-m_i)(m_i-\ell_i)\le w_i^2/4,
 \qquad L\ge f^*-\tfrac\nu8\sum_iw_i^2.                    \tag{2}
\]

There is also a precise sufficient mixture interface. Suppose a relaxation
admits weights `pi_alpha>=0`, summing to one, indexed by complete global
cell assignments, and pairs `(m_alpha,Y_alpha)` such that:

- `m_alpha` belongs to the selected product cell;
- `Y_alpha-m_alpha m_alpha^T` is PSD and obeys its interval moment bounds;
- the relaxation objective is the weighted sum of their quadratic
  objectives.

Applying (1)--(2) to each assignment proves

\[
 L\ge f^*-\tfrac\nu8
       \sum_\alpha\pi_\alpha\sum_i w_{i,\alpha_i}^2.       \tag{3}
\]

This proof needs no realizable distribution inside a global cell: PSD
covariance and the interval inequalities suffice. It does need a common
conditioning index for all variables. Explicitly listing that index can
have `K^n` assignments. No bound `f(p,nu/g) poly(I)` on its compressed
representation is proved here.

## 2. The weaker sparse interface being tested

For each bag and its local coordinate-cell assignment, allow an exact
nonnegative measure supported in that bag cell. These measures can be
discrete; no relaxation within a bag is necessary. Adjacent bags must agree
on the mass, first moment, and second moment of their common separator,
separately for every separator-cell assignment, after summing over the
nonseparator cell labels. The objective is the sum of the assigned bag
factor integrals. Every true feasible point supplies such measures, so
minimizing this objective is a valid lower-bound relaxation.

This is stronger than merely imposing PSD and interval bounds on each
bag-cell moment matrix. An error bound valid for that simpler relaxation
would therefore have to hold for this exact-local-measure interface too.
We also permit imposing an unconditional global PSD completion. The
following witness already satisfies that extra condition.

## 3. A uniformly conditioned family

Take rational `0<h<=1/2`, put `tau=1/16`, and use four variables
`(s,u_1,u_2,v) in [0,1]^4`. Define

\[
\begin{split}
 F_h={}&8\left(s/h-(u_1+u_2)/2\right)^2
       +8\left(s/h-1/4-v/2\right)^2\\
      &+u_1(1-u_1)+u_2(1-u_2)+v(1-v)
       +\tau(u_1+u_2+v).                                  \tag{4}
\end{split}
\]

Assign the first square and the `u` unary terms to
`B_L={s,u_1,u_2}`, and the second square and `v` unary terms to
`B_R={s,v}`. These two bags form a tree decomposition with largest bag
size three and separator `{s}`. The interaction graph contains the
triangle on `B_L` and has treewidth exactly two. For `h=2^-k`, the
input has `O(k+1)` bits because there are only four variables.

Write `t=s/h`, `w=(u_1,u_2,v)`, and

\[
 \bar t=1/8+(u_1+u_2+v)/4,\qquad \delta=t-\bar t.
\]

Direct expansion gives the exact identity

\[
 F_h-1/4
 =16\delta^2
  +2\bigl[(1-v)u_1u_2+v(1-u_1)(1-u_2)\bigr]
  +\tau(u_1+u_2+v).                                      \tag{5}
\]

The two cubic terms cancel in their sum, consistently with (4) being
quadratic. Every term on the right is nonnegative on the box. Equality
forces `w=0` and then `s=h/8`. Thus the unique optimum is

\[
 x^*=(h/8,0,0,0),\qquad f^*=1/4.                           \tag{6}
\]

For growth, `sum w_i>=||w||^2` and

\[
 (t-1/8)^2\le2\delta^2+\tfrac38\|w\|^2,
 \quad
 \|x-x^*\|^2
 \le2\delta^2+\tfrac{11}{8}\|w\|^2.                     \tag{7}
\]

The second inequality uses `h<=1`; it holds even when `t>1`.
Equations (5)--(7) imply

\[
 F_h-f^*\ge16\delta^2+\tfrac1{16}\|w\|^2
           \ge\tfrac1{22}\|x-x^*\|^2.                  \tag{8}
\]

The Hessian of the two squares is PSD, while the three concave unary
terms have Hessian `-2` on the controls and zero on `s`. Hence
`H_h>=-2I`. The vector `(0,1,-1,0)` annihilates both square residuals
and is an eigenvector with eigenvalue `-2`. Therefore the negative
curvature is **exactly** `nu=2`, and the valid ratio is `nu/g=44`.
The largest diagonal curvature is `32/h^2`; this is the quantity the
proposed new interface was meant to avoid.

## 4. Exact local distributions with a fixed gap

The left bag uses the following probability measure. The first coordinate
in the table is `t=s/h`.

| `t` | `u_1` | `u_2` | Mass |
| --- | --- | --- | --- |
| `0` | `0` | `0` | `1/8` |
| `1/2` | `1` | `0` | `3/8` |
| `1/2` | `0` | `1` | `3/8` |
| `1` | `1` | `1` | `1/8` |

The right bag uses `(t,v)=(1/4,0),(3/4,1)`, each with mass `1/2`.
All local square residuals vanish; all controls are binary, so all local
concave penalties vanish. Both separator marginals satisfy

\[
 E[t]=1/2,\quad E[t^2]=5/16,\quad E[t^3]=7/32.             \tag{9}
\]

They therefore agree on separator moments of orders zero through three.
The fourth moments differ: `11/64` on the left and `41/256` on the
right. In particular the separator distributions are different.

For dyadic `h<=1/2`, give every coordinate a uniform partition of mesh
`2h`. All separator atoms lie in the first cell `[0,2h]`; its upper
endpoint is unused, so any consistent half-open boundary convention works.
Each control atom is at a domain endpoint and belongs to an endpoint cell.
Disaggregate each bag measure by these cell labels. Matching separator
moments still holds cell-by-cell; every other separator state has zero
mass. All occupied cell widths are `2h`. The example also works on a
partition that refines only the occupied endpoint cells of the controls.

Each control has mean `1/2`. Thus the feasible relaxed objective is

\[
 L_{\rm witness}=\tau(1/2+1/2+1/2)=3/32,
 \qquad f^*-L_{\rm witness}=5/32.                         \tag{10}
\]

The relaxation optimum is at most this witness value, so its gap is at
least `5/32`. Since `nu=2` and the sum of four squared occupied cell
widths is `16h^2`, no error bound

\[
 f^*-L\le C(p,\nu/g)\,\nu\sum_iw_i^2                   \tag{11}
\]

can hold for this interface uniformly in positive curvature, even with
fixed `n=4`, `p=3`, and `nu/g=44`. Taking `h` to zero contradicts it.

This does not say an adaptive algorithm must spend many stages on (4).
Additional cell conditioning, exact min-marginal exclusions, or an explicit
valid inequality can resolve this small example. The claim concerns the
proposed direct passage from local cell moments to the error estimate.

## 5. A global PSD completion still does not repair it

The common global mean is

\[
 m=(h/2,1/2,1/2,1/2).
\]

The bag covariances have the following rational PSD completion:

\[
 \Sigma=\tfrac1{16}aa^T+\tfrac3{16}bb^T,
 \qquad a=(h,1,1,2)^T,\quad b=(0,1,-1,0)^T.             \tag{12}
\]

The restrictions of `(m,mm^T+Sigma)` to both bags are exactly the moments
of the displayed distributions. Both affine square residuals have zero
mean and zero covariance under (12), so the entire large PSD energy is
retained exactly. All global degree-two McCormick inequalities also hold
when the tighter interval `s in [0,2h]` and the original control boxes
are used. The nonedge cross moments are
`E[u_1v]=E[u_2v]=3/8`.

There is no genuine joint distribution realizing these moments on the
box. Binary control second moments force all controls to be binary almost
surely. The zero square moments would then force

\[
                   u_1+u_2-v=1/2
\]

almost surely, which is impossible. A simple violated global inequality
makes the defect visible:

\[
 u_1u_2+v-u_1v-u_2v
 =(1-v)u_1u_2+v(1-u_1)(1-u_2)\ge0.                       \tag{13}
\]

Its pseudoexpectation is `1/8+1/2-3/8-3/8=-1/8`.
Equation (13) couples variables from both sides of the separator; it is
not an inequality on either original bag.

The unconditional trace in (1) is `3/4+h^2/16`. Its three control
variances do not shrink with their occupied endpoint-cell widths, because
each control mixes distant cells. Replacing that trace by the sum of
within-cell variances would require the globally conditioned PSD
representation in Section 1. Equations (8)--(12) prove that the sparse
interface does not furnish it.

## 6. Consequence for the constructive program

Retaining convex energy works algebraically: (1) and (2) are valid and
avoid any upper bound on positive curvature. The unresolved constructive
question is how to make the **conditional** covariance and cell choices
globally consistent using only `f(p,nu/g) poly(I)` work.

Three routes remain outside this obstruction:

- derive suitable nonlocal inequalities or a sparse extended formulation
  that guarantees the globally conditioned representation in (3);
- use selective refinement and lower bounds to discard incompatible cell
  combinations without representing all of them;
- exploit additional structure that permits exact common separator laws
  or an affine convex recourse representation.

Full common separator laws on a junction tree do glue into a global
distribution, whereas finitely many common moments need not. The existing
[exponential unique-optimum message family](../../../research-20261002/new-direction/unique-message-growth-obstruction.md)
shows why switching directly to complete exact value messages does not
supply the requested state-count proof either. The
[affine recourse result](../affine-convex-recourse.md) is a separate scoped
constructive escape.

Matching the fourth separator moment already excludes the displayed
witness. This example supplies no lower bound for arbitrary higher-order
moment hierarchies or a theorem that every finite order must fail.

## 7. Literature and verification

The distinction between PSD completion and a representing probability
measure is established theory. The primary reference for chordal PSD
completion is [Grone, Johnson, Sa, and Wolkowicz (1984)](https://doi.org/10.1016/0024-3795(84)90207-6).
For sparse box-QP formulations that strengthen ordinary PSD relaxations
with products and additional structure, see
[Khajavirad (February 12, 2026), Sections 2--3](https://optimization-online.org/wp-content/uploads/2026/02/paper.pdf).
Those results impose particular structural hypotheses and extended
constraints; this note does not claim that the example defeats their
formulations. The displayed parameter-controlled example was derived
directly here; no publication-priority claim is made.

The exact checker in [check_conditional_moment_gap.py](check_conditional_moment_gap.py)
verifies the polynomial identity, optimizer and growth on rational
fixtures, the Hessian decomposition and exact negative eigenvector, the
bag distributions, moments through degree four, the rational PSD
completion, all global McCormick bounds, and the fixed objective gap.
Finite point checks supplement the universal argument, rather than prove
it. The command run was

```sh
python3 research-20261002-decomposition/negative-curvature/convex-energy/check_conditional_moment_gap.py > research-20261002-decomposition/negative-curvature/convex-energy/check-results.json
```

The [saved results](check-results.json) pass 11 family parameters,
11 symbolic polynomial identities, 2,673 exact growth point checks, and
704 global McCormick inequality checks. The smallest parameter is
`h=2^-256`, so the tests also exercise large rational coefficients without
floating-point evaluation. No project-wide checks or CI inspection were
run.
