# Hardness sanity check for the pruned shared-grid candidate

Date: 2026-10-02. Scope: compare the proposed global-point-growth,
bounded-treewidth algorithm with the strongest identified width-two
box-QP hardness reduction and relevant local mixed-variable barriers.
This is a complexity compatibility check, not an approval of the pruning
proof or a literature novelty assessment.

The examined hardness reductions do not preserve a useful uniform global
point-growth constant. In the Del Pia--Khajavirad construction, even a
family with a unique optimizer, unit boxes, bounded integer coefficients,
and treewidth two forces \(L/g\) to grow exponentially in the number of
constructed variables. The failure is quantitative, not merely an
unverified possibility of tied optima.

## 1. Primary source and exact reduction

I read Del Pia and Khajavirad, *Treewidth and the complexity of
box-constrained quadratic programs*, arXiv:2609.35595v1, Theorem 3 and its
complete proof, using the existing
[KB package](../../literature/papers/pia2026-treewidth-and-the-complexity-of/paper.md).
The equations were checked directly in the
[original PDF](../../literature/papers/pia2026-treewidth-and-the-complexity-of/original.pdf),
printed pages 21--24, because the extracted Markdown omits several
displayed equations. The public source is
[arXiv:2609.35595v1](https://arxiv.org/abs/2609.35595v1).

For a SUBSET SUM instance with item values \(a_i\) and target \(T\),
the reduction sets

\[
U=\sum_i a_i,\quad \ell=\lceil\log_2(U+1)\rceil,
\quad D=2^\ell,
\]

and encodes \(a_i\) and \(T\) by bits \(b_{ik}\) and \(t_k\).
Its objective, before removing an irrelevant constant, is

\[
\begin{aligned}
\Psi={}&\sum_i\left[x_{i1}(1-x_{i1})+
                   \sum_{k=2}^{\ell}(x_{ik}-x_{i,k-1})^2\right]\\
&+\sum_{i,k}(2z_{ik}-z_{i,k-1}-b_{ik}x_{ik})^2\\
&+\sum_i(s_i-s_{i-1}-z_{i\ell})^2\\
&+\sum_k(2w_k-w_{k-1}-t_k)^2+(s_n-w_\ell)^2.
\end{aligned}
\]

All variables lie in \([0,1]\); the zero-indexed quantities are fixed
to zero. Every term is nonnegative. A zero objective forces the \(x\)
copies to encode one binary subset and all recurrences to hold exactly.
The terminal equality then says that the subset sum is \(T\).

The paper proves that the resulting \(N=2n\ell+n+\ell\)-variable QP
has treewidth at most two and integral coefficients
\(\|Q\|_{\max}\le5\), \(\|c\|_\infty\le4\), in its convention
\(F(y)=y^TQy+c^Ty\). The construction preserves no stated lower bound
on global quadratic growth.

## 2. A unique optimum with exponentially poor growth

Take a two-item source instance

\[
a_1=A=2^r,\qquad a_2=A+1,\qquad T=A,\qquad r\ge1.
\]

Its only successful subset is \((1,0)\). The nonnegative reduction
objective therefore has a unique zero \(y^*\): the chosen binary bits
fix all copies, and the recurrences uniquely determine every other
variable. Here

\[
\ell=r+2,\qquad D=4A,\qquad N=5\ell+2=5r+12.
\]

Construct a second feasible point \(y'\) from the unsuccessful subset
\((0,1)\). Keep every bit-copy relation, bit-serial recurrence, and
partial-sum recurrence exact. Keep the target recurrence exact as well.
The only nonzero term is the last square:

\[
s_2=(A+1)/D,\qquad w_\ell=A/D,
\qquad \Psi(y')-\Psi(y^*)=D^{-2}.
\]

The two points differ by one in all \(\ell\) copies of each of the two
binary choices. Thus

\[
\|y'-y^*\|_2^2\ge2\ell.
\]

Every constant in a global fixed-point growth inequality must consequently
satisfy

\[
\boxed{g\le\frac{1}{2\ell D^2}.}
\]

The exact largest coordinate second derivative is ten: each target-state
coordinate \(w_k\) has squared coefficient five, including the final
coordinate with its terminal square. The paper's diagonal bound shows
that no coordinate has a larger second derivative. Hence any valid common
upper-coordinate-curvature bound has \(L\ge10\), and \(L=10\) works.
Therefore

\[
\boxed{\kappa=L/g\ge20\ell D^2
       =320(r+2)4^r.}
\]

This is exponential in \(N\). The reduction graph has bounded degree,
so the full Hessian norm is bounded by an absolute constant too. For
example, degree at most four and \(\|Q\|_{\max}\le5\) give the safe
bound \(\|\nabla^2F\|_2\le50\). Replacing coordinate curvature by a
supplied full Hessian norm does not remove this example's small growth
constant.

These unique instances do admit some positive global growth constant.
More generally, a quadratic objective with a unique optimizer on a compact
box has this property. To see the local point, write the exact expansion
along feasible unit directions as
\(F(x^*+tv)-f^*=t\nabla F(x^*)^Tv+t^2q(v)\).
The linear term is nonnegative. If the gap-to-squared-distance ratio
approached zero as \(t\downarrow0\), a limiting feasible tangent
direction would have both zero linear term and zero quadratic term.
The corresponding short feasible ray would consist of other optima,
contradicting uniqueness. Compactness and uniqueness bound the ratio
away from zero outside a neighborhood as well. The displayed family
shows that this positive constant need not be polynomially large.

Strong NP-hardness restricts the magnitudes of the instance coefficients;
it does not make objective gaps at continuous rational points integral.
The paper's bit-serial construction moves the original large integers
into the graph structure and generates scale \(D^{-1}\) inside unit
boxes. Squaring a one-unit subset discrepancy produces exactly the
\(D^{-2}\) gap above.

## 3. Local mixed-variable hardness has the same distinction

The repository's
[indicator-quadratic hardness result](../../results/indicator-quadratic-treewidth-two-hardness.md)
has two additional qualifications. Its original indicator relations
\(v_j(1-z_j)=0\) do not define a Cartesian mixed box. Also, a
near-identity continuous Hessian on each support says nothing by itself
about objective separation between distinct supports. An independent
reviewer checked explicit unique-support examples with global growth
of order \(B^{-2}\) when the source target \(B\) is binary encoded.
Replacing indicator wells by product-box squares preserves that
conditioning problem rather than resolving it.

The simpler local
[modewise-growth barrier](../new-direction/modewise-growth-barrier.md)
already supplies a genuine product-box example with constant full Hessian
norm. For two items \(a_1=B\), \(a_2=B-1\), it has unique optimum
mode \((1,0)\), state vector \((1/2,1/4)\), and value zero. The
other mode \((0,1)\) has a feasible recurrence trajectory
\((0,(B-1)/(4B))\) with gap \(1/(16B^2)\). Including the two binary
coordinate differences gives

\[
\|y'-y^*\|^2=\frac94+\frac1{16B^2},\qquad
g_{\rm full}\le\frac1{36B^2+1}.
\]

Its largest coordinate curvature is four, so
\(L/g_{\rm full}\ge144B^2+4\). Every continuous mode nevertheless
retains a constant strong-convexity bound. This directly distinguishes
the candidate's global fixed-point growth promise from modewise
conditioning.

These two-item examples demonstrate conditioning failure, not
fixed-dimensional NP-hardness. The hardness reductions use variable
dimension.

## 4. Consequence for the candidate claim

The examined reductions do not contradict an algorithm parameterized by
treewidth and \(L/g\). They do contradict dropping global growth,
replacing it by unique optimality without a quantitative constant, or
replacing it by conditioning only within each discrete mode.

For a bounded-conditioning claim, the relevant reduction would have to
preserve the global growth promise and a sufficiently small curvature-to-
growth ratio. Bounded coefficients and strong NP-hardness alone do not
establish that promise. The primary reduction explicitly fails to give a
uniform polynomial bound, as the family above demonstrates. This does
not exclude a different hardness reduction satisfying additional
promises; no such reduction has been established by this check.

Conversely, this compatibility finding does not validate the new
algorithm. The min-marginal lower-bound validity, optimizer-preserving
cuts, contraction on restricted domains, per-stage grid count, absolute
input exponent, arithmetic growth, and unknown-constant scheduling each
need their independent proofs. This report approves none of those steps
merely because a known hardness contradiction is absent.

## 5. Verification record

The primary theorem and full reduction were read from the existing KB
using targeted `rg` and `sed` reads and
`pdftotext -f 21 -l 24 -layout .../original.pdf -`.
The displayed conditioning bounds were derived algebraically. A
delegated reviewer independently read the primary reduction from the PDF
and confirmed the unique-optimizer family, all constants, and the
qualitative growth lemma, in addition to examining the local mixed-variable
hardness examples. No literature search or ingestion, executable
optimization checks, project-wide verification, or CI inspection was
performed by this reviewer.
