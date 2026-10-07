"""Reviewer r2: for each tapped branch of MATPOWER case39, test whether untapped or tapped
admittance values occur among the numeric coefficients of powerflow0039r/0039p GAMS files."""
import re, sys
def mat(path, name):
    s = open(path).read()
    blk = re.search(r'mpc\.%s = \[(.*?)\];' % name, s, re.S).group(1)
    return [[float(t) for t in ln.split(';')[0].split()] for ln in blk.strip().splitlines() if ln.strip() and not ln.strip().startswith('%')]
br = mat('case39_matpower.m', 'branch'); bus = mat('case39_matpower.m', 'bus')
print('bus shunts nonzero:', [(int(b[0]), b[4], b[5]) for b in bus if b[4] or b[5]])
for f in sys.argv[1:]:
    nums = [abs(float(x)) for x in re.findall(r'(?<![\w.])(\d+\.\d+(?:[eE][-+]?\d+)?|\d+)(?![\w.])', open(f).read())]
    nums = sorted(set(nums))
    import bisect
    def has(v):
        if v == 0: return None
        i = bisect.bisect_left(nums, v * (1 - 1e-11))
        return i < len(nums) and nums[i] <= v * (1 + 1e-11)
    print('==', f)
    for r in br:
        tau = r[8]
        if tau == 0: continue
        R, X = r[2], r[3]; z2 = R * R + X * X; g, b = R / z2, X / z2
        un = [has(g), has(b)]
        tp = [has(g / tau), has(b / tau), has(g / tau ** 2), has(b / tau ** 2)]
        print('  %2d-%2d tau=%.3f r=%g x=%g  untapped g,b present: %s  tapped g/t,b/t,g/t2,b/t2 present: %s' % (r[0], r[1], tau, R, X, un, tp))
