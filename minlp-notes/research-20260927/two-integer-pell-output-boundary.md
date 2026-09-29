# Two integer variables can force exponential binary output

Date: 2026-09-28. Status: complete elementary proof, independently reviewed.
This is a classical Pell-equation phenomenon recorded as a
supporting boundary for the nonconvex one-integer results. No novelty is
claimed for the family, the divisibility calculation, or the output barrier.

There are quadratic integer optimization problems with two integer
variables, no continuous variables, and input length \(N\), for which
the shortest feasible point and the finite attained optimal value have
\(2^{\Theta(N)}\) binary digits. Every feasible point therefore requires
exponentially many bits. Thus a polynomial ordinary-output theorem
for one integer variable cannot extend to two integer variables for
arbitrary nonconvex quadratic constraints, even with continuous Hessian
span zero.

This obstruction concerns explicit output length. It establishes no
hardness result for feasibility decisions or succinct output.

## 1. The explicit family

For an integer \(m\ge1\), put \(D_m=5^{2m+1}\) and consider

\[
 \begin{array}{ll}
 \text{minimize}&x\\
 \text{subject to}&x^2-D_m y^2=1,\\
                 &x\ge2,\quad y\ge1,\quad x,y\in\mathbb Z.
 \end{array}                                                   \tag{1}
\]

The integer coefficient \(D_m\) is written explicitly in binary. There
are constantly many coefficients and variables, so the input length is
\[
                            N_m=\Theta(m).                    \tag{2}
\]
This is not a succinct encoding of a large coefficient: its ordinary
binary expansion has \(\Theta(m)\) digits.

The equality can be expressed by the two weak quadratic inequalities
\[
 x^2-D_my^2-1\le0,\qquad -x^2+D_my^2+1\le0.                    \tag{3}
\]
Their full Hessians are negatives of each other and span one dimension.
Both are indefinite. There are no continuous variables, so the
continuous Hessian span is \(h_{\rm cont}=0\). An unused continuous
variable fixed to zero by an affine equality can be added without
changing either the argument or that span.

Define the positive integers \(X_n,B_n\), for \(n\ge1\), by
\[
 \alpha=9+4\sqrt5,\qquad
                    \alpha^n=X_n+B_n\sqrt5.                   \tag{4}
\]

**Proposition.** The unique optimizer of (1) is
\[
          x_m^*=X_{5^m},\qquad y_m^*=B_{5^m}/5^m.              \tag{5}
\]
Its optimal value has binary length \(\Theta(5^m)\). Every feasible
point of (1) has at least this many bits in its \(x\)-coordinate.
Consequently the optimal value and the shortest ordinary feasible witness
have length \(2^{\Theta(N_m)}\), while every feasible witness has length
at least \(2^{\Omega(N_m)}\).

## 2. All positive solutions for the fixed radicand five

The classical Pell parametrization says that every solution of
\[
                   X^2-5B^2=1,\qquad X,B\in\mathbb Z_{>0}     \tag{6}
\]
is given by (4), with a unique \(n\ge1\). Here is a short proof for this
particular radicand.

For a solution, let \(\beta=X+B\sqrt5>1\). Its conjugate is
\(\beta^{-1}=X-B\sqrt5>0\). Choose the unique integer \(n\ge0\) with
\[
                         1\le\beta\alpha^{-n}<\alpha.
\]
Since \(\alpha^{-1}=9-4\sqrt5\), the quotient has integer coefficients:
\(\beta\alpha^{-n}=U+V\sqrt5\), where \(U,V\in\mathbb Z\) and
\(U^2-5V^2=1\). Positivity of the quotient and its conjugate gives
\[
 U=\frac{\gamma+\gamma^{-1}}2,\qquad
 V=\frac{\gamma-\gamma^{-1}}{2\sqrt5},\qquad
 \gamma=\beta\alpha^{-n}.
\]
Because \(1\le\gamma<\alpha\), one has \(U\ge1\) and \(0\le V<4\).
For \(V=1,2,3\), the required squares \(1+5V^2\) are respectively
\(6,21,46\), none a square. Thus \(V=0\), \(U=1\), and
\(\beta=\alpha^n\). As \(B>0\), necessarily \(n\ge1\).
Conversely every positive power has positive integer coefficients and
norm one. Uniqueness follows from \(\alpha>1\).

## 3. An elementary exact divisibility identity

For a positive integer \(a\), let \(v_5(a)\) be the largest integer \(r\)
such that \(5^r\) divides \(a\).

**Lemma.** For every \(n\ge1\),
\[
                              v_5(B_n)=v_5(n).                 \tag{7}
\]

**Proof.** In the binomial expansion of \((9+4\sqrt5)^n\), the
coefficient of \(\sqrt5\) is
\[
 B_n=\sum_{j=0}^{\lfloor(n-1)/2\rfloor}
       {n\choose 2j+1}\,9^{n-2j-1}\,4^{2j+1}\,5^j.
\]
Consequently
\[
                         B_n\equiv4n9^{n-1}\pmod5.            \tag{8}
\]
In particular, \(5\nmid B_n\) whenever \(5\nmid n\).

Expanding \((X_n+B_n\sqrt5)^5\) gives
\[
 B_{5n}
   =5B_n\bigl(X_n^4+10X_n^2B_n^2+5B_n^4\bigr).               \tag{9}
\]
The norm identity \(X_n^2-5B_n^2=1\) implies \(X_n^2\equiv1\pmod5\).
The parenthesized factor in (9) is therefore \(1\) modulo \(5\).
It follows exactly that
\[
                         v_5(B_{5n})=v_5(B_n)+1.              \tag{10}
\]
Write \(n=5^rs\) with \(5\nmid s\), use (8) at \(s\), and apply
(10) \(r\) times. This proves (7). \(\square\)

No algebraic-number-theoretic lifting-the-exponent theorem is needed.
All divisibility steps are identities and congruences of ordinary
integers.

## 4. Least feasible exponent and output length

Set \(B=5^m y\). Then the quadratic equation in (1) is precisely
\[
                             x^2-5B^2=1,
\]
with \(5^m\mid B\) and \(x,B>0\). Sections 2 and 3 show that its
feasible points correspond exactly to exponents \(n\ge1\) with
\[
            5^m\mid B_n
       \quad\Longleftrightarrow\quad
            v_5(n)\ge m
       \quad\Longleftrightarrow\quad
            5^m\mid n.                                       \tag{11}
\]

The least such exponent is \(n=5^m\). Its associated \(y\) in (5) is
a positive integer. Moreover
\[
                 X_n=\frac{\alpha^n+\alpha^{-n}}2
\]
is strictly increasing for positive integers \(n\). This proves the
existence and uniqueness of (5), including attainment.

Since \(0<\alpha^{-n}<\alpha^n\),
\[
                    \frac{\alpha^n}{2}<X_n<\alpha^n.
\]
Hence
\[
             n\log_2\alpha-1<\log_2X_n<n\log_2\alpha,          \tag{12}
\]
and the ordinary binary length of \(X_n\) is \(\Theta(n)\).
Substitute \(n=5^m\) and use (2) to obtain the proposition.
For the upper bound on the shortest witness, the optimizer itself suffices:
\(0<y_m^*\le B_{5^m}<X_{5^m}\), so its two coordinates together have
\(\Theta(5^m)\) bits. Other feasible witnesses can be arbitrarily larger.

In particular, an algorithm required to print the exact optimal value
in binary takes exponentially many steps just to write that output.
The obstruction is unconditional and remains with a feasibility oracle
of arbitrary computational power: an oracle does not shorten a required
explicit output.

## 5. Scope and succinct descriptions

The [one-integer value theorem](unbounded-misocp-value-frontier.md)
controls a nonconvex problem's integer tails through a one-dimensional
semialgebraic description. This example shows that the polynomial
ordinary-output conclusion cannot hold for arbitrary nonconvex
quadratic systems with two integer variables, even when there is no
continuous nonlinear part to control.

The optimal value is an integer, so its minimal polynomial has degree
one, \(T-X_{5^m}\). Its coefficient encoding nevertheless has exponential
length. This is a coefficient-height obstruction, not an algebraic-degree
obstruction; ordinary minimal-polynomial output does not avoid it.

It does not rule out the convex multivariate integer results: the real
feasible set of (1) is a hyperbola branch and is nonconvex. Neither
quadratic row in (3) is native PSD. It also does not establish that a
two-integer feasibility problem is outside NP or that deciding this
particular family's feasibility is hard. Every instance of (1) is
feasible by (5).

There is a short exact description of the optimizer. Starting from
\((X_1,B_1)=(9,4)\), apply the fifth-power coefficient map \(m\) times:
\[
 \begin{aligned}
 X'&=X^5+50X^3B^2+125XB^4,\\
 B'&=5X^4B+50X^2B^3+25B^5.
 \end{aligned}                                                \tag{13}
\]
The resulting pair is \((X_{5^m},B_{5^m})\). A circuit recording these
constant-size updates has \(O(m)\) arithmetic gates; dividing its second
output by the explicitly known integer \(5^m\) gives \(y_m^*\), with
exact division. Equivalently, (4) with exponent \(5^m\) is a compact
power description. Arithmetic-circuit size is not bit-operation time:
evaluating and printing the large integers still has the output cost in
(12).

Thus any broader exact theory must distinguish ordinary numerical output
from a succinct expression and separately justify operations on that
expression. This note provides no general succinct-output algorithm.

## 6. Prior work and what this note adds

The underlying phenomenon is classical. The following sources were
examined on 2026-09-28.

- H. W. Lenstra Jr., *Solving the Pell Equation*, Notices of the AMS
  49(2), 2002, 182–192,
  [open primary full text](https://wstein.org/edu/Fall2002/124/refs/lenstra_pell.pdf).
  Page 182 states the positive-solution power parametrization. Pages
  185–186 relate the regulator to explicit output length and explain
  that infinitely many radicands force exponential output time in the
  binary input length. Page 185 states the stronger family pattern
  \(d=d_0d_1^{2n}\), with regulator proportional to \(\sqrt d\) for
  all sufficiently large \(n\); \(d_0=d_1=5\) includes (1).
  Pages 187–188 discuss compact power-product representations.
  Therefore neither the output obstruction nor its geometric-radicand
  mechanism is new.
- Keith Conrad, *Pell's Equation, I*,
  [author's notes](https://kconrad.math.uconn.edu/math3240s20/handouts/pelleqn1.pdf),
  Theorem 5.3 and Example 5.6. These give the power parametrization and
  explicitly identify \(9+4\sqrt5\) as the generator for radicand five.
  The self-contained descent above is a specialization of this
  standard argument.
- A. H. M. Smeets's OEIS entry
  [A298212](https://oeis.org/A298212), submitted in 2018, concerns the
  least Pell exponent whose second coefficient is divisible by a given
  integer. The inspected entry explicitly records \(a(5^m)=5^m\).
  Thus even the specific least-exponent identity is already recorded
  publicly. The entry is a prior record; the proof here does not rely
  on it.

The purpose of this note is to supply an explicit, independently checked
boundary for the current MINLP research: fixed integer dimension two
and zero continuous Hessian span do not ensure polynomial-size ordinary
feasible witnesses or optimal values for general quadratic constraints.
It makes no publication or priority claim.

## 7. Verification

The [independent review](two-integer-pell-output-review.md) reconstructs
the Pell descent, divisibility identity, and encoding argument and found
no gap in the main proof. A second reviewer independently checked the
input/output interpretation. The review corrected the proposition's
wording: every feasible witness has the exponential lower bound, while
the matching upper bound concerns the shortest witness. It also corrected
the number of Conrad's radicand-five example. The author independently
checked both corrections and reread the proof review and its reproducible
exact-integer checker.

The reviewer ran:

    python research-20260927/check_two_integer_pell_output.py

The check passed the valuation identity and Pell norm for
\(1\le n\le3125\), both fifth-power coefficient identities for
\(1\le n\le40\), direct least-exponent searches for \(1\le m\le4\),
feasibility, circuit agreement, and output-size inequalities for
\(1\le m\le6\), and an
independent enumeration of positive base-Pell solutions with
\(1\le B<200000\). For \(m=1,\ldots,6\), the input coefficient has
\(7,12,17,21,26,31\) bits, while the optimal \(x\) has
\(20,104,520,2603,13017,65085\) bits.

These calculations corroborate finite instances. The universal statement
rests on the proof above. A targeted inline Python command checked this
note and its review for local-link existence, trailing whitespace, control
characters, final newline, and paired math delimiters; it passed.
No Lean formalization, project-wide
verification, or CI inspection was performed.
