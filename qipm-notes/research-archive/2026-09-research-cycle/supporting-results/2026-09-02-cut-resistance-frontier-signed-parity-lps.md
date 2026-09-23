# A cut--resistance frontier for local signed-parity LP gadgets

Date: 2026-09-02

## Result

The path-bundle size--dynamic-range tradeoff extends to every
cycle-consistent signed-equality graph whose coefficient oracle associates each
edge with at most one hidden input sign. The graph need not be a path, tree,
series-parallel graph, or bundle of disjoint paths.

If the graph has \(M\) propagation edges, all exact reference heights are at most
\(H\), and all propagation rows are scaled by at most \(B\), then constant
\(\ell_2\)-residual soundness that forces the designated outputs to retain a
nonzero \(N\)-bit parity signal requires

\[
             M B^2H^2=\Omega(N^2).                       \tag{1}
\]

In particular, a linear-size gadget with bounded row scale cannot have bounded
solution dynamic range. It needs \(H=\Omega(\sqrt N)\). The gain--plateau LP in
`2026-09-02-linear-size-robust-gain-parity-lp.md` attains this boundary, while the
bounded-height parallel-path LP attains the opposite endpoint \(M=\Theta(N^2)\).

The obstruction constructs nonnegative points whose root, reference, and cap
equations are exact and whose objective is exactly the optimum. One point erases
the parity signal at every designated output; a second flips every output sign.
Both have propagation residual obeying the upper bound dual to (1).

## Model

Let \(G=(V,E)\) be a connected undirected multigraph with a chosen orientation of
each edge. Fix a root \(r\) and a nonempty output set \(S\). For
\(\sigma=(\sigma_1,\ldots,\sigma_N)\in\{-1,+1\}^N\), an oriented edge
\(e=(u,v)\) has sign label

\[
 a_e(\sigma)\in
 \{\epsilon_e,\epsilon_e\sigma_1,\ldots,
   \epsilon_e\sigma_N\},qquad \epsilon_e\in\{-1,+1\}.   \tag{2}
\]

Thus one coefficient value depends on at most one raw input bit. Give every vertex
a public height \(h_v>0\), normalized by \(h_r=1\), and put

\[
 g_e=\frac{h_v}{h_u}>0.
\]

The propagation equality, with an optional public nonzero row scale \(\lambda_e\),
is

\[
 \lambda_e\bigl(d_v-g_ea_e(\sigma)d_u\bigr)=0.           \tag{3}
\]

Assume these equations are cycle-consistent for every input: there are signs
\(\tau_v(\sigma)\) with \(\tau_r=1\) such that

\[
 \tau_v=a_e(\sigma)\tau_u
 \quad(e=(u,v)).                                          \tag{4}
\]

Every output is required to carry full parity, up to a public fixed sign:

\[
 \tau_s(\sigma)=\epsilon_s\prod_{i=1}^N\sigma_i
 \quad(s\in S),qquad \epsilon_s\in\{-1,+1\}.            \tag{5}
\]

Fixed signs can be removed by a public vertex gauge and play no role below.

For the standard-form LP embedding, introduce \(u_v,v_v,h_v^{\rm var},t_v\ge0\),
with \(d_v=u_v-v_v\), \(q_v=u_v+v_v\). Pin and propagate the reference variables
so that \(h_v^{\rm var}=h_v\), and impose

\[
 q_v+t_v-2h_v^{\rm var}=0.                               \tag{6}
\]

Use the local objective \(2u_v+2v_v+h_v^{\rm var}+t_v\), as in the robust parity
LPs. Define the effective propagation scale

\[
 L=\max_{e=(u,v)}|\lambda_e|h_v.
\]

If \(|\lambda_e|\le B\) and \(h_v\le H\), then \(L\le BH\).

## Theorem 1 (general graph frontier)

Under (2)--(6), there is a nonnegative point \(x\) such that:

1. the root, reference, and cap rows are exact;
2. its objective equals the exact optimum;
3. every output difference is zero, \(d_s=0\), so the designated output region
   contains no parity signal;
4. its residual satisfies
   \[
      \|Ax-b\|_2^2\le\frac{ML^2}{N^2}
      \le\frac{MB^2H^2}{N^2}.                            \tag{7}
   \]

There is also a sign-flipped point with \(d_s=-\tau_sh_s\) and four times the
squared-residual bound in (7). If the only nonzero entries of \(b\) are the unit
difference and reference anchors, then \(\|b\|_2=\sqrt2\), and the erased point
satisfies

\[
 \frac{\|Ax-b\|_2}{\|b\|_2}
 \le\frac{L\sqrt{M/2}}{N}.                               \tag{8}
\]

Consequently, if a claimed residual-soundness theorem at threshold \(\eta\)
rules out every erased-output point of this form, it must have

\[
 ML^2>2\eta^2N^2,
 \qquad\text{and hence}\qquad
 MB^2H^2>2\eta^2N^2.                                    \tag{9}
\]

If soundness only rules out a fully sign-flipped output, the corresponding
necessary condition is the weaker \(ML^2>\eta^2N^2/2\).

### Proof

#### Each input bit is an output-separating cut

For bit \(i\), let \(E_i\subseteq E\) contain the edges whose label in (2)
depends on \(\sigma_i\). Cycle consistency implies that every cycle contains an
even number of edges from \(E_i\): multiply (4) around the cycle and compare the
exponent of the independent variable \(\sigma_i\).

Over \(\mathbb F_2\), a set of graph edges has even intersection with every cycle
if and only if it lies in the cut space. Hence there is a vertex set \(U_i\) with

\[
 E_i=\delta(U_i).                                         \tag{10}
\]

Equation (5) says that every root-to-output path contains an odd number of
\(\sigma_i\)-labelled edges. Thus \(E_i\) separates \(r\) from every vertex in
\(S\). Finally, the sets \(E_1,\ldots,E_N\) are pairwise edge-disjoint because
one edge label depends on at most one input bit.

#### Effective resistance

Give propagation edge \(e=(u,v)\) electrical conductance

\[
 c_e=(\lambda_eh_v)^2\le L^2.                            \tag{11}
\]

Wire the vertices in \(S\) together. Let \(\mathcal R_{r,S}\) be the effective
resistance between \(r\) and the wired output terminal. For any unit flow from
\(r\) to \(S\), one unit of net flow crosses each cut \(E_i\). Weighted
Cauchy--Schwarz gives

\[
 \sum_{e\in E_i}\frac{f_e^2}{c_e}
 \ge\frac1{C_i},
 \qquad C_i=\sum_{e\in E_i}c_e.                          \tag{12}
\]

The cuts are edge-disjoint, so Thomson's principle and then Cauchy--Schwarz imply

\[
 \mathcal R_{r,S}
 \ge\sum_{i=1}^N\frac1{C_i}
 \ge\frac{N^2}{\sum_iC_i}
 \ge\frac{N^2}{ML^2}.                                   \tag{13}
\]

This is the weighted Nash--Williams bound, with its short proof included to make
the oracle-specific role of the disjoint cuts explicit.

#### The wrong-parity point

Let \(w:V\to[0,1]\) be the harmonic voltage minimizing

\[
 \mathcal E(w)=\sum_{e=(u,v)}c_e(w_v-w_u)^2              \tag{14}
\]

subject to \(w_r=1\) and \(w_s=0\) for every \(s\in S\). The maximum principle
gives the displayed range. Dirichlet's principle and (13) give

\[
 \mathcal E(w)=\frac1{\mathcal R_{r,S}}
 \le\frac{ML^2}{N^2}.                                   \tag{15}
\]

Set

\[
 d_v=\tau_vh_vw_v,qquad
 q_v=h_v^{\rm var}=t_v=h_v.                              \tag{16}
\]

Because \(|w_v|\le1\), the coordinates

\[
 u_v=\frac{h_v+d_v}{2},qquad
 v_v=\frac{h_v-d_v}{2}
\]

are nonnegative. The reference and cap equations are exact, as are both anchors.
For edge \(e=(u,v)\), equations (3)--(4) give residual

\[
 \lambda_e(d_v-g_ea_ed_u)
 =\lambda_e\tau_vh_v(w_v-w_u),                           \tag{17}
\]

whose squared norm summed over all edges is exactly (14). At an output,
\(w_s=0\), so \(d_s=0\) and its pair \((u_s,v_s)=(h_s/2,h_s/2)\) contains no
parity bias.

Finally, on the exact feasible affine space the local objective is
\(q_v+3h_v\), minimized at \(q_v=h_v\). The point (16) uses the same values of
\(q,h,t\), so its objective is **exactly** the optimum even though its propagation
rows are inexact. Objective accuracy, including zero two-sided objective error,
cannot remove the obstruction. This proves the theorem. \(\square\)

Replacing the boundary condition \(w_s=0\) by \(w_s=-1\) gives the asserted
sign-flipped point. The voltage difference doubles, so Dirichlet energy and the
squared residual are multiplied by four; the maximum principle still ensures
\(|w_v|\le1\) and hence nonnegativity.

### Proposition 2 (constant-locality labels)

The same conclusion is stable if one row may depend on a constant number of raw
signs. Suppose

\[
 a_e(\sigma)=\epsilon_e\prod_{i\in I_e}\sigma_i,
 \qquad |I_e|\le k.                                      \tag{18}
\]

Then there is an erased-output, exactly objective-optimal nonnegative point with

\[
 \|Ax-b\|_2^2\le\frac{k^2ML^2}{N^2}.                    \tag{19}
\]

Hence constant residual soundness requires

\[
 Mk^2B^2H^2=\Omega(N^2).                                 \tag{20}
\]

To prove this, define \(E_i=\{e:i\in I_e\}\). Each \(E_i\) is still a
root--output cut, but an edge now lies in at most \(k\) cuts. For any unit flow,

\[
 \sum_i\frac1{C_i}
 \le\sum_i\sum_{e\in E_i}\frac{f_e^2}{c_e}
 \le k\sum_e\frac{f_e^2}{c_e}.
\]

Also \(\sum_iC_i\le kML^2\), so

\[
 \mathcal R_{r,S}
 \ge\frac1k\sum_i\frac1{C_i}
 \ge\frac{N^2}{k^2ML^2}.
\]

The harmonic construction is then unchanged. For every fixed \(k=O(1)\), the
quadratic frontier survives with only a constant loss. Simulating such a
coefficient from raw signs also costs at most \(k\) queries, so this extension
matches the natural constant-locality oracle model.

## Consequences

### Bounded dynamic range

If \(M=\Theta(N)\), \(B=O(1)\), and \(H=O(1)\), Theorem 1 constructs a
signal-erased, exactly objective-optimal point with relative residual
\(O(N^{-1/2})\). Therefore constant global \(\ell_2\) approximate feasibility
cannot force a nonzero parity bias at the designated outputs of any linear-size
gadget in this model.

More generally, a linear-size constant-row-scale gadget needs

\[
 H=\Omega(\sqrt N).                                      \tag{21}
\]

This explains why the gain--plateau construction's \(\Theta(\sqrt N)\) solution
height is not an incidental proof choice: it is optimal throughout this graph
propagation class.

### A unified frontier

The three known repairs occupy the three factors in (9):

- parallel paths use \(M=\Theta(N^2)\), \(B=H=1\);
- direct row amplification can use \(M=\Theta(N)\), \(B=\Theta(\sqrt N)\),
  \(H=1\);
- the gain--plateau LP uses \(M=\Theta(N)\), \(B=1\),
  \(H=\Theta(\sqrt N)\).

All saturate \(MB^2H^2=\Theta(N^2)\). Row amplification is visible in matrix
normalization; gain amplification is visible in primal radius and optimal value;
parallel amplification is visible in dimension. None is a parameter-free way to
obtain constant residual soundness.

### Equality cycles and full-row-rank QIPMs

There is an additional regularity obstruction in the pure propagation model. Once
the public heights and input signs are gauged out, the propagation block is a
weighted graph-incidence matrix. Pinning the root gives full row rank only when
the retained propagation edges form a tree. Every cycle adds a dependent equality
row, separately in both the difference and reference blocks. Thus an expander
cannot be added to (3) while retaining both exact cycle consistency and the usual
full-row-rank standard-form assumption, unless redundant rows are removed; after
removal the propagation graph is again a tree.

This does not affect Theorem 1, which permits arbitrary graphs and hence also
covers every full-row-rank tree member. It further explains why “add
input-local expander equalities” is not a free robustification of a regular QIPM
instance.

For a tree, the capped-pair LP has all the usual regularity properties. Exact
feasibility fixes \(d_v=\tau_vh_v\), \(h_v^{\rm var}=h_v\), and leaves the product
intervals \(h_v\le q_v\le2h_v\). Taking \(q_v=3h_v/2\) is strictly primal
feasible, while zero equality multiplier and \(s=c>0\) give strict dual
feasibility. The sign-selected pair coordinate together with \(h_v^{\rm var},t_v\)
at every vertex forms a triangular positive-column basis. The optimum
\(q_v=t_v=h_v\) is therefore unique, nondegenerate, and strictly complementary,
exactly as in the gain--plateau path. Thus the resistance obstruction persists
inside the regular bounded-degree QIPM subclass; it is not caused by redundant
equalities.

### Adaptive trajectories do not evade the pointwise obstruction

The constructed point is available at every requested output stage because it is
defined from the fixed LP data and the residual contract, not from an algorithm's
history. Earlier iterates, warm starts, or cached queries cannot make approximate
feasibility and objective accuracy logically imply the correct output sign when
the point (16) satisfies both promises. This is a contract obstruction, not a
per-iteration query lower bound.

Conversely, no fixed-input trajectory can have an unconditional fresh
\(\Omega(N)\) coefficient-query cost at every iteration: after querying and
caching all \(N\) hidden signs, all later iterates can be generated without new
coefficient queries. Any per-iteration lower bound must therefore impose a
streaming input, limited memory, destructive access, or fresh external data. Those
are different models and should not be inferred from a standard fixed-LP oracle.

## Scope and novelty calibration

The proof uses standard cut-space duality, Thomson's principle, and the
conductance-weighted form of the classical Nash--Williams resistance bound; see
Nash-Williams,
[*Random walk and electric currents in
networks*](https://doi.org/10.1017/S0305004100033879) (1959). The apparent new
point is not a new signed-graph or resistance lemma. Harary's balance theorem
already identifies a cycle-consistent signing with a vertex switching, or,
equivalently, identifies its negative edges with a cut
([DOI:10.1307/mmj/1028989917](https://doi.org/10.1307/mmj/1028989917)). Applied
separately to the exponent of each independent input bit, this is exactly the
structural step \(E_i=\delta(U_i)\) in (10). The candidate contribution is the
combination of that coefficientwise cut decomposition with the coefficient-query
locality condition and the nonnegative capped-pair LP embedding. It strictly
generalizes the earlier path-bundle resistance calculation.

Proposition 2's bounded-overlap resistance estimate is also prior graph theory,
not a new Nash--Williams extension. Lyons--Peres--Sun Lemma 2.1 proves for
possibly overlapping separating cutsets \(C_i\) that

\[
 R_{\rm eff}(A,B)\ge
 \sum_i\left(\sum_{e\in C_i}j(e)c_e\right)^{-1},
 \qquad j(e)=|\{i:e\in C_i\}|,
\]

([arXiv:1812.03127](https://arxiv.org/abs/1812.03127), published as
[DOI:10.1214/20-AIHP1056](https://doi.org/10.1214/20-AIHP1056)). Taking
\(j(e)\le k\), followed by Cauchy--Schwarz and
\(\sum_i C_i\le kML^2\), gives the \(k^2\) loss in (19) directly. The possible
novelty of Proposition 2 is only its use inside this local-sign LP residual
contract.

The theorem does not cover arbitrary sparse linear constraints involving three or
more propagation variables, nor an oracle coefficient that depends jointly on
several hidden signs. It also does not prove that every conceivable bounded-range
linear-size LP embedding of parity lacks constant residual soundness. It gives a
sharp impossibility theorem for the broad and natural class of cycle-consistent
signed-equality graph gadgets, and it identifies exactly which assumption a more
general construction must leave.

The erased-output point can still depend on partial prefix products at internal
vertices. The theorem therefore does not prove that its *entire* amplitude state
is easy to prepare or contains no parity information under every possible global
measurement. It rules out the standard proof strategy in which approximate
feasibility and objective accuracy force a fixed amplified output region to carry
a uniform parity bias. A global state-generation lower bound needs an additional
argument about all coordinates, as in the gain--plateau positive construction.

Effective resistance also has an established quantum-query role through
\(s\)-\(t\)-connectivity span programs: Belovs--Reichardt introduced the graph
framework ([arXiv:1203.2603](https://arxiv.org/abs/1203.2603)), and
Jarret--Jeffery--Kimmel--Piedrafita identify positive witness size with effective
resistance and negative witness size with effective capacitance
([arXiv:1804.10591](https://arxiv.org/abs/1804.10591)). Those results analyze
connectivity algorithms and witness sizes, not a coefficient-query lower bound
for an amplitude encoding of an approximately feasible LP point. Likewise,
Apers--de Wolf's optimal graph-sparsification and cut-approximation query bounds
([arXiv:1911.07306](https://arxiv.org/abs/1911.07306)) do not imply the residual
frontier here.

The nearest optimization lower bounds use different output and access contracts.
Van Apeldoorn--Gily\'en--Gribling--de Wolf and
Chakrabarti--Childs--Li--Wu lower-bound optimization from membership,
separation, or evaluation oracles
([arXiv:1809.00643](https://arxiv.org/abs/1809.00643),
[arXiv:1809.01731](https://arxiv.org/abs/1809.01731)); Apers--Gribling Theorem
8.4 lower-bounds sparse-LP *optimal-value estimation* in a row-query model
([arXiv:2311.03215v3](https://arxiv.org/abs/2311.03215v3)). None states a
necessary \(MB^2H^2\) tradeoff for a nonnegative, exactly objective-optimal,
globally residual-small point that erases a designated parity output.

Targeted searches through 2026-09-02 found no theorem combining the
coefficientwise signed cuts, the resistance bound, and this approximate-feasible
capped-LP contract. This supports apparent novelty only for that conjunction and
its sharp LP tradeoff, not for the per-input cut lemma, the disjoint-cut
Nash--Williams inequality, the bounded-overlap extension, or the use of
effective resistance in quantum query algorithms.
