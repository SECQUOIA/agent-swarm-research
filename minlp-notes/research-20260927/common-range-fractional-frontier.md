# Exact affine-fractional optimization parameterized by a common nonlinear range

Date: 2026-09-28. Status: complete proof. The
[independent review](common-range-fractional-review.md) accepted the
alternative parametric proof and proposed the simpler kernel refinement
used below; the author checked that refinement independently. Its final
appendix also checks the PSD quadratic and mixed-model extension.
The separate [canonical-witness proof](common-range-fractional-witness.md)
supplies attainment and exact continuous output and has fresh independent
[field](fractional-common-range-field-review.md) and
[algorithm](fractional-common-range-algorithm-review.md) reviews.
The proof depends on the separate
[common-range feasibility theorem](common-range-fpt-frontier.md) and
[quasiconvex mixed-value theorem](quasiconvex-mixed-value-frontier.md).
Novelty is not established.

An affine-fractional objective can be added to the common-range framework
by retaining one additional continuous direction: the denominator's
variation along the otherwise linear variables. All remaining linear
variables can then be eliminated by the existing constant-matrix Farkas
argument. The resulting projected epigraph has only quadratic atoms and
a number of quantified variables bounded by the structural parameter.

## 1. Input and result

Let \(F\subseteq\mathbb R^k\times\mathbb R^n\) be a rational
closed convex feasible set given by native SOC constraints, quadratic
inequalities with positive-semidefinite full Hessians, or their
intersection, together with arbitrary rational affine rows, in variables
\((z,x)\). The integer variables are \(z\in\mathbb Z^k\).
Minimize

\[
                         p(z,x)/q(z,x),                    \tag{1}
\]

where \(p,q\) are rational affine and \(q>0\) on the entire real
set \(F\). No variable bounds are supplied. The positivity
hypothesis can, for example, follow from an input row \(q\ge1\).

For the native quadratic rows and the squared residuals of the cone rows,
let \(H_i\) be their full Hessians. Define

\[
 K_* = \{v\in\mathbb R^n:H_i(0,v)=0\text{ for every }i\},
 \qquad \rho=\operatorname{codim}K_* .                     \tag{2}
\]

This is the cross-aware common continuous nonlinear range used in the
unbounded feasibility theorem. It includes continuous directions
participating in integer-continuous products. It does not include the
affine numerator or denominator.

**Optimization theorem.** For some computable function \(f\) and absolute
constant \(C\), the problem can be classified as infeasible, unbounded
below, or having finite infimum in \(f(k,\rho)N^C\) bit operations.
In the finite case its exact value is returned as a minimal polynomial
and a rational isolating interval. Its degree is at most
\(f(k,\rho)\), and its coefficient bit length is at most
\(f(k,\rho)N^C\). Here \(N\) is the explicit rational input
length. An attained value has an optimal integer assignment whose
bit length obeys the same bound. The algorithm also decides attainment.
When attained, it returns an optimal integer assignment and all continuous
coordinates in one exact real algebraic representation, of total length
at most \(f(k,\rho)N^C\). The entire algorithm has this FPT running
time, with an absolute input exponent.

For the all-PSD model, \(\rho\) equals the common range dimension
of the continuous Hessians. This simplification need not hold when SOC
rows are present. Section 6 extends the result to a maximum of ratios
and to an explicitly restricted positive-denominator domain.

## 2. Retain the denominator direction

Let \(q_x\) be the denominator's continuous gradient. Refine the
eliminated kernel to

\[
                   K'=K_*\cap\ker(q_x^T),\qquad
                   r=\operatorname{codim}K'\le\rho+1.     \tag{3}
\]

A rational basis and complement give an invertible change

\[
                    x=T_1u+T_0v,\qquad u\in\mathbb R^r.  \tag{4}
\]

The transformation and inverse have polynomial-bit rational coefficients.
All native quadratic rows, squared cone rows, sign conditions, and affine rows become

\[
                            Cv\le b(z,u),                  \tag{5}
\]

where \(C\) is constant rational and \(b\) is quadratic. This
follows from \(K'\subseteq K_*\): the full Hessians kill every
eliminated continuous direction, so there are no products involving
\(v\), including products with integer coordinates. Original affine
equalities are represented by both signs. Cone sign conditions are
retained, so (5) is equivalent to the original native system.

The denominator no longer depends on \(v\). Write

\[
           p=p_v^Tv+p_0(z,u),\qquad q=q_0(z,u).
\]

The epigraph threshold at a free real \(t\) is

\[
                   p_v^Tv\le t q_0(z,u)-p_0(z,u).          \tag{6}
\]

Its left-hand coefficient row is constant rational. Its right-hand side
is quadratic in \((z,u,t)\). Thus (5)--(6) have the form
\(\widehat C v\le\widehat b(z,u,t)\), with constant rational
\(\widehat C\), and all components of \(\widehat b\) of degree
at most two.

By the established Farkas projection lemma, feasibility in \(v\) is
equivalent to

\[
                  \lambda^T\widehat b(z,u,t)\ge0
 \quad\text{for every extreme ray of }
                  \{\lambda\ge0:\widehat C^T\lambda=0\}. \tag{7}
\]

Extreme-ray generators have supports of size at most
\(\operatorname{rank}\widehat C+1\) and can be normalized using
constant rational minors. Consequently the projected atoms satisfy

\[
 \deg P_j\le2,\qquad
 \operatorname{bit}P_j\le N^{C_0},\qquad
 \log(\#\{P_j\}+1)\le N^{C_0},                           \tag{8}
\]

for an absolute constant \(C_0\). The exponential family is used
only to prove degree and height bounds. It is never generated by the
final algorithm.

Retaining the numerator direction is unnecessary: its coefficient row
in (6) is already constant. If the denominator gradient vanishes on
\(K_*\), no additional direction is needed.

## 3. Finite-value and integer-witness bounds

The exact projected epigraph is

\[
 E=\{(z,t):\exists u\in\mathbb R^r:
                         \bigwedge_j P_j(z,u,t)\ge0\}.     \tag{9}
\]

Every weak threshold slice is convex, because before projection it is
the original convex set intersected with \(p-tq\le0\), an affine
inequality for fixed \(t\). Positivity of \(q\) makes this
inequality equivalent to the ratio threshold. Strict slices are
nested unions of weak slices and are also convex. Joint convexity
of \(E\) is not required.

Quantifier elimination of \(u\), using the individual degree and
coefficient bounds independent of atom count, gives an implicit
quantifier-free description with

\[
                    d\le f_1(r),\qquad
                    H\le f_2(k,r)N^{C_1}.                 \tag{10}
\]

The quasiconvex mixed-value theorem is linear in the incoming coefficient
bit length. It therefore gives, for every finite infimum \(\theta\),

\[
 \deg\theta\le f_3(k,r),\qquad
 \operatorname{bit}\operatorname{minpoly}(\theta)
                      \le f_4(k,r)N^{C_2},                 \tag{11}
\]

with absolute \(C_2\). Since \(r\le\rho+1\), these are the
claimed bounds. The weak slice \(E_\theta\) is convex, so the
same theorem gives an optimal integer vector of bit length
\(f_5(k,r)N^{C_3}\) whenever the infimum is attained.

## 4. Exact value recovery

First run the common-range exact feasibility algorithm. For a
feasible instance, (11) gives an effective universal finite-value root
bound \(M\). A feasible threshold \(p-(-M-1)q\le0\) is equivalent
to unboundedness below. Otherwise, rational threshold bisection and
algebraic recognition recover the finite value.

For a rational threshold, the additional row \(p-tq\le0\) is
an affine row in the original variables. It leaves \(k,\rho\)
unchanged. The threshold oracle is therefore FPT in the original
parameters, without actually performing the split (4). Threshold bit
lengths, the number of queries, recognition precision, and output size
are all \(f(k,\rho)N^C\). Composing these bounds with the FPT
feasibility oracle proves the value part of the theorem.

The feasibility oracle also covers a mixture of PSD quadratic and SOC
rows. One explicit reduction writes a rational PSD row as
\(\sum_j a_j\ell_j(w)^2+b^Tw+c\le0\), with \(a_j>0\) rational,
using rational LDL elimination. Introduce continuous \(s_j\) and rows

\[
 \|(2\ell_j(w),s_j-1/a_j)\|\le s_j+1/a_j,\qquad
                   \sum_j s_j+b^Tw+c\le0.
\]

These encode \(s_j\ge a_j\ell_j(w)^2\). Their squared residuals
are \(4\ell_j(w)^2-4s_j/a_j\); all new continuous columns are
Hessian-zero. Since the original PSD kernel is the common kernel of the
\(\ell_j\), the reduction preserves \(\rho\) exactly and has
polynomial encoding length. It therefore permits direct use of the SOC
oracle without an unstated mixed-model assumption.

## 5. Attainment and exact optimizers

A small optimal integer-assignment bound alone does not decide attainment:
individual continuous fibers can have unattained infima. The
[canonical-witness theorem](common-range-fractional-witness.md) supplies
the additional uniform bound and recovery algorithm. Its mechanism is
as follows. At an algebraic optimal value \(\theta\), the optimal-level
equation has constant rational coefficients in \(v\):

\[
                   p_v^Tv=\theta q_0(z,u)-p_0(z,u).         \tag{12}
\]

After fixing an integer assignment, Farkas elimination of these
constant rational rows shows that the projected optimal set in \(u\)
is closed and convex. Choose its unique minimum-norm point \(u_*\),
then the unique minimum-norm \(v_*\) in that optimal fiber. If
\(D=\deg\theta\), the witness theorem proves

\[
 [\mathbb Q(\theta,u_*,v_*):\mathbb Q]\le D3^{2r},\qquad
 \operatorname{encoding}(\theta,u_*,v_*)\le f(k,\rho)N^C.    \tag{13}
\]

The bound holds uniformly after substituting any integer assignment in
the conditional attaining-integer box from Section 3. Thus one computable
rational box in \((u,v)\) contains the specified canonical point of
every nonempty optimal-level fiber in that integer box. No enumeration
of the integer assignments is needed.

Intersect the original mixed-integer domain with both boxes. It is a
finite union of compact continuous fibers. On this set the ratio is
continuous, so a nonempty boxed domain has an attained minimum \(\beta\).
The original finite value \(\theta\) is attained exactly when the
boxed domain is nonempty and \(\beta=\theta\). The forward direction
uses the small attaining integer vector and its canonical continuous
point; the reverse direction uses compactness. The value algorithm
decides this condition.

When it holds, integer interval bisection preserves boxed value
\(\theta\) and fixes an optimal integer vector using polynomially
many queries in its bit bound. In the selected fiber, rational norm
and coordinate cuts in \(u\), combined with the full continuous box,
give an exact optimal-set oracle: a nonempty compact cut meets the
optimal set exactly when its fractional minimum is \(\theta\).
Norm bisection and the convex projection inequality approximate the
same minimum-norm \(u_*\) at every precision. Each precision request
restarts from the original box.

Approximate \(v_*\) by rational minimum-norm QPs with outward-rounded
right-hand sides; the rational-matrix Hoffman bound controls their error.
Common-field recognition of the fixed tuple \((\theta,u_*,v_*)\)
then gives exact output. All value queries have FPT input length and
an absolute polynomial input exponent. The linked witness proof gives
the arithmetic bound, quantitative error estimate, and full composition.

A full norm bound on the original \(x\) must not simply be introduced
as a new oracle constraint: its squared Hessian has full rank and can
increase the common nonlinear range to \(n\). A norm constraint on
\(u\) preserves a parameter bounded by \(\rho+1\). The distinction
is unnecessary for the older matrix-span parameter but essential here.

## 6. Maximum of ratios and positive-denominator domains

For an objective \(\max_j p_j/q_j\), with each denominator positive
on the entire original closed feasible set, retaining all denominator
gradients on \(K_*\) gives the same value argument with
\(r\le\rho+\ell\), where \(\ell\) is their joint rank on that
kernel. The numerator gradients need not be retained; every threshold
row has constant coefficients in the remaining \(v\). The resulting
optimization theorem is FPT in \((k,\rho,\ell)\). At the optimal
value, the optimal set is exactly the simultaneous weak thresholds
\(p_j-\theta q_j\le0\). Their eliminated-variable normals are
constant rational, so the same canonical-point proof gives attainment
and exact continuous output. It is not claimed FPT in \((k,\rho)\)
when \(\ell\) is unrestricted.

The same conclusions hold if the problem is explicitly defined on the
open domain \(F\cap\{q_j>0\text{ for all }j\}\). Introduce one
shared continuous variable \(s\) and the rational SOC rows

\[
                 \|(2,q_j-s)\|\le q_j+s\quad\text{for all }j. \tag{14}
\]

They are equivalent to \(q_js\ge1\) and \(q_j+s\ge0\), which
force \(q_j,s>0\). Conversely, every original feasible point lifts
by taking \(s\ge\max_j1/q_j\). Thus the closed lifted set has
exactly the intended projection, with the same objective values and
the same attainment status. Denominators are now positive throughout
that closed set, as required by the preceding proof.

The new cross-aware kernel contains
\(\{(v,0):v\in K_*,\ q_{j,x}^Tv=0\ \forall j\}\), so its
codimension is at most \(\rho+\ell+1\). Each denominator gradient
annihilates the new kernel, so no additional denominator directions
are needed there. For a single ratio the increase is at most two.
Hence the parameter families remain \((k,\rho)\) for one ratio and
\((k,\rho,\ell)\) for a maximum. A direct compactness argument on
the unlifted open domain would be invalid; all compact queries use
the closed lift. The [witness note](common-range-fractional-witness.md)
records the kernel calculation and its separate review.

An alternative proof without enlarging the retained dimension gives
cubic projected atoms for a single varying threshold row. It is recorded
in the supporting [parametric Farkas lemma](one-row-parametric-farkas.md).
That lemma is not needed for the simpler quadratic proof above.

## 7. Prior comparison and verification

The kernel refinement and Farkas elimination are applications of rational
linear algebra and classical LP duality. The parameterized optimization result
comes from combining them with the quantitative quasiconvex value theorem
and the common-range feasibility oracle. No novelty claim is made for
fractional threshold reformulation or for the kernel refinement itself.

The strongest fractional predecessor currently identified is
[Espinoza--Fukasawa--Goycoolea (2010), *Lifting, tilting and fractional
programming revisited: a study on mixed integer linear sets*](https://mgoycool.github.io/papers/10espinoza_orl.pdf).
Theorem 2.3 and Section 5 give point or recession-ray values and
asymptotically optimal sequences for rational mixed-integer linear
fractional programs. The result here concerns SOC and native convex
quadratic feasible sets, with an FPT bound in their common continuous
nonlinear range and exact algebraic optimizer output. This comparison
does not establish priority.

The independent reviewer verified the alternative parametric proof and
then proposed retaining the denominator direction as a simpler route.
The author rechecked (3)--(8) independently. The previous exact checks
of 600 rational linear systems apply to the separate parametric lemma;
they are not a computational verification of the general FPT theorem.
An inline SymPy check verified a nontrivial kernel refinement with an
integer-continuous cross term, the one-direction rank increase, and the
constant threshold row after substitution. The PSD extension has a
separate targeted review in the value review's final appendix. The
canonical-witness proof and its two fresh reviews verify the field bound,
uniform-box argument, compact optimal-set queries, and FPT composition.
The shared reciprocal lift has a separate
[positive-domain review](common-range-positive-domain-review.md).
The final targeted inline Python check passed for this note and the
small arithmetic-wording clarification in the convex mixed-value note:
two documents, 18 local links, whitespace, control characters, and paired
math delimiters. These are document checks, not mathematical verification.
The main proof depends on the separately reviewed algebraic bounds and
common-range threshold oracle. No project-wide verification or CI
inspection was performed.
