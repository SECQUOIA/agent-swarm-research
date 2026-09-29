# PosSLP, bounded arithmetic, and certified odd-root circuits

Date: 2026-09-28. Status: primary-source audit with independent checks of
the closest bounded arithmetic constructions. No priority claim.

The strongest relevant prior result found is an exact reduction from
PosSLP to comparison of bounded arithmetic circuits. It follows directly
from Etessami--Yannakakis's 2009 recursive Markov chain construction and
uses averaging and multiplication. A 2026 paper gives another explicit
bounded normalization. Neither removes multiplication in favor of the
restricted odd-root gates used by the repository's quartic construction.

The sources examined do not establish a PosSLP reduction to that root
model. This search result is not evidence of novelty by itself. Exact
convex and semidefinite feasibility have separate prior hardness results;
this note audits the proposed intermediate root-circuit step, not the
entire history of exact convex optimization.

## 1. Keep the target model fixed

The [reviewed signed odd-root construction](signed-odd-root-circuit-quartic.md)
takes gates

\[
 \xi_i^{d_i}=c_i+
 \sum_{j<i}\sum_{e=1}^{(d_j+1)/2}a_{ije}\xi_j^e,
 \qquad d_i\ge3\text{ odd},
\]

with unary degrees and binary rational coefficients. Rational intervals
not containing zero must certify each radicand by interval evaluation.
The proposed hardness route uses degree three and gate values near one,
with an affine final comparison. Thus a gate may use earlier values and
their individual squares; an independent product \(\xi_j\xi_k\) is
not an allowed primitive. General arithmetic circuits with optional root
gates already contain integer SLPs, so their trivial PosSLP hardness
would not settle this restricted problem.

The intended final target has explicit rational coefficients and fixed
degree: one globally strongly convex, SOS-convex quartic sublevel row
and one affine inequality. Hardness of succinct polynomials whose
expanded degree or coefficient length is exponential is different.

## 2. Established arithmetic simulations

### Tarasov--Vyalyi: addition and squaring already suffice

[Tarasov and Vyalyi, *Semidefinite Programming and Arithmetic Circuit
Evaluation*, arXiv:cs/0512035v1](https://arxiv.org/pdf/cs/0512035v1),
Theorem 3, page 5, proves polynomial equivalence of output comparison
over the arithmetic, division-free, monotone, and
\(\{+,x\mapsto x^2/2\}\) bases. Circuits start from constant one;
division circuits carry the usual definedness promise. Lemma 3, pages
6--7, supplies the addition/squaring simulation through differences of
positive quantities. Thus replacing multiplication by addition and
scaled squares for output comparison is established prior work. This
theorem requires neither bounded intermediate values nor mandatory
root gates. It does not compile ordinary addition/squaring circuits into
Section 1's gate syntax, where a retained square is available only for
an already constructed root value.

### Etessami--Yannakakis, recursive Markov chains

[Etessami and Yannakakis, *Recursive Markov Chains, Stochastic Grammars,
and Monotone Systems of Nonlinear Equations*, JACM 56(1), 2009](https://homepages.inf.ed.ac.uk/kousha/final_rmc_jacm_version.pdf),
proof of Theorem 5.2, author-PDF pages 26--27, converts an integer SLP
into two nonnegative arithmetic circuits, then gives them common depth
and alternating addition/multiplication levels. Their probability
construction replaces addition by averaging and retains multiplication.

Consequently PosSLP reduces to comparing two outputs of a polynomial-size
circuit with leaves \(0,1\), gates

\[
 \operatorname{Avg}(x,y)=(x+y)/2,
 \qquad \operatorname{Mul}(x,y)=xy,
\]

and all values in \([0,1]\). This is a direct corollary of their proof,
not a separately named theorem. A level-\(r\) value is the original
integer value divided by \(2^{a_r}\), where

\[
 a_0=0,\qquad
 a_r=\begin{cases}a_{r-1}+1&\text{addition level},\\
                   2a_{r-1}&\text{multiplication level}.
       \end{cases}
\]

The final common positive scale preserves comparison. Applying
\(N\mapsto2N-1\) before this conversion removes equality while
preserving the predicate \(N>0\). Since \(a_k<2^k\), the resulting
nonzero output difference has magnitude at least \(2^{-2^k}\).
Bounded exact arithmetic comparison is therefore established prior
work. This construction still uses products.

### Etessami--Yannakakis, Nash equilibria and FIXP

[Etessami and Yannakakis, *On the Complexity of Nash Equilibria and Other
Fixed Points*, SIAM Journal on Computing 39(6), 2010](https://homepages.inf.ed.ac.uk/kousha/nash_focs07_full_j_spec_issue_sub.pdf),
Lemma 5, author-PDF pages 22--23, gives a linear-size PosSLP conversion
to a circuit over addition, multiplication, and division, with input
\(1/2\), all gates in \((0,1)\), and two unequal outputs preserving
the decision. Its multiplication normalization divides by a circuit value
\(t=2^{-2^d}\). It cannot directly supply a division-free root-only
simulation.

The broader FIXP definition also allows integer-indexed real root gates
(pages 38--39), with nonnegative radicands and roots for even indices.
Its circuit normalization uses the other arithmetic operations, and its
reductions concern fixed-point search. Optional roots in this richer
basis do not eliminate multiplication or prove hardness for the target
basis in Section 1. In particular, removing root gates from FIXP without
changing that search class is not a sign-preserving arithmetic-circuit
simulation by odd roots.

### Doron-Arad--Mossel, polynomial activations

[Doron-Arad and Mossel, *Why ReLU? A Bit-Model Dichotomy for Deep Network
Training*, arXiv:2602.19017v1](https://arxiv.org/pdf/2602.19017v1),
Lemma A.5, pages 21--22, transforms an \(n\)-gate integer SLP into an
\(m=O(n^2)\)-gate SLP over \(+,-,\times\), initialized at
\(2^{-m}\), with every value in \([-1,1]\) and output
\(2^{-m2^n}N\). It computes the gate count first, then emits the
circuit; exponent alignment uses repeated squaring and retains products.

Lemma 3.1, page 13, gives exact multiplication using rational linear
combinations of shifted evaluations of any nonlinear rational
polynomial. Theorem F.1, page 42, excludes its specific finite template

\[
 xy=\sum_{j=0}^m\lambda_j
 \big((x+y+j)^\alpha-(x+j)^\alpha-(y+j)^\alpha\big)
\]

for \(\alpha\in\mathbb Q\setminus\mathbb Z_{\ge0}\), even when the
identity is required only for sufficiently large positive rational
\(x,y\). This includes \(\alpha=1/3\). It does not exclude nested
gadgets, different affine arguments, retained squares, or controlled
local approximation. The polynomial activation reduction therefore
does not already cover the proposed root simulation. The inspected
arXiv record lists only version 1, dated 22 February 2026.

## 3. Root-expression tools do not supply the missing simulation

[Li and Yap, *A New Constructive Root Bound for Algebraic Expressions*,
author extended abstract](https://cs.nyu.edu/~exact/doc/rootBd_abs.pdf),
dated 7 July 2000 and associated with SODA 2001, explicitly models shared
expression DAGs with arithmetic, indexed radicals, and explicitly
represented polynomial-root constants. Section 4, Theorem 1, bounds a
nonzero value away from zero using a degree bound, a conjugate-magnitude
bound, and a leading-coefficient bound. The general degree parameter
contains products of radical indices. These separation tools can support
exact sign algorithms, but do not prove polynomial bit complexity or a
restricted odd-root simulation of multiplication. This audit read the
extended abstract; it does not treat omitted proofs there as newly
verified results.

[Maaz and Strzeboński, *A New Method for Reducing Algebraic Programs to
Polynomial Programs*, arXiv:2502.08210v1](https://arxiv.org/pdf/2502.08210v1),
Theorems 1--4 and Algorithms 1--2, use resultant defining polynomials
and derivative-sign conditions to isolate algebraic functions on suitable
connected components. Their reformulation can use one new variable per
algebraic function. It does not establish a polynomial-size, fixed-degree,
globally convex conversion. The conclusion explicitly identifies degree,
monomial, and connected-component growth as barriers. The inspected
arXiv record lists version 1, dated 12 February 2025. This is relevant
representation prior, not a PosSLP hardness theorem for the current target.

The [earlier radical audit](odd-radical-sum-complexity-prior.md) separately
checks plain radical-sum equality, cube-sum comparison upper bounds,
unnested radical identity testing, Tulone--Yap--Li's nested square-root
zero testing, and the 2024 *PosSLP and Sum of Squares* paper. None of
those checked statements removes the intermediate step identified here.
In particular, integer sums of squares, polynomial perfect-square testing,
and explicit SOS-convexity certificates are different problems.

## 4. What a new root simulation would need to prove

The following are requirements for the candidate reduction, not
consequences already established by the sources above.

1. Each gadget must compile into the exact gate syntax of Section 1.
   Products or divisions introduced during analysis cannot remain as
   unallowed circuit gates.
2. All rational constants and interval endpoints must have polynomial
   binary length. A doubly exponentially small parameter may have a
   short arithmetic circuit, but not a short ordinary rational encoding.
   Its production must use allowed root gates if it is needed internally.
3. Gate boxes must satisfy the explicit interval-containment condition,
   including the effect of cancellation. Knowing the actual values stay
   near one is insufficient if the supplied independent boxes do not
   certify the radicands.
4. The complete propagated error must be below the final sign gap.
   Fixed local accuracy does not suffice for a difference potentially of
   magnitude \(2^{-2^{\mathrm{poly}(n)}}\). Equality must be treated
   explicitly, for example by the integer shift before simulation.
5. The final sign test must be affine in the retained gate coordinates,
   so that composing with the reviewed quartic realization actually
   gives the stated convex feasibility reduction.

If proved, the source-side addition would be a restricted odd-root
simulation with explicit encoding and sign control. The strongest
potential final contribution would be the resulting exact feasibility
hardness under the quartic's simultaneous regularity restrictions.
Neither the bounded-source normalization nor generic radical-to-polynomial
rewriting should be presented as new. No claim about practical running
time, weak feasibility, or approximation follows automatically from an
exact threshold reduction.

## 5. Search and verification record

Searches combined `PosSLP` with `bounded`, `root gates`, `cube root`,
`radical`, `analytic`, `nonlinear`, `power functions`, and `root
extraction`; additional searches covered `radical expressions`, `sign
determination`, and `algebraic programs to polynomial programs`. Search
snippets and secondary sites located sources; the statements above were
checked in the linked primary texts. This is a targeted audit, not an
exhaustive search or a declaration of an established open problem.

[An independent reader](posslp-bounded-circuit-source-check.md) located
the older bounded averaging/product
construction and checked the division issue in the Nash normalization.
This author then read the relevant primary proof directly. The independent
reader also adversarially checked Lemma A.5's gate counting, exponent
alignment, and boundedness, and Theorem F.1's scope and proof. No
substantive gap was found in those narrow statements. These checks do
not review all learning or fixed-point results in the cited papers, and
do not verify the proposed odd-root simulation.

A targeted inline Python command checked the final newline, trailing
whitespace, control characters, paired math delimiters, and all three
local links; it passed. No project-wide checks or CI inspection were run.
