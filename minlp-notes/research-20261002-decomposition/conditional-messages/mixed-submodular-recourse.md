# Exact conditional recourse with concave coordinates and a convex block

Date: 2026-10-02. Status: direct theorem and certificate construction;
targeted exact diagnostic and independent review are recorded below.
This supplements the [minimum-cut recourse construction](note.md).
The algorithm combines established convex quadratic programming and
submodular minimization. It does not claim a new general submodular
minimization algorithm, and general submodular box QP is outside its scope.

## 1. A broader box-stable quadratic oracle

Consider the rational conditional problem

\[
 \min_{\ell\le z\le u}
 q(z)=\tfrac12z^{\mathsf T}Az+b^{\mathsf T}z+c,
 \qquad A=A^{\mathsf T}\in\mathbb Q^{r\times r}.              \tag{1}
\]

Supply signs `epsilon_i in {-1,1}` such that

\[
           \varepsilon_i\varepsilon_j A_{ij}\le0
                         \quad(i\ne j).                    \tag{2}
\]

Partition the coordinates into `D` and `C`, requiring

\[
              A_{ii}\le0\ (i\in D),\qquad A_{CC}\succeq0.   \tag{3}
\]

One possible partition takes all nonpositive-diagonal coordinates in
`D`; the remaining principal block must then pass the PSD test. A supplied
partition satisfying (3) also works. The PSD condition is essential to
the oracle below; (2) alone is not being asserted sufficient.

**Theorem.** Under (2)--(3), (1) has an exact rational global optimizer,
value, and a polynomial-size certificate computable in polynomial bit
time. The polynomial exponent is absolute. This conclusion remains true
after any rational coordinate-box restriction and any rational change
to the linear and constant terms. Empty boxes are detected. Any subset
of `D` may instead consist of integer coordinates: first replace their
lower and upper bounds by their ceilings and floors. All coordinates of
`C` must remain continuous.

The statement supplies the full exact box-stable interface used by the
[quadratic recourse theorem](../../research-20261002/new-direction/smoothed-box-stable-recourse.md).
It permits arbitrarily many concave coordinates and arbitrarily many
coupled convex coordinates, with no restriction on their graph width.

## 2. Endpoint reduction and a submodular value function

Remove fixed coordinates by substitution, and reject an empty interval.
Write

\[
 z_i=\alpha_i+d_i t_i,
 \quad
 (\alpha_i,d_i)=
 \begin{cases}
  (\ell_i,u_i-\ell_i),&\varepsilon_i=1,\\
  (u_i,-(u_i-\ell_i)),&\varepsilon_i=-1.
 \end{cases}                                                \tag{4}
\]

The continuous box becomes `[0,1]^r`; integer coordinates in `D` retain
their transformed finite domains, which contain both endpoints. The
transformed quadratic Hessian has
off-diagonal entries `d_i d_j A_ij<=0`. Its `C` principal block is PSD by
congruence. In each coordinate of `D`, keeping all other coordinates
fixed gives a concave univariate quadratic. Replace that coordinate by
the better endpoint. Repeating this operation for all of `D` never
increases the objective. Consequently some optimum has `t_D` binary.
The argument uses effective integer endpoints when applicable, so no
integer enumeration or interval-width factor is introduced.

For a subset `S` of `D`, let `a(S)` denote its zero-one indicator, and
define

\[
                  g(S)=\min_{t_C\in[0,1]^C}q(a(S),t_C).     \tag{5}
\]

Here and below `q` denotes the polynomial after (4). Each query in (5) is
a rational convex box QP. It has an exact rational minimizer and value
in polynomial bit time, including singular Hessians and nonunique
solutions. This is the classical exact convex-QP result of
[Kozlov--Tarasov--Khachiyan](../../literature/papers/kozlov1980-the-polynomial-solvability-of-convex/paper.md).

The transformed objective is submodular on the product lattice: for
vectors `x,y`,

\[
       q(x)+q(y)\ge q(x\wedge y)+q(x\vee y).                \tag{6}
\]

Unary quadratic and linear terms cancel in this comparison. For a pair
term with nonpositive coefficient, (6) follows by checking the two
possible relative coordinate orderings. Thus (6) follows by addition.
Choose minimizers in (5) for `S` and `T`. Their componentwise minimum and
maximum are feasible completions for `S intersect T` and `S union T`.
Using (6) gives

\[
              g(S)+g(T)\ge g(S\cap T)+g(S\cup T).           \tag{7}
\]

Hence `g` is a submodular set function with a polynomial-bit exact value
oracle. Classical rational submodular minimization returns a minimizing
set `S*`; one final query returns its continuous completion. Endpoint
reduction proves that this is a global optimizer of (1).

The source for oracle submodular minimization and the certificate identity
below is [Iwata--Fleischer--Fujishige, JACM 2001](https://www.opt.mist.i.u-tokyo.ac.jp/~iwata/papers/sfm.pdf),
especially Lemma 2.1 and equations (2.1)--(2.2). We use these established
results after constructing (5); we do not apply a discrete theorem
directly to an unrestricted continuous box.

## 3. A certificate that requires only polynomially many convex-QP queries

Put `m=|D|` and `h(S)=g(S)-g(empty)`. For a permutation `pi` of `D`,
let `S_j` be its first `j` elements and define its greedy vector by

\[
              b^\pi_{\pi(j)}=h(S_j)-h(S_{j-1}).             \tag{8}
\]

Submodularity implies `b^pi(T)<=h(T)` for every `T`, and
`b^pi(D)=h(D)`: reveal the elements of `T` in the permutation order and
apply decreasing marginal increments. Thus (8) belongs to the base
polytope

\[
 B(h)=\{w:w(T)\le h(T)\ (T\subseteq D),\ w(D)=h(D)\}.      \tag{9}
\]

Supply at most `m+1` permutations and rational nonnegative weights summing
to one, and set

\[
                    w=\sum_j\lambda_j b^{\pi_j}.           \tag{10}
\]

For any `S`,

\[
 g(S)\ge g(\varnothing)+w(S)
       \ge g(\varnothing)+\sum_{i\in D}\min(0,w_i).         \tag{11}
\]

Each chain value used in (8) comes with its rational continuous optimizer.
Its convex-QP certificate is particularly small: verify its box
feasibility and, in each nonfixed `C` coordinate, that the gradient is
zero in the interior, nonnegative at its lower bound, or nonpositive at
its upper bound. Convexity then proves global optimality of that query.
The gradient at a fixed coordinate needs no sign test. Exact rational
evaluation verifies the claimed value. An exact rational PSD test for
the supplied `A_CC` justifies convexity for every query at once.

Finally supply an endpoint label `S*` and its certified completion such
that

\[
          g(S^*)=g(\varnothing)+\sum_i\min(0,w_i).           \tag{12}
\]

Equations (11)--(12) prove global optimality. A checker evaluates at most
`O(m^2)` chain queries; it need not trust an SFM implementation or check
exponentially many inequalities in (9). When `m=0`, only the original
convex-QP certificate is needed.

## 4. Why an exact polynomial certificate can be constructed

Existence follows from the classical base-polytope min--max identity

\[
           \min_S h(S)=\max_{w\in B(h)}\sum_i\min(0,w_i).   \tag{13}
\]

For a constructive bit bound, let `B` have all greedy vectors as columns.
Consider the rational linear program

\[
 \min\sum_i r_i\quad\text{subject to}\quad
 B\lambda+r\ge0,\quad {\bf1}^{\mathsf T}\lambda=1,
                   \quad \lambda\ge0,\quad r\ge0.         \tag{14}
\]

Its dual, with only `m+1` variables, is

\[
 \max\beta\quad\text{subject to}\quad
 0\le y_i\le1,\qquad
              \beta+(b^\pi)^{\mathsf T}y\le0
                                  \quad\text{for all }\pi.\tag{15}
\]

To separate (15), sort `y` in decreasing order and compute its greedy
vector. This maximizes `(b^pi)^T y`; if its constraint holds, all the
permutation constraints hold. The oracle makes `m+1` exact convex-QP
queries. Its outputs have uniformly polynomial encoding length: every
query uses the same rational Hessian and box and a polynomial-length
endpoint label. Exact convex-QP solution bounds therefore give a
polynomial bound on every possible `g(S)` and greedy-vector entry.
There is no need to form a common denominator over all subsets.

Exact rational oracle linear programming, including dual recovery, now
solves (15) and recovers a solution to (14) using polynomially many
returned constraints. A precise source is Grötschel--Lovász--Schrijver,
[Geometric Algorithms and Combinatorial Optimization](../../literature/papers/grotschel1988-geometric-algorithms-and-combinatorial-optimization/paper.md),
Theorem 6.4.9 and Lemma 6.5.15; the latter returns an optimal basic dual
solution using oracle inequalities. These are the exact rational
polyhedral results, rather than a weak convex-optimization guarantee.

A basic solution of (14) has at most `m+1` positive permutation weights.
Its coefficients have polynomial rational height by the determinant
bound for the selected polynomial-size linear system. At optimum
`r_i=max(0,-w_i)`, so (13) proves equality (12). This constructs the
certificate, rather than merely asserting that a minimizer-producing
SFM routine must expose one.

The same LP also supplies a minimizing label without a separate SFM
call. For an optimal `y` in (15), the greedy maximum equals `-beta`.
Sort its coordinates as `y_pi(1)>=...>=y_pi(m)` and set
`y_pi(m+1)=0`. Then

\[
 \max_\pi(b^\pi)^{\mathsf T}y
  =\sum_{j=1}^m(y_{\pi(j)}-y_{\pi(j+1)})h(S_j)
                        +(1-y_{\pi(1)})h(\varnothing).     \tag{15a}
\]

This is a convex combination of prefix values, and its value is `min h`
by (13)--(15). At least one prefix with positive weight is therefore
optimal. Querying the prefixes, including the empty set, recovers a
minimizing label and its convex completion. This proves the stated
optimizer, time, and certificate bounds.
This oracle-LP construction is a complexity proof; the diagnostic below
does not implement general SFM or an ellipsoid algorithm.

## 5. Stability and use in the decomposition program

Fixing a rational core vector in a larger quadratic objective changes
only the residual linear and constant terms. Every residual box
restriction preserves (2), the signs of the diagonal entries in (3),
and positive semidefiniteness of the remaining `C` principal block.
Fixed variables can be substituted out. These facts establish the entire
box-stable interface, including the excluded-coordinate slabs used to
localize conditional optimizers.

For an all-continuous unit-box QP with a supplied core of size `k` and
core upper coordinate curvature `L`, the existing exact finite-noise
recourse theorem therefore applies when its residual satisfies (2)--(3).
Under that theorem's single base-selected rational noise law of half-width
`sigma`, it returns an exact rational global optimizer on every draw,
with expected work and proof size bounded by

\[
      8^k\left[3+\frac{(1+k/2)L}{2\sigma}\right]^k
                             \operatorname{poly}(I).       \tag{16}
\]

This is a corollary of the existing search and closure theorem. The new
scope is the explicit conditional oracle and its checkable certificates.
It removes outside grid error in precisely the stated class; it gives no
general treewidth-only algorithm.

The exact conditional oracle itself permits integer coordinates in `D`.
Equation (16) is stated here for the all-continuous theorem. No automatic
mixed-integer smoothed-runtime corollary is inferred from an oracle
working on a mixed domain.

The class includes the minimum-cut case `C=empty`, and convex submodular
QP when `D=empty`. It also includes coupled instances outside both.
For example, take arbitrarily many `D` coordinates with block
`A_DD=-I-11^T`, arbitrarily many `C` coordinates with
`A_CC=(|C|+1)I-11^T`, and any entrywise nonpositive cross block. The
`C` block is positive definite; the `D` block is negative definite.
With all cross entries negative the graph is complete, and the full
Hessian is indefinite. Restricting to the `D` subspace proves that its
number of negative eigenvalues is at least `|D|`. Neither bounded
treewidth, bounded forest-deletion size, nor bounded negative inertia
explains this residual oracle.

## 6. Limits and prior-art boundary

The endpoint argument is classical coordinate-concavity rounding; the
convex QP and SFM algorithms and the dual certificate identity are also
established. This note provides their explicit composition for certified
conditional recourse. It makes no novelty claim for the underlying
tractable optimization class. Earlier mixed binary/continuous
submodularity work is relevant to any publication-level priority audit.

In particular, Bunton and Tabuada's Theorem 4 applies the classical
partial-minimization principle to continuous/discrete model selection;
Corollary 6 and the following convex-oracle discussion combine it with
submodular minimization. Their support-based feasible sets differ from
the fixed endpoint labels here, but the value-function and SFM
composition is a direct precedent.
[JMLR 23 (2022), pp.9--12](https://jmlr.org/papers/volume23/21-0166/21-0166.pdf)

Gómez and Han's Lemma 1 and Theorems 1--2 likewise use partial minimization
and convex recourse for indicator-linked boxes; Section 5 treats extreme
base computation. These are precedents for the method and certificate
ingredients, not just adjacent applications. The present supplement
records their rational-bit, box-restriction, and QP-witness requirements
for this project's conditional interface; it does not claim invention of
the composition or greedy-base certificate representation.
[Current paper, arXiv:2209.13161v2](https://arxiv.org/pdf/2209.13161)

The proof requires a product box. Additional coupled constraints need a
separate argument that both endpoint rounding and the lattice
minimum/maximum operations remain feasible. Integer coordinates in `C`
are not covered. Replacing the PSD check by nonnegative diagonals does
not make its QP value oracle convex. An approximate continuous solve is
not an exact `g(S)` query; small uncontrolled errors can destroy the
submodularity and equality certificates. The polynomial degree and oracle
constants can be large, so this theorem by itself establishes no practical
advantage over a direct MINLP solver.

## 7. Targeted verification

The accompanying [exact diagnostic](check_mixed_submodular.py) checks the
endpoint/convex composition, submodularity, and a certificate requiring a
nontrivial convex combination. Its output is in
[mixed-submodular-results.json](mixed-submodular-results.json). It uses
small endpoint and active-face enumeration as independent diagnostic
methods; it is not a general SFM implementation.

The fixed certificate fixture has two concave coordinates `a,b` and one
convex coordinate `z`, all in `[0,1]`, with objective

\[
 -a^2-b^2+2a+2b-\tfrac32ab+z^2
               -\tfrac12(1+a+b)z+\tfrac1{16}.              \tag{17}
\]

Its exact conditional optimizer is `z=(1+a+b)/4` at endpoint labels.
The four values are `0,13/16,13/16,0`. Its two greedy vectors are
`(13/16,-13/16)` and `(-13/16,13/16)`; equal weights give `w=0` and
certify optimum zero. Either vector alone gives the strictly weaker
lower bound `-13/16`. This checks the need for mixtures and retains
multiple optimal labels.

The command actually run was
`python3 -B research-20261002-decomposition/conditional-messages/check_mixed_submodular.py`.
It passed 60 rational-box QP comparisons with independent full active-face
enumeration, 560 conditional queries, 6,720 exact submodular inequalities,
six singular convex-block cases, and 60 mixed-integer endpoint comparisons
against all integer labels in the small test boxes. The mixture fixture
and three adverse certificate/interface guards also passed.

An independent reader reviewed the actual theorem file, verified the
primary-source LP and base-polytope statements, and found no substantive
gap. The review's correction distinguishing transformed integer domains
from continuous unit intervals is incorporated. The author ran the
diagnostic; the reviewer separately checked the fixture symbolically.
These first-release checks did not implement a general SFM algorithm.
The subsequent [implementation completion](../completion/submodular-recourse.md)
adds an exact Lovasz-extension cutting-plane solver for this mixed class,
automatic construction of greedy-base mixtures, and independent replay.
Its cut count can be factorial and its convex-QP fallback exponential;
it does not implement the polynomial oracle algorithm proved above.
No project-wide checks or CI inspection were performed in either phase.
