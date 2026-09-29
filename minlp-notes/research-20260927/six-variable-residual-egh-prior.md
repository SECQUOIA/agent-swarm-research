# A deferred EGH route for residual lengths 17 and 19

Date: 2026-09-28. Status: checked primary-source statements and a proposed
deduction awaiting an independent proof audit. This note records a short
lead; it does not promote a new six-variable degree bound. The current
priority is the five-variable positive-dimensional-base obstruction.

## The filtered problem

In a proper intersection of six quadrics, the finite coordinate algebra
has a residue functional annihilating polynomials of degree at most five.
Multiplication by a quadric gives, on its nonzero support quotient $B$,
a nondegenerate multiplication pairing with functional $\psi$ satisfying
$\psi(F_3B)=0$. Set

\[
\ell=\dim B,\qquad v=\dim F_1B,\qquad
a=\dim F_2B-\dim F_1B.
\]

Then $F_2B\subseteq(F_1B)^\perp$, so

\[
2v+a\leq\ell.
\tag{1}
\]

The support scheme has finite quadratic base in its span
$\mathbb P^{v-1}$. The elementary degree bound is
$\ell\leq2^{v-1}$. The remaining cases $\ell=17,19$ therefore require
$v=6$ or $v=7$. The associated graded algebra need not be Gorenstein;
the [filtered source audit](small-residual-and-excess-prior.md) explains
why graded Gorenstein classifications cannot be applied directly.

## Applicable prior results

Caviglia, De Stefani, and Sbarra,
[*The Eisenbud–Green–Harris Conjecture*](https://people.dm.unipi.it/sbarra/pdfs/Research/EGH_FINAL-Corr-2022.pdf),
Theorem 4.14, proves EGH for an ideal containing a regular sequence of
five quadrics. Thus its Hilbert function equals that of a monomial ideal
containing the five variable squares. The corrected author PDF and the
proof were examined.

Abedelfatah,
[*Quadratic Ideals in Six Variables and the Eisenbud–Green–Harris Conjecture*](https://arxiv.org/pdf/2607.20035),
arXiv:2607.20035v1, Theorem 2.3, restates a split-factor reduction from his
2015 paper: if one member of a regular sequence splits into linear
factors and EGH holds after quotienting by each factor, then EGH holds
for every ideal containing that sequence. Theorem 4.3 covers six-variable
quadratic almost complete intersections. Theorem 4.2 proves the sharp
degree-three bound for six quadrics plus two more.

This 2026 preprint also exhibits an error in the earlier
Gunturkun–Hochster Proposition 3.12. Its explicit counterexample and the
discussion were read. The five-variable result remains available through
the independent Caviglia–De Stefani–Sbarra proof. No general six-variable
EGH theorem is inferred from these sources.

The split-factor reduction originates in Abedelfatah,
[*On the Eisenbud–Green–Harris conjecture*](https://doi.org/10.1090/s0002-9939-2014-12216-7),
Proc. Amer. Math. Soc. 143 (2015), 105–115. The available
[arXiv version](https://arxiv.org/abs/1212.2653) has different theorem
numbering; the precise statement used here was checked in the 2026
restatement, not verified against the published 2015 theorem.

## Proposed deduction to audit

Take the projective support scheme of $B$ in its linear span and a linear
form avoiding it. Its Artinian reduction has Hilbert function equal to
the differences of the affine degree filtration. Its quadratic equations
should contain a regular sequence of $r=v-1$ quadrics: the finite
quadratic base and the chosen hyperplane give an empty projective base
after reduction. This transfer, including nonreduced support, needs a
fresh review before the following argument is used.

For $r=5$, Theorem 4.14 applies directly. In the squarefree monomial
model, the surviving degree-two monomials are the edges of a graph on
$r$ vertices. Every surviving higher-degree monomial is a clique of
that graph; additional generators can only decrease the length. By (1),
$a\leq5$ if $\ell=17$, and $a\leq7$ if $\ell=19$. The corresponding
maximum clique counts, including the empty set and vertices, are 13
and 18. Both contradict the proposed length.

For $r=6$, (1) gives $a\leq3$ or $a\leq5$. Consequently the quadratic
ideal has dimension at least $21-5=16$. Over $\mathbb C$, reducible
quadrics form a closed projective variety of dimension ten in
$\mathbb P^{20}$. The projectivized quadratic ideal therefore meets
that variety. Choose a nonzero reducible quadric in it and extend it to
a quadratic regular sequence, using the empty projective base. Reduction
modulo either linear factor leaves a regular sequence of five quadrics.
The split-factor theorem and five-variable EGH would then apply.
The maximum clique counts are respectively 11 and 14, again too small.

The combinatorial maxima used above are:

| Variables $r$ | Allowed surviving edges $a$ | Maximum total clique count |
|---:|---:|---:|
| 5 | 5 | 13 |
| 5 | 7 | 18 |
| 6 | 3 | 11 |
| 6 | 5 | 14 |

Allowing fewer edges cannot increase the maximum, since edges can be
added to obtain the listed count. Exact enumeration of all graphs at
these four sizes confirmed the table. This verifies only the finite
combinatorics, not EGH or the scheme-to-graded transfer.

## Limits and verification record

The route uses the actual ideal of the support scheme, not a claim that
the filtered algebra is a standard graded Gorenstein algebra. No novelty
claim is made for the deduction. A fresh audit should reconstruct the
Artinian reduction, regular-sequence extension, and split-factor
hypotheses. The smaller odd residual lengths and the passage to an
application-level six-variable bound are not developed here. No
positive-dimensional quadratic base is covered.

Targeted commands run: a Python enumeration using
itertools.combinations over all graphs with $(r,a)$ equal to
$(5,5),(5,7),(6,3),(6,5)$, counting every complete vertex subset;
and a structural check of this Markdown file. No project-wide checks or
CI inspection were run.

