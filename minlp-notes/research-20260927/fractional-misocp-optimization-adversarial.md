# Fresh adversarial review of quasiconvex values and fractional MISOCP

Date: 2026-09-28. Reviewed manuscript:
[quasiconvex-mixed-value-frontier.md](quasiconvex-mixed-value-frontier.md),
with particular attention to Section 6.2. I did not propose the
value-variable lift or develop this proof. I read the complete saved
manuscript and independently reconstructed the fractional optimization
argument. A fresh separate reviewer audited Sections 1--5 and 7 in
[quasiconvex-transition-independent-audit.md](quasiconvex-transition-independent-audit.md);
I read that audit and independently checked its main deductions.

**Finding:** no substantive gap was found. Under positivity of the affine
denominator on the entire real SOC feasible set, the proof gives exact
classification, finite-value recovery, attainment decision, and an
algebraic optimizer for fixed integer dimension and continuous squared-
Hessian span. Its running-time exponent may depend on both parameters.
The general quasiconvex finite-value theorem and its separate weak-slice
condition for a small attained integer witness also pass this review.

During review the author made explicit that the continuous box retains
every eligible fiber's canonical optimizer, empty compact cuts return
false, and each approximation request restarts from that box. I reread
those additions. They clarify the already referenced recovery argument;
no mathematical repair was needed. This is not formal verification,
a novelty finding, or an FPT result.

## 1. The transition argument does not assume joint convexity

Strict sublevels are nested. Their affine hulls are nested when nonempty,
and their spaces of two-sided bounded linear forms are reverse nested.
Within either nested family, equality of dimensions forces equality of
the spaces. Each dimension predicate changes truth at most once. The
affine-dimension-zero predicate separately records nonemptiness, so the
empty-set case is not lost. This justifies at most \(2k+1\) transition
levels and constancy on the open complementary intervals.

The defining dimension formulas use only \(O(k^2)\) variables and
degrees bounded in terms of \(d,k\). Quantitative elimination therefore
bounds every finite transition level independently of the atom count.
A value equal to such a level is handled immediately; the proof does
not assert constancy across the transition itself.

For a value inside a transition interval, the cap construction avoids
using the unknown value as an algebraic coefficient. At a finite right
endpoint \(\beta\), the convex strict slice \(C_\beta\) contains
an integer point. Its algebraic endpoint description supplies a bounded
integer witness. A common-field sample then supplies an actually feasible
level \(s_0<\beta\) in that integer fiber. Since
\(\theta\le s_0\), a rational number between \(s_0\) and
\(\beta\) is the required cap. Separation is applied to two numbers
already having controlled representations, not to the unknown
\(\theta\). For an infinite right endpoint, the total projection
is a nested union of convex sets; its integer witness and a fiber sample
give a controlled cap directly.

Below the optimum but inside the same transition interval, the strict
slice is nonempty. In the full-dimensional branch, its closure is
lattice-free in the interior sense because
\(\operatorname{int}\overline C=\operatorname{int}C\subseteq C\).
Maximal lattice-free containment gives a nonzero bounded rational form.
The constant bounded-form space on the interval transfers that form to
the cap. The lower-dimensional branch instead rationalizes a sampled
affine equation before any full-dimensional argument is used. Both
branches preserve an infimizing integer sequence and reduce dimension.

The affine substitutions retain the original polynomial degrees and
increase logarithmic coefficient heights linearly. Common-field sampling,
rational-part extraction, and lattice parametrization have the needed
polynomial dependence on field degree. Thus the preceding reviewed
coefficient accounting still gives degree \(d^{G(k)}\) and coefficient
bits \((H+1)d^{G(k)}\). In dimension zero, the finite value is exactly
the transition from empty to nonempty strict slices.

The arithmetic and lattice-free imports are the same primary statements
checked in the preceding bounded-form audit:
[Khachiyan--Porkolab](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
Theorem 1.1, Propositions 2.1--2.2 and Corollary 2.3, and
[Basu--Conforti--Cornuejols--Zambelli](https://personal.lse.ac.uk/zambelli/papers/lattice-free.pdf),
Theorem 2(i) and Corollary 17 in the author version. The fresh transition
reviewer also inspected them. Their encoding bounds are distinct from
their formula-size-dependent running times.

## 2. Strict and weak slices have different roles

The finite-value induction needs only convex strict slices. The integer
witness theorem for an attained optimum is applied to the weak slice
\(E_\theta\), so its convexity is an additional condition. Upward
closure alone does not imply it. Closed vertical fibers do give the
intersection identity in the manuscript, including empty fibers and
fibers equal to the whole line.

The Pell example correctly separates the two conclusions. I checked
the infinite argument: division by the fundamental positive norm-one
unit leaves an integral unit in the stated interval; the remaining
nonnegative second coefficient is zero. The valuation identity follows
from the odd-index congruence and the doubling formula with odd first
coefficient. Requiring divisibility by \(2^a\) forces an index at
least \(2^{a-1}\), and then at least \(2^a\) binary digits in the
first coordinate. Its weak optimal slice is nonconvex, while the value
is the small transition level zero. It challenges the omitted witness
hypothesis, not the finite-value theorem.

## 3. Positive affine denominators preserve the threshold class

The hypothesis is \(q>0\) throughout the original real feasible set
\(F\). It is not merely positivity at integer-feasible points.
Consequently, for every real threshold \(t\), both strict and weak
ratio sublevels are intersections of \(F\) with the corresponding
affine halfspace \(p-tq<0\) or \(p-tq\le0\). Their projections
are convex, even when they are not closed. In particular the weak
optimal slice satisfies the extra condition needed to bound an optimal
integer assignment.

For a rational threshold, the added row is affine in all optimization
variables and does not alter \(k\) or the native continuous Hessian
span \(h\). When the threshold is a free parameter in the compressed
formula, the coefficient of each continuous variable is affine in that
parameter and the constant term is at most quadratic in \((z,t)\).
These are the existing rank-chart coefficient degrees. No bilinear
threshold term is being treated as an affine function jointly in its
parameter and variables.

Thus the finite-value bound and rational threshold oracle give exact
value recovery independently of the later attainment argument. The
test below the universal finite-value lower bound correctly detects
unboundedness, including escape with an arbitrarily small positive
denominator. No global positive lower bound on \(q\) is assumed.

## 4. The rational value-variable lift supplies the missing optimizer bound

Fix an integer assignment. The row
\[
                         p(x)-v q(x)\le0
\]
is a rational quadratic inequality. Since \(q>0\), it says exactly
\(v\ge p(x)/q(x)\). Together with the original weak squared SOC
rows and their signs, it defines a closed rational quadratic system.
There is no need to add a strict positivity constraint to this system:
positivity is already valid on all points satisfying the original rows.

The original continuous Hessians are embedded with a zero value-variable
row and column. The new row adds one matrix to their span, hence at most
one direction, regardless of the number of original continuous variables.
The system may be nonconvex, but the invoked
[nonconvex attained-optimizer theorem](nonconvex-attainment-and-optimizer.md)
allows that. Its objective is the rational affine coordinate \(v\).
No algebraic optimal value is supplied as a coefficient of that theorem.

If the ratio attains its finite minimum \(\theta\), every lifted
optimizer has \(v=\theta\). Its original-coordinate optimal set is
\[
                   F_z\cap\{p(x)-\theta q(x)=0\},
\]
which is closed and convex. The minimum-norm lifted point therefore
minimizes \(\|x\|^2+\theta^2\) on this set and has exactly its
unique minimum-norm \(x\). The optimizer theorem's common-field bound
applies to this canonical tuple, rather than only to an arbitrary
optimizer. Squared norms are polynomial expressions in that same field;
their degree and height bounds require no product of coordinate degrees.

The optimal integer bound supplies polynomial-bit assignments for fixed
\((k,h)\). Their rational fiber coefficients have a uniform polynomial
bit bound. Applying the lifted theorem uniformly therefore gives a
continuous box containing the canonical point of every attaining fiber
inside the integer box. This is the stronger property needed after
integer bisection selects a fiber.

## 5. Compact ratio queries decide attainment and recover one fixed point

The original SOC set is closed. Its intersection with both finite boxes
and the integer lattice is compact. On any nonempty such domain,
continuity and strict positivity of \(q\) imply a positive minimum
denominator and continuity of the ratio. Its fractional minimum is
therefore attained. The algorithm need not compute that denominator
minimum or its separation from zero.

If the original optimum exists, the conditional boxes retain one.
Conversely, equality of a nonempty boxed minimum with the original
infimum gives an original optimizer by compactness. This proves the
attainment test without circularity: exact boxed ratio values use the
already established value algorithm, not the attainment algorithm.

For integer selection, an empty tested half is rejected. Every nonempty
tested half is compact, so equality of its minimum with \(\theta\)
certifies an attained optimizer. An equal unboxed infimum would not
supply that conclusion. Storing current integer endpoints keeps the
number of rows fixed, and only polynomially many bisections are needed.

For the selected fiber, let \(x^*\) be its canonical optimizer.
The universal continuous box contains it. Any rational coordinate cut
and rational norm cap within this box gives another compact SOC domain.
If nonempty, its exact ratio minimum equals \(\theta\) exactly when
it meets the original optimal set. This simulates optimal-set feasibility
without an algebraic-coefficient oracle.

The norm cap has the rational SOC form
\(\|(2x,r-1)\|\le r+1\), for rational \(r\ge0\), and adds
at most one native Hessian direction. Only one current norm row and two
current endpoints per coordinate are retained. Thus oracle parameters
remain fixed, with span at most \(h+1\), independently of accuracy.

Norm bisection gives a feasible cap at most \(\delta^2/16\) above
\(\|x^*\|^2\). Convex minimum-norm optimality makes every optimal
point under that cap lie within \(\delta/4\) of \(x^*\).
Coordinate bisection preserves at least one such point, and its final
box midpoint approximates \(x^*\). Restarting from the universal box
for every accuracy request ensures all approximations target this same
tuple. The manuscript now states that restart explicitly.

The required degree, height, and recognition precision are polynomial
in input length for fixed \((k,h)\). Repeated radius, ratio-value,
comparison, and approximation calls compose polynomial exponents
depending only on those parameters. The proof makes no FPT claim and
needs no sharper coefficient-sensitive composition to establish its
stated polynomial-time result. Common-field recognition returns the
specified optimizer. Its ratio can be checked in the point's own field:
the denominator is nonzero and \(p(x)/q(x)\) belongs to that field.

## 6. Distinct exact checks and limitations

I ran a targeted inline `python -` command with SymPy for three
fractional boundaries, without rerunning the existing Pell script.

First take \(x\ge\sqrt2\), represented by
\(\|(1,1)\|\le x\), impose \(y\ge2x-1\), and minimize
\(x/(x+1)\). The optimum is
\(\theta=2-\sqrt2\). Its unbounded optimal set has canonical
point \((\sqrt2,2\sqrt2-1)\), with squared norm
\(11-4\sqrt2\). The command checked the objective identity,
positive derivative, the value polynomial \(T^2-4T+2\), and the
norm polynomial \(T^2-22T+89\). It also checked that the native
cone Hessian and the new row \(x-v(x+1)\) span exactly two
directions in \((x,y,v)\). This tests irrational exact output,
canonical selection on an unbounded optimal set, and the one-direction
increase.

Second, on \(x,y\ge0\), \(xy\ge1\), the affine denominator
\(q=x\) is positive everywhere but has global infimum zero. The
ratio \(y/x\) has unattained infimum zero. In a box of radius
\(R\ge1\), it has minimum \(1/R^2\), attained at
\((R,1/R)\): the lower bound follows from
\(y/x\ge1/x^2\ge1/R^2\). The command checked the cone residual
and boundary substitution.

Third, use \(z\in\{0,1\}\), \(x,y\ge0\),
\(xy\ge(1-z)^2\), and ratio \(y/(x+1)\). Both fibers have
infimum zero, but only \(z=1\) attains it. In a box of radius
\(R\ge1\), the \(z=0\) minimum is
\(1/[R(R+1)]>0\), while the \(z=1\) minimum is zero.
The command checked the rational SOC residual and both boundary points;
the minimum formula follows from
\(y/(x+1)\ge1/[x(x+1)]\). This tests why compact fiber selection
is essential for fractional objectives too. All checks passed.

The separate transition audit records additional exact examples and a
larger Pell-index check. I independently rechecked its sharp transition
construction, finite-right-endpoint cap example, and field expansion.
Those examples and all finite calculations support particular identities;
they do not establish the general geometric or complexity bounds.

Targeted local-link, paired-math-delimiter, control-character, whitespace,
and final-newline checks passed for this review and the new transition
audit, as did a scoped `git diff --check`. No project-wide verification,
CI inspection, or Lean formalization was performed. The theorem still
depends substantively on the separate compressed projection, exact
feasibility, nonconvex optimizer encoding, and recognition results.
No practical speedup or publication priority is established by this review.
