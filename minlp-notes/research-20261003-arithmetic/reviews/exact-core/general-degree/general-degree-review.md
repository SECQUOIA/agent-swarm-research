# Independent review of the variable-degree PosSLP upper bound

Date: 2026-10-03. **Result: passed after minor input-boundary clarifications.**

I read the complete
[general-degree theorem](strong-convex-polynomial-posslp-upper.md), checked
its analytic and representation arguments, and directly inspected the two
primary sources used below. I reread the revised file after the author
added the zero-dimensional case, explicit certificate-format checks, and
the enlarged input length for a derived curvature bound. No mathematical
gap remains in the stated theorem. This review does not establish priority.

The uniform claim is valid for sparse polynomials whose degree is at most
the input length, and therefore for the stated unary-degree convention.
It is not merely a collection of fixed-degree claims with an uncontrolled
degree-dependent exponent.

1. **Polynomial-precision initialization.** Strong monotonicity gives
   \(\|p\|\le\|\nabla f(0)\|/\mu\le2^{3L}\). For derivatives
   of orders zero through three on the radius-\(2^{4L}\) ball, the
   coefficient bound, degree factors, and tensor dimension factors give
   the displayed \(2^{2L}L^{9/2}2^{4L^2}\) bound. Its logarithm is
   below \(16L^2\) for every \(L\ge2\), using
   \(\log_2L\le L\). The proposed initial objective tolerance has
   polynomial encoding length and places the initial point in the
   required Newton neighborhood.

   I checked §1.2 and Corollary 1.2 of
   [Slot, Steurer, and Wiedmer](https://arxiv.org/html/2511.03440v1).
   Their encoding explicitly permits sparse nonzero coefficients and
   unary monomial exponents, with variable degree. Their polynomial-time
   approximation theorem applies to the unconstrained problem here.
   No conversion to an exponentially large dense polynomial is needed.

2. **Uniform separation.** I checked the degree and integer-coefficient
   bounds in [Basu, Theorem 2.16, printed page 12](https://www.math.purdue.edu/~sbasu/raag_survey2011.pdf).
   With one quantified block of size \(n\) and one free variable, they
   give \(D^{O(n)}\) degrees and \(\tau D^{O(n)}\) coefficient
   bit lengths. Sparse differentiation and denominator clearing leave
   \(\tau\) polynomially bounded. Since \(n,D\le L\), a single
   effective polynomial \(a(L)\) bounds both outputs by \(2^{a(L)}\).
   The real singleton argument and removal of a possible zero root then
   give the claimed nonzero gap. The proof neither runs quantifier
   elimination nor assumes that the complex critical locus is finite.

3. **Polynomial-size circuits.** Sparse differentiation creates at most
   a polynomial factor more terms. Each monomial can be evaluated by a
   polynomial-size multiplication circuit, and the positive definite
   Newton Hessian permits branch-free rational elimination. The Newton
   error recurrence keeps every iterate in its certified neighborhood.
   For observable accuracy, the factors \(B\) cancel:
   \(B e_k\le2\mu\,2^{-3\cdot2^k}\). Thus the stated polynomial
   number of Newton steps reaches the doubly small separation scale.
   Sharing circuit nodes prevents any expansion of huge fractions.
   The five offset predicates correctly cover positive, negative, and
   zero exact observables. The division-elimination formula preserves
   positive denominators without querying their signs.

4. **Arbitrary listed Hessian monomials.** The certificate extension is
   valid because the monomial vector contains every \(v_i\). If its
   Gram is bounded below by \(\mu I\), its biform is at least
   \(\mu\|w(X,v)\|^2\ge\mu\|v\|^2\). No assumption that the
   list contains every monomial of some degree is needed. An explicitly
   listed vector of length \(m\) gives at most \(m^2\) products for
   coefficient matching. Symmetry, format, degree bounds, the identity,
   and rational positive definiteness are all checked in polynomial
   time. The determinant-over-trace bound has polynomial bit length;
   counting that derived number in the enlarged \(L\) makes all earlier
   estimates applicable. The separate constant case avoids a zero-size
   Gram formula.

5. **Classification and limits.** The quartic full-Gram class is a
   subclass of this checked input class. Its existing strict and weak
   comparison lower bounds therefore combine with the new upper bound.
   No equality lower bound is inferred. The strict-feasibility circuit
   witness follows from the same approximation and separation estimates;
   it need not have short expanded fractions. Neither arbitrary
   circuit-encoded input polynomials nor sparse binary degree without
   a polynomial degree bound is covered.

This review checks a mathematical generalization. No implementation of
quantifier elimination or an exact high-precision convex solver was run,
and no project-wide verification or CI inspection was performed.
