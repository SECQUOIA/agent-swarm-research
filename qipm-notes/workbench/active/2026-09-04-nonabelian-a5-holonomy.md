# Intrinsically nonabelian word hardness and sparse SDP transfer

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem; moderate-to-high on apparent novelty  
Question: Can the group-holonomy SDP lower bound use a genuinely noncommuting
promise rather than a cyclic restriction?

## Word-query theorem

Let \(G=A_5\) and let \(C_3\subset A_5\) be the conjugacy class of its twenty
3-cycles. Given

\[
 (g_1,\ldots,g_N)\in G^N,\qquad w=g_N\cdots g_1,
\]

through a coherent local-symbol oracle, promise that either \(w=e\) or
\(w\in C_3\). Distinguishing the cases with bounded error has quantum query
complexity

\[
 \boxed{Q=\Theta(N).}
\]

This is intrinsically nonabelian: every coordinate ranges over all of \(A_5\),
the adversary uses all twenty noncommuting 3-cycles, and the perfect group
\(A_5\) has trivial abelianization, so no abelian quotient separates the two
promise classes.

### Generating-word strengthening

The lower bound survives after restricting both promise fibers to tuples whose
entries generate all of \(A_5\). More generally, for a fixed finite noncyclic
group and a nonidentity conjugacy class, delete every tuple contained in a
maximal proper subgroup from the full-fiber incidence adversary. The deleted
vertex and edge fractions are \(O(\rho^N)\), where
\(\rho=\max_{H<G}|H|/|G|<1\). Restricting an adversary cannot increase a
filtered coordinate norm, while its norm loses only the deleted edge fraction.
Consequently

\[
 \operatorname{Adv}\geq N(1-O(\rho^N)).
\]

For \(A_5\), an exact version uses the conjugacy class \(C_{2,2}\) of fifteen
double transpositions. The maximal proper subgroups are five \(A_4\)'s, six
\(D_5\)'s, and ten \(S_3\)'s. Direct counting gives

\[
 \delta_X\leq5(1/5)^{N-1}+6(1/6)^{N-1}+10(1/10)^{N-1},
\]

\[
 \delta_Y\leq(1/5)^{N-1}+2(1/6)^{N-1}+2(1/10)^{N-1}.
\]

The induced adversary on generating tuples has ratio at least
\(N(1-\delta_X-\delta_Y)=\Omega(N)\); already for \(N=3\) the parenthesis is
positive. Every individual promised word now uses symbols generating the
whole nonabelian simple group, so there is literally no cyclic- or proper-
subgroup-supported promised input.

## Adversary proof

Let \(X=\{x:w(x)=e\}\), \(Y=\{y:w(y)\in C_3\}\), and let
\(\Gamma[x,y]=1\) exactly when \(x,y\) differ in one coordinate. Fix a
coordinate \(i\) and write

\[
 w(x)=L_ix_iR_i,
 \quad L_i=x_N\cdots x_{i+1},
 \quad R_i=x_{i-1}\cdots x_1.
\]

For \(x\in X\) and \(c\in C_3\), the unique coordinate-\(i\) neighbor with
product \(c\) is obtained by setting

\[
 y_i=L_i^{-1}cR_i^{-1}.
\]

Conversely, every \(y\in Y\) has one coordinate-\(i\) neighbor in \(X\),
obtained by setting \(x_i=L_i^{-1}R_i^{-1}\). Hence \(\Gamma\) is
\((20N,N)\)-biregular, while \(\Gamma\circ\Delta_i\) is a disjoint union of
20-leaf stars. Therefore

\[
 \|\Gamma\|=N\sqrt{20},\qquad
 \|\Gamma\circ\Delta_i\|=\sqrt{20}.
\]

The adversary ratio is \(N\), and reading all symbols supplies the matching
upper bound.

The promise has no hidden classical shortcut: under the uniform distribution
on either fiber, every marginal on fewer than \(N\) coordinates is uniform on
the corresponding Cartesian power of \(A_5\).

## Sparse holonomy SDP consequence

Use the natural five-point permutation representation \(U:A_5\to O(5)\) in
the existing copied trace-one holonomy construction, with \(d=5\), block order
\(k=3d=15\), and cost scale \(u=1/10\). If \(W=U_w\), the triangle connection
matrix has eigenvalues

\[
 2\cos((\theta+2\pi\ell)/3),\qquad \ell=0,1,2,
\]

for every \(e^{i\theta}\in\operatorname{spec}(W)\). Therefore

\[
 v_e=15-\frac1{10}=14.9,
\]

whereas a 3-cycle, with permutation spectrum
\(1^3,\omega,\bar\omega\), gives

\[
 v_3=15+\frac15\cos(8\pi/9)\approx14.8120614758.
\]

The constant gap is

\[
 \Delta=v_e-v_3\approx0.0879385242.
\]

Thus additive error \(1/25\), or relative error \(1/400\), distinguishes the
promise cases.

With \(K=16N\), the copied construction has \(P=2K+N=33N\) PSD blocks of
order 15, \(\Theta(N)\) variables, constraints, and nonzeros, and constant
row/column incidence. In `svec` coordinates there are
\(120P=3960N\) primal scalar coordinates and \(3960N-119\) equality rows.
A clean sparse-coefficient query is simulated by at most two \(A_5\)-symbol
queries using a fixed reversible lookup for the induced permutation. Hence
constant-accuracy value estimation needs

\[
 \Omega(N)=\Omega(P)
\]

raw sparse queries.

## Condition-one Newton-state consequence

At the public point \(X_i^{(0)}=I_{15}/15\) and \(\mu=1/P\), the reduced
Hessian is \(15^2I\), its condition number is exactly one, and the free-root
Newton direction is

\[
 \Delta Z_W=-\frac{u}{15^2}A_W.
\]

Its normalization is public, the Newton decrement is
\(u\sqrt{2/15}=\sqrt{30}/150\), and the full step stays positive definite.
Let \(J\) swap the `svec` coordinates of the \((1,2)\) and \((1,3)\)
off-diagonal blocks. On the normalized root direction, and on every copied
physical direction,

\[
 \langle J\rangle=\frac{2\operatorname{tr}(W)}{15}.
\]

This is \(2/3\) for the identity and \(4/15\) for a 3-cycle. The public
contraction

\[
 T_{A_5}=\frac{15}{22}J-\frac7{22}I
\]

has expectations \(+3/22\) and \(-3/22\), respectively. A constant number of
measurements therefore distinguishes the cases, even after trace-distance
error \(1/100\). Preparing either the normalized root or global primal Newton
direction consequently requires \(\Omega(N)\) raw queries, although the
reduced Hessian has condition number one and the primal-barrier KKT sparsity
graph is a forest.

The same argument yields an \(\Omega(N)\) setup-plus-first-call lower bound for
a sufficiently accurate tangent-projector block encoding. It does not yet
give the complete primal-plus-multiplier KKT-state decoder, whose earlier proof
used the special diagonalization of a fixed transposition.

For the generating-word version with \(C_{2,2}\), the SDP constants become
especially clean. A double transposition has permutation spectrum
\(1^3,(-1)^2\), so

\[
 v_{C_{2,2}}=15-1/5=14.8,
\]

giving the exact value gap \(1/10\) from the identity case. Its trace is one,
so \(\langle J\rangle=2/15\); the contraction

\[
 T=(5/7)J-(2/7)I
\]

has exact expectations \(+4/21\) and \(-4/21\). This is the strongest and
cleanest version for a final theorem statement.

## Prior art and defensible novelty statement

The closest group-query sources found were
Bucicovschi--Copeland--Meyer--Pommersheim,
[arXiv:1503.05548](https://arxiv.org/abs/1503.05548), on two-element quantum
group multiplication; Meyer--Pommersheim,
[arXiv:1107.1940](https://arxiv.org/abs/1107.1940), on cyclic multi-query sums;
and Copeland--Pommersheim,
[arXiv:1812.09428](https://arxiv.org/abs/1812.09428), on symmetric-oracle/coset
identification. A targeted search found no long-word identity-versus-
conjugacy-class query lower bound or holonomy-SDP transfer.

The adversary calculation may be folklore. The defensible apparent novelty is
the full-\(A_5\) class-fiber theorem and its constant-gap, bounded-incidence,
condition-one sparse SDP and Newton-state realization. This closes open problem
A5 in the paper without using an abelian subgroup restriction.
