#!/usr/bin/env bash
set -e
echo "[+] Reset AI learned signatures"
echo "[]" > controller/data/learned_signatures.json
echo "[]" > controller/data/static_known_rules.json
echo "[+] Done"
