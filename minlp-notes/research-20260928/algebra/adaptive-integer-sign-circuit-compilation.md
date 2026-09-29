# Removing adaptive integer sign tests with rational circuits

Date: 2026-09-28.

Status: completed derivation with a
[fresh full proof review](adaptive-closure-fresh-review.md). The rational
compressor, global error bound, denominator clearing, and explicit adaptive
interpreter have been independently checked. No
novelty claim is made. This is a supporting complexity observation, not a new
MINLP algorithm or an ordinary polynomial-time decision procedure.

## Statement and scope

Let a circuit of size at most \(S\geq1\), counting its input and constant
vertices as well as operation vertices, use constants \(0,1\), Boolean
inputs, binary arithmetic gates \(+, -, \times\), and unary gates
\[
 H(v)=\begin{cases}1&v>0,\\0&v\leq0.\end{cases}
\]
Assume its designated output is Boolean on Boolean inputs. All its exact
intermediate values are integers, including values that depend on previous
sign tests.

**Proposition.** In time polynomial in \(S\), one can construct a
division-free integer arithmetic circuit with the same Boolean input
variables whose output is positive exactly when the original circuit outputs
one. Its size is \(O(S^2)\). The construction is uniform and does not query a
sign oracle.

The proposition concerns a finite integer circuit with threshold gates. It
does not remove discontinuities on arbitrary real inputs. The unit separation
between distinct integers is essential to this proof.

## A range compressor

Put \(M_j=2^{2^j}\), so \(M_0=2\) and \(M_{j+1}=M_j^2\). These
constants have a shared arithmetic circuit of linear size in the largest
index.

For \(M\geq1\), define
\[
 F_M(x)=\frac{2Mx}{M+x^2}.
\]
Its denominator is positive everywhere. If \(1\leq |x|\leq M\), then
\[
 1\leq |F_M(x)|\leq\sqrt M,
 \qquad \operatorname{sgn}F_M(x)=\operatorname{sgn}x.
\]
Indeed, for \(t=|x|\), the lower bound is equivalent to
\(t^2-2Mt+M\leq0\). The left side is convex, and its values at the
endpoints \(1,M\) are \(1-M\) and \(M-M^2\). The upper bound follows
from \(M+t^2\geq2\sqrt M\,t\).

Consequently the composition with parameters
\(M_J,M_{J-1},\ldots,M_1\) maps signed magnitudes in \([1,M_J]\) into
signed magnitudes in \([1,2]\), using \(J\) rational steps.

## Accurate sign approximation

Define
\[
 G(x)=\frac{2x}{1+x^2}.
\]
Applied to signed magnitudes in \([1,2]\), it gives magnitudes in
\([4/5,1]\). For \(0\leq t\leq1\),
\[
 1-G(t)=\frac{(1-t)^2}{1+t^2}\leq(1-t)^2.
\]
Thus after \(r\geq1\) applications of \(G\), the error from the correct
sign is at most
\[
 2^{-2^{r-1}}.
\]
The bound uses only that the error after the first step is below \(1/2\).
Converting the result \(z\) to \((1+z)/2\) halves this error and produces
a value in \([0,1]\).

## Global error budget

Every exact circuit value has magnitude at most
\[
 B=2^{2^S}.
\]
This follows by starting with the bound \(2\): each arithmetic gate can
at most square the preceding bound, since \(2b\leq b^2\) for \(b\geq2\),
and threshold gates output zero or one.

Set
\[
 L=3B,\qquad \varepsilon=2^{-2^{2S+4}}.
\]
Then
\[
 \varepsilon L^S<\tfrac14. \tag{1}
\]
For completeness, \(\log_2L\leq2^S+2\), whereas
\(2^{2S+4}>2+S(2^S+2)\) for \(S\geq1\).

Replace each arithmetic gate by the same operation on the approximate
inputs. Replace a threshold gate with exact integer input \(v\) and
approximate input \(\widetilde v\) as follows:

1. Form \(x=4\widetilde v-2\).
2. Apply \(F_{M_{S+2}},F_{M_{S+1}},\ldots,F_{M_1}\).
3. Apply \(G\) exactly \(2S+5\) times.
4. Return \((1+z)/2\).

Provided \(|\widetilde v-v|\leq1/4\), integer separation gives
\[
 \begin{aligned}
 v\geq1&\Longrightarrow x\geq1,\\
 v\leq0&\Longrightarrow x\leq-1.
 \end{aligned}
\]
Also \(|x|\leq4B+3\leq B^4=M_{S+2}\). Hence the replacement is
well defined and approximates \(H(v)\) with absolute error at most
\(\varepsilon\).

Order the original gates topologically. Inductively, after gate \(i\), the
maximum error among constructed original-gate values is at most
\(\varepsilon L^i\). Exact inputs have zero error. At an arithmetic gate,
write \(\delta\) for the preceding maximum error. Addition and subtraction
amplify it by at most two. Multiplication amplifies it by at most
\[
 2B\delta+\delta^2\leq(2B+1)\delta\leq L\delta,
\]
because the induction and (1) ensure \(\delta<1\). At a threshold gate,
the preceding error is below \(1/4\), so the replacement error is at most
\(\varepsilon\), as just proved. Previously constructed values continue to
satisfy the new, weaker bound.

The approximate output is therefore below \(1/4\) if the exact output is
zero and above \(3/4\) if it is one. Testing it against \(1/2\) determines
the answer.

## Division-free compilation and size

Represent each approximate rational value by integer arithmetic circuits
\(P,Q\) with \(Q>0\), denoting \(P/Q\). Addition, subtraction, and
multiplication use the usual common-denominator formulas, preserving positive
denominators. In particular,
\[
 F_M(P/Q)=\frac{2MPQ}{MQ^2+P^2},
 \qquad
 G(P/Q)=\frac{2PQ}{Q^2+P^2}.
\]
Both displayed denominators are strictly positive because \(Q>0\) and
\(M>0\). Converting \(z\) to \((1+z)/2\) also preserves positivity.
These are constant-size operations on the pair representation; existing
subcircuits are shared, not copied as formula trees. No actual division gate
is needed in the final circuit.

There are \(O(S)\) compressor steps for each of at most \(S\) threshold
gates. The shared constants and the other arithmetic gates add only linear
size. If \(P/Q\) is the final approximate Boolean output, output the integer
\(2P-Q\). Its positivity is equivalent to the original answer. This proves
the proposition.

## Application to polynomial-time adaptive PosSLP queries

The usual circuit simulation of a polynomial-time oracle Turing machine can
be made explicit here. Suppose its running time and maximum query length
are at most \(T\), polynomial in the ordinary input length. Unroll its
Boolean configurations for \(T\) steps. At every step, allow a query module;
if no oracle call occurs, its answer is ignored. All ordinary Boolean logic
can be expressed with integer arithmetic gates: \(ab\), \(1-a\), and
\(a+b-ab\) implement AND, NOT, and OR on exact bits.

A query module evaluates a possibly variable SLP description of length at
most \(T\) using a polynomial-size arithmetic circuit:

- Parse and validate the description with a Boolean circuit. A malformed
  description is assigned the ordinary negative answer.
- Reserve polynomially many instruction slots. For each slot, compute
  Boolean indicators for the opcode and for its operand addresses.
- Select each operand by a sum of its previously computed slot values
  multiplied by the corresponding address indicators. Force invalid or
  unavailable addresses to select zero, so evaluation is defined even on
  malformed descriptions.
- Compute the candidate sum, difference, and product, and select the
  indicated opcode by Boolean multiplication and addition.
- Select the output slot in the same way, apply one threshold gate, and
  conjoin its answer with the validity bit.

There are polynomially many slots and possible addresses, so this is a
polynomial-size construction. It enumerates possible addresses, not possible
oracle-answer transcripts. This distinction avoids exponential branching.
Any standard explicit binary encoding of acyclic SLPs admits this bounded
interpreter; delimiters, lengths, and padding are ordinary Boolean parsing
issues. Every exact intermediate value is an integer.

The resulting arithmetic-and-threshold circuit has size polynomial in
\(T\), even when later query descriptions depend on earlier answers. Apply
the proposition and hardwire the ordinary input bits. This gives a
polynomial-time many-one reduction from the language accepted by the oracle
machine to PosSLP.

Thus the derivation gives many-one completeness of PosSLP for
\(\mathrm P^{\mathrm{PosSLP}}\). This is a closure statement about reductions,
not a polynomial-time algorithm for PosSLP or a collapse to ordinary
\(\mathrm P\). Its status in the literature requires a fuller prior audit
before presenting it as anything beyond an explicit consequence of known
rational approximation methods.

## Prior results, checks, and limitations

The [companion Boolean-closure audit](posslp-boolean-closure-audit.md)
identifies the compressor as a scaled instance of the classical
inverse-Newton sign iteration, and records primary sources for both that
iteration and rational-function composition. The scale schedule, exact
integer separation, and error budget are stated explicitly here; the
numerical iteration itself is not claimed as new.

Allender, Bürgisser, Kjeldgaard-Pedersen, and Miltersen,
[*On the Complexity of Numerical Analysis*](https://epubs.siam.org/doi/10.1137/070697926),
state the Turing-oracle characterization
\(\mathrm P^{\mathrm{PosSLP}}=\mathrm{BP}(\mathrm P^0_\mathbb R)\).
Section 3 also discusses very accurate rational approximations computed by
short straight-line programs and cites Kung and Traub, *All algebraic
functions can be computed fast*, JACM 25 (1978), 245–260. The repository's
[2009 full text](../../literature/papers/allender2009-on-the-complexity-of-numerical/fulltext.md)
was examined at the approximation paragraph and reference 46. That paragraph
is a strong reason to regard efficient sign compression as established
approximation machinery rather than claim novelty from this elementary
construction. The exact adaptive closure formulation above has not yet been
located in a source.

The proof gives a concise exact representation; its numerator and denominator
can have exponentially many bits. Evaluating them explicitly may therefore
be expensive. No solver speedup follows from the representation theorem
alone. For applications that already permit adaptive PosSLP queries, the
observation changes the reduction form, not the ordinary computational
complexity.

Independent adversarial review checked the compressor, error propagation,
positive-denominator elimination, and universal-interpreter step. It found no
mathematical gap and emphasized that decoder, selector, and control gates
must count toward the original circuit size. A review is evidence, not formal
verification.

A [fresh cross-branch review](adaptive-closure-fresh-review.md) independently
rechecked the complete argument, including variable oracle-query descriptions,
and found no gap. Its requested binary-gate convention is now explicit above;
the gate-height recurrence and size count both use that convention. The
[deeper primary-source audit](posslp-prior-deep.md) identifies Balaji's
extended-basis sign-gate model as a close predecessor. It also establishes
that SQRT-SUM many-one reducibility already follows from earlier PPS results;
that consequence must not be presented as a newly resolved open problem.
The generic closure statement's publication priority remains unestablished.

The targeted command actually run was
`python research-20260928/algebra/check_adaptive_sign_compilation.py`.
It passed 3,003 exact rational samples of the compressor range bound, 100
integer instances of the error-budget inequality, and 25 exact rational
refinement checks. An earlier inline Python run performed the same checks
and verified that the local literature link resolves. These finite checks
can expose arithmetic mistakes; they do not establish the universal bounds
or implement the adaptive query compiler. Subsequent
[targeted Lean verification](formal-coverage.md) proves local compression,
refinement, threshold-margin, and product-error lemmas. It does not
formalize the full schedule, global error induction, integer circuit
semantics, compiler, DAG size, adaptive interpreter, or closure conclusion.
No project-wide checks or CI inspection was performed for this note.

A subsequent [reference implementation and verification record](sign-compiler-reference-verification.md)
constructs the actual shared integer DAG. Selected small circuits were
evaluated exactly with the full proof schedule, while larger schedules
were checked for construction size without expanding their integers.
Additional tests deliberately shorten the schedule; those are diagnostic
only, and the record includes a counterexample to their universal validity.
The implementation counts operation gates separately from source-description
length. The total-size convention above absorbs that distinction in the
stated polynomial-time theorem.
