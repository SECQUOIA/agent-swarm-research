# A resistance frontier for bounded-arity character-linear parity LPs

Date: 2026-09-02

## Scope relative to the later general theorem

The single-flip mixture theorem in
2026-09-02-single-flip-mixture-frontier-sparse-lps.md is the stronger default
obstruction: it covers arbitrary sparse rows and auxiliary variables without
Walsh-character or homogeneity assumptions. The present theorem remains useful
as a structural and geometric explanation of the same \(mA^2H^2\) frontier
for character-linear propagation systems, and because its interpolating
witness is constructed within one fixed instance rather than by averaging
exact witnesses from neighboring instances.

## Main result

The cut--resistance obstruction for signed graph equalities extends to arbitrary
constant-arity homogeneous linear rows, provided the intended exact wire values
are signed products of the input bits and every coefficient depends on only a
constant number of bits.

Consider \(m\) propagation rows of arity at most \(q\). Suppose coefficient
magnitudes are at most \(A\), every coefficient character contains at most \(k\)
input signs, and every intended wire height is at most \(H\). If root wires carry
the trivial character and designated output wires carry \(N\)-bit parity, then
there is an output-erasing, nonnegative, exactly objective-optimal point with

\[
 \|r\|_2^2
 \le \frac{4k^2q^3mA^2H^2}{N^2}.                        \tag{1}
\]

Consequently, for fixed \(k,q\), constant residual soundness of this entire
multi-variable class requires

\[
                    mA^2H^2=\Omega(N^2).                 \tag{2}
\]

Thus bounded-arity hyperedges, auxiliary product wires, and constant-locality
linear combinations do not by themselves evade the dimension--row-scale--
solution-scale frontier. At linear size and bounded coefficients, the intended
wire height must still be \(\Omega(\sqrt N)\).

The proof is not a reduction of a hyperedge to an asserted pairwise equality.
Walsh-character independence first decomposes each valid row into exact
zero-sum character groups. Each group is then bounded by a star energy, after
which a bounded-congestion Nash--Williams argument applies.

## Model

Let

\[
 \chi_J(\sigma)=\prod_{i\in J}\sigma_i,
 \qquad \sigma\in\{-1,+1\}^N,
\]

be the Walsh characters. There is a set \(V\) of signed wire variables. Wire
\(v\) has public height \(h_v\in(0,H]\), public character label
\(J_v\subseteq[N]\), and intended exact value

\[
                     d_v^*(\sigma)=h_v\chi_{J_v}(\sigma). \tag{3}
\]

At least one anchored root wire \(r\) has \(J_r=\varnothing\). Every designated
output \(s\in S\) has \(J_s=[N]\), up to a public fixed sign that can be gauged
away.

Propagation row \(a\in[m]\) is homogeneous and has support
\(V_a\), \(|V_a|\le q\):

\[
 \sum_{v\in V_a}
   \alpha_{av}\chi_{I_{av}}(\sigma)d_v=0,
 \qquad
 |\alpha_{av}|\le A,\quad |I_{av}|\le k.                 \tag{4}
\]

Every row is valid at (3) for every input \(\sigma\). Coherent access to one
coefficient in (4) is simulated with at most \(k\) raw sign queries.

For the nonnegative LP embedding, represent \(d_v=u_v-v_v\), put
\(q_v=u_v+v_v\), fix a positive reference variable to \(h_v\), and impose the
usual cap

\[
 q_v+t_v-2h_v=0,\qquad u_v,v_v,h_v,t_v\ge0.              \tag{5}
\]

The local objective is \(2u_v+2v_v+h_v+t_v\). The reference, cap, and anchor
rows are not included among the \(m\) propagation rows and will be satisfied
exactly by the obstruction.

Assume that the comparison graph defined in the proof connects the anchored
root component to the outputs. If it does not, the output character is
unconstrained by (4), and the theorem holds with zero propagation residual.

## Theorem 1 (bounded-arity Walsh-row frontier)

Under (3)--(5), there is \(x\ge0\) satisfying every reference, cap, and root
anchor exactly, with

\[
                         d_s=0\qquad(s\in S),             \tag{6}
\]

and propagation residual bounded by (1). Its objective is equal to the exact
optimum of the intended feasible family.

If the right-hand side consists of one unit difference anchor and one unit
reference anchor, so that \(\|b\|_2=\sqrt2\), any theorem claiming that relative
residual at most \(\eta\) forces a nonzero parity signal on \(S\) must satisfy

\[
             4k^2q^3mA^2H^2>2\eta^2N^2.                 \tag{7}
\]

### Proof

#### 1. Walsh decomposition of every valid row

Substitute (3) into row (4):

\[
 \sum_{v\in V_a}
   \beta_{av}\chi_{K_{av}}(\sigma)=0,
 \qquad
 \beta_{av}=\alpha_{av}h_v,\quad
 K_{av}=I_{av}\triangle J_v.                             \tag{8}
\]

Distinct Walsh characters are linearly independent as functions on
\(\{-1,+1\}^N\). Therefore, for each character \(K\) occurring in row \(a\),

\[
 \sum_{v\in G_{a,K}}\beta_{av}=0,
 \qquad
 G_{a,K}=\{v\in V_a:K_{av}=K\}.                          \tag{9}
\]

A nonzero singleton group is impossible. This is the structural restriction
that bounded-locality coefficients impose on a row purporting to manipulate
high-degree parity characters.

#### 2. Comparison graph and row-energy domination

For each nonempty group \(G=G_{a,K}\), select one pivot \(p=p(G)\). Add a
comparison edge \((p,v)\) for every \(v\in G\setminus\{p\}\), with conductance

\[
                         c_{av}=q^2\beta_{av}^2.          \tag{10}
\]

Parallel edges are retained. There are at most \(qm\) comparison edges, and

\[
                   c_{av}\le q^2A^2H^2.                 \tag{11}
\]

For arbitrary real vertex multipliers \(w_v\), put

\[
             d_v=h_v\chi_{J_v}(\sigma)w_v.              \tag{12}
\]

The residual of group \(G\) is

\[
\begin{aligned}
 g_{a,K}
 &=\sum_{v\in G}\beta_{av}w_v\\
 &=\sum_{v\in G\setminus\{p\}}
      \beta_{av}(w_v-w_p),
\end{aligned}                                             \tag{13}
\]

where (9) was used. Two applications of Cauchy--Schwarz give, for the complete
row residual \(r_a=\sum_K\chi_K(\sigma)g_{a,K}\),

\[
\begin{aligned}
 r_a^2
 &\le q\sum_Kg_{a,K}^2\\
 &\le q^2\sum_K\sum_{v\in G_{a,K}\setminus\{p\}}
       \beta_{av}^2(w_v-w_p)^2.
\end{aligned}                                             \tag{14}
\]

Summing (14) over rows shows

\[
                \|r\|_2^2\le
                \sum_{e}c_e(w_{\mathrm{head}(e)}
                               -w_{\mathrm{tail}(e)})^2.  \tag{15}
\]

#### 3. Every comparison edge crosses few bit cuts

The two endpoints \(p,v\) of a comparison edge belong to the same group, so

\[
 I_{ap}\triangle J_p=I_{av}\triangle J_v.
\]

Consequently,

\[
                  J_p\triangle J_v
                  =I_{ap}\triangle I_{av},\qquad
                  |J_p\triangle J_v|\le2k.               \tag{16}
\]

For bit \(i\), define the vertex cut

\[
                  U_i=\{v:i\in J_v\}.
\]

It separates every trivial-character root from every full-parity output. By
(16), each comparison edge lies in at most \(2k\) of the \(N\) cuts
\(\delta(U_i)\).

#### 4. Bounded-congestion resistance

Wire all roots together at one terminal and all outputs together at another.
Let \(C_i\) be the conductance of cut \(\delta(U_i)\). For any unit
root-to-output flow \(f\), weighted Cauchy--Schwarz gives

\[
 \sum_{e\in\delta(U_i)}\frac{f_e^2}{c_e}\ge\frac1{C_i}.
\]

Each edge is counted at most \(2k\) times, so Thomson's principle yields

\[
 \mathcal R_{\mathrm{eff}}
 \ge\frac1{2k}\sum_{i=1}^N\frac1{C_i}.                   \tag{17}
\]

Moreover,

\[
 \sum_iC_i
 \le2k\sum_ec_e
 \le2k(qm)(q^2A^2H^2).
\]

Another Cauchy--Schwarz inequality gives

\[
 \mathcal R_{\mathrm{eff}}
 \ge\frac{N^2}{4k^2q^3mA^2H^2}.                         \tag{18}
\]

#### 5. Harmonic signal erasure

Let \(w\) minimize the comparison-graph energy with boundary values one on the
root terminal and zero on every output. The maximum principle gives
\(0\le w_v\le1\). Dirichlet's principle, (15), and (18) give

\[
 \|r\|_2^2
 \le\mathcal E(w)
 =\frac1{\mathcal R_{\mathrm{eff}}}
 \le\frac{4k^2q^3mA^2H^2}{N^2}.                         \tag{19}
\]

Use (12), set \(q_v=h_v\), \(t_v=h_v\), and take

\[
 u_v=\frac{h_v+d_v}{2},\qquad
 v_v=\frac{h_v-d_v}{2}.
\]

These variables are nonnegative because \(|d_v|\le h_v\). Every reference,
cap, and root row is exact. The output differences vanish because \(w_s=0\).

At the intended exact point, \(|d_v^*|=h_v\), so nonnegativity and the cap
force \(q_v\ge h_v\). The local objective reduces to \(q_v+3h_v\), minimized
at \(q_v=h_v\). The obstructing point uses exactly these same \(q,h,t\)
coordinates. It therefore has objective equal to the exact optimum despite its
small propagation residual. This proves the theorem. \(\square\)

## Corollaries

### Auxiliary product equalities do not escape the frontier

An auxiliary wire intended to hold a product of a subset of signs is precisely a
Walsh-labelled wire. A bounded-arity linear row with coefficient characters of
degree at most \(k=O(1)\) can only cancel terms in the groups (9). Thus a
linear-size network of such auxiliary wires, with bounded coefficients and
bounded intended heights, admits an \(O(N^{-1/2})\)-residual point that erases
every designated full-parity output.

This covers linear extended formulations built from signed difference wires and
homogeneous local propagation equalities. It does not cover a genuinely
nonlinear product constraint or an integer restriction.

### Full-row-rank regularity does not help

The comparison graph is a proof device, not the equality matrix itself. The
original \(q\)-ary rows may be linearly independent and need not be graph
incidences. Therefore Theorem 1 is not explained by the row-dependence issue that
affects cycle-consistent graph equalities. It applies equally when the original
standard-form equality matrix has full row rank.

### Constant-locality coefficient queries

A coefficient \(\alpha\chi_I(\sigma)\) with \(|I|\le k\) is simulated coherently
using \(O(k)\) raw sign queries. Hence fixed \(k\) is exactly the coefficient
locality regime relevant to constant-overhead parity reductions. Packaging a
long parity into one coefficient can evade (2), but it also destroys the
\(O(1)\)-query simulation.

## Why parity-polytope and LDPC constraints still have a fractional loophole

Theorem 1 concerns character-linear equality wires. A different proposal is to
use the convex hull of a Boolean XOR or a constant-arity parity predicate.
That route has its own exact obstruction.

For a check \(C\) and parity \(b_C\), write

\[
 \mathcal P(C,b_C)=
 \operatorname{conv}\left\{
    x\in\{0,1\}^C:\bigoplus_{j\in C}x_j=b_C
 \right\}.                                                \tag{20}
\]

### Lemma 2 (stopping-set pseudocodeword)

Fix some variables to a satisfying Boolean codeword \(x^*\). Let \(U\) be a set
of unfixed variables such that every parity check meets \(U\) in either zero or
at least two variables. Then the assignment

\[
 x_j=\begin{cases}
      1/2,&j\in U,\\
      x_j^*,&j\notin U
     \end{cases}                                          \tag{21}
\]

lies in every local parity polytope. In particular, if an output belongs to
\(U\), exact LP feasibility permits an unbiased fractional output.

#### Proof

For a check disjoint from \(U\), (21) is the satisfying Boolean point. If the
check contains \(r\ge2\) variables from \(U\), fix its other coordinates and
average uniformly over the \(2^{r-1}\) assignments to those \(r\) variables
having the required residual parity. Every one of the \(r\) coordinates has
marginal \(1/2\), so the average is exactly (21) restricted to the check.
Thus that restriction belongs to the convex hull (20). \(\square\)

The set \(U\) in Lemma 2 is the standard stopping-set obstruction familiar from
iterative decoding. Expander degree does not by itself remove it. To avoid the
half-integral point, the fixed inputs and checks must admit a peeling order that
eventually fixes the output, or the formulation must add nonlocal facets,
integrality, or an objective that quantitatively excludes every pseudocodeword.

### Strict-feasibility obstruction for exact gate hulls

Every satisfying truth-table point is a vertex of its exact local parity
polytope. Hence it lies on supporting facets. In a standard-form conversion of
those inequalities, some slack variables are zero at every exact Boolean gate
assignment. A circuit whose inputs force one Boolean computation therefore does
not have a strictly positive standard-form realization at that assignment.

Adding a public thickness \(\delta>0\) to every facet restores positive slacks,
but changes the exact predicate. It then becomes necessary to prove that
gate-level intervals and approximate residual cannot accumulate into an
output-erasing fractional assignment. Neither LDPC expansion nor PCP Boolean
soundness proves this for the continuous LP relaxation: Boolean soundness counts
violated predicates, whereas the LP admits small distributed real violations and
convex pseudocodewords.

### Peeling paths retain a distributed-drift mode

Even when there is no stopping set, a peeling dependency chain of length \(D\)
has a continuous sensitivity obstruction. Along a chain of XOR gates whose
off-chain input is fixed to a Boolean value, the exact gate relation on the
remaining two wires is either \(z=x\) or \(z=1-x\). In the sign-corrected gauge,
set successive wire errors to \(0,1/D,2/D,\ldots,1\). At each gate only one
of the two opposing hull facets is violated, by \(1/D\). The total Euclidean
violation is

\[
                         \frac1{\sqrt D}.                 \tag{22}
\]

The final wire is flipped while every variable remains in \([0,1]\). A balanced
formula has \(D=\Theta(\log N)\), already making this residual vanish. Copying
the final wire does not help because all copies can be made exact.

Fault-tolerant recoding would have to rule out both alternatives: stopping-set
pseudocodewords in cyclic/expanding constraint graphs and distributed drift in
peelable dependency graphs. No linear-size, bounded-coordinate LP construction
doing so was found.

## Scope and status

Theorem 1 is a sharp impossibility result for bounded-arity homogeneous linear
rows whose coefficients and intended wire values are bounded-degree Walsh
characters. It strictly extends the signed-graph cut frontier to genuine
multi-variable rows and remains compatible with full row rank.

It does **not** cover arbitrary inequality extended formulations whose exact
slack values are sums of many Walsh characters, nonhomogeneous objectives that
select among fractional pseudocodewords, semidefinite constraints, or integer
variables. Lemma 2 and the peeling drift identify concrete failures of the
standard XOR/LDPC proposals but are not a universal lower bound for every such
extension.

The electrical part uses the classical Nash--Williams inequality. The new
structural step is the Walsh decomposition (8)--(9), which turns coefficient
query locality into bounded cut congestion. Targeted open-literature searches
through 2026-09-02 found no QIPM or LP theorem with this combination. This is
evidence of apparent novelty, not proof of priority.
