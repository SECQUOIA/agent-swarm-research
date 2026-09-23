# Independent review of the four kinetics certificate pairs

**Accepted.** The four new kinetics cases exactly match their original benchmark
data, and their dense and all-splits certificate values reproduce through
independent exact dense covariance calculations. Each finite-memory upper bound
is strictly below the optimum of every admissible scalar-split continuous Liu
relaxation for the same stored problem.

This is a narrow artifact extension of the
[dense certificate review](research-20260912-dense-certificate-independent-review.md)
and [all-splits review](research-20260912-all-splits-independent-review.md), performed
by the same independent reviewer, `dense_exact_review`. Both certificate cores
retain their previously reviewed hashes:

- `certify_dense_design.py`:
  `0bb28391c819a6463d573e44f09790fc069986b062f31c3bc0de51c1f11d2f17`;
- `certify_all_splits.py`:
  `27a1977f6c7ba51aa64207a71bfe0b508c21aa1b7d3a14bf75e37da1b15bcf14`.

The unchanged library tests were not repeated. The reviewer did not modify author
code. The separate
[review script](../code/research_20260912/review_kinetics_certificates_independent.py)
and [saved report](../code/research_20260912/results/kinetics-dense-certificates-independent-review.json)
record the exact differences, source hashes, and input hashes.

For each new case, the review checked:

- exact equality of the model data in the original kinetics probe, dense
  certificate, all-splits certificate, and memory certificate;
- the source file hashes, case indices, regime labels, and certificate provenance;
- exact fractional feasibility, the dense information matrix, every gradient
  entry, the determinant, top-\(k\) tangent price, and bound arithmetic;
- exact incumbent feasibility and its determinant from the selected covariance;
- the all-splits information matrix from an independently constructed dense
  covariance with virtual noise;
- exact reconstruction of the positive LDL split factor and the nonpositive
  spectral upper-bound witness;
- all new logarithm intervals using the separate, narrower rational enclosure
  from the original independent review;
- the exact positive differences reported by
  [`compare_kinetics_certificates.py`](../code/research_20260912/compare_kinetics_certificates.py)
  and its [saved comparison](../code/research_20260912/results/kinetics-dense-memory-certified-comparison.json).

| Candidates | Regime | Fixed-split continuous lower minus memory upper | All-splits lower minus memory upper |
|---:|:---|---:|---:|
| 48 | fast | 0.1203779020261562 | 0.1092374662040422 |
| 48 | slow | 0.0943291403633041 | 0.0837810216245328 |
| 96 | fast | 0.1159597767181429 | 0.1043660456226959 |
| 96 | slow | 0.0986737296545475 | 0.0877134983293031 |

The table displays decimal approximations; positivity was checked on exact
rational differences. The all-splits statement has the same scope as the earlier
proof: every scalar \(0<a<\lambda_{\min}(R)\), for the continuous cardinality
relaxation. It does not include arbitrary diagonal splits or additional valid
inequalities and does not compare complete mixed-integer solves.

The original probe hashes are
`022386d46378b3b04e4aac40546609df00011e7aaeb3b35f90cd2175fb7e3d0c`
for 48 candidates and
`e680b5b01a1a2b424ace6dd1e19a06e435005a31565190fd282b688335dabc8a`
for 96 candidates. The exact-decimal sensitivity data are treated as frozen model
inputs. This review does not replace the separate kinetics mean-model review or
provide an error enclosure for generating sensitivities from the physical model.
The memory certificates retain the assumptions and previously reviewed algorithm
of the memory certificate core; its dynamic program was not independently replayed
again here.

Reproduction:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_kinetics_certificates_independent.py
```

No certificate defect or additional literature was identified.
