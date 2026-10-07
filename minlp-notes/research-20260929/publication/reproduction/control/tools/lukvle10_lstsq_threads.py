"""Diagnostic: do the lukvle10 least-squares KKT multipliers (lukvle10_lagr.kkt_multipliers,
np.linalg.lstsq) depend on the OpenBLAS thread count? Run from open-instances/ with
python3 - < this file; prints a hash of the multiplier vector."""
import hashlib, json, os
import numpy as np
from lukvle10_lagr import kkt_multipliers, load_sol
x = load_sol("minlplib_sol/lukvle10.p5.sol")
lam, res = kkt_multipliers(x)
print(json.dumps(dict(threads=os.environ.get("OPENBLAS_NUM_THREADS"), sha256=hashlib.sha256(lam.tobytes()).hexdigest(),
                      lam_495=repr(float(lam[495])), residual=float(res))))
np.save(f"/tmp/ctrl_lam_t{os.environ.get('OPENBLAS_NUM_THREADS')}.npy", lam)
