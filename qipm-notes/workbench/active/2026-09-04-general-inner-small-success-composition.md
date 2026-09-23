# General-inner small-success composition

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem; moderate on novelty  
Question: Does the small-success winner-finding lower bound extend from parity
to an arbitrary inner predicate?

## Result

Let \(f:\mathcal X_0\sqcup\mathcal X_1\to\{0,1\}\) be a nonconstant,
possibly partial Boolean predicate, and put

\[
 A=\operatorname{Adv}^{\pm}(f)=\Theta(Q(f)).
\]

There are \(G\) independent input blocks, and one raw query addresses one
coordinate of one block. Suppose a \(T\)-query circuit, on every input with
exactly \(k\) positive blocks, outputs a label \(g\in[G]\) with

\[
 \Pr[f(x_g)=1]\geq\delta.
\]

No behavior is required on zero-positive inputs. There are universal constants
\(c,C>0\) such that

\[
 \boxed{
 T\geq cA\sqrt{\delta\lfloor G/k\rfloor}-CA.
 }
\]

Equivalently,

\[
 T=\Omega\!\left(Q(f)
 \left(\sqrt{\delta\lfloor G/k\rfloor}-1\right)\right).
\]

When \(\delta G/k\) is at least a sufficiently large constant, this is

\[
 T=\Omega\!\left(\sqrt\delta\,Q(f)\sqrt{G/k}\right).
\]

The subtractive \(O(Q(f))\) term is necessary. This closes open problem A2 in
the current paper on the natural nontrivial parameter range.

## Proof

Put \(M=\lfloor G/k\rfloor\). Reduce the promise problem
\(\operatorname{UniqueOR}_M\circ f\), whose input has zero or exactly one
positive \(f\)-block, to the proposed finder. Replace each source block by
\(k\) addressable copies and fill the fewer than \(k\) unused positions with a
fixed public element of \(\mathcal X_0\). One query to a copy is simulated by
one query to the source. On a unique-positive source input, the finder is
therefore a \(T\)-query candidate generator whose true-candidate probability is
at least \(\delta\).

Choose a coherent bounded-error verifier for \(f\) of cost
\(q=O(Q(f))=O(A)\). The imperfect-verifier amplification construction of
Høyer--Mosca--de Wolf turns a candidate generator of success
\(s\geq\delta\) into a constant-error existence test with

\[
 O((T+q)/\sqrt\delta)
\]

queries. Its recurrence is

\[
 C_{j+1}=3C_j+O(jq),\qquad C_1=T+q,
\]

so \(C_j=O(3^j(T+q))\). Level \(j\) handles
\(s\in[9^{-(j+1)},9^{-j}]\); trying the geometrically increasing levels
through \(\lceil\log_9(1/\delta)\rceil+O(1)\) has the displayed total cost.
The proof uses only the true- and false-positive amplitudes, not a uniform
candidate-label distribution.

For completeness, the composite decision lower bound has a direct adversary
witness. Let \(B\), indexed by the zero and one fibers of \(f\), satisfy

\[
 \|B\|=A,\qquad \max_j\|B\circ\Delta_j\|\leq1.
\]

Between the all-zero sector and the sector whose unique winner is block \(a\),
put

\[
 C_a=I_0^{\otimes(a-1)}\otimes B\otimes
 I_0^{\otimes(M-a)},\qquad C=[C_1\ \cdots\ C_M].
\]

Then

\[
 CC^*=\sum_{a=1}^M I_0^{\otimes(a-1)}\otimes BB^*\otimes
 I_0^{\otimes(M-a)},
\]

whose commuting tensor summands give \(\|C\|=A\sqrt M\). Filtering by a raw
query to coordinate \((a,j)\) leaves only sector \(a\), with norm at most one.
Thus

\[
 Q(\operatorname{UniqueOR}_M\circ f)=\Omega(A\sqrt M).
\]

Combining this with the amplified upper bound gives

\[
 (T+q)/\sqrt\delta=\Omega(A\sqrt M),
\]

and hence the theorem.

## Mixed-state output corollary

The result applies to a \(T\)-query state-preparation circuit even when the
declared output is mixed. Suppose a target state has winning-label mass \(p\)
and the prepared state obeys

\[
 D_{\rm tr}(\widetilde\rho_x,\rho_x)\leq\epsilon<p.
\]

For the projector \(\Pi_S\) onto winning labels, trace-distance contractivity
gives

\[
 \operatorname{Tr}(\Pi_S\widetilde\rho_x)\geq p-\epsilon.
\]

Deferring measurements and retaining discarded registers purifies the circuit;
the usual XOR or phase query gives inverse access at the same query cost.
Applying the theorem with \(\delta=p-\epsilon\) yields

\[
 \boxed{
 T\geq cQ(f)\sqrt{(p-\epsilon)\lfloor G/k\rfloor}-CQ(f).
 }
\]

This does not cover an externally supplied forward-only CPTP state channel,
unknown-unitary access without an inverse, free postselection, or unrestricted
expected-query algorithms.

## Sharp baseline and counterexamples

Uniform guessing uses no queries and succeeds with probability \(k/G\).
Therefore the unsubtracted expression
\(\Omega(\sqrt\delta Q(f)\sqrt{G/k})\) is false at the baseline. For example,
with \(f=\operatorname{PARITY}_N\), \(G=N^2\), \(k=1\), and
\(\delta=1/G\), it incorrectly demands \(\Omega(N)\) queries.

Subtracting the success excess inside the square root is also invalid. For odd
\(N\), take \(f=\operatorname{MAJ}_N\), choose independent uniform labels
\(I,J\), query one uniform bit of block \(I\), and output \(I\) if it is one
and otherwise \(J\). With \(r=k/G\), this one-query algorithm succeeds on
every exactly-\(k\) input with probability at least

\[
 r\left(1+\frac{1-r}{N}\right).
\]

For \(G=N^2,k=1\), the naive excess-success formula would still be too large.

## Prior art and defensible novelty statement

The robust amplification ingredient is due to Høyer, Mosca, and de Wolf,
“Quantum Search on Bounded-Error Inputs,” ICALP 2003,
[arXiv:quant-ph/0304052](https://arxiv.org/abs/quant-ph/0304052). General
adversary tightness and composition are standard; relevant sources include
Lee--Mittal--Reichardt--Špalek--Szegedy,
[arXiv:1011.3020](https://arxiv.org/abs/1011.3020), and Reichardt,
[arXiv:1005.1601](https://arxiv.org/abs/1005.1601).

A targeted search did not find the displayed arbitrary-inner,
small-success finder theorem stated explicitly. It is nevertheless a short
combination of known tools. The defensible claim is therefore “apparently new
as stated and a closure of the QIPM state-conversion gap,” not a new adversary
or amplification technique.

