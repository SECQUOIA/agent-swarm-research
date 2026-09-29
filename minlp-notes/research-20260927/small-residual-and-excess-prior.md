# Prior results for filtered residual algebras and quadratic excess intersections

Date: 2026-09-28. Status: primary-source audit and supporting deductions.
This note does not claim a new classification or an unconditional degree bound.
The search began with residual lengths 17 and 19 in six variables, then moved
to the positive-dimensional quadratic-base obstruction in five variables.

## Filtered Frobenius algebras: the exact distinction

Write \(F_iB\) for the images of polynomials of degree at most \(i\) in a
finite affine algebra \(B\), and \(H_B(i)=\dim F_iB\). If a functional
\(\psi:B\to\mathbb Q\) has nondegenerate multiplication pairing and
annihilates \(F_3B\), then

\[
H_B(1)+H_B(2)\leq\dim B.
\]

Indeed, \(F_2B\subseteq(F_1B)^\perp\). This elementary filtered inequality
does not make the associated graded algebra Gorenstein.

Kreuzer, Long, and Robbiano, [*On the Cayley–Bacharach Property*](https://arxiv.org/pdf/1804.09469),
arXiv:1804.09469v2, gives the appropriate framework over arbitrary fields,
including nonreduced schemes and nonrational support. Theorem 5.6 characterizes
locally Gorenstein algebras with the Cayley–Bacharach property using a faithful
canonical-module element annihilating the filtration immediately below the
regularity index. Corollary 5.7 gives the corresponding Hilbert-function
inequalities. Theorem 6.8 requires both that property and symmetry of the
affine Hilbert function to conclude that the degree-associated graded algebra
is Gorenstein. Example 6.11 is locally Gorenstein and Cayley–Bacharach, with
last Hilbert-function difference one, but is not strict Gorenstein. Thus even
those stronger premises do not remove the distinction. When only
\(\psi(F_3B)=0\) is known, one must also establish the relevant regularity
index before invoking their full Cayley–Bacharach characterization.

Migliore and Nagel, [*Gorenstein algebras presented by quadrics*](https://arxiv.org/pdf/1106.2825),
Theorem 3.1, is stronger than a classification restricted to ideals generated
by quadrics: it allows a homogeneous Gorenstein ideal containing a regular
sequence of quadrics. With embedding dimension \(r\geq5\), no linear
relations, and socle degree \(r-1\), the possible second entries are
\(\binom r2,\binom r2-1,\binom r2-2\). For \(r=5\), the socle-degree-four
lengths are therefore 22, 21, and 20. This excludes lengths 17 and 19 under
these **graded** assumptions. It does not exclude them for the filtered
residual algebra without an additional transfer argument. Proposition 3.3,
which classifies quadratic presentations in small embedding dimension, has
the same graded limitation.

Migliore and Zanello, [*Stanley's nonunimodal Gorenstein h-vector is optimal*](https://arxiv.org/pdf/1512.01433),
Theorem 3.2, classifies socle-degree-four graded Gorenstein Hilbert functions
up to embedding dimension 17. It does not impose a finite quadratic base or
address the filtered transfer. Iarrobino and Macias Marques,
[*Symmetric Decomposition of the Associated Graded Algebra of an Artinian Gorenstein Algebra*](https://arxiv.org/pdf/1812.03586),
studies nonhomogeneous local Gorenstein algebras with the maximal-ideal
filtration. That filtration must not be silently substituted for the affine
degree filtration, especially for a product of local algebras.

No examined result directly settles the original filtered length-17/19
question. This is a search outcome, not an assertion that the question is open.

## A quantitative excess-intersection source

Fulton and Lazarsfeld, [*Positivity and excess intersection*](https://www.math.stonybrook.edu/~roblaz/Reprints/Fulton.Laz.Positivity.Excess.Intersection.pdf),
1982, Theorem 2(B), p. 101, applies to an irreducible cone \(C\) of dimension
\(k\geq e\) in a rank-\(e\) vector bundle \(N\). If
\(\operatorname{Sym}^mN\otimes L^{-1}\) is globally generated and \(L\)
is ample, it gives

\[
\deg_L z(C,N)\geq
m^{-(\dim\operatorname{Supp}C+e-k)}
s(C)\deg_L(\operatorname{Supp}C),
\]

where \(s(C)\) is the positive multiplicity along the zero section.
The printed theorem was checked visually because the PDF text extraction
drops some exponents and dual signs. It is a normal-cone statement; neither
a reduced zero scheme nor a smooth excess component is assumed.

Apply it to normal-cone components for a section of
\(E=\mathcal O_{\mathbb P^5}(2)^{\oplus5}\), using \(m=1\) and
\(L=\mathcal O(2)\). The contribution of a positive-dimensional support
\(W\) is at least \(2^{\dim W}\deg W\). Together with the degree-32
top Chern class and the positive contributions at isolated simple points,
this yields the weighted budget

\[
D+\sum_W 2^{\dim W}\deg W\leq32,
\tag{1}
\]

if one keeps one cone component over each irreducible positive-dimensional
component and discards the other nonnegative contributions. The sum uses
the reduced supports; retaining normal-cone multiplicities can strengthen it.

For a real scheme whose positive-dimensional support has no real point,
the conjugation-stable union of components of each dimension has even
degree: a general real complementary linear section has no real point,
so its length is even. Consequently \(D\geq23\) and (1) leave only
curves of total degree at most four, or surfaces of total degree two.
Dimensions at least three are impossible. A surface and a curve cannot
both occur, since their smallest even-degree contributions already sum
to twelve. This reduction still needs an analysis of the remaining low-degree
cases to reach a ten-unit minimum excess contribution.

## Enlarging the linear system instead of comparing Segre classes

Eklund, Jost, and Peterson, [*A method to compute Segre classes of subschemes of projective space*](https://arxiv.org/pdf/1109.5895),
Theorem 3.2, treats an arbitrary projective subscheme defined by homogeneous
generators of maximum degree \(m\). General degree-\(m\) equations give
a residual degree formula. For five quadrics through \(Y\subset\mathbb P^5\),
it specializes to

\[
\deg R=32-\deg\{c(E)\cap s(Y,\mathbb P^5)\}_0.
\tag{2}
\]

Its proof, Step 1, identifies the residual upstairs with general hyperplane
sections of the morphism from the blow-up defined by \(2H-E_Y\).
Lemma 2.1 permits a singular blow-up. At zero residual dimension the
general intersection avoids the exceptional divisor. Remark 3.3 gives
reduced residual points away from \(Y\). The theorem therefore supplies
the needed generic calculation without assuming the original five equations
have maximal normal rank along \(Y\).

Here is the separate deformation argument used with (2). Suppose
\(\mathcal I_Y(2)\) is globally generated and the original five quadrics
vanish on \(Y\), with \(D\) simple isolated zeros outside it. Their
coefficient vectors lie in \(H^0(\mathcal I_Y(2))^5\). The complex
implicit function theorem preserves these distinct simple zeros under
sufficiently small perturbations in this space. A generic coefficient
tuple can be chosen in that neighborhood. Hence

\[
D\leq\deg R=\int_{\operatorname{Bl}_Y\mathbb P^5}(2H-E_Y)^5.
\tag{3}
\]

For the source's ideal hypothesis, use the homogeneous ideal generated by
\(H^0(\mathcal I_Y(2))\). Global generation says it defines \(Y\)
scheme-theoretically after sheafification; saturation of this ideal is
unnecessary. If \(Y\) is a local complete intersection, then
\(s(Y,\mathbb P^5)=c(N_{Y/\mathbb P^5})^{-1}\cap[Y]\).
This method allows a reduced subscheme \(Y\) inside a nonreduced original
base, without asserting monotonicity of individual Segre contributions.

## Sources for the remaining low-degree geometry

Eisenbud, Green, Hulek, and Popescu,
[*Small Schemes and Varieties of Minimal Degree*](https://arxiv.org/pdf/math/0404517),
states \(\deg X\geq1+\operatorname{codim}(X,\operatorname{span}X)\)
for reduced irreducible varieties, and recalls the minimal-degree
classification in Theorem 0.1. In particular, an integral degree-two
surface is a quadric in its three-dimensional span, and an integral
quartic spanning \(\mathbb P^4\) is a rational normal quartic.

Lin and Swanepoel,
[*Ordinary planes, coplanar quadruples, and space quartics*](https://eprints.lse.ac.uk/100526/1/Ordinary_Planes_v3.pdf),
Section 3.1, records the classical dichotomy for irreducible nonplanar
quartics in \(\mathbb P^3\): either their containing quadrics form a
pencil, or there is a unique containing quadric. The first case is a
\((2,2)\) complete intersection; the second has a surface quadratic base.
Their Section 3.2 discusses singular first-species quartics as well.

A useful warning comes from Hoffman, Wang, Jia, and Goldman,
[2010 primary article](https://www.ejpam.com/index.php/ejpam/article/view/841/132),
Section 4.1: singular rational space quartics can be complete intersections
of two quadrics. The claim that every rational quartic lies on a unique
quadric needs a smoothness assumption. No classification of nonreduced
quadratic bases follows from these curve statements alone.

## Verification and limits

The cited theorem statements and relevant proofs were read in the openly
available primary PDFs. The Fulton–Lazarsfeld theorem was also checked in
a rendered page. No exhaustive literature search or priority determination
is claimed. The deformation argument above was independently communicated
to the author of the five-variable excess analysis; it is supporting
reasoning, not an independent review of that complete argument.

No mathematical test suite, project-wide verification, or CI inspection
was run for this source audit. Only the new Markdown file received a
targeted structural check.
