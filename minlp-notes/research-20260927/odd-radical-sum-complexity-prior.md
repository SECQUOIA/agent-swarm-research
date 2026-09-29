# Complexity audit for sums of odd radicals

Date: 2026-09-28. Status: primary-literature audit and an independently
checked elementary upper-bound derivation. No hardness or
publication-priority claim is established.

The safe reduction target is an explicitly defined **signed cube-root-sum
comparison problem**. It fits the reviewed quartic singleton construction.
The sources examined do not establish NP-hardness, PosSLP-hardness,
completeness, or a reduction from square-root-sum for this restriction.
Failure to find such a result does not establish that the problem is open.

## 1. Input models that must remain distinct

Define `CubeSum>=` on binary rational inputs by

\[
 c_0+\sum_{i=1}^m c_i\sqrt[3]{a_i}\geq0,
 \qquad c_i,a_i\in\mathbb Q.
 \tag{1}
\]

All cube roots mean real cube roots. Zero radicands can be removed and
negative radicands absorbed into the coefficient sign. For fixed exponent
three, rational and integer radicands are polynomially interconvertible:

\[
 \sqrt[3]{p/q}=q^{-1}\sqrt[3]{pq^2}
 \quad(p\geq0, q>0).
 \tag{2}
\]

Clearing coefficient denominators by a positive product then gives an
integer-coefficient instance with positive integer radicands. This operation
has polynomial bit cost. Integer coefficients can also be absorbed into
signed integer radicands using
$c\sqrt[3]{a}=\sqrt[3]{c^3a}$. Thus the signed version is equivalent to
comparison of two unweighted positive cube-root sums. This observation does
**not** establish equivalence with a sum having only positive terms compared
with a rational threshold: both sides may contain irrational summands.

Other relevant input models are:

- Fixed odd exponent $d$, with real $d$th roots and signed rational
  coefficients. Formula (2) becomes $q^{-1}\sqrt[d]{pq^{d-1}}$.
- Variable odd exponents written in unary or represented by dense
  polynomials. Their numeric sizes count toward the input length.
- Variable odd exponents written in binary. Dense output of $T^d-a$ or a
  realization using $d-1$ coordinates can be exponentially large.
- Dense rational polynomials $p_i$, each promised to have exactly one real
  root $\alpha_i$, and a comparison $c_0+\sum_i c_i\alpha_i\geq0$.
- Arithmetic circuits whose leaves include radicals. These permit products
  and repeated squaring; a general circuit need not have a polynomial-size
  expansion as a linear radical sum.

Statements about one model do not automatically transfer to the others.

## 2. Primary sources and their actual conclusions

### Radical equality is already easy

[Hunter, Bouyer, Markey, Ouaknine, and Worrell,
*Computing Rational Radical Sums in Uniform TC0*, FSTTCS 2010,
Theorem 1, printed pp. 309 and 315](https://drops.dagstuhl.de/opus/volltexte/2010/2873/pdf/27.pdf),
consider rational $C_i,A_i,X_i$ with $A_i>0$ and $0\leq X_i\leq1$,
all explicitly encoded. They place
$\sum_i C_i A_i^{X_i}=0$ in DLOGTIME-uniform $TC^0$.
Consequently cube-sum equality is in deterministic polynomial time,
including signed coefficients. This is an equality result; it gives no
sign test for a nonzero sum. Their introduction separately discusses
square-root-sum and distinguishes it from PosSLP.

The repository also contains the inspected primary text of
[Blömer, *Computing Sums of Radicals in Polynomial Time*, FOCS 1991](../literature/papers/blomer1991-computing-sums-of-radicals-in/fulltext.md).
Theorem 21 treats field membership for sums of real radicals over an
explicit real number field, with randomized polynomial bit complexity.
The rational case has a deterministic procedure in Section 3. The general
number-field representation includes a minimal polynomial, isolating
interval, and coefficient tuples. The paper expressly distinguishes
field membership and equality from sign. The 2010 theorem above is the
stronger relevant equality bound for rational inputs.

### The familiar PosSLP connection is an upper bound

[Allender, Bürgisser, Kjeldgaard-Pedersen, and Miltersen,
*On the Complexity of Numerical Analysis*, SIAM J. Comput. 38(5), 2009,
Theorem 1.4 and Corollary 1.5](https://people.cs.rutgers.edu/~allender/papers/slp.pdf)
put PosSLP and square-root-sum in the counting hierarchy. PosSLP asks
whether an integer produced by a division-free arithmetic straight-line
program is positive. Section 1.4 explains the square-root-sum reduction
using Tiwari's rational Newton approximation circuits. Proposition 3.2
concerns eliminating a **fixed finite set of algebraic machine constants**;
it is not by itself a uniform theorem for input lists of algebraic numbers
of varying degree. Their theorem does not assert that square-root-sum is
PosSLP-hard. Section 4 below supplies the corresponding elementary
cube-root upper-bound argument without attributing a cube-specific theorem
to this source.

Tiwari's 1992 article,
[*A problem that is easier to solve on the unit-cost algebraic RAM*](https://doi.org/10.1016/0885-064X(92)90003-T),
was identified through these primary papers, but its full text was not
inspected in this audit. No stronger statement is attributed directly to it.

### A primary paper explicitly includes cube roots in its discussion

[Kayal and Saha, *On the Sum of Square Roots of Polynomials and Related
Problems*, author manuscript, Sections 1 and 5](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Sum20of20Square20Roots20ToCT.pdf),
state on printed p. 16 that their methods and results extend to other
radical sums, explicitly including cube and fourth roots. Their Theorem 1.4
proves polynomial-precision separation for a restricted class of integer
radicands with a common large-base representation and small digits. The
large-base condition is essential to the stated theorem. Theorem 2.1 is
about orders of vanishing of sums of polynomial square roots, and Theorem
1.5 concerns the separate circuit-degree problem DegSLP. These results do
not solve arbitrary integer cube-root-sum comparison or establish its
hardness. The cube-root extension is stated as a concluding observation,
without a separately quantified cube-specific theorem.

The later [Gaillard--Jindal, *On the Order of Power Series and the Sum of
Square Roots Problem*, 2023, Theorem 5 and Corollary 1(iii)](https://arxiv.org/pdf/2304.13605)
gives order-of-vanishing bounds for sums involving
$(p_i(x)/q_i(x))^{\alpha_i}$, including cube roots when $\alpha_i=1/3$.
These are formal power-series bounds with nonvanishing denominators and
numerators at the expansion point. They do not give a general
polynomial-bit separation bound for arbitrary integer cube-root sums.
The same paper treats equality when square-root radicands are supplied
as straight-line programs, a different encoding from (1). Its introduction
and conclusion were also checked for subsequent complexity resolutions;
they supplied none for the fixed-cube comparison restriction.

### Circuit identity testing is a different problem

[Balaji, Nosan, Shirmohammadi, and Worrell,
*Identity Testing for Radical Expressions*, 2022,
Theorems 1 and 2](https://arxiv.org/pdf/2202.07961v4)
study a polynomial represented by an arithmetic circuit evaluated at
nonnegative real radicals, with binary radicands and root indices. Their
general identity problem is in coNP under GRH. The special case involving
square roots of prime integers is in coNP unconditionally and in coRP under
GRH. These concern equality of circuit expressions. They give neither a
cube-sum sign algorithm nor a reduction from arbitrary circuit positivity
to a linear cube-root sum. In particular, the circuit model's ability to
represent exponentially large integers cannot be silently imported into
explicitly encoded rational coefficients in (1).

## 3. Consequences for the quartic construction

For each nonrational cube root, $T^3-a$ is irreducible over $\mathbb Q$
after the rational cases are removed. The reviewed
[strongly convex quartic realization](general-strongly-convex-quartic-singleton.md)
and [rational Hessian certificate](sos-convex-quartic-realization.md)
therefore produce a nonnegative rational quartic $F_i$ in two variables
whose unique zero has first coordinate $\sqrt[3]{a_i}$, with polynomial
construction time and coefficient bit length. Rational roots can be
absorbed into $c_0$.

On disjoint blocks, set $F=\sum_i F_i$. Then $F\leq0$ fixes all blocks
to their prescribed zeros. Adding the single affine row

\[
 -c_0-\sum_i c_i x_{i,1}\leq0
 \tag{3}
\]

makes feasibility equivalent to (1). The sum $F$ remains globally strongly
convex and SOS-convex, with a rational Hessian certificate obtained by
embedding and summing the block certificates. This uses one quartic row
and one affine row. There is no need to claim that each separate $F_i$
is strongly convex in all other blocks' coordinates.

The same reduction works for sums of roots of dense irreducible rational
polynomials having exactly one real root, using a block per polynomial.
It also covers fixed odd radicals. It does not give a polynomial-size
reduction for binary-encoded unbounded root indices by directly expanding
their degrees.

Thus a polynomial-time exact feasibility algorithm for this quartic class
would solve `CubeSum>=` in polynomial time. This is a precise consequence,
and a useful test of what exact feasibility would require. On this audit,
it should be described as an **arithmetic comparison reduction**, not as
an established complexity hardness barrier of the same standing as a
verified square-root-sum or PosSLP reduction.

## 4. An explicit cube-sum upper bound

This section records an elementary adaptation of the classical
separation-plus-Newton argument. It is not claimed as an original result.
Its proof is included to avoid mistaking an upper bound for hardness.

**Proposition.** Both strict and weak signed cube-root-sum comparison
polynomial-time many-one reduce to PosSLP. In particular they belong to
the counting hierarchy, using the PosSLP containment cited above.

After the normalization in Section 1, write
$S=c_0+\sum_{i=1}^m c_i\sqrt[3]{a_i}$ with all coefficients integral and
$a_i\geq1$. Let

\[
 H=\max\{2,|c_0|+\sum_i|c_i|a_i\},\quad
 h=\lceil\log_2(H+1)\rceil,\quad
 \delta=2^{-h3^m}.
 \tag{4}
\]

The number $S$ is an algebraic integer in a field of degree at most $3^m$.
Every conjugate of $S$ has absolute value at most $H<2^h$. If $S\ne0$,
its nonzero integer field norm has absolute value at least one. Dividing
by the other conjugate factors proves $|S|\geq\delta$. No minimal
polynomial or common field is computed by the reduction.

Let $b$ be at least one and at least the binary length of every $a_i$.
For $r=\sqrt[3]{a_i}$ start at $x_0=2^b$ and use rational Newton steps

\[
 x_{j+1}=(2x_j+a_i/x_j^2)/3.
 \tag{5}
\]

For the relative error $e=x_j/r-1\geq0$, direct simplification gives

\[
 e_{\rm new}=\frac{e^2(3+2e)}{3(1+e)^2}
 \leq\min\{\tfrac23e,e^2\}.
 \tag{6}
\]

After $2b+2$ steps, $e<1/2$: indeed $e_0\leq2^b-1$ and
$(2/3)^{2b+2}2^b=(4/9)(8/9)^b<1/2$. After another $t$ steps,
$e\leq2^{-2^t}$. As $r\leq2^b$, this bounds absolute error by
$2^{b-2^t}$.

Put $C=\sum_i|c_i|$ and choose $t$ so that

\[
 2^t\geq h3^m+b+\lceil\log_2(C+1)\rceil+3.
 \tag{7}
\]

The resulting rational approximation $\widehat S$ satisfies
$|\widehat S-S|<\delta/8$. The iteration count is polynomial in the
binary input length. The integer exponent $h3^m$ itself has polynomial
binary length; hence repeated squaring builds $\delta$ using polynomially
many rational arithmetic gates, despite its exponential denominator
length in an expanded binary representation.

Now

\[
 S>0\iff\widehat S-\delta/2>0,\qquad
 S\geq0\iff\widehat S+\delta/2>0.
 \tag{8}
\]

All denominators in these circuits are positive: Newton iterates and
their squares are positive. Maintaining numerator and denominator circuits
at each gate converts the rational circuit to a division-free integer
circuit with polynomial overhead. Its numerator has the required sign.
Binary integer constants can be constructed from $0,1$ with polynomially
many gates. This proves a many-one reduction; it does not require a
separate equality oracle. The case $m=0$ is an ordinary rational comparison.

For a fixed number of radicals, the same norm estimate and ordinary
polynomial-precision root approximation give a deterministic polynomial
bit-time sign algorithm. With variable $m$, the estimate allows
exponentially many precision bits. It is only a sufficient precision
bound; it proves no necessary precision lower bound.

## 5. General root sums, and the square-root obstruction

For dense polynomials promised to have unique real roots, the comparison
has the existential formulation

\[
 \exists x_1,\ldots,x_m:\quad
 \bigwedge_i p_i(x_i)=0,\quad c_0+\sum_i c_ix_i\geq0.
 \tag{9}
\]

The complementary strict inequality has the same existential form.
Thus on the promised inputs both the problem and its complement reduce
to the existential theory of the reals, yielding PSPACE upper bounds.
The same holds for variable binary odd-root indices: repeated-squaring
auxiliary variables encode each equation $x_i^{d_i}=a_i$ by polynomially
many quadratic equations. The PSPACE containment for existential real
feasibility is the classical result used explicitly by the inspected
Balaji et al. paper; this audit does not claim a sharper uniform bound
for all of these input models.

There is a real arithmetic distinction from square roots. A field
generated by finitely many algebraic numbers, each with exactly one real
conjugate, has exactly one real embedding: every real embedding must fix
each generator. Its degree is odd. In particular, it cannot contain
$\sqrt2$, whose degree is two. A rational function of these generators
cannot equal $\sqrt2$ either. More generally, a nonrational element of a
totally real field cannot lie in a field with exactly one real embedding:
the odd-degree extension argument in the
[singleton field audit](singleton-field-characterization-prior.md)
would force its own field to have just one real embedding.

This excludes directly representing arbitrary square roots, or their
nonrational totally real sums, as coordinates or rational functions of
these singleton blocks. It **does not exclude a decision reduction**
which transforms a square-root-sum instance into a different number
having the same sign. No such reduction was established by this audit.

## 6. Search scope, assessment, and verification

The audit read the local primary texts of Blömer 1991, Allender et al.
2009, and Balaji et al. 2022, and the open primary PDFs of Hunter et al.
2010 and Kayal--Saha, and the relevant statements in Gaillard--Jindal 2023.
Searches included the phrases `sum of cube roots`,
`sum of cubic roots`, `cube-root-sum`, `sum of odd roots`, `odd radicals`,
`sum of algebraic numbers`, `PosSLP`, `polynomial time`, and `complexity`
in combinations. General web results led back mainly to square-root-sum,
radical equality, and Kayal--Saha's explicit cube-root observation.
Search snippets and secondary pages were used only to locate sources.

The strongest verified literature connection here is that the reduction
captures a natural radical comparison operation within a highly regular
convex class. Equality is already efficiently decidable. The present
search supplies no NP-hardness, PosSLP-hardness, completeness result, or
current primary-source declaration that the fixed-cube sign restriction
is an unresolved standard benchmark. It is reasonable to investigate this
restriction further; it is not reasonable to promote a failed search to
a novelty or hardness claim.

The checks recorded below verify exact algebra used in (6), representative
Newton error bounds, and document integrity. They do not establish the
literature search's completeness, the optimal complexity of cube sums,
or an independently reviewed proof of the quartic realization (which has
its own review files).

The [independent reduction review](quartic-exact-arithmetic-reductions-review.md)
checked Section 4's norm argument, Newton recurrence, iteration count,
weighted error, equality offsets, and conversion to integer circuits,
and reported no flaw. A [second independent check](odd-radical-sum-upper-bound-review.md)
also found no gap. Neither proof review certifies completeness of the
literature search.

An inline `python - <<'PY'` check using SymPy and `fractions.Fraction`
verified the Newton identity and the factorizations

\[
 \tfrac23e-e_{\rm new}=\frac{e(e+2)}{3(1+e)^2},\qquad
 e^2-e_{\rm new}=\frac{e^3(3e+4)}{3(1+e)^2}.
\]

The same command passed 2,020 exact one-step rational probes, 100 exact
contraction-bound probes, and checks for final newline, trailing
whitespace, control characters, balanced display delimiters, and four
local links. An earlier check attempted to expand whole rational Newton
trajectories and was interrupted during fraction arithmetic; it produced
no pass result. That expansion is unnecessary for the symbolic argument
or for the circuit reduction, which retains shared arithmetic gates.
No project-wide tests or CI checks were requested or run.

## 7. Follow-up: squarehood and nested square-root identity papers

Two additional primary sources were checked against the
[signed odd-root circuit draft](signed-odd-root-circuit-quartic.md), whose
inputs have unary odd degrees, affine combinations of retained predecessor
powers, and rational intervals certifying nonzero gate values. Neither
source supplies a sign-comparison theorem for that input model.

[Bläser, Dörfler, and Jindal, *PosSLP and Sum of Squares*,
FSTTCS 2024](https://drops.dagstuhl.de/storage/00lipics/lipics-vol323-fsttcs2024/LIPIcs.FSTTCS.2024.13/LIPIcs.FSTTCS.2024.13.pdf)
prove \(\mathrm{PosSLP}\le_T^P\mathrm{3SoSSLP}\) (Theorem 1.12):
3SoSSLP asks whether an integer produced by an arithmetic SLP is a sum of
three integer squares. They also prove coNP-hardness of deciding whether
an SLP-encoded univariate integer polynomial is nonnegative everywhere
(Theorem 1.19). The polynomial's degree and expanded coefficient lengths
may be exponential. Neither result establishes hardness for explicit
rational convex quartics, odd-root comparisons, or input SOS certificates.

There is a qualification discrepancy relevant to this audit. Their
Theorem 4.9 states without qualification that polynomial squarehood
(`SqPolySLP`) belongs to coRP. Its proof invokes the integer squarehood
procedure in [Gaillard--Jindal, Section 4.2](https://arxiv.org/pdf/2304.13605).
That procedure assumes GRH; Bläser--Dörfler--Jindal themselves state this
qualification after Problem 3.6 (page 13:10). The checked text provides no
replacement procedure or standing assumption resolving the discrepancy.
We therefore do not use Theorem 4.9 as a verified unconditional bound.
This is an unresolved qualification issue, not a proof that its conclusion
is false. The final publication and the supplied author manuscript were
both inspected; theorem numbers here refer to the final publication.

[Tulone, Yap, and Li, *Randomized Zero Testing of Radical Expressions and
Elementary Geometry Theorem Proving*](https://cs.nyu.edu/exact/doc/prover.pdf)
allow arithmetic SLPs with division and nested square-root gates
(Section 3.1, PDF pages 8--9). Their model allows shared subexpressions,
but does not include odd-root gates. Theorem 3 (PDF page 19) gives error
at most \(2^{-c}\) in time polynomial in
\(2^r,2^s,k,c,\log t,\log d\), where \(r\) counts square roots,
\(s\) counts nonzero hypotheses, \(k\) counts construction stages, and
\(t,d\) describe the thesis polynomial's monomial count and degree.
Consequently this is not a polynomial bound in the number of radical gates.
The proof uses root-separation precision of order \(pL2^{2r}\) and may
examine \(2^r\) root-branch sign assignments. Its target is identity
testing in geometric theorem proving. The conclusion (PDF page 23)
explicitly leaves thesis inequalities as an extension to investigate.
It therefore does not supply the missing odd-root or general root-circuit
sign theorem.

A fresh independent reader checked Tulone--Yap--Li's gate model and
complexity parameters and separately confirmed the squarehood
qualification discrepancy in the final 2024 paper. These checks support
the narrow source interpretations above; they do not certify that the
literature contains no stronger result. The follow-up leaves the verified
proofs and the absence of a hardness claim unchanged.

After this follow-up, a targeted inline Python check passed final-newline,
trailing-whitespace, control-character, paired-math-delimiter, and all
seven local-link checks. No mathematical proof was changed.
