#!/usr/bin/env python3
import sys
import re

for line in sys.stdin:
    line = line.strip().lower()
    words = re.findall(r'[a-z0-9]+', line)
    for word in words:
        print(f"{word}\t1")

