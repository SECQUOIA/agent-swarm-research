# Stage 1 fixes

All accepted findings in `stage1-assessment.md` and the five round-one
reviews are addressed. The changes clarify domains, definitions, and the
scope of claims; the constructions and query exponents are unchanged.

| Review finding | Change |
| --- | --- |
| R1.1: general Hermitian definite-parity implementation | In `sections/02-model.tex`, the implementation proof now explains the even identity `p(|H|)=p(H)` and the odd identity `sign(H)p(|H|)=p(H)`, including `p(0)=0` on the zero eigenspace. |
| Review 2's domain finding; review 3's domain finding; R4.2; R5-1 | In `sections/04-fixed-accuracy.tex`, the pinned-tail statement and its proof now specify `C_0 delta <= |x| <= 1`; `G_r-e` is explicitly nonnegative on `[1,rho]`; and the bound on `d(x)` is restricted to `0 <= x <= 1`. The Fejer-tail bound additionally specifies `0 < u <= 1`, addressing the extra domain omission identified by R5-1. |
| R4.1: parity lower-bound cutoffs | The parity subsection introduces `E_r` as approximation errors governing lower bounds, names `E_1` the affine cutoff, and explicitly says that no complete optimal even-parity staircase or matching equality construction is asserted. |
| R5-2: integer indices | The opening of `sections/04-fixed-accuracy.tex` declares all approximation-order indices, including `r` and `j`, to be nonnegative integers. This covers the threshold definitions, minimization, Taylor orders, and `E_r`. |
| R5-3: positive general normalization | `sections/02-model.tex` now defines an exact normalization-`nu` encoding by `J_out^* V J_out = A/nu`, with `nu > 0`. The exact-interval impossibility proposition in `sections/03-exact.tex` explicitly states `0 < nu < 2`. The formal differentiated-bound caveat remains in place. |

Validation completed with:

```sh
conda run -n qipm --live-stream make -C /workspace/qipm/notes/spectral-shift-paper
```

The build succeeded and produced the 10-page `main.pdf`. The first LaTeX
pass requested updated cross-references; the subsequent passes resolved
them. The final `main.log` and `main.blg` contain no warnings, undefined or
multiply defined references, or overfull/underfull boxes. A whitespace
check on the edited source files also passed. No major mathematical
finding required a proof change or another review round.
