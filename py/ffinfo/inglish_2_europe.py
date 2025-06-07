#!/usr/bin/python3
from datetime import datetime
import fontforge
# import uuid
import hashlib

def create_uuid_from_string(val: str):
    hex_string = hashlib.md5(val.encode("UTF-8")).hexdigest()
    return int(hex_string, 16) % 10**16
##############    
def inglish_2_europe(sfdroot,encoding,ftype):
    langscripts = (
        # "inglish",
        "french","russian","german","spanish",
        # "hindi",
        # "bangla","guzrati","gurmukhi","oriya",
        # "korean",
        # "telugu","tamil","kannada","malayalam","sinhala"
        # "binaryv"
    )
    inglish_ffobz = fontforge.open(     f"{sfdroot}/{encoding}/{encoding}{ftype}/inglish{encoding}{ftype}.sfd"      )
    for lscript in langscripts:
        lscriptfontname = f"{lscript}{encoding}{ftype}"  
        ########
        todayd = datetime.today().strftime('%Y-%m-%d')
        unikname = f"{lscriptfontname} hscii 4finger1thumb 4f1t maths {todayd}"
        inglish_ffobz.familyname = f"{lscriptfontname}"
        inglish_ffobz.fullname = f"{lscriptfontname}"
        inglish_ffobz.fontname = f"{lscriptfontname}"    
        inglish_ffobz.uniqueid = create_uuid_from_string(f"{lscriptfontname} {unikname}")
        inglish_ffobz.copyright = f"github.com/zawa8/font hscii 4finger1thumb 4f1t maths"
        inglish_ffobz.version = f"w0.000"
        inglish_ffobz.os2_vendor = "zawa"    
        # ########
        #f.appendSFNTName(language, strid, string)
        inglish_ffobz.sfntRevision = 1.0000000
        ##############
        inglish_ffobz.appendSFNTName('English (US)', 'UniqueID', f"FontForge 2.0 : {lscriptfontname} : 30-3-2025")
        inglish_ffobz.appendSFNTName('English (US)', 'Fullname', f"{lscriptfontname}")
        inglish_ffobz.appendSFNTName('English (US)', 'UniqueID',  f"{unikname} 0.000;zawa;hscii5 {lscriptfontname}-regular")
        inglish_ffobz.appendSFNTName('English (US)', 'PostScriptName', f"{lscriptfontname}")
        inglish_ffobz.appendSFNTName('English (US)', 'Family', f"{lscriptfontname}")
        ##############  
        inglish_ffobz.appendSFNTName('English (US)', 'Version', 'wersion 0.0000')
        inglish_ffobz.appendSFNTName('English (US)', 'Copyright', 'github.com/zawa8/font hscii4(4phinger maths) hscii5')
        inglish_ffobz.appendSFNTName('English (US)', 'SubFamily', 'regular')
        inglish_ffobz.appendSFNTName('English (US)', 'Version', 'wersion 0.0000')
        inglish_ffobz.appendSFNTName('English (US)', 'Trademark', 'hscii5/4 fonts 5/4phingrmaths')
        inglish_ffobz.appendSFNTName('English (US)', 'Manufacturer', 'simbxls hscii github zawa8')
        inglish_ffobz.appendSFNTName('English (US)', 'Designer', 'wimxl kumar merged and changed fonts')
        inglish_ffobz.appendSFNTName('English (US)', 'Descriptor', 'merged changed by zawa8 pff(python fontforge)')
        inglish_ffobz.appendSFNTName('English (US)', 'Vendor URL', 'https://github.com/zawa8/font')
        inglish_ffobz.appendSFNTName('English (US)', 'Designer URL', 'https://github.com/zawa8/pff')
        inglish_ffobz.appendSFNTName('English (US)', 'License', 'license file present in : https://github.com/zawa8/font/')
        inglish_ffobz.appendSFNTName('English (US)', 'License URL', 'https://github.com/zawa8/font')
        print("####################")
        lscript_sfd_path = f"{sfdroot}/{encoding}/{encoding}{ftype}/{lscript}{encoding}{ftype}.sfd"
        print(f"lscript_sfd_path is {lscript_sfd_path}.")    
        inglish_ffobz.save(lscript_sfd_path)
        print("####################")          
        print("####  language is {lang}  ####")
        print(f"lscript_sfd_path is {lscript_sfd_path}. inglish_ffobz file_path is {inglish_ffobz.path}")    
        print(f"inglish_ffobz family name is {inglish_ffobz.familyname}")
        print(f"inglish_ffobz fullname is {inglish_ffobz.fullname}")
        print(f"inglish_ffobz fontname is {inglish_ffobz.fontname}")
        print(f"inglish_ffobz copyright is {inglish_ffobz.copyright}")
        print(f"inglish_ffobz version is {inglish_ffobz.version}")
        print(f"inglish_ffobz uniqueid is {inglish_ffobz.uniqueid}")
        print(f"inglish_ffobz fondname is {inglish_ffobz.fondname}")
        print(f"inglish_ffobz os2_vendor is {inglish_ffobz.os2_vendor}")
        print("####################")
        print(f"inglish_ffobz f.sfntRevision is {inglish_ffobz.sfntRevision}") 
        print(f"inglish_ffobz sfnt_names is {inglish_ffobz.sfnt_names}") 
        print("####################")
        ########
    inglish_ffobz.close()
        ########
##############
if __name__ == "__main__":
    sfdroot = "/home/viml/mg/zw8/pff/sfd/"
    langscripts = (
    # "inglish",
    "french","russian","german","spanish",
    # "hindi",
    # "bangla","guzrati","gurmukhi","oriya",
    # "korean",
    # "telugu","tamil","kannada","malayalam","sinhala"
    # "binaryv"
    )
    for encoding in ("englosoftw8","englodotw8","onlyw8",) :
        for ftype in ("utf","asc","mono",) :
            inglish_2_europe(sfdroot,encoding,ftype)


