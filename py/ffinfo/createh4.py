#!/usr/bin/python3
from datetime import datetime
import fontforge
import hashlib

def create_uuid_from_string(val: str):
    hex_string = hashlib.md5(val.encode("UTF-8")).hexdigest()
    return int(hex_string, 16) % 10**16
##############    
def createh4(sfdroot,ftype):
    lscript = (
        "inglish", "russian", "korean",
        "hindi",
        "bangla","guzrati","gurmukhi","oriya",
        "telugu","tamil","kannada","malayalam","sinhala"
        # "binaryv"
    )
    for lscript in lscript:
        englosoftw8_ffobz = fontforge.open(     f"{sfdroot}/englosoftw8/englosoftw8{ftype}/{lscript}englosoftw8{ftype}.sfd"      )
        lscriptfontname = f"{lscript}hscii4w8{ftype}"  
        ########
        todayd = datetime.today().strftime('%Y-%m-%d')
        unikname = f"{lscriptfontname} hscii 4finger1thumb 4f1t maths {todayd}"
        englosoftw8_ffobz.familyname = f"{lscriptfontname}"
        englosoftw8_ffobz.fullname = f"{lscriptfontname}"
        englosoftw8_ffobz.fontname = f"{lscriptfontname}"    
        englosoftw8_ffobz.uniqueid = create_uuid_from_string(f"{lscriptfontname} {unikname}")
        englosoftw8_ffobz.copyright = f"github.com/zawa8/font hscii 4finger1thumb 4f1t maths"
        englosoftw8_ffobz.version = f"w0.000"
        englosoftw8_ffobz.os2_vendor = "zawa"    
        # ########
        #f.appendSFNTName(language, strid, string)
        englosoftw8_ffobz.sfntRevision = 1.0000000
        ##############
        englosoftw8_ffobz.appendSFNTName('English (US)', 'UniqueID', f"FontForge 2.0 : {lscriptfontname} : 30-3-2025")
        englosoftw8_ffobz.appendSFNTName('English (US)', 'Fullname', f"{lscriptfontname}")
        englosoftw8_ffobz.appendSFNTName('English (US)', 'UniqueID',  f"{unikname} 0.000;zawa;hscii5 {lscriptfontname}-regular")
        englosoftw8_ffobz.appendSFNTName('English (US)', 'PostScriptName', f"{lscriptfontname}")
        englosoftw8_ffobz.appendSFNTName('English (US)', 'Family', f"{lscriptfontname}")
        ##############  
        englosoftw8_ffobz.appendSFNTName('English (US)', 'Version', 'wersion 0.0000')
        englosoftw8_ffobz.appendSFNTName('English (US)', 'Copyright', 'github.com/zawa8/font hscii4(4phinger maths) hscii5')
        englosoftw8_ffobz.appendSFNTName('English (US)', 'SubFamily', 'regular')
        englosoftw8_ffobz.appendSFNTName('English (US)', 'Version', 'wersion 0.0000')
        englosoftw8_ffobz.appendSFNTName('English (US)', 'Trademark', 'hscii5/4 fonts 5/4phingrmaths')
        englosoftw8_ffobz.appendSFNTName('English (US)', 'Manufacturer', 'simbxls hscii github zawa8')
        englosoftw8_ffobz.appendSFNTName('English (US)', 'Designer', 'wimxl kumar merged and changed fonts')
        englosoftw8_ffobz.appendSFNTName('English (US)', 'Descriptor', 'merged changed by zawa8 pff(python fontforge)')
        englosoftw8_ffobz.appendSFNTName('English (US)', 'Vendor URL', 'https://github.com/zawa8/font')
        englosoftw8_ffobz.appendSFNTName('English (US)', 'Designer URL', 'https://github.com/zawa8/pff')
        englosoftw8_ffobz.appendSFNTName('English (US)', 'License', 'license file present in : https://github.com/zawa8/font/')
        englosoftw8_ffobz.appendSFNTName('English (US)', 'License URL', 'https://github.com/zawa8/font')
        print("####################")
        lscript_sfd_path = f"{sfdroot}/hscii4w8/hscii4w8{ftype}/{lscript}hscii4w8{ftype}.sfd"
        print(f"lscript_sfd_path is {lscript_sfd_path}.")    
        englosoftw8_ffobz.save(lscript_sfd_path)
        print("####################")          
        print("####  language is {lang}  ####")
        print(f"lscript_sfd_path is {lscript_sfd_path}. inglish_ffobz file_path is {englosoftw8_ffobz.path}")    
        print(f"inglish_ffobz family name is {englosoftw8_ffobz.familyname}")
        print(f"inglish_ffobz fullname is {englosoftw8_ffobz.fullname}")
        print(f"inglish_ffobz fontname is {englosoftw8_ffobz.fontname}")
        print(f"inglish_ffobz copyright is {englosoftw8_ffobz.copyright}")
        print(f"inglish_ffobz version is {englosoftw8_ffobz.version}")
        print(f"inglish_ffobz uniqueid is {englosoftw8_ffobz.uniqueid}")
        print(f"inglish_ffobz fondname is {englosoftw8_ffobz.fondname}")
        print(f"inglish_ffobz os2_vendor is {englosoftw8_ffobz.os2_vendor}")
        print("####################")
        print(f"inglish_ffobz f.sfntRevision is {englosoftw8_ffobz.sfntRevision}") 
        print(f"inglish_ffobz sfnt_names is {englosoftw8_ffobz.sfnt_names}") 
        print("####################")
        ########
        englosoftw8_ffobz.close()
        ########
##############
if __name__ == "__main__":
    sfdroot = "/home/viml/mg/zw8/pff/sfd/"
    for ftype in ("utf","asc","mono",) :
        createh4(sfdroot,ftype)


