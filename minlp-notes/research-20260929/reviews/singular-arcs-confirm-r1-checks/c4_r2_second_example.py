"""R2 second example: n = 1 with a = -0.5, c = 1, R = 1, S = -0.25, Q = -2,
so N(cos w) = f(w)|e^{iw} - a|^2 = -1 + 0.5 cos w.  Shows f(pi) < 0,
f(0) < 0, f''(pi) > 0, and real eigenvalues of the transfer matrix."""
import mpmath as mp
a, c, R, S, Q = mp.mpf(-0.5), mp.mpf(1), mp.mpf(1), mp.mpf(-0.25), mp.mpf(-2)
f = lambda w: R + 2 * S * mp.re(c / (mp.expj(w) - a)) + Q * abs(c / (mp.expj(w) - a)) ** 2
tr2 = (Q * c**2 - 2 * S * a * c + R * (1 + a**2)) / (2 * (a * R - c * S))
print("f(0)=%.4f f(pi)=%.4f f''(pi)=%.4f trPhi/2=%.4f eigenvalues=%s" % (
    f(0), f(mp.pi), mp.diff(f, mp.pi, 2), tr2, [float(tr2 + s * mp.sqrt(tr2**2 - 1)) for s in (1, -1)]))
