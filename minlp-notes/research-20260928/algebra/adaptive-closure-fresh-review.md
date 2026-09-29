# Fresh adversarial review of PosSLP closure compilation

Date: 2026-09-28.

Reviewed independently from the author: [adaptive integer sign compilation](adaptive-integer-sign-circuit-compilation.md) and [Boolean closure](posslp-boolean-closure-audit.md). This review checks the arguments as written and the reduction model. It is not a formal proof or a determination of priority.

**Verdict:** I found no mathematical error in either compiler under the stated Boolean-input, integer-intermediate, arithmetic-DAG assumptions. In particular, the adaptive proposition does imply polynomial-time many-one completeness of PosSLP for `P^PosSLP`. The decoder and control logic can be made polynomial size without enumerating oracle transcripts. This is a stronger reduction-form statement than the generic oracle simulation in the principal sources inspected. Its originality remains unestablished. The square-root-sum many-one consequence, however, already follows from older problem-specific results; it should not be presented as a new consequence in the literature.

## 1. Magnitude and precision audit

The compressor is valid on its entire claimed domain. For `t` in `[1,M]`,

\[
2Mt-(M+t^2)=(t-1)(M-t)+(M-1)t\ge0.
\]

The upper bound follows from `M+t^2 >= 2 sqrt(M) t`. Positivity of the denominator establishes sign preservation, including the endpoints `M=1` and `t=1`. No assumption that the compressor is monotone in `t` is needed; it is not globally monotone on this interval.

The schedule is aligned correctly: `sqrt(M_j)=M_{j-1}`. Starting at index `J`, exactly `J` applications with indices `J,...,1` therefore reach magnitude at most `M_0=2`. Each stage retains magnitude at least one. Neither square roots nor the expanded binary representations of `M_j` are used by the circuit.

For the refinement map, the first application takes magnitude in `[1,2]` to `[4/5,1]`. Thereafter,

\[
1-\frac{2t}{1+t^2}=\frac{(1-t)^2}{1+t^2}\le(1-t)^2
\quad(0\le t\le1).
\]

Thus the stated bound `2^(-2^(r-1))` after `r` steps is conservative. The final affine conversion halves the error. With `r=2S+5`, it therefore gives error at most the stated `epsilon`, with an additional factor of two available.

The original circuit bound `B=2^(2^S)` uses the standard convention that arithmetic gates have fan-in two and counts *all* original arithmetic and threshold gates. This gate convention should be made explicit in the proposition; allowing unbounded fan-in at unit size would not justify the displayed height bound. Starting with two as a bound, each gate at most squares the preceding bound: addition and subtraction use `2b <= b^2`, multiplication uses `b^2`, and threshold outputs are bits. This also bounds scratch values in an interpreter, including candidates that are subsequently multiplied by zero.

The global error argument survives adversarial cancellation and reuse of a wire. If exact multiplication inputs are bounded by `B` and both approximation errors by `delta`, then

\[
|(a+e)(b+f)-ab|\le 2B\delta+\delta^2.
\]

This does not assume independent input errors. In particular, it also applies to a squaring gate whose two inputs are the same circuit wire. For `delta<1`, this is at most `3B delta`. Cancellation at a subtraction gate does not introduce a relative-error requirement: the proof consistently uses absolute errors.

The threshold shift handles zero correctly. For an integer `v` and `|v_tilde-v| <= 1/4`, the value `4 v_tilde-2` belongs to `[1,infinity)` if `v>=1`, and to `(-infinity,-1]` if `v<=0`. The exact zero case is therefore safely on the negative side. Also `|4 v_tilde-2| <=4B+3 <=B^4=M_(S+2)`; the smallest permitted case `S=1` already has `B=4`.

The exponent inequality is amply sufficient:

\[
\log_2(\varepsilon L^S)
\le-2^{2S+4}+S(2^S+2)<-2.
\]

Therefore the induction can assume the required `1/4` input margin at every threshold gate. This is not circular: at gate `i`, the preceding maximum error is bounded using the induction hypothesis, and the global numerical inequality holds for every index up to `S`.

The proof does not approximate every internal numerator or denominator numerically. It constructs them exactly as a circuit. The large conditioning of an expanded rational representation consequently does not invalidate this symbolic argument. It would matter to a proposed floating-point implementation, which is outside the theorem.

## 2. Rational representation and output size

Every represented rational has a positive denominator. At a compressor step the new denominator is

\[
MQ^2+P^2>0,
\]

since `M>0` and `Q>0`; at refinement it is `Q^2+P^2>0`. Addition, subtraction, multiplication, and the final affine conversion preserve positive denominators. Thus the final test of `2P-Q` has the asserted direction and never silently reverses an inequality.

The construction must use a DAG. Each pair update adds a constant number of integer gates that reference previously constructed outputs. It does not substitute the entire previous expression twice. Under this representation there are `O(S)` steps per threshold gate and at most `S` such gates. The shared constants use `O(S)` additional gates, so the claimed `O(S^2)` gate count is correct. Binary gate-address encoding adds logarithmic factors to the bit length, leaving a polynomial-time reduction.

No huge binary constant is hidden in the output description: two is made from `1+1`, and successive `M_j` use repeated squaring. The error parameter is an analytic budget; its expanded binary representation need not be generated. Expanding either the circuit into a formula or its output into binary would invalidate the size argument, but neither operation is part of the claim.

The designated Boolean-output hypothesis is used only for the final separation from `1/2`. If a source computation instead ends by asking whether an integer arithmetic output is positive, appending one threshold gate restores this hypothesis.

## 3. Adaptive query interpretation

The interpreter is the part most likely to hide an exponential expansion. The described construction avoids it.

For an explicit standard encoding, reserve `T` instruction slots for a query of length at most `T`. Let `e_(j,i)` be the Boolean equality test between the first address field of instruction `j` and the constant address `i`. Equality to a fixed `O(log T)`-bit address has a Boolean circuit of that size. The selected operand is

\[
A_j=\sum_{i<j}e_{j,i}V_i.
\]

The other operand `B_j` has the same form. Opcode indicators select among `0`, `1`, `A_j+B_j`, `A_j-B_j`, and `A_j B_j`. All these operations are division-free and defined even when a malformed address selects no previous instruction. A separate validity bit rejects malformed encodings. Variable-length encodings can first be parsed into bounded slots by an ordinary polynomial-time Boolean parser, then converted to a Boolean circuit.

This enumerates polynomially many *addresses*, not exponentially many executions. There are `O(T^2)` address candidates per module, with polynomial parsing and decoder overhead. A module at each of `T` unrolled machine steps still has polynomial total size. Binary constants, if allowed by the chosen query syntax, can alternatively be built from their explicit bits using shifts implemented by doubling and addition; their total bit length is bounded by the query length.

The Turing-machine configuration updates and the parser are exact Boolean circuits before sign elimination. AND, NOT, and OR translate into integer arithmetic by `ab`, `1-a`, and `a+b-ab`. Query answer bits may affect later parsing, opcodes, operand addresses, and branch control. These dependencies do not require a new proof after compilation: every such intermediate is an integer in the exact source circuit, and every arithmetic gate is already included in the global absolute-error induction. Approximate decoder outputs need not themselves be exact bits.

An inactive query module can be evaluated and ignored. A malformed query returns the agreed negative answer by multiplication with the validity bit. Because there are no division gates in the interpreter, neither case causes an undefined intermediate. Halted configurations can similarly retain their halting answer while the unrolling continues.

Finally, construct this circuit for the fixed oracle machine and the input length, count its actual gates to obtain `S`, apply the compiler, and hardwire the ordinary input bits. The reduction writes a polynomial number of gate records and never evaluates the large integer values or invokes PosSLP. This establishes the claimed many-one reduction for each language in `P^PosSLP`.

## 4. Independent check of the Boolean-only lemma

The shifted query outputs `2a_i-1` are nonzero integers with the required sign. The size bound `N=n+2` safely contains their magnitudes, including constant-only input circuits.

For normalized `u,v`, the AND and OR formulas have the exact interval margins listed in the note. Mixed signs give `u+v` in `[-1,1]`; this is the potentially adverse case, and the shifts by three leave magnitude at least one. Both operations have magnitude at most eleven. Applying `F_16` and `F_4` restores `[1,2]` in magnitude. The pair formulas use the positive product of input denominators. Boolean NOT simply negates the numerator. There is therefore no hidden depth-dependent loss of margin.

The Boolean-only result does not logically imply the adaptive result: later adaptive queries can encode different arithmetic circuits, so their values are not a fixed polynomial list of independently known input circuits. The universal evaluator and the absolute-error simulation supply the missing step.

## 5. Literature findings and novelty limits

The following primary texts were examined on 2026-09-28. Bibliographic website metadata occasionally disagrees with the actual PDF; the author names and statements below follow the papers themselves.

- Allender, Bürgisser, Kjeldgaard-Pedersen, and Miltersen, [*On the Complexity of Numerical Analysis*](https://people.cs.rutgers.edu/~allender/papers/slp.pdf), 2009. The local full text was inspected at Proposition 1.1 and the discussion of efficient rational approximation before Theorem 3.9. Proposition 1.1 gives the oracle characterization and implements machine branches by PosSLP calls. It does not eliminate those calls in its proof. The approximation discussion is relevant methodologically, but it does not explicitly establish the adaptive compiler reviewed here.

- Etessami and Yannakakis, [*Recursive Markov Chains, Stochastic Grammars, and Monotone Systems of Nonlinear Equations*](https://homepages.inf.ed.ac.uk/kousha/final_rmc_jacm_version.pdf), JACM 2009, printed pp. 5–6 and the reductions in Section 5. This version explicitly distinguishes the known Turing reduction from square-root sum to PosSLP from a then-unknown many-one reduction. It also supplies direct many-one reductions from square-root sum to quantitative 1-exit RMC/PPS thresholds. The historical absence of a many-one reduction is not evidence that it remains absent today.

- Etessami, Stewart, and Yannakakis, [*A Polynomial Time Algorithm for Computing Extinction Probabilities of Multi-type Branching Processes*](https://www.pure.ed.ac.uk/ws/portalfiles/portal/29051677/revised_sicomp_sub_after_rev_august16_v3_1.pdf), 2017, Corollary 6.6 and its proof, printed pp. 34–36. This source explicitly gives polynomial-time many-one reductions from PPS coordinate comparisons to PosSLP using a fixed number of Newton iterations and numerator/denominator circuits. Together with the previous paper, this already yields a many-one square-root-sum reduction. Strict versus weak inequalities cause no obstacle: if an integer circuit output `N` represents the strict comparison, its complement is represented by `1-N`, since `N<=0` exactly when `1-N>0`. The proof carefully distinguishes the generic oracle characterization from its problem-specific circuit construction. It does not state a compiler for arbitrary adaptive oracle machines.

- Bürgisser and Jindal, [*On the Hardness of PosSLP*](https://goravjindal.github.io/assets/pdf/posslpsoda2024.pdf), SODA 2024, introductory Proposition 1.1 and Problem 1.2. These restate the oracle characterization and the Turing equivalence for the generic numerical-computation task. They do not settle whether a stronger adaptive-closure theorem exists elsewhere.

- Bläser, Dörfler, and Jindal, [*PosSLP and Sum of Squares*](https://goravjindal.github.io/assets/pdf/SoSposslp2024.pdf), FSTTCS 2024, introductory Theorems 1.1–1.2. These likewise state the Turing characterization. The paper distinguishes many-one from Turing reductions elsewhere, so the terminology is deliberate, but its choice of statement does not prove that adaptive many-one closure is open.

- Bodirsky, Loho, and Skomra, [*Reducing Stochastic Games to Semidefinite Programming*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol334-icalp2025/LIPIcs.ICALP.2025.145/LIPIcs.ICALP.2025.145.pdf), ICALP 2025, pp. 145:2–145:3. Figure 1 was visually inspected: square-root sum to PosSLP is a **solid** arrow, denoting a many-one reduction. The dotted Turing arrow is between stochastic games. This is consistent with the earlier problem-specific results, and supplies no general adaptive-closure theorem.

Searches included `"PosSLP" "many-one" "Turing"`, `"PosSLP" "adaptive"`, `"PosSLP" "closed under" "Turing"`, `"PosSLP" "Karp"`, `"PosSLP" "Cook reductions"`, `"PosSLP" "many-one complete"`, `"PosSLP" "sign gates"`, `"PosSLP" "sign function"`, and `"PosSLP" "rational approximation"`. No directly matching general closure theorem was located. This is a limited literature search, not proof of novelty or proof that a stated open question has been resolved for the first time.

## 6. Significance and remaining work

If the proof is accepted, its precise contribution is a uniform removal of all intermediate integer sign tests with polynomial growth in arithmetic-circuit size, and the corresponding strengthening from adaptive oracle reductions to a single PosSLP instance. The given construction appears to establish that claim, rather than merely suggest it.

This does not improve the known ordinary decision-time bound for PosSLP, produce short expanded integer witnesses, or establish a numerical speedup. It also does not transfer arbitrary oracle reductions *to a different target oracle*, such as 3SoSSLP: the closure argument specifically exploits the arithmetic and sign structure of PosSLP.

For MINLP, the relevant possibility is to compile a polynomial arithmetic decision procedure with adaptive exact comparisons into one succinct comparison, when integer separation is available. Applications still require a solver formulation or algorithm that benefits from this representation. No such improvement follows merely from many-one completeness. Classical rational sign approximation should be credited, and the reduction-form statement needs a broader priority audit before an originality claim.

This review used direct analytic checks and primary-source inspection. It did not rerun the author's finite rational sample tests, implement an end-to-end universal query compiler, or formally verify the induction. Those existing finite tests do not establish the adaptive interpreter construction. No project-wide checks or CI inspection were performed. The only new repository file is this review. Targeted command: `git diff --no-index --check /dev/null research-20260928/algebra/adaptive-closure-fresh-review.md`. It returned no whitespace diagnostics (exit status 1 for a new-file diff).
