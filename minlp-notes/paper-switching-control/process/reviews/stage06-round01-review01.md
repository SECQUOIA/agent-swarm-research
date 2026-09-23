# Independent review 01 — stage 6, round 1

**Verdict: no major findings. One minor clarification is needed.** The new mathematical consequences and the exact public computations checked in this review are correct. The accepted proofs retain their earlier text and scope.

## Finding

### MINOR — make the deterministic input formula unambiguous

Locator: `sections/12-computations.tex:163–166`, especially line 165; compare `verification/stage06/experiments.py:193` and the identical construction in `check_results.py`.

The text specifies weights as `1+((j+2)(i+3)+i^2\bmod 11)`. It does not group the entire sum before applying the remainder operator. A reader can therefore read this as adding `(j+2)(i+3)` to the remainder of `i^2`, whereas the code takes the remainder of the entire sum. For example, with `j=0, i=2`, the code gives `1+((10+4) mod 11)=4`; the other natural reading gives `1+10+(4 mod 11)=15`. For the first three-mode cell this changes the normalized input from `(7,9,4)/20` to `(7,9,15)/31`.

Suggested correction: write

```tex
1+\bigl(((j+2)(i+3)+i^2)\bmod 11\bigr)
```

or define the weight as one plus the least nonnegative residue of the explicitly parenthesized sum. No numerical result or algorithm needs changing.

## Scope and checks

I read the new abstract and main document, the complete introduction, computations and discussion, the new classical comparison in section 07, the moved higher-reach appendix, references, generated tables and figure code, stage 6 scripts and source record, the offline runner and README. I checked the permitted claim-coverage map and repository inventory against the earlier developments. I did not read other current reviews, author/root assessments, or root research outputs, and did not communicate with other reviewers.

A byte comparison with `process/snapshots/stage05-accepted` confirms that every earlier section other than section 07 is unchanged. The appendix is a verbatim move of section 07's former higher-reach material. The section 07 addition is the explicitly attributed classical bound. The changed stage 4 summary reflects the portable runner's default execution without optional numerical LP audits, not a changed theorem or checker.

All execution and generated artifacts were confined to `verification/reviewer01/stage06-round01/`; the manuscript and snapshot were not modified.

### Independent mathematical and computational evidence

The independent program `verification/reviewer01/stage06-round01/independent_audit.py` imports no manuscript algorithm or experiment helper. Its completed output is `independent-audit.log`.

- Downloaded the pinned public CSV into the review directory and verified its SHA-256. Parsed the decimals exactly. Reconstructed quantization by enumerating floor/ceiling allocations and minimizing total absolute rate deviation, with the stated index tie rule. All 12,000 rows, all three derived grids, and the exact normalization, pointwise quantization, and cumulative quantization summaries agree with the archive.
- Located all six continuous pair crossings independently by binary search of integer cumulative masses. Evaluated the complete signed cumulative discrepancy at every original input knot and at each candidate switch, for every pair. This reproduces all six archived pair optima, including `4721469/2500000` for mode two followed by mode three. Separately scanned all fine-grid pair/boundary choices using signed residuals at the switch and terminal time, obtaining `1889/1000` at time `1889/1000` with the same modes. The gap is exactly `1031/2500000` and is below half the fine width.
- Implemented a different exact grid algorithm whose state records cumulative cell-service counts, the last label and the actual number of switches. It extends all possible next cell labels, retaining the smallest historical maximum at each state. This uses all grid prefixes and does not partition nominal blocks or use the manuscript subset costs. It independently confirms **every public value for all four budgets on 12, 24 and 48 cells**, including the 48-cell values not independently enumerated in the archived experiment script.
- The same cumulative-count algorithm independently confirms every uniform three-mode convergence point. I also checked the analytic continuous `1/6` proof directly: fewer than three distinct served modes leave mass `1/3` unserved; otherwise the last start gives the displayed lower bound, and the proposed quarter/half schedule attains it.
- Checked every archived public lower endpoint, clipping/strictness flag, and nested-grid applicability. The perturbation enlargement applies to the normalized source, as stated. Exact optima are consistently attributed to the quantized source.
- Recomputed the headline regime transitions `n=5,8,12` rationally and checked consistency with the new classical upper bound. The source bound is `(2n−3)/(2n−2)` times the largest cell width. Cell averaging on `k` equal cells yields the stated hard-budget consequence for every `n≥2, k≥1`; its comparison with `T/(k+1)` is strict precisely when `k>2n−3`. The paper does not transfer the source's unrestricted-grid tightness to the hard-budget problem.
- Independently verified all archived timing medians from their three individual samples, and all controlled enumeration case counts. The timing scope, shared-host limitations, arithmetic complexity versus measured runtime distinction, and absence of an external-solver performance claim are clear.

### Portable verification and build

In the relocated snapshot, the complete offline command `python verification/run_all.py` finished successfully, including all proof, integrity, algorithm and archived-experiment suites and the generated-table check. The log is `offline-runner.log`.

A clean `latexmk -C` followed by `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` succeeded and produced 56 pages. The final TeX log contains no overfull/underfull boxes, undefined references, or warnings. The build log is `clean-build.log`. I visually inspected the newly rendered figures and computation tables on pages 2, 49 and 50 and checked the surrounding extracted text. The plots match the stated normalization and domain, distinguish the one-sided geometric term from the full minimax, and limit connecting lines to the displayed cases.

### Literature checks

I independently checked the new classical consequence against [Zeile–Robuschi–Sager, Corollary 1](https://link.springer.com/article/10.1007/s10107-020-01533-x), whose publisher text states the bound and makes `N≥n−1` a condition of tightness rather than of the upper bound. The introduction respects that distinction.

The publisher's indexed preview of [Abbasi-Esfeden et al.](https://www.sciencedirect.com/science/article/abs/pii/S0959152425001507) explicitly confirms the absence of a general global-optimality guarantee, consistent with the paper's characterization. Direct page access returned 403; I did not obtain or claim to inspect the complete final article. Publisher metadata supports the bibliographic entry. The earlier CIA switch-constrained decomposition attribution is consistent with the primary publisher abstract of Sager–Jung–Kirches.

I read the relevant local primary text for Knuth's network rounding, Kirches–Manns–Ulbrich's convergence setting, the tight SUR paper, the nonuniform-grid preprint, and Zeile–Weber–Sager's state-error theorem/corollary. The manuscript's limited descriptions are supported. The new introduction does not claim that fixed-budget refinement converges to the relaxed input or supplies a dynamics-independent state/objective guarantee.

## Limitations

This is the final-authoring/integration stage review, not the separately planned fresh proof audit of the entire manuscript. The unchanged accepted proofs were consulted as dependencies rather than all rederived again. The independent computational checks are finite evidence for the displayed examples; the portable universal certificates and analytic proofs remain their separately stated proof foundations. I did not independently reproduce historical timing measurements or conduct an exhaustive literature-priority search. The supported preview-level scope of the 2025 DP paper is as described above.
