# Review of the quasiconvex mixed-integer value extension

Date: 2026-09-28. This is an independent adversarial review of the
[quasiconvex extension](quasiconvex-mixed-value-frontier.md) of the
[convex semialgebraic value theorem](unbounded-misocp-multiple-integer-frontier.md)
to an upward semialgebraic set whose strict sublevels are convex. The
finite-value argument passes this review, subject to the explicit
quantifier-elimination, algebraic-sampling, and integer-witness inputs
identified below. Strict-sublevel convexity alone does **not** give the
proposed size bound for an attained optimizer. Section 6 gives a fixed
dimension, quadratic counterexample with exponentially long optimizers.
No novelty claim is made in this review. After auditing the proposed
argument, I read the complete saved manuscript, Sections 1–8. Its
finite-value theorem, restricted attained-integer corollary, and
affine-fractional value application agree with the reviewed argument.
I also checked the subsequently added attainment and recovery argument
in Section 6.2. I suggested its value-variable lift during this review,
so that subsection needs an additional fresh review for full reviewer
independence; the author has independently checked the proposed lift.

## 1. Statement reviewed

Let \(E\subseteq\mathbb R^k\times\mathbb R\) be upward closed in its
last coordinate. Suppose it has a quantifier-free Boolean description
whose integer polynomial atoms have degree at most \(d\ge2\) and
individual coefficient bit length at most \(H\ge1\). The number of atoms
is unrestricted. Assume each strict sublevel

\[
 C_t=\{z:\exists s<t\ ((z,s)\in E)\}
\]

is convex, the mixed-integer domain is nonempty, and

\[
 \theta=\inf\{t:(z,t)\in E,\ z\in\mathbb Z^k\}
\]

is finite. The reviewed conclusion is that the minimal polynomial of
\(\theta\) has degree at most \(d^{G(k)}\) and coefficient bit length at
most \((H+1)d^{G(k)}\), for an effective function \(G\). These bounds do
not depend on the number of atoms. This is a bound on the value, not a
claim that the required intermediate descriptions can be constructed
without a running-time dependence on atom count.

## 2. The finite transition set

For every \(t\), including levels with empty sublevel, set

\[
 A_t=\{a\in\mathbb R^k:\sup_{z\in C_t}|a^Tz|<\infty\},
 \qquad r_t=\dim A_t,
 \qquad e_t=\dim\operatorname{aff}C_t,
\]

with \(A_t=\mathbb R^k\) and \(e_t=-1\) when \(C_t\) is empty.
Nesting gives \(A_t\supseteq A_u\) and
\(\operatorname{aff}C_t\subseteq\operatorname{aff}C_u\) for \(t<u\).
Consequently \(r_t\) is nonincreasing and \(e_t\) is nondecreasing.

For each \(1\le j\le k\), the predicate \(r_t\ge j\) has a first-order
definition: choose \(j\) vectors with positive Gram determinant and
require every chosen form to be bounded on \(C_t\). One common positive
bound suffices. The predicate \(e_t\ge j\), for \(0\le j\le k\), is
defined by \(j+1\) affinely independent points in \(C_t\); \(j=0\)
expresses nonemptiness. These formulas need only \(O(k^2)\) additional
real variables and a number of quantifier blocks depending on \(k\).
Their atomic degrees are at most \(\max\{d,O(k)\}\), and their
coefficient bits are \(H+O_k(1)\).

Each such predicate defines an initial or terminal interval, possibly
empty or all of the line. Each has at most one finite boundary point.
Let \(K\) be the union of these boundary points. Then

\[
                         |K|\le 2k+1.
\]

Quantifier elimination bounds the degree and coefficient bits of every
finite point of \(K\) by \(d^{O_k(1)}\) and
\((H+1)d^{O_k(1)}\). This does not require bounding the number of output
atoms: at a finite boundary, at least one nonzero output atom vanishes.
Otherwise all signs, and hence the Boolean formula, are constant nearby.

On an open component \(J\) of \(\mathbb R\setminus K\), both dimensions
are constant. Inclusions of finite-dimensional linear or affine spaces
with equal dimensions are equal. Thus the actual spaces \(A_t\) and
\(\operatorname{aff}C_t\), not only their dimensions, are constant on
\(J\). Endpoint conventions do not affect this statement. Empty levels
must be accounted for through \(e_t=-1\); omitting them would leave a gap.

## 3. A controlled cap inside the relevant interval

If \(\theta\in K\), the value bound is already proved. Otherwise write
\(J=(\alpha,\beta)\) for the component containing \(\theta\). All \(C_t\)
in \(J\) are nonempty: there is a feasible mixed-integer value below some
level of \(J\), and the constant affine dimension rules out emptiness at
another level. The proposed cap construction is valid as follows.

If \(\beta<\infty\), then \(C_\beta\) is convex and contains an integer
point because \(\theta<\beta\). Specify \(\beta\) by a polynomial and a
rational isolating interval. The convex integer-witness theorem applied
to

\[
 \exists s<\beta\ ((z,s)\in E)
\]

gives some integer \(z_0\) with bit length \((H+1)d^{O_k(1)}\).
Algebraic sampling gives a value \(s_0<\beta\) with
\((z_0,s_0)\in E\), with the same form of degree and height bounds.
In particular \(s_0\ge\theta>\alpha\). Algebraic root separation then
gives a rational \(U\in(s_0,\beta)\) whose bit length has the same
bound. This provides \(\theta<U<\beta\) without presuming that
\(\theta\) is already algebraic.

If \(\beta=+\infty\), apply the integer-witness theorem to the convex
projection \(\bigcup_t C_t\). A controlled integer point and a sampled
feasible value \(s_0\) again exist. A rational integer \(U>s_0\), chosen
using the sample's root bound, has controlled size. Since
\(s_0\ge\theta>\alpha\), there is no separate need to place \(U\) above
\(\alpha\).

Root separation between \(s_0\) and \(\beta\) does not require them to
have been sampled in the same number field. A product polynomial and
the usual root-separation bound suffice. Its degree depends on \(k,d\),
and its logarithmic height remains linear in \(H+1\).

## 4. Descent and its coefficient accounting

Suppose first that \(C_U\) is not full-dimensional. A formula for a
nonzero affine normal to \(C_U\) has a controlled algebraic sample
\((a,b)\) in one field. Expand \(a^Tz=b\) in a rational basis of that
field. Every integral point in \(C_U\) satisfies each resulting rational
equation. At least one normal is nonzero. After clearing denominators,
one such equation has the form \(p^Tz=q\) with integer data of bit
length \((H+1)d^{O_k(1)}\). It is consistent over the integers because
\(C_U\) contains an integer point. A lattice parametrization decreases
the integer dimension and retains all improving points below \(U\).

Now suppose that \(C_U\) is full-dimensional. If
\(A_U\cap\mathbb Q^k=\{0\}\), choose \(t\in J\) below \(\theta\).
Then \(C_t\) is nonempty, full-dimensional, convex, and integer-free.
Its closure is lattice-free because
\(\operatorname{int}\overline{C_t}=\operatorname{int}C_t\subseteq C_t\).
Maximal lattice-free containment supplies a set \(P+L\) containing it,
where \(P\) is a polytope and \(L\) a proper rational linear space.
A nonzero rational form in \(L^\perp\) is bounded in both directions on
\(C_t\), hence belongs to \(A_t=A_U\), a contradiction.

Therefore \(A_U\) has a nonzero rational vector. The common-field basis
and rational-kernel construction in the earlier value proof gives an
integer vector \(a\ne0\) of bit length \((H+1)d^{O_k(1)}\). Its finite
range endpoints over \(C_U\) have controlled algebraic degree and
height. Hence only integers \(b\) of controlled bit length can occur as
\(a^Tz\) on \(C_U\cap\mathbb Z^k\). One such \(b\) occurs along a
subsequence approaching \(\theta\). Restricting to \(a^Tz=b\) again
decreases the integer dimension and preserves the infimum.

The transformed set remains upward, and its strict sublevels are affine
preimages of the original convex sublevels. Crucially, carry the
transformed original atoms into the next stage. Integer affine
substitution leaves their degree at most \(d\); if the substitution data
has \(L\) bits, it adds at most \(O_k(dL+\log(d+1))\) coefficient bits.
Thus at most \(k\) restrictions preserve a bound of the form
\((H+1)d^{O_k(1)}\). Replacing the carried atoms with successive
quantifier-elimination outputs is unnecessary.

This also clarifies the terminal case. If the value is not already a
transition, each positive-dimensional stage must decrease the integer
dimension. In dimension zero, a finite infimum is a nonemptiness
transition. There is no need for a separate terminal identification
with a continuous relaxation.

## 5. Attainment needs a stronger hypothesis

Strict-sublevel convexity does not imply that the actual weak slice

\[
                    E_t=\{z:(z,t)\in E\}
\]

is convex. The set \(\bigcap_{\varepsilon>0}C_{t+\varepsilon}\) is
convex, but it can contain points whose vertical infimum is not attained.
The integer-witness theorem cannot be applied to an arbitrary subset
\(E_\theta\) of that intersection.

An additional assumption that every \(E_t\) is convex repairs the
optimizer-size argument. After the value bound, specify \(\theta\) by
its polynomial and isolating interval and apply the convex integer
witness theorem to \(E_\theta\).

A sufficient condition is that every vertical fiber of \(E\) is closed.
Indeed, upward closure and vertical closedness give

\[
             E_t=\bigcap_{\varepsilon>0}C_{t+\varepsilon}.
\]

For the nontrivial inclusion, membership in each set on the right gives
feasible vertical levels approaching \(t\) from above, unless a feasible
level at most \(t\) already exists. Closedness then supplies \((z,t)\).
Ordinary epigraphs of extended-real functions have closed vertical
fibers, independently of lower semicontinuity or joint convexity.

More generally, for any semialgebraic \(S\subseteq\mathbb R^k\), the set

\[
 (\mathbb R^k\times(0,\infty))\ \cup\ (S\times\{0\})
\]

has convex strict sublevels and finite mixed-integer infimum zero.
Attainment is exactly the assertion \(S\cap\mathbb Z^k\ne\varnothing\).
Thus the strict-sublevel hypothesis places no restriction on the integer
feasibility problem hidden at the optimal level.

## 6. A quadratic counterexample with exponentially long optimizers

For \(a\ge1\), define an upward set in two integer coordinates by

\[
 E_a=\{(x,w,t):t>0\}\ \cup
 \{(x,w,0):x^2-2^{2a+1}w^2=1,\ x\ge1,\ w\ge1\}.
\]

The number of atoms and their degree, at most two, are fixed. Their
largest coefficient has \(2a+2\) bits. Its strict sublevels are empty
for \(t\le0\) and all of \(\mathbb R^2\) for \(t>0\). The value is zero
and is attained, but every attaining integer \(x\) has at least \(2^a\)
bits.

To prove the last statement, put \(y=2^a w\). All positive integer
solutions of \(x^2-2y^2=1\) are

\[
             x_n+y_n\sqrt2=(3+2\sqrt2)^n,\qquad n\ge1.
\]

For completeness, multiplication by \(3-2\sqrt2\) maps any positive
solution with \(y\ge2\) to
\((3x-4y,3y-2x)\), a solution with positive first coordinate and smaller
nonnegative second coordinate. Here \(\sqrt2<x/y\le3/2\), with equality
at \((x,y)=(3,2)\). Repetition reaches \((1,0)\), proving the stated
parametrization.

Every \(x_n\) is odd. For odd \(n\), binomial expansion modulo four
gives \(y_n\equiv2\pmod4\). The identity

\[
                         y_{2n}=2x_ny_n
\]

therefore proves

\[
                        v_2(y_n)=v_2(n)+1.
\]

The divisibility \(2^a\mid y_n\) forces \(n\ge2^{a-1}\), and this
smallest exponent does give an admissible positive \(w\). Since
\(3+2\sqrt2>4\),

\[
 x_n=\frac{(3+2\sqrt2)^n+(3-2\sqrt2)^n}{2}
       >2^{2n-1}.
\]

Its binary length is therefore at least \(2n\ge2^a\). With fixed
\(k=2,d=2\), this contradicts any bound \((H+1)d^{G(k)}\) for an
attained optimizer under strict-sublevel convexity alone. The finite
value bound remains valid: the value is exactly zero.

## 7. The affine-fractional application

The manuscript's application to \(p(z,x)/q(z,x)\) on a rational SOC set
\(F\), under \(q>0\) throughout \(F\), preserves convexity of every
weak threshold set: it is \(F\cap\{p-tq\le0\}\). Rational thresholds
add only an affine row and preserve the continuous squared-Hessian
span. Treating \(t\) as an additional free parameter in the compressed
projection also fits the existing construction: coefficients of \(x\)
are affine in the parameters and constant terms have degree at most
two. Thus the stated exact finite-value application passes this review,
conditional on the separately reviewed compressed projection and
MISOCP feasibility theorems.

The completion added as Section 6.2 was suggested during this review and
independently checked by the author. At a fixed integer assignment,
introduce a continuous variable
\(v\) and the rational quadratic row

\[
                         p(x)-v q(x)\le0.
\]

Minimizing \(v\) over this set and the original squared SOC rows and
sign rows gives precisely the fractional problem, because \(q>0\) on
the original feasible set. The new row adds at most one direction to
the continuous Hessian span. Therefore the existing rational
nonconvex attained-optimizer theorem gives the missing
uniform continuous optimizer bound with span at most \(h+1\), without
inserting the algebraic optimal value as an input coefficient.

Combined with the attained-integer corollary, that bound supplies an
optimizer box if the optimum is attained. On the compact original
feasible set in such a box, \(q>0\) implies that the fractional
objective is continuous and attains its minimum. Exact boxed
fractional value recovery then decides attainment by comparing the
boxed and unboxed values. This is noncircular: the boxed value algorithm
was established without an attainment test.

For exact recovery, the optimal set in a fixed attaining fiber is
\[
                  F_z\cap\{x:p(z,x)-\theta q(z,x)=0\}.
\]
It is closed and convex. The minimum-norm optimizer of the lifted
problem is \((x^*,\theta)\), where \(x^*\) is the unique minimum-norm
point of this set. The cited optimizer theorem explicitly bounds the
joint field and representation of the minimum-norm point, not merely
some arbitrary optimizer. Its radius can be chosen uniformly for
every attaining integer assignment in the prescribed integer box;
the original continuous box therefore contains the canonical point of
the fiber eventually selected by integer bisection.

On a rational box or norm cut, compute the exact fractional minimum,
returning false if the cut is infeasible. Otherwise, that cut meets the
optimal set exactly when this minimum equals \(\theta\), because its
domain is compact. Norm and coordinate approximation with this oracle
is the previously reviewed continuous SOCP recovery construction.
The extra norm row adds at most one Hessian direction. The common-field
bound for \(x^*\) also controls its squared norm, without multiplying
individual coordinate degrees.

I found no mathematical gap in the saved Section 6.2 under its stated
dependencies. Since I proposed the value-variable lift, this part of
the review should not be counted as a wholly independent review of
that additional step.

## 8. Sources and verification limits

The following primary statements were inspected for this review:

- Khachiyan and Porkolab, [*Integer Optimization on Convex Semialgebraic
  Sets*](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
  Theorem 1.1 and Propositions 2.1–2.2 and Corollary 2.3. They supply the
  convex integer-witness, elimination, and common-field sample bounds.
  Their degree and individual coefficient bounds are independent of
  atom count and linear in the input coefficient bit bound. Their
  runtime bounds are not atom-count independent. Their discussion of
  quasiconvex polynomial integer optimization does not itself establish
  the present continuous, possibly unattained value extension.
- Basu, Conforti, Cornuéjols and Zambelli, [*Maximal lattice-free convex
  sets in linear subspaces*](https://personal.lse.ac.uk/zambelli/papers/lattice-free.pdf),
  Theorem 2 and Corollary 17 in the linked version. This supplies the qualitative
  bounded rational form; no quantitative facet bound is being claimed.

The review is a mathematical audit, not a formal proof. The targeted
command `python research-20260927/check_quasiconvex_attainment_pell.py`
passed. The exact script
[check_quasiconvex_attainment_pell.py](check_quasiconvex_attainment_pell.py)
checks the Pell identity and valuation for the first 1,024 positive
powers and the optimizer growth for \(a=1,\ldots,11\). The all-parameter
claim is proved above; the finite computation only checks the recurrence
and indexing. No project-wide tests or CI checks were run.
