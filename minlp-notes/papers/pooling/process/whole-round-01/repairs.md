# Whole-paper round 1: separate repair record

Implemented accepted finding M1 only, after independently reading `adjudication.md`, `review13.md`, `results/rank-one-zero-lower-hardness.md`, and the earlier biclique reduction in `results/rank-one-row-column-hardness.md`.

Section 6.7 now states strong threshold hardness for the general-cost rank-one margin block with every row and column lower bound zero, every upper bound one, integer matrix costs, and a specified negative threshold. The surrounding distinction from additive physical source/product economics is unchanged. The bibliography cites the actual unpublished repository note under `s6:zero-lower-note`, without an author or public publication claim. The source index records its exact title, path, and SHA256; its opening description now covers sources used for the manuscript. The coverage row records the restriction, citation, existing exact checker, and retained root checker output.

The proof check covered both mass cases in the saturated-margin repair. At total mass at least one, each distinguished margin can be raised to one at fixed total, giving entrywise distance at most twice the sum of deficits. Below one, the distinguished unit matrix satisfies the same bound. A penalty larger than twice the largest absolute cost forces both distinguished margins to one. Taking the integer penalty `L = 2B + 1` shifts the optimum by `-2L`; the earlier biclique construction therefore gives the negative threshold and polynomially bounded integer costs. Its nonadditive cost scope is essential.

Validation passed:

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` built a temporary source-only copy successfully: 91 pages, no undefined references or citations, no overfull boxes, and eight underfull diagnostics. The revised statement and new bibliography entry appear in extracted PDF text. The repository's existing PDF and build artifacts were preserved for root's final build.
- All 49 bibliography keys are cited; no citation key or cross-reference label is missing or duplicated. All 13 adjacent source hashes match, including `26431afa15e32381c4aa342a0e8765ffaa5bb6cab1cb39ccbe6a2e013f7d70d0` for the new note.
- All ten frozen manuscript files still match their round-1 manifest. All 269 protected pooling files and consulted source notes match the pre-repair hashes retained in `repair-protected-hashes.json`. Only the four authorized existing source files changed. Their exact before/after diff is retained in `repair.diff`.
- Root had already run `code/rank_one_zero_lower/verify_penalty.py`: 2,000 exact rational cases passed, as recorded in `papers/pooling/verification/logs/whole-round01-zero-lower-penalty.txt`. This repair did not repeat that finite check or use it as a substitute for the proof.

The build output is in `repair-build.txt`; hashes and check results are in `repair-validation.json`. An initial PDF text check expected a hyphen that `pdftotext` omits at a bibliography line break; checking the title prefix and exact source filename resolved that check without changing the manuscript.

This repair does not certify every manuscript theorem, establish literature priority, or provide final whole-paper PDF visual inspection. Root's independent checks and the required fresh round of fifteen whole-paper reviewers remain pending. No other accepted or unaccepted finding was implemented, and no original source note, literature file, snapshot, or existing review report was edited.
