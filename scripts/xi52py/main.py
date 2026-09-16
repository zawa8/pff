#!/usr/bin/env python3
"""
main.py -- xi52 build pipeline orchestrator (p1onli branch)

Runs the whole xi52 build end-to-end by loading each step's script as
a module (via importlib, by file path -- these aren't a package with
__init__.py files) and calling its function(s) directly, instead of
invoking `fontforge -script <name>.py` once per file by hand.

Run with FontForge's own Python (every step imports `fontforge`):

    fontforge -script main.py            # full pipeline, steps 1..N
    fontforge -script main.py --list      # print the numbered steps and exit
    fontforge -script main.py --from 4    # resume from step 4 (1-based)
    fontforge -script main.py --only 7    # run just step 7

Steps 1-3 rebuild the xi38 base fonts themselves (Noto glyph sourcing,
using this branch's p1onli-restricted consonant set --
see glyph_copy/glyph_kopi_u9scripts_p1onli.py). Every step after that
derives xi52 from whatever is in sfd/xi38font/ at that point. If
you've already rebuilt xi38 and only want to redo the xi52 derivation,
skip straight to step 4 with --from 4.

Known quirk, not fixed here: several of the called scripts set up
their own `logging.basicConfig(...)` and `logging.getLogger('').
addHandler(console)` at module import time. `logging.basicConfig` is a
no-op once the root logger already has a handler, so only the *first*
step's log FILE actually ends up receiving file-logged messages when
run through this orchestrator (each script's own file-log path is
still printed in its "Done! Logs: ..." line, but nothing is written
there past step 1). The extra console `StreamHandler`s do all still
get added though, so WARNING+ console output can appear duplicated
more times as the pipeline goes on. Cosmetic only -- doesn't affect
the actual font output -- but don't be alarmed if a later step's log
file comes back empty or a warning prints several times.
"""
import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(rel_path: str):
    """Import a script that lives at HERE/rel_path as its own module,
    by file path -- avoids needing __init__.py or sys.path tricks."""
    path = HERE / rel_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_main(rel_path: str):
    """Most steps just expose main() with no arguments -- wrap that
    in a zero-arg callable for the PIPELINE table below."""
    def runner():
        load(rel_path).main()
    return runner


def run_u9scripts_p1onli():
    # glyph_kopi_u9scripts_p1onli.py's own main() reads sys.argv for a
    # script name / "all", so call process_script() directly instead
    # of going through main() and having to fake argv.
    mod = load("glyph_copy/glyph_kopi_u9scripts_p1onli.py")
    for script_name in mod.SCRIPTS:
        mod.process_script(script_name)


PIPELINE = [
    ("rebuild xi38asc consonants, 9 scripts (p1onli set)", run_u9scripts_p1onli),
    ("rebuild xi38asc Sinhala (p1onli set)", run_main("glyph_copy/glyph_kopi_usinhala_p1onli.py")),
    ("rebuild xi38utf from xi38asc (p1onli set)", run_main("glyph_copy/glyph_kopi_u2utf_p1onli.py")),
    ("copy xi38asc -> xi52asc", run_main("copy_xi38_to_xi52.py")),
    ("copy English chars into xi52asc", run_main("copy_e52_chars_xi52.py")),
    ("copy xi38utf -> xi52utf", run_main("copy_xi38utf_to_xi52utf.py")),
    ("add unicode-range references to xi52utf", run_main("add_unicode_ranges_utf_52.py")),
    ("copy English chars into xi52utf", run_main("copy_e52utf_chars_xi52utf.py")),
    ("rename xi52utf font internals", run_main("rename_utf_fonts_52.py")),
    ("copy xi52utf -> xi52mono", run_main("copy_utf_to_mono_xi52.py")),
    ("center glyphs in xi52mono", run_main("center_glyphs_mono_xi52.py")),
    ("fix glyph widths in xi52mono", run_main("fix_mono_width_xi52.py")),
    ("generate ttf/woff2 from xi52asc", run_main("generate_xi52asc_ttf_woff2.py")),
    ("generate ttf/woff2 from xi52utf", run_main("generatefonts/generate_xi52_ttf.py")),
    ("generate ttf/woff2 from xi52mono", run_main("generate_mono_ttf.py")),
]


def main():
    parser = argparse.ArgumentParser(description="xi52 build pipeline orchestrator")
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
