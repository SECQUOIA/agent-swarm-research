# Independent review of the two-integer Pell output-size boundary

Date: 2026-09-28.

Scope: the proposed family

\[
 \min x,\qquad x,y\in\mathbb Z,\quad x\ge2,\ y\ge1,\quad
 x^2-5^{2m+1}y^2=1,\qquad m\ge1.
\]

The equality is encoded by its two opposite quadratic inequalities. This
review reconstructs the proof independently, checks the input/output
claims, and verifies the completed note's cited comparisons.

**Verdict: the claimed exponential ordinary binary output bound is correct.**
The fixed integer dimension is two. The continuous Hessian span is zero
because there are no continuous variables; the full quadratic Hessian span
is one. The example is nonconvex.

Reading the completed draft identified two minor corrections: the uniform
claim for *every* feasible witness is an exponential lower bound, since
arbitrarily large feasible witnesses exist; and the radicand-five example
in Conrad's notes is Example 5.6, not Example 5.5. Both were sent to the
author, corrected, and independently rechecked in the revised manuscript.
Neither affects the mathematical proof or the output obstruction.

## 1. All positive solutions of the base Pell equation

Put \(B=5^m y\). The equality becomes
\(x^2-5B^2=1\). Every solution with positive integers \(x,B\) is a positive
power of \(9+4\sqrt5\). Here is an elementary proof that avoids assuming the
fundamental-unit assertion.

There is no solution for \(B=1,2,3\), since \(6,21,46\) are not squares.
Thus \(B\ge4\). Multiplication by \(9-4\sqrt5\) gives integers

\[
 x'=9x-20B,\qquad B'=9B-4x,
 \qquad (x')^2-5(B')^2=1.
\]

We have \(x/B>\sqrt5>20/9\), so \(x'>0\). Also
\(x/B=\sqrt{5+B^{-2}}\le9/4\), so \(B'\ge0\). Finally,
\(x>2B\) gives \(B'<B\). Descent therefore reaches \(B'=0,x'=1\).
Reversing these steps proves the claimed parametrization. Conversely,
every positive power has positive integer coefficients and norm one.

Write

\[
 (9+4\sqrt5)^n=X_n+B_n\sqrt5,\qquad n\ge1.
\]

The sequence \(X_n\) is strictly increasing, for example from
\(X_{n+1}=9X_n+20B_n\).

## 2. The exact divisibility condition

The binomial expansion gives

\[
 B_n\equiv4n9^{n-1}\pmod5.
\]

Consequently \(5\nmid B_s\) when \(5\nmid s\). Independently expanding the
fifth power gives the exact identity

\[
 B_{5n}=5B_n\bigl(X_n^4+10X_n^2B_n^2+5B_n^4\bigr).
\]

Since \(X_n^2-5B_n^2=1\), the parenthesized factor is congruent to one
modulo five. Therefore

\[
 v_5(B_{5n})=v_5(B_n)+1,
 \qquad v_5(B_n)=v_5(n).
\]

The second identity follows by writing \(n=5^a s\) with \(5\nmid s\)
and iterating the first. Thus \(5^m\mid B_n\) holds exactly when
\(5^m\mid n\). The smallest feasible exponent is \(n=5^m\), and the
unique optimizer is

\[
 x^*=X_{5^m},\qquad y^*=B_{5^m}/5^m.
\]

In particular, feasibility and attainment hold for every \(m\ge1\).

## 3. Encoding and output length

Under the usual explicit binary encoding of integer coefficients,
\(5^{2m+1}\) has \(\Theta(m)\) bits. There are constantly many variables,
rows, and coefficients, so the complete input length is \(\Theta(m)\).
The displayed exponential notation abbreviates that binary coefficient;
the claim does not require a compressed coefficient encoding.

Put \(\alpha=9+4\sqrt5\), so \(16<\alpha<32\) and

\[
 X_n=(\alpha^n+\alpha^{-n})/2.
\]

It follows that
\(2^{4n-1}<X_n<2^{5n}\). The ordinary binary length of \(X_n\) is between
\(4n\) and \(5n\), inclusive. The optimal value therefore needs
\(\Theta(5^m)\) output bits, exponential in the input length. Every feasible
point has \(x\ge X_{5^m}\), so the same lower bound applies to ordinary
binary output of any feasible point.

The completed note's additional minimal-polynomial claim is also correct:
the optimal value has degree one over the rationals, but the constant
coefficient of \(T-X_{5^m}\) itself needs exponentially many bits. Thus
ordinary minimal-polynomial output does not remove the obstruction.

A separate reviewer independently checked the encoding and output argument
and found the stated scope correct.

## 4. What the construction does and does not show

- It rules out a polynomial total-time algorithm returning the expanded
  binary optimal value or a feasible integer point for this family.
- The objective is linear, finite, and attained. The obstruction is the
  size of the required output, without a computational hardness assumption.
- Both quadratic inequality matrices are indefinite. Their opposite signs
  encode a nonconvex equality, and the real feasible set is nonconvex and
  unbounded. The example does not refute results for convex MICP or SOCP.
- The distinction between zero continuous Hessian span and full Hessian
  span one must remain explicit.
- This does not establish decision hardness. The instances in this family
  are all feasible. It does not exclude succinct outputs such as the power
  expression above or an arithmetic circuit obtained by repeated powering.
- The argument uses standard Pell arithmetic, and the specific
  construction is already covered by the sources checked in Section 6.
  It should remain a supporting boundary with no novelty claim.

## 5. Targeted verification

Command:

```text
python research-20260927/check_two_integer_pell_output.py
```

The exact integer checks passed: the recurrence and valuation identity for
\(1\le n\le3125\); both fifth-power coefficient identities for
\(1\le n\le40\); direct searches for the least divisible exponent for
\(1\le m\le4\); feasibility, repeated-fifth-power circuit agreement, and
binary-length bounds for \(1\le m\le6\); and independent enumeration
of all positive Pell solutions with \(1\le B<200000\). The enumerated four
solutions are the first four powers of \(9+4\sqrt5\).

For \(m=1,\ldots,6\), the coefficient lengths are respectively
\(7,12,17,21,26,31\) bits; the optimal-value lengths are
\(20,104,520,2603,13017,65085\) bits. These finite computations corroborate
the proof; they do not prove the assertions for all parameters or establish
novelty. No project-wide verification or CI inspection was performed.

## 6. Independent source and circuit checks

The sources were opened and checked on 2026-09-28.

- [Lenstra, *Solving the Pell Equation*](https://wstein.org/edu/Fall2002/124/refs/lenstra_pell.pdf),
  pages 185–186, explicitly relates regulator size to binary output and
  gives a geometric-radicand family with regulator proportional to the
  square root of the radicand. The stated assumptions are that the two
  fixed integers exceed one and the first is nonsquare; choosing both
  equal to five covers this family. Pages 187–188 discuss compact
  power-product representations. The draft correctly treats the
  output obstruction and its family mechanism as classical.
- [Conrad, *Pell's Equation, I*](https://kconrad.math.uconn.edu/math3240s20/handouts/pelleqn1.pdf),
  Theorem 5.3, establishes the power parametrization. Example 5.6 gives
  the generator \(9+4\sqrt5\).
- [OEIS A298212](https://oeis.org/A298212) explicitly records the
  least-exponent identity \(a(5^m)=5^m\). This is a public prior record;
  the independent proof above does not rely on it.

The circuit coefficients in the completed draft also check exactly:

\[
 X'=X^5+50X^3B^2+125XB^4,\qquad
 B'=5X^4B+50X^2B^3+25B^5.
\]

They follow by the even and odd terms of the fifth-power binomial
expansion. Applying this constant-size update \(m\) times uses
\(O(m)\) arithmetic gates. The final exact division by \(5^m\) correctly
produces the second optimizer coordinate. These arithmetic-gate counts
do not bound the bit cost of expanding the outputs.
