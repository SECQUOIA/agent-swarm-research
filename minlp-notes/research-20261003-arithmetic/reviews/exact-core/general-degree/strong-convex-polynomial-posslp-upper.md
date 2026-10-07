# Exact comparison for strongly convex polynomials of variable unary degree

Date: 2026-10-03. This is a generalization of the
[quartic upper bound](../../../../research-20260927/strong-convex-quartic-posslp-upper.md).
The proof uses the same approximation, Newton-circuit, and algebraic-separation
method. It does not claim a new method or established publication priority.

## Statement and encoding

Let \(n\ge1\), and let \(f,h\in\mathbb Q[X_1,\ldots,X_n]\) be explicitly supplied sparse
polynomials, and let \(\mu>0\) be an explicitly encoded rational number.
Assume
\[
                  \nabla^2 f(X)\succeq\mu I
                    \qquad(X\in\mathbb R^n).
\]
The input contains the coefficient fractions and exponent vectors of the
nonzero monomials, the dimension, and unary degree bounds for both polynomials.
Let \(L\ge2\) be the total bit length, enlarged by a fixed constant if needed.
In particular, \(n,\deg f,\deg h\le L\). Let \(p\) be the unique minimizer
of \(f\) on \(\mathbb R^n\).
For \(n=0\), evaluate the constant observable by direct rational comparison.

**Theorem.** Each strict order, weak order, or equality comparison of
\(h(p)\) with zero has a deterministic polynomial-time many-one reduction
to a single PosSLP instance. The construction makes no PosSLP query while
building the instance. A rational threshold is absorbed into \(h\), with
its encoding counted in \(L\).

The theorem is a promise result when only \(\mu\) is supplied. It also
applies to the verifiable Hessian-certificate input class described below.
Unary degree can be replaced by any encoding convention that guarantees
\(\deg f,\deg h\le\operatorname{poly}(L)\), with an adjusted polynomial
runtime bound. No polynomial-time assertion in sparse binary-degree length
alone is made.

## Polynomial-bit initial approximation

The coefficient one-norms of \(f\) and \(h\) are at most \(2^{2L}\), and
\(2^{-L}\le\mu\le2^L\). Strong convexity gives coercivity and
\[
          \|p\|\le\|\nabla f(0)\|/\mu\le2^{3L}.
\]
Set
\[
                    R=2^{4L},\qquad B=2^{16L^2}.
\]
On \(\|X\|\le R\), the scalar value, Euclidean gradient norm, Hessian
operator norm, and third derivative operator norm of either polynomial are
bounded by \(B\). To see this, put \(D=\max(1,\deg f,\deg h)\le L\).
Each derivative component of order \(j\le3\) has magnitude at most
\(2^{2L}D^jR^D\). Passing to tensor Frobenius norm costs at most
\(n^{j/2}\). Thus a common upper bound is
\[
 2^{2L}L^{9/2}2^{4L^2}<2^{16L^2}\qquad(L\ge2).
\]
The third derivative bound is a Hessian Lipschitz bound on this convex ball.

Define
\[
              \rho=\frac{\mu}{4B},\qquad
              \varepsilon_0=\frac{\mu^3}{32B^2}.
\]
These constants have \(O(L^2)\) bits. A rational point satisfying
\(f(x_0)-f(p)\le\varepsilon_0\) has \(\|x_0-p\|\le\rho\).
The radius-\(\rho\) ball about \(p\) lies in the radius-\(R\) ball.

[Slot, Steurer, and Wiedmer, Corollary 1.2](https://arxiv.org/html/2511.03440v1)
supplies this point in polynomial time. Their sparse encoding includes
degree, and their theorem permits variable degree and unconstrained
optimization as a special case. Only polynomially many accuracy bits are
requested here. Alternatively, the displayed search radius and derivative
bounds permit the usual rational ellipsoid warm start. No exact-arithmetic
oracle is used in this step.

## Uniform separation at variable degree

For \(\alpha=h(p)\), consider the singleton-defining formula
\[
 \exists X:\quad\nabla f(X)=0\quad\text{and}\quad z=h(X).
\]
It has one quantified block, one free variable, at most \(n+1\) polynomial
equations, and degree at most \(\max(1,\deg f,\deg h)\le L\).
Clearing denominators leaves integer coefficient bit lengths
\(\tau=\operatorname{poly}(L)\).

[Basu, Theorem 2.16, printed page 12](https://www.math.purdue.edu/~sbasu/raag_survey2011.pdf)
bounds both the degrees and coefficient bit lengths of a one-block
quantifier-free description by \(D^{O(n)}\) and \(\tau D^{O(n)}\),
respectively, when the number of free variables is one. Consequently both
are at most \(2^{a(L)}\) for one fixed effective polynomial \(a\).
Indeed, \(n\log D\le L\log L\), which is polynomially bounded.
Increase \(a\), if necessary, so that \(a(L)\ge32L^2+10\).

Since the described real set is a singleton, a nonzero integer polynomial
from the quantifier-free description vanishes at \(\alpha\). Otherwise
the description would be locally constant on a neighborhood of \(\alpha\).
After removing a power of \(z\), its nonzero constant coefficient and
the elementary root bound give
\[
        \alpha\ne0\quad\Longrightarrow\quad
        |\alpha|\ge 2^{-2^{a(L)+1}}=:g.
\]
This does not assume the complex critical locus is finite.

The reduction does not execute quantifier elimination or expand a dense
degree-\(D\) polynomial. The quantifier-elimination theorem is used only
to choose the effective polynomial \(a\). Its bound applies to the
mathematical sparse input polynomials without requiring a dense encoding
to be constructed. The gap \(g\) has a circuit of \(a(L)+1\) successive
squarings starting with \(1/2\).

## Newton circuits and the final sign

Take exact Newton steps
\[
            x_{t+1}=x_t-\nabla^2f(x_t)^{-1}\nabla f(x_t).
\]
Within the indicated neighborhood, \(e_t=\|x_t-p\|\) satisfies
\[
       e_{t+1}\le\frac{B}{2\mu}e_t^2,
       \qquad e_t\le\frac{2\mu}{B}\,2^{-3\cdot2^t}
                  \le2^{L+1-3\cdot2^t}.
\]
The same inequalities keep every iterate inside that neighborhood. The
positive definite Hessian can be inverted using rational
\(LDL^{\mathsf T}\) elimination without pivoting or sign queries.

Differentiating the sparse input produces only polynomially many terms.
At an explicit point of polynomial bit length, their values also have
polynomial bit length because the degree is at most \(L\). At subsequent
circuit points, each monomial is evaluated by multiplication and repeated
squaring. Every Newton step therefore adds polynomially many rational
circuit gates. Sharing nodes between steps is essential.

For \(k=a(L)+2\), the gradient bound for \(h\) gives
\[
 |h(x_k)-\alpha|
 \le B e_k\le2^{L+1-12\cdot2^{a(L)}}\le g/8.
\]
Writing \(\widehat\alpha=h(x_k)\), the rational circuits
\[
\begin{array}{c|c}
 \widehat\alpha-g/2&\alpha>0\\
 \widehat\alpha+g/2&\alpha\ge0\\
 -\widehat\alpha-g/2&\alpha<0\\
 -\widehat\alpha+g/2&\alpha\le0\\
 g^2/4-\widehat\alpha^2&\alpha=0
\end{array}
\]
are positive precisely for their stated predicates, including equality
cases. Representing a rational gate by \(N/D\) with \(D>0\), eliminate
division by the rule
\[
       \frac{N_a/D_a}{N_b/D_b}
          =\frac{N_aD_bN_b}{D_aN_b^2}.
\]
All divisors are nonzero, and each rational gate creates only a constant
number of integer gates. The final numerator is the PosSLP instance.
All printed constants and the circuit itself have polynomial total size.
Expanded Newton numerators and denominators need not have polynomial size.

## Checked inputs and consequences

A verifiable subclass supplies a rational positive definite matrix \(M\)
and an explicitly listed monomial vector \(w(X,v)\), linear in \(v\),
containing the coordinates \(v_1,\ldots,v_n\), with
\[
        v^{\mathsf T}\nabla^2 f(X)v=w(X,v)^{\mathsf T}Mw(X,v).
\]
Count the full matrix, monomial list, and unary degree bounds in the input
length. Check matrix symmetry, the monomial-list format and required
coordinates, and the degree bounds. Sparse coefficient comparison checks
the identity in polynomial time; rational symmetric elimination checks
positive definiteness. For
\(m=\dim M\),
\[
               \mu=\det(M)/(\operatorname{tr}M)^{m-1}
\]
is a positive rational curvature lower bound with polynomial bit length.
For this certificate format, enlarge \(L\) to include the derived
\(\mu\) before applying the preceding estimates; the enlarged length is
polynomial in the original input length.
Invalid certificates are rejected before the reduction. This yields an
ordinary decision language, not recognition of a semantic curvature
promise. The broad class includes the full quartic Hessian basis
\((v,X\otimes v)\).

The existing quartic reductions therefore give PosSLP-completeness for
strict and weak minimum-value and optimizer-coordinate comparisons in
this variable-degree certified class. Equality has the proved upper bound;
no matching equality lower bound is added here. No SOS-membership extension
is claimed from an arbitrary choice of the Hessian monomial vector.

For any strictly feasible instance \(\min f<0\), taking \(h=f\) also
constructs a polynomial-size rational-circuit feasible point without a
sign oracle. It need not be a polynomial-size expanded rational witness,
and validating its objective sign is not asserted to be ordinary
polynomial-time arithmetic.

The degree condition is material: with only binary exponents, even
evaluation at a small rational input can produce exponentially many
ordinary bits. The warm-start argument above is not a proof for that
different encoding model. Removing supplied strong curvature is likewise
outside this theorem.
