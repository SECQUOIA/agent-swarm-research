# Review of exact fractional MISOCP value elimination

Date: 2026-09-28. I independently read Sections 1–6 of
[the fractional common-range manuscript](common-range-fractional-frontier.md)
and checked its parametric elimination and FPT composition. No gap was found
in the value theorem, conditional on the separate common-range feasibility
and quasiconvex mixed-value theorems. The original proof remains valid, but
Section 4 below gives a simpler route using one additional retained
continuous direction. That alternative was contributed during this review,
so its adoption requires an independent check by the author or another
reviewer; this review is independent of the original parametric proof.

No claim about FPT attainment or continuous optimizer recovery follows from
this review. Those require the additional witness bounds identified in the
manuscript. Novelty was not established or independently audited here.

## 1. Farkas signs and unbounded multiplier polyhedra

Fix real values of \((z,u,t)\) and abbreviate the linear system by

\[
                 Cv\le b,\qquad a^Tv\le\beta.
\]

Farkas' alternative requires

\[
 \lambda^Tb+\mu\beta\ge0
 \quad\text{whenever}\quad
 \lambda\ge0,\ \mu\ge0,\ C^T\lambda+\mu a=0.
\]

The signs in the manuscript are correct. When \(\mu=0\), this is
exactly feasibility of the native system. When \(\mu>0\), division
by \(\mu\) leaves

\[
 \Lambda_t=\{\lambda\ge0:C^T\lambda=-a(t)\},\qquad
                  \lambda^Tb+\beta\ge0.
\]

The nonnegative orthant has no lineality, so neither does \(\Lambda_t\).
If it is nonempty, its vertices and recession cone give

\[
 \Lambda_t=\operatorname{conv}(\operatorname{vert}\Lambda_t)
              +\{r\ge0:C^Tr=0\}.
\]

Native feasibility already supplies \(r^Tb\ge0\) on the recession
cone. For a convex combination of vertices, the single constant
\(\beta\) distributes because the convex coefficients sum to one.
Consequently checking the vertex inequalities suffices, even when the
multiplier polyhedron is unbounded. No finite optimum of a primal LP is
assumed.

There is also an elementary support-reduction proof of the decomposition
needed here. A feasible multiplier whose positive-support columns of
\(C^T\) are dependent has a nonzero supported kernel vector. If that
vector has both signs, the multiplier lies between two feasible points
with smaller supports. If it has one sign, subtract a nonnegative multiple
until a coordinate vanishes, recording a recession contribution. Repeating
this process leaves independent-support feasible vectors and nonnegative
kernel directions. Applying the same support argument to a kernel direction
reduces it to the positive circuits that generate the native cone.

If \(\Lambda_t\) is empty, no positive-\(\mu\) certificate exists.
The vertex conditions are therefore correctly vacuous. This conclusion is
used only together with native feasibility. If the native system is empty,
its ray conditions reject the parameter point already.

## 2. Vertex formulas, ranks, and degenerate thresholds

A feasible multiplier is a vertex exactly when its positive-support rows
of \(C\) are linearly independent. Dependence permits a sufficiently
small perturbation in both directions, contradicting extremality.
Conversely, in any convex decomposition of an independent-support
multiplier, its zero coordinates force both summands to have that support;
the independent equations then force the summands to coincide.

For an independent row set \(I\), choose columns \(J\) so that
\(C_{I,J}\) is square and nonsingular. The proposed candidate is

\[
              \lambda_I(t)=-(C_{I,J}^T)^{-1}a_J(t).
\]

Its inverse is fixed and rational. The candidate is affine in \(t\),
and the remaining coordinates of the equation
\(C_I^T\lambda_I=-a(t)\) are essential consistency guards.
They cannot be omitted when \(C\) has deficient rank. A guard may hold
only at an isolated threshold, and the Boolean implication retains that
case. Allowing zero coordinates in a candidate is harmless because its
actual support is a subset of an independent set.

The empty support must be included. When \(a(t)=0\), its condition
is exactly \(\beta\ge0\). Without it, a false zero-normal row would
be accepted whenever all other multiplier candidates disappear. The
manuscript includes this case. Zero rows of \(C\), a zero native ray
cone, and a multiplier right-hand side outside the span of \(C^T\)
also cause no missing condition.

## 3. Degree, coefficient, and FPT bounds

The splitting hypothesis must use the full Hessians on continuous
directions:

\[
           K_* = \{v:H_i(0,v)=0\text{ for every }i\}.
\]

Using only the \(xx\)-Hessian kernels would leave possible \(zv\)
products and a parameter-dependent matrix \(C\). The displayed
constant-minor argument would then no longer apply. The manuscript uses
the required cross-aware kernel.

Rational kernel bases, coordinate inverses, native ray generators and
the fixed inverses above have polynomial coefficient bit length in the
explicit input. Their sizes can depend on the ambient dimensions, but
only through an absolute polynomial in input length. All denominators
are constant rational numbers. Clear them with positive common
denominators in inequalities, so no threshold-dependent sign choice or
division by a vanishing polynomial is introduced.

The native right-hand side \(b(z,u)\) has degree at most two.
The vector \(\lambda_I(t)\) is affine in \(t\), and
\(\beta=tq_0-p_0\) has degree at most two. Therefore

\[
              \beta+\lambda_I(t)^Tb(z,u)
\]

has total degree at most three. Each atom has polynomial coefficient
bit length. There are exponentially many row subsets at most; the
number of guards attached to one subset is polynomial. These facts
give the asserted implicit-description bounds independently of whether
support enumeration would be computationally practical.

Eliminating the \(\rho\) retained variables consequently gives
individual degree bounded by a function of \(\rho\), and individual
coefficient bits bounded by \(f(k,\rho)N^C\) with an absolute
\(C\). The atom-count-independent quasiconvex value theorem preserves
an absolute input exponent because its coefficient bound is linear in
the incoming bit bound. The number of atoms is not used as the size of
a constructed input to the final algorithm.

For a rational threshold, the original inequality \(p-tq\le0\)
is affine in \((z,x)\) and adds no Hessian. Thus the original
common-range feasibility oracle has the same parameters \((k,\rho)\).
The value bound controls the required number and precision of threshold
queries and the algebraic recognition work. Polynomial composition
preserves the FPT form \(f(k,\rho)N^C\).

Denominator positivity is required on the entire real SOC feasible set,
as stated in the manuscript. It gives equivalence between ratio and affine
thresholds, upward closure of the projected epigraph, and convex weak
threshold slices. Positivity only on selected integer fibers would not
justify all of these real-projection arguments. A uniform positive lower
bound on the denominator is not needed for the value proof.

## 4. A simpler constant-matrix proof

For the single-fraction theorem, replace the eliminated kernel by

\[
                  K'=K_*\cap\ker(q_x^T).
\]

Its codimension is at most \(\rho+1\). Choose a rational split
\(x=\widehat T_1u+\widehat T_0v\) for this kernel. Every native
quadratic still has a constant coefficient on \(v\), because
\(K'\subseteq K_*\). Now the denominator has no \(v\) term:

\[
 p=p_v^Tv+p_0(z,u),\qquad q=q_0(z,u).
\]

The threshold becomes

\[
             p_v^Tv\le tq_0(z,u)-p_0(z,u).
\]

The entire matrix of the linear system, including this extra row, is
constant and rational. Its right-hand sides have degree at most two in
\((z,u,t)\). The existing constant-matrix Farkas projection lemma
therefore eliminates \(v\) using quadratic atoms with polynomial
coefficient bits. Only \(\dim u\le\rho+1\) variables remain to
be eliminated by real quantifier elimination.

Since adding one to a parameter can be absorbed into its parameter
function, this yields exactly the same FPT value conclusion in
\((k,\rho)\). It avoids all parametric vertices, and the degree of
the implicit projection is two rather than three. The original cubic
lemma is a valid supporting result, but is unnecessary for this
particular FPT theorem.

The same observation works for several simultaneous fractional threshold
rows by retaining the denominator-gradient directions on \(K_*\).
If those restrictions span \(\sigma\) dimensions, the retained
dimension is at most \(\rho+\sigma\). Numerator gradients need not
be retained: their coefficients on the eliminated variables are constant.
This is an implication of the linear elimination calculation, not a
separate reviewed optimization theorem in this file.

## 5. Targeted verification

I ran an inline `python -` calculation using exact rational arithmetic
and SymPy, with deterministic seed `20260928`. It generated 600 systems
with one or two eliminated variables and one to four native rows. Native
and objective coefficients ranged over small integers; tested thresholds
were \(-2,0,3\). The calculation compared:

- native extreme-ray conditions and all guarded independent-support
  multiplier candidates; and
- independent Fourier–Motzkin elimination of the complete primal system.

All 600 comparisons agreed. The cases included zero objective normals,
rank-deficient native matrices, empty systems, and unrestricted objective
directions. This checks finite examples and implementation of the signs
and guards. The support-reduction and linear-algebra arguments above
establish the universal claims.

Only this review document received local formatting checks. No
project-wide verification or CI inspection was performed.

## Appendix: native PSD quadratics and mixed PSD/SOC models

Added 2026-09-28. This targeted extension review found no obstruction to
allowing rational native quadratic inequalities with **full PSD Hessians
in all \((z,x)\) variables**, rational SOC rows, or their intersection.
PSD continuous blocks alone are insufficient: the real feasible set and
its projected threshold slices must remain convex.

For the union of native PSD Hessians and squared SOC Hessians, use
\(K_*=\{v:H_i(0,v)=0\ \forall i\}\), as before. Each row has a
constant rational coefficient on the eliminated variables. The denominator
refinement and fractional-threshold Farkas proof are unchanged. The
common-range feasibility proof also permits a mixture: its radius and
gap arguments apply to the entire quadratic family, and each original
row receives its own already established rational outer lift.

An independently checked alternative removes any ambiguity about the
mixed-model oracle. Write a PSD row, after absorbing any factor of one
half into its matrix, as

\[
 g(w)=\sum_j d_j(\ell_j^Tw)^2+a^Tw+c\le0,\qquad d_j>0,
\]

using rational LDL decomposition. Introduce continuous \(s_j\), the
affine row \(\sum_js_j+a^Tw+c\le0\), and rational cones

\[
 \|(2\ell_j^Tw,s_j-1/d_j)\|_2\le s_j+1/d_j.
\]

Each cone is exactly \(s_j\ge d_j(\ell_j^Tw)^2\); the right-hand
side sign follows from this inequality. Its squared Hessian is
\(8\ell_j\ell_j^T\) on \(w\) and zero on all auxiliary directions.
PSD implies

\[
 Q(0,v)=0\quad\Longleftrightarrow\quad
                 \ell_j^T(0,v)=0\quad\text{for every }j.
\]

Consequently the common continuous kernel becomes exactly the old
\(K_*\) times the full space of new auxiliary variables. The conversion
preserves \(\rho\), introduces no integer variables, and has polynomial
encoding size. Intersecting with existing SOC rows preserves this identity.
A fresh narrow reviewer independently confirmed the equivalence, rational
coefficient bounds and kernel preservation.

If **all** native quadratic Hessians are PSD, then
\(\ker H_{i,xx}=\{v:H_i(0,v)=0\}\), so \(\rho=r_x\).
This equality must not be asserted for a mixed system with indefinite
squared SOC Hessians. For example a row \(4-4zx_j\le0\) has zero
\(xx\)-Hessian but excludes the \(x_j\) direction from \(K_*\).

The denominator hypothesis remains positivity on the entire original
closed real feasible set. It survives integer substitution, affine
restrictions and compact boxing. Thus each nonempty compact query domain
has a continuous positive-denominator objective and an attained minimum.
Adding a strict domain condition \(q>0\) instead would not justify that
compactness argument.

The optimizer queries use \(u=Lx\) for the fixed denominator-refined
kernel \(K'\). A native norm row \(\|u\|^2\le t\) has PSD Hessian
\(2L^TL\); its SOC encoding has squared Hessian \(8L^TL\).
Both annihilate \(K'\). The augmented common range is therefore at most
\(\rho+1\), or \(\rho+\ell\) for denominator rank \(\ell\).
Affine box and coordinate rows add no Hessians. This holds for native PSD,
native SOC and mixed inputs; a full norm row on all original continuous
coordinates is still inadmissible for this parameter bound.

I read the separate
[field review](fractional-common-range-field-review.md) and
[recovery review](fractional-common-range-algorithm-review.md).
Their arguments use convexity, the rational constant-matrix fiber,
the controlled field bound, compact value comparisons and the norm cuts
just checked. None requires all native rows to be of the same type.
The extended value oracle therefore supplies the missing model-specific
dependency for their complete optimization conclusion. Every subsequent
query has parameters bounded by \((k,\rho+1)\) and encoding length
\(f(k,\rho)N^C\); the stated absolute-exponent arithmetic and oracle
bounds compose to the same FPT form. This verifies the model extension,
not a replacement independent review of those entire optimizer proofs.

A targeted inline `python -` SymPy calculation checked a rational PSD
matrix built from \(\frac23(z+x_1)^2+\frac57(x_2+x_3)^2\), both
displayed cone identities, preservation of the kernel after adding their
auxiliaries, and a mixed row \(4-4zx_4\). It verified \(\rho=r_x=2\)
for the PSD row, but \(\rho=3>r_x=2\) for the mixed family. A retained
norm cut increased the refined codimension only to four and still killed
an unused continuous direction. All exact assertions passed. These are
finite algebraic checks; the preceding kernel identities establish the
general result. Only local formatting checks were added; no project-wide
or CI checks were run.
