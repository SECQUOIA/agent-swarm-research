#!/bin/bash
# Print title, authors, date, and abstract for arXiv ids from the abs pages.
for id in "$@"; do
  curl -s -m 60 -L "https://arxiv.org/abs/$id" | python3 -c "
import sys,re,html
s=sys.stdin.read()
def m(p):
    r=re.search(p,s,re.S); return html.unescape(' '.join(r.group(1).split())) if r else '?'
print('==', '$id', m(r'<meta name=\"citation_title\" content=\"(.*?)\"'))
au=re.findall(r'<meta name=\"citation_author\" content=\"(.*?)\"',s)
print('   ', '; '.join(au[:6]), '|', m(r'<meta name=\"citation_date\" content=\"(.*?)\"'))
print('   ', m(r'<meta name=\"citation_abstract\" content=\"(.*?)\"'))
print()"
  sleep 1
done
