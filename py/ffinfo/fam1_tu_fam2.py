#!/usr/bin/python3
import fontforge

langscripts = (
    # "ing",
    "hindi",
    "bangla","guzrati","gurmukhi","oriya",
    "korean",
    "telugu","tamil","kannada","malayalam","sinhala"
    # "binaryv"
)
##############
def fam1_tu_fam2(dir1,dir2,sfiks1,sfiks2,srclok_trglok_dikt):
    #sfddir=f"{sfdroot}/{b_or_s}/source{ftype}/"
    for lscript in langscripts:
        fobz1 = fontforge.open(f"{dir1}/{lscript}{sfiks1}.sfd")
        fobz2 = fontforge.open(f"{dir2}/{lscript}{sfiks2}.sfd")
        print(f"lscript is {lscript}.")
        print(f"fobz1 file_path is {fobz1.path} . fobz1 familyname is {fobz1.familyname}")
        print(f"fobz2 file_path is {fobz2.path} . fobz1 familyname is {fobz2.familyname}")
        for srclok, trglok in srclok_trglok_dikt.items():
            fobz1.selection.select(srclok)
            fobz1.copy()
            fobz2.selection.select(trglok)
            fobz2.clear()
            fobz2.paste()
        fobz2.save()
        fobz2.close()
        fobz1.close()
############## 4sa means 4finger soft asciionly
if __name__ == "__main__":
    dir1=f"/home/viml/mg/zw8/pff/sfd/4s/4smold/"
    dir2=f"/home/viml/mg/zw8/pff/sfd/4s/4sm/"
    sfiks1 = "15mb"
    sfiks2 = "4sm"
    srclok_trglok_dikt={
        "B" : "B","D" : "D","J" : "J","K" : "K",
        "Q" : "Q","S" : "S","T" : "T","Z" : "Z",
        "j" : "j","q" : "q",
        "V" : "v","X" : "x",
    }
    fam1_tu_fam2(dir1,dir2,sfiks1,sfiks2,srclok_trglok_dikt)

