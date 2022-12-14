#!/usr/bin/env bash

PANDOC_DATA_DIR="${PANDOC_DATA_DIR:-build/pandoc}"

pandoc --verbose \
  --data-dir="$PANDOC_DATA_DIR" \
  --defaults=input.yaml

python build/update_manuscript.py
