#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
echo "ATLAS Super Calculator: http://127.0.0.1:8765"
python3 -m http.server 8765 --bind 127.0.0.1
