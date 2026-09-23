#!/usr/bin/env bash
# Build only current sources in a fresh directory, then deliver the PDF and bbl.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
paper_build_dir=$(mktemp -d "${TMPDIR:-/tmp}/certified-minlp-paper-build.XXXXXX")
trap 'rm -rf "$paper_build_dir"' EXIT
cp main.tex references.bib "$paper_build_dir/"
cp -R sections tables "$paper_build_dir/"
mkdir -p build
(
  cd "$paper_build_dir"
  latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
) > build/current-build.log 2>&1
cp "$paper_build_dir/main.pdf" main.pdf
cp "$paper_build_dir/main.bbl" main.bbl
cp "$paper_build_dir/main.log" build/current-main.log
printf '%s\n' 'Built main.pdf and main.bbl from a fresh source directory.'
