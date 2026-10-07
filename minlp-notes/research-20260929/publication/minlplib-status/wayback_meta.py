"""Part B: download archived MINLPLib metadata (statistics CSV, instance
listings, change logs) from the Internet Archive, sequentially with a delay
of at least 1 s; retries with a longer pause if the archive refuses.

Usage: python3 wayback_meta.py
"""
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "pages", "wayback", "meta")
UA = "minlp-notes MINLPLib history check (sequential, 1 req/s)"
GW = "http://www.gamsworld.org:80/minlp/minlplib2/"
ML = "http://www.minlplib.org:80/"
SPECS = [
    ("20160308235739", GW + "instancedata.csv", "gw_instancedata_20160308.csv"),
    ("20171114234214", GW + "instancedata.csv", "gw_instancedata_20171114.csv"),
    ("20190623060413", ML + "instancedata.csv", "ml_instancedata_20190623.csv"),
    ("20191021211413", ML + "instancedata.csv", "ml_instancedata_20191021.csv"),
    ("20200219193207", ML + "instancedata.csv", "ml_instancedata_20200219.csv"),
    ("20240315154357", "https://www.minlplib.org/instancedata.csv", "ml_instancedata_20240315.csv"),
    ("20241114095424", "http://www.minlplib.org/instancedata.csv", "ml_instancedata_20241114.csv"),
    ("20141209130957", GW + "html/instances.html", "gw_instances_20141209.html"),
    ("20150608015753", GW + "html/instances.html", "gw_instances_20150608.html"),
    ("20160307053446", GW + "html/instances.html", "gw_instances_20160307.html"),
    ("20171114234204", GW + "html/instances.html", "gw_instances_20171114.html"),
    ("20141209130938", GW + "html/allinstancedata.html", "gw_allinstancedata_20141209.html"),
    ("20150608015733", GW + "html/allinstancedata.html", "gw_allinstancedata_20150608.html"),
    ("20141209130952", GW + "html/dates.html", "gw_dates_20141209.html"),
    ("20171114234159", GW + "html/dates.html", "gw_dates_20171114.html"),
    ("20190623060513", ML + "minlplib.solu", "ml_solu_20190623.solu"),
    ("20200219193404", ML + "minlplib.solu", "ml_solu_20200219.solu"),
    ("20220119050949", "http://www.minlplib.org/minlplib.solu", "ml_solu_20220119.solu"),
]


def get(ts, url, path):
    for attempt in range(4):
        p = subprocess.run(["curl", "-s", "-L", "-m", "300", "-A", UA, "-w", "%{http_code}", "-o", path,
                            f"http://web.archive.org/web/{ts}id_/{url}"], capture_output=True, text=True)
        code = p.stdout.strip()
        if p.returncode == 0 and code == "200":
            return code
        time.sleep(10 * (attempt + 1))
    return f"failed rc={p.returncode} http={code}"


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for ts, url, name in SPECS:
        path = os.path.join(OUT, name)
        if os.path.exists(path) and os.path.getsize(path) > 0:
            continue
        r = get(ts, url, path)
        print(name, r, os.path.getsize(path) if os.path.exists(path) else 0, flush=True)
        time.sleep(1.5)
