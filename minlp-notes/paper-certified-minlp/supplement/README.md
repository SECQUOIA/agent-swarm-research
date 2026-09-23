# Experiment supplement

Start with `certified-minlp-core.tar.gz` (about 6.5 MB). It contains a standalone
README, checker, pinned dependency specifications, all 289 campaign models, original compact
records, exact audit data, source snapshots, tests, representative certificates,
and reproducible tables/catalog. Extract it to a new directory and follow
`minlp-certified-evidence/README.md`.

`certified-minlp-certificates.tar.gz` (about 30.7 GB) is the optional complete
proof collection: accepted and rejected historical completed proofs, uniform
and targeted-repair attempts, exact master and lemma artifacts, and relevant
logs. It expands to about 93.7 GB of regular files. Extract it beside the core
only for full replay; the core also supplies a streaming verifier that reads
its entire manifest without extraction. No vendor solver is needed for replay.

Archive SHA-256 values:

- `certified-minlp-core.tar.gz`: 6,478,681 bytes; `d2805b1cfead992904b840d4a63c913287d42aec309f1502b1d4e90e9d2e9f1b`.
- `certified-minlp-certificates.tar.gz`: 30,664,561,063 bytes; `88c23497c2d20c76b3ac25cfc2c60a529aecb35da98e8de00213f4513ed314d4`.

`archives.json` is the machine-readable archive index. The core contains separate
core/bulk manifests, frozen protocols and source versions, proof provenance, and
MINLPLib CC-BY 4.0 attribution. The default checker is the final reporting-repair
version; its README explains the one known acceptance-count difference from
the preserved original primary replay. The original timed outcomes remain
unchanged.

The core was rebuilt after clarifying the generated campaign-table caption. The
bulk byte count and SHA-256 above are retained from its previous full readback;
this core-only rebuild checked its size and did not reread or rehash bulk contents.
