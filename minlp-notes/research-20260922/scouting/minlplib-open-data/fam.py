import re
FAM=[
(r'^autocorr_bern','autocorr_bern (low-autocorrelation binary seq.)'),
(r'^(chimera|ising|maxcsp|pb\d|qap$|qapw|qspp|color_lab|graphpart)','BQP / binary polynomial (maxcut, QAP, CSP, qspp, coloring)'),
(r'^(sonet|edgecross|faclay|sporttournament|mbtd|flay)','binary quadratic w/ linear constraints (layout, partition, tournament)'),
(r'^(powerflow|acopf)','AC OPF (powerflow/acopf)'),
(r'^transswitch','AC OPF + line switching (transswitch)'),
(r'^(deb\d|var_con)','generation with trig (deb/var_con)'),
(r'^pooling_spp','pooling_spp (Alfaki-Haugland style large pooling)'),
(r'^(pooling_|crudeoil_pooling|mpbp|blendgap)','other pooling/blending (digabel, epa, crudeoil_pooling, mpbp)'),
(r'^crudeoil_li','crude oil scheduling (Li)'),
(r'^waterno1','waterno1 (water op., Darcy signpower)'),
(r'^waterno2','waterno2 (water op., trig/polynomial pump)'),
(r'^waternd_','waternd (water network design, H-W signpower)'),
(r'^(water$|water3|waterful|waternd2|waters|watersbp|waterx|waterz)','water design (Karuppiah/Grossmann-type)'),
(r'^waterund','waterund (water under design, pooling-like)'),
(r'^wastewater','wastewater (Castro)'),
(r'^nuclear','nuclear core reload'),
(r'^(ndcc|nd_netgen|telecomsp)','network design w/ congestion/queue (ndcc, nd, telecomsp)'),
(r'^sfacloc','sfacloc (stochastic facility location)'),
(r'^(multiplants|csched)','multiplant/cyclic scheduling'),
(r'^(heatexch|ex1233|synheat)','heat exchanger networks (LMTD / area)'),
(r'^(knp|elec|pointpack|ringpack|kall_|p_ball|ball_mk|polygon|ngone|maxmin|orth_|gabriel|tspn|space\d|shiporig|eq6_1)','geometry / packing / distance'),
(r'^(camshape|catmix|chain|gasoil|glider|lnts|methanol|pinene|popdynm|rocket|parabol|dtoc|optcdeg|junkturn|trainf|cont6|hvycrash|truck|lukvle)','discretized optimal control (COPS etc.)'),
(r'^ex[0-9]','GlobalLib ex*'),
(r'^arki','arki (ARKI consulting)'),
(r'^(ann_|kan_|kriging)','ML surrogate (ANN tanh / KAN / kriging)'),
(r'^(chp_|super3t)','CHP / power plant operation'),
(r'^(unitcommit|hydroenergy|gams02|gams04)','unit commitment / energy scheduling'),
(r'^(topopt)','topology optimization'),
(r'^(tls|tln)','trim loss'),
(r'^(portfol|kport|saa_|worst|hhfair)','portfolio / finance'),
(r'^(hadamard)','hadamard'),
]
def family(n):
    for rx,f in FAM:
        if re.search(rx,n): return f
    return 'misc'
