# Verification of regular recourse multiplier rates

Date: 2026-09-28. This record covers
[active-region-rates.md](active-region-rates.md) and its
[prior-work audit](active-region-prior.md). The theorem is complete within
its stated assumptions. No general multivariate Lipschitz-multiplier or
ordinary-module claim is included.

## Exact targeted checks

Ran from the repository root:

```sh
python3 -B research-20260928/solver/check_active_region_rates.py
```

Result: pass. The checker verified:

- 32 explicit interval certificate identities for `1+-T_n`, including
  the odd-degree cases, and 10 tensor parity certificate identities;
- 319 adjacent kernel-multiplier inequalities, 72 exact commutator
  identities including modes beyond kernel support, and six exact
  displacement identities;
- 3,332 nonzero tensor commutator frequencies satisfying the rounded
  half-degree condition. Of these, 1,237 exceed the simpler total-degree
  bound `|alpha|<=r`, so they exercise the substantive degree correction;
- the sharp example's two KKT regions and a non-diagonal matrix KKT
  identity with exact coefficients.

These finite rational and symbolic checks target signs, constants, and
degree formulas. They do not prove the formulas for every order or
dimension, control infinite coefficient series, establish measurable
selection, or assess novelty. Those points use the written arguments and
separate review.

## Independent adversarial review

The [fresh review](active-region-fresh-review.md) rederived the KKT
inequality, checked every use of positivity against the truncated
hierarchy, examined kernel-support boundary terms, and reviewed the
Hölder-to-polynomial transfer and measurable selection. It found no
required mathematical correction. It also confirmed the scalar-network
limitation and the sharp example's actual-measure lower-bound transfer.

The independent reviewer ran:

```sh
python3 -B research-20260928/solver/check_active_region_sdp_review.py
```

That command passed 4,165 exact rational comparisons between independently
evaluated Dirac moment matrices and their assembled polynomial entries.
It also solved the sharp example's anisotropic SDPs at `r=2,3,4`, with
approximate objectives `-0.0369846834`, `-0.0106354741`, and `-0.0055493930`.
All three statuses were `optimal_inaccurate`. The largest PSD violation
was about `2.15e-9`, and the largest equality residual was about `5.49e-12`.
These numerical results challenge implementation and finite-order
behavior; they are not certified bounds or evidence of an asymptotic rate
on their own. The review records full numerical details.

## Source and scope checks

The [audit](active-region-prior.md) records primary sources, exact theorem
locators, searches, and one inaccessible older full PDF that is not used
as a formal hypothesis reference. During closure, the relevant
parametric-QP, joint+marginal, two-stage polynomial approximation, and
sparse multiplier-relaxation theorem passages were rechecked. The audit
now distinguishes the established sensitivity and approximation facts
from the proved fixed-private-degree hierarchy result. The search did
not establish publication priority.

A targeted Python scan checked trailing whitespace and local Markdown
link targets in the four active-region Markdown files and trailing
whitespace in the two associated checkers. It passed for six files and
21 local links. An initial overly broad link pattern also matched a
mathematical expression; restricting the scanner to file-link extensions
removed that false positive. Only this topic was
checked. No Lean formalization, project-wide test command, or CI status
or log inspection was run.
