# Windows 3D rendering errors with small dedicated graphics memory

The known symptom on the N5 MAX: with the dedicated graphics memory set to
1 GB or 2 GB, 3DMark Time Spy may occasionally produce rendering errors.
This is optional — apply the fix only if you encounter errors in a 3D
application.

## Fix

Size the dedicated graphics memory **above what your 3D application or game
requires** — 4 GB is only the value that resolved 3DMark Time Spy in our
testing, and other software may need more. Both methods below set the same
firmware-level value:

1. **BIOS** — `Setup` → `AMD CBS` → `NBIO Common Options` →
   `GFX Configuration` → `UMA Frame buffer Size`.
2. **AMD Software: Adrenalin Edition** — `Performance` → `Tuning` →
   `Variable Graphics Memory`.

Then restart and re-run the affected application.

## Background

Observed sporadically on the N5 MAX with 3DMark Time Spy at 1 GB and 2 GB
dedicated memory. For LLM workloads the recommended settings are far larger,
so this issue normally does not apply.
