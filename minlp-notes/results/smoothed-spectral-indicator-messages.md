# Exact smoothed indicator messages under spectral bounds

Date: 2026-09-22. Status: complete proof checked by two fresh independent
adversarial reviews without a substantive correction. Novelty is provisional.
The proof combines classical partition enumeration, the Sauer--Shelah
inequality, and finite-domain treewidth
dynamic programming. It does not introduce these ingredients.

## Main conclusion

For indicator quadratic optimization with a rational matrix satisfying
`mu I <= Q <= H I`, fixed graph treewidth, and bounded linear coefficients,
small independent perturbations of the indicator penalties permit exact
construction of every separator message on a prescribed bounded box in
polynomial expected bit complexity. The output is a list of rational full
quadratics whose minimum equals the message everywhere on the box. The list
contains every support that attains the message anywhere, including a support
that is optimal only at a tie or on the boundary. It can contain additional
supports.

The construction uses one common perturbation vector, with only `O(log n)`
random bits per coordinate. It is correct for every realization; only its
running time is averaged. It needs neither diagonal dominance nor a bound
on the size of biconnected blocks. The bound is polynomial in numerical
spectral and coefficient bounds and in inverse perturbation scale, rather
than their logarithms alone. The treewidth and separator dimension are fixed.

The central distinction from a representation bound is constructive:
restricted additive optimization oracles enumerate a short list at each
point of a parameter net. No recursive construction of child envelopes, no
invariant box for all intermediate conditional problems, and no algebraic
decomposition of the envelope are needed. Ordinary minima of full
quadratics are the exact output representation.

## 1. A first-moment bound for near-optimal binary supports

Let `Z` be any nonempty subset of `{0,1}^m`. Fix arbitrary deterministic
costs `g_z`. Let the independent random variables `xi_i` satisfy

```
Pr(xi_i in J) <= phi length(J)+tau
```

for every closed interval `J`. Put

```
F_z=g_z+xi dot z,
v=min_z F_z,
A_a={z in Z: F_z<=v+a},  a>=0.
```

**Lemma 1.**

```
E |A_a| <= (1+2 phi a+tau)^m.                         (1)
```

This estimate includes exact ties and arbitrary deterministic offsets.

**Proof.** A coordinate set `I` is *shattered* by a binary family if every
binary pattern on `I` appears in a member of that family. The upper half of
the classical sandwich inequality, a strengthening of the Sauer--Shelah
bound, states

```
|A| <= number of coordinate subsets shattered by A.  (2)
```

Here is an induction proof, including the counting convention. The empty
family shatters no set. A nonempty family shatters the empty set. Split a
family on its last coordinate, giving projected families `A_0,A_1`. Write
`U=A_0 union A_1` and `V=A_0 intersect A_1`. Then
`|A|=|U|+|V|`. Every set shattered by `U` is shattered by `A` without using
the last coordinate; every set shattered by `V` extends to a set shattered
by `A` with the last coordinate. These two collections are disjoint.
Induction proves (2).

Fix a coordinate set `I` of size `r` and condition on the noise outside
`I`. For each pattern `b` on `I`, let

```
C_b=min_(z_I=b) [g_z+sum_(j outside I) xi_j z_j].
```

If a pattern class is empty, `I` cannot be shattered. Otherwise, shattering
by `A_a` implies that every class minimum lies in `[v,v+a]`. Comparing the
zero pattern with each unit pattern gives

```
|C_ei+xi_i-C_0|<=a,  i in I.
```

The remaining coordinates therefore belong to fixed intervals of length
`2a`. Independence gives probability at most `(2 phi a+tau)^r`.
Taking expectations in (2) and summing over all `I` proves (1). There is
no union over the exponentially many supports. QED.

Uniform noise on `N` equally spaced points in `[-sigma,sigma]` satisfies
the interval assumption with `phi=1/(2 sigma)` and `tau=1/N`: an interval
of length `ell` contains at most `ell(N-1)/(2 sigma)+1` grid points.

## 2. Certified enumeration using approximate restricted minimization

For a partial assignment `p` of binary coordinates, suppose an oracle
either recognizes `Z_p` as empty or returns a support `z_p` together with
its exact cost `V_p=F_(z_p)` satisfying

```
min_(z in Z_p) F_z <= V_p <= min_(z in Z_p) F_z+epsilon.
```

Thus `LB_p=V_p-epsilon` is a certified lower bound. The oracle must work
under arbitrary fixed-bit restrictions. An unrestricted approximation
oracle alone is not enough.

Fix `delta>=0` and `epsilon>0`. Query the root cell, obtaining an initial
cost `U`; keep this number fixed. Store every nonempty cell with its oracle
candidate and lower bound. While the smallest stored lower bound is at
most `U+delta`, extract that cell and output its candidate. Partition the
remaining supports of this cell by their first free coordinate differing
from the extracted candidate. Query these at most `m` child cells, discard
empty cells, and insert the others. Stop if no cells remain or every lower
bound exceeds `U+delta`.

More explicitly, if the cell's free coordinates in order are
`j_1,...,j_r` and its candidate is `z`, child `ell` fixes
`j_h=z_(j_h)` for `h<ell` and `j_ell=1-z_(j_ell)`, while retaining the
parent's assignments. This is the classical first-difference partition.

**Lemma 2.** The output `E` satisfies

```
{z:F_z<=v+delta} subset E subset {z:F_z<=v+delta+2epsilon}.  (3)
```

There are no repeated outputs and at most `1+m|E|` oracle calls.

**Proof.** The cells always partition precisely the unextracted supports.
Every support of cost at most `v+delta` has cost at most `U+delta`, because
`U>=v`. Its cell's lower bound cannot exceed its cost, so the procedure
cannot stop while this support remains. Conversely an extracted candidate
has cost

```
V_p=LB_p+epsilon <= U+delta+epsilon <= v+delta+2epsilon.
```

Each extraction removes exactly one support and creates at most `m` cells.
The finite family guarantees termination for every oracle behavior
satisfying its approximation guarantee. QED.

This lemma does not require that candidates are extracted in cost order.
The oracle may return the worst permitted approximate candidate. The
probability analysis below applies to the original complete noise vector;
it does not condition on an adaptive search history.

## 3. Constructing a complete parametric dictionary

Let `q_z(t)` be deterministic `L`-Lipschitz functions on a nonempty compact
parameter set `T`. Define `F_z(t)=q_z(t)+xi dot z`. Assume an efficiently
constructible rational `epsilon/(2L)`-net `t_1,...,t_J` when `L>0`. If `L=0`, use one
parameter point. Assume exact rational evaluation and the restricted oracle
of Section 2 at each net point. To output full functions, also assume an
efficient exact construction of the representation of `q_z` from `z`.

Use a common ambient bound `n>=max(1,m)` and set

```
epsilon=delta=1/(12 n phi),
N=the smallest power of two with N>=2n.                (4)
```

For grid noise, use `phi=1/(2 sigma)` and `tau=1/N`. Run the enumeration
at every net point and take the union of its outputs, called `D`.

**Theorem 3.** The dictionary `D` contains every support that is optimal
at any parameter in `T`, and

```
E sum_j |E_j| <= e J.                                 (5)
```

Consequently

```
min_(z in D) F_z(t)=min_(z in Z) F_z(t),  for every t in T.  (6)
```

**Proof.** If `z` is optimal at `t`, and `w` is optimal at a net point
`t_j` within distance `epsilon/(2L)`, then

```
F_z(t_j)<=F_z(t)+epsilon/2
         <=F_w(t)+epsilon/2
         <=F_w(t_j)+epsilon.
```

Lemma 2 includes `z` in `E_j`, even if its only optimal occurrence is a tie.
All enumerated supports are valid members of `Z`, proving (6). Lemma 2
also gives `E_j subset A_(3epsilon)(t_j)`. By (1) and (4),

```
E |E_j| <= (1+6 phi epsilon+1/N)^m
          <=(1+1/n)^m <=e.
```

Summing proves (5). Independence across net points is unnecessary. QED.

For `T=[-R,R]^k`, with fixed positive integer `k` and `R,L>0`, take
`B=max(1,ceil(2kRL/epsilon))` equal intervals in each coordinate and their
Cartesian-product midpoints. These are rational when `R,L,epsilon` are
rational. Their covering radius is at most `kR/B<=epsilon/(2L)`, and

```
J<= (1+2kRL/epsilon)^k.                               (7)
```

If `R=0` or `k=0`, the parameter space is a singleton. The global optimum
is therefore already a special case of the construction.

**Work bound.** Suppose each restricted oracle call and exact function
construction costs a deterministic polynomial in the input size and
`1/epsilon`. The expected work is then polynomial whenever `J` is
polynomial. A heap implements the cell queue. At one net point there are
at most `1+m 2^m` cells ever generated, so each heap operation has
`O(m+log(m+1))` comparisons. Rational support strings can be deduplicated
using a binary trie in `O(m)` time per output. Thus all overhead is linear
in the number of outputs up to deterministic polynomial factors. Only the
first moment (5) is needed. An exact envelope represented as the minimum
of a list requires no algebraic arrangement computation.

For rational data and rational grid noise, assume the oracle's intermediate
values have uniformly polynomial bit length. Then the same argument proves
expected polynomial *bit* complexity. Sampling each coordinate uses
`log_2 N=O(log(n+1))` random bits. The algorithm returns a correct dictionary
for every grid-noise realization, including exceptional realizations with
many tied supports and a very large output.

## 4. Spectral bounds provide the conditional indicator-QP oracle

Consider rational data with a symmetric matrix `Q` and `n>=1` for

```
min x'Qx+c'x+sum_i (lambda_i+xi_i)z_i,
    x_i(1-z_i)=0,  z in {0,1}^n,
mu I <= Q <= H I,  mu>0,  |c_i|<=C.                   (8)
```

Here `mu,H,C` are certified rational bounds, and `lambda` is arbitrary
rational data. Supply a tree decomposition of the graph of nonzero
off-diagonal entries of `Q`, of fixed width `w` and polynomially many bags.

For disjoint internal and boundary index sets `I,S`, with `|S|=k` fixed,
define the conditional message excluding boundary-only terms by

```
M_(I,S)(t)=min [x_I' Q_II x_I+(c_I+2Q_IS t)'x_I
                    +sum_(i in I)(lambda_i+xi_i)z_i],
t in [-R,R]^k,  x_i(1-z_i)=0.                        (9)
```

For a support `A subset I`, its full quadratic is

```
q_A(t)= -1/4 (c_A+2Q_AS t)' Q_AA^(-1)(c_A+2Q_AS t)
        +sum_(i in A)lambda_i.                       (10)
```

For `A` empty the quadratic is zero. Its conditional minimizer is the
affine rational map

```
x_A(t)=-1/2 Q_AA^(-1)(c_A+2Q_AS t).                  (11)
```

Noise only adds the constant `sum_(i in A)xi_i` to (10).

Every principal submatrix has spectral bounds `mu,H`, and
`||Q_AS||_2<=H`. Hence throughout the boundary box,

```
||x_A(t)||_2 <= (C sqrt(n)+2H sqrt(k) R)/(2mu)
             <= M := (nC+2H k R)/(2mu),
||gradient q_A(t)||_2=||2Q_SA x_A(t)||_2<=2HM=:L.     (12)
```

The rational bounds `M,L` are polynomial in the displayed numerical
parameters. They hold for every support and every fixed-bit restriction.
If `M=0`, every conditional minimizer is zero and the oracle below is
trivial. If `I` is empty, the message is identically zero and needs no
enumeration.

At a rational net point `t`, construct an additive oracle as follows.
Take an even positive integer `B` satisfying

```
B^2 epsilon >= H n M^2.
```

Use the continuous grid `{-M+2Mj/B:j=0,...,B}`. Each internal vertex has
one inactive state `(z_i,x_i)=(0,0)` and `B+1` active states with `z_i=1`.
A fixed bit deletes the incompatible states. Active zero is retained:
fixing a bit to one does not require its continuous coordinate to be
nonzero. Assign the unary costs

```
Q_ii x_i^2+(c_i+2(Q_IS t)_i)x_i+(lambda_i+xi_i)z_i
```

and the internal edge costs `2Q_ij x_i x_j` to bags containing their
variables. The induced graph on `I` inherits width at most `w`. Standard
finite-domain dynamic programming minimizes this grid objective in
`poly(n) (B+2)^(w+1)` arithmetic operations: child tables are first minimized
over their internal states at each separator state and then added to each
parent-bag state. Each cost is assigned exactly once.

To prove the approximation guarantee, take an exact optimal support for
the restricted conditional problem and its continuous minimizer. Its
coordinates lie in `[-M,M]` by (12). Round its active coordinates to the
grid, leaving inactive coordinates zero. The error has squared norm at
most `nM^2/B^2`. Stationarity on the active support makes the first-order
term vanish. Therefore the objective increases by at most

```
e'Q_II e <= H ||e||_2^2 <= H n M^2/B^2 <= epsilon.    (13)
```

The optimal grid support therefore has conditional continuous optimum
within `epsilon` of the true restricted optimum. Evaluate that support
exactly using (10), returning this value and support. This is the oracle
required by Section 2. Restrictions can never make this particular model
infeasible, since every indicator pattern permits the all-zero continuous
vector; the general empty-cell convention still applies to enumeration.

All grid coordinates, costs, and messages in this finite-domain oracle
are rational. Their bit lengths are polynomial in the rational input,
`log B`, `log N`, and the net-point bit length. Sums involve polynomially
many input terms. Formula (10) and its coefficients have polynomial bit
length by rational linear algebra, or determinant bounds for the principal
systems. This is an exact bit-complexity statement, not a floating-point
conditioning claim.

## 5. All messages on a tree decomposition

Root the supplied tree decomposition. For an oriented child-parent edge,
let `S` be the bag intersection and `I` the vertices occurring in the child
subtree that do not belong to `S`. The running-intersection property
ensures no edge joins `I` to a vertex outside `I union S`. Thus (9) is the
usual exact subtree message, with boundary unary costs and boundary-only
edges excluded. Internal coefficients remain the principal matrix `Q_II`;
they are not an arbitrary selection of bag-assigned matrix terms.

Boundary indicators require no additional family of messages here. Their
only effect on the internal optimization is to require `t_j=0` when their
bit is zero. Their own penalties are excluded from (9). Restricting the
same full message to the appropriate coordinate face handles that case,
including the distinction between active zero and inactive zero at the
boundary.

Compute each message independently by Theorem 3 and the oracle in Section
4. Also compute the empty-boundary message with `I` all vertices; it
returns a global optimal support and rational continuous optimizer.
There are polynomially many messages and `k<=w+1`. The same noise vector
is used in every message. Linearity of expectation suffices to sum their
work; overlap and dependence between message noise sets cause no problem.

**Theorem 4.** Fix `w`. Given (8), a width-`w` decomposition with
polynomially many bags, a rational box radius `R>=0`, and rational
`sigma>0`, perturb each penalty independently by uniform noise on the
smallest power-of-two grid of at least `2n` points in `[-sigma,sigma]`.
There is an always-correct exact algorithm that constructs a quadratic
dictionary for every subtree message on `[-R,R]^|S|`, contains every
support attaining each message anywhere on that box, and returns a global
optimizer. Its expected bit complexity is polynomial in the rational input
length and in

```
n, C, H, 1/mu, R, 1/sigma,
```

where the degree may depend on `w`. Negative penalties are allowed.
No diagonal-dominance, bounded-degree, volume-growth, or bounded-block-size
assumption is used.

The output includes a rational affine minimizer map for each support if
desired. At any rational boundary point, comparing all dictionary entries
therefore returns both the exact value and a conditional optimizer. The
same is true for a queried real point in an exact real-arithmetic model.
The claim concerns a bounded prescribed box; it does not provide all
messages on an unbounded parameter domain.

## 6. Consequences and limits

An immediate consequence is a randomized additive approximation algorithm
for the *unperturbed* objective, with an always-valid certificate. Let
`v_xi` be the exact perturbed optimum and `(xhat,zhat)` its optimizer. Then

```
LB=v_xi-sum_i max(xi_i,0),
UB=v_xi-xi dot zhat,
LB <= original optimum <= UB,
UB-LB<=sum_i |xi_i|<=n sigma.                         (14)
```

The inequalities follow by subtracting `xi dot z` from every perturbed
objective value. The certificate is the standard bounded-perturbation
inequality. Choosing `sigma=eta/n` gives an always-valid additive gap at
most `eta` and expected complexity polynomial in `1/eta` under fixed
structural magnitude bounds. This is an additive guarantee, not a relative
FPTAS. Exact optimization of the original rational instance does not
follow by taking an unspecified infinitesimal perturbation.

The construction provides a theoretical route to reusable exact value
functions under penalty smoothing. Its exponents and repeated grid solves
may make it unsuitable as a direct solver implementation. It does not
establish a measured speedup, remove dependence on the spectral lower
bound, or cover arbitrary mixed-integer nonlinear constraints. Standard
worst-case exponential message examples remain possible; the expectation
allows rare large outputs.

The numerical coefficient dependence is substantive. A
[reviewed scaling obstruction](../notes/research-20260922-smoothing-magnitude-obstruction.md)
preserves the fixed-Hessian width-two hardness gap under every bounded
penalty perturbation when linear coefficients and penalties can have large
encoded magnitudes. Thus conditioning and treewidth alone cannot justify a
uniform bit-polynomial bound over such data unless NP is contained in ZPP.

## 7. Prior results and novelty status

- [Kozma and Moran (2013), *Shattering, Graph Orientations, and
  Connectivity*, Theorem 5](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v20i3p44/pdf)
  states the classical sandwich theorem whose upper inequality is (2).
  That source credits earlier work by Pajor, Bollobás and Radcliffe, Dress,
  and Holzman and Aharoni. The inequality is an established ingredient;
  its short induction is included here to make the probabilistic proof
  self-contained.
- [Lawler (1972), *A Procedure for Computing the K Best Solutions to
  Discrete Optimization Problems and Its Application to the Shortest Path
  Problem*](https://pubsonline.informs.org/doi/10.1287/mnsc.18.7.401)
  is the classical partition-enumeration antecedent. Its published abstract
  states the `O(K n c(n))` cost from an exact optimizer. Here the restricted
  oracle is additive, and certified lower bounds give the two-sided
  inclusion (3). The first-difference partition itself is classical.
- [Röglin and Teng (2009), *Smoothed Analysis of Multiobjective
  Optimization*](https://www.roeglin.org/publications/FOCS09.pdf), especially
  Sections 6.1--6.2, proves higher-winner-gap bounds and converts
  pseudopolynomial binary optimization into exact expected-polynomial
  smoothed optimization. Neither expected-polynomial smoothed optimization
  nor polynomial moments were introduced here. The present direct
  first-moment count applies to arbitrary deterministic support offsets and
  one shared random linear penalty; the net and restricted additive oracle
  construct complete bounded-parameter dictionaries.
- [Bhathena, Fattahi, Gómez, and Küçükyavuz (2026), *Solving Convex
  Quadratic Optimization with Indicators Over Structured
  Graphs*](https://arxiv.org/html/2603.02103v1), Definition 5 and its exact
  algorithm, explicitly control near-optimal support sets by a margin
  assumption. The present proof controls such sets in expectation under
  independent penalty perturbations and uses a spectral-bound grid oracle
  to construct all messages. A complete comparison of all their parameter
  dependences remains necessary before a publication priority claim.
- [Choi, Fattahi, Gómez, Han, and Lozano (2026), *Convexification of
  Mixed-Integer Quadratic Optimization via Decision
  Diagrams*](https://arxiv.org/html/2608.22815v1), provides structured exact
  diagrams and approximation theory using spectral decay and graph growth.
  Those results are substantial antecedents for representing and
  approximating indicator-QP value functions. The current theorem instead
  assumes fixed treewidth and directly smooths indicator penalties.

The inspected sources were the Kozma--Moran open article, the Lawler
publisher record and abstract, the open Röglin--Teng FOCS manuscript, and
the two cited arXiv HTML manuscripts.
The local [higher-moment note](../notes/research-20260922-envelope-higher-moments.md)
supplies the shattering argument and discusses its isolation antecedents.
The local [additive-oracle note](../notes/research-20260922-approximation-exact-smoothing.md)
supplies the spectral grid-oracle precursor for one optimizer. Its
independent [review](../notes/review-20260922-approximation-exact-oracle.md) checks
that precursor. These local reviews do not replace independent review of
the present complete-message construction.

No claim of first discovery is established by this comparison. The proposed
contribution is the complete algorithm and its spectral-bound indicator-QP
specialization. Two independent proof reviews support correctness; publication
priority remains unresolved. The [priority audit](../notes/review-20260922-fixed-treewidth-priority.md)
compares the strongest inspected antecedents and records the limits of this claim.

## Verification status

The following targeted command was run:

```
python3 code/research_20260922/check_oracle_all_messages.py
```

It passed 80 exact affine-family net instances with 1,132 rational net
points and 200 active supports. The checker computes each support's whole
activity interval by intersecting rational linear inequalities, then checks
that the net enumeration includes it. A dedicated instance contains a
support optimal only at a single tie point. The approximate oracle
deliberately returns the worst permitted approximate candidate. These
checks test the finite net/enumeration interaction and tie handling; they
do not prove the probabilistic bound or implement the spectral treewidth
oracle. A separate reviewer's enumeration and first-moment checker covers
the nonparametric ingredients without duplicating that suite here.

A fresh [independent review](../notes/review-20260922-nearopt-enumeration.md) checked
the full mathematical argument and passed. Its requested explicit
nonempty-parameter convention and sandwich-theorem citation have been
incorporated. That reviewer separately ran its own exact first-moment and
enumeration checks; their counts and scope are recorded in the review.
A second [independent integrated review](../notes/review-20260922-spectral-parametric-oracle.md)
checked the spectral conditional bounds, all-message construction, and bit
complexity without finding a substantive gap.

The coordinator also ran `python3 code/research_20260922/check_nearopt_enumeration.py`:
3,276 exact near-optimal-count cases over 18,270 noise outcomes and 12,420
adversarial enumeration runs passed. This included 75,522 extractions and
182,948 oracle calls, exact ties, empty child cells, and complete inclusion
of every support within the prescribed objective tolerance.

No Lean proof, project-wide checks, or CI inspection were performed for this
result. These checks do not establish a practical speedup or publication priority.
