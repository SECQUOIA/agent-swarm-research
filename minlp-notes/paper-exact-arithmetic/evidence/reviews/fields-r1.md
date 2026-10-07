# Fields and certificate review, round 1

This review reads the actual manuscript in `sections/08-fields.tex`,
`sections/09-certificates.tex`, `appendices/G-fields.tex`, and
`appendices/H-certificates.tex`. It also reads the shared model, algebraic,
and height statements and proofs used by these chapters. The prewriting
reviews are background, not the verdict. A delegated independent reviewer
also reconstructed the tower stationary-space induction and cyclic
quadratic-space argument. No manuscript file was edited.

The author was still revising Appendix G during the first pass. The latest
refresh and disposition of the findings are recorded below. Line references
in the initial findings are historical unless the refresh says otherwise.

## Findings requiring resolution

### F-R1. Arbitrary scale is missing from compact-certificate size bounds

**Severity: substantive encoding error; straightforward repair.**

At the initial reviewed snapshot, Section 08 lines 492–507 permits an
arbitrary rational scale `lambda`, counts its binary length in the input,
and then states time and output size polynomial only in `k` in both parts
of `thm:fields-compact`. Appendix G's compact-certificate proof likewise
says that the bit lengths of rational coefficient polynomials are
polynomial in `k` alone. The matrices depend on `lambda`; an arbitrarily
long supplied rational cannot be read or copied to rational circuit
constants within a bound polynomial only in `k`. Fix these bounds to be
polynomial in `k` and the binary length of `lambda`, or restrict the scale
to the constructed polynomial-bit scale. The former matches the stated
input contract and the proof. This does not affect the least-field theorem.

### F-R2. Rational radial finiteness omits nonnegativity and needs its exact contract

**Severity: false literal statement plus unresolved source/proof contract
for an ancillary existence claim.**

Section 09 lines 223–232 asserts that a rational polynomial of even degree
with positive definite leading form, finitely many real zeros, and
positive definite Hessian at those zeros admits a rational SOS after
multiplication by a power of `1+||X||^2`. It omits nonnegativity. The root
identified the direct counterexample `f=x^2-1`: its leading form is
positive definite, its two real zeros have Hessian 2, and every radial
multiple is negative at zero. Explicitly require `f>=0` on all real
points. The constructed certified quartics with minimum zero satisfy
that repaired hypothesis.

The text cites Burgdorf,
Scheiderer, and Schweighofer (2012), generally describing pure states and
order units on the sphere. It does not state the exact imported theorem or
give the rational sphere-ring deduction. The distinction matters: a
real-coefficient Hessian theorem alone does not establish rational
descent. The root was asked to obtain the exact theorem, ring/ideal
hypotheses, and rational descent contract through the authorized Luna
literature agent. Alternatively, include the complete sphere-ring
deduction from precisely stated imported contracts.

The unbounded and quantitative radial lower bounds do not depend on this
existence claim: they remain valid with order in the extended nonnegative
integers. Appendix H invokes this source only to say the order is finite.

### F-R3. Cyclic diagnostics and local notation

**Severity: minor scope/clarity issue; no false uniform claim.**

Section 08 lines 719–724 correctly leaves cyclic `J_4=W` open for all
dimensions and applies descent conditionally. It says only that small
exact computations are consistent with the equality. The retained record
covers `n=2` and `4<=n<=16` for the descent application; `n=3` has five
quadratic relations and fails the required dimension. If these diagnostics
are retained, state their finite range and identify them as recorded
diagnostics rather than a proof of any uniform stationary-space theorem.
No rerun is needed or authorized. The current manuscript does not use the
diagnostics to prove a theorem.

Appendix G's cyclic proof switches from `d_n,e_i` to `d,s_i` and uses `a`
without a local definition. Add `d=d_n`, `s_i=e_i`, and `a=2^(1/d)`.

### F-R4. Shared-lemma references repaired during authoring

**Severity: resolved in the live authoring pass, pending final refresh.**

The first snapshot had a proof of `lem:fields-tools(e)` although the main
lemma now lists only (a)–(d), and retained undefined private labels for the
canonical Gram, regularization conditions, and block-square estimate. The
later snapshot removes the duplicate Taylor-square proof and uses the
shared Taylor and quartic-realization interfaces. The prime proof now
obtains its rational canonical Gram directly from the shared realization
bound. These are the correct interfaces; check final source references
after the author finishes.

### F-R5. Tower baseline normalization no longer matches its multiplier proof

**Severity: substantive interface error introduced during authoring;
straightforward repair.**

The refreshed Appendix G lines 552–558 defines
`F_{k,0}=(G_k/(t nu))^2+sum (r_{i,j}/nu)^2`, with weights
`sigma_0=(t nu)^(-2)` and `sigma_1=nu^(-2)`. Section 09 lines 203–208 still
applies the multiplier theorem to the alleged factors `G_k,t r_{i,j}` of
this same `F_{k,0}`. Those factors instead represent `t^2 nu^2 F_{k,0}`.
Because the resulting `lambda_*` is then used directly as a scale of
`F_{k,0}`, this is more than a missing explanatory scalar.

Use the actual factors `G_k/(t nu),r_{i,j}/nu`, select the first factor as
the positive-leading quadratic, and supply
`r_{k,3}=nu x_k(r_{k,2}/nu)-nu y_k(r_{k,1}/nu)` as affine membership. The
multiplier theorem then applies with the stated scale. In part (b), make
the analogous scalar explicit: for `h_i=(N_1/N_0)C_i`, use
`r=(N_0/N_1)(x_0 h_1-x_1 h_0)`.

### F-R6. The refreshed dimension remark drops an authorized result

**Severity: coverage issue pending exact source verification.**

Section 08 lines 343–348 now says that the two-variable case is not settled
here and makes no claim that three variables are minimal. This is weaker
than the F2 inventory and the first authored version. Obtain the exact
Scheiderer (2016), Theorem 4.1 contract before deciding the result: the
original deduction from four distinct complex linear factors in general
position is valid if that is the theorem's applicable conclusion. A
conjugate pair intersects at a real point, two pairs give distinct real
zeros, and a real line factor would give infinitely many zeros, all
contradicting the unique real projective zero. A temporary deletion is not
a completed source verification or a coverage repair.

## Latest refresh

The refresh found F-R1 resolved: Section 08 lines 493–510 defines
`L_lambda=k+bits(lambda)` and states both time and size bounds in that
quantity; Appendix G lines 683–687 now uses the same bound. The rational
coefficient-polynomial construction proves this revised statement.

F-R2's missing nonnegativity is now repaired at Section 09 lines 227–232.
The exact rational source contract remains unresolved. The author removes
the use of finiteness in Appendix H lines 399–400 and describes the general
statement as a route through prior theory; the lower-bound proofs are
therefore independent of it. The prose still states the general existence
conclusion, so it still needs its precise source contract.

F-R3's cyclic notation is repaired at Appendix G lines 858–866. The finite
diagnostic range remains unspecified, and no all-dimension stationary-space
claim is made. F-R4 is resolved: the duplicate private Taylor proof and
unresolved private labels are absent in the refreshed files. The new prime
proof uses `t=N_0^(-1)`, the shared realization margin
`gamma>=1/(30n)`, and an origin-Gram bound on the removed square. Its
constants and normalization check out.

The same refresh identified F-R5 and F-R6, which were sent to the root
immediately. A separate minor shared-interface wording issue was sent to
the root: Section 06's quadratic-graph discussion should say
`g_hatp(w_*)=0` exactly, rather than saying the exposing quadratic
“vanishes exactly at” that point, which can suggest a unique zero. The
assembled quartic has the unique zero; a nonzero small gradient of the
exposing quadratic prevents it from having a unique zero.

## Mathematical audit

The rational-Hessian Taylor-square interface is sound. It first eliminates
a rational PSD Hessian Gram using rational weights, then writes each
positive rational as a sum of rational squares. The exact integration
identity uses only rational constants. Thus a stationary zero in a real
field gives actual square factors over that field. It never factors an
arbitrary field-valued PSD Gram into squares over the same field. The
`sqrt(2) X_1^2` example now correctly concerns a PSD full-basis Gram (and a
positive scalar Gram on its one-monomial basis).

The odd-radical lemma works over every real subfield, including fields with
transcendental elements. The real constant term of a factor of `T^D-2`
forces `a^r` into the field; Bezout then gives `r|D` and the binomial minimal
polynomial. The degree-five slice in the tower follows from the tower law,
without a hidden number-field assumption.

The prime construction supplies an integer quartic and an integer positive
definite full Hessian Gram. Its exposing identity, chain Jacobian bound,
rational approximation preserving exact vanishing, and Schur/realization
margin are uniform in the prime. The coefficient functional excludes both
square factorizations and PSD Grams independently. The ternary example
prints enough exact rational data and principal minors to specify and
certify its full Hessian Gram; its five vanishing relations and their
fifteen independent products are proved algebraically. The four-variable
example correctly supplies a different obstruction: `yz^3` lies in the
stationary space and outside the rational vanishing-product span.

The tower baseline's exposing form, geometric coupling weights,
dyadic coefficient approximations, and residual Jacobian bounds give a
polynomial-size rational full Hessian Gram. Its last-gate slice has the
five stated vanishing quadratics and independent products. The negative
direction of the unique restricted matrix excludes both certificates
over an arbitrary real field lacking the terminal radical. Actual Taylor
squares prove the converse. The Galois proof of the individual-degree
claim is valid: an order `ell^k` automorphism in the radical splitting
field lifts to the normal closure of the coefficient field, while a
product of symmetric groups of smaller degrees has no element whose order
has that `ell`-adic valuation. A large compositum degree alone is not being
used as a substitute for this proof.

The compact auxiliary identity has the correct signs and degrees. Taylor
integration gives a rational SOS in `(X,Y)`, and the signed rational
quadratic-square representation supplies the degree-two ideal
multipliers. The two redundant quadratic equations have affine membership
in the chain residuals, raising the identity degree to at most five. The
root system is explicitly solvable. The root-circuit output remains an
algebraic coefficient representation; it does not turn irrational
coefficients into rational ones.

The tower quadratic-space, product-independence, and stationary-space
proofs are uniform. The local cubic first-jet map has five nonsingular
residue blocks. The quartic induction correctly uses earlier derivatives
to force the sum of the `y_k^2` and `x_k z_k` coefficients to vanish, then
removes mixed relation products and applies the cubic and earlier quartic
inductions. The recognition algorithm reduces monomial exponents without
expanding the degree-`5^k` field, solves a polynomial-size rational system,
and performs one rational PSD test. It recognizes rational SOS at the
supplied tower point; it does not claim real-SOS recognition or recovery of
an unknown zero.

The descent theorem is sound under all three stated hypotheses. The
baseline has a PD restricted Gram because a singular matrix would give at
most `n` real squares. The first singular point along the segment is
permitted to have irrational parameter: the real SOS-length theorem
applies. The nonnegative leading quartic forms ensure the interpolant
still has degree four. The same boundary argument proves product
independence. The shared SOS-length proof explicitly removes quartic-flat
directions using convexity, then applies proper-map degree and parity; it
does not silently assume a positive definite leading form. The cyclic
quadratic-space proof is uniform for `n>=4`: an unused cyclic index and
the magnitude estimate reduce modular collisions to integer equality,
and valuation gives exactly the stated disjoint pairs. Its stationary
quartic equality is still open in the manuscript.

Affine denominators cancel by vanishing on their real hyperplane. The
multiplier-to-denominator identity correctly clears to `omega^2 f`, not
`omega f`. The general affine-membership proof retains both constant and
linear corrections in its zero identity, allows an arbitrary-signature
target matrix, and does not infer membership of low degree from ideal
membership alone. The explicit target `1` separates degree-two membership
from affine membership. The higher-membership proof's diagonal congruence
leaves an extra small factor on every correction and produces the stated
PD matrix and zero set. Its complexity counts the expanded monomial basis;
the targets remain quadratic.

The radial proofs use the real span of rational vanishing polynomials,
not the full real vanishing space. The grid functional supplies strict
positivity on that span at each degree, and the Schur extension preserves
the negative value on the fixed quartic. The adjugate, determinant--trace,
and grid bounds give the stated `O(N log N)` bound on the logarithm of the
threshold's logarithm; inversion yields the lower bound for every
sufficiently large integer scale. The fixed Hessian at the minimizer and
short adapted quadratic denominator are correctly distinguished from the
prescribed radial hierarchy.

The block lift's completed-square identity has the correct error sign.
The graph realization provides a separate rational SOS baseline with full
PD Hessian Gram and the same graph zero, without computing the optimizer.
Adding it makes the second block strongly SOS-convex. A separated
certificate induces one scalar component; evaluating at both zero minima
forces that scalar to zero. The growing-field lower bound therefore
follows from the tower, whereas the joint rational SOS stays short. The
positive family forces `0<c<=m_k`; denominator arithmetic gives the
claimed local-Gram and unweighted-square length lower bounds. The two
separately stored constant coordinates are correctly part of the output
model. Cross-block monomial coefficients force every full joint Hessian
Gram to be singular, so no full joint PD claim is made. The shared graph
theorem preserves the exact minimum `N+1` real-square length.

## Checks and limits

The commands used for this audit were targeted text inspection with `rg`,
`nl`, `sed`, and `wc` on the manuscript and its review/authoring records.
No mathematical scripts, experiments, compilation, project-wide checks,
or CI inspection were run. The printed large fixed certificate identities
and principal minors were inspected as exact supplied proof data; no
historical diagnostic was presented as a computation performed here.

The internal proof mechanisms check out. The latest actual source still
requires the normalization repair in F-R5. Journal readiness also requires
the exact source contract in F-R2 and the dimension-three minimality
disposition in F-R6. The root and its SOS literature reviewer were asked
to verify the exact classification and rational sphere-ring contracts.
The scale-length defect F-R1 and private-interface defect F-R4 are
resolved, as recorded in the refresh.
