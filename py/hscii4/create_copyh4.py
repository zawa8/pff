#!/usr/bin/python3
from datetime import datetime
import fontforge
from dikt_esoft2hscii4 import dikt_esoft2hscii4

    
def create_copyh4(sfdroot,ftype):
    lscript = (
        "inglish", "russian", "korean",
        "hindi",
        "bangla","guzrati","gurmukhi","oriya",
        "telugu","tamil","kannada","malayalam","sinhala"
        # "binaryv"
    )
    for lscript in lscript:
        englosoftw8_ffobz = fontforge.open(     f"{sfdroot}/englosoftw8_copy/englosoftw8{ftype}/{lscript}englosoftw8{ftype}.sfd"      )
        englosoftw8_ffobz.selection.select(("ranges",None),":","~")
        englosoftw8_ffobz.unlinkReferences()
        englosoftw8_ffobz.save()
        #return
        hscii4w8_ffobz = fontforge.open(     f"{sfdroot}/hscii4w8/hscii4w8{ftype}/{lscript}hscii4w8{ftype}.sfd"      )
        print(f"englosoftw8_ffobz path is {englosoftw8_ffobz.path} n family name is {englosoftw8_ffobz.familyname}")
        print(f"hscii4w8_ffobz path is {hscii4w8_ffobz.path} n family name is {hscii4w8_ffobz.familyname}")
        ########
        for srclok, trglok in dikt_esoft2hscii4.items():
            englosoftw8_ffobz.selection.select(srclok)
            englosoftw8_ffobz.copy()
            hscii4w8_ffobz.selection.select(trglok)
            hscii4w8_ffobz.clear()
            hscii4w8_ffobz.paste() 
        ########
        hscii4w8_ffobz.save()
        hscii4w8_ffobz.close()
        englosoftw8_ffobz.close()
        ########
##############
if __name__ == "__main__":
    sfdroot = "/home/viml/mg/zw8/pff/sfd/"
    for ftype in ("utf","asc","mono",) :
        create_copyh4(sfdroot,ftype)


