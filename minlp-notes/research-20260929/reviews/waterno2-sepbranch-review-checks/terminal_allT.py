"""Independent terminal-row derivation (ind_verify.terminal_row) for other T."""
import sys
import ind_verify
import vmodel

for T in [int(a) for a in sys.argv[1:]]:
    ind_verify.T = T
    I = vmodel.instance(T)
    print(f"T = {T}")
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        end, rhs = ind_verify.terminal_row(I)
    print("  " + [l for l in buf.getvalue().splitlines() if "sum_t d_t" in l][0].strip())
    print("  terminal row:", {I["m"]["names"][v]: str(a) for v, a in end.items()}, ">=", rhs)
