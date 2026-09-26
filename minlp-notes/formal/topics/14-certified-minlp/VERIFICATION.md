# Certified MINLP targeted verification

The [standalone verification record](../../../paper-certified-minlp/formal/VERIFICATION.md)
contains the actual commands, results, and links to logs and source fingerprints.

All 24 new modules passed warning-free targeted builds. The targeted axiom
audit passed for 1,112 declarations. Independent reviews cover all 49
mathematical obligations; a [supplementary review](../../../paper-certified-minlp/formal/REVIEW-CM04-CM34.md)
on 2026-09-25 covers CM04 and CM34, which the three original reviews did not
name. The discrete and PSD examples passed Lean's kernel checking. Source
fingerprints and all documentation links passed at `875a71ab`; two audit
programs were changed later; on 2026-09-25 both were rerun at `549a5786` and a
new source manifest was written (see the standalone record). The revised paper
built without warnings, and its revised formalization pages were visually
checked. This topic is complete.

The [source-package check](verification/delivery.json) is historical. It
records the archive committed in `875a71ab` (549,496 bytes, SHA-256
`58ac0855…`) and found that all 86 archived files matched the sources of that
revision and that the portable coverage documents resolved within it. View
that archive with
`git show 875a71ab:paper-certified-minlp/certified-minlp-paper-source.tar.gz`.
The current archive was replaced in `2071ed80` and has a different fingerprint;
no package comparison is recorded for it or for the current sources.

No project-wide verification, full-project kernel replay, or CI inspection
was performed. CI owns project-wide verification under the repository
[local verification rule](../../../AGENTS.md).
