#!/usr/bin/env python3
"""Generate the N5 MAX interface block diagram as SVG.

This script is the source of truth for Datasheet/N5-MAX-Block-Diagram.svg.
Standard library only: run it and redirect the output.

    python3 N5-MAX-Block-Diagram.py > N5-MAX-Block-Diagram.svg

Layout rules:
- A full-height SoC column in the middle; internal interfaces on the left,
  external interfaces on the right. Every link is straight and horizontal.
- The SoC is labelled with the platform name only ("Strix Halo"); core
  counts are the platform-supported maximum, not a specific SKU.
- Each link segment is labelled with the protocol it carries ("PCIe 4.0
  x1", "SATA 6 Gbps", ...); controller chips (JMB585, RTL8127, JHL9580)
  sit inline between the SoC and the final connector.
- A single interface is one plain box. Several interfaces of the SAME type
  are drawn as a stack (the box plus cascaded layer boxes behind it) with
  the count noted beside the stack. Interfaces of DIFFERENT types are
  always drawn separately; the two 10GbE ports each get their own row.

To adjust geometry, edit the CONFIG block; to change content, edit ROWS_L
and ROWS_R below. Coordinates are plain pixels on a fixed canvas.
"""

# ---------------------------------------------------------------- palette
BLACK = "#000000"
WHITE = "#ffffff"
GRAY_FILL, GRAY_STROKE = "#f0f0f0", "#666666"      # SoC frame
FRAME_FILL, FRAME_STROKE = "#fafafa", "#a0a0a0"    # side group frames
GREEN_FILL, GREEN_STROKE = "#d6e8d2", "#4a7a44"    # memory
BLUE_FILL, BLUE_STROKE = "#cce0f5", "#3a6ea5"      # controller chips
LAV_FILL, LAV_STROKE = "#d8c8e0", "#7a5a9a"        # USB4 v2
YEL_FILL, YEL_STROKE = "#fcefc0", "#b09030"        # USB

STYLE = {
    "white": (WHITE, BLACK),
    "green": (GREEN_FILL, GREEN_STROKE),
    "blue": (BLUE_FILL, BLUE_STROKE),
    "lav": (LAV_FILL, LAV_STROKE),
    "yel": (YEL_FILL, YEL_STROKE),
}

# --------------------------------------------------------------- geometry
EP_W = 250          # endpoint column width (outermost)
CT_W = 230          # controller column width
CPU_W = 300         # SoC column width
GAP = 175           # horizontal gap that carries the segment labels
BOX_H = 56          # device box height
YC0 = 164           # y of the first row centre
PITCH_L = 92        # left row pitch (8 rows -> span 644)
R_PITCH = 107       # right row pitch (7 rows, centred in the same span)
DX = 7              # cascade offset per stacked layer
FONT = 'font-family="DejaVu Sans, Arial, Helvetica, sans-serif"'

XL0, XL1 = 40, 40 + EP_W                 # left endpoint column   40..290
XC0, XC1 = XL1 + GAP, XL1 + GAP + CT_W   # left controller column 465..695
XU0, XU1 = XC1 + GAP, XC1 + GAP + CPU_W  # SoC column             870..1170
XR0, XR1 = XU1 + GAP, XU1 + GAP + CT_W   # right controller col   1345..1575
XE0, XE1 = XR1 + GAP, XR1 + GAP + EP_W   # right endpoint column  1750..2000

CPU_TOP, CPU_BOT = 96, 852
FRAME_TOP, FRAME_BOT = 108, 840
CANVAS_W = XE1 + 40          # computed: keep 40 px margin around everything
CANVAS_H = CPU_BOT + 40

# ------------------------------------------------------------------ rows
# Row tuples: (endpoint title, endpoint sub, style, controller or None,
#              label 1, label 2, stack count)
# Left rows: label 1 = endpoint->controller (or endpoint->SoC),
#            label 2 = controller->SoC.
ROWS_L = [
    ("LPDDR5X unified memory", "64 / 128 GB", "green", None,
     "LPDDR5X 256-bit", None, 1),
    ("HDD Bays", "3.5 / 2.5-inch SATA 3.0", "white",
     ("JMicron JMB585", "SATA controller", "blue"),
     "SATA 6 Gbps", "PCIe 3.0 x2", 5),
    ("M.2 Slot A (2280)", "fastest M.2 slot", "white", None,
     "PCIe 4.0 x4", None, 1),
    ("M.2 Slot B (2230/2280)", "system disk pre-installed", "white", None,
     "PCIe 4.0 x1", None, 1),
    ("M.2 Slot C (2280)", None, "white", None, "PCIe 4.0 x1", None, 1),
    ("M.2 Slot D (2280)", None, "white", None, "PCIe 4.0 x1", None, 1),
    ("M.2 Slot E (2280)", None, "white", None, "PCIe 4.0 x1", None, 1),
    ("Internal USB port", "USB 3.2 Gen1 Type-A", "yel", None,
     "USB 3.2 Gen1", None, 1),
]

# Right rows: label 1 = SoC->controller (or SoC->endpoint),
#             label 2 = controller->endpoint.
ROWS_R = [
    ("HDMI", "up to 8K@60 / 4K@144", "white", None, "HDMI 2.1 FRL", None, 1),
    ("10GbE RJ45", None, "white",
     ("Realtek RTL8127", "10GbE NIC", "blue"),
     "PCIe 4.0 x1", "10GbE", 1),
    ("10GbE RJ45", None, "white",
     ("Realtek RTL8127", "10GbE NIC", "blue"),
     "PCIe 4.0 x1", "10GbE", 1),
    ("USB4 v2 (rear)", "80 Gbps, Alt DP 2.0, PD 15 W", "lav",
     ("Intel JHL9580", "USB4 v2 controller", "lav"),
     "PCIe 4.0 x4", "USB4 v2", 2),
    ("USB4 (front)", "40 Gbps, Alt DP 2.0, PD 15 W", "lav", None,
     "USB4 40Gbps", None, 1),
    ("USB 3.2 Gen2", "Type-A, front + rear", "yel", None,
     "USB 3.2 Gen2", None, 2),
    ("USB 2.0 (rear)", "Type-A", "yel", None, "USB 2.0", None, 1),
]

CPU_LINES = [
    ("AMD Strix Halo", 22),
    ("CPU: up to 16 cores / 32 threads", 14),
    ("GPU: up to 40 CU Radeon graphics", 14),
    ("NPU: XDNA 2", 14),
]

# --------------------------------------------------------------- renderer
parts = []


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rect(x, y, w, h, fill, stroke, sw=1.2):
    parts.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def text(x, y, s, size=16, anchor="middle", fill=BLACK):
    parts.append(
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" {FONT} '
        f'font-size="{size}" fill="{fill}">{esc(s)}</text>')


def box(x, y, lines, style, stack=1):
    """lines: list of (string, size). Box is BOX_H high, vertically centred.

    stack > 1 draws (stack - 1) cascaded layers behind the labelled box.
    """
    fill, stroke = STYLE[style]
    w = EP_W if x in (XL0, XE0) else CT_W
    for k in range(stack - 1, 0, -1):        # farthest layer first
        rect(x + DX * k, y + DX * k, w, BOX_H, fill, stroke)
    rect(x, y, w, BOX_H, fill, stroke)
    h = sum(sz + 9 for _, sz in lines) - 9
    cy = y + BOX_H / 2
    base = cy - h / 2 + lines[0][1] * 0.5 + 3
    for s, sz in lines:
        text(x + w / 2, base, s, sz)
        base += sz + 9


def link(xa, xb, y, label=None):
    """Straight horizontal link from xa to xb with hollow double arrowheads."""
    parts.append(
        f'<polygon points="{xa},{y} {xa + 9},{y - 4.5} {xa + 9},{y + 4.5}" '
        f'fill="{WHITE}" stroke="{BLACK}" stroke-width="1.1"/>')
    parts.append(
        f'<polygon points="{xb},{y} {xb - 9},{y - 4.5} {xb - 9},{y + 4.5}" '
        f'fill="{WHITE}" stroke="{BLACK}" stroke-width="1.1"/>')
    parts.append(
        f'<line x1="{xa + 9}" y1="{y}" x2="{xb - 9}" y2="{y}" '
        f'stroke="{BLACK}" stroke-width="1.1"/>')
    if label:
        text((xa + xb) / 2, y - 7, label, 15)


# frames behind everything
rect(20, FRAME_TOP, XC1, FRAME_BOT - FRAME_TOP,
     FRAME_FILL, FRAME_STROKE)
rect(XR0 - 20, FRAME_TOP, XE1 + 20 - (XR0 - 20), FRAME_BOT - FRAME_TOP,
     FRAME_FILL, FRAME_STROKE)
text(36, FRAME_TOP + 20, "Internal interfaces", 15, "start", "#444444")
text(XR0, FRAME_TOP + 20, "External interfaces", 15, "start", "#444444")

# side links
for i, (t, sub, st, ctrl, lab1, lab2, n) in enumerate(ROWS_L):
    y = YC0 + i * PITCH_L
    xa = XL1 + DX * (n - 1)              # link starts at the stack's edge
    if ctrl:
        link(xa, XC0, y, lab1)
        link(XC1, XU0, y, lab2)
    else:
        link(xa, XU0, y, lab1)
    if n > 1:
        text(xa + 8, y - 34, f"x{n}", 14, "start")

# right rows spread evenly over the same vertical span as the left side
span = (len(ROWS_L) - 1) * PITCH_L
for i, (t, sub, st, ctrl, lab1, lab2, n) in enumerate(ROWS_R):
    y = YC0 + (span - R_PITCH * (len(ROWS_R) - 1)) // 2 + i * R_PITCH
    if ctrl:
        link(XU1, XR0, y, lab1)
        link(XR1, XE0, y, lab2)
    else:
        link(XU1, XE0, y, lab1)
    if n > 1:
        text(XE0 - 8, y - 34, f"x{n}", 14, "end")

# SoC column
rect(XU0, CPU_TOP, CPU_W, CPU_BOT - CPU_TOP, GRAY_FILL, GRAY_STROKE, 1.5)
h = sum(sz + 16 for _, sz in CPU_LINES) - 16
base = (CPU_TOP + CPU_BOT) / 2 - h / 2 + CPU_LINES[0][1] * 0.5 + 4
for s, sz in CPU_LINES:
    text((XU0 + XU1) / 2, base, s, sz)
    base += sz + 16

# device boxes (drawn after links so borders stay crisp)
for i, (t, sub, st, ctrl, _, _, n) in enumerate(ROWS_L):
    y = YC0 + i * PITCH_L - BOX_H / 2
    lines = [(t, 16)] + ([(sub, 13)] if sub else [])
    box(XL0, y, lines, st, n)
    if ctrl:
        box(XC0, y, [(ctrl[0], 16), (ctrl[1], 13)], ctrl[2])

for i, (t, sub, st, ctrl, _, _, n) in enumerate(ROWS_R):
    y = (YC0 + (span - R_PITCH * (len(ROWS_R) - 1)) // 2 + i * R_PITCH
         - BOX_H / 2)
    lines = [(t, 16)] + ([(sub, 13)] if sub else [])
    box(XE0, y, lines, st, n)
    if ctrl:
        box(XR0, y, [(ctrl[0], 16), (ctrl[1], 13)], ctrl[2])

# title
text(CANVAS_W / 2, 44, "N5 MAX", 28)
text(CANVAS_W / 2, 74, "Interface Block Diagram", 18)

# ----------------------------------------------------------------- output
print(f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" '
      f'height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}">')
print(f'<rect x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" '
      f'fill="{WHITE}"/>')
for p in parts:
    print(p)
print("</svg>")
