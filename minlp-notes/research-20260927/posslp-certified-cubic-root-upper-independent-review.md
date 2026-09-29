# Independent review of the PosSLP upper bound for certified cubic roots

Date: 2026-09-28. Status: the frozen proof passes independent
adversarial review. No substantive defect or needed correction was found.

The reviewed [upper-bound note](posslp-certified-cubic-root-upper.md)
has SHA256
3049dd0c34ac35bbe3d06c4832d213df4384d1d28acb5591ba722ccc7b2cc40f.
This reviewer did not contribute to its construction. The audit
independently reconstructs the algebraic separation, Newton iteration,
propagation, single-comparison reduction, and circuit size. It also
checks the scope of the cited methodological precedent. It does not
establish publication priority for the restricted circuit classification.

## Common denominator and algebraic separation

Let \(D\) be the product of the printed denominators of all gate
coefficients and the rational threshold. The input convention gives
\(D\le2^L\). Multiplying every root by the same \(D\) is enough:

\[
 (D\xi_i)^3
 =D^3c_i+\sum_{j<i}
       \bigl(D^2a_{ij}(D\xi_j)+Db_{ij}(D\xi_j)^2\bigr).
\]

All displayed scalar coefficients are integers. For example, the
quadratic term only requires \(Db_{ij}\) integral. Each new scaled
root satisfies a monic polynomial over the ring of previously obtained
algebraic integers. Integrality over that ring, followed by transitivity
of integrality, proves that every \(D\xi_i\) is an algebraic integer.
There is no need to multiply by an increasingly large scale at each
gate.

Each new root has degree at most three over the preceding field.
Thus the degree of \(K=\mathbb Q(\xi_1,\ldots,\xi_n)\) is at most
\(3^n\), even if some gate polynomials factor. For every complex
embedding of \(K\), the gate equations remain valid. With
\(M=(2L+1)2^L\ge1\), the induction estimate is

\[
 |c_i+\sum(a_{ij}\xi_j+b_{ij}\xi_j^2)|
 \le2^L(1+LM+LM^2)
 \le(2L+1)2^LM^2=M^3.
\]

Consequently all conjugate coordinates have modulus at most \(M\).
This uses absolute values and tolerates arbitrary coefficient signs
and cancellations. The supplied real intervals are not used as
bounds on complex conjugates.

Because \(Dr\) is an integer, \(\beta=D(\xi_o-r)\) is integral.
If \(\xi_o\ne r\), it is nonzero, every embedding sends it to a
nonzero number, and its field norm is a nonzero integer. The actual
real embedding is one factor of the norm. Every other factor is at
most

\[
 D(M+|r|)\le2^{4L+1}.
\]

Dividing by \(D\) gives exactly

\[
 |\xi_o-r|
 \ge2^{-L-(4L+1)(3^L-1)}
 \ge2^{-2^{6L}}=g.
\]

The last replacement is conservative. The elementary estimates in the
note hold for every integer \(L\ge2\), and the exponent on the first
bound is already at most \(2^{4L}\). The bound is expressly conditional
on a nonzero difference; the equality case is handled later rather
than excluded without a test.

The number \(g\) is represented by \(6L\) squarings of \(1/2\).
Neither its expanded denominator nor the field \(K\) is computed.

## Newton iteration

For \(z>0\), let \(\eta=z^{1/3}\). The initialization
\(x_0=2^{L+1}\) is at least \(\eta\) whenever
\(\eta\in[2^{-(L+1)},2^{L+1}]\). Writing \(x_t=\eta(1+e_t)\)
in the exact rational update yields

\[
 e_{t+1}
 =\frac{e_t^2(3+2e_t)}{3(1+e_t)^2}.
\]

In particular, \(e_t\ge0\) is preserved. The two upper bounds follow
from the exact nonnegative differences

\[
 e^2-\frac{e^2(3+2e)}{3(1+e)^2}
 =\frac{e^3(4+3e)}{3(1+e)^2},
\]

\[
 \frac23e-\frac{e^2(3+2e)}{3(1+e)^2}
 =\frac{e(e+2)}{3(1+e)^2}.
\]

Initially \(e_0\le2^{2L+2}\). After \(4L+6\) steps,
\((2/3)^2<1/2\) makes the relative error at most \(1/2\).
The next \(10L\) steps square that error repeatedly. Multiplying by
\(\eta\le2^{L+1}\) gives the stated absolute error
\(\varepsilon=2^{L+1-2^{10L}}\).

All divisions are legitimate: the initial iterate and each radicand
are positive, and the iteration preserves positive iterates.
The construction prints the arithmetic operations, without evaluating
their potentially enormous rational numerators and denominators.

## Error propagation and its bootstrap

The positive certified intervals give
\(2^{-L}\le\xi_i\le2^L\). If the predecessor error is at most one,
then \(|\widehat\xi_j|\le2^{L+1}\). Thus

\[
 |\widehat\xi_j^2-\xi_j^2|
 \le3\cdot2^L|\widehat\xi_j-\xi_j|.
\]

Summing signed radicand errors by absolute values gives
\(L(2^L+3\cdot2^{2L})E_{i-1}\le2^{4L}E_{i-1}\).
For example, the last inequality follows from
\(L(3+2^{-L})\le4L\le4^L\).

If \(E_{i-1}\le2^{-7L-1}\), the perturbed radicand differs from
the true one by at most \(2^{-3L-1}\). Its lower bound is then
\(2^{-3L-1}>0\). Its upper bound is at most
\(2^{3L}+2^{-3L-1}<2^{3(L+1)}\).
Taking cube roots places the perturbed root in the interval required
for Newton initialization. The cube-root derivative on the intervening
positive segment is at most \(2^{2L+2}\).

Combining the radicand error, derivative bound, and Newton error gives

\[
 E_i\le2^{6L+2}E_{i-1}+\varepsilon.
\]

This also bounds older errors, so it applies to the maximum over all
completed gates. Starting from \(E_0=0\), the geometric bound
\(E_i\le2^{(6L+3)i}\varepsilon\) follows.
For \(i\le L\), its exponent is at most

\[
 6L^2+4L+1-2^{10L}.
\]

The note's inequalities make this at most both \(-7L-1\) and
\(-2^{6L}-3\). For completeness, \(2^{6L}\ge20L^2\) follows
from its value at \(L=2\) and induction: the exponential grows
by a factor 64, while the squared term grows by at most \(9/4\).
The inequality \(6L^2+11L+5\le20L^2\) is immediate for \(L\ge2\);
the remaining exponential difference is larger still.

This is a valid induction, not a circular use of positivity:
the bound at stage \(i-1\) permits that stage's perturbed-radicand
argument, and the resulting bound at stage \(i\) again lies in the
required range. It also gives \(E_n\le g/8\).

## Equality, denominator signs, and output size

The output \(q=\widehat\xi_o-r-g/2\) has the following bounds:

\[
 \begin{array}{c|c}
 \xi_o>r & q\ge3g/8>0\\
 \xi_o=r & q\le-3g/8<0\\
 \xi_o<r & q\le-11g/8<0 .
 \end{array}
\]

Only the unequal cases use norm separation. The downward shift handles
equality directly, so no zero test or branching oracle is hidden in
the construction. For a weak comparison, an upward shift works by the
same calculation.

Represent every rational value as \(N/D\) with \(D>0\), retaining
shared numerator and denominator circuits. For a nonzero divisor,

\[
 \frac{N_a/D_a}{N_b/D_b}
 =\frac{N_aD_bN_b}{D_aN_b^2}.
\]

The new denominator is strictly positive because \(N_b\ne0\).
The formula works for positive and negative divisors, with no sign
query. Addition, subtraction, and multiplication likewise take only
constantly many new integer arithmetic gates per rational gate.
Input integer constants are constructed from zero and one using their
binary expansions.

There are \(O(L)\) Newton steps per root and at most \(L\) roots.
Explicit radicand evaluation and certificate checking are polynomial
in the printed input. Reusing shared subcircuits keeps the total
integer circuit polynomial in size. No expanded rational intermediate
is computed, and no oracle is called when printing the reduction.
For an invalid certificate, the fixed negative output implements
rejection. The final numerator alone is the required PosSLP instance.

## Prior work and exact scope

The source's methodological attribution is accurate. Section 1.4 of
[Allender, Bürgisser, Kjeldgaard-Pedersen and Miltersen](https://people.cs.rutgers.edu/~allender/papers/slp.pdf)
explicitly connects Newton circuits of high precision with the
sum-of-square-roots reduction. Proposition 1.1 discusses numerator and
denominator simulation; Proposition 1.3 also separates rational
numerators and denominators. The passage before Theorem 3.9 describes
small rational circuits for algebraic-function approximation. These
were inspected directly. They support the classical-method
characterization; they do not by themselves state this exact nested
cubic language with its interval certificates. Tiwari's original
article was not inspected in this review.

The [Radical Identity Testing abstract](https://arxiv.org/abs/2202.07961)
defines equality testing for a circuit polynomial evaluated at
individually specified radicals of integers. That confirms the stated
distinction from nested root gates and a sign question. Its algorithms
are not used in the proof under review.

Together with the independently reviewed lower bound, the theorem
classifies the specified certified positive cubic-root comparison
language as PosSLP-complete under deterministic polynomial-time
many-one reductions. It gives no upper bound for general convex
quartic feasibility, and no claim that PosSLP is NP-hard. The upper
proof's usefulness is the matching classification; its main method is
classical, as the author states.

## Exact checks and remaining limits

The focused command

~~~text
python research-20260927/check_posslp_upper_independent_review.py
~~~

passed. Its exact symbolic calculations verify Newton's relative-error
identity, both nonnegative difference formulas, and the
denominator-positive division identity. Exact integer calculations
check the displayed size and error margins for \(2\le L\le128\).
Those finite checks supplement the universal arguments above; they
do not prove algebraic integrality, norm separation, or the all-input
induction by themselves.

The proof was not formalized in Lean. No project-wide verification or
CI inspection was run. An attempted additional independent subreview
was unavailable because the agent thread limit had been reached.
This review found no hidden expansion of field representations or
high-precision rationals, and no unhandled threshold-equality case.

## Reconciliation of the final status update

The final source has SHA256
127752cd4b65fe3b88bd104e28cc11e87ecece32959b263a79366dfa6b8738b6.
The reviewed changes update the proof status, remove the completed
review condition from the restricted-language classification, and
record the actual checker command and its limits. These changes pass
scoped reconciliation. The mathematical construction and quantitative
bounds are unchanged.
