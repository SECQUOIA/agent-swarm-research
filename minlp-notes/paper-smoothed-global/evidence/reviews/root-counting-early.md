# Root review of the first shared-tools section

Snapshot: first `sections/03-counting.tex`, read 2026-10-05 before Appendix A
and the complete draft. No experiment or literature research was performed.

1. **Computability wording.** A Turing machine can sample a countably infinite
   rational law if sampling time is unbounded. For example, return an integer
   geometrically distributed by fair bits. The paper deliberately uses
   bounded samplers and finite support, which should be stated without the
   false assertion that every Turing-samplable law has finitely many atoms.
2. **Universal scope.** The closure/fallback paragraph following the fixed-atom
   example must distinguish the lattice and strong-field theorems, which do
   not need a rare fallback. A fixed atom defeats this particular endlessly
   refined retention count, not every exact algorithm.
3. **Output contract.** The generic fallback currently returns separate
   coordinate/value root isolators, whereas the model defines algebraic
   output by one common root. A Sol development is in progress at
   `author-reports/fallback-shared-root-sol.md` to convert the canonical tuple
   to a shared-root representation within a larger base-only exponential
   factor. Incorporate that proof and state the stronger result, or reconcile
   the model precisely. Canonical selection proves consistency but is not
   itself a common-root representation.
4. **Degenerate domain.** Rare-fallback budget part (b) divides by S. State
   S>0, or handle a singleton domain directly before choosing thresholds.
5. **Notation and cross references.** The model names the grid law U while
   this section uses mathcal U. Use one name consistently. Recourse's
   corrected-corner references should cite `lem:count:rounding` or
   `thm:count:cells`, not just `thm:count:local`, which is the count theorem.
6. **Fallback encoding.** Explicitly distinguish base-only defining-polynomial
   degree bounds from coefficient heights that depend polynomially on I+b.
   A runtime bound B(I+b)^c alone does not imply degrees independent of b.
   The block-QE construction gives this stronger format bound and the
   shared-root conversion needs it. Similarly the raw fallback's output
   length is at most B(I+b)^c, not at most B when b is arbitrary.

The local interval, balanced-mesh ratio, and deterministic dominating-count
arguments are sound as stated. The rare-budget Gaussian constants fit the
3rho bound. The general reduced-value bad-growth event can indeed be expressed
using two point blocks: an existential optimum/comparison pair and a universal
global-competitor point, including residual variables in each point block.
