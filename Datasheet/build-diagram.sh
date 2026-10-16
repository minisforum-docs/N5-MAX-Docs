#!/bin/sh
# Rebuild the N5 MAX interface block diagram.
#
# Step 1 regenerates N5-MAX-Block-Diagram.svg from the Python source
#        (standard library only, no dependencies).
# Step 2 rasterizes the SVG to N5-MAX-Block-Diagram.png with headless
#        Chromium. Any SVG rasterizer works for step 2 (rsvg-convert,
#        inkscape, ...); Chromium is used here because it is available on
#        the machines this repository is maintained on.
#
# The window size must match CANVAS_W x CANVAS_H in the Python source
# (2040 x 892 at the time of writing); --force-device-scale-factor=2 gives
# the 2x PNG resolution (4080 x 1784).
set -eu
cd "$(dirname "$0")"

python3 N5-MAX-Block-Diagram.py > N5-MAX-Block-Diagram.svg

BROWSER="${BROWSER:-chromium-browser}"
"$BROWSER" --headless=new --disable-gpu --hide-scrollbars \
    --window-size=2040,892 --force-device-scale-factor=2 \
    --screenshot="$PWD/N5-MAX-Block-Diagram.png" \
    "file://$PWD/N5-MAX-Block-Diagram.svg"

echo "Rebuilt: N5-MAX-Block-Diagram.svg + N5-MAX-Block-Diagram.png"
