# A constant-treewidth \(k\)-block Pareto-SOC compiler

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on theorem; moderate on apparent novelty  

## Theorem

Let \(N=km\), with \(m\geq2\).  There is a rational, bounded-incidence,
constant-treewidth SOCP lift with \(N\) hidden cone factors and \(k\) public
sentinels such that:

\[
 Q=\Theta(\sqrt{Nk}),\qquad R=\Theta(N)
\]

queries are necessary and sufficient both to compile the exact active
projected cone system and to solve one fixed linear objective to
coordinate error below \(1/[40(m+1)]\).  After compilation exactly \(2k\)
incomparable cone factors remain on a \(2k+1\)-dimensional affine space.

The natural and compiled explicit log barriers have sharp orders

\[
 \nu_o=\Theta(N),\qquad \nu_c=\Theta(k),
\]

and, for a separate public path objective, exact central-path lengths

\[
 L_o(\epsilon)=\Theta(\sqrt N\log(1/\epsilon)),\qquad
 L_c(\epsilon)=\Theta(\sqrt k\log(1/\epsilon)).
\]

Thus the barrier/path compression and oracle-query advantage have the same
factor \(\sqrt{N/k}\).

## Rational cone family

For \(\ell\in[m]\), put

\[
 u_\ell=\frac{\ell}{2(m+1)},\qquad
 Q_*=4I_3,\qquad
 Q_\ell=\operatorname{Diag}
 \bigl(1,(1+u_\ell)^2,(3-u_\ell)^2\bigr).
\]

In block \(j\), use coordinates \((y_j,p_j,q_j)\).  The public sentinel is

\[
 4y_j^2+4p_j^2+4q_j^2<1,
\]

and hidden slot \(\ell\) either duplicates the sentinel or, when marked,
imposes

\[
 y_j^2+(1+u_\ell)^2p_j^2+(3-u_\ell)^2q_j^2<1.          \tag{1}
\]

Each block contains exactly one mark.  These are direct \(Q_4\) slices:

\[
 (1,2y_j,2p_j,2q_j)\in Q_4,\qquad
 (1,y_j,(1+u_\ell)p_j,(3-u_\ell)q_j)\in Q_4.
\]

The coefficients are rational with \(O(\log m)\) bits.  Identify the
\(y_j\)'s across blocks by path consensus.  To keep both row and column
incidence bounded, give each slot a full triple copy, enforce triple
consensus along a path inside its block, and connect only representative
\(y\)-copies between blocks.  The resulting scalar/KKT graph has
treewidth \(O(1)\), constant degree, and \(\Theta(N)\) lifted size.

## Every surviving factor is essential

The matrices \(Q_\ell\) are pairwise Loewner-incomparable: their \(p\)
coefficient increases with \(\ell\), while their \(q\) coefficient decreases.
They are also incomparable with \(Q_*\).

For the marked factor, set \(y=p=0\) and
\(q=(3-u_\ell)^{-1}\).  It is tight, while the sentinel value is

\[
 \frac4{(3-u_\ell)^2}<1.
\]

For the sentinel, set \(y=q=0,p=1/2\); every marked value is
\((1+u_\ell)^2/4<1\).  Hence both factors in every block own a boundary
patch, all \(2k\) compiled factors are essential, and distinct marked
locations give distinct projected bodies.

## Tight query bounds and a fixed decoding objective

Finding the unique mark in every block takes
\[
 O(k\sqrt m)=O(\sqrt{Nk})
\]
quantum queries.  The direct-sum adversary for \(k\) independent unique
searches gives the matching lower bound; randomized query complexity is
\(\Theta(N)\).

This lower bound also holds for one fixed optimization task, not only a
reusable body compiler.  Maximize

\[
 \sum_{j=1}^k q_j.
\]

The unique optimum has

\[
 y=p_j=0,\qquad
 q_j^*=\frac1{3-u_{\ell_j}},
\]

where \(\ell_j\) is the marked location in block \(j\).  Adjacent possible
values differ by at least

\[
 \frac1{18(m+1)}.
\]

Every feasible coordinate satisfies \(q_j\leq q_j^*\), so total objective
gap below \(1/[40(m+1)]\) bounds every coordinate deficit tightly enough to
recover all \(\ell_j\).  This proves the lower bounds for a materialized
full solution or a coordinate oracle with the stated precision.  It does not
apply to objective value alone or merely an amplitude-encoded vector.

After the marks are known, the fixed problem is solved in \(O(k)\) arithmetic.
Thus the oracle-model end-to-end costs are

\[
 \widetilde O(\sqrt{Nk}+k)
 \quad\text{quantum preprocessing/solve},\qquad
 \Theta(N)
 \quad\text{randomized classical}.
\]

This is active-cone discovery, not a QLSA advantage.

## Exact barrier and path separation

Let

\[
 f_A(y)=-\log(1-Ay^2).
\]

After consensus elimination, the natural and compiled barriers restricted to
the ray \(p_j=q_j=0\) are exactly

\[
 \Phi_o(y)=Nf_4(y)+kf_1(y),\qquad
 \Phi_c(y)=kf_4(y)+kf_1(y).                          \tag{2}
\]

The coefficient \(N\) counts, in every block, the public sentinel plus the
\(m-1\) unmarked sentinel duplicates.  Since

\[
 f_A''(y)=\frac{2A(1+Ay^2)}{(1-Ay^2)^2},
\]

the max-\(y\) exact central paths both traverse
\(0\leq y<1/2\), and (2) gives uniformly

\[
 L_o(\epsilon)=\Theta(\sqrt N\log(1/\epsilon)),\qquad
 L_c(\epsilon)=\Theta(\sqrt k\log(1/\epsilon)).
\]

Approaching the common sentinel boundary, the Newton-decrement certificate
for the full barriers tends respectively to \(N\) and \(k\).  Additivity
gives upper certificates \(N+k\) and \(2k\), proving
\(\nu_o=\Theta(N)\) and \(\nu_c=\Theta(k)\).  The max-\(y\) objective is used
for this exact path theorem; the decoding objective above is intentionally
different.

The compiled postproblem is non-product because of the common \(y\), but it
is only rank-one coupled and conditionally separable.  Specialized classical
solution after compilation is near-linear in \(k\).

## Access and novelty boundaries

If the \(N\) slots are explicit bounded-fan-in input wires, outputting the
\(k\) marked indices requires depth \(\Omega(\log(N/k))\) and, for
\(m\geq4\), \(\Omega(N)\) source incidences.  Parallel classical priority
encoders match these bounds.  The speedup assumes a coherent input oracle or
prebuilt data structure.

Redundant constraints inflating product-barrier parameters, classical
presolve, Grover search, and skyline enumeration are prior art.  The
apparently new conjunction is a hidden family of essential anisotropic SOC
factors with a tight all-solutions query law, a fixed-objective recovery
lower bound, constant-treewidth bounded-incidence lift, and exact
\(\Theta(N)\)-to-\(\Theta(k)\) barrier/path compression.  A targeted search
found no collision, but priority is not guaranteed.

The [fixed-dimensional companion](2026-09-04-pareto-soc-barrier-compiler.md)
has a genuinely coupled two-dimensional Pareto frontier.  This note trades
fixed projected dimension for a coordinate-readable fixed-objective lower
bound; after compilation its blocks remain only rank-one coupled through the
shared scalar.
