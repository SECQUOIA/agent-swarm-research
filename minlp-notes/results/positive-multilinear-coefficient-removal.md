# Removing positive coefficients from worst-case multilinear gap ratios

Date: 2026-09-04. Status: independently audited; no unresolved mathematical issue identified. See `notes/review-multilinear-coefficient-removal.md`. The probabilistic blow-up argument is a standard weighted-to-unweighted approximation mechanism. The claim here is its application to both multilinear envelope gaps and term-by-term gaps, not novelty of the random-sampling method itself.

## Statement

Fix an integer degree allowance d≥2. The supremum R(d) of the term-by-term/convex-hull gap ratio for positive multilinear polynomials on the unit cube is unchanged if one requires simultaneously:

- every included monomial has coefficient one;
- every monomial has degree exactly d;
- the evaluation point is strictly inside its unit cube.

The dimension and the number of monomials may increase. This does not preserve a fixed dimension or produce a small explicit unweighted example. A finite positive polynomial with a ratio above a target gives a finite unweighted homogeneous polynomial above the same target, provided the original inequality is strict.

The [nonnegative-box comparison](positive-multilinear-degree-upper-bound.md) shows that allowing arbitrary finite boxes with nonnegative lower bounds does not enlarge the degree-based supremum beyond its unit-cube value. Indeed, each box-normalized positive monomial expands into nonnegative unit-cube monomials, the original term-by-term gap is no larger than the expanded gap, and the full hull gap is unchanged. Thus the stated equality of suprema also applies when the original R(d) permits those boxes.

## Homogenization and interior points

Affine terms affect neither gap and may be removed. Introduce d−2 new padding variables. For each original degree-k monomial, multiply it by the first d−k padding variables. The resulting polynomial is multilinear and homogeneous of degree d. At the point where all padding variables equal one, every feasible binary coupling fixes them at one, so the full convex and concave envelopes reduce to the original ones. The termwise envelopes also reduce to their original values, leaving both gaps unchanged.

The envelopes of a fixed multilinear polynomial on a cube are finite piecewise-linear functions and are continuous on the cube. The termwise envelope gaps are continuous as well. At a point with positive hull gap, the ratio is therefore continuous. Perturb all coordinates, including any padding coordinates, into the open cube. The ratio can be made arbitrarily close to its original value. Thus it suffices to prove the approximation result below for one fixed positive homogeneous polynomial at a strictly interior point with positive hull gap.

Finally divide the entire polynomial by its largest coefficient. This scales both gaps by the same factor, so it does not change the ratio. The coefficients may consequently be assumed to lie in (0,1].

## Exact cloning before random sampling

Let

\[
f(x)=\sum_{e\in E}a_e\prod_{i\in e}x_i,
\qquad |e|=d,\quad 0<a_e\le1,
\]

have n variables and s=|E| distinct monomials. Fix an interior point x with positive hull gap. For each positive integer m, replace variable i by m distinct clones y_{i1},...,y_{im}, and put

\[
\bar y_i=\frac1m\sum_{r=1}^my_{ir},\qquad
F_m(y)=m^d f(\bar y).
\]

Every original monomial expands into m^d distinct degree-d squarefree clone monomials with coefficient a_e. Monomials arising from different original supports remain distinct because each clone retains its original variable group. The polynomial F_m has s m^d candidate monomials. Evaluate it at the repeated point y_{ir}=x_i.

Both full-function envelope values scale exactly:

\[
\operatorname{vex}F_m(y)=m^d\operatorname{vex}f(x),\qquad
\operatorname{cav}F_m(y)=m^d\operatorname{cav}f(x).
\tag{1}
\]

To prove this, consider any joint binary clone distribution with the repeated means. Its averages form a random vector q∈[0,1]^n with E q=x, and F_m=m^d f(q). Conditional on q, round the original variables independently to binary values with means q_i. Multilinearity gives conditional expected value exactly f(q). This converts any clone distribution into an original binary distribution with mean x and the same normalized objective value. Conversely any original binary distribution can be realized by setting every clone in each original variable group equal to that original binary variable. This proves equality of the complete ranges of feasible expectations, and hence both equalities in (1).

Each clone monomial also has exactly the same coordinate marginals as its original monomial. Therefore

\[
\operatorname{tbtgap}_{F_m}(y)=m^d\operatorname{tbtgap}_f(x),\qquad
\operatorname{chgap}_{F_m}(y)=m^d\operatorname{chgap}_f(x).
\tag{2}
\]

## Random sampling removes the coefficients

Independently retain each clone monomial arising from e with probability a_e, and give every retained monomial coefficient one. Let G_m denote the resulting random homogeneous multilinear polynomial. Then E G_m(v)=F_m(v) at every vertex v.

At a fixed binary vertex, G_m(v)−F_m(v) is a sum of s m^d independent centered random variables, each with range length at most one. [Hoeffding's bounded-sum inequality](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf) (1963), applied to each tail, gives

\[
\mathbb P\{|G_m(v)-F_m(v)|>t\}
\le2\exp\{-2t^2/(s m^d)\}.
\]

There are 2^{nm} binary vertices. At the repeated evaluation point, the term-by-term gap of G_m is also a sum of independent retained-monomial indicators times fixed nonnegative single-monomial gaps bounded by one. Its expectation equals the term-by-term gap of F_m, and the same concentration bound applies.

Choose a constant K with K²>s n ln2/2, and put

\[
t_m=K m^{(d+1)/2}.
\]

A union bound shows that both events

\[
\max_{v\in\{0,1\}^{nm}}|G_m(v)-F_m(v)|\le t_m,
\qquad
|\operatorname{tbtgap}_{G_m}(y)-\operatorname{tbtgap}_{F_m}(y)|\le t_m
\tag{3}
\]

hold simultaneously with positive probability for all sufficiently large m. The total failure probability is at most

\[
2(2^{nm}+1)\exp\{-2K^2m/s\},
\]

which tends to zero by the choice of K. This is an existence argument; no specific successful sample is claimed without generating and checking one.

Uniform approximation at the binary vertices implies that each of the convex and concave envelope values at every fixed marginal vector differs by at most t_m: compare expected values under each feasible binary distribution and then take the minimum or maximum. In particular, on the event (3),

\[
|\operatorname{chgap}_{G_m}(y)-\operatorname{chgap}_{F_m}(y)|\le2t_m.
\]

Since d≥2,

\[
\frac{t_m}{m^d}=K m^{(1-d)/2}\longrightarrow0.
\]

Using (2), the normalized gaps of successful samples converge to the original gaps. The limiting hull gap is positive, so their ratios converge to the original ratio. Taking suprema proves the statement.

## A finite unweighted homogeneous cubic existence bound

The [homogeneous 25-variable cubic example](positive-cubic-gap.md) has 464 monomials, positive integer coefficients at most 13, and an interior evaluation point. Its term-by-term gap T_0 equals 943, while its hull gap H_0 satisfies

\[
H_0\le80947/175,\qquad T_0-2H_0\ge3131/175>0.
\]

Normalize the coefficients by 13 and apply the degree-three cloning construction with m=1000. There are 25,000 variables and464m³ candidate monomials. Retain each clone monomial with the corresponding normalized coefficient as its probability. The expected polynomial is m³ times the normalized original polynomial.

Take t=m³/10. The probability that either the uniform vertex approximation or the termwise-gap approximation fails is at most

\[
2(2^{25m}+1)\exp\{-m^3/23200\}<1
\qquad(m=1000).
\]

For example, 2^{25m}+1≤2^{25m+1}, so the logarithm of this bound is at most (25m+2)ln2−m³/23200. At m=1000 it is negative, even using the weaker bound ln2<1.

For every successful sample,

\[
\begin{aligned}
\operatorname{tbtgap}_{G_m}-2\operatorname{chgap}_{G_m}
&\ge\frac{m^3}{13}(T_0-2H_0)-5t\\
&\ge m^3\left(\frac{3131}{2275}-\frac12\right)>0.
\end{aligned}
\]

The strict inequality above ensures that the sample is nonempty. For a nonempty positive polynomial of degree at least two at an interior point, each monomial has its coordinate product strictly below its minimum coordinate. Thus the concave envelope is strictly above the polynomial value, which itself is at least the convex envelope, proving that the hull gap is positive. Hence there exists a unit-coefficient homogeneous cubic polynomial on 25,000 variables, at a strictly interior point, with gap ratio above two.

This is a nonconstructive finite existence bound. It is deliberately loose and does not claim that the random polynomial has been generated, stored, or individually certified. The compact 18- and24-variable examples remain the explicit rational certificates.

## Smaller explicit cubic witness

The general coefficient-removal theorem above remains useful for preserving an arbitrary degree-based ratio. For the particular existence of a unit-coefficient homogeneous cubic ratio above two, the later [two-marginal construction](positive-cubic-two-level-family.md) is stronger and explicit: 52 variables, 4,320 distinct cubic monomials, interior marginals, and a certified ratio at least 2700/1343. Its direct construction avoids random sampling.
