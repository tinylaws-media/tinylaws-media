"""Contact sheets for v5: hook (0-8 s / 0.5 s), ~30 key frames, last 8 s every 0.25 s."""
import sys
import importlib
from exit_render import sheet, key_times
ep = sys.argv[1]
E = importlib.import_module(ep)
which = sys.argv[2:] or ["hook", "keys", "end"]
if "hook" in which:
    sheet(ep, [round(0.5 * k, 2) for k in range(17)], name=f"{ep}_sheet_hook")
if "keys" in which:
    sheet(ep, key_times(E), name=f"{ep}_sheet_keys")
if "end" in which:
    D = E.DURATION
    sheet(ep, [round(D - 8 + 0.25 * k, 2) for k in range(32)], cols=8, name=f"{ep}_sheet_end")
