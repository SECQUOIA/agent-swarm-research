# Independent review of the box-preordering growth obstruction

Date: 2026-10-02. Verdict: **pass** for the stated certificate family
and for the separate homogeneous-corner multiplier result.

This review read the complete
[author note](../new-direction/box-preordering-growth-obstruction.md)
and its diagnostic source. A separate child independently checked the
multiplier coefficient identity, degree bound, bit size, and search without
a supplied growth constant. No substantive correction is required.

## The all-degree obstruction is valid

The decisive claim is the local equivalence
\(x^TQx\in\mathcal T([0,1]^n)\) if and only if \(Q\) is SPN.
It holds for the full preordering, including products containing both
the lower and upper slack of the same coordinate.

At zero, the constant contribution from terms with no lower slack is a
sum of nonnegative SOS values. Each must vanish. Every polynomial being
squared therefore vanishes at zero, so these multipliers have zero linear
part and PSD quadratic part. Multiplication by upper slacks preserves
that quadratic part. The degree-one identity then forces the constants
of all one-lower-slack multipliers to vanish, so those terms begin at
degree at least three. Only two-lower-slack terms can supply additional
quadratic contributions, and those are nonnegative cross-products.
Thus the quadratic jet is PSD plus entrywise nonnegative.

Conversely, PSD quadratics and nonnegative cross-products have the claimed
preordering representations. Nonnegative diagonal terms are squares.
The proof also works with arbitrary positive upper endpoints because
the upper-slack constant products are positive. It does not rely on a
degree restriction, rational SOS coefficients, or a sparse representation.

For the five-cycle example, the support-merging argument correctly proves
\((\sum x_i)^2\ge4\sum x_ix_{i+1}\) on the nonnegative orthant.
Two nonadjacent positive coordinates can be merged without decreasing
the edge sum, so a minimum-support maximizer is supported on a clique;
the cycle has clique size two. Equal adjacent coordinates attain the
growth ratio \(g=1/5\). The diagonal Hessian bound is exactly \(12/5\),
and the interaction graph is \(K_5\), not the cycle.

The separator is exact. For \(W=13I/8+A(C_5)\), entrywise
nonnegativity is immediate, and its least eigenvalue is
\(9/8-\sqrt5/2>0\). The displayed leading principal determinants
agree with the path recurrence and full cycle determinant. The trace
pairing is \(39/4-10=-1/4\). A PSD matrix and an entrywise nonnegative
matrix both have nonnegative pairing with \(W\), so \(Q\) cannot be
SPN. This proves nonexistence at every finite preordering degree.

The subsequently added connected chain of five-variable blocks also
passes review. Its nonnegative coupling squares preserve growth
\(g=1/5\), and taking the same equal adjacent-pair vector, including
coordinate one, in every block attains equality. A block has at most two
incident bridges, so \(L\le2(6/5+2/100)=61/25\) and
\(\kappa\le61/5\). Five-cliques joined by bridges have treewidth four.
Setting every other block to zero preserves any purported preordering
identity and leaves \(Q+(d/100)e_1e_1^T\), \(d\le2\).
Its pairing with \(W\) is at most \(-87/400\), so the restricted
identity is impossible. The direction \((1,1,-1,-1,0)\) has value
at most \(-16/5+2/100<0\), confirming nonconvexity. This gives a
connected family of unbounded dimension with fixed parameters, without
an optimization-hardness claim. The author additionally reports eight
chain-length checks and 36 restricted-separator checks passing; this
review verifies the formulas analytically and does not repeat those runs.

## Finite boxes and the nonisolated variant

The finite-cover argument is sound. Some closed sub-box contains
infinitely many points of the positive diagonal sequence tending to
zero. It consequently contains zero and a point positive in every
coordinate. Its lower endpoints are all zero and its upper endpoints
are all positive. The same local obstruction therefore applies to that
cell, regardless of degenerate cells elsewhere in the cover.

This statement requires a finite cover by axis-aligned sub-boxes and
the specified exact cell certificates. It establishes nothing about
general polyhedral partitions, extra generators, vanishing multipliers,
or approximate positivity certificates.

For the connected seven-variable example, the optimal set is exactly
\(\{(0,t,t):0\le t\le1\}\). Projection onto this segment gives squared
distance \(\|x\|^2+(y-z)^2/2\). With \(r=x_1-y+z\),
this is at most \(2\|x\|^2+r^2\), hence at most
\(10\widetilde F\). The stated \(g=1/10\), \(L=22/5\), and
treewidth four are valid. The growth constant need not be the largest
one for the claimed bound.

Substitution \(y=x_1,z=0\) preserves SOS multipliers and turns the
seven-variable slacks into zero, one, or original five-variable slacks.
Repeated powers can be absorbed as square factors. A purported full
preordering identity would therefore give the already excluded identity
for \(F\). The connected variant is valid without attributing the
obstruction to nonisolatedness.

## The multiplier escape and its scope

Independent multinomial expansion gives the coefficient identity

\[
 \operatorname{coeff}_{x^a}\bigl((\textstyle\sum_i x_i)^{d-2}q\bigr)
 =\frac{\binom d a}{d(d-1)}
 \left(a^TQa-\sum_iQ_{ii}a_i\right).
\]

Under orthant growth \(q\ge g\|x\|^2\), with
\(D=\max_iQ_{ii}\), the bracket is at least
\(gd^2/p-Dd\). Thus \(d\ge pD/g\), \(d\ge2\), is sufficient.
For the example, \(p=5,D=6/5,g=1/5\), giving \(d=30\) and
the multiplier \((\sum x_i)^{28}\).

Nonnegative monomial coefficients certify the multiplied polynomial.
The multiplier is positive everywhere in the nonnegative orthant except
zero, where the homogeneous quadratic already vanishes. This proves
the original inequality. A multiplier positive at zero would preserve
a positive multiple of the obstructed quadratic jet and would not work.

There are \(\binom{p+d-1}{d}\) coefficients. A common denominator of
the rational input coefficients has polynomial bit length; multinomial
factors add at most \(O(d\log(p+1))\) bits. With
\(d=O(p\kappa)\), coefficient generation, verification, and a search
through successive degrees take \(f(p,\kappa)\operatorname{poly}(I)\)
work. Nonnegative rational Gram weights can be verified directly;
irrational square-root encodings are unnecessary.

A successful search certifies nonnegativity and optimality at the known
origin. It does not verify a supplied growth modulus or uniqueness.
Termination within the displayed bound follows under the positive-growth
promise. This is a single homogeneous-corner result: applying it in all
variables, or to bags that are not individually nonnegative, supplies
no general sparse certificate theorem.

## Verification and significance

The author ran the targeted exact-rational checker and reports all five
principal minors, the separator identity, 1,024 growth fixtures, 9,216
connected-set fixtures, all 46,376 degree-30 coefficients, and 1,281
independently expanded small-degree identities passing. This review
inspected the checker source and did not repeat that command. Its finite
algebra checks support the formulas; the all-degree impossibility and
continuous-domain inequalities rest on the proofs above.

The result rules out a particular proposed certificate family even on one
fixed conditioned instance. It is not an optimization lower bound,
a lower bound on every algebraic certificate, or a new positivity
principle. The explicit multiplier escape is essential to interpreting
the result correctly.

A scoped inline Python check passed whitespace, paired mathematical
delimiters, and local links in this review. No external search,
project-wide verification, or CI inspection was performed.
