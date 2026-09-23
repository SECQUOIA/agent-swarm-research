# Thresholding sparse inverse observables into one optimizer coordinate

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem and oracle accounting; moderate on novelty

## Main theorem

Let \(g\) be the standard promised 2-Forrelation predicate: \(g=0\) when
\(|\Phi|\le\alpha=1/100\), and \(g=1\) when
\(\Phi\ge\beta=3/5\). For every \(T\), there is one sparse LP containing
\(T\) independent cyclic inverse-history instances and a designated bounded
scalar coordinate \(P^*\) of its unique optimizer such that

\[
 \boxed{P^*=g_1\mathbin\oplus\cdots\mathbin\oplus g_T.}      \tag{1}
\]

Consequently, returning only \(P^*\in\{0,1\}\) to additive error less than
\(1/3\) computes \(\mathsf{XOR}_T\circ g^T\). This is one bounded bit, not
\(T\) checkpoint outputs or an explicit optimizer.

Use the notation of the audited parameterized one-cone scalar-frontier
construction. One inner block has dimension \(N_0\), row and column
sparsity \(s=\Theta(q)\), condition number \(K\), and

\[
 a_j^TM_j^{-1}e=h\Phi_j,\qquad h=\Theta(\delta),            \tag{2}
\]

where \(a_j,e,h\) are public and full-SQ access to \(M_j\) is simulated with
constant raw Forrelation-query overhead. Its classical query lower bound is

\[
 R(g)=\Omega\!\left(\frac{q^{\ell/2}}{r\ell}\right),        \tag{3}
\]

with

\[
 \ell=\frac{\log(1/\delta)}
 {3\log((K+1)/(K-1))}+O(1).                                \tag{4}
\]

The compiled LP has dimension \(\mathcal N=\Theta(TN_0)\), sparsity
\(s+O(1)\), and only \(O(T)\) bounded scalar inequalities. Under the same
raw oracle and full-SQ simulation,

\[
 \boxed{
 Q_{\rm quantum}(P^*)=\Theta\!\bigl(TQ(g)\bigr)=\Theta(T),
 \qquad
 R_{\rm classical}(P^*)
 =\Omega\!\left(T\frac{q^{\ell/2}}{r\ell}\right).}          \tag{5}
\]

The upper bound is the standard adversary-based composition algorithm for
the Boolean function \(\mathsf{XOR}_T\circ g^T\); it does not estimate all
\(g_j\)'s separately to error \(O(1/T)\). Thus the construction gives an
exponential classical-versus-quantum query separation in the inner
sparse-inverse parameters while retaining the full linear \(T\) factor in
one bounded optimizer coordinate.

The product logarithmic barrier for the displayed bounded variables has
parameter at most \(12T\), independent of \(N_0\). Equalities carry the
high-dimensional sparse inverse histories.

For the literal scalar product barrier below, use the certified parameter
\(\nu_{\log}=12T-4\). Hence (5) may equivalently be read as

\[
 Q_{\rm quantum}(P^*)=\Theta(\nu_{\log}),\qquad
 R_{\rm classical}(P^*)
 =\Omega\!\left(
   \nu_{\log}\frac{q^{\ell/2}}{r\ell}\right),              \tag{5a}
\]

up to absolute constants. This is an endpoint-output law indexed by the
displayed barrier parameter, not a claim that each of
\(\Theta(\sqrt{\nu_{\log}})\) short-step iterations independently pays the
inner cost.

## 1. A robust LP threshold compiler

The following constant-size gadget may be useful beyond Forrelation. Suppose
\(\varphi\in[-1,1]\) has the promise

\[
 |\varphi|\le\alpha\quad(g=0),
 \qquad\text{or}\qquad
 \varphi\ge\beta\quad(g=1),                                \tag{6}
\]

where \(0\le\alpha<\beta\le1\). Put

\[
 c=\frac{\alpha+\beta}{2},\qquad
 \Delta=\frac{\beta-\alpha}{2},\qquad
 G=\Delta^{-1},\qquad M_0=2G,\qquad C=4G.                  \tag{7}
\]

For variables \(z,r,t\), impose

\[
 0\le z\le1,\qquad 0\le r\le2,\qquad
 0\le t\le z,\qquad t\le Gr,\qquad
 r\ge z(\varphi-c),                                       \tag{8}
\]

and maximize

\[
 Cz-M_0r+t.                                                \tag{9}
\]

Although (8) is written after eliminating the inverse-history equalities,
the actual formulation below replaces \(z\varphi\) by a linear readout
variable. Thus the gadget is an LP, not a bilinear program.

### Lemma 1

Under promise (6), (8)--(9) has a unique optimizer and

\[
 (z^*,t^*)=(1,g).                                         \tag{10}
\]

#### Proof

In the low case \(\varphi-c\le-\Delta\), so the last inequality does not
improve the lower bound \(r\ge0\). For fixed \(z\), if
\(0\le r\le z/G\), the best \(t\) is \(Gr\), and the variable part is
\((G-M_0)r\), uniquely maximized at \(r=t=0\). For \(r\ge z/G\), the best
\(t=z\), and \(-M_0r+z\le z(1-M_0/G)<0\). Hence
\(r^*=t^*=0\), and the remaining objective \(Cz\) uniquely sets \(z^*=1\).

In the high case \(d:=\varphi-c\ge\Delta=1/G\). For fixed \(z\), feasibility
requires \(r\ge dz\), which already implies \(Gr\ge z\). Hence \(t=z\), and
the negative coefficient of \(r\) uniquely sets \(r=dz\). The objective is

\[
 z(C+1-M_0d)>0                                             \tag{11}
\]

because \(d\le1-c<1\) and \(C=2M_0\). It uniquely sets \(z=1\), and then
\(t=1\). \(\square\)

The feasible set has a strict relative interior uniformly over
\(\varphi\in[-1,1]\): for example, take \(z=1/2\), \(r=3/2\), and a
sufficiently small positive \(t<\min\{z,Gr\}\). It is compact after the
equalities are eliminated.

## 2. Sparse compilation of one Forrelation block

For block \(j\), introduce an activation \(z_j\) and inverse-history
variables \(y_j\), with the sparse equalities

\[
 M_jy_j=z_je.                                              \tag{12}
\]

Because \(M_j\) is invertible,

\[
 y_j=z_jM_j^{-1}e.                                        \tag{13}
\]

Use the public three-sparse accumulator from the scalar-frontier construction
to define a literal readout coordinate

\[
 q_j=\frac{a_j^Ty_j}{h}=z_j\Phi_j.                         \tag{14}
\]

The \(O(1/h)\) normalization is public. Equations (12)--(14) are all linear.
Now impose

\[
 0\le z_j\le1,\quad 0\le r_j\le2,\quad
 0\le t_j\le z_j,\quad t_j\le Gr_j,\quad
 r_j\ge q_j-cz_j,                                         \tag{15}
\]

and give the block objective

\[
 \theta_j(Cz_j-M_0r_j+t_j),\qquad \theta_j>0.              \tag{16}
\]

Lemma 1 applies with \(\varphi=\Phi_j\). Every promised block has the unique
optimizer

\[
 z_j^*=1,\qquad t_j^*=g_j,\qquad
 y_j^*=M_j^{-1}e.                                         \tag{17}
\]

The constraints in (15) have constant row and column incidence. In (12),
the one row selected by the basis vector \(e\) gains one \(z_j\) entry.
The readout chain in (14) is public and three-sparse. Therefore the compiled
block has row and column sparsity \(s+O(1)\).

## 3. One bounded XOR scalar

Take the Cartesian product of the \(T\) compiled blocks and append a public
three-sparse summation chain ending in

\[
 W=\sum_{j=1}^Tt_j.                                       \tag{18}
\]

This optional coordinate has \(W^*=\sum_jg_j\). To obtain a bounded readout
with no quantum error-amplification logarithm, set \(p_1=t_1\) by a public
equality. For \(2\le j\le T\), impose the four XOR-polytope facets

\[
 \begin{aligned}
 p_j&\le p_{j-1}+t_j,&
 p_j&\ge p_{j-1}-t_j,\\
 p_j&\ge t_j-p_{j-1},&
 p_j&\le2-p_{j-1}-t_j .
 \end{aligned}                                             \tag{18a}
\]

For Boolean inputs, these inequalities uniquely force
\(p_j=p_{j-1}\mathbin\oplus t_j\). For fractional inputs in \([0,1]^2\),
they are the convex hull of the four Boolean XOR triples and project onto
the whole input square. Thus (18a) does not change the feasible projection
onto the \(t_j\)'s or their unique optimizer values. It gives

\[
 P^*:=p_T^*=g_1\mathbin\oplus\cdots\mathbin\oplus g_T,      \tag{18b}
\]

which proves (1). Once the \(t_j^*\)'s are fixed, all \(p_j^*\)'s are
unique, so the entire optimizer is unique.

The whole augmented LP has a strict relative interior. In every threshold
block take \(z_j=3/4\), \(r_j=3/2\), and \(t_j=1/2\), with \(q_j=z_j\Phi_j\)
and \(y_j\) fixed by the equalities. Set \(p_1=t_1=1/2\) and
\(p_j=1/2\) thereafter. The threshold inequalities and all four facets of
every later XOR gate are then strict.

Choosing

\[
 \theta_j=\Gamma^{-j}                                     \tag{19}
\]

places the base count formulation on one scale-separated logarithmic central
path. Before adding the XOR inequalities, after
eliminating equalities, block \(j\)'s barrier problem at global multiplier
\(\eta\) is exactly its one-block problem at multiplier
\(\eta\theta_j\). Thus the instance has \(T\) separated objective scales,
not \(T\) independently sampled LPs. Unlike the raw signed-chain
construction, no elementary closed form for \(t_j(\eta)\) is claimed: its
analytic center depends on \(\Phi_j\). The XOR facets couple the barrier
path of the bounded-output formulation, so exact one-block rescaling is
claimed only for the count formulation. Both formulations use the same
unique block optimizer and need no checkpoint-output contract.

There are eight scalar inequalities per block in the displayed formulation.
The XOR readout adds \(4(T-1)\), so the ordinary scalar product barrier for
the bounded-output formulation has parameter at most \(12T-4\). This
constant is not optimized.

## 4. Query lower bounds

An additive-\(1/3\) estimate of \(P^*\) directly recovers
\(\mathsf{XOR}_T\circ g^T\). Alternatively, the count \(W^*\) to this
accuracy recovers the exact integer \(\sum_jg_j\), and hence its parity.

The negative-weight adversary bound characterizes bounded-error quantum
query complexity for partial Boolean functions and composes perfectly:

\[
 \operatorname{ADV}^{\pm}(\mathsf{XOR}_T\circ g^T)
 =\operatorname{ADV}^{\pm}(\mathsf{XOR}_T)
  \operatorname{ADV}^{\pm}(g)
 =\Theta(TQ(g)).                                           \tag{21}
\]

The adversary bound also characterizes bounded-error quantum query
complexity from above. Thus (21) proves both sides of the quantum statement
in (5), with no \(\log T\) loss, while allowing arbitrary coherent
interleaving of queries among blocks and arbitrary persistent workspace.

For randomized algorithms, the strong XOR lemma of Brody, Kim,
Lerdputtipongporn, and Srinivasulu applies to every partial Boolean function:

\[
 \overline R_\epsilon(\mathsf{XOR}_T\circ g^T)
 =\Theta\!\left(T\overline R_{\epsilon/T}(g)\right).       \tag{22}
\]

At constant outer error, monotonicity in the inner error gives
\(\Omega(TR_{1/3}(g))\), up to the standard constant conversion between
expected and worst-case query bounds. Combining this with (3) proves the
classical statement in (5).

These are composition theorems on the \(T\) independent blocks of one oracle
\(O(j,\cdot)\), not a multiplication of \(T\) separately sampled
one-instance bounds.

### Objective-gap transfer

There is an exact quantitative version of the objective-gap caveat. Let

\[
 f_j=Cz_j-M_0r_j+t_j,\qquad
 \mathcal F=\sum_{j=1}^T\theta_jf_j.                       \tag{22a}
\]

The proof of Lemma 1 gives more than uniqueness. In the low case,

\[
 f_j^*-f_j=C(1-z_j)+M_0r_j-t_j\ge t_j,
\]

because \(M_0=2G\) and \(t_j\le Gr_j\). In the high case, writing
\(d=\Phi_j-c\), feasibility gives
\[
 f_j\le(C-M_0d)z_j+t_j,
\]
and \(C-M_0d>0\), so
\[
 f_j^*-f_j\ge1-t_j.
\]
Thus in both cases

\[
 f_j^*-f_j\ge|t_j-g_j|.                                   \tag{22b}
\]

The XOR facets also obey the deterministic stability recursion

\[
 |p_j-(g_1\mathbin\oplus\cdots\mathbin\oplus g_j)|
 \le\sum_{i=1}^j|t_i-g_i|.                                \tag{22c}
\]

For \(g_j=0\), this follows from
\(|p_j-p_{j-1}|\le t_j\); for \(g_j=1\), it follows from
\(|p_j-(1-p_{j-1})|\le1-t_j\). Therefore every feasible point with global
objective gap \(\tau\) satisfies

\[
 |p_T-P^*|
 \le\sum_j|t_j-g_j|
 \le\frac{\tau}{\theta_T}.                                \tag{22d}
\]

For the scale-separated choice \(\theta_T=\Gamma^{-T}\), gap
\(\tau<\Gamma^{-T}/3\) transfers the same parity lower bound to the returned
coordinate of a feasible approximate optimizer. If instead all
\(\theta_j=1\), the transfer holds already at constant objective gap
\(\tau<1/3\), but that unweighted variant has no separated path scales.

## 5. Matched full-SQ access

All new coefficients \(c,G,M_0,C,\theta_j\), all count/XOR coefficients,
all right-hand sides, and every support location are public. Hidden data
occur only inside the original \(M_j\)'s. Every XOR row has at most three
public nonzeros. A full-SQ query to the block
diagonal collection \(\operatorname{diag}(M_1,\ldots,M_T)\) first resolves
the public block label \(j\), then invokes exactly the audited one-block
simulator. The added \(z_j\) column and threshold/readout rows are public.

More explicitly, the one row of (12) selected by \(e\) is a public
two-component mixture of the old \(M_j\) row state and the basis state of
\(z_j\), with normalization
\(\sqrt{\|M_j(\mathrm{row})\|^2+1}\). A \(y_j\) column touched by the
readout chain is likewise a public mixture of its old column state and one
new accumulator-row basis state. All other new rows have constant public
support. Thus augmented row and column norms and state preparations follow
from the audited old full-SQ interface with constant overhead; they are not
silently supplied as a stronger oracle.

Thus each formulation query costs at most a constant number of queries to
the same multiplexed Forrelation oracle, including row/column norm and
state-preparation access. Conversely, every raw hidden sign occurs at a
known matrix position, so the structured source algorithm can query it
through the formulation oracle with constant overhead. This gives matched
access in both directions.

The factors \(1/h\) and \(\theta_j\) are public and may have long
descriptions, but no hidden precision is queried. The geometric weight
\(\theta_j=\Gamma^{-j}\) uses \(O(T\log\Gamma)\) bits. In the exact-real
convention of the scalar-frontier theorem, the normalized readout
\(b=a_j/h\) is exact. For a finite-bit public readout, the audited identity
\(\|M_j^{-1}e\|=R\) shows that replacing \(b\) by \(\widetilde b\) with

\[
 \|\widetilde b-b\|_2\le \frac{\Delta}{10R}                \tag{23}
\]

perturbs \(q_j\) by at most \(\Delta/10\) for \(0\le z_j\le1\).
The effective promises become
\(\alpha'=\alpha+\Delta/10\) and
\(\beta'=\beta-\Delta/10\), with half-gap
\(\Delta'=9\Delta/10\). Recompute the public compiler constants using
\(c'=(\alpha'+\beta')/2=c\),
\(G'=1/\Delta'\), \(M_0'=2G'\), and \(C'=4G'\); Lemma 1 then applies
unchanged. Keeping the old \(G\) at the exact high boundary would not
provide enough margin to force \(t^*=1\).

Since \(\|b\|=1/(Rh)\), coordinate rounding on a support of size at most
\(N_0\) needs only
\(O(\log N_0+\log R+\log(1/\Delta)+\log(1/h))\)
scale/precision bits. The actual plateau support is smaller, but the
conservative ambient bound avoids overloading \(T\), which denotes the
number of outer blocks.
This is a rounding statement for the public readout and threshold
coefficients only. Rounding the hidden matrix \(M_j\) would require a
separate condition-number-sensitive resolvent budget and is not claimed.

## 6. Why the direct Forrelation sum is insufficient

Without the threshold variables, the natural final scalar would be
\(\sum_j\Phi_j\). The high promise allows every
\(\Phi_j\in[\beta,1]\), while the low promise allows
\(\Phi_j\in[-\alpha,\alpha]\). Different Boolean patterns can therefore
produce overlapping sums, so rounding does not recover their XOR.
Adversary composition cannot be invoked merely because every summand is
individually distinguishable.

Lemma 1 is the missing step: it converts the interval promise to an exact
optimizer bit using only a constant-size linear gadget. The large positive
coefficient \(C\) pins activation \(z=1\), the penalty \(-M_0r\) implements
the positive part of \(q-cz\), and \(t\le\min\{z,Gr\}\) saturates precisely
on the high branch.

## 7. Literature and novelty

Perfect negative-adversary composition is prior art; see Høyer, Lee, and
Špalek, [*Negative weights make adversaries
stronger*](https://arxiv.org/abs/quant-ph/0611054), and Reichardt,
[*Reflections for quantum query
algorithms*](https://doi.org/10.1137/120896201). The randomized theorem used
in (22) is Brody et al.,
[*A strong XOR lemma for randomized query
complexity*](https://doi.org/10.4086/toc.2023.v019a011).
The inner separation is the Forrelation line of Aaronson and Ambainis,
[*Forrelation: a problem that optimally separates quantum from classical
computing*](https://arxiv.org/abs/1411.5729), with the fixed-\(k\) extension
of Bansal and Sinha,
[*\(k\)-Forrelation optimally separates quantum and classical query
complexity*](https://arxiv.org/abs/2008.07003).

Optimization-value Boolean composition is known. Apers and Gribling,
[*Quantum speedups for linear programming via interior point
methods*](https://arxiv.org/abs/2311.03215), embed a
majority--OR--majority composition in an LP optimum. The local
batched-holonomy note composes parity blocks into one sparse-SDP scalar, and
the local multiplexed-LP note places independent inverse-history observables
at separated path scales but requires all increments.

A targeted search found no prior use of the threshold compiler (8)--(9) to
turn promised sparse inverse observables into exact optimizer bits, nor the
resulting combination of:

1. a unique optimizer of one sparse LP;
2. one bounded XOR-valued scalar coordinate;
3. \(T\) independent Forrelation inverse histories on one weighted central
   path;
4. only \(O(T)\) bounded inequalities and barrier parameter \(O(T)\); and
5. matched full-SQ classical lower bound
   \(\Omega(Tq^{\ell/2}/(r\ell))\) with a structured
   \(\Theta(T)\) quantum query law.

The composition theorems and inner Forrelation separation are prior art.
The candidate new result is the robust LP threshold compiler and this sparse
single-coordinate central-path instantiation.

## 8. Scope

This removes the explicit-checkpoint-output loophole and, unlike an averaged
observable, does not lose the \(T\) factor to coherent mean estimation.
It still does not prove that an algorithm must spend the cost sequentially
at each path scale. A static-oracle solver can target the final optimizer
function directly. The theorem is a total same-instance query lower bound
for one succinct QIPM-relevant optimizer output, not an online chronology
lower bound.

The coordinate \(P^*\in\{0,1\}\) is bounded. No constant-accuracy lower
bound is asserted for its amplitude in a
normalized state of the full optimizer: that amplitude can shrink with both
\(T\) and \(N_0\), and the accumulator coordinates can further change the
normalization.

Because \(\theta_T=\Gamma^{-T}\), the unique optimizer-coordinate theorem is
not automatically a constant-objective-gap LP-solving theorem. An
approximate optimizer may ignore the last block unless its global objective
gap is \(O(\theta_T)\), up to the public threshold-gadget constants.
Equation (1) is a designated-coordinate contract; transferring it to a
standard objective-gap contract requires charging this exponentially fine
gap or redesigning the scale schedule.
