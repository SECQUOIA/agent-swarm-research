"""Search arXiv via the HTML search page; print id | title | submitted date."""
import re, sys, html, subprocess, urllib.parse, time

def search(q, size=50):
    url = ("https://arxiv.org/search/?query=" + urllib.parse.quote_plus(q)
           + f"&searchtype=all&order=-announced_date_first&size={size}")
    s = subprocess.run(["curl", "-s", "-m", "60", "-L", "-A", "Mozilla/5.0", url],
                       capture_output=True, text=True).stdout
    items = s.split('<li class="arxiv-result">')[1:]
    if not items:
        print("  (no results or failed)")
    for li in items:
        i = re.search(r'arxiv.org/abs/([\w.]+)', li).group(1)
        t = " ".join(re.sub("<.*?>", "", re.search(r'<p class="title is-5 mathjax">(.*?)</p>', li, re.S).group(1)).split())
        d = re.search(r'Submitted</span>\s*(.*?);', li, re.S)
        au = re.findall(r'<a href="/a/[^"]*">(.*?)</a>', li)
        print(" ", i, "|", html.unescape(t)[:140], "|", ", ".join(au[:3]), "|", d.group(1).strip() if d else "")

if __name__ == "__main__":
    for q in sys.argv[1:]:
        print("###", q)
        search(q)
        time.sleep(2)
