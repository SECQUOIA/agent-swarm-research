"""Query the arXiv API and print date, id, title (and optionally abstract)."""
import re, sys, urllib.parse, subprocess, html

def query(q, n=40, abstracts=False):
    url = ("https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(q)
           + f"&start=0&max_results={n}&sortBy=submittedDate&sortOrder=descending")
    import time
    s = ""
    for k in range(6):
        s = subprocess.run(["curl", "-s", "-m", "60", "-L", url], capture_output=True, text=True).stdout
        if "<feed" in s:
            break
        time.sleep(10 * (k + 1))
    if "<feed" not in s:
        print("QUERY FAILED:", q)
    for e in s.split("<entry>")[1:]:
        t = " ".join(re.search(r"<title>(.*?)</title>", e, re.S).group(1).split())
        i = re.search(r"<id>(.*?)</id>", e).group(1).split("/abs/")[-1]
        d = re.search(r"<published>(.*?)</published>", e).group(1)[:10]
        a = [x.strip() for x in re.findall(r"<name>(.*?)</name>", e)]
        print(d, i, "|", html.unescape(t)[:140], "|", ", ".join(a[:4]))
        if abstracts:
            ab = " ".join(re.search(r"<summary>(.*?)</summary>", e, re.S).group(1).split())
            print("   ", html.unescape(ab)[:900])

if __name__ == "__main__":
    ab = "-a" in sys.argv
    args = [x for x in sys.argv[1:] if x != "-a"]
    query(args[0], int(args[1]) if len(args) > 1 else 40, ab)
