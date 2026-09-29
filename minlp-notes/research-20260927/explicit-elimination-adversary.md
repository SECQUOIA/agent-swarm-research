# Exact adversarial examples for the deformation elimination lemma

This check concerns the following proposed construction. For equations
\(G_i(\epsilon,\lambda)=0\) of degree at most \(d\), deform them to
\(G_i+\delta\lambda_i^{d+1}=0\). In the standard monomial basis with every
exponent below \(d+1\), let \(A\) and \(B\) be multiplication by
\(\Delta^2\) and \(N\). Clear the powers of \(\delta\) in
\(H=\det(wA-B-\zeta I)\), take its lowest nonzero \(\zeta\) coefficient,
and then take that coefficient's lowest nonzero \(\delta\) coefficient.
The proposed relation \(R(\epsilon,w)\) should vanish at
\(w=N/\Delta^2\) at each original root with invertible Jacobian in
\(\lambda\) and \(\Delta\ne0\).

The exact examples below support that claim. They do not prove it for all
systems or establish its degree and coefficient bounds.

## Persistent base locus

Take one variable, \(d=2\), \(G=x(x-1)\), \(\Delta=x\), and \(N=x\).
The deformation is \(x(x-1)+\delta x^3\). The root \(x=0\) is a persistent
base point, so the naive determinant \(\det(wA-B)\) is identically zero.
Up to a nonzero power of \(\delta\), the characteristic determinant is

\[
-\zeta\bigl(\delta^2\zeta^2-2\delta w\zeta-\delta\zeta-\delta
 +w^2-w\zeta-w\bigr).
\]

The extraction gives \(R=w-w^2\). The isolated regular root \(x=1\)
has \(N/\Delta^2=1\), which is a root of \(R\).

## A positive-dimensional component and a regular isolated root

Take

\[
G_1=x(x-1),\qquad G_2=x(y-\epsilon),\qquad
\Delta=x,\qquad N=x+y.
\]

The original zero set consists of the line \(x=0\) and the isolated point
\((1,\epsilon)\). The latter has Jacobian determinant one and value
\(N/\Delta^2=1+\epsilon\). After adding \(\delta x^3\) and
\(\delta y^3\), the base point \((0,0)\) has algebraic length three.
The characteristic determinant therefore has lowest \(\zeta\) power
three, and its two-stage extraction is

\[
R(\epsilon,w)=-w^3(w-1-\epsilon).
\]

The desired factor survives. Direct computation of the two multiplication
matrices agrees with an independent iterated resultant computation: the
iterated resultant is \(\delta^9 H\). Specializing
\(\epsilon\in\{-2,-1,0,1,2\}\) before extraction still gives a relation
vanishing at the target, including the collision of target value zero
with the extra zero factor.

## A specialization that increases base multiplicity

Take \(G=x(x-1)(x-\epsilon)\), \(d=3\), \(\Delta=x\), and
\(N=x\), with deformation \(G+\delta x^4\). Generically the lowest
\(\zeta\) power is one, and the extraction gives

\[
R(\epsilon,w)=-\epsilon w(w-1)(\epsilon w-1).
\]

At \(\epsilon=0\), the base root \(x=0\) becomes double and this
global relation specializes to the zero polynomial. Nevertheless the
target \(x=1\) remains regular. Extracting the lowest nonzero
\(\epsilon\) coefficient of \(R\) gives \(w(w-1)\), which retains
the target. Alternatively, specializing before the two-stage extraction
raises the lowest \(\zeta\) power to two and gives the same relation
\(w(w-1)\). A specialization identically zero is therefore a real
possibility, not merely a precaution in the lemma's statement.

## Why the regular-root hypothesis matters

If \(G_1=G_2=x\), \(d=1\), \(\Delta=1\), and \(N=y\), every
\((0,y)\) is an original root. Deformation gives
\(x+\delta x^2=0\) and \(x+\delta y^2=0\). The extraction yields
\(R=-w^2\), which does not vanish at the original root \((0,1)\).
Its Jacobian is singular, so this does not contradict the stated lemma.
It rules out extending the lemma to all points of the original variety
without an additional argument.

## Verification

Ran `python research-20260927/check_explicit_span_resultant.py`.
All assertions passed using exact SymPy arithmetic. The check constructs
the stipulated standard-basis multiplication matrices, performs both
coefficient extractions, and compares the second example with iterated
resultants. No project-wide verification or CI inspection was performed.
