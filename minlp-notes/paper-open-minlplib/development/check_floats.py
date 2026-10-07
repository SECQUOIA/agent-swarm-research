#!/usr/bin/env python3
"""Layout check for clipped floats (round-1 item G7-03).

LaTeX gives no warning when a sideways table or a wide float runs off the
page, and pdftotext does not reliably extract rotated captions. This script
renders every page of build/main.pdf and build/supplement.pdf at 40 dpi into a
temporary folder and reports each page with ink closer than MARGIN_MM to an
edge of the paper (the text block keeps 25 mm, the page number about 15 mm).
It also checks that the main PDF names all 31 closures (the rows of Table 2).

Usage, from paper-open-minlplib/ after `make`:
    python3 development/check_floats.py
Needs pdftoppm and pdftotext (poppler) and Python with Pillow. Exit status 1
if a page is flagged or a closure name is missing. Inspect flagged pages and
every page with a sideways table or longtable by eye as well.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

DPI = 40
MARGIN_MM = 10.0
P = Path(__file__).resolve().parent.parent
CLOSURES = ['lnts50', 'lnts100', 'lnts200', 'lnts400', 'dtoc5', 'optcdeg2', 'lukvle10', 'chain50', 'chain100',
            'chain200', 'chain400', 'catmix100', 'catmix200', 'catmix400', 'catmix800', 'camshape100',
            'camshape200', 'camshape400', 'camshape800', 'ex6_2_5', 'ex6_2_7', 'pricing050', 'etamac', 'pindyck',
            'powerflow0030p', 'powerflow0039p', 'powerflow0039r', 'hvycrash', 'eg_int_s', 'eg_disc_s', 'eg_disc2_s']


def flagged_pages(pdf):
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['pdftoppm', '-r', str(DPI), '-gray', '-png', str(pdf), f'{tmp}/p'], check=True)
        for f in sorted(Path(tmp).glob('p-*.png'), key=lambda x: int(x.stem.split('-')[1])):
            im = Image.open(f).convert('L')
            w, h = im.size
            px = im.load()
            cols = [x for x in range(w) if any(px[x, y] < 200 for y in range(h))]
            rows = [y for y in range(h) if any(px[x, y] < 200 for x in range(w))]
            if not cols:
                continue
            mm = 25.4 / DPI
            gaps = dict(left=min(cols) * mm, right=(w - 1 - max(cols)) * mm,
                        top=min(rows) * mm, bottom=(h - 1 - max(rows)) * mm)
            close = {k: round(v, 1) for k, v in gaps.items() if v < MARGIN_MM}
            if close:
                out.append((int(f.stem.split('-')[1]), close))
    return out


def main():
    bad = 0
    for name in ('main', 'supplement'):
        pdf = P / 'build' / f'{name}.pdf'
        flags = flagged_pages(pdf)
        for page, close in flags:
            print(f'{name}.pdf page {page}: ink within {MARGIN_MM} mm of the edge {close}')
        print(f'{name}.pdf: {len(flags)} flagged page(s)')
        bad += len(flags)
    text = subprocess.run(['pdftotext', str(P / 'build' / 'main.pdf'), '-'], check=True,
                          capture_output=True, text=True).stdout
    missing = [n for n in CLOSURES if n not in text]
    print(f'main.pdf: {31 - len(missing)} of 31 closure names found' + (f'; missing {missing}' if missing else ''))
    return 1 if bad or missing else 0


if __name__ == '__main__':
    sys.exit(main())
