# Pinned kinetics input

The numerical table used by the historical checks is
[`kinetics_source_data/Q_drop0.csv` from dowlinglab/measurement-opt](https://github.com/dowlinglab/measurement-opt/blob/430090e610446aab88328ce495ffb15b684c56c4/kinetics_source_data/Q_drop0.csv).
Its full source commit is `430090e610446aab88328ce495ffb15b684c56c4` and its
SHA-256 is `54506ecb5606ea8900a99cb8490508bdd4b9a364aba4f26efe2676f9a7f6f3ca`.
The adjacent provenance JSON records the original input identification; neither
that record nor hash verification establishes how the physical sensitivities
were generated.

From the parent directory, prepare the input explicitly:

```sh
python data/prepare_input.py
```

This retrieves the pinned source URL and verifies the SHA-256 before writing
`data/kinetics_Q_drop0.csv`, an ignored local input. Use `--from-file PATH` to
verify a separately obtained copy. Numerical checks do not fetch inputs.
