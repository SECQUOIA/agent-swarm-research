# Late mathematical repairs, Opus R1

Source: `evidence/reviews/opus-math-r1.md`, findings NEW-1 to NEW-6.
Edited files: `sections/02-model.tex`, `sections/04-quadratic.tex`,
`appendices/F-integer.tex`. No other TeX file was edited. The five
companion-attribution sections were not touched, and the stale front-R2
rewrite in `evidence/concurrent-front-r2-preserved/` was not used.
Starting hash of 02-model was b2ee85b7…c8ca, as the root specified.

No theorem, lemma, corollary, or definition statement changed. No equation,
label, bibliography entry, or output, evaluation, law, or precision contract
changed. `evidence/reviews/late-opus-math-disposition-sol-r1.md` did not exist
when this work finished, so it was not read.

## Responses

### NEW-1: proof gap in `lem:int:affine-margin` (fixed)

Location: `appendices/F-integer.tex`, the proof directly after the lemma
(about lines 944–957). The statement (lines 937–942) is unchanged.

New proof:

- If `Z_p` is nonempty, then `π ≠ 0`, because a constant nonzero `p` has no
  zeros. `π_min ≥ 2^{-H_0}` is defined only in this branch. It is the least
  nonzero `|π_i|`: its numerator is at least 1 and its denominator is at
  most `2^{H_0}`.
- If `p(x) = 0`, the bound holds trivially.
- If `p(x) > 0`, set `v_i = 0` when `π_i > 0`, `v_i = 1` when `π_i < 0`, and
  `v_i = x_i` when `π_i = 0`. This point minimizes `p` on the cube. Because
  `Z_p ≠ ∅`, `p(v) ≤ 0`. The proof calls `v` a point of the cube, not a
  vertex, because coordinates with `π_i = 0` keep their possibly
  nonintegral values.
- Move from `x` to `v` one nonzero-slope coordinate at a time. The path
  stays in the cube. On each leg, `p` decreases at the exact rate
  `|π_i| ≥ π_min` per unit length. Since `p` is continuous and ends at a
  value `≤ 0`, it reaches zero at some point `y ∈ Z_p`. The `ℓ_1` length up
  to `y` is at most `p(x)/π_min`. Then `dist(x, Z_p) ≤ ‖x − y‖_2 ≤
  ‖x − y‖_1 ≤ p(x)/π_min ≤ 2^{H_0} p(x)`.
- If `p(x) < 0`, apply the same argument to `−p`. It has the same
  coefficient bit lengths and the same zero set.
- The empty-zero-set branch is unchanged. It also covers a nonzero constant
  `p`.

Checked against the reviewer's counterexample `p = x_1 − 2x_2 + 1/2` at
`x = 0`. The construction gives `v = (0, 1)`. Only `x_2` moves, and the path
reaches zero at `x_2 = 1/4`, which is within the bound `p(x)/π_min = 1/2`.
The constants are unchanged, so `cor:int:bilinear` and the bilinear part of
`thm:int:tu` keep `2^{-(k+1)H_0}δ/2` and `log_2 M ≤ poly_d(I)`.

### NEW-2: aligned model narrower than the lattice law (fixed by an extension paragraph)

Location: `sections/02-model.tex`, new paragraph "Row-scaled aligned noise"
directly after `def:model:perturbation` (line 125). The definition itself is
unchanged.

The paragraph does the following:

- It identifies the law of `thm:int:lowrank`: the `ξ_i` are independent,
  `ξ_i ~ U_{σ_i,M}`, each row has a specified rational scale `σ_i > 0`, and
  all rows share one resolution `M` chosen from the base instance.
- It notes that equal scales give model (iii) with `D = U_{σ,M}`.
- It explains why rescaling the rows of `T` does not remove unequal scales:
  `T` also enters the objective.
- It states that the common `M` is essential, because it fixes the spacing
  of the attainable-value lattice. In the proof, that spacing is
  `1/(D_0(M−1))`.
- It states that each theorem asserts its bounds only for the law it states,
  and that no result covers independent rows with unrelated laws.

The base-chosen-law paragraph was left unchanged. `M` is computed from the
base data, and the `σ_i` are specified, which matches that paragraph's
description. The row-specific regret bound `Σ σ_i ω_X(T_i·)` in
`sec:model:original` already existed.

### NEW-3: lattice search attribution (already fixed, not edited)

`sections/08-integer.tex:710–711` already reads "The corrected-corner search
of `\cref{thm:count:cells}` on the k auxiliary coordinates". The finding's
request to cite `cor:count:levels` as well was not acted on, because section
08 was not authorized for editing. The root should judge whether that
citation is still wanted.

### NEW-4: closure-template bit length (already fixed, checked read-only)

`sections/03-counting.tex:614–616` reads "All have polynomial bit length in
I, except in the results with parameter-dependent sampling precision." This
resolves the finding. No edit was made.

### NEW-5: fixed-parameter list in `sec:model:parameters` (fixed)

Location: `sections/02-model.tex`, around lines 410–418.

The fixed-parameter form is now claimed only for:

- the low-negative-inertia results under aligned or Gaussian-like noise;
- the core results;
- the integer-dimension results.

The claim is joint in the structural parameters and the numerical ratios
(`ν diam(X)/σ`, `L/σ`), which are included in `κ`. A new sentence states
that `thm:qp:uniform` is not of this form: its bound contains a power of `n`
that grows with `k`. That result is polynomial for fixed structure when the
ratios are polynomially bounded, but it is not fixed-parameter in the
structure.

The following text is unchanged:

- the fixed-width versus width-only FPT distinction for the sparse results;
- the `thm:lim:width` limitation;
- the qualification on numerical magnitudes;
- the FPT meaning;
- the `R = poly(I) ⇒ I^{O(k)}` sentence.

The new wording agrees with the introduction (01:285–293) and with the
remarks at 04:590, 04:611–613, and 04:629.

### NEW-6: regret remark used the auxiliary widths (fixed)

Location: `sections/04-quadratic.tex`, `rem:qp:regret` (about lines
636–644).

The ambient bound is now `σ̄ W_noise`, where
`W_noise = Σ_{j=1}^n (max_X x_j − min_X x_j)` is the original-domain width
of `sec:model:original`. The remark now says explicitly that this is not a
sum of the auxiliary widths `w_i`. On a mixed polytope, the widths of the
continuous relaxation give an upper bound.

Validity: `max_{x,y∈X} γᵀ(x−y) ≤ Σ_j |γ_j| (max_X x_j − min_X x_j)`.

The following are unchanged:

- the Gaussian support factor `b + 20`;
- the aligned bound `σ̄ Σ_i (u_i − ℓ_i)`, where `u_i − ℓ_i = ω_X(T_i·)`;
- the interpretation that these results do not recover the unperturbed
  optimizer.

## Checks run

These were targeted source checks only. No build, experiment, CI, or
project-wide verification was run.

- Python exact-match replacement, asserting that each old fragment occurred
  exactly once.
- `grep` confirmed that `thm:qp:uniform`, `thm:int:lowrank`, and
  `sec:model:original` are each defined exactly once.
- The lemma statement was reread after the edit to confirm it is unchanged.
- The new text was read back for brace balance and wording.
- The LaTeX was not compiled. The root's final build should confirm that the
  new `\cref` targets resolve, including the forward references from
  section 02.

## Remaining concerns

- NEW-3: adding `cor:count:levels` to the 08:711 citation is optional and
  would require editing section 08.
- `sec:int:lowrank` (08:656) still says the theorem "uses aligned noise
  (`def:model:perturbation`)". With the new paragraph in section 02 this is
  acceptable. A pointer to the extension paragraph would need an
  unauthorized edit to section 08.

## Final hashes

```
29fffb0feeedd481d0144ba94259dd8490bb91b7d2b2cdb2d93b70e73776bf49  sections/02-model.tex
3e94534ea4c3eceb2022e5ec36a6e80290bb4c208ae1a9e48f658a72904df824  sections/04-quadratic.tex
8c2208bc4603195f3e2e1d021ce0486ab4b6c1d2696119d4935189ef7456077a  appendices/F-integer.tex
```

## Follow-up: final NEW-2 integration

Authorized files: `sections/02-model.tex`, the opening sentence of
`sec:int:lowrank` in `sections/08-integer.tex`, and this report. Sol
independently confirmed all six dispositions and the current patches.

This follow-up supersedes one point of the earlier report. That report said
no statement changed. One proposition statement has now been clarified:
`prop:model:uniform`(a). The change is a clarification of notation and
contract only. The resolution bound `M(I)=2^{P(I)}`, the level-cap reset,
and every other definition, theorem, formula, and proof are unchanged.

Changes:

1. `sections/02-model.tex`, paragraph "Row-scaled aligned noise": I removed
   the final clause "no result covers independent rows with unrelated laws".
   It was too broad, because `thm:count:local` allows arbitrary independent
   concentrations and `cor:count:levels` allows differing marginals. The
   paragraph now ends with "Every theorem asserts its bounds only for the law
   it states."
2. `prop:model:uniform`(a) now reads as follows. A grid law is replaced by
   `U_{σ,M(I)}` with `M(I)=2^{P(I)}`. In the lattice theorem, the law of
   row `i` is replaced by `U_{σ_i,M(I)}`, keeping each specified scale `σ_i`
   and one common `M(I)` for all rows, and the level cap is reset to
   `log_2 M(I)`.
3. The scalar-law paragraph after the proposition now says that the law is
   rescaled "by the supplied σ, or by the specified row scales σ_i in the
   lattice theorem".
4. `sections/08-integer.tex`, opening sentence of `sec:int:lowrank`: "uses
   aligned noise (`\cref{def:model:perturbation}`)" became "uses the
   row-scaled aligned extension described after
   `\cref{def:model:perturbation}`".

The optional `cor:count:levels` citation in section 08 was left out, as you
instructed.

Checks: Python exact-match replacements, asserting that each old fragment
occurred exactly once, and a read-back of the edited sentence in section 08.
No build, experiment, CI run, or watcher was used.

Current hashes:

```
867c8675779f8657087a77b1d91c37bcb2ad0abc016be83d2feb91aa27d98970  sections/02-model.tex
3e94534ea4c3eceb2022e5ec36a6e80290bb4c208ae1a9e48f658a72904df824  sections/04-quadratic.tex
8c2208bc4603195f3e2e1d021ce0486ab4b6c1d2696119d4935189ef7456077a  appendices/F-integer.tex
bf6c8d6bc3027b6f49558e47e6f5a320c88561bff3bc4c4c08a263da061c76ab  sections/08-integer.tex
```
