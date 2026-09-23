#!/usr/bin/env python3
"""
main.py -- xi52/xi38 build pipeline orchestrator

3 phases (asc, utf, mono) + final TTF/WOFF2 generation.

Run with FontForge's own Python:

    fontforge -script main.py            # full pipeline
    fontforge -script main.py --list     # print steps
    fontforge -script main.py --from N   # resume from step N
    fontforge -script main.py --only N   # run step N only
"""
import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(rel_path: str):
    """Import a script that lives at HERE/rel_path as its own module."""
    path = HERE / rel_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_main(rel_path: str):
    """Most steps just expose main() with no arguments."""
    def runner():
        load(rel_path).main()
    return runner


def run_u9scripts_p1onli():
    """Build xi38asc + xi52asc for 9 scripts via G1-G5 rules.

    Calls glyph_kopi_u9scripts_p1onli.py's functions directly,
    bypassing its argparse-based main().
    """
    mod = load("glyph_copy/glyph_kopi_u9scripts_p1onli.py")
    csv_rows = mod.read_csv()
    sources = {
        "xe52":      mod.fontforge.open(str(mod.ENGLISH_52)),
        "xe38":      mod.fontforge.open(str(mod.ENGLISH_38)),
        "xh38":      mod.fontforge.open(str(mod.XH38_SOURCE)),
        "noto_math": mod.fontforge.open(str(mod.NOTO_MATH)),
    }
    try:
        for name, cfg in mod.SCRIPTS.items():
            mod.process_script(name, cfg, csv_rows, sources)
    finally:
        for f in sources.values():
            f.close()


PIPELINE = [
    # --- Phase 0: sources -> targets ---
    ("[src] copy sources -> targets", run_main("copy_sources_to_targets.py")),

    # --- Phase 1: asc (xi38asc + xi52asc parallel) ---
    ("[asc] build xi38asc + xi52asc, 9 scripts (G1-G5)", run_u9scripts_p1onli),
    ("[asc] build xi38asc + xi52asc, Sinhala", run_main("glyph_copy/glyph_kopi_usinhala_p1onli.py")),

    # --- Phase 2: utf ---
    ("[utf] xi38asc -> xi38utf (copy 128 + unicode refs)", run_main("glyph_copy/glyph_kopi_u2utf_p1onli.py")),
    ("[utf] xi52asc -> xi52utf (copy + refs)", run_main("copy_xi38utf_to_xi52utf.py")),
    ("[utf] add unicode-range refs to xi52utf", run_main("add_unicode_ranges_utf_52.py")),
    ("[utf] rename xi52utf internals", run_main("rename_utf_fonts_52.py")),

    # --- Phase 3: mono ---
    ("[mono] xi52utf -> xi52mono", run_main("copy_utf_to_mono_xi52.py")),
    ("[mono] center glyphs in xi52mono", run_main("center_glyphs_mono_xi52.py")),
    ("[mono] fix widths in xi52mono", run_main("fix_mono_width_xi52.py")),
    # TODO: xi38mono pipeline (not yet implemented)

    # --- Phase 4: generate TTF/WOFF2 (last) ---
    ("[gen] TTF/WOFF2 from xi38asc", run_main("generate_xi38asc_ttf_woff2.py")),
    ("[gen] TTF/WOFF2 from xi38utf", run_main("generatefonts/generate_xi38utf_ttf_p1onli.py")),
    ("[gen] TTF/WOFF2 from xi52asc", run_main("generate_xi52asc_ttf_woff2.py")),
    ("[gen] TTF/WOFF2 from xi52utf", run_main("generatefonts/generate_xi52_ttf.py")),
    ("[gen] TTF/WOFF2 from xi52mono", run_main("generate_mono_ttf.py")),
]


def main():
    parser = argparse.ArgumentParser(description="xi52/xi38 build pipeline orchestrator")
    parser.add_argument("--list", action="store_true", help="print the numbered steps and exit")
    parser.add_argument("--from", dest="start", type=int, default=1,
                        help="1-based step to start from (default: 1, i.e. run everything)")
    parser.add_argument("--only", type=int, default=None,
                        help="run only this one 1-based step, ignoring --from")
    args = parser.parse_args()

    if args.list:
        for i, (label, _fn) in enumerate(PIPELINE, 1):
            print(f"{i:2d}. {label}")
        return

    if args.only is not None:
        steps = [(args.only, PIPELINE[args.only - 1])]
    else:
        steps = list(enumerate(PIPELINE, 1))[args.start - 1:]

    total = len(PIPELINE)
    for i, (label, fn) in steps:
        print(f"\n=== step {i}/{total}: {label} ===")
        try:
            fn()
        except Exception as e:
            print(f"\n\u2717 step {i} ({label}) failed: {e}")
            print(f"fix the error above, then resume with:\n"
                  f"    fontforge -script main.py --from {i}")
            sys.exit(1)

    print("\n\u2713 pipeline complete.")


if __name__ == "__main__":
    main()