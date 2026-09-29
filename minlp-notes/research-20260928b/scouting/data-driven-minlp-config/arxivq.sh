#!/bin/bash
# usage: arxivq.sh 'query' [max]   (arXiv API search_query syntax, spaces as +)
curl -s -m 90 "https://export.arxiv.org/api/query?search_query=$1&max_results=${2:-25}&sortBy=relevance" | python3 -c "
import sys, re
t = sys.stdin.read()
for e in re.findall(r'<entry>(.*?)</entry>', t, re.S):
    i = re.search(r'<id>(.*?)</id>', e).group(1).split('/abs/')[-1]
    ti = ' '.join(re.search(r'<title>(.*?)</title>', e, re.S).group(1).split())
    d = re.search(r'<published>(.*?)</published>', e).group(1)[:10]
    print(d, i, ti)
"
