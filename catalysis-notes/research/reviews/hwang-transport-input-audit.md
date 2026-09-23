# Hwang transport inputs: arithmetic and scope

2026-09-15. Narrow source check for the optional oxygen-return measurement. No new experiment or revised source value is asserted.

The original [Hwang 2026 SI](../../literature/papers/hwang2026-supplementary-information-for-mechanism-and/fulltext.md), page S3, prints these inputs for `r_V R²/(D C)`:

| Input | Printed value |
|---|---:|
| Aggregate radius `R` | 0.011 cm |
| Oxygen concentration `C` | 1.8 × 10−5 mol cm−3 |
| Volumetric net O2 consumption `r_V` | 1.1 × 10−7 mol cm−3 s−1 |
| Effective diffusivity `D` | 0.12 cm² s−1 |
| Reported dimensionless result | 0.0010 |

Direct substitution instead gives

`(1.1e−7 × 0.011²) / (0.12 × 1.8e−5) = 6.162e−6`.

The approximately 162-fold discrepancy was checked against a rendered image of the original PDF, not only extracted text. The source does not identify which printed quantity or normalization accounts for it. Do not silently replace a source input or treat the recalculated number as a newly measured transport parameter. Both results are small, so this arithmetic issue alone does not overturn the source's conclusion about negligible concentration gradients for its measured net reaction rate.

**Separate scope limit:** net O2 consumption is not an upper bound on gross O2 reconsumption when simultaneous oxygen return is the hypothesis being tested. Substituting `k = r_V/C` into a pore-escape model would assume away an unknown part of that cycle. The estimated effective diffusivity is also not, by itself, a validated lower bound for every region in which returned O2 could originate. Thus neither printed ratio supplies the escape calibration required for the isotope rejection test.

The original PDF is retained at `/tmp/epoxidation-process/hwang2026-si.pdf`; the inspected page image is `/tmp/ag-aging-prior-art/hwang-si-s3.png`. This note was sent to the sole literature maintainer for a qualified source-note correction. The primary article's kinetic conclusions are not rejected by this check.
