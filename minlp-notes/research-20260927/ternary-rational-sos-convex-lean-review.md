# Independent Lean correspondence review for the ternary quartic

Date: 2026-09-28. Status: the frozen Lean source passed independent
inspection and a targeted rerun. No correspondence defect was found.

This review compares
[TernarySOSDescent.lean](../formal/TernarySOSDescent.lean) with the
[mathematical construction](ternary-rational-sos-convex-counterexample.md)
and checks the scope described in the
[verification record](ternary-sos-descent-lean-verification.md).
It does not formalize the field-theoretic SOS obstruction.

## Definitions and the prescribed zero

The Lean definitions reproduce the exact integer polynomial:

\[
\begin{aligned}
r_0&=2-2xy,&r_1&=2x^2-2yz,&r_2&=2y^2-4z,\\
r_3&=2z^2-x,&r_4&=2xz-y,\\
A&=4r_0+5r_1+3r_2+9r_3,\\
F&=A^2+r_0^2+r_1^2+r_2^2+r_3^2-r_4^2.
\end{aligned}
\]

All arguments are real. No approximate root or rounded polynomial
coefficient appears in these definitions. The negative square is
retained throughout the derivative calculations.

The theorem about the zero assumes a real \(a\) with \(a^5=2\),
and uses the polynomial-coordinate point
\[
                     p=(a^4/2,a,a^2/2).
\]
This is exactly the alternative expression for the point in the
mathematical note. The residual theorem checks all five equations;
the zero theorem then evaluates the displayed sum and difference of
squares. The stationarity theorem proves that the actual derivative
of \(t\mapsto F(p+tv)\) at zero is zero for every real direction.
These are conditional statements: the file does not itself construct
or characterize the real fifth root.

## The curvature expression is an actual derivative

The definitions of the five first directional derivatives agree with
the residuals. The quadratic coefficient in the exposing polynomial
along direction \((a,b,c)\) is
\[
                 -8ab+10a^2-10bc+6b^2+18c^2,
\]
which matches the weights \(4,5,3,9\).

Lean first proves the derivative of
\((q+td+t^2e)^2\) at every real \(t\), and the derivative of that
first-derivative formula at zero. Its value is \(2d^2+4qe\).
Polynomial identities connect these formulas with the residuals on
the actual affine line. Sum and difference rules then establish a
first derivative for \(F(X+tv)\) at every \(t\).

The theorem about the second derivative explicitly identifies the
function \(t\mapsto\operatorname{deriv}(s\mapsto F(X+sv))(t)\)
with its proved first-derivative formula before differentiating again.
Thus the lower bound is not a statement about an independently named
polynomial assumed to be a Hessian. It is a theorem about
\[
 \left.\frac{d^2}{dt^2}F(X+tv)\right|_{t=0}.
\]
The differentiability proofs also avoid relying on the default value
of Lean's total derivative operator at a nondifferentiable point.

The final theorem is unconditional in \(X\) and \(v\). It has no
restriction to a bounded set, positive coordinates, or unit directions.
It proves the lower bound \(v_1^2+v_2^2+v_3^2\) at every base point.

## The exact weighted-square certificate

The certificate uses the same rational center \((3/4,1,1/2)\) as the
mathematical checker. Let \(u=X-(3/4,1,1/2)\) and
\(Z=(v,u\otimes v)\). Its literal expression consists of twelve
positive rational multiples of squared integer linear forms in \(Z\),
and the nine additional squares \(Z_3^2,\ldots,Z_{11}^2\).

The extra nine squares are necessary. The generator starts from a
factorization of \(M-I\), while the desired curvature gap subtracts
only \(\|v\|^2\), rather than \(\|Z\|^2\). The identity is therefore
\[
 v^{\mathsf T}\nabla^2F(X)v-\|v\|^2
   =\sum_{i=0}^{11}c_iW_i(Z)^2+\sum_{i=3}^{11}Z_i^2.
\]

Lean proves this complete identity after substitution into the original
variables. The rational constants are elaborated as real field
operations; they are not truncated integer divisions. Positivity of
the expression is checked separately, and the actual derivative
theorem transfers it to the final curvature bound.

I independently reran the
[generator](generate_ternary_lean_certificate.py) and compared its
complete output with the certificate definition in the Lean file.
They match exactly. The generator is not a proof premise: even an
incorrect external factorization would have had to pass the polynomial
identity and positivity proofs in Lean.

## Compilation, axioms, and source fingerprint

From the formal directory, I ran:

    lake env lean TernarySOSDescent.lean
    lake env lean --version

The targeted file check exited with code zero and no warnings.
The compiler reported Lean 4.33.1, matching the pinned toolchain.
All six printed transitive axiom reports contained exactly

    [propext, Classical.choice, Quot.sound]

These reports cover the zero, stationarity, actual second derivative,
weighted-square identity, its nonnegativity, and the final curvature
lower bound. No report contains a custom axiom or a placeholder proof
axiom. Source inspection also found no admitted proof, unsafe code, or
native decision procedure.

The independently checked file SHA-256 was

    d290557f8c15084e53e51a883f3a23c4bb18975239a7523442e35cd8aec14e5e

It matches the author's frozen version and verification record. An
additional inline Python command checked exact generator correspondence
and the twelve generated LDL square forms. No project-wide build or
CI inspection was performed.
A final standard-library document check passed newline, whitespace,
control-character, math-delimiter, and five local-link checks, and
confirmed that the compiled Lean source hash remained unchanged.

## Precisely what the Lean result leaves open

The verification record correctly distinguishes the formal statements
from their mathematical consequences. The file does not package
global convexity, strong convexity, the global lower bound
\(F(X)\geq\|X-p\|^2/2\), nonnegativity, or uniqueness of the zero
as separate Lean theorems. Those follow mathematically from the
verified zero, directional stationarity, and uniform curvature bound,
using the analytic argument in the main note.

Nor does this file prove the field-degree calculation, nonexistence
of rational SOS, the classification of real coefficient fields,
minimal affine dimension, or rational SOS after adding a positive
constant. It does not formalize an integer-polynomial datatype,
coefficient counts, or positive definiteness of the particular full
Hessian Gram matrix. The scalar identity proves the directional
curvature statement without packaging those matrix assertions.

These exclusions do not reveal a proof gap in the stated Lean
theorems. They define the formalization's scope. The broader results
retain their separate mathematical proofs, exact checks, and
[independent review](ternary-rational-sos-convex-counterexample-independent-review.md).
Publication priority is outside this verification.
