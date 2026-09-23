# Certified MINLP targeted verification

The [standalone verification record](../../../paper-certified-minlp/formal/VERIFICATION.md)
contains the actual commands, results, and links to logs and source fingerprints.

All 24 new modules passed warning-free targeted builds. The targeted axiom
audit passed for 1,112 declarations. Independent reviews cover all 49
mathematical obligations, and the discrete and PSD examples passed Lean's
kernel evaluation. Source fingerprints and all documentation links passed.
The revised paper built without warnings, and its revised formalization pages
were visually checked. This topic is complete.

The [source-package check](verification/delivery.json) records the refreshed
archive fingerprint and confirms that all 86 archived files match the current
sources. The portable coverage documents resolve within that archive.

No project-wide verification, full-project kernel replay, or CI inspection
was performed. CI owns project-wide verification under the repository
[local verification rule](../../../AGENTS.md).
