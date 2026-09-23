# Pareto-active SOC compilation with a coupled two-dimensional postproblem

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on construction and query bounds; moderate on novelty  

## Statement

For \(1\leq k\leq N/2\), there is a family of sparse, strictly feasible SOCP
lifts with:

- \(N+1\) constant-rank Lorentz-cone factors and a path factor graph of block
  treewidth one;
- exactly \(k+1\) irredundant projected cone factors on the hard inputs;
- quantum exact reusable compilation cost
  \(\Theta(\sqrt{Nk})\) queries and randomized cost \(\Theta(N)\);
- a natural lifted product barrier whose parameter certificate is at least
  \(N-k+1\), versus an explicit compiled barrier with certificate at most
  \(k+1\); and
- an exact natural-barrier path length
  \(\Theta(\sqrt{N-k+1}\log(1/\epsilon))\), versus compiled length
  \(\Theta(\sqrt{k}+\log(1/\epsilon))\).

Unlike the chain-cover example, the \(k\) retained constraints are mutually
incomparable and define a genuinely coupled two-dimensional intersection.
The lower bound is for an objective-oblivious exact reusable compiler, not for
solving one fixed objective.

## Ellipse family

Put

\[
 u_i=\frac{i}{2(N+1)},\qquad
 q(v)=(1+v,3-v^2),\qquad q_*=(2,2)=q(1),
\]

and \(q_i^-=(1+u_i,1)\).  For \(q=(a,b)>0\), let

\[
 E(q)=\{z\in\mathbb R^2:az_1^2+bz_2^2<1\}.
\]

This is an affine slice of a linearly transformed \(Q_3\).  Coordinatewise
larger \(q\) gives a smaller ellipse.  An input trit
\(\sigma_i\in\{0,+,-\}\) selects respectively \(q_*,q(u_i),q_i^-\), and a
public sentinel \(E(q_*)\) is always present.  Consensus copies of \(z\) are
linked along a path.

The minus factors are dominated by the sentinel and zero factors duplicate
it.  Consequently the exact projected domain is

\[
 D_\sigma=E(q_*)\cap\bigcap_{i\in S}E(q(u_i)),
 \qquad S=\{i:\sigma_i=+\}.
\]

All scalar coefficients lie in \([1,3]\), \(z=0\) is a strict point, every
row has constant support, and the lifted scalar KKT graph has constant
treewidth.

## Irredundance and coupling

For every retained \(v\in\{1\}\cup\{u_i:i\in S\}\), set \(s_v=(2v,1)\).
The identity

\[
 \langle q(v)-q(w),s_v\rangle=(v-w)^2
\]

shows that the point whose squared coordinates are

\[
 (z_1^2,z_2^2)=
 \frac{s_v}{\langle q(v),s_v\rangle}
\]

lies on \(E(q(v))\) and strictly inside every other retained ellipse.  Hence
every factor is essential, and different subsets \(S\) define different
bodies.

There is also a two-active-factor witness.  If \(v<w\) are adjacent retained
parameters and \(s=(v+w,1)\), then

\[
 \langle q(r)-q(v),s\rangle=(r-v)(w-r).
\]

The point with squared coordinates \(s/\langle q(v),s\rangle\) has exactly
the \(v\) and \(w\) ellipses tight.  A positive combination of their outward
normals exposes this point, so generic linear objectives genuinely use two
active cones.  The projected problem is not a list of \(k\) independent
scalar minima.

## Tight compilation complexity

Under the promise \(|S|=k\) and coherent trit access, repeated all-solutions
Grover search recovers \(S\) in \(O(\sqrt{Nk})\) queries.  It then writes the
exact \(k+1\)-factor projected barrier

\[
 \Phi_c(z)=F_*(z)+\sum_{i\in S}F_i(z),\qquad
 F_q(z)=-\log(1-z^T\operatorname{Diag}(q)z).
\]

For the lower bound, divide the \(N\) positions into \(k\) public blocks of
size \(m=\lfloor N/k\rfloor\), promise exactly one plus trit per block, and
make all other trits zero.  Because the resulting bodies are distinct and
every marked ellipse is irredundant, a source-independent classical
description supporting exact reusable membership, boundary evaluation, or
barrier evaluation must identify all \(k\) marked positions.  The direct-sum
adversary for \(k\) unique searches gives

\[
 Q=\Omega(k\sqrt m)=\Omega(\sqrt{Nk}).
\]

Randomized query complexity is \(\Theta(N)\).  Thus the quantum upper bound is
optimal for this exact reusable-output contract.

## Barrier parameter separation

On the hard branch, the natural lifted product barrier reduces after
consensus to

\[
 \Phi_o=(N-k+1)F_*+\sum_{i\in S}F_i.
\]

It has the standard certificate at most \(N+1\).  The certificate is also at
least \(N-k+1\): approach a sentinel-only boundary point, where all marked
ellipses retain uniform slack.  In the singular normal direction,
\(\nabla\Phi_o^T(\nabla^2\Phi_o)^{-1}\nabla\Phi_o\to N-k+1\).
The compiled sum has certificate at most \(k+1\).

This is a separation between explicit local product barriers.  Since the
projected dimension is two, a nonlocal universal or entropic barrier has
constant existential parameter; no all-barriers lower bound is claimed.

## Exact path-length separation

Take objective \(e_1^Tz\).  Symmetry makes both exact central paths lie on
\(z=(a,0)\), \(0\leq a<1/\sqrt2\), and traverse the same scalar interval.
For \(F_A(a)=-\log(1-Aa^2)\),

\[
 F_A''(a)=\frac{2A(1+Aa^2)}{(1-Aa^2)^2}.
\]

The marked coefficients satisfy \(A=1+u_i\leq3/2\), so their Hessians are
uniformly \(\Theta(1)\) on the full interval.  For the sentinel \(A=2\),

\[
 \int_0^{1/\sqrt2-\epsilon}\sqrt{F_2''(a)}\,da
 =\Theta(\log(1/\epsilon)).
\]

Writing \(M=N-k+1\) and using \(M\geq k\),

\[
 L_o(\epsilon)=\Theta(\sqrt M\log(1/\epsilon)),
\qquad
 L_c(\epsilon)=\Theta(\sqrt k+\log(1/\epsilon)).
\]

The ratio is \(\Theta(\sqrt{N/k})\) at ordinary accuracy and approaches
\(\Theta(\sqrt N)\) when \(\log(1/\epsilon)\gg\sqrt k\).  Moreover, since
\(\nabla^2\Phi_o\succeq M\nabla^2F_*\), any schedule starting at zero with
natural-barrier Dikin steps bounded by a fixed \(\rho<1\) needs
\(\Omega_\rho(\sqrt M\log(1/\epsilon))\) moves.

## Access-model closure and novelty boundary

Public copying reconstructs every lifted coordinate from the two-dimensional
solution.  If the trits are instead explicit bounded-fan-in wires, producing
the \(k\) marked indices needs depth \(\Omega(\log(N/k))\) and, away from
degenerate block size two, \(\Omega(N)\) source incidences; parallel priority
encoders match these bounds.

Search in posets, planar skyline algorithms, redundant-constraint presolve,
and sums of cone barriers are prior art.  The apparent novelty is the combined
Pareto-SOC construction: exact irredundant body compilation, a tight
\(\sqrt{Nk}\) query law, constant-treewidth lift, two-active-cone coupling,
and the uniform barrier/path/access separation.  A targeted literature search
has not found this conjunction, but priority is not guaranteed.

The [growing-dimensional block construction](2026-09-04-kblock-pareto-soc-compiler.md)
adds a fixed-objective full-vector decoder.  The present note instead keeps a
genuinely shared two-dimensional frontier and proves the two-active-cone
witness; the two results have different strengths.
