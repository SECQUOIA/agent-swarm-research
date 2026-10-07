"""Independent lnts Theorem 3 review. Standard library; no float arithmetic.

All outputs stay beside this file. Repository files are read only as data.
The root is located by certified rational bisection from [0,4/N], not Newton.
"""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import os
import hashlib
import json
import xml.etree.ElementTree as ET

REPO = Path(os.environ['MINLP_REPO_ROOT'])
OSIL = Path(os.environ['MINLPLIB_OSIL_ROOT'])
OUT = Path(__file__).resolve().parent
SCALE = 10 ** 120


def attrs(node, allowed):
    assert set(node.attrib) <= set(allowed), (node.tag, node.attrib)


def expand(node, integer=False):
    result = []
    for el in node:
        assert el.tag == 'el' and not len(el)
        attrs(el, ['mult', 'incr'])
        val = Q(el.text)
        step = Q(el.get('incr', '0'))
        mult = int(el.get('mult', '1'))
        assert mult > 0
        result.extend(val + k * step for k in range(mult))
    if integer:
        assert all(v.denominator == 1 for v in result)
        return [v.numerator for v in result]
    return result


def ast(node):
    if node.tag == 'number':
        attrs(node, ['value', 'type', 'id'])
        assert node.get('type', 'real') == 'real' and not len(node)
        return ('number', Q(node.attrib['value']))
    if node.tag == 'variable':
        attrs(node, ['idx', 'coef'])
        assert not len(node)
        return ('variable', int(node.attrib['idx']), Q(node.get('coef', '1')))
    attrs(node, [])
    assert node.tag in ['product', 'sum', 'sin', 'cos']
    assert len(node) == 1 if node.tag in ['sin', 'cos'] else len(node) >= 2
    return (node.tag,) + tuple(ast(ch) for ch in node)


def var(j):
    return ('variable', j, Q(1))


def bound(s):
    return s if s in ['INF', '-INF'] else Q(s)


def inspect_osil(N, raw=None):
    path = OSIL / f'lnts{N}.osil'
    raw = path.read_bytes() if raw is None else raw
    root = ET.fromstring(raw)
    for node in root.iter():
        node.tag = node.tag.rsplit('}', 1)[-1]
    assert root.tag == 'osil'
    data = root.find('instanceData')
    assert len(data) == 6
    assert set(x.tag for x in data) == {
        'variables', 'objectives', 'constraints', 'linearConstraintCoefficients',
        'quadraticCoefficients', 'nonlinearExpressions'}
    h = 5 * (N + 1)
    blocks = [list(range(k * (N + 1), (k + 1) * (N + 1))) for k in range(5)]
    theta, px, py, vx, vy = blocks
    fixed = {px[0]: Q(0), py[0]: Q(0), py[-1]: Q(5), vx[0]: Q(0),
             vx[-1]: Q(45), vy[0]: Q(0), vy[-1]: Q(0)}
    variables = data.find('variables')
    attrs(variables, ['numberOfVariables'])
    assert int(variables.attrib['numberOfVariables']) == len(variables) == h + 1
    B = Q('1.5707963267949')
    names = []
    for j, v in enumerate(variables):
        assert v.tag == 'var' and not len(v)
        attrs(v, ['name', 'type', 'lb', 'ub'])
        assert v.get('type', 'C') == 'C'
        names.append(v.attrib['name'])
        actual = (bound(v.get('lb', '0')), bound(v.get('ub', 'INF')))
        expected = ((-B, B) if j <= N else
                    (fixed[j], fixed[j]) if j in fixed else
                    (Q(0), 'INF') if j == h else ('-INF', 'INF'))
        assert actual == expected, (j, actual, expected)
    assert len(set(names)) == len(names)
    objectives = data.find('objectives')
    attrs(objectives, ['numberOfObjectives'])
    assert int(objectives.get('numberOfObjectives', '1')) == len(objectives) == 1
    obj = objectives[0]
    assert obj.tag == 'obj'
    attrs(obj, ['name', 'maxOrMin', 'constant', 'weight', 'numberOfObjCoef'])
    assert obj.get('maxOrMin') == 'min'
    assert Q(obj.get('constant', '0')) == 0 and Q(obj.get('weight', '1')) == 1
    assert int(obj.attrib['numberOfObjCoef']) == len(obj) == 1
    coef = obj[0]
    attrs(coef, ['idx'])
    assert coef.tag == 'coef' and int(coef.attrib['idx']) == h and Q(coef.text) == N
    constraints = data.find('constraints')
    attrs(constraints, ['numberOfConstraints'])
    assert int(constraints.attrib['numberOfConstraints']) == len(constraints) == 4 * N
    for con in constraints:
        assert con.tag == 'con' and not len(con)
        attrs(con, ['name', 'lb', 'ub', 'constant'])
        assert bound(con.get('lb', '-INF')) == bound(con.get('ub', 'INF')) == 0
        assert Q(con.get('constant', '0')) == 0
    lin = data.find('linearConstraintCoefficients')
    attrs(lin, ['numberOfValues'])
    assert len(lin) == 3 and set(x.tag for x in lin) == {'start', 'colIdx', 'value'}
    starts = expand(lin.find('start'), True)
    cols = expand(lin.find('colIdx'), True)
    vals = expand(lin.find('value'))
    assert int(lin.attrib['numberOfValues']) == len(cols) == len(vals) == 8 * N
    assert len(starts) == 4 * N + 1 and starts[0] == 0 and starts[-1] == len(vals)
    assert all(a <= b for a, b in zip(starts, starts[1:]))
    linear = []
    for row in range(4 * N):
        entries = list(zip(cols[starts[row]:starts[row + 1]], vals[starts[row]:starts[row + 1]]))
        assert len(entries) == len(dict(entries)) == 2
        linear.append(dict(entries))
    quad = data.find('quadraticCoefficients')
    attrs(quad, ['numberOfQuadraticTerms'])
    assert int(quad.attrib['numberOfQuadraticTerms']) == len(quad) == 4 * N
    quadratic = [[] for _ in range(4 * N)]
    for term in quad:
        assert term.tag == 'qTerm' and not len(term)
        attrs(term, ['idx', 'idxOne', 'idxTwo', 'coef'])
        row = int(term.attrib['idx'])
        assert 0 <= row < 4 * N
        quadratic[row].append((int(term.attrib['idxOne']), int(term.attrib['idxTwo']), Q(term.attrib['coef'])))
    nls = data.find('nonlinearExpressions')
    attrs(nls, ['numberOfNonlinearExpressions'])
    assert int(nls.attrib['numberOfNonlinearExpressions']) == len(nls) == 2 * N
    nonlinear = {}
    for nl in nls:
        attrs(nl, ['idx'])
        row = int(nl.attrib['idx'])
        assert nl.tag == 'nl' and len(nl) == 1 and 0 <= row < 4 * N and row not in nonlinear
        nonlinear[row] = ast(nl[0])
    for row in range(4 * N):
        block, i = divmod(row, N)
        state = [px, py, vx, vy][block]
        assert linear[row] == {state[i]: Q(-1), state[i + 1]: Q(1)}
        if block < 2:
            velocity = [vx, vy][block]
            assert sorted(quadratic[row]) == [(velocity[i], h, Q(-1, 2)), (velocity[i + 1], h, Q(-1, 2))]
            assert row not in nonlinear
        else:
            assert not quadratic[row]
            fn = 'cos' if block == 2 else 'sin'
            expected = ('product', ('sum',
                ('product', (fn, var(i)), ('number', Q(100))),
                ('product', (fn, var(i + 1)), ('number', Q(100)))),
                ('number', Q(-1, 2)), var(h))
            assert nonlinear[row] == expected, row
    return {'N': N, 'sha256': hashlib.sha256(raw).hexdigest(),
            'variables': len(variables), 'rows': len(constraints), 'h_name': names[h],
            'continuous': True, 'all_rows_bounds_objective_checked': True}


def derive_weights(N):
    # Symbolic forward recurrence, normalized by a*h and a*h^2.
    # Velocity coefficients are represented in units 1/2; positions in 1/4.
    velocity = [0] * (N + 1)
    position = [0] * (N + 1)
    for i in range(N):
        before = velocity.copy()
        velocity[i] += 1
        velocity[i + 1] += 1
        position = [p + u + v for p, u, v in zip(position, before, velocity)]
    w = [Q(v, 2) for v in velocity]
    c = [Q(p, 4) for p in position]
    assert w == [Q(1, 2)] + [Q(1)] * (N - 1) + [Q(1, 2)]
    assert c == [Q(2 * N - 1, 4)] + [Q(N - j) for j in range(1, N)] + [Q(1, 4)]
    r = [cj / wj - Q(N, 2) for wj, cj in zip(w, c)]
    assert all(c[N - j] == N * w[j] - c[j] for j in range(N + 1))
    assert all(r[N - j] == -r[j] for j in range(N + 1))
    assert max(map(abs, r)) == Q(N - 1, 2)
    return w, c, r


def invsqrt(t):
    q = 1 + t * t
    # k = floor(SCALE/sqrt(q)). The following inequalities certify both ends:
    # k^2 * numerator <= SCALE^2 * denominator < (k+1)^2 * numerator.
    k = isqrt((SCALE * SCALE * q.denominator) // q.numerator)
    assert k * k * q.numerator <= SCALE * SCALE * q.denominator
    assert SCALE * SCALE * q.denominator < (k + 1) ** 2 * q.numerator
    return Q(k, SCALE), Q(k + 1, SCALE)


def cd(w, r, nu):
    assert nu >= 0
    C0 = C1 = D0 = D1 = Q(0)
    for wj, rj in zip(w, r):
        lo, hi = invsqrt(nu * rj)
        C0 += wj * lo
        C1 += wj * hi
        # By reflection, sum c_j sin(theta_j) = nu * sum w_j r_j^2/sqrt(...).
        # This independent form has only nonnegative terms.
        coefficient = nu * wj * rj * rj
        D0 += coefficient * lo
        D1 += coefficient * hi
    return (C0, C1), (D0, D1)


def g(w, r, nu):
    C, D = cd(w, r, nu)
    return (D[0] - Q(20, 81) * C[1] ** 2,
            D[1] - Q(20, 81) * C[0] ** 2), C


def bracket(N, w, r):
    left, right = Q(0), Q(4, N)
    assert g(w, r, left)[0][1] < 0 < g(w, r, right)[0][0]
    for _ in range(300):
        mid = (left + right) / 2
        (lo, hi), _ = g(w, r, mid)
        if hi < 0:
            left = mid
        elif lo > 0:
            right = mid
        else:
            raise AssertionError('Insufficient precision to decide bisection sign')
    assert left > 0
    gl, Cl = g(w, r, left)
    gr, Cr = g(w, r, right)
    assert gl[1] < 0 < gr[0]
    assert right - left < Q(1, 10 ** 90)
    obj = Q(9 * N, 20) / Cl[1], Q(9 * N, 20) / Cr[0]
    assert obj[0] < obj[1] and obj[1] - obj[0] < Q(1, 10 ** 90)
    return left, right, gl, gr, Cl, Cr, obj


def atan_small(x):
    assert 0 < x < 1
    partial = sum(((-1) ** k * x ** (2 * k + 1) / (2 * k + 1) for k in range(40)), Q(0))
    return partial, partial + x ** 81 / 81


def pi_check():
    # Machin identity pi/2 = 8*atan(1/5) - 2*atan(1/239), with series remainders.
    a, b = atan_small(Q(1, 5)), atan_small(Q(1, 239))
    lo, hi = 8 * a[0] - 2 * b[1], 8 * a[1] - 2 * b[0]
    B = Q('1.5707963267949')
    assert hi < B
    # atan(3/2) = pi/4 + atan(1/5) < pi/4 + 1/5 < 1.
    assert hi / 2 + Q(1, 5) < 1
    return {'pi_over_two': [str(lo), str(hi)],
            'B_minus_pi_over_two': [str(B - hi), str(B - lo)]}


def dec(q, digits, upward=False):
    scale = 10 ** digits
    n = -((-q.numerator * scale) // q.denominator) if upward else (q.numerator * scale) // q.denominator
    sign = '-' if n < 0 else ''
    s = str(abs(n)).rjust(digits + 1, '0')
    return sign + s[:-digits] + '.' + s[-digits:]


def pair_decimal(pair, digits):
    return [dec(pair[0], digits), dec(pair[1], digits, True)]


def rejected(call):
    try:
        call()
    except AssertionError:
        return True
    raise AssertionError('Mutation unexpectedly accepted')


def main():
    dossier = json.loads((REPO / 'paper-open-minlplib/development/dossiers/checks/lnts-lukvle10/lnts_exact_opt.json').read_text(), parse_float=Q)
    results = []
    for N in [50, 100, 200, 400]:
        model = inspect_osil(N)
        w, c, r = derive_weights(N)
        a, b, gl, gr, Cl, Cr, obj = bracket(N, w, r)
        tmax = b * max(map(abs, r))
        assert tmax < Q(3, 2)  # proves |theta*| < 1 < B.
        original = OSIL.joinpath(f'lnts{N}.osil').read_bytes()
        assert b'value="100"' in original
        model_mutation = rejected(lambda: inspect_osil(N, original.replace(b'value="100"', b'value="100.0000000000000000000000000000000000000001"', 1)))
        def sign_certificate(left, right):
            assert g(w, r, left)[0][1] < 0 < g(w, r, right)[0][0]
        shifts = []
        for shift in [Q(1, 10 ** 55), -Q(1, 10 ** 55)]:
            shifts.append(rejected(lambda: sign_certificate(a + shift, b + shift)))
        entry = next(d for d in dossier if d['N'] == N)
        display = Q(entry['opt_lower']), Q(entry['opt_upper'])
        assert display[0] <= obj[0] < obj[1] <= display[1]
        point = json.loads((REPO / f'research-20260929/publication/primal/lnts/points/lnts{N}_point.json').read_text(), parse_float=Q)
        assert model['sha256'] == point['osil_sha256']
        printed_primal = tuple(map(Q, point['objective_enclosure']))
        assert printed_primal[0] <= obj[0] < obj[1] <= printed_primal[1]
        henc = next(x for x in point['enclosures'] if x[0] == model['h_name'])
        primal = N * Q(henc[1]), N * Q(henc[2])
        assert primal[0] <= obj[0] < obj[1] <= primal[1]
        delta = primal[0] - obj[1], primal[1] - obj[0]
        assert delta[0] < 0 < delta[1]
        middle = Q(point['fixed_controls'][f'x{N // 2 + 1}'])
        assert 0 < abs(middle) < Q(1, 10 ** 110)
        result = {'model': model,
                  'nu_bracket_exact': [str(a), str(b)], 'nu_bracket_decimal_96': pair_decimal((a, b), 96),
                  'g_at_left_exact': list(map(str, gl)), 'g_at_right_exact': list(map(str, gr)),
                  'g_at_left_decimal_100': pair_decimal(gl, 100), 'g_at_right_decimal_100': pair_decimal(gr, 100),
                  'C_at_left_exact': list(map(str, Cl)), 'C_at_right_exact': list(map(str, Cr)),
                  'opt_exact': list(map(str, obj)), 'opt_decimal_96': pair_decimal(obj, 96),
                  'opt_width_upper': dec(obj[1] - obj[0], 100, True),
                  'display_16': pair_decimal(obj, 16), 'display_40': pair_decimal(obj, 40),
                  'dossier_40_digit_enclosure_contains_own': True,
                  'primal_25_digit_enclosure': point['objective_enclosure'],
                  'primal_60_digit_h_objective_enclosure': pair_decimal(primal, 60),
                  'primal_minus_opt_interval': pair_decimal(delta, 65),
                  'gap_to_stored_primal_upper_bound': dec(delta[1], 65, True),
                  'stored_primal_middle_control_nonzero_exact': str(middle),
                  'stored_primal_strictly_suboptimal_by_middle_support_term': True,
                  'tmax_upper': dec(tmax, 18, True),
                  'mutated_model_rejected': model_mutation, 'shifted_brackets_rejected': shifts}
        results.append(result)
        print(json.dumps({k: v for k, v in result.items() if not k.endswith('_exact')}, indent=2), flush=True)
    output = {'arithmetic': 'Python int/Fraction/isqrt only; 120 decimal-place reciprocal-root grid; 300 rational bisections',
              'angle_bound_check': pi_check(), 'results': results}
    (OUT / 'certificate.json').write_text(json.dumps(output, indent=2) + '\n')
    print('PASS: all four models, exact sign certificates, optimum enclosures, comparisons, and negative tests')


if __name__ == '__main__':
    main()
