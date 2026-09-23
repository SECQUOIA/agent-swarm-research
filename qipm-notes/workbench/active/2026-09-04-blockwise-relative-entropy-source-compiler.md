# A blockwise relative-entropy source compiler

Status: Proved; independently audited; literature boundary identified  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on theorem; moderate on novelty and impact

## Construction

Let \(N=Bm\), with \(B\) blocks of \(m\) oracle slots.  In block \(j\),
exactly one slot \(r_j\in[m]\) has

\[
 d_{j,r_j}=e^{-\gamma_{r_j}},
\]

while all other slots have \(d_{ji}=1\).  Choose public
\(\gamma_1<\cdots<\gamma_m\) in \([1,2]\), with spacing
\(h=\Theta(1/m)\).  All terms in a block share scalar variables
\(U_j,V_j\).

For homogeneous scalar relative entropy,

\[
 \sum_{i=1}^m D(U_j\|d_{ji}V_j)
 =mU_j\log(U_j/V_j)+\gamma_{r_j}U_j
 =D(mU_j\|m e^{-\gamma_{r_j}/m}V_j).                         \tag{1}
\]

Thus projection of \(N\) source epigraphs is exactly \(B\) ordinary
relative-entropy epigraphs.  Projection is literal: sum the local epigraph
variables in each block; conversely, allocate any aggregate nonnegative slack
among the local epigraph variables.

An aligned binary aggregation and vector-copy tree gives a scalar lift with
constant row/column incidence and scalar KKT treewidth \(O(1)\).  For
\(n\times n\) matrix variables the analogous scalarized width grows with the
matrix block size; no constant-width matrix claim is made.

## Tight source-erasing acquisition

An explicit reusable compiler that erases the source oracle must identify all
\(r_j\), or equivalently output all effective coefficients in (1).  Grover
search in every block gives

\[
 Q=O(B\sqrt m)=O(\sqrt{NB})
\]

quantum queries; exhaustive randomized search costs \(O(Bm)=O(N)\).
Both are optimal:

\[
 \boxed{Q=\Theta(\sqrt{NB}),\qquad R=\Theta(N).}             \tag{2}
\]

For the quantum lower bound, index inputs by
\((r_1,\ldots,r_B)\in[m]^B\) and take the adversary matrix

\[
 \Gamma=\sum_{j=1}^B
 I^{\otimes(j-1)}\otimes(J-I)\otimes I^{\otimes(B-j)}.
\]

Its norm is \(B(m-1)\).  Schur multiplication by a query-difference matrix
for one slot kills every summand except that slot's block, whose norm is
\(\sqrt{m-1}\).  Hence
\(\operatorname{Adv}^{\pm}=\Omega(B\sqrt m)\).

This is an explicit/source-erasing output theorem.  A coherent implicit
oracle that continues querying the original data can answer a block request
in \(O(\sqrt m)\) queries and need not pay (2) once and for all.

## Full projected-solution decoder

Fix \(U_j=V_j=1\), use one aggregate epigraph coordinate \(t_j\) per block,
and minimize \(\sum_jt_j\).  Equation (1) gives the unique lower boundary

\[
 t_j^*=\gamma_{r_j}.
\]

For an exactly feasible vector, write
\(e_j=t_j-\gamma_{r_j}\geq0\).  If its total objective excess is below
\(h/3\), then every \(e_j<h/3\), and rounding every \(t_j\) recovers all
marked locations.  Therefore the bounds (2) apply to this full
coordinate-readable projected solution task at objective accuracy
\(\Theta(1/m)\).

This is not a value-only lower bound: the sum \(\sum_j\gamma_{r_j}\) can have
collisions.  It is also not a normalized quantum-state lower bound.  If
coordinate feasibility violations are permitted, their total negative part
must be included; a generic per-block violation bound may need
\(O(1/(Bm))\) accuracy.

## Exact fixed-slice path comparison

On the fixed slice \(U_j=V_j=1\), the natural product barrier has one
logarithmic epigraph slack per source term.  At barrier multiplier \(\eta\),
each slack is \(1/\eta\), the total objective gap is \(N/\eta\), and the
projected block slack is \(m/\eta\).  The compiled barrier has one slack per
block, total gap \(B/\widehat\eta\), and block slack
\(1/\widehat\eta\).

At matched total gap \(\Delta\), take

\[
 \eta=N/\Delta,qquad \widehat\eta=B/\Delta.
\]

The projected central points then coincide, and their exact barrier-metric
lengths between gaps \(\Delta_0\) and \(\epsilon\) are

\[
 L_{\rm natural}=\sqrt N\log(\Delta_0/\epsilon),
 \qquad
 L_{\rm compiled}=\sqrt B\log(\Delta_0/\epsilon).            \tag{3}
\]

They do not coincide at equal barrier multipliers, and (3) is only the stated
fixed-variable epigraph slice, not a general path theorem with moving
\(U_j,V_j\).

## Novelty boundary

By the
[exact exponential-product barrier theorem](2026-09-04-exponential-product-exact-barrier-parameter.md),
\(3N\) and \(3B\) are the exact optimal barrier parameters of the two
displayed full ambient exponential-cone products, even against arbitrary
coupled standard self-concordant barriers.  They are still not intrinsic
lower bounds for a barrier on the projected feasible image or on a different
formulation.  Fawzi--Saunderson already
give small optimal barriers for noncommutative perspectives, and
He--Saunderson--Fawzi explicitly exploit shared positive-map structure in QRE
programs.  Equation (1) is also an elementary specialization of the
two-moment identity in the
[dilation-rank note](2026-09-04-dilation-rank-perspective-compilers.md).

The defensible contribution is the complete source-access theorem (2), its
coordinate-readable optimization decoder, and the exact matched-gap metric
comparison (3), all on a bounded-incidence scalar nonsymmetric-cone lift.
It is best viewed as a data-loading/formulation separation rather than a new
QRE barrier theorem.
