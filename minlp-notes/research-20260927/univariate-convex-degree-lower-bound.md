# Exponential degree is necessary for some univariate convex realizations

Date: 2026-09-28. Status: complete proof with a fresh
[independent review](univariate-convex-degree-lower-bound-review.md)
of the assembled manuscript, its corollaries, and both representation
comparisons. No remaining mathematical gap was found. A separate
[prior audit](univariate-convex-degree-lower-bound-prior.md) compares
Markov inequalities, convexifying multipliers, and positive-coefficient
multiples. Novelty is unestablished.

There are rational cubic inputs of bit length \(O(n)\) with one real
root \(\alpha_n\) for which every rational globally convex
univariate polynomial having precisely that real zero has degree
exponential in \(n\). Such strongly convex realizations nevertheless
exist. A polynomial-size globally strongly convex quartic in two
variables realizes the same number as its first zero coordinate.

Thus auxiliary variables can avoid an unavoidable exponential degree
cost of an exact univariate convex realization. This concerns exact
rational polynomial descriptions and their dense output, not a lower
bound on approximate optimization or on compressed circuit encodings.

## 1. The cubic family and the lower bound

For every integer \(n\ge1\), put

\[
 \varepsilon_n=2^{-2n},\qquad
 p_n(X)=(X+2)(X-1)^2+\varepsilon_n
       =X^3-3X+2+\varepsilon_n.                 \tag{1}
\]

**Theorem.** The polynomial \(p_n\) is irreducible over
\(\mathbb Q\), has exactly one real root \(\alpha_n\), and
has a dense rational description of length \(O(n)\). If
\(F\in\mathbb Q[X]\) is globally convex and
\(F^{-1}(0)\cap\mathbb R=\{\alpha_n\}\), then

\[
                   (\deg F)^2>\frac34\,2^n.       \tag{2}
\]

The conclusion applies to every such polynomial, with unrestricted
coefficient heights and without prescribing a multiplier form. It
therefore applies to globally strongly convex realizations as well.

The following consequences hold for the same family.

1. If a finite family of rational globally convex inequalities
   \(F_i(x)\le0\) has feasible set exactly \(\{\alpha_n\}\),
   then at least one nonzero row satisfies (2). Increasing the number
   of univariate convex rows cannot avoid the degree obstruction.
2. If a nonconstant rational globally convex polynomial \(J\)
   has an unconstrained minimizer at \(\alpha_n\), then
   \((\deg J-1)^2>3\,2^n/4\). Its minimum value need not be zero
   or rational.

## 2. Irreducibility and the complex conjugates

The derivative is \(p_n'(x)=3(x^2-1)\). Its local maximum at
\(-1\) is \(4+\varepsilon_n>0\), and its local minimum at
\(1\) is \(\varepsilon_n>0\). There is exactly one real root,
and it is less than \(-2\). Write it as

\[
       \alpha=-2-t,\qquad t>0,\qquad
                     t(3+t)^2=\varepsilon_n.          \tag{3}
\]

There is no rational root. Indeed, if \(t=a/b\) in positive
coprime integers, the rational number in (3) is

\[
                  \frac{a(a+3b)^2}{b^3}.
\]

This fraction is reduced because both \(a\) and \(a+3b\)
are coprime to \(b\). Its numerator exceeds one, whereas the reduced
numerator of \(\varepsilon_n\) is one. This is impossible.
A cubic with no rational root is irreducible. This argument works for
every \(n\); no congruence restriction on \(n\) is needed.

Let the other two roots be \(\beta\pm i\eta\), with
\(\eta>0\). Comparing coefficients gives

\[
 \beta=1+t/2,\qquad
 \eta^2=3t+3t^2/4,\qquad
 \ell:=\beta-\alpha=3+3t/2>3.                 \tag{4}
\]

These relations can also be checked by expanding
\((X-\alpha)((X-\beta)^2+\eta^2)\).
The exact identity

\[
 \varepsilon_n-\eta^2
             =t(6+21t/4+t^2)>0                  \tag{5}
\]

shows that \(0<\eta<2^{-n}\). Thus two complex conjugates
approach the real point 1 while the real conjugate remains below \(-2\).
All input coefficients have \(O(n)\) bits; for example, clearing
denominators gives
\(2^{2n}X^3-3\cdot2^{2n}X+2^{2n+1}+1\).

## 3. A short interval bound excludes a nearby complex zero

The classical Markov inequality states that a real polynomial of degree
at most \(D\) satisfies

\[
 \|P'\|_{[-1,1]}\le D^2\|P\|_{[-1,1]}.
\]

It is stated in [Pierzchala, Theorem 1.1](https://link.springer.com/article/10.1007/s00208-015-1294-9).
The original [Markov translation](https://www.math.auckland.ac.nz/hat/fpapers/markov4.pdf),
Problem 2, pages 14--16, also states the scaled interval bound used here.
Iterating the first-derivative inequality, while conservatively retaining
the same upper degree \(D\), gives

\[
 \|P^{(j)}\|_{[a,b]}
   \le\left(\frac{2D^2}{b-a}\right)^j
                     \|P\|_{[a,b]}.                 \tag{6}
\]

No sharp higher-derivative inequality is needed.

Suppose a real polynomial \(P\) satisfies
\(P(b)=1\), \(0\le P\le1\) on \([a,b]\), and
\(P(b+i\eta)=0\), with \(\eta\ne0\). Its finite Taylor
expansion at \(b\), together with (6), gives

\[
 1\le\sum_{j=1}^{D}\frac{q^j}{j!},\qquad
                      q=\frac{2D^2|\eta|}{b-a}.       \tag{7}
\]

If \(q<1/2\), that sum is at most the infinite geometric sum
\(q/(1-q)<1\), a contradiction. Therefore

\[
                      D^2\ge\frac{b-a}{4|\eta|}.      \tag{8}
\]

Retaining the exponential-series bound improves the constant to
\(D^2\ge(b-a)\log(2)/(2|\eta|)\). The simpler bound (8)
is enough for the encoding conclusion. This is an application of
classical derivative bounds, not a new Markov inequality.

## 4. Applying the bound to convex zero realizations

Let \(F\) satisfy the theorem. Since \(F\) has rational
coefficients and vanishes at \(\alpha\), irreducibility gives
\(p_n\mid F\). In particular,
\(F(\beta+i\eta)=0\), and \(F\) cannot be affine.

A nonaffine globally convex univariate polynomial has positive leading
coefficient and even degree, so it tends to \(+\infty\) at both
ends. If it were negative somewhere, continuity would give a zero on
either side of that negative point. Uniqueness of its real zero therefore
implies \(F\ge0\) and \(F(\alpha)=0\). Also
\(F(\beta)>0\), since \(\beta\ne\alpha\).

Normalize \(P=F/F(\beta)\). For \(x\in[\alpha,\beta]\),
convexity places its value below the chord joining 0 and 1, and
nonnegativity supplies the lower bound. Thus \(0\le P(x)\le1\).
Apply (8), then (4)--(5):

\[
           (\deg F)^2\ge\frac{\ell}{4\eta}
                              >\frac34\,2^n.
\]

Although the normalization scalar can be irrational, (6)--(8) concern
real polynomials and remain valid. Rationality is used to force the
complex conjugate to remain a root before this normalization.

### Finite convex inequality systems

Remove identically zero rows from a finite system whose feasible set is
\(\{\alpha\}\). At least one row is active at \(\alpha\).
If every active row had negative derivative there, all active rows would
be strictly negative on a sufficiently short right-hand interval.
Inactive rows remain negative by continuity. Finiteness would then give
a right-hand feasible interval, a contradiction. Hence some nonzero
active row \(F_i\) satisfies \(F_i'(\alpha)\ge0\).

Its supporting line at \(\alpha\) gives
\(F_i(x)\ge0\) for all \(x\ge\alpha\).
Moreover, \(F_i(\beta)>0\): if it were zero, convexity and
nonnegativity would make the polynomial vanish on the entire interval
\([\alpha,\beta]\), forcing it to be identically zero.
Its rational coefficients again imply \(p_n\mid F_i\).
Normalize this row and repeat the chord and Markov argument. This proves
the first corollary without a bound on the number of rows.

### Unconstrained convex objectives

Let a nonconstant rational globally convex \(J\) attain a minimum at
\(\alpha\). Then \(J'(\alpha)=0\), so \(p_n\mid J'\).
Convexity makes \(J'\) nondecreasing. It follows that
\(0\le J'(x)\le J'(\beta)\) on \([\alpha,\beta]\).
The last value is positive: otherwise \(J'\) vanishes throughout
that interval and is identically zero. Apply (8) to
\(P=J'/J'(\beta)\), whose degree is \(\deg J-1\).
This proves the second corollary. Convexity of \(P\) itself is
unnecessary; its interval bounds suffice.

## 5. What lifting and quasiconvexity change

The [univariate existence lemma](univariate-convex-zero-realization.md)
does apply to each \(p_n^2\), so a rational globally strongly convex
univariate polynomial with unique zero \(\alpha_n\) exists. The
lower bound is an unavoidable size cost, not failure of existence.

The reviewed [quartic singleton theorem](general-strongly-convex-quartic-singleton.md)
constructs, in time polynomial in this cubic's input length, a rational
quartic \(H_n(x,y)\) satisfying

\[
 \nabla^2H_n\succeq I,\qquad
 H_n^{-1}(0)=\{(\alpha_n,\alpha_n^2)\}.
\]

Its expanded coefficients and rational sum-of-squares representation
have polynomial bit length. The single convex inequality
\(H_n(x,y)\le0\) therefore projects exactly to
\(\{\alpha_n\}\). This contrasts with every finite univariate
rational convex inequality description, which needs a row of exponential
degree. The comparison imports the quartic theorem's separate proof and
review; the Markov argument does not re-prove that construction.

Global quasiconvexity also differs materially from global convexity for
unconstrained objective representations. The rational quartic

\[
 J_n(x)=x^4/4-3x^2/2+(2+\varepsilon_n)x               \tag{9}
\]

has derivative \(p_n\), which is negative to the left of
\(\alpha_n\) and positive to its right. Thus \(J_n\) decreases
and then increases, has convex sublevels, and has unique minimizer
\(\alpha_n\). It is globally quasiconvex but is not globally
convex, since \(J_n''(0)=-3\). In contrast, the second corollary
requires exponential degree for any rational globally convex polynomial
with that same unconstrained minimizer. This comparison does not claim
that every alternative constrained formulation has the same obstruction.

These are exact representation separations. They do not establish
practical numerical improvements or show that dense univariate
realizations are an appropriate solver representation. Dense expanded
output requires at least a number of entries proportional to its degree;
sparse exponents and circuits can encode large degree more compactly,
and no lower bound for those encodings is proved here.
The target number itself still has its short cubic description and
\(p_n'(\alpha_n)=3(\alpha_n^2-1)>9\). The obstruction concerns
convex polynomial encoding, not a demonstrated difficulty in locating
this real root.

## 6. Prior comparison, verification, and remaining questions

The [prior audit](univariate-convex-degree-lower-bound-prior.md)
records the sources examined and unresolved priority. Kurdyka--Spodzieja
already show coefficient-dependent exponents for a prescribed family of
convexifying powers. That does not bound every rational convex multiple:
their example starts with an already convex polynomial. Motzkin--Straus
give complex-root degree obstructions for multiples with nonnegative
coefficients, a narrower coefficient class. Markov inequalities and
derivative-based complex-neighborhood estimates are classical. The
candidate addition is the unrestricted rational convex realization
obstruction and its formulation comparison, not those ingredients.
No unsuccessful search establishes novelty.

The multiplier existence proof and this lower bound were reconstructed
independently. A fresh reviewer checked the cubic family, the interval
normalization, Taylor estimate, and the two convex corollaries; it also
found the all-\(n\) irreducibility simplification used above. Exact
inline SymPy checks verified the cubic factorization and separation
identities and irreducibility for every integer from 1 through 21. Another
reviewer independently checked a second cubic family before confirming
the simpler dyadic family. These finite checks test formulas and examples;
the universal claims rely on the proofs above.

The extra quasiconvex objective comparison and the final assembled note
were independently checked. Exact identities \(J_n'=p_n\) and
\(J_n''(0)=-3\) were also checked symbolically. Targeted document checks cover local
links, math delimiters, whitespace, control characters, and final newline.
No project-wide verification, CI inspection, or Lean formalization is
claimed.

The result rules out a degree bound depending only on the algebraic
degree, and rules out polynomial dense output in coefficient bit length.
It does not determine the optimal asymptotic degree for (1), the best
dependence on complex-root separation in general, or the shortest sparse
or circuit representation. Those are precise remaining questions; no
matching upper bound or further algorithmic benefit is asserted.
