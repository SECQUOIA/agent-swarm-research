# Appendix L author report

Scope: Q13 and Q14, written in `appendices/L-further-arithmetic.tex`.
The root authorized the Sol fallback after the assigned Opus author reached
its rate limit before producing Appendix L. No other manuscript, historical
note, bibliography, or shared macro was edited in this lane.

## Coverage and exact contracts

- `app:further-arithmetic` is the appendix entry point.
- `thm:ncq-feasible` gives common-field feasible points and NP membership
  for arbitrary weak rational quadratic systems of fixed constraint
  Hessian span. It explicitly credits Grigoriev–Pasechnik Theorem 1.2 and
  proves the minimum-dimensional-face corollary. It does not use their
  announced optimization Theorem 1.5.
- `lem:ncq-generic`, `lem:ncq-perturbation`, `lem:ncq-common-field`, and
  `lem:ncq-field-bounds` supply the separate nonconvex algebraic machinery.
  It covers indefinite Hessians, uses the full bordered KKT determinant,
  and counts explicit field degree in the input.
- `thm:ncq-infimum` gives an annihilator for a finite possibly unattained
  infimum. If attained, it gives at least one minimum-norm optimizer with
  one common-field representation. The objective Hessian is excluded from
  the span. The proof takes the inner generic perturbation limit before
  the outer norm-regularization limit and proves eventual inactivity of
  unknown auxiliary boxes before forming coefficients.
- `thm:ncq-oracle` gives fixed-span FP^NP classification, value, and
  minimum-norm output. Explicitly bounded integer variables can be guessed;
  no arbitrary unbounded-integer NP statement is made. The manuscript
  includes span-one feasibility and known-zero attainment hardness, an
  irrational span-one feasible set, and a finite unattained example.
- `thm:cone-feasibility` gives ordinary polynomial-time common-field
  SOCP/MISOCP feasibility for fixed integer dimension and continuous
  squared-Hessian span, without boxes or Slater assumptions. It returns
  an integer assignment whose original exact fiber is nonempty.
- `eq:cone-projection-prefix` and `eq:cone-blocks` expose the exact
  compressed projection, with fixed radius outside the universal block,
  all rank charts, a pointwise selected common finite perturbation grid,
  and algebraic-field block dimensions `(2,1,h+1)`. Fixed-block
  quantifier elimination supplies a mathematical quantifier-free
  description for the radius proof; neither large formula nor elimination
  is constructed by the algorithm.
- `lem:cone-rational-lift` prints a complete exact-rational Lorentz folding
  and tree construction, including coefficient bits and apex behavior.
  `eq:cone-rounding-error` proves the `66 Delta/256` residual bound. The
  gap belongs to the original exact system; rounded Hessians can have
  larger span and are used only in the final rational MILP.
- `thm:cone-witness` gives the absolute field `Q(alpha,x*)`, degree and
  total length `L^{O(h+1)}`, and runtime `L^{C_h}` for the continuous
  unique minimum-norm point. It recovers the tuple `(alpha,x*)`, keeps
  the input embedding map, and verifies original rows. The proper
  extension example has input field `Q(sqrt(2))`, point `sqrt(3)`, span
  one, and absolute degree four. Mixed output uses the original exact
  returned fiber and has polynomial bounds for fixed integer dimension
  and span, without a sharp exponent in the original mixed input.
- `cor:cone-threshold` covers rational original cone data and a known
  exact algebraic affine threshold, and the attainment query for a known
  finite infimum. `cor:cone-fractional` covers a known attained affine
  fractional optimum with rational original cone data and positive
  affine denominator. Its reciprocal cone adds at most one continuous
  Hessian direction. Neither corollary computes an unknown mixed value.

The coefficient-sensitive rational bounds separate structural size from
coefficient bits and stay linear in the latter. Nonconvex minimum-norm
optimizers are not called canonical unless uniqueness is established.
No ordinary polynomial global nonconvex optimization, standalone short
global-optimality certificate, arbitrary unbounded-integer NP result, or
absolute-exponent expanded-output FPT result is claimed.

## Mathematical interfaces read and used

Read the brief, conventions, decisions (including superseding D3), and
integration record. Read the complete independent prewrite audits
`prewrite-nonconvex-extension.md` and `prewrite-algebraic-cones.md`.
Inspected the source Hessian-span, finite-infimum, attainment, algebraic
threshold, algebraic witness, unbounded projection, and cone gap/lift
notes and their recorded review material. No recorded mathematical script
or experiment was rerun.

Read the actual Appendix J statements and proofs. L reuses:

- `lem:qc-heights` for product-formula and determinant height accounting;
- `lem:qc-elimination` for nonsingular multiplier roots and finite ordered
  scalar limits, including a dummy-inner-parameter specialization;
- `eq:qc-minpoly-height` for elementary rational factor height;
- `thm:qc-kll` and `thm:qc-recovery` for recognition and constructive
  recovery of one fixed tuple;
- `lem:qc-sign` for exact selected-root verification.

L does not apply J's native-PSD degree, height, or feasible-point theorems
to indefinite squared cone rows. All nonlinear limit arguments needed
by L are printed in L itself.

## Review responses and source precision

Two delegated read-only actual-draft reviews found no substantive gap in
the final nonconvex and cone architectures; the cone review included a
second independent witness/field scrutiny. Additional root reviewers
checked the same actual draft. The following local corrections were
applied:

- handled the zero-dimensional selected face before invoking GP;
- restored three omitted TeX command backslashes;
- included the polynomial summand factor in archimedean determinant
  coefficient-sum bounds;
- made the input-field scalar-height and integral-scaled primitive-element
  coefficient budgets explicit;
- stated mixed-coordinate minimum norm as the minimum over finitely many
  slices of the integer squared norm plus continuous squared norm;
- changed the opening to refer explicitly to Appendix J and counted only
  internal vertices in the Lorentz tree;
- broke the Pythagorean triple display to eliminate the only isolated
  overfull box.

The vetted literature lead confirmed GP Theorem 1.2, Lenstra Section 5,
Kocuk's cone construction, and the cumulative affine degree/projection
contracts. A preliminary KP relay omitted quantified-block factors. The
author flagged the impossible interpretation using an existential
repeated-squaring singleton. A second relay placed a block product outside
the degree exponent; the root's independent cone reviewer correctly
rejected that grouping using a repeated-d-th-power singleton. The
literature lead zoomed the primary display and corrected its grouping.

The final manuscript uses a simpler contract: Basu 2014 Theorem 2.27
gives per-output-atom degree `d^{O(n_w)...O(n_1)}` and integer
coefficient bits `b*d^{O(n_w)...O(n_1)O(l)}`, independently of input
atom count. For blocks `(2,1,h+1)` and `l=t+1`, these bounds are
`L^{O(h+1)}` and `L^{O((h+1)(t+1))}`. Only the quantifier-free
Khachiyan–Porkolab witness theorem is then used, with the unambiguous
bound `b'*(d')^{O((t+1)^4)}` independent of output atom count.
Its fixed-zero-coordinate feasibility reduction gives the displayed
integer radius `L^{C(h+1)(t+1)^4}`. The literature lead verified the
fixed-block degree/height contract on printed Basu pages 16–17 and the
quantifier-free empty-block convention in KP. No first-order source
superscript grouping is needed by the final L proof.

A fresh changed-scope cone review and its independent nested check
verified this final QE-first radius step at body SHA-256
`eb1b9e925d0299e07f6eed8e742a1e0522789164522bb267b719b2d72a292a74`.
They confirmed the radius exponent, convexity and integer-feasibility
preservation of the fixed-zero coordinate, and attainment of the constant
objective even for a nonclosed projection.

Actual citation keys requested for bibliography integration:
`GrigorievPasechnik2005`, `KrickPardoSombra2001`, `Heintz1983`,
`KhachiyanPorkolab2000`, `Kocuk2021`, `BenTalNemirovski2001`,
`Lenstra1983`, and existing `BombieriGubler2006` and `Basu2014`.
The literature lead owns
bibliography additions and canonical key reconciliation. Bibliography
integration is a root responsibility; no bibliography was edited here.

## Checks actually run

Targeted inline Python document checks on L checked final newline,
control characters, trailing whitespace, balanced environments and display
delimiters, 46 unique labels, and resolution of L's 68 current references
against the manuscript label catalog. They passed. This was a document
check, not a mathematical computation or project-wide verification.

`git diff --check -- paper-exact-arithmetic/appendices/L-further-arithmetic.tex`
returned no errors, but the file was untracked; the direct document check
supplies actual saved-file assurance.

An isolated temporary LaTeX wrapper, containing only Appendix L and the
shared preamble/macros, was compiled with:

    pdflatex -interaction=batchmode -halt-on-error -output-directory=/tmp/appendix-l-syntax-zxbh096y /tmp/appendix-l-syntax-zxbh096y/appendix-l.tex

It passed and produced a 15-page standalone appendix. The one initial
overfull triple display was repaired and the repeat had no overfull or
underfull boxes. Undefined cross-reference/citation warnings in the
isolated wrapper are expected because it excludes the other appendices
and bibliography. No full manuscript build, experiment, historical
mathematical script, CAS, project-wide check, or CI inspection was run.
