# Correspondence review of the quartic Lean proof

Date: 2026-09-28. Scope: independent source review of
[ConvexQuarticIrrationalZero.lean](../formal/ConvexQuarticIrrationalZero.lean)
against [the quartic construction](convex-quartic-irrational-zero.md)
and [the root audit](convex-quartic-root-audit.md).
Verdict: the formalized polynomial and zero-set conclusions match the
mathematical notes. No missing hypothesis, changed coefficient, admitted
proof, or mathematical mismatch was found. The addendum below also checks
the later formal derivative, rational certificate, and convexity extension.

**Current coverage includes global convexity and the actual second
directional derivative bound with constant 4096**, together with the
algebraic zero set, existence, uniqueness, and exclusion of rational
feasible points. The stronger constant 4124 is not formalized. The
original review below records the earlier zero-set-only snapshot; its
limitations are historical and are superseded where stated by the
addendum.

## Exact polynomial correspondence

The Lean definition `quadratic` is precisely

\[
 A(x,y)=12599x^2-10000xy+7937y^2-15874x-12599y+20000.
\]

Its definition `quartic` is precisely

\[
 F(x,y)=A(x,y)^2+10000\bigl((x^2-y)^2+(y^2-2x)^2\bigr).
\]

All six coefficients of $A$, both factors $10000$ and $2$ in $F$, and
both signs inside the squares agree with the note and root audit.
Lean's expression `quadratic x y ^ 2` means `(quadratic x y) ^ 2`;
it does not substitute $y^2$ into the second argument. The definitions
have real inputs and outputs with exact integer numerals, so no decimal
rounding or approximate root is involved.

The file does not package $F$ as a multivariate polynomial over
$\mathbb Z$ or formally state its degree or expanded coefficient bound.
Those facts are readable from the exact expression and checked elsewhere;
they should not be listed as separate theorems proved by this file.

## Theorem correspondence and assumptions

| Lean declaration | Exact content relevant to the note |
| --- | --- |
| `quartic_nonneg` | $F(x,y)\geq0$ for every real $x,y$. |
| `quartic_eq_zero_iff` | $F(x,y)=0$ iff $x^3=2$ and $y=x^2$, for arbitrary real $x,y$. |
| `quartic_le_zero_iff` | The same characterization with $F(x,y)\leq0$. |
| `cube_two_bounds` | Every real solution of $x^3=2$ lies strictly between 1 and 2. |
| `cube_two_irrational` | Every real solution of $x^3=2$ is irrational. |
| `quartic_pos_at_rationals` | $F(x,y)>0$ for every rational pair, evaluated after coercion into $\mathbb R$. |
| `cubeRootTwo_cube` | The defined real number $2^{1/3}$ has cube 2. |
| `quartic_zero_unique` | $F(x,y)=0$ iff $x=2^{1/3}$ and $y=(2^{1/3})^2$. |
| `quartic_has_zero` | There exists a real pair at which $F$ is zero. |
| `quartic_has_no_rational_nonpositive_point` | There is no rational pair satisfying $F\leq0$. |

These declarations have no standing hypotheses about convexity,
positivity of the variables, a bounded box, existence of a zero, or
irrationality. The two lemmas about a real cube root explicitly assume
$x^3=2$, and their callers establish that assumption. Existence is
proved separately, so the zero-set equivalence is not merely a
conditional uniqueness statement.

The forward direction of `quartic_eq_zero_iff` extracts vanishing of all
three squares, obtains $y=x^2$, and excludes $x=0$ because
$A(0,0)=20000$. It then cancels the nonzero factor in
$x(x^3-2)=0$. The reverse direction uses $x^3=2$ and $x^4=2x$ to
prove $A(x,x^2)=0$ exactly. This is the same argument as the root audit.

For irrationality, Mathlib's `irrational_nrt_of_notint_nrt` states that
a real number with an integer positive power is irrational if it is not
an integer. The file proves the latter condition from $1<x<2$ and uses
the lemma with exponent 3 and integer 2. The assumptions and actual
lemma statement were inspected in the installed Mathlib source. This is
a valid alternative to the note's Eisenstein argument.

The definition `cubeRootTwo` uses real exponentiation, with the existence
identity supplied by `Real.rpow_inv_natCast_pow`; its hypotheses are
$0\leq2$ and a nonzero natural exponent 3, both discharged explicitly.
Strict monotonicity of the odd power $x\mapsto x^3$ identifies every
real cube root with that definition. In particular, there is no ambiguity
about a complex root or a negative branch.

Nonnegativity, existence, and unique zero together imply a unique global
minimum of value zero, but this implication is not separately expressed
using a Lean optimization predicate. The identity
$(2^{1/3})^2=\sqrt[3]4$ and membership of the point in the interior of
$[1,2]^2$ are also not separate formal statements in this file.

## Compilation, axioms, and reproducibility

The author reported the completed targeted command, run from `formal/`:

```text
lake env lean ConvexQuarticIrrationalZero.lean
```

It exited with code zero and printed only the four requested axiom
reports. For each of `quartic_eq_zero_iff`, `quartic_zero_unique`,
`quartic_has_zero`, and
`quartic_has_no_rational_nonpositive_point`, the report was

```text
[propext, Classical.choice, Quot.sound]
```

These are standard Lean foundations. No `sorryAx` or additional custom
axiom appeared. Source inspection found no `sorry`, `admit`, `axiom`
declaration, unsafe proof escape, or unproved local assumption. Imports
are Mathlib's real-power and irrationality results and ordinary
proof-producing tactics.

The reviewer independently checked that the inspected source has SHA-256

```text
3971d6af149c96a569a0cd1fa75e364fcfa252252ea11f010202865f1d4994a5
```

matching the author's successful compilation record. The workspace pins
Lean and Mathlib to version `v4.33.1`. This review did not repeat the
completed Lean build. Its independent contribution is source-to-statement
correspondence and examination of the hypotheses, proof structure, and
reported axiom dependencies. The compiler success and axiom output are
the author's observed check, tied to the matching source hash.

## Original snapshot: limitations and documentation correction

There was no Hessian, derivative, matrix inequality, strong-convexity
predicate, or bound $\nabla^2F\succeq4124I$ in the original inspected
snapshot. At that stage, its formal result established the exact
algebraic and irrationality components. The extension reviewed below
adds derivatives and convexity. Novelty and interpretation of the
literature remain outside Lean's scope.

At the time of review, the construction note's final paragraph still
said that no formal proof-assistant verification was claimed. This has
become stale for the algebraic part. The author was notified to replace
it with the precise scope above. The root audit's account of checks it
personally ran remains accurate and can link the later formalization.

Targeted checks performed by this reviewer were source reads, searches
for admitted proofs and declaration assumptions, inspection of the two
Mathlib lemmas, a SHA-256 comparison, and Markdown link and whitespace
checks of this review. No Lean build, project-wide verification, or CI
inspection was repeated.

## Addendum: directional derivatives, rational certificate, and convexity

The final extended source was reviewed at SHA-256

```text
71930973ac11e67f5b223414bad754c6c112723acb99b2c0bd59e08f8d28dc61
```

An independent `sha256sum` call matched this fingerprint to the author's
reported successful build. The definitions of $A$ and $F$ and all
zero-set declarations above are unchanged. The added declarations
match the [rational Hessian certificate](convex-quartic-rational-sos.md)
and the updated [formal verification record](convex-quartic-lean-verification.md).
No substantive correction was required.

### Actual derivatives of the original quartic

The functions `quadraticFirst` and `quadraticSecond` are respectively

\[
 \begin{aligned}
 DA(x,y)[a,b]&=(25198x-10000y-15874)a
                 +(-10000x+15874y-12599)b,\\
 D^2A[(a,b),(a,b)]&=25198a^2-20000ab+15874b^2.
 \end{aligned}
\]

Their coefficients and mixed-term factor agree with direct
differentiation of $A$. The added `quarticFirst` is
$2A\,DA+20000(q_1Dq_1+q_2Dq_2)$, and `hessianForm` is

\[
 2(DA)^2+2A\,D^2A+
 20000\bigl((Dq_1)^2+q_1D^2q_1+(Dq_2)^2+q_2D^2q_2\bigr),
\]

with $Dq_1=2xa-b$, $Dq_2=2yb-2a$, $D^2q_1=2a^2$, and
$D^2q_2=2b^2$. Thus its intended mathematical meaning is the exact
quadratic-form Hessian of $F$.

The proof does not merely assign these names. The four `HasDerivAt`
theorems establish the first and second derivatives along
$(x+ta,y+tb)$ for every real base point, direction, and parameter $t$,
using sum, product, and power rules. `quartic_line_second_deriv` then
proves the actual equality

\[
 \left.\frac{d^2}{dt^2}F(x+ta,y+tb)\right|_{t=0}
 =\operatorname{hessianForm}(x,y,a,b).
\]

In particular, Lean's totalized derivative operator is not being used
at a potentially nondifferentiable point: differentiability of the
function and its first derivative is proved everywhere.

### Exact 21-square certificate

`hessianGapSOS` uses the substitutions
$X=100x-126$ and $Y=100y-1587/10$, exactly inverse to the rational
coordinate change in the certificate note. Its six expressions $v_i$
and 21 positive integer square coefficients match the documented
diagonally dominant Gram decomposition, including every off-diagonal
sign. The theorem `hessian_sos_identity`, proved by `ring`, states

\[
 16000000\bigl(\operatorname{hessianForm}(x,y,a,b)
                  -4096(a^2+b^2)\bigr)
 =\operatorname{hessianGapSOS}(x,y,a,b).
\]

The right-hand side is proved nonnegative by `positivity`. Division by
the positive scaling constant yields `hessianForm_lower_bound`, and
the actual derivative equality yields
`quartic_second_deriv_lower_bound` for all real $x,y,a,b$. No
restriction to a rational point, a finite test grid, a neighborhood of
the zero, or a unit direction is present.

As a separate correspondence check, an inline Python command parsed the
integer matrix $N$ in the certificate note, computed its six diagonal
dominance margins, and compared the resulting six individual squares
and 15 pair squares against the Lean expression. All 21 coefficients
and signs matched exactly. The command also checked the rational shift,
scale $16000000$, and bound $4096$. It did not rerun the overlapping
symbolic polynomial identity check or Lean compilation.

### Functional convexity, not only a curvature expression

`quartic_line_convex` proves convexity on every complete affine line.
The installed Mathlib theorem `convexOn_univ_of_deriv2_nonneg` requires
differentiability of the real function, differentiability of its first
derivative, and nonnegativity of its second derivative at every real
point. The proof supplies all three requirements from the preceding
`HasDerivAt` theorems and the global Hessian-form lower bound.

Finally, `quartic_convex` has the unconditional statement

```text
ConvexOn ℝ Set.univ (fun p : ℝ × ℝ => quartic p.1 p.2)
```

Its proof applies line convexity with base point $p$ and direction
$q-p$, takes the line parameters 0 and 1, and identifies the weighted
parameter with the convex combination of the two points. The weights
are assumed nonnegative and sum to one exactly as required by
`ConvexOn`. The endpoint and interpolation identities are proved by
ring arithmetic. This establishes global convexity of the same
two-variable function whose irrational singleton zero sublevel was
already formalized.

### Final build evidence and remaining limits

The author reported that the final targeted command
`lake env lean ConvexQuarticIrrationalZero.lean` exited with code zero
and no warnings. The six headline `#print axioms` outputs comprise the
original four statements plus `quartic_second_deriv_lower_bound` and
`quartic_convex`; each lists only
`propext`, `Classical.choice`, and `Quot.sound`. The reviewer again
inspected the entire source for admissions and custom assumptions and
found none. The build was not repeated.

The reviewed final source therefore formalizes the rational quartic's
global `ConvexOn` property, positive uniform directional curvature with
constant 4096, real zero existence and uniqueness, and absence of any
rational point in its zero sublevel. It does not identify an explicit
matrix of second partial derivatives or package the quantitative result
as a named strong-convexity predicate. The mathematical implication to
strong convexity follows from the verified directional bound. The
stronger constant 4124, polynomial degree and coefficient-size
statements, box-interior membership, and literature comparison retain
their separate mathematical checks.

The main note and verification record have now replaced the stale
zero-set-only scope statement. Targeted checks for this addendum were
the independent final fingerprint, the 21-term transcription check,
inspection of Mathlib's second-derivative convexity criterion, and
Markdown link, display-delimiter, and whitespace checks. No
project-wide verification, CI inspection, or duplicate Lean build was
run.
