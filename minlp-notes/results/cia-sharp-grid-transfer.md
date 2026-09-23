# Sharp switch-preserving transfer to a uniform grid

Date: 2026-09-07. Status: proved with independent mathematical review and exact checks; primary-source comparison completed with qualified novelty claims.

Let `D(alpha,w)=max_i sup_t |integral_0^t(alpha_i-w_i)|`. Initial activation is free; a switch is a change between distinct consecutive modes.

**Theorem.** A finitely switching integer control on `[0,N Delta]`, with `Delta>0` and integer `N>=1`, can be replaced by a control constant on each uniform-grid cell with no more switches and cumulative deviation strictly less than `Delta`. The replacement's mode word is a chronological subsequence of the original word, after merging consecutive equal modes. Rational switch times and rational `Delta` permit a polynomial-bit construction in the explicit grid length and input size.

For the same relaxed input and switch budget this implies

```
OPT_cont <= OPT_grid < OPT_cont+Delta.
```

The coefficient one is optimal uniformly over mode counts and budgets, even for relaxed inputs constant on that grid and budgets `1<=s<=N-2`. With two modes the transfer bound improves to half the largest grid-cell length, including nonuniform grids.

With at most one switch, the same half-mesh estimate holds on **every grid
and for any number of modes**. For a fixed measurable relaxed input, let
`U_grid=OPT_grid(alpha,1)` and let `barDelta` be the largest cell length. Then

```
U_grid-barDelta/2 <= OPT_cont(alpha,1) <= U_grid.
```

Move the switch of an attained continuous optimum to the nearer endpoint
of its containing cell. Its displacement is at most `barDelta/2`, which
bounds the change in cumulative occupation. Both inequalities are
non-strict. This argument does not assert that the gap between the two
optima attains `barDelta/2`.

## Proof and sharp example

Average the original integer control on each uniform-grid cell. Standard integral prefix rounding can be restricted to assignments with positive cell occupation. It gives one supported mode per cell and floor/ceiling occupation counts at every prefix, hence error strictly below one cell width. Choosing an original occurrence of each selected mode inside its cell gives increasing occurrence times; deleting intervening original blocks cannot increase the switch count. Within a cell every component of the discrepancy is monotone, so endpoint bounds suffice. This explicitly uses established controlled/matching rounding; the temporal-support consequence supplies the switch guarantee.

For sharpness use unit cells, `n>=2` modes, `N=n+1`, and `s=n-1=N-2`. The relaxed input is uniform across all modes in the first cell and stays in mode `n` afterward. The grid optimum is exactly `1-1/n`: every first-cell selection forces that error at time one, and the constant mode-`n` schedule attains it. A continuous schedule visits modes `1,...,n` for `1/n` time each in the first cell and remains in mode `n` afterward. It uses `n-1` switches and has error `(n-1)/n^2`. Consequently

```
OPT_grid-OPT_cont >= (1-1/n)^2 -> 1.
```

Already `n=4,N=5,s=3` gives a gap at least `9/16>1/2`. This corrects the instance-wise half-grid justification immediately before Conjecture 1 in Sager and Zeile's final article, printed p.615. It is not a claim about the difference between suprema over two different adversarial input classes. The source passage is an argument leading to a conjecture, not a proved half-grid theorem.

For two modes on a cell of length `d`, let `a` be the original mode-one occupation and `e` the incoming mode-one discrepancy. The choices give `e-a` or `e+d-a`. If `0<a<d`, both choices are supported; when `|e|<=D/2` and `d<=D`, at least one new discrepancy stays in that interval. If `a=0` or `a=d`, the only supported choice leaves `e` unchanged. Induction and the same chronology prove the binary refinement. A single cell split equally between two original modes makes its half-cell constant sharp for schedule transfer.

## Evidence and scope

[Lean topic 17](../formal/topics/17-grid-switching/COVERAGE.md) verifies
supported prefix rounding, switch preservation, the transfer inequalities,
sharpness examples, and the arbitrary-grid one-switch certificate
(`coarsening_certificate_one_switch`). Its verification record retains the
completed proof checks. The formal proof of prefix rounding uses Hall's
marriage theorem; it does not verify a network-flow implementation or its
bit-cost bounds.

The [full derivation](../notes/cia-reopened-grid-transfer.md), [independent review](../notes/review-cia-reopened-grid-transfer.md), and [exact independent checker](../code/cia_reopened/check_grid_transfer_review.py) include boundary cases, arbitrary repeated modes, 8,819 exhaustive controls, and rational sharpness and binary nonuniform examples.

The [source comparison](../notes/cia-reopened-literature.md) credits Bestehorn and Kirches's support-preserving matching result and identifies the exact Sager–Zeile passage. Primary sources: [matching-rounding result](https://d-nb.info/122645075X/34), [Sager–Zeile final article](https://link.springer.com/article/10.1007/s10589-020-00244-5). No matching sharp switch-budget transfer statement was found in the checked sources; this does not establish exhaustive priority.

The construction rounds a supplied continuous schedule; it does not find its continuous optimum. It does not preserve arbitrary transition restrictions or minimum dwell times. The general multi-mode, arbitrary-budget transfer theorem requires a uniform grid; the binary and one-switch refinements above admit arbitrary grids. Taking suprema only immediately proves `F_grid<=F_cont+Delta` when the continuous adversary includes all measurable controls; the reverse comparison must not be inferred when the relaxed-input classes differ.
