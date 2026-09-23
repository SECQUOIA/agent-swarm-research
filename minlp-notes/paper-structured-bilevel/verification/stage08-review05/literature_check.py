import re,requests,json,concurrent.futures,pathlib
text=pathlib.Path('references.bib').read_text();entries=re.split(r'(?=@\w+\{)',text)[1:]
def check(e):
 key=re.match(r'@\w+\{([^,]+)',e)[1];m=re.search(r'doi=\{([^}]+)',e)
 if not m:return {'key':key,'doi':None}
 doi=m[1]
 try:
  r=requests.get('https://api.crossref.org/works/'+doi,timeout=25);r.raise_for_status();a=r.json()['message'];return dict(key=key,doi=doi,title=a.get('title'),author=a.get('author'),year=a.get('published'),volume=a.get('volume'),issue=a.get('issue'),page=a.get('page'),article_number=a.get('article-number'))
 except Exception as er:return dict(key=key,doi=doi,error=str(er))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:a=list(ex.map(check,entries))
pathlib.Path('bibliography-crossref.json').write_text(json.dumps(a,indent=2))
for d in a:print(d['key'],d.get('title'),d.get('year'),d.get('volume'),d.get('page'),d.get('article_number'),d.get('error',''))
