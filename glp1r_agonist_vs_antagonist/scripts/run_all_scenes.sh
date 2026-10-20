#!/bin/bash
cd "$(dirname "$0")"
for s in scene_a2 scene_b scene_c scene_d scene_e scene_f; do
  echo "== $s"; python3 $s.py 2>&1 | grep -v Warning | tail -3
done
echo ALLDONE
