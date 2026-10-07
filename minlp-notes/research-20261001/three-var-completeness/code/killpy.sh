#!/bin/bash
# kill python processes whose script name matches $1 (avoids matching this shell)
ps -eo pid,args | awk -v pat="$1" '$2 ~ /python/ && $3 ~ pat {print $1}' | xargs -r kill
