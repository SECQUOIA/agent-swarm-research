# Root reconstruction of the cyclic quartic family

Date: 2026-09-28. Status: independent reconstruction of the algebraic
identities and quantitative estimates supplied by the construction
author. The root also suggested alternative constants and the translated
coordinate consequence. This is therefore an additional audit, not the
fresh noncontributor review of the complete theorem.

The [main construction](cyclic-quartic-exponential-degree.md) turns a
cyclic system of rational quadratic equations into one globally strongly
convex integer quartic with a unique zero of exponential field degree.
The root checked the mechanism below independently before reading that
manuscript. Its rational Hessian Gram output additionally uses the
separately reviewed general SOS-convexity construction.

## The exact quadratic system

Let \(n\ge2\), \(m=n+1\), and set

\[
 d=\frac{2^m-(-1)^m}{3},\qquad
 s_i=\frac{(-2)^i-1}{3},\qquad
 \alpha=2^{1/d},\qquad p_i=\alpha^{s_i}
 \quad(0\le i<m).
\]

Here \(d\) is an odd integer, \(p_0=1\), and \(s_1=-1\).
Use \(x_0=1\), interpret subscripts cyclically modulo \(m\), and put

\[
 q_i=x_i^2-2^{k_i}x_{i+1}x_{i+2},
 \quad
 k_i=\begin{cases}
 (-1)^m,&i=m-2,\\
 -(-1)^m,&i=m-1,\\
 0,&\text{otherwise}.
 \end{cases}
\]

The exponent identity
\(2s_i-s_{i+1}-s_{i+2}=k_i d\) holds, including the wraparound
indices. Thus every \(q_i\) vanishes at \(p=(p_1,\ldots,p_n)\).
Since \(|s_i|<d\), every \(p_i\) lies in \([1/2,2]\).

The exposing combination with real coefficients is

\[
 G_*=\sum_{i=0}^{m-1}p_i^{-2}q_i.
\]

Writing \(X_i=x_i/p_i\), with \(X_0=1\), gives the exact identity

\[
 G_*=\sum_iX_i^2-\sum_iX_iX_{i+1}
     =\frac12\sum_i(X_i-X_{i+1})^2.
\]

It follows that \(G_*\) is zero and stationary at \(p\), and its
affine quadratic part is positive definite. In particular the original
quadratic equations have no other real common zero: such a point would
make \(G_*=0\), forcing every \(X_i=X_0=1\).

The polynomial \(T^d-2\) is Eisenstein at two. Because \(p_1=\alpha^{-1}\),
the coordinate field of the point is exactly \(\mathbb Q(\alpha)\),
of degree \(d\). This argument needs no expansion of a large
elimination polynomial.

## Uniform curvature and Jacobian bounds

For a displacement \(u\in\mathbb R^n\), write
\(\delta_0=0\) and \(\delta_i=u_i/p_i\). The grounded path estimate is

\[
 \|\delta\|^2\le n^2\sum_i(\delta_i-\delta_{i+1})^2.
\]

Consequently, in \(G_*(p+u)=u^{\mathsf T}H_*u\),

\[
 \frac1{8n^2}I\preceq H_*\preceq8I.
\]

The upper estimate uses
\(\sum_i(\delta_i-\delta_{i+1})^2\le4\|\delta\|^2\).
Both bounds use only \(p_i\in[1/2,2]\).

Let \(S\) be the cyclic shift and let \(E\) insert a zero in coordinate
zero. The residual Jacobian at \(p\) is

\[
 J=\operatorname{diag}(p_i^2)(2I-S-S^2)E
                         \operatorname{diag}(p_j^{-1}).
\]

The factorization
\(2I-S-S^2=(I-S)(2I+S)\), commutativity of its factors, and
\(\|(2I+S)v\|\ge\|v\|\) show that
\(\|(2I-S-S^2)E\delta\|\ge\|(I-S)E\delta\|\).
The same grounded path estimate gives

\[
                         J^{\mathsf T}J\succeq\frac1{64n^2}I.
\]

Each residual has translated quadratic part of operator norm at most
one. Its gradient norm is at most eight: a row has at most three
nonzero derivatives, each of magnitude at most four; rows involving
\(x_0=1\) satisfy an even smaller bound.

## Short rational coefficients

Use the author's constants

\[
 M=10^6n^5,\qquad \varepsilon=M^{-2},\qquad
 Q=32mM^2.
\]

Choose integers \(k_i'\) with
\(|k_i'/Q-p_i^{-2}|\le1/Q\), and set
\(G=\sum_i(k_i'/Q)q_i\). This preserves exact vanishing at \(p\).
In \(G(p+u)=\ell^{\mathsf T}u+u^{\mathsf T}Hu\), the preceding
bounds give

\[
 \|\ell\|\le8m/Q=\varepsilon/4,\qquad
 \|H-H_*\|\le m/Q=\varepsilon/32.
\]

Thus \(H\succeq hI\), \(\|H\|\le9\), and
\(J^{\mathsf T}J\succeq\nu^2I\), where
\(h=1/(16n^2)\) and \(\nu=1/(8n)\).
There are \(m\) residuals in \(n\) variables; these two counts must
remain distinct.

For the established quartic and SOS-convexity estimates it suffices that

\[
 \varepsilon\le
 \min\left\{\frac{h^2}{2m},
       \frac{\nu^2h^2}{36n(9+8m)^2}\right\}.
\]

Since \(9+8m\le17n\), the second right-hand side is at least
\(1/(170459136n^9)\). The chosen \(\varepsilon=1/(10^{12}n^{10})\)
satisfies both conditions for every \(n\ge2\). Those estimates prove

\[
 \nabla^2\left(G^2+\varepsilon\sum_iq_i^2\right)
                       \succeq\frac32\varepsilon\nu^2I.
\]

The integer SOS polynomial is

\[
 F=A^2+\sum_i\left(\frac{2Q}{M}q_i\right)^2,
 \qquad A=2\sum_i k_i'q_i.
\]

All squared quadratics have integer coefficients: the only denominators
in the \(q_i\) are two, and \(2Q/M=64mM\).
Also \(F=4Q^2(G^2+\varepsilon\sum_iq_i^2)\), so

\[
                  \nabla^2F\succeq
                  96(m/n)^2M^2 I\succeq I.
\]

Its expanded support has \(O(n^2)\) terms, each with \(O(\log n)\)
coefficient bits. Computing the weights requires only \(O(\log n)\)
accuracy bits for bounded numbers
\(\exp((-2s_i/d)\log2)\), whose rational exponents have \(O(n)\)
bits. Certified rational logarithm and exponential series therefore
give a polynomial-time route without isolating a degree-\(d\)
polynomial. The complete series and Gram-certificate implementation
bounds remain part of the author's main proof and its fresh review.

## What the output-size consequence actually excludes

The original first coordinate has sparse minimal polynomial
\(2T^d-1\). Its large degree alone excludes short dense
minimal-polynomial output, but does not exclude sparse output.

Make the rational translation \(y_1=1+x_1\), leaving all other
coordinates unchanged. It preserves strong convexity, SOS structure,
and the same coefficient-size order for the quartic. The first zero
coordinate now has irreducible minimal polynomial

\[
                              2(T-1)^d-1.
\]

All its \(d+1\) coefficients are nonzero; the constant is \(-3\),
because \(d\) is odd. Thus this family also forces exponential
length in ordinary sparse monomial-list minimal-polynomial output.
The argument does not exclude a shifted basis, an algebraic circuit,
or an extension-tower representation, and does not prove a decision
complexity lower bound.

## Exact checks and prior limits

A targeted inline Python command using fractions.Fraction and SymPy
checked the wraparound exponent identities, odd degree, coordinate
bounds in exponent form, and an independent safe regularization scale
for \(m=3,\ldots,80\). For \(m=3,\ldots,12\), it additionally
checked the exact grounded determinant, operator factorization, and
grounded-energy identity. All assertions passed. The alternate scale
in that check was \(2^{-32}m^{-10}\); the displayed author's scale
was rechecked through the uniform rational inequalities above.
These finite checks validate identities and indexing cases. The
dimension-uniform argument is the proof, not numerical sampling.

The determinant and its directed spanning-tree interpretation have
classical antecedents. The root directly inspected the publisher's
abstract for Lonc--Parol--Wojciechowski,
[On the number of spanning trees in directed circulant graphs](https://onlinelibrary.wiley.com/doi/10.1002/net.2).
It states the same extremal closed-form integer for out-degree two;
the root has not inspected the full paper or its rooted-tree convention.
The main source audit must credit the graph and binomial-system
ingredients separately from the convex quartic assembly. This audit
does not establish novelty. No project-wide verification or CI
inspection was performed.
