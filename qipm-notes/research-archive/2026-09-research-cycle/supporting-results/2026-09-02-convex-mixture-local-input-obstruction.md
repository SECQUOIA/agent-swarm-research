# Convex-mixture obstruction for bounded-range robust parity LPs

Date: 2026-09-02

> Verification update (2026-09-20): this is a historical research record.
> The current statements are in the paper's first two Gadget-Class Frontiers
> subsections; see the [Lean verification report](../../../formal/MIXTURE.md).
> The finite residual, decoder, and centrality results are now formalized.
> For the pair decoder's bias to equal half its signed expectation, output
> an independent **fair** sign outside the selected coordinate pairs.
> A merely sign-independent assignment does not suffice for that identity.
> The separate sharpness constructions and query reductions are outside
> this Lean development.

This is the canonical statement of the sharp one-bit-local theorem, its
amplitude-pair consequence, and the three-factor amplification frontier.  The
companion `2026-09-02-single-flip-mixture-frontier-sparse-lps.md` is retained
only as a supplement for the genuinely broader case in which one coefficient
may depend on several input bits.

## Result

The \(\Theta(\sqrt N)\) range requirement of the gain--plateau parity LP is
not only a signed-path or effective-resistance phenomenon.  It follows from a
more general convex-mixture argument for any fixed-pattern real equality LP
whose coefficients are sparse and depend locally on the input bits.

Fix an input \(\sigma\in\{-1,+1\}^N\).  Average one exact witness from each of
the \(N\) instances obtained by flipping a single bit of \(\sigma\).  Every
one of those instances has the opposite parity.  The average is nonnegative;
it has exactly the common optimal objective value when the objective and
optimal value are input-independent;
and any affine parity output with a uniform margin still reports the wrong
parity.  Nevertheless its equality residual for the original instance is at
most

\[
             {2BH\sqrt{sM_{\rm dep}}\over N}.
\tag{1}
\]

Here \(B\) bounds coefficient magnitudes, \(H\) bounds witness coordinates,
\(s\) is row sparsity, and \(M_{\rm dep}\) is the total number of
input-dependent coefficient positions.  Consequently
\(s,B=\Theta(1)\), \(M_{\rm dep}=\Theta(N)\), and \(H=\Theta(1)\) always
produce an \(O(N^{-1/2})\)-feasible convex mixture of opposite-parity
witnesses. It is a wrong-parity **output** only when the decoder is stable under
that mixture, as in the affine and pair-margin hypotheses below. A fixed
global residual tube together with such a decoder requires

\[
             M_{\rm dep}B^2H^2=\Omega(N^2).
\tag{2}
\]

This rules out the most direct bounded-range, linear-size LDPC, expander, and
redundant-check repairs, even when their constraint graph is not a signed
equality graph.  It does not rule out nonlocal input coefficients, a
non-mixture-stable output contract, or a theorem restricted only to central
points.

## 1. Local-input model

Consider a fixed-support family

\[
 {\cal F}_\sigma=\{x\in\mathbb R_{\ge0}^d:A_\sigma x=b\},
\tag{3}
\]

where \(b\) is public.  Assume:

1. every row of \(A_\sigma\) has at most \(s\) nonzeros;
2. \(|(A_\sigma)_{rk}|\le B\);
3. each nonpublic coefficient position \((r,k)\) depends on one designated
   input bit \(\sigma_{\ell(r,k)}\), and all other positions are public; and
4. the total number of nonpublic positions is \(M_{\rm dep}\).

The third condition is the natural raw-query-preserving locality condition.
A sparse coefficient query can be simulated with one query to the designated
input bit.  A bit may label many positions and several positions in one row,
but one coefficient position may not hide a many-bit parity.

Let \(\sigma^{(i)}\) denote \(\sigma\) with bit \(i\) flipped.  Suppose that
for every \(i\) there is an exact nonnegative witness

\[
 x^{(i)}\in{\cal F}_{\sigma^{(i)}},
 \qquad
 \|x^{(i)}\|_\infty\le H.
\tag{4}
\]

Define their coordinatewise average

\[
                  \bar x={1\over N}\sum_{i=1}^N x^{(i)}.
\tag{5}
\]

### Theorem 1 (single-flip convex-mixture bound)

Under (3)--(5),

\[
 \boxed{\ \|A_\sigma\bar x-b\|_2
       \le {2BH\sqrt{sM_{\rm dep}}\over N}\ }.
\tag{6}
\]

#### Proof

Feasibility of \(x^{(i)}\) for its own instance gives

\[
\begin{aligned}
 N(A_\sigma\bar x-b)
 &=\sum_{i=1}^N(A_\sigma x^{(i)}-b)\\
 &=\sum_{i=1}^N(A_\sigma-A_{\sigma^{(i)}})x^{(i)}.
\end{aligned}
\tag{7}
\]

For a row \(r\), let \(D_r\) be its input-dependent coefficient positions
and put \(m_r=|D_r|\).  Only the summand \(i=\ell(r,k)\) can change the
coefficient at \((r,k)\).  Thus the \(r\)-th coordinate of the numerator in
(7) is a sum of at most \(m_r\) scalar terms, each of magnitude at most
\(2BH\).  Cauchy--Schwarz and \(m_r\le s\) imply

\[
 \left|N(A_\sigma\bar x-b)_r\right|^2
 \le 4B^2H^2m_r^2
 \le 4sB^2H^2m_r.
\tag{8}
\]

Summing (8) and using \(\sum_rm_r=M_{\rm dep}\) proves (6).
\(\square\)

If the right-hand side also depends one-bit-locally on \(\sigma\), the same
proof applies to the augmented matrix \([A_\sigma,-b_\sigma]\) and augmented
vector \((x,1)\). Replace \(B\) by a bound on all entries of the augmented
matrix, \(s\) by \(s+1\), and \(H\) by
\(\max\{H,1\}\), and include input-dependent right-hand-side positions in
\(M_{\rm dep}\).
Linear inequalities are covered after their ordinary conversion to
standard-form equalities, provided the corresponding slack coordinates obey
the same bound \(H\).

### Corollary 1.1 (local-sensitivity extension)

Let \(f:\{-1,+1\}^N\to\{-1,+1\}\) be any Boolean function and fix a base
input \(\sigma\). Define its sensitive set and local sensitivity by
\[
 S_f(\sigma)=\{i:f(\sigma^{(i)})=-f(\sigma)\},
 \qquad k=|S_f(\sigma)|>0.
\]
Let \(M_S\) be the number of nonpublic coefficient positions whose designated
input bit lies in \(S_f(\sigma)\), and average only the selected exact
witnesses for these sensitive neighbors:
\[
 \bar x_S=\frac1k\sum_{i\in S_f(\sigma)}x^{(i)}.
\]
Then
\[
 \boxed{
 \|A_\sigma\bar x_S-b\|_2
 \le\frac{2BH\sqrt{sM_S}}{k}.}
\tag{8a}
\]

The proof of Theorem 1 applies verbatim after replacing \([N]\) by
\(S_f(\sigma)\), \(N\) by \(k\), and \(M_{\rm dep}\) by \(M_S\). Every
witness in the mixture has Boolean value \(-f(\sigma)\). Therefore, under
the common-objective hypothesis and either the affine-margin condition below
or the pair-margin hypothesis of Corollary 2, in each case with \(f\) in
place of parity,
\(\bar x_S\) is an objective-exact wrong-output point.

Consequently, a relative-residual soundness claim of radius \(\eta\) under
those output assumptions requires
\[
 M_SB^2H^2>
 \frac{\eta^2\|b\|_2^2k^2}{4s}.
\tag{8b}
\]
Parity has \(k=N\) at every input and recovers Theorem 1's frontier. For a
general Boolean function the governing parameter is local sensitivity at the
chosen base input, not the ambient number of bits.

This is a useful scope extension but a routine corollary of the mixture proof,
not an independent lower-bound method. In particular, (8b) is a structural
obstruction to a robust LP output contract. It is not by itself a classical
or quantum query lower bound, and local sensitivity \(k\) must not be
identified with quantum query complexity.

### Corollary 1.2 (weighted sensitive-neighbor mixture)

The uniform average can be sharpened when the input bits occur with unequal
frequency. For \(i\in S_f(\sigma)\), let
\[
 M_i=
 |\{(r,j):\ell(r,j)=i\}|
\]
be the number of coefficient positions designated by bit \(i\). For arbitrary
weights \(w_i\ge0\), \(\sum_{i\in S_f(\sigma)}w_i=1\), define
\[
 x_w=\sum_{i\in S_f(\sigma)}w_ix^{(i)}.
\]
Then
\[
 \boxed{
 \|A_\sigma x_w-b\|_2^2
 \le4sB^2H^2\sum_{i\in S_f(\sigma)}M_iw_i^2.}
\tag{8c}
\]

Indeed, in row \(r\), expand the residual numerator directly over its
input-dependent positions. The term at position \((r,j)\) has magnitude at
most \(2BHw_{\ell(r,j)}\). Cauchy--Schwarz over at most \(s\) row positions
and then summation over rows proves (8c).

If every \(M_i>0\), the residual upper bound is minimized by
\[
 w_i=
 \frac{M_i^{-1}}{\sum_{h\in S_f(\sigma)}M_h^{-1}},
\]
which gives
\[
 \|A_\sigma x_w-b\|_2
 \le
 2BH\sqrt{
 \frac{s}{\sum_{i\in S_f(\sigma)}M_i^{-1}}}.
\tag{8d}
\]
This is never weaker than the uniform estimate (8a), because
\[
 \frac1{\sum_iM_i^{-1}}
 \le\frac{\sum_iM_i}{k^2}
 =\frac{M_S}{k^2}.
\]
If some sensitive bit has \(M_i=0\), its neighboring instance has the same
constraint matrix as the base instance; choosing that one witness gives zero
residual, so the robust-output contract already fails under the stated
objective and output assumptions.

All sensitive neighbors have the same wrong Boolean value. Therefore every
convex weighting preserves the common objective and any uniform affine or
pair margin. A relative-residual soundness claim consequently requires
\[
 B^2H^2>
 \frac{\eta^2\|b\|_2^2}{4s}
 \sum_{i\in S_f(\sigma)}M_i^{-1}.
\tag{8e}
\]
The right resource is thus a harmonic, rather than arithmetic, incidence
profile when coefficient copies are highly imbalanced. As before, this is a
structural output-contract obstruction, not a query lower bound.

## 2. Robust parity consequences

Suppose a public objective \(c\) has the same optimum value \(v_*\) on every
instance and the witnesses in (4) are optimal.  Linearity gives

\[
                       c^T\bar x=v_*.
\tag{9}
\]

Thus the fractional adversary loses neither nonnegativity nor objective
accuracy, although it is only approximately feasible for \(\sigma\).  Strict
primal feasibility elsewhere in the instance does not remove it.

The cleanest output hypothesis is an affine parity score.  Let
\(\phi(x)=a^Tx-a_0\) be public and suppose that every selected witness for
an input \(\rho\) obeys

\[
             \left(\prod_j\rho_j\right)\phi(x_\rho)\ge\gamma
\tag{10}
\]

for some \(\gamma>0\).  All single flips have parity
\(-\prod_j\sigma_j\), so (5) and affine linearity give

\[
             \left(\prod_j\sigma_j\right)\phi(\bar x)\le-\gamma.
\tag{11}
\]

The average is therefore an objective-exact, wrong-parity point for
\(\sigma\).  If a robust theorem excludes every such point whenever

\[
              \|A_\sigma x-b\|_2\le\eta\|b\|_2,
\tag{12}
\]

then (6) forces

\[
 H>{\eta\|b\|_2N\over2B\sqrt{sM_{\rm dep}}},
 \qquad\text{or equivalently}\qquad
 M_{\rm dep}B^2H^2>
 {\eta^2\|b\|_2^2\over4s}N^2.
\tag{13}
\]

For constant \(s,B,\eta,\|b\|_2\), (13) is (2).  It gives the same phase
boundary as the path-bundle resistance theorem but assumes no graph,
propagation path, or one-dimensional local state.

### Corollary 2 (pair-margin amplitude-state decoder)

An amplitude-state measurement is quadratic rather than affine, so (11)
does not hold for an arbitrary collection of witnesses.  Identical output
templates are not necessary, however.  It is enough that every selected
witness has the same signed linear margin on fixed output pairs.

Let \({\cal S}\) be a public set of \(L\ge1\) disjoint coordinate pairs
\((u_\ell,v_\ell)\).  Suppose that the selected witness for every input
\(\rho\) satisfies, for every \(\ell\in{\cal S}\),

\[
 p(\rho)(u_\ell^\rho-v_\ell^\rho)\ge a,
 \qquad p(\rho)=\prod_{j=1}^N\rho_j,
 \qquad a>0.
\tag{14}
\]

Every single-bit neighbor of \(\sigma\) has parity \(-p(\sigma)\), so
linearity of (5) gives

\[
             -p(\sigma)(\bar u_\ell-\bar v_\ell)\ge a.
\tag{15}
\]

Nonnegativity implies
\(\bar u_\ell+\bar v_\ell\ge
 |\bar u_\ell-\bar v_\ell|\ge a\).  Therefore

\[
 -p(\sigma)(\bar u_\ell^2-\bar v_\ell^2)
 =[-p(\sigma)(\bar u_\ell-\bar v_\ell)]
   (\bar u_\ell+\bar v_\ell)
 \ge a^2.
\tag{16}
\]

For the fixed diagonal observable

\[
 Q_{\cal S}=\sum_{\ell\in{\cal S}}
 (|u_\ell\rangle\langle u_\ell|
  -|v_\ell\rangle\langle v_\ell|),
\tag{17}
\]

and \(n\) LP variables, \(\|\bar x\|_2^2\le nH^2\) and hence

\[
 \boxed{
 -p(\sigma)
 \left\langle{\bar x\over\|\bar x\|_2}\middle|Q_{\cal S}\middle|
                    {\bar x\over\|\bar x\|_2}\right\rangle
 \ge {La^2\over nH^2}.}
\tag{18}
\]

Thus \(La^2=\Omega(nH^2)\) gives a constant wrong-parity observable
expectation without any identical-coordinate assumption.  If the outcome
\(+1\) is decoded as one sign and \(-1\) as the other (with any probability
outside the selected pairs assigned independently of the sign), the
wrong-parity success-probability bias is one half of the expectation in
(18).  This is a contract obstruction, not a procedure for preparing
\(\bar x\): it disproves the assertion that every approximate-feasible,
exact-objective point must encode the base parity.

Without an affine score, the pair-margin hypothesis, a common template, or
another mixture-stability property, averaging vectors need not preserve a
quadratic normalized-state decoder.  Theorem 1 alone is therefore not an
unconditional lower bound for every amplitude-state encoding.

### The three amplification currencies

For a constant relative tube with fixed \(s,\eta,\|b\|_2\), (13) charges
three interchangeable resources:

| endpoint | \(M_{\rm dep}\) | \(B\) | \(H\) |
|---|---:|---:|---:|
| bounded-height parallel replication | \(\Theta(N^2)\) | \(\Theta(1)\) | \(\Theta(1)\) |
| direct row scaling | \(\Theta(N)\) | \(\Theta(\sqrt N)\) | \(\Theta(1)\) |
| gain--plateau scaling | \(\Theta(N)\) | \(\Theta(1)\) | \(\Theta(\sqrt N)\) |

In all three cases
\(M_{\rm dep}B^2H^2=\Theta(N^2)\), so the dependence in (13) is sharp up
to constants along every pure axis.  Parallel replication uses \(N\)
bounded-height copies of an \(N\)-bit propagation gadget.  Direct row scaling
multiplies the \(\Theta(N)\) propagation/check rows by \(\sqrt N\) while
leaving the public anchor normalization at constant scale; the exact feasible
set and coordinate range are unchanged, but a distributed \(1/N\) violation
becomes \(1/\sqrt N\) per scaled row and therefore has constant global
\(\ell_2\) residual.  Gain--plateau scaling instead keeps coefficients
bounded and amplifies the relevant coordinates to height \(\Theta(\sqrt N)\).
These are scale-sharp examples for the frontier, not a claim that the three
LP formulations have identical conditioning or QIPM cost.

### Constant self-check

The factor \(2\) in (6) is exactly the worst-case change between two
coefficients in \([-B,B]\).  Squaring (6) and comparing it with
\(\eta^2\|b\|_2^2\) gives the denominator \(4s\) in (13); there is no extra
row input-degree factor in the one-bit-per-position model.  In (16), the first
factor is at least \(a\) and nonnegativity makes the second factor at least
\(a\), so the contribution is \(a^2\) per pair, with no factor \(1/2\).
The only factor \(1/2\) occurs when converting the observable expectation to
bias over binary success probability \(1/2\).  Finally, substituting each row
of the endpoint table gives
\(N^2\cdot1^2\cdot1^2\),
\(N\cdot(\sqrt N)^2\cdot1^2\), and
\(N\cdot1^2\cdot(\sqrt N)^2\), respectively, for
\(M_{\rm dep}B^2H^2\).

## 3. Why sparse LDPC and expander repairs fail

Theorem 1 exposes three common dead ends.

### Public redundant checks

Add any number of public linear rows, including a constant-degree expander or
LDPC system, provided every exact witness \(x^{(i)}\) satisfies them.  Their
residual at \(\bar x\) is exactly zero by linearity.  Such rows do not appear
in \(A_\sigma-A_{\sigma^{(i)}}\), so they contribute nothing to (7) and
cannot improve (6).  Public spectral expansion does not detect a convex
average of exact codewords from neighboring instances.

### One-bit-local input-dependent checks

Input-dependent expander checks remain subject to (6).  With bounded row
degree and coefficient scale, only \(O(N)\) dependent coefficient positions,
and bounded \(H\), (6) still gives an \(O(N^{-1/2})\) adversary.  At bounded
coefficient scale, constant range requires
\(M_{\rm dep}=\Omega(N^2)\): on average every input bit must occur in
\(\Omega(N)\) coefficient positions.  This recovers the quadratic-volume
cost of brute-force repetition without assuming a path gadget.

### Balanced XOR extended formulations

A balanced tree of ideal XOR polytopes has linear size and bounded variables,
but fixing its input leaves to Boolean vertices forces gate/output variables
and inequality slacks onto proper faces.  Its standard-form slack
representation is not strictly primal feasible.  Softening the leaves or
gates restores strict feasibility but admits fractional convex mixtures; if
the coefficients remain one-bit-local and sparse, (6) applies.  Enforcing
nonlocal XOR checks through a coefficient equal to a many-bit interval parity
leaves this model: one coefficient query then reveals many raw input bits (or
costs that many raw queries to simulate).

These observations do not prove that every conceivable LP encoding of parity
needs growing range or quadratic size.  They prove the obstruction for the
natural combination needed by the existing robust lower bounds:
one-bit-local raw access, sparse real equalities, a common linear objective,
and an affine or parity-uniform padded output that survives convex averaging.
Classical work on parity polytopes and LP relaxations, for example Ermon,
Gomes, Sabharwal, and Selman,
[*Optimization With Parity Constraints: From Binary Codes to Discrete
Integration*](https://ai.stanford.edu/~ermon/papers/LPCount.pdf), documents
compact versus exponential XOR formulations and their fractional relaxations.

This result is **not** an LP extension-complexity lower bound. Carr--Konjevod
give an \(O(N)\)-size dynamic-programming extended formulation of the parity
polytope in Section 2.6.3 of
[*Polyhedral Combinatorics*](https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15854-f05/www/handouts/carr-konjevod.pdf),
and Ermel--Walter review and extend flow formulations for parity polytopes
([arXiv:1803.10561](https://arxiv.org/abs/1803.10561)). Those exact formulations
do not promise that every point in a fixed global equality-residual tube has a
robust parity output, and so do not contradict (13). Conversely, (13) cannot be
used to claim large extension complexity: it is representation-sensitive and
charges coefficient--input incidences, coefficient scale, witness range, and a
mixture-stable output contract.

Fractional failures of sparse local parity relaxations are classical in LP
decoding. Feldman--Wainwright--Karger introduce the fundamental LP relaxation
and its pseudocodewords
([DOI:10.1109/TIT.2004.842696](https://doi.org/10.1109/TIT.2004.842696));
Koetter--Li--Vontobel--Walker and Vontobel--Koetter characterize
pseudocodewords through Tanner-graph covers
([arXiv:cs/0508049](https://arxiv.org/abs/cs/0508049),
[arXiv:cs/0512078](https://arxiv.org/abs/cs/0512078)). This is a conceptual
collision with the warning that sparse public checks admit fractional points,
not with the quantitative theorem: those papers neither average optima of
single-flip coefficient instances nor derive (6) or (13). Moreover, expander
LP decoding can correct a constant fraction of channel errors (Feldman et al.,
[*LP Decoding Corrects a Constant Fraction of
Errors*](https://www.cs.columbia.edu/~rocco/papers/isit04.html)). There is no
contradiction because the decoding objective changes with the received word;
the common objective and common optimum in (9) are essential here. The phrase
``LDPC and expander repairs fail'' must remain restricted to adding checks to
the present common-objective neighboring-instance construction.

The use of single-bit neighbors and averaging also resembles quantum hybrid and
adversary arguments, beginning with Ambainis's relation between inputs that
differ locally ([arXiv:quant-ph/0002066](https://arxiv.org/abs/quant-ph/0002066)).
Those arguments average changes in algorithm states or progress measures to
lower-bound oracle queries. Theorem 1 instead averages classical feasible
witnesses and controls an LP residual by the number and scale of changing
coefficient positions; it is not a new quantum adversary method and does not by
itself prove a query lower bound.

Robust optimization and adversarial-example convex relaxations are also only
structural neighbors. Robust LP asks for one decision feasible across an
uncertainty set, rather than averaging scenario-dependent optima; see
Bertsimas--Sim
([DOI:10.1287/opre.1030.0065](https://doi.org/10.1287/opre.1030.0065)).
Wong--Kolter construct convex outer adversarial polytopes to certify neural
networks ([arXiv:1711.00851](https://arxiv.org/abs/1711.00851)); they do not
study one-bit-local coefficient oracles or an \(MB^2H^2\) parity frontier.

A targeted primary-literature search through 2026-09-02 found no source stating
the single-flip residual bound (6) or the local-input phase boundary (13). This
supports apparent novelty for the exact sparse-LP quantitative conjunction,
not for convex averaging, neighboring-input hybrid reasoning, compact parity
formulations, or the existence of fractional pseudocodewords.

## 4. Implications for further construction searches

A bounded-range, linear-size construction must violate at least one premise
used above.  Plausible escape routes are:

1. use a nonlinear or genuinely non-mixture-stable output promise and prove
   robustness directly;
2. ask only for a central/Newton state, not every approximate feasible or
   optimal nonnegative point;
3. allow nonlocal input-dependent coefficients and charge their raw-query
   implementation honestly;
4. abandon a common objective/optimal value, so the average is not
   near-optimal; or
5. introduce a nonconvex/integrality promise, which is outside linear
   programming.

For the current goal of a robust theorem quantifying over every nonnegative
point in a fixed equality-residual tube, the first two escapes change the
output theorem and the last three change the optimization or oracle model.
Thus (13), rather than a new bounded-range expander gadget, is the useful
result of this search.

Status: **canonical, proof complete, and independently audited:** a
graph-independent convex-mixture phase boundary under one-bit-local
coefficient access, including the pair-margin amplitude-state corollary and
the three sharp amplification currencies. Corollaries 1.1--1.2 give the
routine local-sensitivity extension and the sharper harmonic-incidence
weighted mixture; neither is claimed as a query lower bound. The companion
`2026-09-02-single-flip-mixture-frontier-sparse-lps.md` is only the
multi-bit-per-coefficient supplement.
