#!/usr/bin/env python3
"""Build the paper's claim index from saved evidence; never run scientific scripts.

The claim register of the supplement (Section S7.3, sections/I-reproduction.tex) gives for each
row the paper labels, the instances and the last column (tier; level; status; trust).
artifact/RUNS.md gives for the same rows, matched by row number, the statement, the checker paths,
the command, the expected output, the recorded time and the folders of run records.
data/numbers.json gives the displayed values."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re

P = 'paper-open-minlplib'
R = 'research-20260929'
N = P + '/data/numbers.json'
GUIDE = P + '/sections/I-reproduction.tex'
RUNS = P + '/artifact/RUNS.md'
REP = R + '/publication/reproduction/'
# verification_label of each status word (Section 2.6 of the paper); 'weaker second' and
# 'partial second' mean proved, with a separately written implementation that certifies a weaker
# bound or part of the domain.  RANK orders the labels from weakest to strongest.
LABEL = {'verified': 'verified by a separately written implementation', 'proved': 'proved',
         'weaker second': 'proved', 'partial second': 'proved',
         'floating-point output': 'floating-point output'}
RANK = ['floating-point output', 'proved', 'verified by a separately written implementation']
# Families whose GAMS and OSIL forms tab:sem-gams (sections/A-semantics.tex) compares only at sample
# points.  A returned point of the one-hour runs (GAMS files) on these instances is shown not exactly
# feasible only if the two forms define the same model (app:solvers-points, sections/H-solvers.tex).
SAMPLED_GAMS = ('lnts', 'lukvle10', 'chain', 'ann_cumene_tanh', 'kan_', 'ex6_2_5', 'ex6_2_7',
                'pricing050', 'etamac', 'pindyck', 'hvycrash')
SAMPLED_QUALIFIER = ('assumes that the GAMS form of the one-hour runs and the OSIL form define the same model; '
                     'tab:sem-gams compares them only at sample points (app:solvers-points)')


def plain(s):
    s = s.replace('\\,', ' ').replace('~', ' ').replace('\\_', '_').replace('\\\\', '')
    s = re.sub(r'\\(?:Cref|cref|nolinkurl|inst|texttt|evid|trust)\{([^{}]*)\}', r'\1', s)
    return re.sub(r'\s+', ' ', s).strip()


def status_words(cell, names):
    """Split a status field such as 'verified (eg_disc2_s: partial second)' into the row's base
    word, one word per instance and one word per named component.  A parenthesis without a colon
    qualifies the whole row.  If the part before the colon lists instances of the row, the word
    applies to them; otherwise it names a component of the row's result, as in
    'verified (emfl enclosures: weaker second)'."""
    status = plain(cell)
    base = status.split('(')[0].strip()
    if base not in LABEL:
        raise ValueError('unknown status in the register: ' + cell)
    words = {n: base for n in names}
    components = {}
    m = re.search(r'\(([^()]*)\)', status)
    if m and ':' in m.group(1):
        who, word = (x.strip() for x in m.group(1).split(':', 1))
        if word not in LABEL:
            raise ValueError('unknown status in the register: ' + cell)
        listed = [x.strip() for x in who.split(',')]
        if all(name in words for name in listed):
            for name in listed:
                words[name] = word
        elif any(name in words for name in listed):
            raise ValueError(f'status mixes instances and other names: {who}')
        else:
            components[who] = word
    return status, base, words, components


def register_rows(text):
    raw = text.split('\\endhead', 1)[1].split('\\end{longtable}', 1)[0]
    rows = []
    for row in (x.strip() for x in re.split(r'\\\\\s*\n', raw) if ' &\n' in x):
        cols = row.split(' &\n')
        assert len(cols) == 4, cols
        rows.append(cols)
    return rows


def runs_blocks(text):
    """Blocks '### Rnn. statement' with fields '- Name: value' (continuation lines indented)."""
    blocks = []
    for m in re.finditer(r'^### R(\d\d)\. (.+?)\n(.*?)(?=^### |^## |\Z)', text, re.M | re.S):
        fields, key = {}, None
        for line in m.group(3).splitlines():
            f = re.match(r'^- ([A-Z][a-z]+(?: [a-z]+)?): (.*)$', line)
            if f:
                key = f.group(1); fields[key] = f.group(2).strip()
            elif key and line.startswith('  ') and line.strip():
                fields[key] += ' ' + line.strip()
        blocks.append({'row': int(m.group(1)), 'statement': m.group(2).strip(), **fields})
    return blocks


def ticks(s):
    return re.findall(r'`([^`]+)`', s)


def walk(x):
    if isinstance(x, dict):
        for v in x.values(): yield from walk(v)
    elif isinstance(x, list):
        for v in x: yield from walk(v)
    elif isinstance(x, str): yield x


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo-root', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    root = args.repo_root.resolve()
    numbers = json.loads((root / N).read_text())
    resultmap = json.loads((root / (REP + 'result-map.json')).read_text())
    auditmap = json.loads((root / (REP + 'audit-map.json')).read_text())
    commands = json.loads((root / (REP + 'commands.json')).read_text())
    rows = register_rows((root / GUIDE).read_text())
    blocks = runs_blocks((root / RUNS).read_text())
    assert len(rows) == 27 and [b['row'] for b in blocks] == list(range(1, 28)), \
        (len(rows), [b['row'] for b in blocks])
    # The waterno2 and KAN sections add keys to the full instance entries; they must not replace
    # them, or the bounds of these instances would be lost.
    allmodels = {k: dict(v) for k, v in numbers['instances'].items()}
    for src in (numbers['waterno2'], numbers['kan']):
        for k, v in src.items():
            allmodels[k] = {**allmodels.get(k, {}), **v}
    allmodels['ann_cumene_tanh'] = {**allmodels.get('ann_cumene_tanh', {}), **numbers['ann']}
    known = set(allmodels) | {m['instance'] for m in auditmap if m.get('instance')}
    cache = {}
    unresolved = []

    def artifact(rel):
        if rel not in cache:
            f = root / rel
            assert f.is_file(), rel
            h = hashlib.sha256()
            with f.open('rb') as stream:
                for b in iter(lambda: stream.read(1024*1024), b''): h.update(b)
            cache[rel] = h.hexdigest()
        return {'path': rel, 'sha256': cache[rel]}

    def sources(data):
        found = set()
        for text in walk(data):
            for rel in re.findall(r'(?:paper-open-minlplib|research-20260929)/[^\s;,)\]}\"]+', text):
                rel = rel.split(':', 1)[0].rstrip('.')
                if (root / rel).is_file(): found.add(rel)
        return found

    def map_paths(data):
        paths = set()
        def visit(x):
            if isinstance(x, dict):
                if 'path' in x:
                    rel = x['path']
                    if rel.startswith('~/.cache/minlplib/minlplib/osil/'):
                        rel = allmodels[Path(rel).stem]['size']['osil']
                    if not rel.startswith((R+'/', P+'/')): rel = R+'/'+rel
                    if (root/rel).is_file(): paths.add(rel)
                    else: unresolved.append(rel)
                for v in x.values(): visit(v)
            elif isinstance(x, list):
                for v in x: visit(v)
        visit(data)
        return paths

    def expand(token):
        return token.replace('$R', R, 1) if token.startswith('$R') else token.replace('$P', P, 1)

    def checker_paths(text):
        """Paths in backticks; a folder contributes its Python files, and a bare name lies in the
        folder of the preceding path."""
        found = set(); parent = None
        for token in ticks(text):
            if token.startswith(('$R/', '$P/')):
                rel = expand(token).rstrip('/')
                if (root/rel).is_dir():
                    parent = rel; found.update(str(p.relative_to(root)) for p in (root/rel).glob('*.py'))
                elif (root/rel).is_file():
                    found.add(rel); parent = str(Path(rel).parent)
            elif parent and re.fullmatch(r'[\w.\-]+(?:/[\w.\-]+)*', token) and (root/parent/token).is_file():
                found.add(parent + '/' + token)
        return found

    def record_paths(text):
        """Folders and files of run records; a folder contributes every file below it."""
        found = set()
        for token in ticks(text):
            if not token.startswith(('$R/', '$P/')):
                continue
            rel = expand(token).rstrip('/')
            assert (root/rel).exists(), token
            if (root/rel).is_dir():
                found.update(str(f.relative_to(root)) for f in (root/rel).rglob('*')
                             if f.is_file() and '__pycache__' not in f.parts and f.suffix != '.pyc')
            else:
                found.add(rel)
        return found

    def scripts_of(command):
        """Repository paths of the Python scripts that a recorded command runs."""
        cwd = command.get('cwd') or ''
        base = expand(cwd) if cwd.startswith(('$R', '$P')) else None
        found = set()
        for tok in re.findall(r'[^\s"\'=;&|()]+\.py\b', command.get('command', '')):
            if tok.startswith(('$R/', '$P/')): found.add(expand(tok))
            elif base and not tok.startswith(('/', '$', '~')): found.add(os.path.normpath(base + '/' + tok))
        return found

    def mentions(command, names):
        # Instance names in the command or its id; the water audit's ids write waterno2_06 as w06.
        text = command.get('command', '') + ' ' + re.sub(r'(?<![\w])w(\d\d)_', r'waterno2_\1 ', command.get('id', ''))
        return {n for n in names if re.search(r'(?<![\w-])' + re.escape(n) + r'(?![\w-])', text)}

    def values(names):
        out = {}
        for name in names:
            d = allmodels[name]
            out[name] = {k: d[k] for k in ('L', 'U', 'gap_abs', 'gap_rel', 'status', 'certificate') if k in d}
            if 'size' in d: out[name]['osil_sha256'] = d['size'].get('osil_sha256')
        return out

    claims = []
    for i, ((result, check, wall, trust), block) in enumerate(zip(rows, blocks), 1):
        assert block['row'] == i
        labels = []
        for group in re.findall(r'\\[Cc]ref\{([^}]+)\}', result): labels.extend(group.split(','))
        run_labels = ticks(block['Labels'])
        assert labels == run_labels, (i, labels, run_labels)
        names = re.findall(r'\\inst\{([^}]+)\}', result)
        if '--' in result and names:
            family = re.sub(r'\d+$', '', names[0])
            if family in ('lnts', 'chain', 'catmix', 'camshape'): names = [n for n in allmodels if n.startswith(family)]
            elif family == 'waterno2_': names = [n for n in allmodels if n.startswith(family) and n != 'waterno2_06']
        if 'six KAN' in result: names = list(numbers['kan'])
        if 'sec:points' in labels: names = list(numbers['instances'])
        names = [n for n in names if n in allmodels]
        paths = {N, GUIDE, RUNS, REP+'README.md', REP+'commands.json', REP+'result-map.json'}
        checkers = checker_paths(block['Checkers'])
        paths |= checkers | record_paths(block.get('Records', ''))
        display = values(names)
        paths |= sources(display)
        # The points row covers every instance but none of their certificate maps.
        selected = [] if 'sec:points' in labels else [m for m in resultmap if m.get('instance') in names]
        for m in selected: paths |= map_paths(m)
        for name in names:
            size = allmodels[name].get('size', {})
            if size.get('osil'): paths.add(size['osil'])
        extra = {}
        if 'thm:eg-bounds' in labels:
            extra = numbers['eg_audit']; paths |= sources(extra)
        if 'sec:points' in labels:
            paths |= sources(display)
        if 'prop:audit-refute' in labels or 'prop:spring-opt' in labels:
            extra = numbers['audit']; paths.add(REP+'audit-map.json')
            for m in auditmap: paths |= map_paths(m)
        if 'prop:spring-opt' in labels:
            spring = R+'/publication/audit-ir/logs/spring_global.json'
            extra = dict(extra, spring=json.loads((root/spring).read_text()))
            paths.add(spring)
        if 'prop:scip-witnesses' in labels:
            # Preserve the actual statements directly from LaTeX.
            extra = {}
            for source in sorted((root/P/'sections').glob('*.tex')):
                text = source.read_text()
                for label in labels:
                    if '\\label{'+label+'}' in text:
                        begin = text.rfind('\\begin{', 0, text.index('\\label{'+label+'}'))
                        end = text.index('\\end{', text.index('\\label{'+label+'}'))
                        extra[label] = text[begin:end]
                        paths.add(str(source.relative_to(root)))
            paths.update(str(f.relative_to(root)) for f in (root/R/'publication/scip-bug').rglob('*')
                         if f.is_file() and f.suffix in ('.py', '.json', '.cip', '.sol', '.log', '.md'))
        if 'tab:claims' in labels:
            extra = numbers['claims_table']; paths |= sources(extra)
            paths |= {P+'/tables/tab-claims.tex', P+'/tables/tab-claims-campaign.tex'}
        if 'tab:solvers' in labels:
            extra = numbers['campaign']; paths |= sources(extra)
            paths |= {P+'/tables/tab-solvers.tex', P+'/tables/tab-claims-campaign.tex'}
        if 'app:displays' in labels:
            extra = numbers['headline']; paths.update(numbers['sources'])
            paths |= {P+'/data/make_tables.py', P+'/data/check.log'}
        fields = [f.strip() for f in trust.split(';')]
        assert len(fields) >= 4, (i, trust)
        status, base, words, components = status_words(fields[2], names)
        by_instance = {n: LABEL[w] for n, w in words.items()}
        by_component = {c: LABEL[w] for c, w in components.items()}
        level = min([LABEL[base]] + list(by_instance.values()) + list(by_component.values()), key=RANK.index)
        tags = ['read', 'code', 'thm'] + re.findall(r'\\trust\{([^}]+)\}', trust)
        if 'thm:eg-bounds' in labels: tags += ['recorded-exp-power-audit']
        historical = [{'cwd': m.get('cwd'), 'command': m.get('command')} for m in selected if m.get('command')]
        # Recorded commands of the earlier package that run one of this row's checkers, matched by
        # full path (working folder plus script); a command that names instances, none of them
        # this row's, belongs to another row.
        scripts = {p for p in checkers if p.endswith('.py')}
        related = [{k: c[k] for k in ('id', 'cwd', 'command', 'exit', 'wall_s', 'expected') if k in c}
                   for c in commands if scripts_of(c) & scripts
                   and not (names and mentions(c, known) and not mentions(c, names))]
        command = ticks(block['Command'])[0]
        key_line = block['Expected output']
        local_lines = {'thm:lnts-opt': 'lnts.log', 'thm:kan-enclosure': 'kan_audit.log'}
        for label, log in local_lines.items():
            saved = root/P/'artifact/logs/corrected'/log
            if label in labels and saved.is_file(): key_line = saved.read_text().splitlines()[-1]
        if 'thm:dtoc5-bracket' in labels: key_line = 'PASS; seconds <elapsed>'
        if 'thm:eg-bounds' in labels: key_line = numbers['eg_audit']['compare_log_last_line']
        if 'app:displays' in labels: key_line = 'exit status 0; data/check.log records all directed-display checks'
        entry = {'claim_id': f'register-{i:02d}', 'statement': block['statement'] + '.',
                 'paper_label': labels[0], 'paper_labels': labels, 'register_row': i, 'instances': names,
                 'displayed_values': display or extra, 'additional_values': extra if display else {},
                 'artifacts': [artifact(p) for p in sorted(paths)], 'checker_command': command,
                 'checker_recipe': block['Checkers'], 'register_checkers_latex': check,
                 'historical_commands': historical,
                 'expected_output': block['Expected output'], 'expected_output_key_line': key_line,
                 'recorded_wall_time': block['Recorded time'], 'register_time': plain(wall),
                 'recorded_commands': related, 'verification_label': level, 'status': status,
                 'status_by_instance': words, 'verification_label_by_instance': by_instance,
                 'evidence_level': re.findall(r'\\evid\{([^}]+)\}', trust),
                 'trust_tags': sorted(set(tags)), 'trust_qualifiers': plain(trust)}
        if components:
            entry['status_by_component'] = components
            entry['verification_label_by_component'] = by_component
        if 'Note' in block: entry['note'] = block['Note']
        claims.append(entry)
    by_label = {e['paper_label']: e for e in claims}
    for i, c in enumerate(numbers['claims_table']):
        name = c['model'].split(' ')[0]
        if name.startswith('QPLIB_'):
            name = 'camshape800' if name == 'QPLIB_3177' else 'camshape100'
        # Certificate rows (register rows 1-20) that hold the instance; else the audit or claims row.
        base = [e for e in claims[:20] if name in e.get('instances', [])]
        if not base: base = [by_label['prop:spring-opt']] if name.startswith('emfl') else [by_label['prop:baron-camshape']]
        paths = {N, P+'/tables/tab-claims.tex', P+'/tables/tab-claims-campaign.tex'} | sources(c)
        for e in base: paths.update(x['path'] for x in e['artifacts'])
        paths |= {R+'/bound-audit/pages.json', P+'/data/make_tables.py'}
        labels = ['tab:claims-campaign'] if c['group'] == 'campaign' else ['tab:claims']
        # What the displayed value is (numbers.json 'evaluation'; round-3 review sol-status 4): a number
        # printed by its source, an exact evaluation of the objective at a listed point, or an ordinary
        # high-precision evaluation without an enclosure. Only the comparison of numbers is proved by the
        # display checker; for the one-hour points the returned objective value of the trace file is
        # also compared exactly, which proves that the point is not exactly feasible; on SAMPLED_GAMS
        # instances this assumes the GAMS/OSIL correspondence (round-3 final verification R1).
        kind = c.get('evaluation', 'none')
        qualifiers = [c['qualifier']] if c.get('qualifier') else []
        sampled = c['group'] == 'campaign' and name.startswith(SAMPLED_GAMS)
        if sampled: qualifiers.append(SAMPLED_QUALIFIER)
        if kind == 'numerical' and c['group'] == 'campaign':
            label, status = 'proved', ('proved: exact comparison with a certified bound of the returned objective value '
                                       'of the trace file (returned_value), so the returned point is not exactly feasible'
                                       + (' (under the assumption in trust_qualifiers)' if sampled else '') + '; '
                                       'the displayed value is an ordinary 50-digit evaluation at the point (computed); '
                                       'one display checker')
        elif kind == 'numerical':
            label, status = 'computed', ('computed: the displayed value is an ordinary evaluation of the objective at the point '
                                         'without an enclosure; its exact comparison with a certified bound (one display '
                                         'checker) is proved, the statement about the point is not')
        elif kind == 'exact':
            label, status = 'proved', ('proved: exact evaluation of the objective at the point (data_source) and exact '
                                       'comparison with a certified bound (one display checker)')
        else:
            label, status = 'proved', 'proved: exact comparison of the reported value with a certified bound (one display checker)'
        entry = {'claim_id': f'reported-{i+1:02d}', 'statement': f"{c['source']}: {c['model']} {c['claim']} lies {c['meaning']}.",
                 'paper_label': labels[0], 'paper_labels': labels, 'numbers_key': f'claims_table[{i}]',
                 'displayed_values': c, 'artifacts': [artifact(p) for p in sorted(paths)],
                 'checker_command': 'cd /tmp && python3 "$P/data/make_tables.py"',
                 'supporting_claim_ids': [e['claim_id'] for e in base],
                 'expected_output': f"Directed margin at least {c['margin']}; display checker exit status 0.",
                 'recorded_wall_time': 'about 5 s (display check); certificate times in supporting_claim_ids',
                 'verification_label': label, 'status': status, 'value_evaluation': kind,
                 'trust_tags': sorted(set(['read', 'code', 'thm', 'int'] + [t for e in base for t in e['trust_tags']])),
                 'trust_qualifiers': '; '.join(qualifiers),
                 'violation_verification_label': 'floating-point output' if c['group'] == 'campaign' else 'see data_source and qualifier'}
        claims.append(entry)
    doc = {'schema_version': 2,
           'description': 'One entry per reproduction-register row plus one per distinct reported-value claim in numbers.json; repeated campaign rows are not duplicated.',
           'root': 'repository root', 'numbers_file': N, 'register_file': GUIDE, 'runs_file': RUNS,
           'verification_note': 'status_by_instance gives the status word of each instance of a register row (Section 2.6; parenthetical exceptions of the status field apply to the instances they name), and status_by_component the word of a named part of the result (for example the emfl enclosures of register-23). verification_label_by_instance and verification_label_by_component map them: verified -> verified by a separately written implementation; proved, weaker second, partial second -> proved; floating-point output for the campaign. A row\'s verification_label is the weakest of its instances, its components and its status word. Reported values: the comparison of the displayed number with the certified bound is exact; value_evaluation says whether the number is as reported (none), an exact evaluation at the point (exact) or an ordinary evaluation without an enclosure (numerical). A numerical value of a listed point makes the entry computed; for the one-hour points the exact comparison of the returned objective value of the trace file proves that the point is not exactly feasible (on instances whose GAMS and OSIL forms tab:sem-gams compares only at sample points, under the assumption stated in trust_qualifiers). Hash and label validation checks packaging, not mathematical correctness; other qualifications remain in trust_qualifiers.',
           'claim_count': len(claims), 'register_row_count': len(rows), 'reported_value_count': len(numbers['claims_table']),
           'unresolved_legacy_map_paths': sorted(set(unresolved)), 'claims': claims}
    args.output.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + '\n')
    print(f'BUILT {len(claims)} claims; {len(cache)} distinct artifacts; {len(set(unresolved))} unresolved legacy-map paths')


if __name__ == '__main__':
    main()
