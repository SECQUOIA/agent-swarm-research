# Submission checklist

The manuscript checks and portable build have passed. The actual final
results are in [FINAL-VERIFICATION.md](FINAL-VERIFICATION.md). Commands run
from `paper-bb-complexity` include:

```sh
python3 verification/check_sources.py --json delivery/source-check.json
python3 verification/package_sources.py
```

The source package includes `BUILD.txt` and all local manuscript inputs. Its
output is `delivery/bb-complexity-sources.zip`.

- [x] Resolve every source-check error: missing local inputs or graphics, duplicate labels or bibliography keys, unresolved references or citations, private paths, and unfinished markers.
- [x] Review the dependency report. Include only manuscript sources, required local TeX support, the referenced bibliography, and original or properly licensed figures. The tools reject dependencies outside the paper directory and inside `evidence`, `review`, `reviews`, `verification`, `delivery`, or `literature` directories. They cannot determine copyright ownership from a figure file.
- [x] Put exact standalone build commands and required TeX packages in `BUILD.txt`. Keep authors blank as requested. Complete mathematical and attribution reviews recorded elsewhere in the evidence directory.
- [x] Build the manuscript using `BUILD.txt`, inspect the PDF, and resolve build warnings that affect references, citations, figures, or layout. Perform only targeted manuscript checks; CI handles project-wide checks.
- [x] Package the checked sources. Extract the ZIP into a fresh directory and build using the included `BUILD.txt`; verify the hashes there with `sha256sum -c SHA256SUMS`.
- [x] Confirm that the source archive contains no internal evidence, reviews, experiment outputs, or downloaded literature. Deliver the final PDF separately if the journal requires it.
- [x] Record the shared Luna lead's serialized post-handoff literature-database check and discovery-run archive; independent BB KB writes/checks remain stopped.

`dependencies.json` records the entry point, reachable source files, and dependency edges. `SHA256SUMS` hashes every other ZIP member, including `dependencies.json`; it does not hash itself. Packaging prints the SHA256 hash of the completed ZIP. Archive member timestamps and permissions are fixed, so identical inputs produce identical archives with the same Python/zlib implementation. The archive is written atomically after its contents have been checked.

The checker follows literal `input`/`include`, `includegraphics`, `bibliography`/`addbibresource`, and existing local class, package, and bibliography-style files. Paths resolve from the manuscript directory, as in a build run there. It handles escaped percent signs, citation options and multiple keys, natbib commands, and common cleveref references and ranges. DOI and URL bibliography fields are allowed.

This is a static source check, not a TeX interpreter or BibTeX validator. Macro-generated paths, labels, citations, alternative entry points, external reference databases, package-specific import commands, and commands in verbatim text need manual review or a simpler literal representation. Installed TeX packages and system files are not archived. A clean standalone build is required to catch those limits, malformed bibliography syntax, and other TeX errors. Commented TeX labels and citations are ignored; private absolute paths are rejected even in comments.

## Targeted verification record

- `python3 paper-bb-complexity/verification/check_sources.py` from the repository root: exited with status 1 and `entrypoint: missing TeX input: main.tex`, as expected before the manuscript existed.
- `python3 /tmp/bb_submission_tools_fixtures.py`, then `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/bb_submission_tools_fixtures.py` after tool refinements: passed synthetic fixtures outside the repository for escaped/commented percent signs, commented labels and citations, nested citation options and multiple keys, cleveref ranges and hyperref labels, root-relative and unbraced inputs, normalized archive paths, bibliography comments and DOI/URL fields, graphics search-path replacement, missing dependencies, duplicate labels and bibliography keys, unresolved references and citations, private paths, internal material, dynamic inputs, cycles, malformed arguments, and symlink rejection. It also checked required build instructions, identical archives on repeated packaging, every manifest hash, successful source checking after extraction, and preservation of an existing archive when validation fails. The fixture script is temporary test material, not a submission dependency.

These targeted checks exercise the submission tools only. No computational experiments were rerun, no project-wide verification was performed, and CI status and logs were not inspected. They do not establish that the final manuscript builds or that its mathematical claims are correct.

The completed paper's source and clean-build checks, independent reviews,
and final artifact identities are recorded in [FINAL-VERIFICATION.md](FINAL-VERIFICATION.md).
