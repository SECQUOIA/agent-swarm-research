# Exact optimization of strongly convex quartics reduces to PosSLP

Date: 2026-09-28. Status: proved, including the polynomial-observable
extension, and passed
[fresh independent adversarial review](strong-convex-quartic-posslp-upper-independent-review.md).
The root and this author independently
suggested the weak-optimization/Newton outline; the root identified the
two primary source dependencies below. This note supplies the detailed
reduction. Publication priority is unestablished.

Let \(f\in\mathbb Q[X_1,\ldots,X_n]\) have degree at most four.
The input includes a positive rational \(\mu\), with the promise
\[
                    \nabla^2 f(X)\succeq\mu I_n
                    \qquad(X\in\mathbb R^n).             \tag{1}
\]
Let \(p\) be its unique unconstrained minimizer. The input also
specifies a rational threshold \(r\) and, for coordinate comparison,
an index \(j\).

**Theorem.** Each of the following questions reduces in deterministic
polynomial time to a single PosSLP instance:
\[
 \min_{X\in\mathbb R^n}f(X)<r,\qquad
 \min_{X\in\mathbb R^n}f(X)\le r,\qquad
 p_j>r.                                                  \tag{2}
\]
The same holds for the other order relations and for equality.
No nonzero-optimum or nonzero-coordinate-gap promise is needed.
The reduction uses ordinary polynomial-time convex optimization only
to produce an initial rational point with polynomially many bits.
Further precision is represented by a rational arithmetic circuit.
No oracle calls are made while constructing the final PosSLP circuit.

More generally, each order or equality predicate comparing \(h(p)\)
with zero has the same one-instance reduction, for any supplied
rational polynomial \(h\) of degree at most four.
The polynomial \(h\) need not be convex. Its encoding is included
in the input length. The questions in (2) use \(h=f-r\) or
\(h=X_j-r\). If zero-dimensional constant objectives are allowed,
handle them by direct rational comparison; below assume \(n\ge1\).

The domain is all of \(\mathbb R^n\). This theorem does not assert
an upper bound for constrained polynomial optimization, or for a
quartic lacking the supplied global strong-convexity bound.

An important fully verifiable input format supplies a rational
positive definite matrix \(M\) satisfying
\[
 v^{\mathsf T}\nabla^2f(X)v
   =(v,X\otimes v)^{\mathsf T}M(v,X\otimes v).             \tag{3}
\]
If \(m\) is the dimension of \(M\), the rational number
\[
              \mu=\frac{\det M}{(\operatorname{tr}M)^{m-1}}
                                                               \tag{4}
\]
satisfies (1). The identity and positive definiteness are checkable in
polynomial time; (4) is computable in polynomial time and has
polynomial bit length. Invalid certificates can be rejected before
constructing the reduction. Thus the theorem also applies to an
ordinary language of quartics with supplied positive definite Hessian
Grams, rather than only to a curvature promise problem.

Combined with the separately reviewed lower-bound constructions, the
theorem gives PosSLP-completeness for both exact unconstrained
minimum order comparison and minimizer-coordinate order comparison in that
certificate format. See the
[unconstrained value reduction](unconstrained-quartic-posslp-reduction.md)
and the
[root-coordinate reduction](posslp-certified-cubic-root-reduction.md).
This completeness statement concerns the strict and weak order
relations. Equality has the upper bound proved here; no matching
equality lower bound is claimed. Publication priority for the combined
classification remains unestablished.

## 1. Explicit bounds and a Newton neighborhood

Let \(L\ge2\) bound the total explicit binary input length after
adding \(\mu\), and including the observable \(h\). In the
certificate format this enlarged length
is polynomial in the original input length. We may assume
\(n\le L\), at most \(L\) nonzero monomials, and
\[
 2^{-L}\le\mu\le2^L,\qquad
 \max\left\{\sum_\alpha |f_\alpha|,
             \sum_\alpha |h_\alpha|\right\}
       \le L2^L\le2^{2L}.                                \tag{5}
\]
Strong convexity makes \(f\) coercive, so \(p\) exists and is
unique, with \(\nabla f(p)=0\). Strong monotonicity of the
gradient, applied at \(0\) and \(p\), gives
\[
 \|p\|\le\frac{\|\nabla f(0)\|}{\mu}
        \le2^{3L}.                                       \tag{6}
\]
Fix the rational bounds
\[
                         R=2^{4L},\qquad B=2^{20L}.
                                                               \tag{7}
\]
On the Euclidean ball \(\|X\|\le R\), \(B\) bounds
\(|f(X)|\), \(\|\nabla f(X)\|\), the Hessian operator
norm, and a Lipschitz constant for the Hessian in operator norm.
The same bounds hold for \(h\), whether or not \(h\) is convex.
Here are conservative estimates that verify this choice. Put
\(C=\sum|f_\alpha|\le2^{2L}\). A partial derivative of
order \(k\le3\) is bounded in magnitude by
\(24C(1+R)^{4-k}\); the order-zero bound is
\(C(1+R)^4\). More sharply, the gradient and Hessian use factors
4 and 12 respectively. The Euclidean gradient norm costs at most
\(\sqrt n\), the Hessian operator norm at most \(n\), and
the third-derivative operator norm at most \(n^{3/2}\).
Using \(1+R\le2^{4L+1}\) and \(n\le L\), the four
bounds are respectively at most
\[
 2^{18L+4},\quad2^{15L+5},\quad2^{11L+6},\quad2^{8L+6},
\]
all bounded by \(B\) for \(L\ge2\). The third bound
controls Hessians, and the fourth gives their Lipschitz constant by
integrating along line segments in the ball.
Replacing \(f\) by \(h\) in this calculation proves the claimed
observable bounds.

Define
\[
           \rho=\frac{\mu}{4B},\qquad
           \varepsilon_0=\frac{\mu\rho^2}{2}
                         =\frac{\mu^3}{32B^2}.           \tag{8}
\]
Both rationals have polynomial bit length. Any point \(x_0\) with
\(f(x_0)\le f(p)+\varepsilon_0\) satisfies
\(\|x_0-p\|\le\rho\), by strong convexity.
Also \(\rho<1\), and the entire radius-\(\rho\) ball
around \(p\) lies strictly inside the ball in (7).

## 2. A polynomial-time rational initial point

We use the following established bit-model result. Slot, Steurer and
Wiedmer, [*Hesse's Redemption: Efficient Convex Polynomial
Programming*](https://arxiv.org/html/2511.03440v1), Corollary 1.2,
give a polynomial-time algorithm for obtaining a rational point with
additive objective error \(\varepsilon>0\) when minimizing an
explicit rational convex polynomial over a nonempty rational
polyhedron; the running time is polynomial in the input encoding and
\(\log(1/\varepsilon)\). Apply it to \(P=\mathbb R^n\)
and \(\varepsilon=\varepsilon_0\). Strong convexity excludes
the theorem's unbounded case.

The result is an explicit rational point \(x_0\) of polynomial bit
length satisfying (8). This preliminary algorithm uses ordinary
rational arithmetic of polynomial bit length. It makes no PosSLP
calls. Only inverse-exponential accuracy with a polynomial-size
exponent is requested here.

The source's encoding convention and Corollary 1.2 were read directly.
Its conclusion is an actual point in \(P\), so no repair of an
approximately feasible point is needed. The displayed Proposition 3.2
in that version omits the convexity hypothesis that its gradient
separation proof uses; the present dependency is the explicitly
convex Corollary 1.2, not a nonconvex reading of Proposition 3.2.
Because (6) already bounds the minimizer, classical convex optimization
with a supplied search radius would also suffice. The cited corollary
provides a convenient explicit statement in the bit model; its more
general solution-radius theorem is not essential here.

## 3. Rapid refinement as a rational circuit

Starting at \(x_0\), take full Newton steps
\[
 x_{k+1}=x_k-\nabla^2f(x_k)^{-1}\nabla f(x_k).              \tag{9}
\]
These are exact rational operations. Write \(e_k=\|x_k-p\|\).
If \(e_k\le\rho\), the Hessian Lipschitz bound and the
identity \(\nabla f(p)=0\) give
\[
\begin{aligned}
 x_{k+1}-p
 &=\nabla^2f(x_k)^{-1}
   \int_0^1\bigl(\nabla^2f(x_k)-
             \nabla^2f(p+t(x_k-p))\bigr)(x_k-p)\,dt,\\
 e_{k+1}&\le\frac{B}{2\mu}e_k^2.                          \tag{10}
\end{aligned}
\]
Let \(q_k=Be_k/(2\mu)\). Then \(q_0\le1/8\),
\(q_{k+1}\le q_k^2\), and therefore
\[
 e_k\le\frac{2\mu}{B}\,2^{-3\cdot2^k}
      \le2^{L+1-3\cdot2^k}.                              \tag{11}
\]
The bound also proves inductively that all iterates stay in the
radius-\(\rho\) neighborhood and hence in the ball where the
derivative bounds were established. Every Hessian is positive definite
with inverse norm at most \(1/\mu\).

To implement (9), evaluate the fixed-degree gradient and Hessian and
solve the symmetric positive definite linear system by rational
\(LDL^{\mathsf T}\) elimination without square roots or pivoting.
All principal pivots are positive. This is a fixed rational arithmetic
circuit with polynomially many operations per step. There is no sign
test during elimination. Alternatively, standard determinant circuits
and the adjugate formula give the same size bound.

Retain shared nodes between steps. A polynomial number of Newton steps
therefore gives a polynomial-size rational arithmetic circuit for
\(x_k\), even though expanding its rational coordinates may take
exponentially many bits. The initial point is printed in binary; the
later rational iterates are only represented by their circuits.

## 4. A uniform algebraic separation bound

We establish the bound for the general observable
\(\alpha=h(p)\). The two original special cases are
\[
                     \alpha=f(p)-r
              \quad\text{or}\quad\alpha=p_j-r.           \tag{12}
\]
Consider the formula in the one free variable \(z\)
\[
 \exists X\in\mathbb R^n:\quad
       \nabla f(X)=0\quad\text{and}\quad z=h(X).          \tag{13}
\]
Its real solution set is exactly the singleton \(\{\alpha\}\).
Clear rational denominators. The formula has \(n+1\) integer
polynomials of degree at most four and coefficient bit lengths
polynomial in \(L\).

Basu's author survey
[*Algorithms in Real Algebraic Geometry: A Survey*](https://www.math.purdue.edu/~sbasu/raag_survey2011.pdf),
Theorem 2.16 on printed page 12, states a one-block quantifier
elimination bound: with one free variable, polynomial degrees and
coefficient bit lengths in the output are singly exponential in the
number of quantified variables when the input degree is fixed. The
coefficient-bit clause is part of that theorem. It follows that there
is a fixed effective polynomial \(a(L)\) with nonnegative integer
coefficients, which we enlarge so that
\(a(L)\ge40L+10\), such that (13) has a quantifier-free
description whose integer polynomials have degrees and coefficient
bit lengths at most \(2^{a(L)}\).

At least one nonzero polynomial in that description vanishes at
\(\alpha\). Otherwise every nonconstant sign test would be
constant on some neighborhood of \(\alpha\), and the Boolean
formula would define a neighborhood rather than a singleton. Zero
polynomials have constant sign and do not affect this argument.
Thus \(\alpha\) is a root of a nonzero integer polynomial
\(P\) with
\[
        \deg P\le2^{a(L)},\qquad
        \max|P_i|\le2^{2^{a(L)}}.                        \tag{14}
\]

If \(\alpha\ne0\), factor the largest power of \(z\)
from \(P\). The remaining polynomial has a nonzero integer
constant term. If \(|\alpha|<1\), comparing this constant
term with all other terms gives
\[
 1\le \deg(P)\,\max|P_i|\,|\alpha|.
\]
The case \(|\alpha|\ge1\) is easier. Consequently, in
both cases,
\[
 \alpha\ne0\quad\Longrightarrow\quad
          |\alpha|\ge2^{-2^{a(L)+1}}=:g.                 \tag{15}
\]

Quantifier elimination is used only to establish this bound; the
reduction never executes it or computes \(P\). Fix once and for
all an effective polynomial majorant \(a\) supplied by the
quantifier-elimination theorem. Its coefficients are absolute
constants of the reduction. The number \(g\) is then represented
by \(a(L)+1\) squarings starting with \(1/2\).

This argument does not assume the complex critical locus is finite.
For example, \(f(x,y)=(x^2+y^2)^2+x^2+y^2\) has real Hessian
at least \(2I\), but its complex critical locus also contains the
curve \(x^2+y^2=-1/2\). The singleton real
projection in (13) is sufficient for the stated real-algebraic bound.

## 5. Exact comparison with one PosSLP call

Use
\[
                         k=a(L)+2
\]
Newton steps. The observable gradient bound gives
\(|h(x_k)-h(p)|\le B\|x_k-p\|\), with no convexity
assumption on \(h\). Equations (11) and (7) yield
\[
 |h(x_k)-\alpha|
 \le2^{21L+1-12\cdot2^{a(L)}}\le g/8.                    \tag{16}
\]
The last inequality follows from
\(21L+4\le10\cdot2^{a(L)}\), guaranteed by the chosen
lower bound on \(a(L)\).

Let \(\widehat\alpha=h(x_k)\). The following rational
circuits are positive precisely in the stated cases:
\[
\begin{array}{c|c}
 \widehat\alpha-g/2 & \alpha>0\\
 \widehat\alpha+g/2 & \alpha\ge0\\
 -\widehat\alpha-g/2 & \alpha<0\\
 -\widehat\alpha+g/2 & \alpha\le0\\
 g^2/4-\widehat\alpha^2 & \alpha=0.
\end{array}                                               \tag{17}
\]
For the four order comparisons, (15)--(16) leave a margin at least
\(3g/8\) in every case, including \(\alpha=0\).
For equality, zero gives \(|\widehat\alpha|\le g/8\),
whereas a nonzero value gives
\(|\widehat\alpha|\ge7g/8\). The final rational circuit
output is therefore nonzero on every promised input.

Convert the selected rational circuit into an integer circuit, with
each value represented as \(N/D\) and \(D>0\). The division
rule
\[
 \frac{N_a/D_a}{N_b/D_b}
       =\frac{N_aD_bN_b}{D_aN_b^2}                       \tag{18}
\]
keeps denominators positive without a sign query; all divisors are
nonzero by the Newton and elimination arguments. Addition,
subtraction, and multiplication use their usual fraction formulas.
Every rational gate introduces only constantly many integer gates.
Build binary constants from zero and one and preserve sharing.

The final numerator is the required PosSLP instance. The initial
optimization takes polynomial bit time. The Newton circuit, the gap
circuit, the comparison circuit and their numerator-denominator
conversion have polynomial size and are constructed in polynomial
time. There is exactly one final sign query.

As an application of the observable statement, let \(f_1\) and \(f_2\)
be two such objectives with curvature bounds \(\mu_1,\mu_2\).
On disjoint variable blocks form
\[
 F(X,Y)=f_1(X)+f_2(Y),\qquad h(X,Y)=f_1(X)-f_2(Y).
\]
The unique minimizer of \(F\) is the pair of minimizers, and
\(\nabla^2F\succeq\min(\mu_1,\mu_2)I\). Thus a single
PosSLP instance compares the two exact minimum values, using a common
algebraic separation bound for their difference. The separable sum
need not have a positive definite Hessian Gram on the full joint basis;
the supplied-curvature version of the theorem is the one used here.
Separate Hessian certificates for the two objectives suffice to obtain
the needed curvature bound.

## 6. Short rational-circuit witnesses for strict feasibility

The constructed Newton vector \(x_k\) has a further consequence.
Take \(r=0\) in the objective case. If \(\min f<0\), then
(15)--(16) imply
\[
                            f(x_k)<0.                   \tag{19}
\]
Thus every strictly feasible instance in this class has a rational
feasible point whose coordinates have a shared arithmetic-circuit
representation of polynomial size. The reduction constructs that
representation in polynomial time without knowing whether the
instance is feasible. Determining the exact sign of its objective
still requires the final PosSLP comparison.

This statement gives no polynomial bound on expanded rational
numerators and denominators. It also does not assert a rational
feasible point when \(\min f=0\); a unique irrational minimizer
can make such a point impossible. The circuit representation and the
usual expanded binary representation are different certificate models.

## 7. Prior work, significance, and verification limits

There is an elementary degree distinction. A globally convex polynomial
of degree at most three has degree at most two: its Hessian is affine in \(X\),
and every linear matrix coefficient must vanish because the Hessian
remains positive semidefinite on both directions of every line.
An unconstrained strongly convex rational quadratic has a rational
minimizer and minimum obtained by polynomial-time rational linear
algebra. Thus degree four is the first possible degree of the hard
instances here. This does not assert a separation between P and PosSLP.

The proof combines existing bit-model convex approximation and real
algebraic bounds with standard quadratic Newton convergence and
rational-circuit simulation. The approximate-optimization theorem of
Slot, Steurer and Wiedmer is used only at polynomial precision.
It does not itself give the exact sign comparison in (2). Conversely,
the separation bound alone would require exponentially many printed
bits; Newton circuits provide a succinct representation of the needed
accuracy.

The closest inspected methodological predecessor is Etessami, Stewart
and Yannakakis,
[*Polynomial Time Algorithms for Multi-Type Branching Processes and
Stochastic Context-Free Grammars*](https://arxiv.org/pdf/1201.2374v2),
Appendix C, Corollary C.8. For least fixed points of probabilistic
polynomial systems, it already gives polynomial-time many-one
PosSLP equivalence for strict coordinate-threshold comparisons. Its
proof combines accurate Newton circuits, algebraic separation,
matrix inversion, repeated squaring and division elimination.
Those systems differ from the gradient equations of general strongly
convex polynomials; no reduction between the two input classes is
assumed here. The source's theorem and proof were read directly.

The broader methodology follows the classical use of high-precision Newton
circuits in reductions to PosSLP; see Allender, Bürgisser,
Kjeldgaard-Pedersen and Miltersen,
[*On the Complexity of Numerical Analysis*](https://people.cs.rutgers.edu/~allender/papers/slp.pdf),
Section 1.4 and Propositions 1.1 and 1.3. The
[certified cubic-root upper bound](posslp-certified-cubic-root-upper.md)
records that precedent in detail. The contribution here is
the matching exact classification for the stated globally strongly
convex quartic class, combined with the restricted lower bound.
The [separate primary-literature audit](strong-convex-quartic-posslp-upper-prior.md)
compares the assumptions and conclusions and records remaining gaps in
the novelty search. Publication priority is unestablished.

For MINLP, this identifies an exact arithmetic comparison problem that
already occurs in unconstrained quartic node bounds with explicit
global curvature certification. It distinguishes the theoretical cost
of exact sign decisions from polynomial-time approximate optimization.
It does not prove that PosSLP is NP-hard, that it lies outside P, or
that the circuit representation makes these decisions practically
efficient.

The author directly checked the cited source statements and all
derivative, Newton, separation and sign calculations. A fresh reviewer
independently reconstructed the original proof, including its source
dependencies, and ran
`python research-20260927/check_strong_convex_quartic_upper_review.py`.
That checker passed exact symbolic Newton and rational linear-system
identities, rational checks of the five final comparison formulas, and
constant-margin checks for \(2\le L\le64\). The finite checks
supplement the all-input proof. The author read the complete review
and did not rerun that checker. The reviewer separately reconstructed
the polynomial-observable extension, the pairwise-minimum application,
and the elementary degree distinction and found no mathematical defect.

No expanded high-precision computation or Lean formalization was
attempted. The author's targeted command
`git diff --check -- research-20260927/posslp-certified-cubic-root-upper.md research-20260927/strong-convex-quartic-posslp-upper.md`
passed after the observable amendment. An inline `python -` check
also passed for these two upper-bound notes, their independent reviews,
and the general-upper prior audit: five files and fifteen local links,
with paired math delimiters, final newlines, no trailing whitespace
or unexpected control characters, and no unescaped quad tokens in the
main notes. No project-wide tests or CI inspection were performed.
