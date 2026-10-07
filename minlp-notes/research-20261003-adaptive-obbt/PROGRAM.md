# Adaptive bound tightening and allocation of solver effort

The user requested completion of the recommended follow-up to the existing
iterated OBBT study, including promising extensions. This continuation develops
screening before the first round, selective tightening during branch and bound,
certificates for remaining benefit, constrained-case theory, and the justified
scope of selecting between different strengthening actions.

## Deliverables

1. Precise mathematical contracts and proofs for screening, stopping and reuse,
   with explicit assumptions and counterexamples to unjustified stronger claims.
2. A working reference implementation and integration into a nonlinear solver,
   preserving local validity and recording decisions and all computational costs.
3. A prospective comparison against native solver behavior and relevant
   ablations, with a frozen policy, original-model validation, full outcomes and
   reproducible inputs. Synthetic checks and public-instance evidence are
   reported separately. Unrelated running experiments remain untouched.
4. A primary-source comparison that distinguishes classical ingredients,
   repository antecedents and proposed contributions. Publication priority is
   not inferred from a failed search.
5. Independent mathematical and implementation reviews, corrected findings,
   targeted verification, and an integrated report with a claim and coverage map.

## Completion standard

Each recommended workstream must have a developed result, a tested method, or a
specific justified limitation. Failed performance hypotheses are retained.
The report must distinguish completion of this research program from resolution
of every general open problem. It cannot label a conjecture proved, an untested
policy effective, or a numerical solve independently certified.

The first experiment targets OBBT. Broader scheduling is developed only as far
as supported by the component evidence; universal runtime guarantees require
their own assumptions. Only checks targeted to this continuation are run.

## Existing material

- `../research-20260922/iterated-obbt/`: contraction theory and external-presolve
  experiment, whose original outcomes remain unchanged.
- `../research-20261003-convexification/`: certified support cuts and budgeted
  native SCIP integration, including its negative comparative result.
- `../paper-decomposition-aware/`: structural bounds and certified reductions.

Existing dirty paths were recorded in `baseline-status.txt` before authoring.
