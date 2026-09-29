# PosSLP is closed under polynomial Boolean combinations: an explicit compiler

Date: 2026-09-28. Status: elementary proof, independently reviewed;
novelty is not claimed. This note replaces an initial concern that polynomial
nonadaptive PosSLP queries could not safely be combined into one query.

## Result and relevance

Given integer arithmetic circuits \(C_1,\ldots,C_k\) over
\(\{0,1,+,-,\times\}\), and a Boolean circuit \(B\) on their positivity bits,
one can construct in deterministic polynomial time one integer arithmetic
circuit \(C\) such that

\[
 C>0\quad\Longleftrightarrow\quad
 B([C_1>0],\ldots,[C_k>0])=1.
\]

Thus the class of languages polynomial-time many-one reducible to PosSLP is
closed under polynomial-time truth-table reductions. In particular, a
polynomial list of independently constructed exact comparison circuits can
be combined by conjunction, disjunction, negation, or any polynomial Boolean
postprocessing without changing a many-one PosSLP upper bound into merely a
Turing upper bound.

This statement concerns an explicitly represented polynomial Boolean circuit.
It does not permit an exponentially long truth table or a succinctly encoded
exponential list of queries. It also does not by itself prove closure under
adaptive oracle computations.

## A rational map that compresses the magnitude range

For \(M\ge1\), define

\[
 F_M(x)=\frac{2Mx}{M+x^2}.
\]

**Lemma 1.** If \(1\le |x|\le M\), then \(F_M(x)\) has the same sign as
\(x\), and

\[
 1\le |F_M(x)|\le\sqrt M.
\]

**Proof.** The denominator is positive and the map is odd. Put \(t=|x|\).
For \(1\le t\le M\),

\[
 2Mt-(M+t^2)
 = (t-1)(M-t)+(M-1)t\ge0.
\]

This gives the lower bound. The upper bound follows from
\(M+t^2\ge2\sqrt M\,t\). No square root needs to be evaluated by the circuit.
\(\square\)

Set \(M_0=2\) and \(M_{j+1}=M_j^2\). All constants
\(M_j=2^{2^j}\) share one straight-line program of length \(O(N)\).
For any \(x\) with \(1\le|x|\le M_N\), apply

\[
 F_{M_N},F_{M_{N-1}},\ldots,F_{M_1}
\]

in that order. Lemma 1 proves that the resulting rational number \(u\)
has the sign of \(x\) and satisfies \(1\le|u|\le2\). There are only
\(N\) stages, even though \(M_N\) has exponentially many bits.

Every input output \(a_i=C_i\) is replaced by \(x_i=2a_i-1\). Since
\(a_i\) is an integer, \(x_i\ne0\), and \(x_i>0\) exactly when
\(a_i>0\). If the input circuits have at most \(n\) arithmetic gates in
total, the elementary gate-height bound \(|a_i|\le2^{2^n}\) holds.
Taking \(N=n+2\) safely gives \(1\le|x_i|\le M_N\). These bounds are
used to construct constants and gates, not to expand their binary values.

## Exact Boolean gates on the normalized values

Maintain the invariant

\[
 u\in[-2,-1]\cup[1,2],\qquad [u>0]=\text{the represented Boolean bit}.
\]

For two such values \(u,v\), define

\[
 W_\wedge(u,v)=2(u+v)-3,
 \qquad
 W_\vee(u,v)=2(u+v)+3.
\]

The AND expression lies in \([1,5]\) when both inputs are positive,
in \([-5,-1]\) when the signs are mixed, and in \([-11,-7]\) when both
are negative. The OR expression lies in \([-5,-1]\) when both inputs
are negative, in \([1,5]\) when the signs are mixed, and in \([7,11]\)
when both are positive. Consequently both expressions have the desired
sign and magnitude between 1 and 11.

After either binary gate, apply \(F_{16}\) and then \(F_4\). The output
again has magnitude in \([1,2]\), with unchanged sign. Negation is simply
\(-u\). Boolean constants can be represented by \(-1\) and \(1\).
Every Boolean gate therefore costs a constant number of rational arithmetic
gates, regardless of the depth of \(B\). There is no approximation error
and no accumulation of error along paths in the Boolean circuit.

## Eliminate division without losing the sign

Store every rational wire as a pair of integer circuit outputs \((P,Q)\)
with \(Q>0\), representing \(P/Q\). For the range compression map, use

\[
 (P,Q)\longmapsto
 \bigl(2MPQ,\;MQ^2+P^2\bigr).
\]

Its denominator is strictly positive because \(M>0\) and \(Q>0\).
For inputs \((P,Q)\) and \((R,S)\), the two Boolean gate expressions use

\[
 (2PS+2RQ\mp3QS,\;QS),
\]

where minus gives AND and plus gives OR. Negation replaces \(P\) by
\(-P\). Start each input as \((2a_i-1,1)\). Induction establishes positive
denominators for all wires, so the final numerator has the required sign.

The circuit is a DAG: references to previously constructed numerators,
denominators, and constants are shared. If \(s\) is the Boolean circuit
size, the integer circuit has size \(O(n+kN+s)\), with a polynomial-time
construction. Expanding the DAG into a formula or evaluating its enormous
integers explicitly is neither required nor part of the reduction.

## Literature audit and the appropriate novelty claim

The following primary sources were examined or consulted on 2026-09-28.

1. Allender, Bürgisser, Kjeldgaard-Pedersen, and Miltersen,
   *On the Complexity of Numerical Analysis*, SIAM J. Comput. 38 (2009),
   1987–2006, [author manuscript](https://people.cs.rutgers.edu/~allender/papers/slp.pdf),
   [local full text](../../literature/papers/allender2009-on-the-complexity-of-numerical/fulltext.md).
   Proposition 1.1 identifies \(\mathrm P^{\mathrm{PosSLP}}\) with the
   Boolean part of constant-free polynomial-time real computation. Its
   proof uses oracle calls to implement branches; it does not itself provide
   the one-circuit compiler above. The generic numerical computation
   equivalence is also expressly a Turing equivalence. The discussion before
   Theorem 3.9 describes compact rational approximations for elementary
   functions and points to earlier approximation literature. This makes a
   claim that compact sign processing is a new general idea unjustified.

2. Kung and Traub, *All Algebraic Functions Can Be Computed Fast*,
   J. ACM 25 (1978), 245–260,
   [author copy](https://www.eecs.harvard.edu/~htk/publication/1978-jacm-kung-traub.pdf).
   The inspected introduction specifies computation of coefficients of a
   local algebraic-function expansion. It does not explicitly state the
   Boolean closure theorem used here. A full derivation of a uniform sign
   compressor from this source was not completed; it should not be cited as
   if it explicitly proved this closure result.

3. Bürgisser and Jindal, *On the Hardness of PosSLP*, SODA 2024,
   [author manuscript](https://goravjindal.github.io/assets/pdf/posslpsoda2024.pdf).
   The inspected introductory statements repeat the standard
   \(\mathrm P^{\mathrm{PosSLP}}\) characterization and distinguish it
   from particular many-one reductions. They do not settle whether the
   explicit compiler above has already appeared elsewhere.

4. Beigel, Reingold, and Spielman, *PP is closed under intersection*,
   [author page](https://cis.temple.edu/~beigel/papers/brs-pp-jcss.html).
   Its abstract records Boolean closure results for PP using threshold
   combination techniques. It is relevant methodological background, not a
   PosSLP closure theorem. No transfer from PP to PosSLP is asserted.

5. Chen and Chow, *A Stable Scaling of Newton–Schulz for Improving the
   Sign Function Computation of a Hermitian Matrix*, 2014 preprint,
   [author copy](https://faculty.cc.gatech.edu/~echow/pubs/chen-chow-2014.pdf),
   pp. 1–2. This is a direct methodological antecedent: it explicitly lists
   the classical inverse-Newton map \(r(z)=2z/(1+z^2)\), along with
   scaled Newton and inverse-Newton schemes. Our map satisfies
   \(F_M(x)=\sqrt M\,r(x/\sqrt M)\). The dyadic schedule above therefore
   applies a classical sign iteration with predetermined rational scaling.
   The source concerns numerical matrix sign computation; it does not
   explicitly state the PosSLP Boolean closure result.

6. Nakatsukasa and Freund, *Using Zolotarev's Rational Approximation for
   Computing the Polar, Symmetric Eigenvalue, and Singular Value
   Decompositions*, 2014 technical report,
   [author report](https://www.keisu.t.u-tokyo.ac.jp/data/2014/METR14-35.pdf),
   §§3.6–3.7. The paper explicitly explains the rapid increase in
   approximation power obtained by composing rational sign approximants,
   and relates scaled Heron iterations to earlier results of Ninomiya and
   Braess. This is stronger prior context than unscaled Newton convergence.
   It does not supply an inspected PosSLP reduction, but establishes that
   composition and scaling of rational sign approximations are classical.

Search phrases included `"PosSLP" "intersection"`, `"PosSLP"
"truth-table"`, `"PosSLP" "nonadaptive"`, `"PosSLP" "conjunction"`,
`"PosSLP" "Boolean combination"`, `"PosSLP" "parallel"`, and
`"PosSLP" "one query"`. No directly matching primary theorem was located
in this focused search. That absence does not establish novelty. The safe
description is **a self-contained elementary compiler lemma obtained from
classical rational sign iteration**, with prior art still to be investigated
before any originality claim about the complexity consequence.

## A misleading route and its limitation

Ordinary square-root Newton iteration started from a crude bound need not
enter its quadratic convergence region in polynomially many circuit-size
steps. For example, when approximating \(\sqrt1\) from \(y_0=M_N\),

\[
 y_{j+1}=\tfrac12(y_j+1/y_j)\ge y_j/2
\]

gives \(y_j\ge M_N/2^j\). Reaching even \(y_j\le2\) takes at least
\(2^N-1\) iterations. This refutes that particular warm-start argument,
not Boolean closure. The predetermined scaling in \(F_M\) is precisely
what avoids this obstruction.

## Verification and limits

The range lemma and gate bounds are analytic statements over real numbers.
They imply the compiler for every permitted input; finite experiments alone
would not establish this. An independent adversarial reviewer checked the
range lemma, all Boolean gate margins, denominator positivity, and the
polynomial DAG size argument, and reported no flaw. The reviewer also ran
5,882 exact rational checks covering compression grids, shifted integer
inputs, Boolean gates, and numerator/denominator updates. The review and
reproducible command are in the
[independent review](posslp-boolean-closure-independent-review.md).

Targeted whitespace verification: the direct new-file checks
`git diff --no-index --check /dev/null research-20260928/algebra/posslp-boolean-closure-audit.md`
and
`git diff --no-index --check /dev/null research-20260928/algebra/posslp-boolean-closure-independent-review.md`
completed without diagnostics.

Subsequent [targeted Lean verification](formal-coverage.md) covers the
compressor range and sign, Boolean gate margins, denominator formulas,
and refinement identities. The complete circuit construction, size bound,
and complexity consequence remain outside its coverage. No project-wide
checks were run. No claim about fast numerical evaluation, polynomial-size
expanded integer witnesses, or practical solver speedup follows from this
arithmetic-circuit reduction.
