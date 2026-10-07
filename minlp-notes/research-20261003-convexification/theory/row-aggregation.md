# Joint support cuts in the original variables

This note gives the mathematical contract for the continuation's native
integration. It combines original nonlinear rows and adds valid linear
inequalities without replacing their nonlinear expressions by graph
auxiliaries. The argument is weak Lagrangian duality and convex separation;
these principles are established. The contribution here is the precise
contract, its implementation, and its checked scope, not a new duality
theorem. See the [primary-source audit](../literature/aggregation-prior.md).

## 1. A direct cut from an aggregated support bound

Let a feasible model point satisfy

\[
 x\in D,\qquad g_i(x)+\ell_i(v)\le b_i\quad(i=1,\ldots,m).
\]

Here \(x\) is the selected block of original variables, \(v\) collects
the model variables, and each \(\ell_i\) is linear. The vectors need not
be disjoint: a variable in \(x\) may also occur in an affine remainder.
All constants have been moved to \(b_i\). The set \(D\) must contain the
block coordinates of every feasible point to which the cut will apply.
It may be a box intersected with valid affine constraints. The actual
source expressions and their domains, not an accidentally simplified
replacement, define the functions \(g_i\).

Choose \(\lambda_i\ge0\) and a vector \(a\), and certify

\[
 a^\mathsf T x+\sum_i\lambda_i g_i(x)\ge\beta
 \qquad\text{for every }x\in D. \tag{1}
\]

Then the original-variable linear inequality

\[
 a^\mathsf T x-\sum_i\lambda_i\ell_i(v)
 \ge\beta-\sum_i\lambda_i b_i \tag{2}
\]

is valid. Indeed, multiplying each source row by its nonnegative
multiplier gives
\(\sum_i\lambda_i g_i(x)\le\sum_i\lambda_i(b_i-\ell_i(v))\).
Substitute this upper bound into (1). No convexity, differentiability,
strong duality, or optimal choice of multipliers is needed. Any certified
lower bound \(\beta\) is sufficient. Exact minimization only strengthens
the constant.

The variables shared by different \(g_i\) are minimized jointly in (1).
Their common domain and retained affine coupling are precisely where
this operation can improve on separate scalar lower bounds. Combining
already linear valid inequalities is different: that operation cannot
strengthen their exact intersection. Here the nonlinear aggregate is
bounded before the nonlinear functions are eliminated.

For globally valid cuts, all bounds and coupling rows used in \(D\) must
be globally valid. Bounds or rows valid only at a branch-and-bound node
produce cuts valid only in that node's subtree. A support certificate
does not establish the provenance of those bounds by itself.

## 2. Equalities and nonlinear objectives

For equality rows
\(h_k(x)+e_k(v)=d_k\), arbitrary real multipliers \(\nu_k\) are valid.
The support expression becomes

\[
 a^\mathsf T x+\lambda^\mathsf T g(x)+\nu^\mathsf T h(x),
\]

and the cut is

\[
 a^\mathsf T x-\lambda^\mathsf T\ell(v)-\nu^\mathsf T e(v)
 \ge\beta-\lambda^\mathsf T b-\nu^\mathsf T d. \tag{3}
\]

Equivalently, represent an equality by its two opposite inequality
sides and use nonnegative multipliers on both. Their difference is the
free equality multiplier. An arbitrary negative multiplier on a single
inequality side is invalid.

For minimization of \(g_0(x)+\ell_0(v)+c_0\), an epigraph variable \(t\)
gives the source row

\[
 g_0(x)+\ell_0(v)-t\le-c_0.
\]

A nonnegative multiplier on this row produces a lower-bound cut involving
\(t\). For maximization, use the hypograph row
\(-g_0(x)-\ell_0(v)+t\le c_0\). The same theorem applies after that
sign change. The objective transformation, including its constant and
sense, must be the same in the native baseline and cut-enabled model.
This is the solver's objective epigraph interface; it does not require
introducing a separate graph variable for every selected function.

An unbounded epigraph variable is allowed in the exact theorem. It
matters when rounded coefficients are exported: its coefficient must
remain exact unless a valid bound in the necessary direction is known.

## 3. Completeness relative to the joint graph relaxation

The direct-row interface can express the entire projection of the joint
graph relaxation, although a bounded implementation need not generate
all these rows.

**Theorem.** Suppose \(D\subset\mathbb R^d\) is nonempty and compact,
and \(g:D\to\mathbb R^m\) is continuous. Let

\[
 K=\operatorname{conv}\{(x,g(x)):x\in D\},\qquad
 P=\{(x,z):\exists y,\ (x,y)\in K,\ y+Lz\le b\}.
\]

Then \(P\) is exactly the intersection, over every
\(a\in\mathbb R^d\) and \(\lambda\in\mathbb R_+^m\), of

\[
 a^\mathsf T x-\lambda^\mathsf T Lz
 \ge\min_{u\in D}\{a^\mathsf T u+\lambda^\mathsf T g(u)\}
       -\lambda^\mathsf T b. \tag{4}
\]

**Proof.** The set \(K\) is compact and convex. Therefore
\(U=K+(\{0\}\times\mathbb R_+^m)\) is closed and convex: from any
convergent sequence of sums, first extract a convergent subsequence of
the compact summands, after which the cone summands also converge.
Membership in \(P\) is equivalent to \((x,b-Lz)\in U\).

Every lower support inequality of \(U\) with finite constant has a
nonnegative coefficient \(\lambda_i\) on its \(i\)-th last coordinate;
a negative coefficient would make its infimum \(-\infty\) along the
corresponding cone ray. For such a coefficient vector the lower support
value is

\[
 \inf_{(u,y)\in U}(a^\mathsf T u+\lambda^\mathsf T y)
 =\min_{u\in D}(a^\mathsf T u+\lambda^\mathsf T g(u)).
\]

Substituting \((x,b-Lz)\) yields (4). Conversely, any point outside the
closed convex set \(U\) is strictly separated by a finite lower support
inequality, whose last coefficients must have the required signs. Its
corresponding row (4) excludes the proposed \((x,z)\). Thus all rows
describe exactly \(P\). \(\square\)

For equality components, assume also that \(h\) is continuous on \(D\).
Use the graph \((x,g(x),h(x))\), add a nonnegative
cone only to the inequality components, and substitute
\((x,b-Lz,d-Ez)\). Their support coefficients are unrestricted. The
same proof gives (3). Additional original linear rows may be intersected
with \(P\) afterwards. The proof does not require the graph hull to have
nonempty interior.

If the affine remainder also uses block variables, introduce a duplicate
of those coordinates for the statement and intersect with the linear
equations identifying the copies. Equivalently, substitute the same
original coordinates directly into every row (4).

This is a formulation statement. It does not say that the restricted
normal family automatically has an efficient separator. With multiple
selected blocks it applies separately to each declared block; it does
not silently replace their intersected hulls by a larger joint hull.

### Why this does not complete the feasible-set hull

Take \(D=[0,1]\) and the equality \(x^2=1/4\). The actual feasible set
is \(\{1/2\}\). Yet the distribution with mass \(3/4\) at zero and
mass \(1/4\) at one has
\(\mathbb E[x]=\mathbb E[x^2]=1/4\). Therefore
\((1/4,1/4)\in\operatorname{conv}\{(x,x^2):x\in[0,1]\}\), and the
projected graph relaxation contains \(x=1/4\).

More directly, for every \(a,\nu\),

\[
 \min_{u\in[0,1]}(au+\nu u^2)
 \le (a+\nu)/4,
\]

so \(x=1/4\) satisfies every row
\(ax\ge\min(au+\nu u^2)-\nu/4\). Exhaustive exact support cuts do
not remove it. Convexifying the graph and then imposing an equality in
expectation need not equal convexifying the points satisfying that
equality. Including the nonlinear constraint inside the support domain
can repair this example, but changes the oracle problem and can exceed
the supported tractable class. Ordinary bound propagation can also
resolve this particular example; that does not change the formulation
distinction.

## 4. Correcting the final floating-point row

After exact elimination, combine every occurrence of each original
variable and write the rational row as

\[
 c^\mathsf T v\ge r.
\]

Let \(\widehat c\) be the exact rational values of the binary64
coefficients that will actually be inserted into the solver, and let
\(\Delta_j=\widehat c_j-c_j\). If
\(L_j\le v_j\le U_j\) are valid bounds, define

\[
 E=\sum_j\inf_{s\in[L_j,U_j]}\Delta_j s
   =\sum_j\min\{\Delta_jL_j,\Delta_jU_j\}, \tag{5}
\]

where a zero delta contributes zero even if a bound is infinite. A
positive delta requires a finite lower bound; a negative delta requires
a finite upper bound. A finite bound on the opposite side is unnecessary.
If a needed bound is unavailable, reject that coefficient conversion
or choose a different exactly representable row; do not silently omit
its error.

The exported row

\[
 \widehat c^\mathsf T v\ge\widehat r,
 \qquad \widehat r\le r+E \tag{6}
\]

is valid because
\(\widehat c^\mathsf T v=c^\mathsf T v+\Delta^\mathsf T v\ge r+E\).
Choose \(\widehat r\) by rounding downward, and compare its exact
binary rational value with the exact bound. Overflow, nonfinite
coefficients, or an unavailable finite right-hand side cause refusal.
An analogous upper row follows by multiplying everything by \(-1\).

The current `solver/row_certificate.py` exporter makes a more conservative
admission choice: for a nonzero coefficient error it requires both bounds
to be finite. The sufficient one-sided condition above is a mathematical
allowance, not a claim that this exporter accepts every such case.
Unchanged coefficients can still occur on unbounded variables.

This correction is an established safe-rounding construction; the
[literature audit](../literature/aggregation-prior.md) identifies the
direct Eifler–Gleixner precedent. It applies after all coefficient
merging, normalization, zero dropping, and other transformations that
change the row. A fixed numerical safety shift cannot replace (5).

The support certificate must bind the multipliers and coefficient vector
actually used in the exact elimination. The integration may first round
a proposed direction to binary64 and then certify that direction, or
retain a rational direction and compensate its final row conversion as
above. Certifying one direction and exporting another without an error
bound is invalid. The certificate should record source-row identities,
side orientation, multipliers, the support bound, exact combined row,
variable bounds, exported coefficients, and corrected right-hand side.

Replay establishes the validity of this concrete row for the bound model
and domain. It does not certify undocumented later solver substitutions,
the solver's complete search, or its final numerical optimality gap.

## 5. What completion means here

The mathematical cut contract is complete for the stated data, and (4)
characterizes its unlimited exact-row closure. Exact quadratic support
over the supported polytopes and constrained stars closes the support
subproblem for those classes. The separate finite-net separation result
closes a specified positive-tolerance graph-separation problem when its
complete mode finishes.

These statements do not imply that a fixed cut budget produces the full
closure, that rounding preserves every tiny separation margin, or that
the cuts improve solve time. They also do not solve support optimization
for unrestricted nonlinear domains or remove the distinction between
the joint graph relaxation and the original feasible-set hull. Those
boundaries are mathematical properties, not missing checks that can be
eliminated by declaring the research topic finished.
