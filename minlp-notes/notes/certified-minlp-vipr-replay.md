# Exact VIPR replay for certified MINLP

Date: 2026-09-13.

The certificate checker now checks MILP proof arithmetic in `code/minlp_solver_lab/certify/vipr.py`. An upstream `viprchk` success message is insufficient for acceptance. The caller must also establish that the VIPR problem is the reconstructed rational master. A VIPR solution is a feasible point of that master; it is not automatically feasible for the nonlinear problem.

## Supported certificate contract

`validate_vipr(path)` accepts a deliberately restricted complete VIPR syntax:

- Versions 1.0 and 1.1, with the required section order and exact declared counts.
- ASCII integer and fraction coefficients, with positive denominators. Decimal and exponent tokens are rejected; the pinned upstream reader does not reliably implement the specification's decimal syntax.
- Distinct variable names, integer indices, coefficient indices, and linear-combination reference indices. Every index must be in range; every inference reference must precede the current row, including references with a zero multiplier.
- Complete `asm`, `lin`, `rnd`, `uns`, and `sol` reasons. Weak and incomplete reasons are rejected.
- One complete derivation per non-comment line, optionally followed by exactly one `global` token after the lifetime annotation. This SCIP metadata is accepted only when the independently computed assumption set is empty; it never discards assumptions. All declared derivations and the end of the file are checked, even if an earlier row already proves the requested bound. Repeated metadata tokens and other trailing material are rejected.
- Nonnegative lifetime annotations within the proof or `-1`. A reference after an annotated last use is rejected. Row labels and the bound-count field are metadata; inference identity comes exclusively from row indices. The bound count must not exceed the constraint count, but the checker does not use it to reinterpret rows.

`parse_problem(path)` uses the same problem parser and exposes exact standard-library `Fraction` values for master comparison. Master-variable renaming must be a bijection checked by the caller.

At least one derived row must have no remaining assumptions and dominate the requested finite dual bound, or be a contradiction for an infeasibility claim. Its index is reported as `proving_derivation`. All later derivations must also pass their own inference checks, and all declared rows and EOF must be consumed; a successful prefix never bypasses suffix validation. This permits common SCIP output that proves the exact target before appending a valid but weaker approximate bound. A finite primal bound requires a checked feasible solution. Infeasibility claims require an empty solution section.

The checker rejects the upstream integer-objective cutoff extension `best - 1`. Its accepted `sol` rule requires an actual checked feasible solution and allows only a row implied by the ordinary incumbent cutoff: `objective <= best` for minimization, or `objective >= best` for maximization. This conservative restriction can reject a solver-produced proof; such rejection does not establish that its claimed bound is false.

## Why the accepted rules establish a bound

Consider minimization. Let `b` be the best exact objective value among the checked solution witnesses, if any exist. Define `S` to contain every feasible master point with objective at most `b`; if there is no witness, let `S` be the entire feasible set.

The induction invariant for every derived row is: every point of `S` satisfying that row's recorded assumptions satisfies the row.

An assumption introduces itself. A suitable exact linear combination preserves the invariant, with the union of the assumptions of its nonzero terms. Rounding is allowed only when every nonzero coefficient is an integer and its variable is integer, with the correct floor or ceiling of the right-hand side. An unsplit inference checks both branch implications and a pair of exhaustive integer disjunctions, then removes the respective branch assumptions. The solution rule holds by the definition of `S`.

Consequently, an assumption-free derived row proving `objective >= L` bounds every point of `S`. When a witness exists, that witness belongs to `S`, so `b >= L`. Every feasible point outside `S` has objective greater than `b`, hence also satisfies the bound. When no witness exists, `S` already contains every feasible point. This establishes the lower bound without assuming that the infimum is attained. The maximization argument reverses the inequalities. For infeasibility, an empty solution section makes `S` the entire feasible set, and an assumption-free derived contradiction proves that this set is empty.

This is an implementation-level argument for the stated subset, not a mechanized proof of the Python parser or kernel. The trust boundary includes Python execution, python-flint/GMP exact arithmetic, file integrity during checking, and the separate master-equivalence and nonlinear-cut checks.

The interpretation follows the ordinary solution rule and assumption semantics formalized by Wood et al.; the executable implementation here and its restricted input syntax are separate work. Their discussion also identifies earlier upstream-checker weaknesses involving solution inferences and lifetime annotations. [Wood et al., *Satisfiability Modulo Theories for Verifying MILP Certificates*, version 4, Sections 3 and 4](https://arxiv.org/html/2312.10420v4)

## Source audit and regressions

The inspected upstream checkout was `/workspace/local-home/build-scip/vipr`, revision `30f2951d1e90e47afa821bdd1b12b82246656c42`. Its `code/viprchk.cpp` SHA-256 was `2baf9c4593f5b8ef42323fbfb7cbfa0e4dfafff65e636cf6a143561b9dca2738`.

The source audit found that its solution rule uses an initially zero best objective even with no solution witness, and its rounding function fails to reject a nonzero continuous-variable coefficient. Other unchecked or incompletely checked parser and reference cases make a success-message wrapper unsuitable as the sole acceptance boundary. These observations concern the inspected checkout, not every release or implementation of VIPR.

The dedicated regression suite includes the previously reproduced million-unit false lower bound for `min x` subject to `x >= 1`, rounding a continuous variable, nonintegral rounding coefficients, invalid solution witnesses, unsupported integer cutoffs, nonexhaustive split disjunctions, incorrect combination signs, duplicate entries, invalid references and lifetimes, unfinished proofs, forged `global` markers on assumption-dependent rows, and trailing material after a valid proof prefix. External-verdict checks require a zero exit code and one complete exact range message matching the independently checked relation.

## Streaming and observed performance

A first pass computes actual last uses in compact integer arrays and checks lifetime annotations. A second pass performs exact arithmetic and releases sparse rows after their actual last uses. This also handles files that set every annotation to `-1`. The first pass uses two arrays with 8 bytes per row each; replay retains one array plus the currently live sparse rows and the longest input line. A pathological proof with many simultaneously live dense rows can still need substantial memory.

A pilot on the existing `syn40m02m/master_complete.vipr` proof checked 125,593 derivations in 54.25 seconds, with 18,264 peak live rows. The file occupies about 427 MiB. The result was accepted, including 1,664 ordinary solution-cutoff inferences. This is a single local timing, not a benchmark aggregate or a claim about nonlinear model validity.

Run the focused tests with:

```sh
cd code/minlp_solver_lab
uv run --with pytest python -m pytest -q certify/tests/test_vipr.py certify/tests/test_vipr_independent_review.py -p no:cacheprovider
```
