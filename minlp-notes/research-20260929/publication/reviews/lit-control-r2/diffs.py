from fractions import Fraction as F
cert = {'camshape100': F('-4.28414712174675'), 'camshape200': F('-4.27850023299273'),
        'camshape400': F('-4.27568847892555'), 'camshape800': F('-4.27427414195420'),
        'dtoc5': F('5.38967211918114'), 'optcdeg2_lo': F('293.87607509587509'), 'optcdeg2_up': F('293.87607509587509328')}
vals = [('ANTIGONE 2738 best feasible', 'camshape100', '-4.284302'),
        ('ANTIGONE 2738 CONOPT polished', 'camshape100', '-4.28414626579'),
        ('BARON 2738', 'camshape100', '-4.28414710266608'),
        ('COPT 2738', 'camshape100', '-4.284189915'),
        ('SCIP9.2.1 2738', 'camshape100', '-4.28414626680553'),
        ('COPT 2480', 'camshape200', '-4.278677725'),
        ('BARON 2480', 'camshape200', '-4.27849246237069'),
        ('ANTIGONE 2480', 'camshape200', '-4.278491'),
        ('COPT 2703', 'camshape400', '-4.276430314'),
        ('SCIP9.2.1 2703', 'camshape400', '-4.33023953971002'),
        ('BARON 2703', 'camshape400', '-4.27565886682199'),
        ('MINOTAUR 3177', 'camshape800', '-4.2774'),
        ('COPT 3177', 'camshape800', '-4.277371318'),
        ('BARON 3177', 'camshape800', '-4.51546318707998'),
        ('ANTIGONE 3177', 'camshape800', '-4.274187'),
        ('SCIP 3177', 'camshape800', '-4.27418677010926'),
        ('Mueller2019 best primal camshape800', 'camshape800', '-4.27431'),
        ('MINOTAUR 8585', 'dtoc5', '5.3897'),
        ('BARON 8585', 'dtoc5', '5.38966688447816'),
        ('COPT 8585', 'dtoc5', '5.389829024'),
        ('BARON 8803', 'optcdeg2_up', '293.876075074557'),
        ('COPT 8803', 'optcdeg2_up', '293.880662592'),
        ('GUROBI MINLPLib optcdeg2', 'optcdeg2_lo', '292.41713458')]
for lab, k, v in vals:
    d = F(v) - cert[k]
    print(f'{lab:40s} {v:>20s}  value - certified = {float(d):+.3e} ({"below" if d < 0 else "above"})')
