# Stage 5 independent review 5

I reviewed the frozen Stage 5 author report, computational section and appendix,
the supplement README and manifests, all five new executable entry points,
the source-kinetics README, and the numerical wrapper's mappings against the
actual archived parser declarations. I found no major scientific issue. Three
localized minor issues should be corrected before accepting the stage.

## Minor findings

1. **The advertised spacing reproduction command fails before running the
   study.** `supplement/reproduce.py:22` invokes
   `noisy_markov_spacing_design.py` without a positional command. The archived
   parser requires `validate` or `first-case` (lines 383–393); the intended
   experiment is `first-case`. In an independent temporary supplement copy,
   `python reproduce.py spacing` exits with status 2 and reports the missing
   `command`. Add `first-case` to this mapping and execute the corrected wrapper
   once in a separate copy. The frozen spacing certificates are unaffected, so
   this is a local reproduction defect rather than a scientific invalidity.

2. **The validation command does not check the new-source manifest.**
   `supplement/validate.py:9–12` reads only `archive-manifest.json`.
   `source-manifest.json` contains eleven hashes for the new checkers, dependency
   specifications and `results/fresh-all.json`, but no entry point verifies it.
   The supplement README says the command verifies frozen input/source hashes;
   this presently covers the archive and source-kinetics subtree, not the new
   executables or fresh input artifact. I independently checked all 159 archive
   entries and all eleven source entries: they currently match. Extend the
   preflight hash verification to both manifests, and update the source manifest
   after the correction. Include a small negative check that changing a listed
   new source or the fresh artifact fails the preflight. This is a gap in the
   advertised reproducibility contract, not evidence of corrupted present data.

3. **The independent fresh-mixture checker should verify that the stored nuisance
   matrix minimizes the quadratic before treating its value as a mixture lower
   bound.** In `supplement/validate_models.py:62–66`, the checker forms
   `N = E.T*M*E`, verifies `W*N = I`, and uses `logdet(N)` as the feasible-mixture
   lower endpoint. For arbitrary `G`, this quadratic is an upper bound on the
   Schur information; the equality needed for a feasible-mixture lower bound
   requires `C*G + B.T = 0` for the nuisance blocks of `M`. The numerical
   producer correctly constructs that minimizer. I independently recomputed
   all four stored mixtures in exact arithmetic and verified both this
   stationarity identity and equality to the saved Schur information; the
   reported intervals are correct. Add these identities to the portable
   independent checker, rather than relying on the producer's construction.
   The empty-anchor case reduces directly to the information matrix. This is
   a localized verification omission, not an error in the present results.

## Independent checks and observations

The review scripts and logs are in `verification/stage05-review5/`.

- Copied the supplement outside the repository into a fresh temporary directory.
  Used the coordinator's isolated base-dependency interpreter, independently
  confirming that Gurobi, CVXPY and Clarabel were absent.
- Verified all 159 archived hashes and all eleven new-source hashes directly.
- Executed `reproduce.py partial` successfully in that copy. Its changed output
  and log were exported under `results/reproduced/partial/`.
- Executed the fresh exact block experiment successfully with a new output file.
- Executed the independent source checker in its documented `--winners` mode:
  all 2,347 schedule descriptors and all 33 criterion/budget comparisons were
  checked; 51 distinct winners/runners-up supplied 306 direct exact objective
  equalities. I did not portray this shortened run as the complete 14,082-value
  source validation.
- Confirmed that all frozen archive/source-kinetics hashes remained unchanged
  after these runs. Repeating a reproduction into an existing destination was
  refused, as documented. Altering a frozen archive file in the temporary copy
  made `validate.py` reject it before scientific validation began.
- Extracted and evaluated every archived parser's actual `add_argument`
  declaration, then parsed all sixteen wrapper command mappings. Fifteen passed;
  only spacing failed. All explicit source/input/memory files referenced by the
  passing commands exist within the supplement. This static parser exercise
  does not claim that all expensive numerical optimization branches were run.
- Independently reconstructed the four fresh augmented mixtures and checked the
  exact nuisance minimizers, stored information matrices, and inverse weight
  matrices. All passed, closing the mathematical concern behind finding 3 for
  the current artifact.

The paper makes appropriate distinctions between exact rational input-instance
certificates, numerical model diagnostics, optimizer proposals, and historical
single-run timings. It retains failures and unfavorable comparisons. The
standalone paths used by the reviewed validation and wrapper entries are local;
original repository paths in historical records are provenance, not execution
inputs. Optional commercial/conic packages are separated from the main suite.
The wrapper's isolated writable copies preserve the original research files.

## Limits and recommendation

I did not repeat the entire expensive 46-certificate replay, which the coordinator
had already run independently outside the repository, nor run the optional
licensed/conic producers or every numerical branch. I did not perform a new
literature search because Stage 5 introduces no additional broad novelty claim;
the accepted theory/prior-work review and final manuscript review remain separate
gates. The later introduction and final package are explicitly pending and were
not counted as Stage 5 omissions.

Accept Stage 5 after the three minor corrections and focused confirmation. I
found no reason to invalidate any of the reported scientific results or to
require a major-issue review cycle on the basis of this review alone.
