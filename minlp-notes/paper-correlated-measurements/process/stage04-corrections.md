# Stage 4 corrections

Correction author: `/root/stage04_corrections`.

Read the coordinator's first-round assessment and reviewer reports 1, 2,
and 5. Both accepted minor findings are addressed. No new mathematical
claim or change to a real-valued theorem was needed.

## Changes

1. In `sections/04-certification.tex`, the continuous relaxation is now
   explicitly compact and convex, with
   `conv{1_S : S in F} ⊆ Z ⊆ [0,1]^n`. The text still distinguishes a query
   in the cube from a point feasible for `Z`; only the latter supplies a
   continuous lower bound.
2. The local certificate's arithmetic discussion now chooses a rational
   symmetric reference `N` or its rational inverse and checks positive
   definiteness exactly. The prescribed weighted-trace objective matrix is
   explicitly rational and checked PSD for that checker. An analytic
   locality bound is replaced in every rational score by a certified
   rational upper enclosure `delta_hat`, with `delta ≤ delta_hat < 1`.
   The text explains why PSD increments preserve validity under this
   enlargement, describes rational envelopes and outward evaluation with
   square-root endpoints checked by squaring, and requires refinement,
   increased memory with recomputation, or rejection if the enclosure does
   not fall below one.
3. The robust-support discussion applies the same convention explicitly
   to each scenario reference and error enclosure. Numerical weight
   proposals are rounded to rationals, clipped and normalized exactly;
   zero remaining mass requires a specified rational simplex point or
   rejection. The weights remain exactly nonnegative and sum to one.
4. The opening of `appendices/certification.tex` collects the rational
   witness conventions for reference matrices, nuisance coefficients,
   split and query witnesses, and scenario weights. It explicitly includes
   the rational locality inflation in the integer-score weight when
   applicable and states that these representation choices restrict the
   checker rather than the real-valued theorems.

## Validation

- Inspected each changed passage against the two accepted findings and the
  unchanged support proofs. In particular, replacing `delta` by a larger
  value below one enlarges each PSD information contribution and its
  nonnegative trace score; nonnegative scenario weights preserve the bound.
- Forced a clean LaTeX rebuild using
  `latexmk -gg -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`.
  It completed successfully and produced `build/main.pdf`, 51 pages.
- The final `build/main.log` has no warnings, undefined references, overfull
  boxes, or underfull boxes. Both edited source files have no trailing
  whitespace. Build output is retained in
  `build/stage04-corrections-build.txt`.

Only the two Stage 4 manuscript source files, this report, and the local build
outputs were changed. Historical results, original tracked files, literature
packages, and the unrelated paper folder were not modified. No outstanding
accepted finding remains.
