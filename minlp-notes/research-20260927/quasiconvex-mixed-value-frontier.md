# Exact mixed-integer values from convex objective sublevels

Date: 2026-09-28. Status: complete proof; the
[initial review](quasiconvex-mixed-value-review.md),
[fresh transition audit](quasiconvex-transition-independent-audit.md), and
[fresh full fractional audit](fractional-misocp-optimization-adversarial.md)
found no gap, conditional on the stated theorem inputs. The first
reviewer contributed the auxiliary-value construction in Section 6.2;
the later full fractional reviewer had no role in that construction.
This extends the
[convex epigraph value theorem](unbounded-misocp-multiple-integer-frontier.md)
to semialgebraic objective sublevels that are convex even when the full
epigraph is not convex. Novelty is not established.

The finite-value theorem below requires convex strict sublevels. A small
optimal integer vector additionally requires convexity of the weak slice
at the optimum. The distinction matters for projected epigraphs whose
vertical fibers can be open: an exact Pell construction shows that the
additional hypothesis cannot simply be dropped.

## 1. Statement and scope

Let \(E\subseteq\mathbb R^k\times\mathbb R\) be upward closed in
its last coordinate. It has a quantifier-free Boolean description with
arbitrarily many integer polynomial atoms of degree at most \(d\ge2\)
and individual coefficient bit length at most \(H\ge1\). Define

\[
 C_t=\{z:\exists s<t\ ((z,s)\in E)\},\qquad
 E_t=\{z:(z,t)\in E\}.
 \tag{1}
\]

Assume every \(C_t\) is convex. The mixed-integer domain is nonempty,
and its objective infimum is

\[
                   \theta=\inf\{t:(z,t)\in E,\ z\in\mathbb Z^k\}.
 \tag{2}
\]

**Finite-value theorem.** There is an effective function \(G(k)\)
such that every finite \(\theta\) has an integer minimal polynomial
of degree at most \(d^{G(k)}\) and coefficient bit length at most

\[
                             (H+1)d^{G(k)}.
 \tag{3}
\]

These bounds do not depend on the number of atoms. They allow an
unattained value and nonclosed sets \(C_t\) and \(E\).

**Attained-integer corollary.** If \(E_\theta\) is also convex and
contains an integer point, then some optimal integer vector has bit
length at most \((H+1)d^{G(k)}\), after increasing \(G\).
In particular, the conclusion holds when every weak slice \(E_t\)
is convex. It also holds if each vertical fiber
\(\{t:(z,t)\in E\}\) is closed: upward closure then gives

\[
                     E_t=\bigcap_{\epsilon>0} C_{t+\epsilon},
 \tag{4}
\]

so convexity of the strict slices implies convexity of the weak slices.
An ordinary epigraph of a quasiconvex extended-real function has this
property. A projected epigraph of a continuous optimization problem can
have open vertical fibers, so closedness in that setting must not be
assumed.

These are structural bounds. An efficient optimization algorithm also
needs an efficient exact threshold-feasibility algorithm for its class
of representations. Section 6 explains that consequence and one conic
application.

## 2. The algebraic inputs

We use the same quantitative real-algebraic inputs as the convex
epigraph note: Khachiyan--Porkolab (2000), Proposition 2.1,
Proposition 2.2, and Corollary 2.3, based on real quantifier elimination
and algebraic sampling. For formulas using a number of variables
depending only on \(k\), atom degree \(d^{O_k(1)}\), and coefficient
bits \((H+1)d^{O_k(1)}\), they give:

* finite one-dimensional endpoints of degree \(d^{O_k(1)}\) and
  coefficient bits \((H+1)d^{O_k(1)}\);
* common-field algebraic samples with those degree and bit bounds.

These degree and individual coefficient bounds are independent of the
number of atoms. The algorithms that construct all intermediate
formulas can depend heavily on it; we do not claim otherwise.

We also use the reviewed rational-part lemma from Section 2.1 of the
convex epigraph note. If a real linear space in \(\mathbb R^k\) has
such a formula and contains a nonzero rational vector, it contains a
nonzero integer vector with \((H+1)d^{O_k(1)}\) bits. A joint sample
of a basis lies in one controlled number field. Field linear algebra,
expansion of annihilating equations in a power basis, and rational
linear algebra then compute its rational part at the stated size.

Integer affine slices use Hermite or Smith normal form. If one equation
\(a^Tz=b\), \(a\ne0\), has integer data of \(L\) bits and an
integer solution, all its integer solutions have a parametrization
\(z=z_0+Ty\), \(y\in\mathbb Z^{k-1}\), whose data have
\(O_k(L+1)\) bits. Substituting it into the carried original
polynomials preserves degree and increases coefficient bit lengths
linearly in \(L\), with a factor depending on \(k,d\).

## 3. Only finitely many geometric changes matter

For each \(t\), define the real linear space

\[
 \mathcal B_t=\{a\in\mathbb R^k:
                 \sup_{z\in C_t}|a^Tz|<\infty\}.
 \tag{5}
\]

When \(C_t\) is empty this space is \(\mathbb R^k\). The sets
\(C_t\) are nested in \(t\), hence

\[
 s<t\quad\Longrightarrow\quad
 \mathcal B_s\supseteq\mathcal B_t,\qquad
 \operatorname{aff}C_s\subseteq\operatorname{aff}C_t
 \quad\hbox{when }C_s\ne\varnothing.
 \tag{6}
\]

Set \(\dim\operatorname{aff}\varnothing=-1\). The dimension of
\(\mathcal B_t\) decreases at most \(k\) times, and the affine
dimension of \(C_t\) increases at most \(k+1\) times. Equal
dimensions of nested nonempty affine spaces, or nested linear spaces,
force equality of those spaces.

**Transition lemma.** There is a set \(K\subset\mathbb R\) of at
most \(2k+1\) real numbers such that both spaces in (6), and the
emptiness status of \(C_t\), are constant on every open component of
\(\mathbb R\setminus K\). Every member of \(K\) has degree
\(d^{O_k(1)}\) and coefficient bit length
\((H+1)d^{O_k(1)}\).

**Proof.** For \(j=1,\ldots,k\), the predicate
\(\dim\mathcal B_t\ge j\) can be expressed by
\(j\) vectors \(a_1,\ldots,a_j\), a common bound \(R>0\), a
positive Gram determinant, and

\[
 \forall z,s:\quad
  \bigl((z,s)\in E\ \wedge\ s<t\bigr)
  \Longrightarrow
  \bigwedge_{i=1}^j(-R\le a_i^Tz\le R).
 \tag{7}
\]

The common \(R\) is valid because there are finitely many vectors.
This formula uses \(O(k^2)\) variables and atom degree
\(\max\{d,O(k)\}\). Its set of true \(t\)'s is downward closed.
It therefore has at most one finite boundary point.

For \(j=0,\ldots,k\), the predicate
\(\dim\operatorname{aff}C_t\ge j\) asks for \(j+1\) points
\((z_i,s_i)\in E\) with \(s_i<t\) and, when \(j\ge1\), a
positive Gram determinant of the differences \(z_i-z_0\).
It has a formula with the same type of bounds. Its truth set is upward
closed and again has at most one finite boundary point. The case
\(j=0\) records nonemptiness.

Let \(K\) collect these finite boundary points. Quantifier elimination
and the endpoint bound in Section 2 give the stated algebraic bounds.
On any component away from \(K\), the dimensions are constant.
The nesting relations then give equality of the spaces. \(\square\)

There is no joint convexity assertion about \(E\) in this lemma.
The dimension argument uses only nested sets; convexity enters later
through lattice-free geometry and the integer witness theorem.

## 4. A small cap without knowing the optimum

Suppose \(\theta\) is finite and does not belong to \(K\). Let
\(J=(\alpha,\beta)\) be the open component containing \(\theta\),
allowing infinite endpoints. The sublevels on \(J\) are all nonempty:
those above \(\theta\) contain integer points, and their emptiness
status is constant on \(J\).

**Cap lemma.** There exists a rational number
\(U\in(\theta,\beta)\) with at most
\((H+1)d^{O_k(1)}\) bits, such that
\(C_U\cap\mathbb Z^k\ne\varnothing\).

**Proof when \(\beta<\infty\).** Since \(\theta<\beta\), the
convex set

\[
                 C_\beta=\{z:\exists s<\beta\ ((z,s)\in E)\}
 \tag{8}
\]

contains an integer point. The transition lemma gives a small minimal
polynomial and isolating interval for \(\beta\). Representing that
fixed algebraic number by one additional real variable gives a
controlled formula for (8). Khachiyan--Porkolab's quantified integer
witness theorem supplies an integer \(z_0\in C_\beta\) with
\((H+1)d^{O_k(1)}\) bits.

Substitute this integer vector and algebraically sample a pair
\((s_0,\beta)\) with \((z_0,s_0)\in E\) and \(s_0<\beta\).
The sample has controlled degree and height. Necessarily
\(\theta\le s_0\). Root separation for these two distinct real
algebraic numbers gives a rational \(U\) between them with the
stated bit length. Then
\(\alpha<\theta\le s_0<U<\beta\) and \(z_0\in C_U\).

**Proof when \(\beta=+\infty\).** The total projection
\(\{z:\exists s\ ((z,s)\in E)\}=\bigcup_t C_t\) is convex,
being a nested union of convex sets, and contains an integer point.
Apply the integer witness theorem to it and sample one feasible
objective coordinate \(s_0\) in the resulting integer fiber. Both
have controlled encoding. A sufficiently large integer \(U>s_0\)
has controlled bit length. Since \(s_0\ge\theta>\alpha\), it
belongs to the required interval. \(\square\)

This argument is the part that a direct appeal to convex sublevels at
the unknown \(\theta\) would miss. The cap is selected from a
small algebraic transition level, rather than using the unknown value
as a coefficient.

## 5. Induction on the integer dimension

We now prove the finite-value theorem. If \(\theta\in K\), the
transition lemma already gives the required bound. Otherwise use the
cap \(U\) from Section 4. On the interval \(J\), the affine hull
and bounded-form space are constant.

### 5.1 A smaller affine hull

If \(C_U\) is not full-dimensional, algebraically sample a nonzero
affine equation \(a^Tz=b\) valid throughout \(C_U\). Its formula
uses a universal quantifier over \(z,s\) and the premise
\((z,s)\in E,\ s<U\), just as in (7). Expand its coefficients in
one number-field basis. For integer \(z\), each resulting rational
equation must hold. Choose one with a nonzero normal and clear
denominators. Its bit length is \((H+1)d^{O_k(1)}\).

This rational integer equation retains every integer point of objective
less than \(U\), so restricting to its integer solutions preserves
the infimum \(\theta\). Parametrize those solutions by an affine
integer map with one fewer integer variable. The equation has an
integer solution because \(C_U\) contains one. Its parametrization
has the size stated in Section 2.

### 5.2 A bounded rational form

Suppose \(C_U\) is full-dimensional. There must be a nonzero
rational vector in \(\mathcal B_U\). Otherwise choose
\(t\in(\alpha,\theta)\). The set \(C_t\) is nonempty and
full-dimensional, by the transition lemma, and has no integer point.
Its closure is lattice-free because
\(\operatorname{int}\overline{C_t}=\operatorname{int}C_t\subseteq C_t\).
The classical maximal lattice-free theorem places this closure inside
a set \(P+L\), where \(P\) is a polytope and \(L\) is a proper
rational linear space. A nonzero rational vector in \(L^\perp\)
is bounded on \(C_t\), hence belongs to
\(\mathcal B_t=\mathcal B_U\), a contradiction.

The rational-part lemma gives a nonzero integer
\(a\in\mathcal B_U\) with \((H+1)d^{O_k(1)}\) bits. Its finite
infimum and supremum on \(C_U\) are endpoints of the set

\[
 \{v:\exists z,s\ ((z,s)\in E,\ s<U,\ v=a^Tz)\}.
 \tag{9}
\]

They have controlled degree and height, so a root bound gives
\(|a^Tz|<B\) throughout \(C_U\), where
\(\log B\le(H+1)d^{O_k(1)}\).

A sequence of mixed-integer points approaching \(\theta\) is
eventually below \(U\). Among its finitely many integer values
of \(a^Tz\), one value \(b\) occurs along a subsequence still
approaching \(\theta\). Thus the slice \(a^Tz=b\) preserves the
infimum. Its coefficients and right-hand side have controlled bit
length. Parametrize its integer solutions and reduce dimension.

### 5.3 Termination and coefficient accounting

Both restrictions preserve upward closure and convexity of strict
sublevels: a new strict sublevel is the affine inverse image of the
old sublevel intersected with the chosen affine space. Its input is
obtained by substituting into the original atoms, so their degree
remains at most \(d\). If their coefficient bits at one stage are
\(H'\), the next stage has bits at most
\((H'+1)d^{O_k(1)}\). The dependence on \(H'\) is linear,
by the sampling, determinant, lattice, and substitution bounds in
Section 2.

If the value is not a transition level, one of the two restrictions
strictly reduces integer dimension. There are at most \(k\) such
steps. In dimension zero, \(\theta\) is necessarily the transition
between empty and nonempty strict sublevels. The transition lemma
therefore finishes the induction. Composing the height bounds proves
(3) for some effective \(G(k)\).

For the attained-integer corollary, describe the fixed value
\(\theta\) by its minimal polynomial and an isolating interval,
and use one real variable to define \(E_\theta\). When that set
is convex, the quantified integer witness theorem gives the stated
small optimal integer vector. Convexity of this weak slice is a
separate hypothesis; the induction did not establish it.

## 6. Consequences for exact optimization

Suppose a representation class has exact rational threshold feasibility
for \(E_t\cap\mathbb Z^k\), and its implicit formulas have the
degree and height bounds above. The finite-value theorem gives an
effective root bound \(|\theta|<M\) whenever the value is finite.
After feasibility has been established, the single threshold
\(-M-1\) decides unboundedness below. In the finite case, rational
bisection and algebraic recognition recover \(\theta\), including
an unattained value. The running time includes the cost of the
threshold oracle. No efficient oracle follows merely from a convexity
promise on the strict sublevels.

### 6.1 Affine-fractional objectives over rational MISOCP

Consider a rational SOC feasible set \(F\) in variables
\((z,x)\), with \(z\in\mathbb Z^k\), and objective

\[
                  \frac{p(z,x)}{q(z,x)},
 \tag{10}
\]

where \(p,q\) are rational affine and \(q>0\) on all of \(F\).
This positivity is a hypothesis; for example a rational affine row
\(q\ge1\) guarantees it. For every real \(t\), the weak
threshold set in the full variables is

\[
                   F\cap\{p-tq\le0\},
 \tag{11}
\]

which is convex. Its projection onto \(z\) is also convex. The
projected epigraph is generally not jointly convex in \((z,t)\),
so the preceding convex-epigraph theorem does not apply directly.

For rational \(t\), (11) is a rational SOC system with one extra
affine row. It preserves the number \(k\) of integer variables and
the span \(h\) of the squared continuous Hessians. The compressed
projection construction also applies with \((z,t)\) treated as
free parameters: in \(p-tq\), the coefficients of \(x\) are
affine in \(t\), and the constant term has degree at most two in
\((z,t)\). These are exactly the parameter degrees already allowed
in the rank-chart construction.

Consequently, combining this note with the reviewed unbounded MISOCP
threshold algorithm gives polynomial-time exact feasibility,
unboundedness classification, and algebraic finite-value recovery for
(10), for fixed \(k,h\). If the infimum is attained, the
attained-integer corollary bounds some optimal integer assignment.
The next subsection supplies the additional continuous witness bound
and completes attainment and optimizer recovery.

### 6.2 Attainment and exact fractional optimizers

At a fixed rational integer assignment \(z\), add a continuous value
variable \(v\) and the rational quadratic row

\[
                         p(z,x)-v q(z,x)\le0.
 \tag{10a}
\]

Minimize the rational affine objective \(v\) on this system together
with the original squared SOC rows and their affine sign conditions.
Since \(q>0\) on the original feasible set, its infimum and
attainment are exactly those of the ratio. The original continuous
Hessians acquire a zero row and column for \(v\). The single new
bilinear row contributes at most one further Hessian direction.
Thus the rational weak quadratic system has continuous Hessian span
at most \(h+1\). It need not be convex; the reviewed
[nonconvex attained-optimizer theorem](nonconvex-attainment-and-optimizer.md)
applies nonetheless.

If the ratio minimum \(\theta\) is attained in this fiber, every
optimizer of the lifted problem has the form \((x,\theta)\), with

\[
                 x\in F_z\cap\{p(z,x)-\theta q(z,x)=0\}.
 \tag{10b}
\]

This is a closed convex set in \(x\): the equality is affine once
\(z,\theta\) are fixed. Minimizing \(\|(x,\theta)\|^2\) on
the lifted optimal set therefore selects its unique minimum-norm
\(x\). The nonconvex theorem supplies a joint-field degree and
coordinate-height bound for this entire tuple. For fixed \(k,h\)
and a polynomial-bit integer assignment, both are polynomial in the
original input length. This proves a uniform optimizer box without
introducing an algebraic coefficient into that quadratic theorem.

The attained-integer corollary supplies a universal box for some
optimal \(z\), if one exists. The preceding fiber argument then
supplies a uniform continuous box containing the global canonical
optimizer for every attaining assignment in that integer box.
Thus later integer interval bisections cannot select an attaining
fiber whose canonical point is excluded by the box. Intersect the
original SOC set with
both boxes and let \(\beta\) be its fractional infimum. This boxed
mixed-integer domain is compact. The denominator is continuous and
strictly positive there, so the ratio is continuous; a nonempty boxed
domain has an attained minimum. Therefore the original value is
attained exactly when the boxed domain is nonempty and
\(\beta=\theta\). The exact value algorithm of Section 6.1
computes \(\beta\), so this is an algorithmic decision.

When equality holds, bisect the integer coordinate intervals. Compute
the exact boxed ratio minimum in each tested half and retain a half
with value \(\theta\). Compactness ensures that the retained half
contains an optimizer. Polynomially many queries fix an optimal integer
assignment.

For the resulting continuous fiber, the canonical point in (10b) can
be recovered by the same norm and coordinate approximation argument
used in [continuous SOCP optimization](continuous-socp-optimization.md).
The required oracle is available: for any additional rational box or
rational squared-norm threshold, minimize the ratio on that compact
rational SOC subdomain. It meets (10b) exactly when its minimum equals
\(\theta\); an empty subdomain returns false. A squared-norm
threshold is representable by a rational
SOC and adds at most one continuous Hessian direction. The oracle
therefore stays in the fixed-\((k,h)\) class.

The joint-field bound from the lifted minimum-norm theorem controls
the canonical point and its squared norm. Bisection of that norm,
followed by coordinate bisections inside a sufficiently thin norm
sublevel, gives certified approximations: the projection inequality
bounds every point in that sublevel by its distance to the unique
minimum-norm point. Common-field algebraic recognition then recovers
the exact tuple. Each requested coordinate precision restarts from the
same universal continuous box; a box retained from an earlier
approximation need not contain the canonical point itself.
This argument requires no algebraic-coefficient
feasibility oracle.

**Fractional MISOCP consequence.** Under the denominator-positivity
hypothesis in Section 6.1, fixed \(k,h\) permits polynomial-time exact
classification, value recovery, attainment decision, and recovery of
an optimal integer assignment and algebraic continuous optimizer for
an unbounded rational affine-fractional MISOCP. The runtime exponent
depends on \(k,h\); this is not an FPT claim.

## 7. Why strict sublevels do not control optimal witness size

For an integer \(a\ge1\), define

\[
 E^{(a)}=
 \{(x,w,t):t>0\}\ \cup\
 \{(x,w,0):x^2-2^{2a+1}w^2=1,\ x\ge1,\ w\ge1\}.
 \tag{12}
\]

The integer coordinates are \((x,w)\), so \(k=2\). This is an
upward semialgebraic set described by a fixed number of degree-two
atoms, with coefficient bit length \(H=O(a)\). Its strict sublevels
are empty for \(t\le0\) and all of \(\mathbb R^2\) for
\(t>0\). In particular every strict sublevel is convex. Its
mixed-integer infimum is zero and is attained.

Nevertheless, every optimal integer point has an \(x\) coordinate
requiring at least \(2^a\) bits. To verify this, put \(y=2^a w\).
The optimality equation becomes

\[
                          x^2-2y^2=1.
 \tag{13}
\]

Every positive solution has
\(x+y\sqrt2=(3+2\sqrt2)^n\) for an integer \(n\ge1\).
An elementary proof divides a positive unit by powers of
\(3+2\sqrt2\) until it lies in \([1,3+2\sqrt2)\): in this
interval its nonnegative integral \(y\) is less than two, and
\(y=1\) would require \(x^2=3\), so the remaining unit is one.

Write \((3+2\sqrt2)^n=x_n+y_n\sqrt2\). Each \(x_n\) is odd.
For odd \(n\), binomial expansion gives \(y_n\equiv2\pmod4\).
The doubling identity \(y_{2n}=2x_ny_n\) therefore gives

\[
                         v_2(y_n)=v_2(n)+1.
 \tag{14}
\]

The requirement \(2^a\mid y_n\) forces
\(n\ge2^{a-1}\); choosing \(n=2^{a-1}\) also proves existence.
Finally
\(x_n=((3+2\sqrt2)^n+(3-2\sqrt2)^n)/2>4^n/2\), so its
binary length is at least \(2n\ge2^a\).

Thus a bound polynomial in \(H\) fails for optimal integer witnesses
under strict-sublevel convexity alone, even at fixed \(k,d\) and
fixed atom count. The weak optimal slice in (12) is not convex.
The finite-value theorem is consistent with this example because its
value is the small transition level zero. No claim is made that the
Pell growth phenomenon itself is new.

## 8. Prior results, significance, and verification

The main predecessors remain Khachiyan--Porkolab's convex semialgebraic
integer witness theorem, its bounded integral slab result (Theorem
3.1(ii)), and its algebraic affine-hull reduction (Theorem 3.4).
Those established results optimize an integer coordinate or a rational
polynomial objective on integer vectors. The present target is the
possibly unattained real objective value after continuous variables
have been projected out.

The geometric step uses the classical theorem that a full-dimensional
maximal lattice-free set is a polytope plus a rational linear space,
including the containment theorem in
[Basu--Conforti--Cornuejols--Zambelli](https://personal.lse.ac.uk/zambelli/papers/lattice-free.pdf).
No new lattice-free structural theorem is claimed. The proposed
quantitative addition is the finite list of small transition levels
and the controlled cap inside the interval containing the unknown
infimum. They replace the sublevel invariance that joint convexity
gave in the earlier note.

For fractional optimization, the prior comparison must include
[Espinoza--Fukasawa--Goycoolea (2010), *Lifting, tilting and fractional
programming revisited*](https://mgoycool.github.io/papers/10espinoza_orl.pdf).
Their Theorem 2.3 and Section 5 treat point or recession-ray values and
asymptotically optimal sequences for fractional mixed-integer linear
optimization. Unattained fractional values in the rational polyhedral
case are therefore established prior knowledge. The candidate conic
application concerns unbounded SOC systems with a controlled continuous
Hessian span.

A separate literature audit is checking quasiconvex integer programming,
mixed-integer real objectives, and fractional optimization. An unsuccessful
search does not establish novelty. The theorem could enable exact
termination and value recovery for representations with efficient convex
threshold oracles; it does not establish a practical implementation or
an immediate solver speedup.

A fresh [independent reviewer](quasiconvex-mixed-value-review.md)
checked the transition formulas, controlled-cap construction,
coefficient accounting, induction, and the Pell boundary, and found
no gap conditional on the stated theorem inputs. The reviewer
contributed the value-variable lift in Section 6.2; the author checked
its Hessian span, joint-field bound, canonical-point selection, compact
boxing, and optimal-face recovery independently. The subsequent
[fresh full audit](fractional-misocp-optimization-adversarial.md) checked
that completion independently and found no remaining gap. A separate
[transition audit](quasiconvex-transition-independent-audit.md) rechecked
the value theorem and Pell boundary.

The reviewer ran
`python research-20260927/check_quasiconvex_attainment_pell.py`,
which checked exact Pell identities and valuations through \(n=1024\).
A separate literature auditor independently checked the infinite
valuation and size proof, and tested \(n\le512\) and the first
divisibility indices for \(1\le a\le10\). An author-run inline
SymPy command checked the exact Hessian of \(p-vq\); its only nonzero
blocks are the two cross blocks between \(v\) and the denominator's
continuous gradient. Local-link, newline, whitespace, and control-character
checks passed on this manuscript. Finite calculations check these
examples and identities; the proofs establish the infinite statements.
No project-wide verification or CI inspection has been performed.
