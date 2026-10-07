# Stage 2 fixes

The sole accepted finding, R5-1 in `stage2-round1-review5.md`, is addressed.
The sentence introducing `eq:FR-max` in `sections/05-joint-accuracy.tex`
now assumes `0 < K <= sqrt(rho) R_0^(-2)/(4 e)` and states that the maximum
has a finite, nonempty index set. The separate `K=0` argument remains
unchanged and uses each finite index in `eq:FR-all-bound`.

Validation:

```sh
conda run -n qipm --live-stream make -C /workspace/qipm/notes/spectral-shift-paper
```

The build succeeded and produced the 20-page `main.pdf`; its output is
recorded in `stage2-fix-build.log`. The final `main.log` and `main.blg`
contain no warnings, undefined or multiply defined references, or
overfull/underfull boxes. The source whitespace check passed. No other
manuscript text was changed.
