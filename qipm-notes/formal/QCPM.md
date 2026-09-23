# QCPM norm correction: formal verification

This development verifies the mathematical core of the QCPM correction in
[`paper/sections/15-corrections.tex`](../paper/sections/15-corrections.tex).
The reading copy is [`paper/main.pdf`](../paper/main.pdf), Section 15.1.
It concerns [arXiv:2311.03977v2](https://arxiv.org/abs/2311.03977v2),
dated 16 October 2024. The constants follow Algorithm 1 of that version.

## Verified statements

All declarations use the namespace `QipmFormal.QCPM`. The potential is an
explicit finite sum of squares, so its norm is Euclidean even though its
coordinate vectors use Lean's function type.

| Module | Mathematical content |
|---|---|
| [Potential.lean](QipmFormal/QCPM/Potential.lean) | Actual affine slack, complementarity, and potential; initialization from the row equations; the initial-point witness; failure of every fixed quadratic-decay coefficient; scalar-shift robustness; joint continuity and continuity of the compact-domain supremum; the fixed-box upper certificate. |
| [Clock.lean](QipmFormal/QCPM/Clock.lean) | The integrated clock, its strict monotonicity and interval image, a continuous inverse, the transformed envelope, and genuine integral substitution. It also checks the scalar chain rule and the kinetic and potential coefficients, and identifies the extra derivative term in the product clock. |
| [Schedule.lean](QipmFormal/QCPM/Schedule.lean) | The actual exponential bump, extended by zero at its endpoints; smoothness, positive normalization, schedule endpoints and range, the exponential tail estimate, and an explicit terminal window. |
| [NormBounds.lean](QipmFormal/QCPM/NormBounds.lean) | Nonnegative-integral terminal-window estimates, the constants 1/128 and 1/64, the Lipschitz norm–speed tradeoff, its bounded-derivative sufficient condition, and the global upper integral bound. |
| [Paper.lean](QipmFormal/QCPM/Paper.lean) | Composition for the spatial supremum of the actual potential and the actual schedule, including continuity and integrability and correspondence with the clock-time integral. |

The manuscript's principal claims map to the following declarations:

| Manuscript claim | Lean declaration |
|---|---|
| Proposition 15.1, initial-point supremum bound | `initial_value_le_sup_of_compact` |
| No fixed coefficient in the proposed quadratic-decay estimate | `no_uniform_quadratic_bound` |
| Robustness under every real scalar shift | `shifted_potential_sup_lower` |
| Equation (693), corrected clock-time norm identity | `clockNorm_eq_paperNorm` |
| Lemma 15.2, explicit terminal window | `schedule_terminal_le_quarter` |
| Theorem 15.3, norm lower bound | `clockNorm_schedule_lower` |
| Theorem 15.3, fixed-box upper bound | `clockNorm_schedule_box_upper` |
| Corollary 15.4, Lipschitz speed bound | `paperNorm_speed_lower`, together with `clockNorm_eq_paperNorm` |
| Bounded-derivative specialization | `clockNorm_derivative_speed_lower` |

For initialization `Me + q = e`, the potential satisfies

\[
f_\mu(e)=\frac d2(1-\mu)^2\leq\sup_{z\in\Omega} f_\mu(z).
\]

The compact fixed domain must contain `e`. The scalar-shift theorem
additionally requires a central point in that domain. For every real shift
`c`, it gives

\[
\sup_{z\in\Omega}|f_\mu(z)-c|\geq\frac d4(1-\mu)^2.
\]

For positive `a, eta` and a continuous positive schedule on `[0,1]`,
the corrected clock and its inverse give the norm identity

\[
\Lambda=\frac1{a\eta}\int_0^1
\frac{\sup_{z\in\Omega}f_{\mu(t)}(z)}{\mu(t)^3}\,dt.
\]

For the exact Algorithm 1 schedule, with its positive normalization `c_e`,
the sufficient threshold is explicit:

\[
0<\varepsilon\leq\min\{1/4,c_e\}
\quad\Longrightarrow\quad
\Lambda\geq\frac{d}{128a\eta\varepsilon^3\log(1/\varepsilon)}.
\]

More generally, an `L`-Lipschitz positive schedule on `[0,1]`, with
endpoints `1` and `eps` and `0 < eps <= 1/4`, satisfies

\[
\Lambda\geq\frac{d}{64a\eta L\varepsilon^2}.
\]

Monotonicity is unnecessary. A uniform derivative bound supplies the
Lipschitz hypothesis by the mean value theorem.

On the fixed box `[0,D]^d`, with `D >= 0` and a continuous schedule
satisfying `0 < eps <= mu(t) <= 1`, the proved upper certificate is

\[
\Lambda\leq\frac{F_D}{a\eta\varepsilon^3},\qquad
F_D=\frac d2\left[D(D\|M\|_\infty+\|q\|_\infty)+1\right]^2.
\]

Here the matrix norm is the maximum absolute row sum. No concentration
estimate replaces the spatial supremum.

## Source correspondence and manuscript changes

The source correspondence was checked against the v2 PDF as well as its
HTML rendering:

- Section 2.1.3 supplies `s(e)=e`.
- Equation (11) defines the squared-residual potential.
- Equations (18)–(20) specify the schedule and evolution.
- Algorithm 1 defines `h(t)=a*mu(t)^2`, where
  `a=gamma^2/(2*R_1*C_{d,delta})` and
  `C_{d,delta}=sqrt(d)/2+(3/4)*log(2/delta)`.
- The proof of Theorem 5 uses the time substitution and supremum estimate
  addressed by the correction. Its equation (23) has a normalization
  inconsistent with Algorithm 1, including a different logarithmic expression.

The manuscript now states the positivity and fixed-domain hypotheses,
defines the concentration factor explicitly, gives the endpoint threshold,
states scalar-shift robustness as a quantified inequality, and strengthens
the norm–speed corollary to Lipschitz schedules. It removes the unproved
assertion that the numerical quantity `J(eps)` tends to one and the associated
sharp asymptotic. The displayed numerical values are retained as diagnostics;
the proved lower bound is `J(eps) >= 1/64` in the stated range.

## Scope

The proofs take the explicit initialization row equations and domain
membership as hypotheses. They do not reconstruct the complete self-dual
embedding from arbitrary LP input. The identification of the Lean formulas
with the cited version is a checked source correspondence, not a formal proof
about an external PDF.

The clock-time envelope is constructed through the inverse clock; its
pullback identity, continuity, and integral substitution are proved.
The norm here is the time-integrated pointwise spatial supremum from the
manuscript. The development does not separately construct a multiplication
operator on an L² space or identify its operator norm with an essential
supremum on an arbitrary compact domain.

The development does not construct Schrödinger evolution or formalize the
external simulation and adiabatic theorems. It does not certify ground-state
preparation, discretization, periodic boundary conditions, or a localized
repair. The later discussion of those obligations is outside this Lean
development. In particular, a lower bound on this simulator norm is not an
unconditional query lower bound.

## Reproduction

From `formal/`, with the pinned Lean and Mathlib versions installed:

```sh
./scripts/verify.sh
```

In the repository's configured environment:

```sh
conda run -n qipm --no-capture-output bash scripts/verify.sh
```

This builds the project and checks every imported project declaration
against the axiom allowlist: `propext`, `Classical.choice`, and `Quot.sound`.
The audit rejects `sorryAx`, `Lean.ofReduceBool`, and project axiom
declarations, including unused axioms. Private declarations and declarations
outside the project namespace remain in scope.

`./scripts/verify.sh --replay` additionally rechecks the import closure in a
fresh Lean kernel environment. This optional full replay is distinct from
the ordinary build and axiom audit; it uses Lean's own kernel.

Rebuild the reading copy from `paper/`:

```sh
conda run -n qipm --no-capture-output make
```

The Lean sources are not needed to compile the PDF. The PDF's formal
verification paragraph describes the proof scope; the formulas and proofs
remain readable without Lean.

## Validation completed on 2026-09-20

- The integrated build and axiom audit passed for **621 project declarations**,
  covering both QCPM and the existing scalar certificate. Every audited
  declaration depends only on the three allowed standard axioms.
- Independent mathematical and source reviews checked the original v2 PDF,
  the formal statements, the complete clock/supremum/schedule composition,
  and the manuscript's claims about verification. All identified issues were
  resolved.
- Temporary negative audit probes correctly rejected an unused project axiom,
  an axiom outside the project namespace, a private proof using `sorry`, and
  a `native_decide` dependency. The temporary probes were not added to the project.
- The scalar baseline needed small proof-elaboration repairs, with no theorem
  statement changes. The audit's counter was explicitly typed, and its imported
  module-name array was computed once rather than repeatedly during the scan.
  Its acceptance criteria are unchanged.
- The PDF rebuilt to 195 pages with no LaTeX warnings, unresolved references
  or citations, or overfull/underfull boxes. Section 15.1 is on pages 173–176;
  those pages were rendered and visually inspected.
- The optional fresh-environment replay of the entire Lean/Mathlib import
  closure was **not run**. The validation above is the project build and
  declaration-level axiom audit.
