#!/usr/bin/python3
import fontforge
languages = (
    "ing",
    "hindi",
    "bangla","guzrati","gurmukhi","oriya",
    "korean",
    "telugu","tamil","kannada","malayalam","sinhala"
)
#b_or_s = "big"
#src15 = f"/home/viml/mg/zw8/pff/sfd/{b_or_s}/source15b/"
#src115 = f"/home/viml/mg/zw8/pff/sfd/{b_or_s}/source115b/"
###############
def asco_22_utf(dir1,dir2,sfiks1,sfiks2):
    for lang in languages:
        fobz1 = fontforge.open(f"{dir1}/{lang}{sfiks1}.sfd")
        fobz2 = fontforge.open(f"{dir2}/{lang}{sfiks2}.sfd")
        print(f"lang is {lang}")
        print(f"fobz1 file_path is {fobz1.path}. fobz1 familyname is {fobz1.familyname}")
        print(f"fobz2 file_path is {fobz2.path}. fobz2 familyname is {fobz2.familyname}")
        fobz1.selection.select(("ranges", None), " ", "~")
        fobz1.copy()
        fobz2.selection.select(("ranges", None), " ", "~")
        fobz2.clear()
        fobz2.paste()
        fobz2.save()
        fobz2.close()
        fobz1.close()
############## 4sa means 4finger soft asciionly
if __name__ == "__main__":
    dir1=f"/home/viml/mg/zw8/pff/sfd/4s/4sa/"
    sfiks1 = "4sa"
    dir2=f"/home/viml/mg/zw8/pff/sfd/4s/4su/"
    sfiks2 = "4su"
    asco_22_utf(dir1,dir2,sfiks1,sfiks2)

