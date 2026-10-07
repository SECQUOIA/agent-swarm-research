"""Compare arXiv @misc entries of references.bib with the arXiv API (title, first author, version)."""
import re, urllib.request
bib = open('references.bib').read()
ents = []
for m in re.finditer(r'@misc\{([^,]+),(.*?)\n\}', bib, re.S):
    key, body = m.groups()
    hp = re.search(r'howpublished\s*=\s*\{arXiv:([0-9.]+)(v\d+)?\}', body)
    ti = re.search(r'title\s*=\s*\{(.*?)\}\s*,\s*$', body, re.M | re.S)
    au = re.search(r'author\s*=\s*\{(.*?)\}\s*,\s*$', body, re.M | re.S)
    if hp:
        ents.append((key, hp.group(1), hp.group(2), ti.group(1), au.group(1)))
ids = ','.join(e[1] for e in ents)
url = 'https://export.arxiv.org/api/query?id_list=' + ids + '&max_results=50'
t = urllib.request.urlopen(url, timeout=60).read().decode()
rec = {}
for e in re.findall(r'<entry>(.*?)</entry>', t, re.S):
    i = re.search(r'<id>http://arxiv.org/abs/([0-9.]+)(v\d+)</id>', e)
    rec[i.group(1)] = (i.group(2), re.sub(r'\s+', ' ', re.search(r'<title>(.*?)</title>', e, re.S).group(1)),
                       re.findall(r'<name>(.*?)</name>', e))
norm = lambda s: re.sub(r'[^a-z0-9]', '', re.sub(r'\\[a-z]+|[{}]', '', s.lower()))
for key, aid, ver, ti, au in ents:
    v, t2, a2 = rec.get(aid, (None, '', []))
    ok_t = norm(ti) == norm(t2)
    fa = au.split(' and ')[0].split(',')[0].strip()
    ok_a = bool(a2) and norm(fa) in norm(a2[0])
    print(f'{key}: arXiv:{aid}{ver or ""} latest={v} title_ok={ok_t} first_author_ok={ok_a}' + ('' if ok_t else f' | bib="{ti}" arXiv="{t2}"'))
