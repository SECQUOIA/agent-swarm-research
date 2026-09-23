# Whole-paper round 2 — correction

The one accepted minor issue is corrected in `sections/introduction.tex`. The canonical coexistence heat-capacity paragraph now defines `w_-` and `w_+` locally as the limiting phase probabilities. It also identifies `aN` as the optional kinetic Gamma shape and explicitly states that `a=0` denotes no kinetic sector. The latter convention does not invoke a shape-zero Gamma distribution.

No formula, theorem, proof, workflow status, or other scientific content was changed. Ran `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`: the 48-page PDF builds successfully, and the final log contains no warnings or overfull/underfull box diagnostics. The correction is ready for coordinator verification and closure.
