# G1-16: reading-(c) infeasibility of the dtoc5, chain and powerflow points

Exact checks (Python `Fraction`) behind the one-line proofs in Appendix A.4
(`sections/A-semantics.tex`, paragraph "Points"). Run on copies in
`/tmp/g1-checks/` of the cached OSIL files (`~/.cache/minlplib/minlplib/osil/`),
of `research-20260929/publication/primal/dtoc5-lukvle10/points/dtoc5_point.txt.gz`,
of `research-20260929/publication/primal/powerflow/points/*.json` and of the
shared reader `research-20260929/reviews/open-instances-verification/osilx.py`
(used by `pf_c.py`; `parse.py` is a separate ElementTree reader used for
`dtoc5` and `chain`). Output: `readingc.log`.

- dtoc5: row e2 is -h*u0 + y0 - y1 + 4h*y0^2 = 0 with the strings "-2e-5"
  and "8e-5", y0 = 1 fixed, u0 = 8.0572...; fl(8e-5) = 4 fl(2e-5), so under
  reading (c) the residual at our point is (fl(h)-h)(4y0^2-u0) != 0.
- chain: rows x_{i+1} - x_i - eta(u_i+u_{i+1}) = 0 with eta = 1/(2N) and
  fl(eta) != eta; x_0 = 1 and x_N = 3 are fixed.
- powerflow: rows P + c*T(x) = 0 whose only non-unit coefficient is +-c,
  with fl(c) != c and P != 0 in the Krawczyk box of our point (radius 1e-45):
  0030p row e2 (c = -7.14285714285714, P = x31 ~ -0.162); 0039p and 0039r
  row e65 (|c| = b = 55.2486187845304, P = P_{30->2} ~ 6.714). Under reading (c)
  the residual is P (c - fl(c))/c != 0.
