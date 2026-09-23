# Stage 5 independent review 2

Reviewed the Stage 5 author report, delivery README, both paper-owned scripts, Appendix A (`sections/08-reproducibility.tex`), the actual paper-source archive and its inventory, current core index/documentation, and formal coverage/source fingerprints. This reviewer performed the designated fresh paper-source extraction/build checks. No peer review reports were read and no shared source, archive, evidence, or proof files were changed.

**Verdict: clean. No major or minor correction is required in the reviewed Stage 5 scope.** The source archive builds independently, packaging is deterministic for unchanged inputs, reproduction instructions match the current artifacts, and formal coverage remains accurately limited.

## Independent source extraction and build

I extracted `certified-minlp-paper-source.tar.gz` to `/tmp/cert-minlp-stage05-review2-972uiua1/certified-minlp-paper` using the tar data extraction filter. Its **476,878-byte** size and SHA-256 **`11e566f2d7aa8e4ca589928635034bc3914625afa5c3d4f76ca81a5f0e4f08d8`** match the external index. The archive contains **49** entries.

Both documented hash checks passed in the extracted tree:

```text
sha256sum -c PAPER-SHA256SUMS
cd formal && sha256sum -c verification/SHA256SUMS
```

The documented plain build command then passed from the fresh extracted paper directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The resulting **32-page** PDF has extracted text identical to the delivered root PDF; its bibliography bytes also match exactly. The final log has no warning, undefined citation/reference, overfull box, or underfull box. The independent extraction/build/hash logs remain beside the temporary paper directory.

I also tested the clean-build script's specific stale-auxiliary contract. In the temporary extracted copy, I replaced `main.aux` with an invalid TeX command and `main.bbl` with an obvious stale sentinel, then ran `bash scripts/build-paper.sh`. It succeeded, replaced the stale bibliography with the correct bibliography, and produced a clean log and 32-page paper. Inspection confirms it copies current main/bibliography/sections/tables to a fresh temporary directory before compilation and copies output artifacts back only after a successful build.

## Packaging and inventory

I ran the extracted `scripts/package-source.py` twice after compilation. Both runs reproduced the delivered archive **byte-for-byte**, including the recorded compressed size/hash. The newly generated LaTeX auxiliaries and PDF were excluded. This directly tests the stated deterministic packaging behavior without modifying the shared delivery.

The archive's inventory contains all eight mandatory section inputs, all referenced generated TeX tables, `main.tex`, `references.bib`, README/reproduction scripts, current evidence maps, and the complete focused formal source/pin/audit/coverage files and saved verification records. The architecture diagram is native TikZ inside Section 4, so there is no missing external figure file. Mandatory inputs ensure an absent required section cannot silently disappear from a successful build.

No `.lake` cache, installed dependency tree, literature PDF, vendor executable, experimental proof archive, compiled paper PDF, stale bibliography, or duplicate build directory is present. The two formal verification logs are intentional provenance records rather than accidentally included build trees. The core/bulk archives are correctly separate; their metadata and outer README are included with paper sources.

## Current experimental artifact references

I independently checked the updated core's size and digest against `supplement/archives.json`: **6,478,558 bytes**, SHA-256 **`80ef5d50faefc97e01832f06b1f730a3a906b7d5b2ca9d8609453df9561f1fc6`**. The actual bulk file size matches **30,664,561,063 bytes**. I did not reread its 30.7 GB compressed contents; the index explicitly identifies retention of the previously validated bulk digest.

The README embedded in the current core now directs historical-version restoration through the separately hashed shared fixture/example data. This agrees with Appendix A's description and addresses the previous directory-replacement defect; no obsolete core hash is used by the reviewed Stage 5 files. The current default and restored-version counts are stated separately. A full V3 primary replay count remains explicitly an expectation, not a newly measured result.

The paper/source README and appendix correctly distinguish paper compilation, focused Lean checks, solver-free core replay, optional full-proof access, and licensed numerical generation. Source manifests may retain historical absolute paths as provenance, while documented portable commands operate in extracted layouts. The appendix does not claim a public deposit or DOI that does not exist.

## Formal proof integrity and coverage consistency

The formal source fingerprints, toolchain pin, complete dependency manifest, ownership/import audit, and kernel-replay script remain the accepted Stage 3 bytes. The inspected archive contains those sources and excludes the development symlink/cache. I did not repeat a Lean build because no formal byte changed and the archived fingerprints passed; this reviewer's earlier independent Stage 3 fresh-project build already validated the same proof package.

Appendix A and Section 5 consistently report coordinate correction, finite-sum safe-cut composition, selected transfer/cutoff/primal implications, and the audit of 95 project declarations. They do not claim executable Python verification, interval computation verification, a formal VIPR replay kernel, or Lean validation of benchmark artifacts. Dependency-cache retrieval is kept separate from project compilation and replay, and the installed-kernel replay is not presented as an independent proof assistant. The coverage table retains the required support/enclosure/embedding assumptions and explicit exclusions.

No missing file, broken required path, altered formal assertion, cache leakage, hash discrepancy, or overstated source-delivery claim was identified in this review. The separate final whole-manuscript review remains pending and is not a Stage 5 defect.
