# Exact global optimization with a fixed core and many small polyhedral blocks

Date: 2026-09-05. Status: two independent proof reviews passed:
[first](../notes/review-fixed-core-block-optimization.md),
[second](../notes/review-fixed-core-block-optimization-second.md).
The final 2016 source confirms that these pooling cases were posed as open;
the search for later prior resolutions remains provisional.

The theorem gives polynomial bit complexity for a nonconvex problem
whose number of variables can grow without bound. Three dimensions remain
fixed: the nonlinear core, each local continuous block, and the vector of
aggregate constraints. It implies a polynomial-time algorithm for standard
pooling with fixed numbers of inputs and pools and unrestricted numbers of
outputs and quality attributes, including capacities and bypass flows.
It also gives a second tractable class: fixed numbers of pools and quality
attributes, with arbitrarily many inputs and outputs, when bypass arcs are
absent.

These corollaries answer the fixed-input and fixed-quality portions of
Haugland's published question for a fixed number of pools. The corresponding
fixed-output case with unrestricted inputs and qualities is not settled here.

This is an exact complexity result based on real-algebraic algorithms. Its
parameter-dependent exponent can be large; it is not a practical runtime
claim, a strongly polynomial algorithm, or a fixed-parameter tractability
claim. Existing ingredients and novelty limits are recorded below.

## 1. Model and theorem

Fix nonnegative integers \(r,k\) and positive integers \(d,D\). All input
coefficients are rational. Let \(C\subset\mathbb R^r\) be a compact set
given by a quantifier-free polynomial formula of degree at most \(D\).
Its compactness is part of the hypothesis. For \(j=1,\ldots,N\), let

\[
P_j(x)=\{z_j\in\mathbb R^{d_j}:B_j(x)z_j\le b_j(x)\},
\qquad 1\le d_j\le d,
\]

where the entries of \(B_j,b_j\) are polynomials in \(x\) of degree at
most \(D\). The inequalities include explicit finite rational box bounds
on every coordinate of \(z_j\); \(P_j(x)\) is allowed to be empty.
The entries of \(A_j(x)\in\mathbb R^{k\times d_j}\),
\(b(x)\in\mathbb R^k\), \(c_j(x)\in\mathbb R^{d_j}\), and \(c_0(x)\)
are also polynomials of degree at most \(D\). Consider

\[
\tag{1}
\begin{aligned}
\min\quad &c_0(x)+\sum_{j=1}^N c_j(x)^\top z_j,\\
\text{s.t.}\quad &x\in C,\quad z_j\in P_j(x)\quad(j=1,\ldots,N),\\
&\sum_{j=1}^N A_j(x)z_j=b(x).
\end{aligned}
\]

**Theorem 1.** For fixed \(r,d,k,D\), feasibility and global optimization
of (1) can be solved in time polynomial in its rational input bit length.
If feasible, an exact real-algebraic optimizer and optimum value can be
returned, with polynomial encoding length. The number of local blocks and
the number of inequalities in any block need not be bounded.

A fixed number of aggregate inequalities can replace the equations: append
bounded scalar slack blocks. Such finite bounds follow by interval arithmetic
from finite core and leaf boxes when these boxes are explicitly available;
alternatively supply slack bounds as part of the input. The pooling application
below has explicit simplex and flow boxes, so this reduction is immediate.

Fixed binary design variables may belong to the core: the equations
\(x_i(x_i-1)=0\) encode them within the fixed-dimensional formula. General
integer core variables with large domains are not claimed.

## 2. Local vertex formulas and their validity

Let \(M_j\) be the number of inequalities defining block \(j\). Enumerate
every \(d_j\)-row subset \(I\) and write

\[
\delta_{jI}(x)=\det B_{jI}(x),\qquad
p_{jI}(x)=\operatorname{adj}(B_{jI}(x))b_{jI}(x).
\]

When \(\delta_{jI}\ne0\), the candidate vertex is
\(v_{jI}=p_{jI}/\delta_{jI}\). Its feasibility is determined by the signs
of \(\delta_{jI}\) and the polynomials

\[
\tag{2}
e_{jIh}(x)=B_{jh}(x)p_{jI}(x)-b_{jh}(x)\delta_{jI}(x),
\quad h=1,\ldots,M_j.
\]

Specifically it is feasible exactly when \(e_{jIh}/\delta_{jI}\le0\)
for every \(h\). Identically zero determinant candidates can be discarded.
The determinant and numerator degrees are at most \(dD\), and the
degrees in (2) are at most \((d+1)D\).

Every nonempty bounded polyhedron has a vertex. At a vertex in
\(\mathbb R^{d_j}\), the active row normals span \(\mathbb R^{d_j}\);
otherwise a nonzero direction orthogonal to every active row gives a small
feasible segment through that point. Thus some \(d_j\) active rows are
independent. This applies also to a lower-dimensional polytope and a
singleton. Consequently \(P_j(x)\ne\varnothing\) exactly when at least
one enumerated candidate has nonzero determinant and passes (2).

## 3. Simultaneously selecting support vertices

Use aggregate dimension \(h=k+1\), and define

\[
W_j(x)=\begin{pmatrix}A_j(x)\\c_j(x)^\top\end{pmatrix},\qquad
T_j(x)=W_j(x)P_j(x),\qquad
w(x,v)=\begin{pmatrix}b(x)\\v-c_0(x)\end{pmatrix}.
\]

Introduce \(\lambda\in\mathbb R^h\). The support score of a valid
candidate is the rational function

\[
\rho_{jI}(x,\lambda)
=\frac{n_{jI}(x,\lambda)}{\delta_{jI}(x)},\qquad
n_{jI}=\lambda^\top W_j(x)p_{jI}(x).
\]

Pairwise order within one block is determined by determinant signs and

\[
\tag{3}
n_{jI}\delta_{jJ}-n_{jJ}\delta_{jI}.
\]

Let \(\mathcal P\) contain every determinant, every feasibility polynomial
(2), and every comparison polynomial (3), omitting identically zero
polynomials while remembering their fixed zero sign. There are polynomially
many polynomials in \(\mathcal P\), since
\(\binom{M_j}{d_j}\le M_j^d\). Their degrees depend only on \(d,D\),
their coefficient bit lengths are polynomial, and they involve only
\(r+h\) variables.

Enumerate all realizable sign conditions of \(\mathcal P\), including
conditions with zero signs. Algorithms for sign determination or a
sign-invariant cylindrical algebraic decomposition do this in polynomial
bit time when the number of variables and degrees are fixed. The total
number of realizable sign conditions is polynomial in \(|\mathcal P|\).
These are standard real-algebraic tools, rather than new claims here.
The primary algorithmic source is Basu, Pollack, and Roy,
[*On the combinatorial and algebraic complexity of quantifier elimination*](https://www.math.purdue.edu/~sbasu/jacm95.ps),
§3.2 (realizable sign conditions); §3.1.3 supplies algebraic sample points.
A [later author survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf)
gives more accessible background.

For each realizable sign condition \(\sigma\), its signs determine:

1. the valid candidate bases in every block;
2. whether any block is empty;
3. a support-maximizing candidate in every nonempty block, taking the first
   in a fixed index order in case of a tie.

The selected basis \(I_j(\sigma)\) is the same throughout the entire
realization of \(\sigma\), even if that realization is disconnected.
No topological connectedness assertion is needed: validity and comparisons
are determined solely by signs. This step avoids the exponential Cartesian
product of local basis choices.

Discard a sign condition if it identifies an empty block. For a retained
condition, abbreviate \(\delta_j=\delta_{j,I_j(\sigma)}\) and
\(n_j=n_{j,I_j(\sigma)}\), and put

\[
H_\sigma(x)=\prod_{j=1}^N\delta_j(x)^2>0
\quad\text{on the realization of }\sigma,
\]

\[
\tag{4}
F_\sigma(x,v,\lambda)
=\lambda^\top w(x,v)H_\sigma(x)
-\sum_{j=1}^N n_j(x,\lambda)\delta_j(x)
\prod_{i\ne j}\delta_i(x)^2.
\]

On this sign condition, \(F_\sigma\le0\) is exactly the support
inequality

\[
\tag{5}
\lambda^\top w(x,v)
\le\sum_j\max_{z_j\in P_j(x)}\lambda^\top W_j(x)z_j.
\]

The use of squared denominators avoids changing the inequality direction.
The degrees of (4) grow at most linearly in \(N\); they are not bounded
solely by \(r,d,k,D\). This causes no exponential encoding blowup: the
number of variables in (4) is fixed, so a degree-\(O(N)\) polynomial has
only polynomially many monomials. Products and sums in (4) can be expanded
in polynomial time, with polynomial coefficient bit lengths. Repeating
this for polynomially many sign conditions remains polynomial.

## 4. A formula with a fixed number of variables

Represent each sign condition by the conjunction
\(S_\sigma(x,\lambda)\) of the indicated strict inequalities and
equalities. Define the polynomial-size quantifier-free formula

\[
\tag{6}
\Phi(x,v,\lambda)
=\bigvee_{\sigma\text{ retained}}
\left[S_\sigma(x,\lambda)\ \wedge\ F_\sigma(x,v,\lambda)\le0\right].
\]

**Lemma 2.** For every fixed \(x,v\), there exist block vectors with
\(z_j\in P_j(x)\), aggregate equations, and objective exactly \(v\)
if and only if

\[
\tag{7}
\forall\lambda\in\mathbb R^h\quad\Phi(x,v,\lambda).
\]

**Proof.** If any block is empty, its candidate-validity signs make every
sign condition containing \((x,\lambda)\) discarded, for every
\(\lambda\). Thus (7) is false. If all blocks are nonempty, the sum
\(T(x)=T_1(x)+\cdots+T_N(x)\) is compact convex. A vector belongs to a
nonempty compact convex set exactly when it satisfies every support-function
inequality. Its support function is the sum of the support functions of
the summands. Formula (6) expresses precisely these inequalities by (5).
Therefore (7) holds exactly when \(w(x,v)\in T(x)\), which is the
required existence of the block vectors. \(\square\)

It follows that the attainable objective values of (1) are described by

\[
\tag{8}
\exists x\in\mathbb R^r\quad
\left[x\in C\ \wedge\ \forall\lambda\in\mathbb R^h\,
\Phi(x,v,\lambda)\right].
\]

There are only \(r+h+1\) free and bound variables. The formula size,
degree, and coefficient bit length are polynomial in the original input.
Fixed-dimensional quantifier elimination therefore produces an equivalent
univariate formula in polynomial bit time. One may use the standard
quantifier-elimination complexity bounds of Basu, Pollack, and Roy,
Theorem 1.3.1 in the primary reference above; they remain polynomial for
fixed total dimension even with the degree growth in (4).

The full feasible set of (1) is closed and contained in a finite product
of compact core and leaf boxes. Its objective is continuous, so its set
of values is compact. Standard univariate root isolation decides emptiness
and extracts the smallest attainable value \(v^*\) exactly. For a direct
joint optimizer construction, let \(E(x,v)\) abbreviate core membership
and (7), and form

\[
\Theta(x,v)=E(x,v)\ \wedge\
\neg\exists x',v'\,[v'<v\ \wedge\ E(x',v')].
\]

Its bound variables, including those inside the two occurrences of \(E\),
are renamed as needed; their total number is still fixed. Quantifier
elimination followed by algebraic sampling yields an optimum pair
\((x^*,v^*)\). A rational univariate sample representation places all
coordinates in one extension \(\mathbb Q(\alpha)\) of polynomial degree,
with polynomial coefficient encoding. The sample-point bounds are those
of §3.1.3 in the primary Basu–Pollack–Roy reference.

## 5. Recovering all continuous blocks

At \(x=x^*\), impose the local inequalities, aggregate equations, and

\[
\sum_jc_j(x^*)^\top z_j=v^*-c_0(x^*).
\]

This is a feasible LP system of polynomial dimension whose coefficients
lie in the same polynomial-degree real-algebraic extension. Its coefficient
encoding lengths are polynomial because the original polynomials have
bounded degree and the sampled coordinates have polynomial descriptions.

Adler and Beling's algebraic LP algorithm has runtime polynomial in the
LP input encoding, dimension, and degree of a common extension containing
the coefficients. It therefore recovers the \(z_j^*\) in polynomial bit
time. The field-degree condition is essential; no assertion that arbitrary
algebraic-coefficient LPs are polynomial in their separate coefficient
encodings is needed.
[Adler and Beling (1994), *Polynomial algorithms for linear programming over the algebraic numbers*, §5, Remark 1](https://adler.ieor.berkeley.edu/ilans_pubs/lp_algebraic_1994.pdf).

Together, Sections 2–5 prove Theorem 1. \(\square\)

## 6. Pooling with fixed inputs and fixed pools

**Corollary 3.** Fix positive integers \(m,p\). Standard pooling with at
most \(m\) inputs and \(p\) pools can be solved exactly in polynomial bit
time, while the numbers of outputs and quality attributes are unrestricted.
The statement allows input capacities, pool capacities, arc capacities,
lower and upper output throughputs and qualities, bypass arcs, and rational
linear arc costs. Finite rational flow upper bounds are assumed, or can be
derived from finite rational input or output capacities. There are no
pool-to-pool arcs in this corollary.

**Proof.** Remove pools having no incoming arcs; all their outgoing flows
must be zero, and conflicting positive lower bounds imply infeasibility.
For every remaining pool \(\ell\), use source fractions

\[
q_{i\ell}\ge0,\qquad \sum_{i=1}^m q_{i\ell}=1,
\]

with \(q_{i\ell}=0\) on missing input-to-pool arcs. These variables form
a compact core of dimension at most \(mp\). For output \(j\), its block
contains pool-to-output flows \(v_{\ell j}\) and bypass flows \(z_{ij}\),
so its dimension is at most \(p+m\). Missing arcs have flow fixed to zero.

For quality \(a\), let input quality be \(C_{ia}\) and output upper
bound be \(U_{ja}\). The output quality constraint is

\[
\tag{9}
\sum_\ell\left(\sum_iC_{ia}q_{i\ell}-U_{ja}\right)v_{\ell j}
+\sum_i(C_{ia}-U_{ja})z_{ij}\le0.
\]

The lower-bound version has the reverse sense with the lower quality bound.
All quality, output-throughput, and outgoing-arc bounds belong to the local
block. Increasing the number of qualities increases only its row count.

Writing \(V_\ell=\sum_jv_{\ell j}\), the remaining input-to-pool flow
is \(x_{i\ell}=q_{i\ell}V_\ell\). Pool capacities, input-to-pool arc
bounds, and input capacities are aggregate constraints of the forms

\[
\tag{10}
L_\ell\le\sum_jv_{\ell j}\le U_\ell,
\]
\[
L_{i\ell}\le\sum_jq_{i\ell}v_{\ell j}\le U_{i\ell},
\]
\[
L_i\le\sum_j\left(\sum_\ell q_{i\ell}v_{\ell j}+z_{ij}\right)
\le U_i.
\]

Their row count is bounded by \(2(p+mp+m)\). Bounded slack blocks turn
them into equations of the required type. An input-to-pool arc cost
\(c_{i\ell}x_{i\ell}\) contributes coefficient
\(\sum_i c_{i\ell}q_{i\ell}\) to each \(v_{\ell j}\). Other arc
costs are already local. All coefficient polynomials are affine in the core.

For a positive-throughput pool, fractions extracted from any original feasible
flow recover exactly this model. For a zero-throughput pool, choose any
fraction vector on its nonempty set of incoming arcs. Conversely, defining
\(x_{i\ell}=q_{i\ell}V_\ell\) ensures pool mass balance, source
composition, all capacities, and output quality constraints. Thus the
reformulation is exact, including inactive pools. Theorem 1 applies.
\(\square\)

A fixed number of core design binaries, such as pool activation or input-to-pool
arc selection, can be added without changing the polynomial conclusion.
An unbounded collection of output activation or assignment binaries is
outside this corollary.

## 7. Fixed pools and qualities, unrestricted inputs and outputs

**Corollary 4.** Fix positive integers \(p,K\). Standard pooling without
bypass arcs, with at most \(p\) pools and \(K\) quality attributes, can
be solved exactly in polynomial bit time. The numbers of inputs and outputs
are unrestricted. Rational capacities and lower bounds on inputs, pools,
outputs, and arcs, lower and upper output quality specifications, and linear
arc costs are allowed. Finite rational flow bounds are assumed or derived
from finite rational input or output capacities.

**Proof.** The core consists of the \(pK\) pool qualities \(q_{\ell a}\),
bounded between the smallest and largest input quality for attribute \(a\).
For a positive-throughput pool its actual quality lies in this interval.
An inactive pool can be assigned any quality in the same interval, so these
core bounds lose no physical feasible solution. An instance with no inputs
has all flows zero and is processed directly.

For each input \(i\), create a block of the \(p\) inlet flows
\(x_{i\ell}\), with its input throughput bounds and individual arc bounds.
For each output \(j\), create a block of the \(p\) outflows
\(v_{\ell j}\), with its output throughput and arc bounds and its quality
constraints

\[
\sum_\ell(q_{\ell a}-U_{ja})v_{\ell j}\le0,
\qquad
\sum_\ell(L_{ja}-q_{\ell a})v_{\ell j}\le0.
\]

Missing arcs are fixed to zero. The only linking equations are pool mass
and quality balances:

\[
\tag{11}
\sum_i x_{i\ell}-\sum_jv_{\ell j}=0,
\]
\[
\sum_i C_{ia}x_{i\ell}-q_{\ell a}\sum_jv_{\ell j}=0
\quad(\ell=1,\ldots,p;\ a=1,\ldots,K).
\]

There are \(p+pK\) equations. Pool throughput bounds add at most \(2p\)
aggregate inequalities. They can be converted to equations with bounded
slack blocks as before. The objective is linear across the inlet and output
blocks. Thus the core dimension, block dimension, and linking dimension are
all fixed. This is exactly the usual concentration formulation of standard
pooling, so Theorem 1 applies. \(\square\)

A fixed number of bypass arcs can be allowed as well. Put their bounded flow
variables in the core and subtract their contributions from the appropriate
input availability, output throughput, and output quality right-hand sides.
These are polynomial changes in a fixed-dimensional core. Arbitrarily many
bypass arcs are not covered by this extension: they can link an unbounded
number of input and output blocks. Corollary 3 instead permits arbitrarily
many bypasses by fixing the input count.

**Published-source comparison.** Haugland's final 2016 article, §6,
printed p. 214, asks whether fixing the pool count together with a bound on
the number of sources, terminals, or qualities gives polynomial algorithms.
Its two-source/two-terminal hardness statements allow the pool count to grow;
they do not contradict Corollary 4. Corollaries 3 and 4 answer the source
and quality portions, respectively. See the
[supplied final article](../literature/papers/haugland2016-the-computational-complexity-of-the/fulltext.md)
and [publisher record](https://doi.org/10.1007/s10898-015-0335-y).

An earlier MAGO 2014 abstract contains an unsupported two-pool hardness
statement absent from the final article; the final article instead poses
the relevant question. We use the final theorem statements and open-question
wording as the literature comparison. This observation does not establish
that a formal retraction or correction of the abstract was published.
The [source audit](../notes/pooling-fixed-pools-qualities-source-audit.md)
records the distinction.

## 8. Literature comparison, verification, and limitations

- Haugland's final 2016 article explicitly asks about a fixed pool count
  combined with fixed sources, terminals, or qualities. The fixed-source
  and fixed-quality cases follow from Corollaries 3–4; the fixed-terminal
  case remains open in this investigation.
  [*The computational complexity of the pooling problem*, §6, p. 214](https://doi.org/10.1007/s10898-015-0335-y).
- Boland, Kalinowski, and Rigterink establish the one-pool fixed-input case
  and ask about polynomial algorithms with two pools and bounded numbers of
  other node/quality types. Corollary 3 would answer the bounded-input case
  for any fixed pool count.
  [Primary preprint, Theorem 1 and §4](https://optimization-online.org/wp-content/uploads/2015/08/5059.pdf).
- Haugland and Hendrix (2016) independently give a one-pool fixed-source
  algorithm. Their Theorem 4.1 and discussion distinguish a network convention
  without direct bypasses. The supplied repository full text is in
  [its literature folder](../literature/papers/haugland2016-pooling-problems-with-polynomial-time/fulltext.md).
- Baltean-Lugojan and Misener's piecewise-parametric results use one quality
  and remove feed and pool capacities under Assumption 2.2. Those important
  subclasses do not imply the capacitated, arbitrary-quality corollary here.
  [*Piecewise parametric structure in the pooling problem*](https://pmc.ncbi.nlm.nih.gov/articles/PMC6417401/).
- The local [common-factor fixed-linking theorem](common-factor-fixed-linking-optimization.md)
  uses a scalar parameter, interval leaves, and bounded-row LP basis
  enumeration. The present support construction handles fixed-dimensional
  polyhedral leaves and several nonlinear core variables. It relies on
  established support-function separation, real quantifier elimination,
  and algebraic-coefficient LP algorithms.
- A [nearby block-structured LP algorithm](https://arxiv.org/abs/2002.07745)
  addresses linear data and few linking rows. The varying nonlinear core
  requires an additional global analysis.
- Two independent proof reviews
  ([first](../notes/review-fixed-core-block-optimization.md),
  [second](../notes/review-fixed-core-block-optimization-second.md)) passed
  Theorem 1, Lemma 2, both pooling corollaries, and the bounded-bypass
  extension. A search for later prior resolutions remains provisional. No
  practical implementation of the general real-algebraic algorithm has
  been built.

The [support-reduction checker](../code/fixed_core_blocks/check.py) passed
1,971 exact rational support/denominator comparisons against explicit small
Minkowski sums, together with independent SciPy LP comparisons. Tests include
parameter values where candidate determinants vanish, lower-dimensional
singletons, empty blocks, and both denominator signs. These checks support
the algebraic reduction; they do not implement or experimentally assess the
full quantifier-elimination algorithm.

Compact polyhedral local blocks are essential to the support representation.
Allowing each leaf to be the discrete set \(\{0,1\}\) makes even one
aggregate equation encode subset sum when the core is absent. Taking convex
hulls of such leaves would solve a relaxation and would not justify an
integer optimization theorem.

Nor can arbitrary small convex nonlinear leaves be substituted without an
arithmetic qualification. For example, independent bounded scalar blocks
\(0\le z_j,\ z_j^2\le a_j\) and objective \(-\sum_jz_j\) already have
optimum \(-\sum_j\sqrt{a_j}\). For distinct prime \(a_j\), this single
value has algebraic degree \(2^N\): the independent sign changes give
distinct conjugates, since the square roots of distinct primes are linearly
independent over \(\mathbb Q\). This happens despite no core and no
linking constraints. The theorem avoids this obstruction because local
polyhedral support values are rational functions of the same
fixed-dimensional core. This example concerns exact algebraic output size;
it does not imply that numerical approximation of those independent convex
blocks is difficult.
