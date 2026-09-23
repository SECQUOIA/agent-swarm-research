# Stage 1 corrections after round 1

The correction agent addressed all four valid minor findings in
`stage01-round01-adjudication.md`. No theorem, proof, or scope beyond those
findings was changed.

1. **Integer domains (R02-01; reviewer 05).** The opening definitions in
   `sections/01-foundations.tex` now state that switch budgets are nonnegative
   integers, activation-block counts are positive integers, and grid sizes
   are positive integers. These declarations apply throughout the paper,
   including the compactness proposition.
2. **Overview mode scope (R02-02; R04-01).** The abstract explicitly restricts
   the full continuous one-switch minimax formula to at least three modes.
   The opening overview in `sections/02-uniform-one-switch.tex` and the
   README's stage overview carry the same restriction; the theorem already
   had the correct domain. The section overview was corrected after primary
   inspection caught this initially missed locator.
3. **Construction normalization (R04-02; reviewer 05).** The implementation
   paragraph after the one-switch proof explicitly restores arbitrary horizon:
   `E=H_n(T)` and `t_i=T-m_i-E`. It defines the largest and second-largest
   mass indices and supplies the large-mass schedule and switching time
   directly. The normalized proof is unchanged. The bundled one-switch
   checker passed 2,080 rational instances on horizons 1 through 20 and all
   13 extremal constructions.
4. **Frozen verification dependencies (R03-01).** The unchanged original
   `one_switch_certificate.py` and `uniform_certificate.py` are bundled in
   `verification/reference/`. `origin-manifest.json` records their original
   repository paths and SHA-256 digests. `stage01/check_boundaries.py` imports
   its dependency relative to the paper's verification directory. The README
   gives commands from the manuscript or snapshot root. These files are
   included by the existing snapshot helper, with no helper changes needed.

## Verification

Created a temporary relocated paper directory under
`verification/stage01-corrections/` containing only current manuscript sources,
the bibliography, the README, the bundled reference scripts and provenance,
and the boundary checker. Ran all three README verification commands and a
clean LaTeX/BibTeX build there. All exited successfully. Removed this temporary
directory after testing so it cannot enter a future snapshot recursively.
Built the live manuscript successfully as well. The clean relocated build
reported no warnings, undefined references, or overfull/underfull boxes.

The exact checks passed:

- Uniform certificates: 60 exhaustive schedule comparisons and 31,200
  continuous/discrete bound comparisons.
- One-switch certificates: 2,080 rational construction and half-grid checks,
  plus 13 extremal constructions.
- Boundary checker: 1,216 half-simplex profiles, 28 uniform three-cell
  sharpness cases, and 162 binary endpoint identities.

Logs are under `verification/stage01/` with the prefix `corrections-`:
`uniform.log`, `one-switch.log`, `boundaries.log`, `relocated-build.log`,
`build.log`, and `integrity.log`. Both bundled references match their original
bytes and recorded hashes. All 13 files in the original round 1 manifest
retain their recorded hashes; the frozen review stage was not edited.

All adjudicated findings are resolved. The primary agent can now inspect the
changes and freeze the accepted stage. No accepted-stage snapshot was created
by the correction agent.

After the final section-overview correction, rebuilt the live manuscript
successfully. That change only adds the mode restriction to prose; the
previous arithmetic checks remain applicable. The final build log is
`verification/stage01/corrections-final-build.log`. No snapshot was edited.
