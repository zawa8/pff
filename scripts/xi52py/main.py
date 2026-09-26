#!/usr/bin/env python3
"""
main.py -- xi52/xi38 build pipeline orchestrator

Phases:
    src   sources -> targets
    asc   xi38asc + xi52asc build (9 scripts + Sinhala)
    utf   xi38utf + xi52utf build
    mono  xi52mono build            (WIP, not run in CI yet)
    meta  font metadata stamp       (Google Fonts format)
    gen   TTF/WOFF2 generation

Run with FontForge's own Python:

    fontforge -script main.py                    # full pipeline (all phases)
    fontforge -script main.py --list             # print numbered steps
    fontforge -script main.py --list-phases      # print phase names
    fontforge -script main.py --phase asc        # run one phase
    fontforge -script main.py --only 11          # run step 11 only
    fontforge -script main.py --from 4           # resume from step 4
    fontforge -script main.py --skip 8,9,10      # skip mono steps
    fontforge -script main.py --dry-run          # print, don't execute
    fontforge -script main.py --continue         # keep going after a failure
"""
import argparse
import contextlib
import importlib.util
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent          # scripts/xi52py -> scripts -> repo root
LOGS_DIR = REPO_ROOT / "logs"
BUILD_INFO = LOGS_DIR / "build-info.txt"


# --------------------------------------------------------------------------
# module loading
# --------------------------------------------------------------------------

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


# --------------------------------------------------------------------------
# custom step: 9-script asc build
# --------------------------------------------------------------------------

@contextlib.contextmanager
def _open_font(mod, path):
    """Open a fontforge font from `path` and guarantee close on exit."""
    font = mod.fontforge.open(str(path))
    try:
        yield font
    finally:
        if font is not None:
            try:
                font.close()
            except Exception:
                pass


def run_u9scripts():
    """Build xi38asc + xi52asc for 9 scripts via G1-G5 rules.

    Calls build_asc_fonts.py's functions directly,
    bypassing its argparse-based main().
    """
    mod = load("glyph_copy/build_asc_fonts.py")
    csv_rows = mod.read_csv()
    with contextlib.ExitStack() as stack:
        sources = {
            "xe52":      stack.enter_context(_open_font(mod, mod.ENGLISH_52)),
            "xe38":      stack.enter_context(_open_font(mod, mod.ENGLISH_38)),
            "xh38":      stack.enter_context(_open_font(mod, mod.XH38_SOURCE)),
            "noto_math": stack.enter_context(_open_font(mod, mod.NOTO_MATH)),
        }
        for name, cfg in mod.SCRIPTS.items():
            mod.process_script(name, cfg, csv_rows, sources)


# --------------------------------------------------------------------------
# pipeline definition
# --------------------------------------------------------------------------

PHASES = [
    ("src",  "Phase 0 -- sources -> targets"),
    ("asc",  "Phase 1 -- asc (xi38asc + xi52asc)"),
    ("utf",  "Phase 2 -- utf (xi38utf + xi52utf)"),
    ("mono", "Phase 3 -- mono (xi52mono)  [WIP, not in CI]"),
    ("meta", "Phase 4 -- font metadata (Google Fonts format)"),
    ("gen",  "Phase 5 -- TTF/WOFF2 generation"),
]

PHASE_ORDER = [name for name, _ in PHASES]
PHASE_LABEL = dict(PHASES)

# (phase, label, runner)
PIPELINE = [
    # ---- src ----
    ("src",  "[src] copy sources -> targets",
             run_main("step0_copy_sources.py")),

    # ---- asc ----
    ("asc",  "[asc] build xi38asc + xi52asc, 9 scripts (G1-G5)",
             run_u9scripts),
    ("asc",  "[asc] build xi38asc + xi52asc, Sinhala",
             run_main("glyph_copy/build_sinhala_asc.py")),

    # ---- utf ----
    ("utf",  "[utf] xi38asc -> xi38utf (copy 128 + unicode refs)",
             run_main("glyph_copy/build_utf_fonts.py")),
    ("utf",  "[utf] xi52asc -> xi52utf (copy + refs)",
             run_main("copy_xi38utf_to_xi52utf.py")),
    ("utf",  "[utf] add unicode-range refs to xi52utf",
             run_main("add_unicode_ranges_utf_52.py")),
    ("utf",  "[utf] rename xi52utf internals",
             run_main("rename_utf_fonts_52.py")),

    # ---- mono (WIP) ----
    ("mono", "[mono] xi52utf -> xi52mono",
             run_main("copy_utf_to_mono_xi52.py")),
    ("mono", "[mono] center glyphs in xi52mono",
             run_main("center_glyphs_mono_xi52.py")),
    ("mono", "[mono] fix widths in xi52mono",
             run_main("fix_mono_width_xi52.py")),
    # TODO: xi38mono pipeline (not yet implemented)

    # ---- meta ----
    ("meta", "[meta] update font metadata (Google Fonts format)",
             run_main("update_font_metadata.py")),

    # ---- gen ----
    ("gen",  "[gen] TTF/WOFF2 from xi38asc",
             run_main("gen_xi38asc.py")),
    ("gen",  "[gen] TTF/WOFF2 from xi38utf",
             run_main("generatefonts/gen_xi38utf.py")),
    ("gen",  "[gen] TTF/WOFF2 from xi52asc",
             run_main("gen_xi52asc.py")),
    ("gen",  "[gen] TTF/WOFF2 from xi52utf",
             run_main("generatefonts/gen_xi52utf.py")),
    ("gen",  "[gen] TTF/WOFF2 from xi52mono",
             run_main("generate_mono_ttf.py")),
]


# --------------------------------------------------------------------------
# build-info
# --------------------------------------------------------------------------

def _git(*args):
    try:
        out = subprocess.check_output(
            ["git", *args], cwd=str(REPO_ROOT),
            stderr=subprocess.DEVNULL, text=True,
        )
        return out.strip()
    except Exception:
        return "(unavailable)"


def _fontforge_version():
    try:
        out = subprocess.check_output(
            ["fontforge", "--version"],
            stderr=subprocess.STDOUT, text=True,
        )
        return out.strip().splitlines()[0] if out.strip() else "(empty)"
    except Exception:
        return "(unavailable)"


def write_build_info(selected_steps):
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        f"pff build-info",
        f"generated:   {datetime.now(timezone.utc).isoformat()}",
        f"git SHA:     {_git('rev-parse', 'HEAD')}",
        f"git branch:  {_git('rev-parse', '--abbrev-ref', 'HEAD')}",
        f"git describe:{_git('describe', '--tags', '--always', '--dirty')}",
        f"fontforge:   {_fontforge_version()}",
        f"python:      {sys.version.split()[0]}",
        f"steps ({len(selected_steps)}):",
    ]
    for i, (phase, label, _fn) in selected_steps:
        lines.append(f"  {i:2d}. [{phase}] {label}")
    BUILD_INFO.write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _print_steps():
    for i, (phase, label, _fn) in enumerate(PIPELINE, 1):
        print(f"{i:2d}. [{phase}] {label}")


def _print_phases():
    for name, label in PHASES:
        print(f"{name:5s}  {label}")


def _select_steps(args):
    """Return a list of (1-based index, (phase, label, fn)) tuples."""
    if args.phase:
        chosen = [(i, s) for i, s in enumerate(PIPELINE, 1) if s[0] == args.phase]
        if not chosen:
            sys.exit(f"no steps in phase '{args.phase}'")
        return chosen

    if args.only is not None:
        if not (1 <= args.only <= len(PIPELINE)):
            sys.exit(f"--only must be 1..{len(PIPELINE)}")
        return [(args.only, PIPELINE[args.only - 1])]

    selected = list(enumerate(PIPELINE, 1))[args.start - 1:]
    if args.skip:
        selected = [(i, s) for i, s in selected if i not in args.skip]
    return selected


def main():
    parser = argparse.ArgumentParser(
        description="xi52/xi38 build pipeline orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="\n".join(f"  {n:5s} {l}" for n, l in PHASES),
    )
    parser.add_argument("--list", action="store_true",
                        help="print the numbered steps and exit")
    parser.add_argument("--list-phases", action="store_true",
                        help="print the phase names and exit")
    parser.add_argument("--phase", choices=PHASE_ORDER,
                        help="run one phase only")
    parser.add_argument("--from", dest="start", type=int, default=1,
                        help="1-based step to start from (default: 1)")
    parser.add_argument("--only", type=int, default=None,
                        help="run only this one 1-based step")
    parser.add_argument("--skip", type=lambda s: {int(x) for x in s.split(",") if x.strip()},
                        default=set(), metavar="N[,M,...]",
                        help="skip these 1-based step numbers")
    parser.add_argument("--dry-run", action="store_true",
                        help="print steps but do not execute")
    parser.add_argument("--continue", dest="keep_going", action="store_true",
                        help="log failures and continue instead of halting")
    args = parser.parse_args()

    if args.list:
        _print_steps()
        return
    if args.list_phases:
        _print_phases()
        return

    if not (1 <= args.start <= len(PIPELINE)):
        sys.exit(f"--from must be 1..{len(PIPELINE)}")

    steps = _select_steps(args)
    total = len(PIPELINE)

    try:
        write_build_info(steps)
    except Exception as e:
        print(f"(warning) could not write build-info.txt: {e}")

    if args.dry_run:
        print(f"dry-run: {len(steps)} step(s) would run:")
        for i, (phase, label, _fn) in steps:
            print(f"  {i:2d}. [{phase}] {label}")
        return

    failures = []
    for i, (phase, label, fn) in steps:
        print(f"\n=== step {i}/{total} [{phase}]: {label} ===")
        try:
            fn()
        except Exception as e:
            failures.append((i, label, e))
            print(f"\n\u2717 step {i} ({label}) failed: {e}")
            if not args.keep_going:
                print(f"fix the error above, then resume with:\n"
                      f"    fontforge -script main.py --from {i}")
                sys.exit(1)
            print(f"(--continue) skipping to next step")

    if failures:
        print(f"\n{len(failures)} step(s) failed:")
        for i, label, e in failures:
            print(f"  {i:2d}. {label}: {e}")
        sys.exit(1)

    print(f"\n\u2713 all {len(steps)} step(s) completed.")