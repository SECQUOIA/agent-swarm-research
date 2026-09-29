# Fixed integer dimension: the exact convex oracle interface

Date: 2026-09-28. Status: focused primary-source audit. The Oertel--Wagner--
Weismantel oracle assumptions, algorithm operations, and correction below
were independently checked by a second agent. This note identifies an
applicable interface; it does not claim novelty for the integer algorithm
or finish the proposed quartic complexity theorem.

Consider a rational polynomial \(f(z,y)\) of degree at most four, with
\(z\in\mathbb Z^k\), \(y\in\mathbb R^n\), and a supplied rational
\(\mu>0\) such that \(\nabla^2f\succeq\mu I\) globally. The integer
dimension \(k\) is fixed; \(n\) can vary. The projected objective is

\[
                    G(z)=\min_y f(z,y).
\]

The strongest directly applicable predecessor found is Oertel--Wagner--
Weismantel (2014), after implementing its first-order oracle and checking
bit lengths under lattice recursion. Merely citing Lenstra, or supplying
exact sublevel membership through PosSLP, would leave an oracle gap.

## 1. The useful predecessor

[Oertel--Wagner--Weismantel, *Integer convex minimization by mixed integer
linear optimization*](https://orca.cardiff.ac.uk/id/eprint/86766/1/IntegerConvexMinRev4.pdf),
Theorem 1, printed p. 1, assumes convex functions on all of
\(\mathbb R^k\), a known integer box bound \([0,B]^k\), value accuracy
\(\epsilon\ge0\), normalized subgradient accuracy
\(\delta=O(B^{-k})\), and an MILP oracle with at most \(k\) integer
variables. It uses polynomially many calls in \(\log B\).
Printed p. 2 explicitly includes exact optimization when \(\epsilon=0\),
without objective bisection. Sections 3--4 query first-order oracles only
at integer points. Values are used for feasibility and incumbent
comparisons, while approximate subgradients supply rational cuts. They
never become MILP coefficients. Section 4 removes centroid computation.
The method handles thin regions through rational polyhedral slices; it
does not require a positive inradius for each objective sublevel.

Thus replacing explicit exact-value output by exact comparison access is
an implementation of the inspected algorithm. The source does not itself
establish a PosSLP implementation for \(G\). Its bound is polynomial for
fixed \(k\); it does not by itself give deterministic fixed-parameter
tractability with an input-size exponent independent of \(k\).

The [2012 preprint](https://arxiv.org/pdf/1203.4175), Theorem 1.1,
pp. 1--2, has a different interface: find an integer point in an
\(\epsilon\)-relaxed set or certify emptiness of the unrelaxed set.
It assumes bounded-denominator continuous feasibility and separation for
an intermediate relaxation. Section 4, p. 6, permits an arbitrarily large
continuous block delegated to these oracles. Its positive-tolerance
statement should not be substituted for the stronger exact 2014 result.

## 2. A repair to the flatness subroutine

The printed proof of Observation 2 in the 2014 paper claims that, after
normalizing facet widths, the difference body \(P-P\) is obtained by
symmetrizing the original inequalities. This equality is false. The
following counterexample and replacement were checked independently by
two agents. They do not invalidate the required fixed-dimensional
flatness computation.

Let

\[
 P=\operatorname{conv}(0,e_1,e_2,e_3)
   =\{x\ge0:x_1+x_2+x_3\le1\}.
\]

Every original facet normal already has width one. The proposed
symmetrized inequalities are \(|x_i|\le1\) and
\(|x_1+x_2+x_3|\le1\). They contain \(v=(1,1,-1)\).
But if \(v=a-b\) for \(a,b\in P\), then \(a_1\ge1\) and
\(a_2\ge1\), contradicting \(a_1+a_2+a_3\le1\).

A direct replacement avoids difference-body representation. Enumerate
the vertices \(p_1,\ldots,p_s\) of the bounded rational polytope
\(P\subseteq\mathbb R^d\). For each \(j=1,\ldots,d\), solve

\[
\begin{split}
 \min\quad &t,\\
 t&\ge v^{\mathsf T}(p_a-p_b)\quad(1\le a,b\le s),\\
 v&\in\mathbb Z^d,\qquad v_j\ge1.
\end{split}
\tag{1}
\]

For fixed \(v\), the least \(t\) is precisely the width of \(P\)
in direction \(v\). Every nonzero integer vector or its negative has
some positive integer coordinate, and width is unchanged by negation.
The best of these \(d\) MILPs therefore computes an exact minimum-width
integer direction. In fixed dimension vertex enumeration has polynomial
output size and bit complexity, so (1) is a polynomial-size rational
replacement. Deficient-dimensional polytopes can first be reduced to
their affine hull, as in the surrounding recursion.

## 3. Why supplied strong convexity helps implement the oracle

The following deductions are for the proposed application, rather than
statements attributed to the papers above. They still need to be
incorporated into the full complexity proof with uniform bit bounds.

Each fiber has a unique minimizer \(y(z)\). Partial minimization preserves
the curvature bound:

\[
 G(tu+(1-t)v)
 \le tG(u)+(1-t)G(v)
       -\frac\mu2t(1-t)\|u-v\|_2^2.
\tag{2}
\]

Indeed apply strong convexity of \(f\) to
\((u,y(u))\) and \((v,y(v))\), and drop the additional nonnegative
term involving \(y(u)-y(v)\). The positive definite fiber Hessian and
the implicit function theorem give

\[
                \nabla G(z)=\nabla_z f(z,y(z)).
\tag{3}
\]

Suppose an oracle query occurs at an integer point \(z\). If
\(\|\nabla G(z)\|_2<\mu/2\), then for every different integer
point \(w\), strong convexity gives

\[
 G(w)-G(z)\ge
   -\|\nabla G(z)\|_2\|w-z\|_2
   +\frac\mu2\|w-z\|_2^2>0.
\tag{4}
\]

Thus a sufficiently small gradient certifies the exact integer optimum;
one need not determine whether that gradient is exactly zero. Otherwise
the gradient has a useful norm lower bound, making absolute precision
sufficient for normalized direction precision.

For example, let \(d\) denote the current lattice-coordinate dimension,
let \(0<\delta\le1\), and compute a rational vector \(q\) with

\[
 \|q-\nabla G(z)\|_\infty\le
                  e:=\frac{\mu\delta}{64d}.
\tag{5}
\]

If \(\|q\|_2\le\mu/4\), then (4) applies because the true norm
is at most \(\mu/4+\sqrt d\,e<\mu/2\). This test uses rational
squared norms. Otherwise, writing
\(a=\|\nabla G(z)\|_\infty\) and \(b=\|q\|_\infty\), we
have \(a\ge\mu/(8\sqrt d)\), \(b\ge a/2>0\), and

\[
 \left\|\frac q b-
       \frac{\nabla G(z)}a\right\|_\infty
 \le\frac{2e}{b}\le\frac{4e}{a}
 \le\frac{32\sqrt d\,e}{\mu}\le\delta.
\tag{6}
\]

The rational vector \(q/b\) is therefore a valid approximate normalized
direction. Its requested absolute precision has polynomial bit length
when \(\mu\), \(\delta\), and the recursion data do. This argument
uses the integrality of the query; it is not a strong separation oracle
for arbitrary continuous sublevels.

After an injective integral affine substitution \(z=z_0+Tu\), curvature
in \(u\) is at least \(\mu\lambda_{\min}(T^{\mathsf T}T)\).
The rational lower bound

\[
 \lambda_{\min}(T^{\mathsf T}T)\ge
 \frac{\det(T^{\mathsf T}T)}
      {\operatorname{tr}(T^{\mathsf T}T)^{d-1}}>0
\tag{7}
\]

has controlled bit length when the lattice basis does. Equation (7)
identifies the needed bound; the complete algorithm must track those
basis sizes and update the current box bound.

## 4. Exact comparisons and the remaining application proof

Ordinary polynomial-precision optimization of the strongly convex
fiber can produce the approximation in (5): a certified objective error
bounds distance to \(y(z)\), and a polynomially bounded derivative of
\(f\) on the relevant box transfers that distance to (3). The input
must include explicit bounds sufficient to make this statement uniform.

Exact incumbent comparisons need a slight extension of
[the continuous PosSLP upper-bound argument](strong-convex-quartic-posslp-upper.md).
To compare \(G(u)\) and \(G(v)\), minimize the strongly convex quartic

\[
       H(y,y')=f(u,y)+f(v,y')
\]

and compare the value of the observable
\(h(y,y')=f(u,y)-f(v,y')\) at its unique minimizer with zero.
This is not the minimum of \(H\). The Newton-circuit and algebraic-gap
argument extends to an explicitly supplied fixed-degree polynomial
observable, but that extension must be stated and proved. A
minimum-versus-rational-threshold oracle alone does not directly compare
two algebraic fiber values.

The full application also needs a polynomial-bit bound on an integer
optimizer, which supplied global strong convexity makes plausible via
the feasible reference point \((0,0)\). It must specify the box
constraint oracle, exact comparisons of all visited incumbents, and
lattice-coordinate recursion. Once these are supplied, the inspected
2014 algorithm offers a credible deterministic polynomial-time route for
each fixed \(k\), with PosSLP calls restricted to exact comparisons.
This audit does not promote that route to a proved complexity theorem.

## 5. Other strong predecessors and their boundaries

**Khachiyan--Porkolab (2000).**
[Theorem 1.2](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
printed p. 208, solves integer optimization over convex sets given by
first-order semialgebraic formulas. Its polynomial-time corollary fixes
the total number of free and quantified variables. Applying it directly
to \(\exists y:f(z,y)\le r\) leaves a variable quantified block of
size \(n\), so it does not establish the desired bound. Its treatment
of algebraic affine hulls is substantive, but algebraic coordinates
are explicitly encoded; a compact PosSLP oracle does not automatically
supply that encoding.

**Heinz and Hildebrand--Köppe.**
[Hildebrand--Köppe](https://arxiv.org/pdf/1006.4661), Theorem 1.1,
treats explicitly encoded quasiconvex polynomial objectives and
constraints in entirely integer variables. Definition 2.1 and Theorem
2.2 use a rational shallow-cut oracle: given a rational ellipsoid,
certify a rounding or return a rational cut. Theorem 5.7 implements it
using the polynomial representation and controls output length.
The projected \(G\) is not generally such a polynomial. Using their
algorithm for \(G\) therefore requires a new oracle implementation;
value comparison alone is insufficient. Heinz's 2005 full article was
not obtained in this audit. Its results were checked only as stated and
used in the Hildebrand--Köppe primary text and in the existing
[local prior audit](quasiconvex-polynomial-nonlinear-dimension-prior.md).

**Dadush--Peikert--Vempala.**
[Theorem 4.7](https://arxiv.org/pdf/1011.5666), printed p. 18,
gives expected-time integer feasibility for a bounded convex body with
a strong separation oracle. Definition B.2, p. 37, requires a rational
normal strictly separating each rejected rational query and a polynomial
bound on that normal's encoding length. The algorithm's running time
depends on this bound. Theorem B.5 rounds or certifies small volume;
an input positive inradius is not the missing hypothesis here. The
missing step for projected quartic sublevels is the specified rational
strong-separation oracle. Exact membership does not supply it. Moreover,
the theorem is randomized in expected time.

**Dadush's thesis and Del Pia.**
[Dadush, Theorem 7.5.1 and Algorithm 7.4](https://ir.cwi.nl/pub/25614/Thesis_DDadush.pdf),
pp. 246--247, optimize a convex objective on lattice points using
separation and subgradient oracles, again in expected time. The
algorithm intersects the current set with exact objective sublevels;
the requisite oracle must remain available after those intersections.
[Del Pia, Section 5](https://arxiv.org/pdf/2311.00099v2), printed p. 23,
explicitly warns that partial minimization and a value oracle do not
alone justify an integer-oracle theorem: global extension, subgradients,
and deterministic versus expected bounds matter. Here \(G\) is already
defined and strongly convex on all of \(\mathbb R^k\), so the extension
issue disappears. The remaining implementation requirements do not.

## 6. Sources and verification

Read the Oertel--Wagner--Weismantel 2014 primary PDF, including its
theorem, both algorithms, and auxiliary flatness and volume arguments.
A separate agent independently inspected these passages and the 2012
preprint. Both agents independently found the simplex counterexample
and the vertex-based MILP repair. Read the linked Hildebrand--Köppe,
Khachiyan--Porkolab, and Dadush--Peikert--Vempala primary theorem and
oracle definitions. Read the relevant Dadush thesis and Del Pia pages
from the existing local primary texts. Earlier local audits were used
as a source map, rather than as substitutes for these decisive passages.

The literature search covered fixed-dimensional convex integer
optimization, first-order and strong-separation oracles, implicit
projected objectives, and exact versus approximate optimization. It
does not establish absence of equivalent results. No mathematical
novelty is claimed for the geometric algorithm, its oracle model, or
the elementary curvature deductions.

Targeted verification: a Python check of this note's local links,
trailing whitespace, final newline, and the exact simplex inequalities;
and `git diff --check --
research-20260927/fixed-integer-quartic-oracle-prior.md`. Both passed.
No project-wide checks or CI inspection were performed.
