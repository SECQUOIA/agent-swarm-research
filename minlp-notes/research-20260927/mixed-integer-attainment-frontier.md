# Unbounded mixed-integer convex quadratic optimization

Date: 2026-09-27. Status: proof and
[independent adversarial review](mixed-integer-attainment-complexity-review.md)
completed, with a separate root review. Publication priority is unestablished.
Finite attainment is established older work, discussed below. The proposed
additional conclusion concerns polynomial bit complexity when the integer
dimension and the span of the continuous constraint Hessians are fixed.

## 1. Proposed result

Consider

\[
 \inf\{q_0(z,x):(z,x)\in C\cap(\mathbb Z^k\times\mathbb R^n)\},
\]

where \(C\) is defined by rational affine equations, rational affine
inequalities, and rational quadratic inequalities \(q_i\le0\).
Every full Hessian, including that of \(q_0\), is positive semidefinite.
There are no variable bounds. Let \(N\) be the explicit binary input
length and let

\[
 h=\dim_{\mathbb Q}\operatorname{span}
       \{\nabla^2_{xx}q_i:i\ge1\}.
\]

**Theorem.** A nonempty instance with finite infimum attains it.
For every fixed \(k,h\), a deterministic polynomial-time Turing algorithm
classifies infeasibility, objective unboundedness, or a finite attained
optimum. In the finite case it returns an optimal integer assignment, the
exact algebraic optimal value, and an exact algebraic continuous optimizer.
Some optimal integer assignment has polynomial bit length, and the optimal
value has polynomial algebraic degree and coefficient bit length, for fixed
\(k,h\). All polynomial bounds are effective and uniform.

The statement is polynomial time for fixed parameters, not an FPT claim.
No useful numerical exponent or implementation advantage is asserted.
The continuous coordinates need not be rational. The objective Hessian is
not counted in \(h\), although objective threshold rows add at most one
to that parameter during the proof.

This would complete exact optimization for the class, including instances
without supplied variable bounds or strict feasible points. The parameter
permits many continuous variables and many quadratic constraints when their
continuous curvature comes from a fixed number of matrices. It could support
exact subroutines for models with a few integer design decisions and shared
quadratic metrics. Practical use still requires much sharper size bounds and
an implementation that avoids the large constants in the algebraic arguments.

Dependencies from this batch are the
[unbounded feasibility and projection theorem](unbounded-integer-frontier.md),
[continuous radius theorem](unbounded-hessian-span.md),
[bounded integer optimization theorem](mixed-integer-span-frontier.md),
[unbounded continuous value theorem](unbounded-value-optimization.md), and
[exact continuous optimizer construction](exact-convex-optimizer-recovery.md).
The latter construction has completed independent and separate root review.
The integer-assignment and value conclusions can also be separated from
that final output step.

## 2. Rational recession elimination

Write every inequality, including affine inequalities, as

\[
 q_i(w)=\tfrac12 w^TQ_iw+a_i^Tw+c_i\le0,
 \qquad w=(z,x),\quad Q_i\succeq0.
\]

Retain affine equalities separately as \(Ew=e\). For any nonempty
objective sublevel \(C\cap\{q_0\le b\}\), its recession cone is

\[
 R=\{d:Q_i d=0,\ a_i^Td\le0\ (i\ge1),\ Ed=0,
                Q_0d=0,\ a_0^Td\le0\}.                 \tag{1}
\]

This follows by expanding each quadratic along a ray. Necessity of
\(Q_i d=0\) uses positive semidefiniteness: a nonzero quadratic
coefficient cannot stay bounded above, and \(d^TQ_i d=0\) implies
\(Q_i d=0\). With that identity, the cross term vanishes and only
the affine slope remains. Equation (1) is independent of \(b\) and is
a rational polyhedral cone.

If (1) contains a vector with \(a_0^Td<0\), it contains such a
rational vector. Scale it so that its integer components are integral.
From any mixed-integer feasible point \(\bar w\), the points
\(\bar w+jd\), \(j\in\mathbb Z_+\), remain mixed-integer feasible
and their objective values tend to minus infinity. Thus this case certifies
objective unboundedness, once feasibility is known.

Otherwise every direction of (1) has zero objective slope. If (1) is
nonzero, choose a nonzero rational \(d\in R\). The identities give

\[
 q_i(w+td)=q_i(w)+t\alpha_i,\qquad
 \alpha_i=a_i^Td\le0,
 \qquad q_0(w+td)=q_0(w).                            \tag{2}
\]

Choose mixed-integer coordinates \((y,t)\) in which varying \(t\)
moves along \(d\). Two cases make the lattice preservation explicit.

* If \(d_z=0\), choose a continuous index \(j\) with \(d_{x,j}\ne0\).
  Every point has a unique form \(w=\widehat w+td\) with
  \(\widehat x_j=0\). All integer coordinates are unchanged.
* If \(d_z\ne0\), multiply \(d\) by a positive rational number so
  that \(p=d_z\) is a primitive integer vector. Complete \(p\) to a
  column of an integer unimodular matrix \(U\). Write
  \(z=U(z',t)\), \(x=x'+d_xt\), with \(z',t\) integral and
  \(x'\) continuous. This is a bijective change of the mixed lattice.

In these coordinates every row has form \(r_i(y)+\alpha_i t\).
Rows with \(\alpha_i=0\), all equalities, and the objective are
independent of \(t\). Projecting out \(t\) therefore deletes exactly
the rows with \(\alpha_i<0\) and retains the other rows. For any
point satisfying the retained rows, all deleted rows hold for sufficiently
large \(t\); this remains true when \(t\) must be integral.

The reduced problem has one fewer variable, rational PSD quadratic rows,
and exactly the same attainable objective values. Feasibility, unboundedness,
and attainment all transfer in both directions. This projection is exact;
no limit at infinity is used as a feasible point.

### Finite termination and attainment

Repeat the preceding elimination until a negative objective direction is
found or (1) becomes \(\{0\}\). At most \(n+k\) eliminations occur.
If \(R=\{0\}\), every nonempty objective sublevel is bounded: every
nonempty unbounded closed convex set has a nonzero recession direction.
It is also closed. A mixed-integer feasible objective sublevel is then
nonempty and compact, so its continuous objective attains its minimum.
Points outside that sublevel cannot improve its minimum.

This proves finite attainment and gives an exact unboundedness test after
feasibility. The argument works without fixed \(k,h\); these parameters
enter the complexity and witness bounds below.

One recession test on the original model is insufficient. For example,
minimizing \(-z\) subject to \(x\ge z^2\), \(z\in\mathbb Z\),
is unbounded below, but every original recession direction has zero
\(z\)-component and zero objective slope. Eliminating the continuous
\(x\)-direction drops its only quadratic row; the next reduced problem
reveals unboundedness. Accordingly, the algorithm reports objective
unboundedness but does not promise a decreasing straight ray in the original
feasible set.

### Bit complexity of the elimination

One can find rational recession directions and test negative objective
slope by rational linear programming. For nonzero directions, test the
finitely many systems \(d_j\ge1\) and \(d_j\le-1\); homogeneity
ensures that one succeeds whenever the cone is nonzero. Standard rational
LP witness bounds give a direction of polynomial bit length in the current
data.

Pure continuous eliminations cause no coefficient growth in the retained
problem: the restriction \(x_j=0\) literally removes the corresponding
coefficients from every retained polynomial. The shear involving \(d\)
is needed only to prove projection exactness, not to encode those rows.

An elimination with \(d_z\ne0\) decreases the number of integer
variables. There are at most \(k\) such steps. Primitive-vector
completion to a unimodular matrix has polynomial bit complexity, for
example by integer Hermite normal form. Substitution and restriction to
\(t=0\) have polynomial bit growth. Therefore the entire reduced
instance has polynomial size for fixed \(k\), even if the number of
continuous eliminations grows with the input.

The continuous Hessian span never increases: a pure continuous restriction
takes common principal submatrices, while an integer-direction elimination
at \(t=0\) changes only the remaining integer coordinates and leaves the
continuous coordinates unchanged. Deleting inequalities can only decrease
the span. The same observations apply to the objective Hessian.

## 3. A box for the terminal integer projection

Assume the original mixed-integer system is feasible and the elimination
terminates with \(R=\{0\}\). Call the reduced problem terminal.
Its encoding length is polynomial in \(N\) for fixed \(k\), and its
parameters are at most the original \(k,h\).

The unbounded integer-witness theorem supplies a terminal feasible integer
assignment of polynomial bit length for fixed \(k,h\). The continuous
radius theorem supplies a feasible continuous representative of polynomial
coordinate bit magnitude after fixing that assignment. Evaluating the
rational quadratic objective on the resulting uniform coordinate bounds
gives a computable rational integer \(B\), of polynomial bit length,
such that

\[
 K=C_{\rm terminal}\cap\{q_0\le B\}
\]

contains a mixed-integer point. The algorithm needs only these uniform size
bounds; it does not need to know that representative first. Since the
terminal recession cone is zero, \(K\) is compact. Its projection
\(Y\) on its remaining \(k'\le k\) integer coordinates is compact.

We need a bound on the whole projection, rather than only one feasible
integer point. Use the compressed projection formula from
[the projection theorem](unbounded-integer-frontier.md). Adding the
objective row raises the continuous Hessian span to at most \(h+1\).
The formula for \(Y\) has a prefix with block sizes
\(1,1,\max\{1,h+1\}\), polynomial atom degree and coefficient size,
and possibly many disjuncts. These atom bounds are uniform over the charts.

For each coordinate \(z_j\), existentially quantify the other
\(k'-1\) integer-coordinate *real* variables. This projects \(Y\)
onto a nonempty compact interval. The extra block can be combined with the
first existential radius block, giving the prefix
\(\exists(z_{-j},R)\,\forall t\,\exists\lambda\), with block sizes
at most \(k',1,\max\{1,h+1\}\). Coefficient-sensitive block quantifier
elimination therefore describes that interval by univariate integer
polynomials of degree and coefficient bit length polynomial in \(N\)
for fixed \(k,h\). The maximum atom degree and height bounds are
independent of the number of chart disjuncts; this is the precise
Khachiyan--Porkolab Proposition 2.1 bound used in the projection theorem.

At each endpoint of a nonempty bounded interval defined by a Boolean
combination of univariate polynomial signs, a nonzero defining polynomial
must vanish. Otherwise all nonzero signs would be locally constant and the
endpoint would not be a boundary point. The upper Cauchy root bound now
gives a computable \(L\), with polynomial bit length for fixed \(k,h\),
such that

\[
              Y\subseteq[-L,L]^{k'}.               \tag{3}
\]

No chart enumeration or quantifier elimination is performed by the
algorithm. These formulas establish a uniform size bound, from which a
conservative integer \(L\) is computed. If \(k'=0\), this step is
unnecessary.

Consequently some terminal optimal integer assignment has polynomial bit
length. Fix such an assignment. The continuous value theorem gives an
integer annihilator of the optimal value \(v\), with degree and
coefficient bit length polynomial in \(N\) for fixed \(k,h\).
The recession eliminations preserve all attainable objective values, so
the same \(v\) is the original optimum. Thus its algebraic complexity
has a uniform polynomial bound.

## 4. An optimal integer witness in the original coordinates

Naively lifting the eliminated coordinates can have poor size bounds:
successive continuous lifts may repeatedly square earlier quantities.
We therefore do not use those lifts to bound or compute the final answer.

Let \(P\in\mathbb Z[T]\) annihilate \(v\), with the degree and
height bound just obtained. Standard square-free factor and root-separation
bounds give a rational isolating interval for the particular root \(v\)
with bit length polynomial in those degree and height bounds, hence
polynomial in \(N\) for fixed \(k,h\). The set

\[
 Y^*=\{z\in\mathbb R^k:\exists x\ (z,x)\in C,
                                    q_0(z,x)\le v\}
\]

is convex and contains an integer point by attainment. Construct its
compressed projection formula symbolically with a free scalar threshold
\(T\). Add an existential quantifier for \(T\), the equation
\(P(T)=0\), and its isolating-interval conditions. The latter predicates
single out \(T=v\); they need not themselves be convex. The set described
in the free \(z\) variables is exactly the convex set \(Y^*\).

The formula has a fixed number of blocks, block sizes bounded by
\(2,1,\max\{1,h+1\}\), and polynomial atom degrees and coefficient
bit lengths for fixed \(k,h\). Apply Khachiyan--Porkolab Theorem 1.1
to this convex set, adjoining a dummy integer objective coordinate fixed
to zero as in the existing feasibility proof. Its integer-witness bound is
polynomial in \(N\) for fixed \(k,h\). Therefore some original
optimal integer assignment lies in a computable box with polynomial bit
length.

This argument needs existence of \(P\) and its isolating interval only;
their uniform bounds are enough to compute a conservative witness box.
It does not assume their coefficients or the optimum are already known.

## 5. Exact algorithm

1. Apply the existing unbounded feasibility algorithm. If infeasible,
   report that status.
2. Perform recession elimination. A negative objective direction in any
   reduced problem proves unboundedness of the original objective, because
   the projections preserve its attainable values. Otherwise termination
   proves that the optimum is finite and attained.
3. Compute the conservative bound from Sections 3--4 and impose the resulting
   box on the **original** integer coordinates. This retains an optimizer.
4. Use the bounded-integer, unbounded-continuous optimization reduction from
   this batch, with the explicit justification below. It returns a globally
   optimal integer assignment. Its threshold comparisons add at most one
   continuous Hessian direction.
5. Fix that assignment and apply exact continuous convex quadratic
   optimization. This returns the original optimal algebraic value and an
   optimal continuous vector.

Every called algorithm has polynomial Turing complexity for fixed \(k,h\).
Composition can increase the exponent; no sharp combined exponent is claimed.
The construction avoids explicitly generating the large projection formulas
and avoids sequentially lifting potentially enormous continuous coordinates.

For completeness, the bounded-integer optimization step does not impose one
continuous box merely known to preserve feasibility. Such a box could lose
an optimum. Instead, every feasible integer fiber has a finite attained
continuous optimum, because the original objective has already been proved
bounded below. Substituting the bounded integer assignment yields a uniform
polynomial input-size bound. The continuous value theorem therefore bounds
the degree and coefficient height of **all** these fiber optima uniformly.
The difference-resultant argument in the bounded optimization note gives a
computable separation \(\sigma>0\), with polynomial \(\log(1/\sigma)\),
between distinct fiber optima. Upper Cauchy bounds put all fiber optima in
a known interval \([-M,M]\), with polynomial \(\log M\).

Bisect from the strict lower bracket \(-M-1\) and feasible upper bracket
\(M\). Each rational threshold query appends \(q_0\le b\) *before*
using the continuous radius theorem. The resulting continuous box preserves
feasibility of that threshold in every bounded integer fiber. Apply the
bounded MILP reduction and fixed-integer-dimension MILP feasibility to this
boxed threshold instance. After polynomially many queries the bracket width
is less than \(\sigma\). An integer assignment feasible for its upper
endpoint must then have fiber optimum equal to the global optimum: any
distinct, larger fiber value would differ by at least \(\sigma\).
This supplies the claimed optimal assignment while allowing every continuous
fiber to be unbounded.

There is also a direct common-box argument using the exact continuous
optimizer theorem. For each feasible integer assignment in the original
witness box, that theorem bounds every coordinate of its minimum-norm
continuous optimizer by a uniform \(2^{\operatorname{poly}(N)}\), for
fixed \(k,h\). Its coordinate degree and coefficient-height bounds are
uniform after substitution of any integer assignment in the box, and the
upper Cauchy root bound gives the common radius. Adding that continuous box
retains an optimizer in every feasible integer fiber. The existing fully
boxed mixed-integer optimization theorem therefore applies directly.
This argument preserves fiber optima, whereas a common radius that only
retains arbitrary feasible fiber points would not justify optimization.

## 6. Prior results and remaining audit

Finite attainment is old. Bank and Mandel, *Nonlinear parametric integer
programming*, in *Parametric Optimization and Related Topics* (1987),
pp. 16--48, prove closedness of the mixed-integer right-hand-side feasibility
domain under a recession-generator condition (Theorem 7(ii), p. 34).
Their Theorem 3(iii), p. 24, makes that condition automatic for rational
quasiconvex polynomial data, including the stable subsystem used in
Theorem 7. Appending the objective as a constraint yields finite attainment
for a broader class than this note. These statements and their relevant
definitions were inspected in the
[accessible primary source](https://api.pageplace.de/preview/DT0400.9783112720936_A50662169/preview-9783112720936_A50662169.pdf).
The same result implies closedness of rational linear images by appending
opposite affine inequalities. The recession proof above is retained for its
explicit quadratic elimination and bit-control role. The
[separate prior audit](mixed-integer-attainment-prior.md) gives the comparison.

[Del Pia's convex quadratic programming theorem](https://arxiv.org/abs/2311.00099)
already classifies and exactly solves rational convex quadratic objectives
over mixed-integer polyhedra, with an FPT dependence on the integer dimension.
That stronger parameter dependence for affine constraints is not improved
here. Its separate feasibility result permits one convex quadratic row.
The candidate extension here permits an arbitrary number of native quadratic
rows with fixed span of their continuous Hessians, without input bounds.

[Khachiyan and Porkolab (2000)](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf)
supplies the integer-witness theorem and coefficient-sensitive elimination
bounds. Applied to the original uncompressed formula, its exponent depends
on the continuous dimension. This draft instead uses the compressed
projection charts already developed in this batch.

[Lubin, Vielma, and Zadik's mixed-integer convex representability paper](https://arxiv.org/abs/1706.05135)
was examined for possible nonattainment mechanisms. Its irrational-slope
constructions and rational conic encodings use constraints beyond native
PSD quadratic inequalities. Its structural Theorem 5.1 assumes the output
set is closed, so it is not by itself an attainment proof here.

The direction argument depends on full joint positive semidefiniteness.
Slice convexity alone does not suffice. General second-order cone systems
can have nonattained finite infima; for example minimizing \(u\) over
\(u,v\ge0,\ uv\ge1\) has infimum zero. Its defining quadratic is
indefinite, despite the feasible set being convex.

Independent review checked the parameter-preserving recession elimination,
the compact terminal projection bound, and the original optimal
integer-witness argument using an isolated algebraic threshold. A fresh
subreviewer separately checked the latter two steps against the primary
Khachiyan--Porkolab source. No unsuccessful literature search establishes
novelty.

## 7. Verification record

This draft records a symbolic proof. It does not rely on numerical testing
or Lean. An independent agent proposed and checked the basic recession
induction while searching for counterexamples; see the separate
[adversarial note](mixed-integer-attainment-adversarial.md). A fresh reviewer
then audited the complete complexity argument in the
[complexity review](mixed-integer-attainment-complexity-review.md). The
review found a missing justification for bounded-integer optimization with
unbounded continuous fibers; Section 5 now supplies both a threshold-specific
proof and a common optimizer-box proof. The author independently found and
rechecked that gap, and the reviewer accepted the completed argument.

The targeted commands `git diff --check --
research-20260927/mixed-integer-attainment-frontier.md` and an inline Python
check of this file's trailing whitespace, control characters, and final
newline passed. These are document checks, not mathematical verification.
No project-wide verification or CI inspection was run for this topic.
