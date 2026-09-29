# Structural repair investigation

Date: 2026-09-28. Outcome: a proved supporting transfer theorem and
sharp limitations, with independent proof review and targeted checks.
This branch did not establish a substantial original MINLP advance.

The [main note](repair-probe.md) proves that, on a tree of compact
local feasible sets, the best deterministic Hölder repair constant
equals the best Wasserstein repair constant for arbitrary local
probability laws. Hard local constraints and bounded integer variables
are included. It also gives exact transport identities, sharp failures
on cycles and for exponents above one, and a strongly contractive
quadratic path with sharp terminal-repair exponent `2^(-m)`.

The [penalty and message note](penalty-messages.md) derives an exact
Wasserstein-penalty formulation and identifies the same linear repair
constant with a sharp universal bound on Lipschitz dual separator
potentials. A small MILP illustrates that such potentials can exist even
when exact conditional feasible value functions are discontinuous.

The [source audit](source-audit.md) records the strong classical
antecedents and the limits of the novelty screen. The
[independent review](repair-proof-review.md) specifies its proof scope.
The structural investigator additionally reread the complete written
proofs. Neither review is a Lean or journal verification.

The targeted command was:

```text
python3 research-20260928/structural/check_repair_transfer.py
```

It passed exact enumeration of a sharp deterministic constant, 300
finite law-repair LP checks, 80 exact rational message-dual checks,
the penalty threshold check, and the cyclic boundary example. These
are finite checks with the limits stated in the source audit; no
project-wide verification or CI inspection was performed.

The theorem identifies the remaining task precisely: obtain a useful
deterministic repair bound and an efficient repair map for an important
nonlinear application class. Neither treewidth nor forward contraction
alone supplies that missing ingredient. Generic Lipschitz recourse and
guard-margin approaches were assessed as standard-derived, so this
branch is not being promoted as the main contribution.
