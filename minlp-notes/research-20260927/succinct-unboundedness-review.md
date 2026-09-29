# Independent review of succinct polynomial escape curves

Date: 2026-09-27. Scope: an adversarial review of the construction in
[succinct-unboundedness-curves.md](succinct-unboundedness-curves.md), using
the rational recession elimination in
[mixed-integer-attainment-frontier.md](mixed-integer-attainment-frontier.md).
This review does not assess publication priority or reprove the linked
algebraic anchor theorems.

**Verdict.** The stated escape-tail construction is correct, conditional on
the linked recession-elimination result. Given an anchor radius, its
polynomial-size rational circuit bound holds for fixed integer dimension
without fixing the continuous Hessian span. Its local proof can be checked
without expanding the output polynomials. A complete unboundedness
certificate additionally needs an exact, efficiently checkable anchor;
the draft correctly treats that representation issue separately.

## 1. The lift and its quantifiers

At one reversed step write

\[
 w^0=Ay^0+ds^0,\qquad
 w(T)=A(y^0+p_y(T))+d(s^0+P_s(T)).
\]

For a deleted row, put \(\beta_i=-\alpha_i>0\). If
\(B(T)\ge1\) bounds all coordinates of \(y^0+p_y(T)\), then its
monomial coefficient norm \(H_i\) gives

\[
 r_i(y^0+p_y(T))\le H_i B(T)^2.
\]

Consequently \(M_s\ge |s^0|\),
\(C\ge1+M_s+H_i/\beta_i\), and
\(P_s(T)=CT(1+B(T)^2)\) imply, for real \(T\ge1\),

\[
 r_i(y^0+p_y(T))-
       \beta_i(s^0+P_s(T))
 \le H_iB(T)^2+\beta_iM_s
           -\beta_i C(1+B(T)^2)\le0.
\]

This argument does not assume that the projected anchor, or its removed
scalar, is rational. Their magnitude bounds suffice. The constants and
circuits can therefore be chosen once for every feasible anchor in the
supplied original box.

The retained rows follow from feasibility in the reduced problem. At
integer parameters, \(P_s(T)\) is integral because its circuit builds an
integer polynomial. In an integer elimination, the integer outputs of
\(A\) depend only on the retained integer coordinates and have integer
coefficients; the integer part of \(d\) is integral. In a continuous
elimination, its integer part is zero and \(A\) preserves the integer
coordinates. Thus the reconstruction preserves the mixed lattice at every
integer parameter. It is not enough merely to say that \(A\) is a
rational matrix: this block structure is the required property, and the
draft records it.

Each increment has zero constant term. Every eliminated direction is
objective-invariant, and the terminal direction is in the terminal
objective Hessian's kernel with negative rational affine slope. These
facts prove the exact identity
\(q_0(a+p(T))=q_0(a)-\gamma T\), including when \(a\) is algebraic.

The proposed polynomials need not give a feasible path for
\(0<T<1\). The explicit qualification in the draft is necessary. For
example, consider

\[
 100z^2\le x_1,\qquad x_1^2\le x_2,
 \qquad a=(0,0,0),\qquad R=1.
\]

Use the terminal bound \(B_*(T)=1+T\), lift \(x_1\) with
\(C_1=102\), update \(B_1=B_*+1+P_1\), and lift \(x_2\) with
\(C_2=3\). These choices obey the construction, but at \(T=1/100\)
the second-row residual is

\[
 x_1(T)^2-x_2(T)=
 \frac{92964972401097}{25000000000000}>0.
\]

The assertion is therefore about a feasible polynomial tail for real
parameters at least one, together with the separate feasible value at
zero. In a purely continuous problem, convexity supplies a feasible
line segment from the anchor to the tail's value at one if a continuous
piecewise-polynomial path is desired. That observation does not turn the
displayed polynomial into a feasible path on the missing interval.

## 2. Size bounds survive the projections

The potentially dangerous distinction is between the reduced problem and
the inverse coordinate maps. A continuous elimination merely takes a
coordinate section in the retained polynomials, so those polynomials do
not accumulate the direction's coefficients. Its projection map does
contain rational ratios from the direction, but that map is recorded
separately. An integer elimination changes the retained polynomials, and
there are at most \(k\) such changes. Rational LP witness bounds and
primitive-vector completion therefore give polynomial-size data at every
stage for fixed \(k\).

For completeness, bounds on projected anchors cannot be read from the
retained polynomial coefficients alone. They follow by composing the
recorded rational projection maps. Give each matrix a common denominator.
The bit length of a product of at most \(n+k\) such matrices is bounded
by the sum of their numerator and denominator bit lengths, plus the
logarithmic contribution from matrix dimensions. All these quantities are
polynomial for fixed \(k\). The same argument applies to a removed
coordinate row composed with the preceding projections. Taking absolute
row sums and multiplying by \(R\) supplies the stated polynomial-bit
anchor and scalar bounds.

The lift's large coefficients occur inside arithmetic gates, not inside
new explicitly written constants. In particular, \(C\) depends on a
reduced row, its nonzero slope, and a projected-anchor bound; it does not
depend on the expanded coefficients of \(B\). The update

\[
 B_w=L\bigl(B+M_s+CT(1+B^2)\bigr)
\]

is an integer polynomial with nonnegative coefficients and bounds the
reconstructed coordinates for every real \(T\ge0\). Each step adds
polynomially many gates with polynomial-bit constants. Beginning at degree
one, the recurrence \(D\mapsto2D+1\) gives
\(\deg p\le2^{\ell+1}-1\). Large expanded coefficient heights do not
contradict the circuit-size conclusion.

## 3. What a verifier must check

The certificate is more than an arbitrary circuit claimed to be feasible.
Its trace records coordinate maps, reduced quadratic rows, directions,
and the constants used by the prescribed lift. A verifier can check:

- The rational inverse coordinate identities and the integer block
  structure, including unimodularity for integer eliminations.
- The original PSD conditions, the direction kernel and equality
  conditions, zero objective slope at eliminated steps, and negative
  objective slope at the terminal step.
- The local quadratic substitution identities, row deletions, and uniform
  bounds obtained from the projection maps.
- The numerical inequalities for \(C,L,M_s,M\), and that the submitted
  circuit is assembled by the displayed reconstruction formulas.

All polynomial identities in this list concern explicitly encoded degree
at most two polynomials or rational matrices. The circuit assembly check
is syntactic. Neither requires general polynomial identity testing on the
expanded escape curve. The verifier also does not need to prove that no
decreasing direction existed at earlier steps: the recorded zero-slope
directions and final decreasing direction already establish the claim.

Anchor feasibility remains a distinct obligation. Coordinatewise minimal
polynomials and isolating intervals identify coordinates, but their small
individual degrees alone do not imply an efficient multivariate sign
algorithm. The linked common-field degree result and a suitable joint
representation must provide that additional step. The escape construction
adds no field extension: all its nonconstant coefficients are rational.

## 4. Lower bound and limits

In the chain \(z^2\le x_1\), \(x_{j-1}^2\le x_j\), an affine,
strictly decreasing objective \(-z(T)\) forces
\(z(T)=a+bT\) with \(b>0\). Feasibility along arbitrarily large
integer parameters forces \(x_j(T)\ge z(T)^{2^j}\), hence
\(\deg x_m\ge2^m\). This argument also permits algebraic polynomial
coefficients and only eventual feasibility.

For this mixed-integer example, the continuous Hessian span is exactly
\(h=m-1\): the first row has no continuous quadratic part, and each
subsequent row supplies a distinct continuous diagonal Hessian. In the
all-continuous version, where \(z\) is also continuous, the span is
\(m\). Thus the example does not give an exponential-degree lower bound
with fixed \(h\).

Exponential degree rules out a polynomial-size dense coefficient list.
It does not rule out a short sparse list: the particular chain already
admits the monomials \(T^{2^j}\). The draft correctly limits the
conclusion to dense output and makes no computational hardness claim.

## Verification record

The review read the escape note, the recession-elimination section, the
linked irrational-singleton example, and the common-field discussion in
the algebraic witness note. A targeted inline command using
`python -` and `fractions.Fraction` checked the example in Section 1:
the constructed integer samples at \(T=1,2,10\) satisfy both rows,
the increment is zero at \(T=0\), and the displayed positive residual at
\(T=1/100\) is exact. It passed. These samples supplement the symbolic
argument; they are not a proof of its universal quantifiers.

No project-wide verification, CI inspection, or Lean verification was
performed. The review does not certify the source theorems' publication
priority or the separate anchor-representation construction.
