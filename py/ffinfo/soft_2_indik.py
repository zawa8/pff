#!/usr/bin/python3
from datetime import datetime
import fontforge
# import uuid
import hashlib

def create_uuid_from_string(val: str):
    hex_string = hashlib.md5(val.encode("UTF-8")).hexdigest()
    return int(hex_string, 16) % 10**16
##############    
def soft_2_indik(sfdroot,ftype):
    langscripts = (
        "inglish", "russian", "korean",
        "hindi",
        "bangla","guzrati","gurmukhi","oriya",
        "telugu","tamil","kannada","malayalam","sinhala",
        # "binaryv"
    )
    softencoding = "englosoftw8"
    indikencoding = "indikw8"
    for lscript in langscripts:
        soft_lang_ffobz = fontforge.open(     f"{sfdroot}/{softencoding}/{softencoding}{ftype}/{lscript}{softencoding}{ftype}.sfd"      )
        # indik_lang_ffobz = fontforge.open(     f"{sfdroot}/{indikencoding}/{indikencoding}{ftype}/{lscript}{indikencoding}{ftype}.sfd"      )
        indiklscriptfontname = f"{lscript}{indikencoding}{ftype}"  
        ########
        todayd = datetime.today().strftime('%Y-%m-%d')
        unikname = f"{indiklscriptfontname} hscii 4finger1thumb 4f1t maths {todayd}"
        soft_lang_ffobz.familyname = f"{indiklscriptfontname}"
        soft_lang_ffobz.fullname = f"{indiklscriptfontname}"
        soft_lang_ffobz.fontname = f"{indiklscriptfontname}"    
        soft_lang_ffobz.uniqueid = create_uuid_from_string(f"{indiklscriptfontname} {unikname}")
        soft_lang_ffobz.copyright = f"github.com/zawa8/font hscii 4finger1thumb 4f1t maths"
        soft_lang_ffobz.version = f"w0.000"
        soft_lang_ffobz.os2_vendor = "zawa"    
        # ########
        #f.appendSFNTName(language, strid, string)
        soft_lang_ffobz.sfntRevision = 1.0000000
        ##############
        soft_lang_ffobz.appendSFNTName('English (US)', 'UniqueID', f"FontForge 2.0 : {indiklscriptfontname} : 30-3-2025")
        soft_lang_ffobz.appendSFNTName('English (US)', 'Fullname', f"{indiklscriptfontname}")
        soft_lang_ffobz.appendSFNTName('English (US)', 'UniqueID',  f"{unikname} 0.000;zawa;hscii5 {indiklscriptfontname}-regular")
        soft_lang_ffobz.appendSFNTName('English (US)', 'PostScriptName', f"{indiklscriptfontname}")
        soft_lang_ffobz.appendSFNTName('English (US)', 'Family', f"{indiklscriptfontname}")
        ##############  
        soft_lang_ffobz.appendSFNTName('English (US)', 'Version', 'wersion 0.0000')
        soft_lang_ffobz.appendSFNTName('English (US)', 'Copyright', 'github.com/zawa8/font hscii4(4phinger maths) hscii5')
        soft_lang_ffobz.appendSFNTName('English (US)', 'SubFamily', 'regular')
        soft_lang_ffobz.appendSFNTName('English (US)', 'Version', 'wersion 0.0000')
        soft_lang_ffobz.appendSFNTName('English (US)', 'Trademark', 'hscii5/4 fonts 5/4phingrmaths')
        soft_lang_ffobz.appendSFNTName('English (US)', 'Manufacturer', 'simbxls hscii github zawa8')
        soft_lang_ffobz.appendSFNTName('English (US)', 'Designer', 'wimxl kumar merged and changed fonts')
        soft_lang_ffobz.appendSFNTName('English (US)', 'Descriptor', 'merged changed by zawa8 pff(python fontforge)')
        soft_lang_ffobz.appendSFNTName('English (US)', 'Vendor URL', 'https://github.com/zawa8/font')
        soft_lang_ffobz.appendSFNTName('English (US)', 'Designer URL', 'https://github.com/zawa8/pff')
        soft_lang_ffobz.appendSFNTName('English (US)', 'License', 'license file present in : https://github.com/zawa8/font/')
        soft_lang_ffobz.appendSFNTName('English (US)', 'License URL', 'https://github.com/zawa8/font')
        print("####################")
        indik_lscript_sfd_path = f"{sfdroot}/{indikencoding}/{indikencoding}{ftype}/{lscript}{indikencoding}{ftype}.sfd"
        print(f"lscript_sfd_path is {indik_lscript_sfd_path}.")    
        soft_lang_ffobz.save(indik_lscript_sfd_path)
        print("####################")          
        print("####  language is {lang}  ####")
        print(f"lscript_sfd_path is {indik_lscript_sfd_path}. inglish_ffobz file_path is {soft_lang_ffobz.path}")    
        print(f"inglish_ffobz family name is {soft_lang_ffobz.familyname}")
        print(f"inglish_ffobz fullname is {soft_lang_ffobz.fullname}")
        print(f"inglish_ffobz fontname is {soft_lang_ffobz.fontname}")
        print(f"inglish_ffobz copyright is {soft_lang_ffobz.copyright}")
        print(f"inglish_ffobz version is {soft_lang_ffobz.version}")
        print(f"inglish_ffobz uniqueid is {soft_lang_ffobz.uniqueid}")
        print(f"inglish_ffobz fondname is {soft_lang_ffobz.fondname}")
        print(f"inglish_ffobz os2_vendor is {soft_lang_ffobz.os2_vendor}")
        print("####################")
        print(f"inglish_ffobz f.sfntRevision is {soft_lang_ffobz.sfntRevision}") 
        print(f"inglish_ffobz sfnt_names is {soft_lang_ffobz.sfnt_names}") 
        print("####################")
        ########
    soft_lang_ffobz.close()
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
    # for encoding in ("englosoftw8","englodotw8","onlyw8",) :
    for ftype in ("utf","asc","mono",) :
        soft_2_indik(sfdroot,ftype)


