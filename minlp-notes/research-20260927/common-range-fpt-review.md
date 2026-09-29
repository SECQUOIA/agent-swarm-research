# Independent review of exact feasibility at small common Hessian range

Date: 2026-09-28. Scope: the proof in
[common-range-fpt-frontier.md](common-range-fpt-frontier.md). This reviewer
did not develop that proof. The review first reconstructed the proposed
argument from its claims, then read the complete manuscript and the relevant
primary theorem statements. This is a mathematical review, not a formal
proof or a novelty determination.

**Finding.** No substantive mathematical gap was found. The argument gives
the claimed absolute input-size exponent, subject to the established
rational outer-lift algorithms identified in the manuscript. The review
required a precise FPT MILP import, explicit treatment of zero nonlinear
dimension, and two small scope clarifications. The author corrected the
four points, and the reviewer independently rechecked each correction.
No issue remains from this review.

## 1. What is being proved

The parameters must be distinguished carefully.

- For a continuous system, \(r\) is the codimension of the common kernel
  of all full constraint Hessians.
- For mixed-integer systems with an input box for the integer coordinates,
  \(r_x\) uses only the continuous Hessian blocks.
- Without that integer box, \(\rho\) is the codimension of continuous
  directions annihilated by the **full** Hessians, including their
  integer-continuous blocks.

The claims are continuous exact feasibility in \(2^{O(r)}N^C\), a
bounded-integer projection MILP of size \(2^{O(r_x)}N^C\), and unbounded
mixed-integer feasibility in \(f(k,\rho)N^C\), where \(C\) is absolute.
The original data are either native jointly convex quadratic inequalities
or rational SOC rows, together with arbitrary rational affine rows.
Squaring a cone row always retains its affine right-hand-side sign.

The common-kernel and scalar-radius arguments also apply to nonconvex
quadratic systems. The LP/MILP construction needs the given convex
quadratic or SOC representation. A short algebraic description by itself
does not provide a polyhedral outer lift of a nonconvex feasible set.

## 2. Farkas projection preserves the needed coefficient bounds

A rational change \(x=T_1u+T_0v\), with the columns of \(T_0\) a basis
of the common kernel, gives every quadratic and affine row the form

\[
                         C_iv+p_i(u)\le0.
\]

Symmetry of each Hessian implies that both its quadratic \(v\) term and
every \(uv\) term vanish. Thus the matrix \(C\) is constant. Rational
linear algebra computes the change and its inverse with polynomial bit
length. Affine equalities are represented by both weak inequalities.

Farkas' lemma gives an exact projection through the rays of
\(\{\lambda\ge0:C^T\lambda=0\}\). This cone is pointed because it
lies in the nonnegative orthant, so its extreme rays generate it. An
extreme-ray support has size at most \(\operatorname{rank}C+1\): a
larger support would allow a nonproportional kernel perturbation while
retaining nonnegativity. On its support the generator is determined up to
scale, and minors supply a rational normalization.

There are at most exponentially many supports. Every resulting inequality
\(\lambda^Tp(u)\le0\) is quadratic, with polynomial coefficient bit
length. Clearing denominators separately in each row is important; clearing
a common denominator across the entire exponential family would create an
unnecessary large coefficient bound. The relevant estimates are

\[
 \deg P_j\le2,\quad \operatorname{bit}(P_j)\le N^{O(1)},
 \quad\log(S+1)\le N^{O(1)}.
\]

Their dependence on an appended coefficient-bit bound \(B\) is
\((B+1)N^{O(1)}\). Determinants multiply polynomially many coefficients,
which adds their bit lengths; they do not raise \(B\) to a power that
depends on \(r\). These facts remain true when a residual-epigraph
coordinate is retained. No exponential row family is constructed by the
algorithm.

This exact finite description also proves that this particular projection
is closed. General projections of closed convex sets need not be closed,
and no such general assertion is used.

## 3. Small points and a positive residual gap

The reviewer inspected the final author manuscript of
[Basu--Roy (2010)](https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf),
Definitions in Section 2.1 and Theorems 3--4 on manuscript pages 4--5.
For degree two in dimension \(d\), their explicit formulas give

\[
 \log(2+R)\le (\tau+\log(S+1)+1)2^{O(d)}.
\]

Theorem 3 contains every bounded connected component; Theorem 4 meets every
component, including unbounded ones. Both apply to conjunctions of weak
inequalities and equations. These are distinct guarantees, and the proof
uses each in the appropriate place.

For a nonempty projected set, the meeting radius supplies a small \(u\).
The remaining fiber has constant rational matrix and a real right-hand side
whose magnitude is bounded by a quadratic expression in \(u\). Project
zero onto this nonempty closed polyhedron. The normal-cone formula puts
the projection in the span of its active normals. Selecting an independent
basis of these normals gives the Gram-matrix formula for that same point.
Its inverse has magnitude at most \(2^{N^{O(1)}}\), by rational minor
bounds. Thus the fiber has a small \(v\), even with lineality and even
when its right-hand side is irrational. A vertex or a rational feasible
point is not required. When \(r=0\), the empty \(u\)-tuple needs no
radius theorem, and this fiber argument applies directly.

For the gap, let \(\alpha\) be the minimum maximum positive residual
over a supplied finite box. A finite upper bound on the epigraph variable
makes the full epigraph compact and nonempty. Its projection \(E\) in
\((u,t)\) is compact and has \(\min_E t=\alpha\). If \(\alpha>0\),
then

\[
 H=\{(u,t,y):(u,t)\in E,\ y\ge0,\ ty=1\}
\]

is compact: \(t\) is bounded away from zero and \(y=1/t\). It is
nonempty, basic closed, and defined by polynomials of degree at most two
in \(r+2\) variables. Its largest \(y\)-coordinate is exactly
\(1/\alpha\). The containing radius bounds this maximum and yields

\[
          \log(1/\alpha)\le(B+1)N^{O(1)}2^{O(r)}.
\]

Here \(B\) accounts for any appended box coefficients. This use of the
reciprocal set is valid even though its compactness is known only under
the case assumption \(\alpha>0\). The uniform radius bound has no
unknown \(\alpha\) in its input. A meeting-radius bound alone would
not control \(\max y\).

The optional Jeronimo--Perrucci--Tsigaridas check is unnecessary for this
proof. Its Theorem 1 assumes ambient dimension at least two, so using it
on \(E\) in dimension \(r+1\) requires \(r\ge1\), or a zero-coordinate
padding when \(r=0\). Its displayed coefficient parameter uses ambient
dimension, rather than polynomial degree, in \(2n+2S\).
The final manuscript explicitly restricts this optional check to
\(r\ge1\) and uses the corrected coefficient parameter.

## 4. Why the input exponent stays absolute

Write \(P(N)\) for a polynomial of fixed absolute degree. The preceding
estimates give a feasible-point radius of bit length
\(2^{ar}P(N)\). Substituting a box with this bit length into the gap
bound gives

\[
 (2^{ar}P(N)+1)P(N)2^{br}=2^{O(r)}P(N)^2.
\]

The exponent of \(N\) has not acquired a factor \(r\). A fixed-degree
polynomial construction applied to this precision still has size and
running time \(2^{O(r)}N^C\).

The cited rational square lifts and actual Lorentz-cone lifts have precisely
this dependence on input bits, box bits, and \(\log(1/\epsilon)\).
Choose the lifted residual error strictly below the positive gap and retain
all affine rows exactly. A feasible lift implies zero minimum residual;
an original feasible point has a lift. Exact rational LP therefore decides
continuous feasibility in the stated bound. The proof does not approximate
an indefinite squared SOC residual as if it were convex.

With supplied integer bounds, every assignment has polynomial bit length.
The matrix of kernel variables can depend on that assignment, but its bits
remain uniformly polynomial. Applying the radius and gap bounds separately
to each fiber therefore gives one effective precision without enumerating
assignments. The joint outer lift preserves precisely the feasible original
integer assignments and introduces no new integer variables.

## 5. Unbounded integer coordinates and the full-kernel requirement

For \(K_*\), the condition \(H_i(0,v)=0\) removes every \(zv\) term
as well as every continuous quadratic term involving \(v\). Thus Farkas
projection gives degree-two rows in \((z,u)\), with \(u\in\mathbb R^\rho\),
and a constant eliminated-variable matrix. The real integer-coordinate
projection is convex because the original represented set is convex.

The already inspected primary
[Khachiyan--Porkolab Theorem 1.1](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf)
then applies with degree two, polynomial coefficient bits, and one quantified
block of size \(\rho\). Feasibility uses their added integer coordinate
fixed to zero. Its predicate-count-independent bound gives

\[
 \operatorname{bit}z^*
       \le N^C2^{O((k+1)^4(\rho+1))}.
\]

This is an existence bound, not a running-time claim for the implicit
formula. The integer box it supplies has FPT encoding length. Applying
the bounded-integer projection construction to that box preserves an
absolute input exponent, since \(r_x\le\rho\).

The distinction between \(r_x\) and \(\rho\) is essential to this
proof. The single rational SOC row

\[
                    \|(2,z-x)\|_2\le z+x
\]

has squared residual \(4-4zx\). With integral \(z\) and continuous
\(x\), its continuous Hessian block is zero, so \(r_x=0\), but its
full Hessian maps \((0,v)\) to \((-4v,0)\), so \(\rho=1\).
The coefficient of the eliminated variable would be \(-4z\), which
is not constant. Its real projection onto \(z\) is \((0,\infty)\),
illustrating the failure of the constant-matrix closed-projection argument
if the larger kernel is omitted. This example limits the proof, not the
truth of a possible stronger parameter theorem.

For a full PSD Hessian, \(Q_{xx}v=0\) gives
\((0,v)^TH(0,v)=0\), hence \(H(0,v)=0\). The converse is immediate.
Consequently \(r_x=\rho\) in the jointly convex quadratic case.

## 6. The MILP subroutine must itself be FPT

The initial generic reference to a fixed-integer-dimension polynomial
algorithm needed refinement. Lenstra's original paper, p. 538, describes
a polynomial degree depending on the integer dimension; that wording alone
does not establish the uniform exponent needed here.

The corrected manuscript imports
[Del Pia, Proposition 4, version 2](https://arxiv.org/html/2311.00099v2#S4.SS2),
which explicitly gives an FPT algorithm parameterized by the number of
integer coordinates for a rational polyhedron intersected with one PSD
quadratic inequality, with arbitrary continuous dimension. The reviewer
checked this primary statement and its setting directly. Taking the extra
quadratic inequality to be \(0\le0\) yields the needed MILP algorithm.
If its input length is \(L=f_1(k,\rho)N^{C_1}\), its running time is
\(f_2(k)L^{C_2}=f_3(k,\rho)N^{C_1C_2}\), with absolute \(C_1,C_2\).

As a separate cross-check, Bandyapadhyay--Fomin--Simonov's
[JCSS 2024 paper, Proposition 7.1](https://fedorvf.github.io/articles/2024/2024h.pdf)
states an explicit mixed-integer bound
\(O(p^{2.5p+o(p)}d^4L)\), where \(p\) counts integral coordinates
and \(d\) all coordinates. This also suffices after weakening it to
\(f(p)L^C\). The proof need not rely on an unstated interpretation of
the original fixed-dimension terminology.

## 7. Scope and verification limits

Bounded common range implies bounded Hessian matrix span:
\(h\le r(r+1)/2\). The reverse implication fails, even for one
full-rank PSD matrix. Thus this is a stronger parameterized running-time
guarantee on a narrower structural class, not two incomparable structural
restrictions. The proof establishes no FPT algebraic-output algorithm and
no full optimization theorem. Such claims require separate arguments.

The [prior audit](common-range-fpt-prior.md) correctly separates the
classical algebraic and integer-optimization inputs from the proposed
combination. This review does not independently establish that the
combination is new, publishable, or practically faster. The potentially
large parameter factors and precision bounds remain significant limitations.

Verification consists of independent symbolic reconstruction, manuscript
comparison, a counterexample to omitting cross terms, and direct inspection
of the imported primary theorem statements. No numerical experiment or Lean
formalization is claimed. Only targeted document checks are used; no
project-wide verification or CI inspection is performed.

A targeted `python -` check verified this review's local links, final
newline, whitespace, control characters, and paired inline and displayed
math delimiters. It passed. These document checks do not verify the proof.
