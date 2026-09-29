# Independent review of the tower's rational auxiliary certificates

Date: 2026-09-28. Status: passed; no substantive defect found.
Reviewer: `one_parameter_spectrahedral_fields`, who did not develop
these companion statements.

The reviewed files are
[tower-rational-auxiliary-certificate.md](tower-rational-auxiliary-certificate.md)
and [tower-sos-coefficient-encoding.md](tower-sos-coefficient-encoding.md).
Their initial frozen hashes were respectively
`c2c2c191276a1dfbc4efbe606c27a33609218f3f4cd3551272bbe1fc21ef985c`
and `85c97557a0e38df63c0e0f3216a422a62bd3d30c9d6cce8c4f145c992dfe33ed`.
This review takes the previously reviewed tower construction and its
individual-coefficient lower bound as inputs. It does not reprove
those earlier results or establish novelty of the companion formats.
The author then applied the final-Gram clarification and reviewed-status
links. I reread the amended text and checked the resulting hashes:
`a500704322d031d67b3ac0233c70b6f8850e59682aab34d3a17171e21f4248e6`
for the auxiliary note and
`c63fab7b45f322c3cbe84a3ed4de2c772a891281b9c39e1def807e0862af581e`
for the encoding note. No review issue remains.

## Taylor identity and rational SOS

Let `M` be the rational positive definite Hessian Gram of the final
quartic `F`. This must be the final Gram, rather than the baseline
Gram also denoted `M` in the tower construction. The final text now
explicitly distinguishes the two, resolving the notation ambiguity.

With `u=X-Y`, `A=(u,Y tensor u)` and `B=(0,u tensor u)`, the
Hessian biform on the line from `Y` to `X` is
`(A+tB)^T M (A+tB)`. The exact integration moments against `1-t`
are `1/2`, `1/6`, and `1/12`. The middle scalar multiplies the
two equal cross terms, so the result is

```text
(1/2) A^T M A + (1/3) A^T M B + (1/12) B^T M B
= (1/2)(A+B/3)^T M (A+B/3) + (1/36) B^T M B.
```

Taylor's formula therefore gives precisely the first-order convexity
difference asserted in the note. Each vector entry has total degree
at most two, so its SOS Gram has degree at most four. Rational
congruence preserves rationality and positive semidefiniteness.

For the signed-square expression `F=sum w_j q_j^2`, differentiation
before any ideal rewriting gives

```text
F(Y)+grad F(Y) dot (X-Y)
= sum w_j [q_j(Y)+2 grad q_j(Y) dot (X-Y)] q_j(Y).
```

This identity permits the negative weight on the removed quadratic
relation: the multipliers are ideal coefficients, not SOS weights.
Every multiplier has total degree at most two. It proves the stated
degree-four SOS-plus-equalities identity without differentiating an
ideal identity as if its coefficient functions were constant.

## Root equations and elimination of the redundant equations

At every gate, direct expansion verifies

```text
y^2-xz = -y(x^2-y) + x(xy-z),
z^2-bx = -z(xy-z) + x(yz-b).
```

These hold as polynomial identities even when `b` is a predecessor
variable. For a quintic gate the local quadratic moment differences
are the two root relations of weights two and three and the relation
`y^2-xz` of weight four. The exposing construction adds `z^2-bx`
and `yz-b`. Thus the returned quadratic `G` is indeed in the root
ideal with affine rational coefficients, as is the removed relation
`R`. Multiplying the degree-two multipliers by these affine
coefficients gives degree at most three; the certificate after their
elimination has total degree at most five. Cancellations account for
the fact that the affine-multiplier identities still represent
quadratic polynomials.

The auxiliary equations have a real solution independently of the
SOS identity. The first two equations at a gate force `y=x^2` and
`z=x^3`; the third then says `x^5=b`. Starting from `b=2`, the
unique real fifth root is positive, and the same recursion applies
to each predecessor value. It produces exactly the stated coordinates
`(a_i,a_i^2,a_i^3)` with `a_i=2^(1/5^i)`. No expanded high-degree
polynomial or algebraic coefficient is needed to state this existence
proof. Substituting this same real solution for every fixed `X`
therefore legitimately proves unrestricted nonnegativity of `F`.
An identity modulo an inconsistent system would not suffice; the
note correctly includes the existence argument.

## Size and the shared-root upper bound

The rational Hessian Gram, exposing quadratic, root equations, and
weights have polynomial printed size by the tower construction.
All transformations here use fixed polynomial degree and polynomial
matrix dimension. Expanding their rational coefficients therefore
takes polynomial time and has polynomial output size. Rational LDL
factorization has polynomial bit complexity on these matrices.

For a positive rational LDL weight `a/b`, write the integer `ab` in
binary. An even-position bit is a single integer square, while an
odd-position bit is the sum of two identical integer squares. Divide
the square bases by `b`. Their squared sum is `ab/b^2=a/b`, using
at most twice the bit length of `ab` factors, all of polynomial bit
length. This avoids assuming a deterministic polynomial-time integer
factorization or four-square algorithm.

For the shared-root encoding, the substitution `Y=p` makes each
Hessian square affine in the line parameter, with coefficients `U,V`
of total degree at most two in `(X,p)`. The formula

```text
integral_0^1 (1-t)(U+tV)^2 dt
= 2 ((U+V/3)/2)^2 + (V/6)^2
```

gives actual squares without adding any irrational scalar operation.
Every coefficient is a rational polynomial of degree at most two in
the coordinates of `p`. The original `k` fifth-root gates and two
multiplications per gate produce those coordinates; a polynomial-size
shared arithmetic circuit then evaluates every coefficient. This
matches the claimed polynomial upper bound for that representation.

Conversely, the imported individual-coefficient theorem supplies an
algebraic coefficient of degree at least `5^k`. Every nonzero rational
annihilating polynomial for it has at least that degree, so a dense
coefficient list uses at least `5^k+1` positions. This is a bound for
dense algebraic output, not for the shared root circuit. The notes
correctly distinguish exponential growth in `k` from a claim of
exponential growth in the whole input bit length. They also avoid
claiming that arbitrary root-circuit identities are easy to verify.

## Primary attribution and exact checks

I directly checked Theorem 3.1 of Ahmadi and Parrilo,
[*A Complete Characterization of the Gap between Convexity and SOS-Convexity*](https://web.mit.edu/~a_a_a/Public/Publications/sos_convexity_tables.pdf).
It states the equivalence between an SOS Hessian biform and an SOS
first-order convexity difference. Thus the main Taylor-SOS principle
is correctly identified as established theory. The explicit rational
quartic formula and representation comparison here do not support a
new general proof-system claim.

Commands actually run:

```text
python research-20260927/check_tower_auxiliary_certificate.py
python research-20260927/check_tower_auxiliary_review.py
```

The author's checker passed its coupled two-gate ideal, derivative,
Taylor, integration-Gram, degree, and rational-square checks.

The [independent checker](check_tower_auxiliary_review.py) uses a
different three-variable quartic with an explicit positive definite
12-by-12 rational Hessian Gram. It checks the actual Hessian identity,
all positive rational LDL pivots, the conversion into 91 rational
Taylor squares, their degree and rational coefficients, and their
exact polynomial identity. This supplements the author's symbolic
test, which does not itself require convexity of its example. Neither
finite check re-verifies the earlier universal tower construction or
its coefficient-field lower bound. No Lean, project-wide checks, or
CI inspection were performed for this review.
