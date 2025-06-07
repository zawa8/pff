#!/usr/bin/python3
import fontforge
languages = (
    "ing",
    "hindi",
    "bangla","guzrati","gurmukhi","oriya",
    "korean",
    "telugu","tamil","kannada","malayalam","sinhala"
)
b_or_s = "big"
src15 = f"/home/viml/mg/zw8/pff/sfd/{b_or_s}/source15b/"
src115 = f"/home/viml/mg/zw8/pff/sfd/{b_or_s}/source115b/"
###############
for lang in languages:
    font115 = fontforge.open(f"{src115}/{lang}115b.sfd")
    font15 = fontforge.open(f"{src15}/{lang}15b.sfd")
    print(f"lang is {lang} and font115 family name is {font115.familyname} and font15 family name is {font15.familyname}")
    font115.selection.select(("ranges", None), " ", "~")
    font115.copy()
    font15.selection.select(("ranges", None), " ", 159)
    font15.clear()
    font15.selection.select(("ranges", None), " ", "~")
    font15.paste()
    font15.save()
    font15.close()
    font115.close()