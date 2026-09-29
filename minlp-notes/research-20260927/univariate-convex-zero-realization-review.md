# Independent review of univariate convex zero realization

Date: 2026-09-28. Scope: the complete proof and prior comparison in
[the univariate multiplier supplement](univariate-convex-zero-realization.md).
This reviewer did not develop that construction. A fresh second reviewer
independently reconstructed its three-region proof and the degree boundary
discussed below.

**Finding.** No gap was found in the multiplier lemma, its rational-center
choice, the uniform strong-convexity conclusion, or the characterization
by exactly one real conjugate. This is a qualitative existence result.
It should remain a modest arithmetic supplement to established polynomial
convexification, separate from the multivariate quartic construction.
The degree question is more consequential: the subsequent
[degree lower bound](univariate-convex-degree-lower-bound.md) rules out
polynomial-size dense univariate output even for cubic algebraic inputs.

## 1. The choices have the required order

Let the input polynomial be nonnegative with its only real zero at
\(\alpha\), and suppose \(f''(\alpha)>0\). Differentiability and
nonnegativity give \(f'(\alpha)=0\). Continuity supplies a neighborhood
on which \(0<m\le f''\le M\), so \(f'\) has the sign of
\(x-\alpha\) and \(|f'(x)|\le M|x-\alpha|\).

The nonconstant polynomial has positive leading coefficient and even
degree at least two. Its second derivative is positive in both tails,
and \(xf'(x)>0\) there. Consequently the manuscript can choose one
radius \(R>|\alpha|+r+1\) that works for every center satisfying
\(|c-\alpha|\le r/2\). The signs of \(x-c\) and \(x\) agree
in these tails.

The compact middle set excludes the only zero, so its positive lower
bound \(a\) exists. The derivative bounds \(B_0,B_1\), the bound
\(Z\), and the resulting \(b>0\) are uniform over the permitted
centers. Thus the lower bound on \(N\) does not depend on a center
that has yet to be selected. Only after selecting \(N\) does the proof
choose a rational center with
\(\delta^2\le m/(8NM)\). Rational density supplies such a center.
There is no circular choice of constants.

This order establishes existence of a suitable pair \((N,c)\), not
eventual convexity for a fixed rational center as \(N\) grows.
The difference is essential.

## 2. The three estimates cover the whole line

Writing \(z=x-c\) and \(w=(1+z^2)^N\), differentiation gives

\[
\frac{(fw)''}{w}=f''+\frac{4Nz}{1+z^2}f'
 +\left(\frac{2N}{1+z^2}
       +\frac{4N(N-1)z^2}{(1+z^2)^2}\right)f.
\]

The final term is nonnegative everywhere.

On the inner interval, the middle term can be negative only between
\(c\) and \(\alpha\). Both \(|z|\) and \(|x-\alpha|\)
are then at most \(\delta\), so that term is at least
\(-4NM\delta^2\). The displayed choice of \(\delta\) gives
\((fw)''/w\ge m/2>0\). This includes both possible orderings of the
center and zero.

On the compact middle region, \(|z|\ge r/2\) and \(|z|\le Z\).
Hence the quadratic-in-\(N\) positive term is at least
\(bN(N-1)\), whereas the middle term is at least \(-2NB_1\).
The chosen condition on \(N\) gives

\[
-B_0-2NB_1+bN(N-1)\ge N(B_0+1)-B_0>0.
\]

On the two tails, both \(f''\) and \((x-c)f'\) are positive,
so positivity follows directly. The three closed regions overlap at
their boundaries and cover \(\mathbb R\).

Pointwise positivity of a continuous second derivative would not alone
give a uniform modulus on an unbounded domain. The manuscript supplies
the missing reason: \((fw)''\) is an even-degree polynomial with
positive leading coefficient and degree at least four, because
\(N\ge2\). It tends to infinity in both tails. Its global minimum
is therefore attained, and pointwise positivity makes this minimum
strictly positive. Thus \((fw)''\ge\mu>0\) globally for some
\(\mu\). This is uniform strong convexity.

The multiplier is strictly positive on the real line, so it preserves
the exact zero set. Rational input coefficients and a rational center
give rational output coefficients.

## 3. The arithmetic characterization is correct

For a rational minimal polynomial \(p\) with exactly one real root,
\(p^2\) is nonnegative with that unique zero. Separability in
characteristic zero gives
\((p^2)''(\alpha)=2p'(\alpha)^2>0\), establishing the lemma's
nondegeneracy premise. Rational algebraic numbers are included; the
minimal polynomial can have degree one.

Conversely, a nonzero rational polynomial vanishing at \(\alpha\)
is divisible by its rational minimal polynomial. Every real conjugate
must therefore be a zero. A unique real zero is possible only when
there is exactly one real conjugate. Strong convexity ensures the
polynomial is nonzero, but convexity is otherwise unnecessary for this
necessity argument.

An additional elementary degree restriction is useful. If a globally
strongly convex polynomial has just one real zero, it is nonnegative
and that zero is its minimizer: coercivity and a negative value would
otherwise give two zeros. Therefore both the polynomial and its
derivative vanish at \(\alpha\). Separability implies \(p^2\)
divides the polynomial, so its degree is at least \(2\deg p\).
This lower bound need not be achievable. For \(p=x^3-2\), its square
has second derivative \(-81/8\) at \(x=1/2\), so no degree-six
rational strongly convex realization exists.

The lemma supplies no controlled expanded degree or runtime. Root
isolation and exact real algebraic calculations make the choices
effective for rational input, but do not make their magnitudes
polynomially bounded. The separate exponential lower bound shows that
polynomial dense output is actually impossible in general, not merely
unproved by this argument. It leaves sparse and circuit encodings open.

## 4. Prior comparison and significance

I read [Kurdyka--Spodzieja](https://arxiv.org/pdf/1507.06191),
Remark 3.2, Lemma 3.3, Remarks 3.4 and 3.6, Theorem 5.5, and
Corollary 5.7 directly. Remark 3.2 permits a zero at the center on a
bounded interval; the other cited global constructions assume strict
positivity or perturb the zeros. Remark 3.6 also permits powers of an
arbitrary positive strictly convex base. These are close predecessors,
not just general background.

There is a short deduction worth acknowledging. Apply Remark 3.2 with
center \(\alpha\); one further positive quadratic factor gives
positive second derivative on that interval, and the tail signs extend
this globally. At a fixed degree, uniform positive curvature persists
under a sufficiently small change of center. A nearby rational center
therefore gives the arithmetic conclusion. This deduction needs the
nondegenerate zero and a uniform tail bound; it is not a direct quoted
theorem. The manuscript's explicit estimates make those points transparent.

Thus the qualitative supplement is best presented as an arithmetic
consequence of established convexification machinery. This review does
not establish novelty. The new quantitative question asks how much
degree is unavoidable when preserving rational coefficients and the
exact zero without auxiliary variables. The exponential lower-bound
note answers one material part of that question and keeps its own
prior audit and independent review separate.

## 5. Verification record

The main identity and fixed-center counterexample were rederived
mathematically; the author's exact symbolic checks were not duplicated.
A fresh scoped reviewer independently reconstructed the proof and ran
an exact inline SymPy check of the degree-six obstruction above. Its
other computations concern the separate degree lower bound and are
recorded there. Numerical examples do not verify the global existence
argument.

A targeted inline `python -` check was used for local links, matching
mathematical delimiters, final newline, whitespace, and control
characters. No project-wide verification, CI inspection, or Lean
formalization was performed. Positive reviews record these checks;
they are not guarantees of correctness or priority.
