#!/usr/bin/python3
import fontforge
from uhin_dikt import asc_2_uhin_dikt
print(asc_2_uhin_dikt)
langscripts = (
    "inglish",
    "hindi",
    "bangla","guzrati","gurmukhi","oriya",
    "korean",
    "telugu","tamil","kannada","malayalam","sinhala"
    # "binaryw", "heks"
)
##############
def asc_2_uhin(sfdroot,encoding,asc_2_uhin_dikt):
    sfddir=f"{sfdroot}/{encoding}/{encoding}utf/"
    for lscript in langscripts:
        ffobzkt_lscript = fontforge.open(f"{sfddir}/{lscript}{encoding}utf.sfd")
        print(f"ffobzkt_lscript path is {ffobzkt_lscript.path} n family name is {ffobzkt_lscript.familyname}")
        for srclok, trglok in asc_2_uhin_dikt.items():
            ffobzkt_lscript.selection.select(srclok)
            ffobzkt_lscript.copyReference()
            ffobzkt_lscript.selection.select(trglok)
            #ffobzkt_lscript.clear()
            ffobzkt_lscript.paste()
        ffobzkt_lscript.save()
        ffobzkt_lscript.close()
##############
if __name__ == "__main__":
    sfdroot=f"/home/viml/mg/zw8/pff/sfd/"
    asc_2_uhin(sfdroot,"englosoftw8",asc_2_uhin_dikt)
    asc_2_uhin(sfdroot,"englodotw8",asc_2_uhin_dikt)
    asc_2_uhin(sfdroot,"onlyw8",asc_2_uhin_dikt)
    asc_2_uhin(sfdroot,"indikw8",asc_2_uhin_dikt)

