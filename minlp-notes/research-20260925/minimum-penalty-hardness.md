# Computing the smallest exact augmented-Lagrangian penalty

Date: 2026-09-25. Status: proved constructions with independent adversarial
review; novelty comparison remains provisional. This note addresses the second
complexity question in the conclusion of Lefebvre and Schmidt's manuscript dated
December 15, 2025. It complements [penalty-geometry.md](penalty-geometry.md).

The strongest result below is a hardness construction with a binary box as the
native set, one linear equality, and the known unique primal solution zero.
Unless P = NP, no polynomial-time algorithm can always return an exact penalty
within any prescribed polynomial factor of the smallest exact penalty, measured
against the binary input length. This does not prevent computing a conservative
sufficient penalty efficiently. A second construction proves strong hardness
with unit coefficients but uses a harder native set.

## Definition and the distinction being studied

For a finite set X, a scalar linear residual r, and objective f, set

\[
 v^*=\min\{f(x):x\in X,\ r(x)=0\},\qquad
 D_\rho=\sup_{\lambda\in\mathbb R}\min_{x\in X}
 \{f(x)+\lambda r(x)+\rho|r(x)|\}.
\]

The parameter of interest is

\[
 \rho_*:=\min\{\rho\ge0:D_\rho=v^*\}.
\]

All constructions here have a finite, attained minimum. This is exactness of
the **dual value**, with the multiplier optimized. It is the convention of
Lefebvre and Schmidt's Definition 1. At the threshold, infeasible points may
tie with feasible points in an augmented subproblem. Requiring every augmented
minimizer to be feasible is a stronger property; its admissible penalty interval
can be open and have no smallest member.

## Binary-box construction

Take an instance of SUBSET SUM with positive integers
\(a_1,\ldots,a_n\) and positive target B. Append the item
\(a_{n+1}=B+1\), and choose any integer \(K\ge2\). Define

\[
 X=\{0,1\}^{n+2},\qquad f(x,q)=-q,\qquad
 r(x,q)=K\sum_{i=1}^{n+1}a_i x_i-(KB+1)q.
\tag{1}
\]

All native constraints are binary bounds. Optimizing any linear function over X
requires only choosing each bit independently. The only coupling constraint in
the primal is r = 0.

**Proposition 1.** The primal has the unique feasible point (x,q) = (0,0),
so its unique optimizer and optimum value zero are known without solving
SUBSET SUM.

**Proof.** If q = 1, the equality in (1) equates an integer divisible by K to
KB + 1, which is impossible. If q = 0, positivity of every item forces x = 0.
\(\square\)

Let S be the finite set of attainable subset sums after appending B + 1, and put

\[
 S_-:=\max\{s\in S:s\le B\},\qquad
 d_-:=K(B-S_-)+1,\qquad d_+:=K-1.
\tag{2}
\]

The empty subset guarantees S_- exists. The appended item guarantees the
smallest attainable sum above B is exactly B + 1. Appending it does not change
whether B itself is attainable, because every item is positive.

**Proposition 2.** For every \(\rho\ge0\),

\[
 D_\rho=\min\left\{0,-1+
 \rho\frac{2d_-d_+}{d_-+d_+}\right\},\qquad
 \rho_* = \frac12\left(\frac1{d_-}+\frac1{d_+}\right).
\tag{3}
\]

An optimal multiplier for the displayed dual value is

\[
 \lambda_\rho=\rho\frac{d_- - d_+}{d_-+d_+}.
\tag{4}
\]

**Proof.** For q = 1, the closest negative and positive residuals to zero are
−d_- and d_+, respectively. Both have objective −1. Their augmented values are

\[
 -1+(\rho-\lambda)d_-,\qquad -1+(\rho+\lambda)d_+.
\]

A convex combination with respective weights d_+/(d_-+d_+) and
d_-/(d_-+d_+) cancels the multiplier. Hence their smaller value is at most
\(-1+2\rho d_-d_+/(d_-+d_+)\), for every multiplier. The feasible zero
point separately bounds the dual value by zero.

At (4), both displayed values equal that upper bound, and
\(\rho\pm\lambda_\rho\ge0\). Thus every other q = 1 point, whose
residual has at least the corresponding absolute size, has augmented value
at least that bound. Every q = 0 point has nonnegative residual, objective
zero, and augmented value \((\rho+\lambda_\rho)r\ge0\). The bound is
therefore attained, proving (3). \(\square\)

A conservative penalty is already known: \(\rho=1\), with multiplier zero,
is sufficient for every instance in (1). Every nonzero residual is an integer,
so its absolute value is at least one, while the objective is either −1 or
zero. Thus the hardness below concerns closeness to the best penalty even
when a simple universal sufficient penalty is available.

## Complexity consequences

If the original SUBSET SUM instance is a YES instance, then S_- = B, so

\[
 \rho_* = \frac{K}{2(K-1)} > \frac12.
\tag{5}
\]

If it is a NO instance, then \(B-S_-\ge1\), so

\[
 0<\rho_*\le\frac12\left(\frac1{K+1}+\frac1{K-1}\right)
 =\frac{K}{K^2-1}.
\tag{6}
\]

**Theorem 3 (a fixed exactness query).** Deciding whether
\(D_{1/3}=v^*\) is coNP-hard even for the binary-box family (1), with
K = 4, the known unique primal optimizer zero, and objective consisting of the
single term −q. On this constructed family the decision problem is coNP-complete.
More precisely,

\[
 D_{1/3}=
 \begin{cases}
  -1/2,&\text{if the SUBSET SUM instance is YES},\\
  0,&\text{if the SUBSET SUM instance is NO}.
 \end{cases}
\tag{7}
\]

**Proof.** Equations (5)–(6) give YES threshold 2/3 and NO threshold at most
4/15 < 1/3. In the YES case d_- = 1, d_+ = 3, so (3) gives −1/2. Membership
in coNP for this family follows because a subset summing to B certifies
nonexactness. This is a classification of the specified family, not a claim
about unrestricted ALD exactness recognition. \(\square\)

Consequently, computing \(\rho_*\) is NP-hard. Even evaluating D at the
fixed penalty 1/3 to absolute error strictly smaller than 1/4 would decide
SUBSET SUM. This contrasts with \(D_0=-1\), which is immediate for every
member of this family.

**Theorem 4 (relative approximation).** Fix any polynomial p with p(L) ≥ 1.
Unless P = NP,
there is no polynomial-time algorithm that, on every member of (1) of binary
input length L, returns a rational \(\widehat\rho\) satisfying

\[
 \rho_*\le\widehat\rho\le p(L)\rho_*.
\tag{8}
\]

Thus even a guaranteed sufficient penalty cannot always be kept within a
polynomial factor of the best sufficient penalty in polynomial time.

**Proof.** Let \(\ell\) be the binary encoding length of the original
SUBSET SUM instance, and construct (1) with \(K=2^\ell\). Each coefficient
has O(\(\ell\)) bits and there are O(\(\ell\)) coefficients, so the
constructed input length L is O(\(\ell^2\)); writing the instance requires
polynomial time. In a YES instance every output satisfying (8) exceeds 1/2.
In a NO instance it satisfies

\[
 \widehat\rho\le p(L)\frac{2^\ell}{2^{2\ell}-1}<\frac12
\]

for every sufficiently large \(\ell\), because an exponential eventually
dominates the fixed polynomial \(p(O(\ell^2))\). The finitely many smaller
inputs can be solved by exhaustive enumeration. Testing the output against
1/2 would therefore give a polynomial-time algorithm for SUBSET SUM.
\(\square\)

The same construction excludes a symmetric multiplicative estimate
\(\rho_*/p(L)\le\widehat\rho\le p(L)\rho_*\): the YES lower bound
is \(1/(2p(L))\), whereas the NO upper bound is exponentially smaller.
For a fixed factor C, constant K with K + 1 > 2C already excludes the
one-sided guarantee; the ratio of (5) to (6) is (K + 1)/2.

These are bit-complexity results. They use potentially large item coefficients
and do not establish strong hardness for binary boxes. Rationally normalizing
the equality row multiplies both possible thresholds by the same reciprocal
scale, so the relative gap persists, but the small arithmetic spacing remains.
The result is not an APX-completeness statement: verifying feasibility of a
proposed penalty is itself coNP-hard, so the usual NPO conventions require care.

## Strong hardness with unit data

The box result does not give strong hardness. A separate construction does,
at the cost of allowing stable-set constraints in the native set.

For a simple graph G = (V,E), take binary x_v, p, m and native constraints

\[
 p+m\le1,\qquad x_v\le p+m\quad(v\in V),\qquad
 x_u+x_v\le1\quad(uv\in E).
\tag{9}
\]

Let \(f=-\sum_vx_v\) and \(r=p-m\). Every coefficient and right-hand
side lies in {−1,0,1}. The equality r = 0 forces p = m = 0 and then x = 0,
so again the unique primal point and value zero are known. Let α(G) be the
maximum stable-set size. The three native branches have residual zero and
objective zero, or residual ±1 and minimum objective −α(G). Thus

\[
 \min_X(f+\lambda r+\rho|r|)
 =\min\{0,\rho-\alpha(G)-|\lambda|\},\qquad
 D_\rho=\min\{0,\rho-\alpha(G)\},\qquad
 \rho_*=\alpha(G).
\tag{10}
\]

Computing the minimum exact penalty is therefore strongly NP-hard even with
one equality, unit data, and a supplied unique primal optimizer. For the family
(G,k), deciding exactness at integer k is coNP-complete: it is precisely the
condition α(G) ≤ k. At equality k = α(G), infeasible maximum stable sets tie;
every augmented minimizer at multiplier zero is feasible only for ρ > α(G).

This short embedding shows that hardness need not come from numerical
precision. Its native subproblem is already difficult, so the binary-box
construction isolates a stronger structural limitation.

## Literature comparison and novelty boundary

- **Lefebvre and Schmidt, manuscript dated December 15, 2025.** Definition 1
  uses zero optimized ALD gap as exactness. Theorem 15 computes a sufficient
  MILP penalty in polynomial time. Its conclusion, p. 24, explicitly asks
  whether the *smallest* gap-closing penalty can be computed in polynomial
  time and conjectures a negative answer. Theorems 3–4 answer that question
  for growing binary dimension, with stronger restrictions and an approximation
  lower bound. They do not address a fixed-total-dimension interpretation.
  [Primary manuscript](https://optimization-online.org/wp-content/uploads/2024/07/exact-penalty-for-minlp-1.pdf),
  [local text](parametric-sources/lefebvre-schmidt-2025.txt).
- **Alessandroni, Ramos-Calderer, Roth, Traversi, and Aolita, _Alleviating the
  quantum Big-M problem_ (2025).** Section IV.A, Lemma 1 of arXiv v4 proves
  hardness of choosing the optimal exact QUBO penalty and of testing a
  supplied penalty under a separation promise. Its reduction already has
  the known original optimum at zero. Neither generic penalty-choice
  hardness nor hardness with a known primal optimizer is new. The reduction
  uses a quadratic objective and squared penalty for the vector constraint
  x = 0, without optimizing linear multipliers. On binaries its penalty is
  \(M\sum_i x_i\), which unrestricted linear multipliers reproduce with
  augmentation coefficient zero. Thus this prior reduction does not prove
  optimized-ALD hardness. The proposed contribution is the restricted
  linear-objective, scalar-residual, binary-box result and its approximation
  lower bound. [Primary journal article](https://www.nature.com/articles/s41534-025-01067-0),
  [primary preprint](https://arxiv.org/abs/2307.10379).
- **Dolgopolik, _Minimax Exactness and Global Saddle Points of Nonlinear
  Augmented Lagrangians_
  (2021).** Defines least minimax exact penalty parameters and studies their
  relationship with augmented duality and global saddle points. These
  concepts predate the present note. The inspected parts concern existence
  and localization, not computational lower bounds.
  [Primary article](https://jano.biemdas.com/issues/JANO2021-1-5.pdf).
- **Díez García et al., _Exact and Sequential Penalty Weights in Quadratic
  Unconstrained Binary Optimisation with a Digital Annealer_ (2022).** Studies
  efficient sufficient upper bounds and sequential tuning for QUBO penalty
  weights. Its formulas concern feasibility of global QUBO minimizers, which
  must be distinguished from the optimized-multiplier norm ALD used here.
  [Open author manuscript](https://ore.exeter.ac.uk/rest/bitstreams/185242/retrieve).

The [publication priority audit](publication-penalty-priority-audit.md)
also directly checks Alessandroni et al.'s
[2026 successor on probabilistic penalization weights](https://arxiv.org/html/2604.02416v1)
and Mirkarimi et al.'s
[linear Ising penalty discussion](https://arxiv.org/html/2404.05476v2).
The former uses probabilistic approximate-solver guarantees. The latter
gives a nonexistence-or-hardness observation for linear penalty tuning.
Neither inspected statement supplies the restricted polynomial-factor
optimized norm-ALD theorem proved here; both are relevant prior work on
the broader difficulty of choosing useful penalty weights.

Searches on 2026-09-25 included combinations of “smallest penalty parameter,”
“minimum penalty,” “least exact penalty parameter,” “optimal penalty,”
“augmented Lagrangian,” “QUBO,” “NP-hard,” “coNP,” and “approximation.”
The local literature was searched for equivalent penalty-complexity wording.
Unsuccessful searches are not evidence of novelty. The general scalar
threshold formula and its two-point proof are elementary consequences of
linear programming duality and are not proposed as independent contributions.
See [the independent novelty audit](minimum-penalty-novelty.md) for the
source-by-source comparison, additional sources, and limitations of the search.

## Verification, meaning, and limitations

The targeted command

```sh
python research-20260925/check_minimum_penalty_hardness.py
```

passed on 2026-09-25. It checked 976 binary-box instances and 75 unit-data graph
instances using exact rational arithmetic, comparing the claimed formula with
all zero-mean mixtures of one or two native residual points. It also evaluated
the explicit multiplier, checked the unique primal point, and checked the
SUBSET SUM gap. An independent reviewer separately checked 120 seeded box
instances by enumerating the breakpoints of the piecewise-linear dual, using
four penalties per instance. See
[the independent review](minimum-penalty-independent-review.md).

The arithmetic checks establish the formulas on those finite instances. They
do not prove the reduction for all inputs, establish novelty, or check a
polynomial-time algorithm. The symbolic proofs above provide the general
argument. No project-wide checks or CI checks were run for this note.

The practical implication is a limit on guaranteed penalty calibration, not
a new solver. Even knowing the complete solution of the primal need not make
the best penalty easy to compute: the threshold records the quality and
distance of infeasible native points. Useful methods can still exploit special
structure, compute conservative bounds, solve the calibration problem with
oracles, or accept instance-dependent guarantees. These constructions do not
show that such methods fail in practice, nor that conservative penalties are
always unusable. A practical advance would require identifying classes where
the relevant nearest residuals can be bounded sharply or found efficiently.
