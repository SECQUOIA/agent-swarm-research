# Independent composition and scope review

Date: 2026-09-28. Reviewer: `/root/unconstrained_posslp_adversary`.
Status: [the complexity synthesis](exact-convex-quartic-complexity.md)
passes this review. No substantive mathematical correction was needed.
One rescaling clarification was requested, applied by the author, and
rechecked in the resulting text.

I did not author the synthesis. I previously reviewed the unconstrained
cubic-perturbation lower bound and the separate rational-witness lower
bound. This is a fresh review of their composition and claimed scope,
not a second independent review of those components. I read the entire
[general upper proof](strong-convex-quartic-posslp-upper.md), its
[independent review](strong-convex-quartic-posslp-upper-independent-review.md),
and both linked primary-literature audit notes. The upper theorem and
its inspected primary dependencies are used as reviewed results.

The input format is an ordinary polynomially checkable language:
rational coefficient comparison verifies the Hessian identity, and
rational symmetric elimination verifies positive definiteness on the
specified full basis. The determinant bound yields \(M\succeq\mu I\)
and hence global strong convexity. Invalid certificates can be mapped
to a fixed negative PosSLP circuit. The broader upper theorem with a
supplied curvature bound is a promise theorem; the synthesis does not
silently claim that its promise is generally polynomially checkable.

The many-one polarities are correct. If \(V\) is the integer input
output, the minimum lower construction has

\[
 \operatorname{sign}(\min G)=-\operatorname{sign}(2V-1),
\]

whereas the unperturbed coordinate construction has

\[
 \operatorname{sign}(p_j-\kappa)=\operatorname{sign}(2V-1).
\]

Both gaps are nonzero. Replacing \(V\) by \(1-V\) negates
\(2V-1\). Thus the minimum construction directly gives the
\(<,\le\) lower bounds and, after that replacement, the
\(>,\ge\) lower bounds. The coordinate construction directly
gives the \(>,\ge\) lower bounds and, after replacement, the
\(<,\le\) lower bounds. The thresholds are explicitly encoded
rationals: zero for the minimum and \(\kappa\) for the coordinate.
This argument uses the absence of equality only for the constructed
lower-bound instances.

The general upper theorem handles equality as well. For an observable
\(\alpha\), it constructs \(\widehat\alpha\) and a positive
gap \(g\) such that \(|\widehat\alpha-\alpha|\le g/8\)
and \(\alpha\ne0\) implies \(|\alpha|\ge g\). Its four
shifted expressions give the strict and weak comparisons. The single
expression \(g^2/4-\widehat\alpha^2\) is positive exactly
when \(\alpha=0\). Fraction conversion preserves positive
denominators and introduces only constantly many integer gates per
rational gate. Therefore all these are many-one upper bounds, rather
than adaptive oracle reductions. The synthesis correctly claims no
matching equality lower bound.

The SOS rows require distinct arguments and are stated correctly.
Taylor integration at the stationary minimizer gives real SOS for
\(f-f(p)\). Thus real SOS membership is equivalent to
\(\min f\ge0\) in this class. Rational positive definite
polynomial-Gram existence is instead equivalent to \(\min f>0\).
For its forward implication, the corrected text rescales the pair
\((f,M)\) to \((f/\mu,M/\mu)\), applies the rational
Taylor-center and full-span argument, and multiplies the resulting
polynomial Gram by \(\mu\). This preserves both polynomial
identities. For the reverse implication, the constant monomial in
the full basis gives \(f(X)\ge\lambda_{\min}(Q)>0\).

At zero minimum, a positive definite polynomial Gram is impossible,
but real SOS still holds. Rational SOS can either hold or fail; the
reviewed ternary counterexample prevents identifying that property
with nonnegativity. The singular rational SOS row therefore receives
only the demonstrated lower bound. After the polarity replacement
above, its yes instances have positive minima and rational positive
definite polynomial Grams, and its no instances take negative values.
No general rational-SOS upper bound is obtained from these facts.

The witness comparison also composes correctly. The upper proof's
Newton vector is a polynomial-size shared rational arithmetic circuit.
If the minimum is negative, the separation and error bounds ensure
that this vector is strictly feasible. Producing the circuit needs
no sign oracle. Expanding it or validating its exact objective sign
is a different task. The separate lower family forces
\(\Omega(n2^{n/2})\) bits in a rational feasible coordinate's
denominator despite compactness, nonempty interior, and bounded
coordinates. This contradicts no circuit-size bound and gives no
conclusion about NP membership under other certificate models.

The significance and prior qualifications are appropriate. The
synthesis distinguishes the restricted quartic classification from
older exact SDP hardness and the recorded SOCP deduction. It credits
the existing Newton/separation/single-PosSLP architecture for
probabilistic polynomial systems. It neither treats convexity
recognition hardness as sufficient nor claims a practical speedup,
NP-hardness, a separation from P, or a result for constrained quartics.
The elementary quadratic-versus-quartic degree observation is valid;
it does not assert a complexity-class separation. Priority remains
unestablished. This review did not perform another exhaustive
literature search or infer novelty from the absence of a match.

No new mathematical computation was needed for this composition
review. The component reviews record their targeted exact checks.
I did not rerun those checks, implement the reductions, formalize the
composition in Lean, inspect CI, or run project-wide verification.
