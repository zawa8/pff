#!/usr/bin/python3
from datetime import datetime
import fontforge
# import uuid
import hashlib

def create_uuid_from_string(val: str):
    hex_string = hashlib.md5(val.encode("UTF-8")).hexdigest()
    return int(hex_string, 16) % 10**16

langs = (
    "ing",
    "hindi",
    "bangla","guzrati","gurmukhi","oriya",
    "korean",
    "telugu","tamil","kannada","malayalam","sinhala",
    # "binaryw"
)
for l in langs:
    tudedate = datetime.today().strftime('%Y-%m-%d')
    thisfontname = f"{l}15b"
    unikname = f"{thisfontname} hscii5 5phinger mAThs {tudedate}"
    sfdname = f"{thisfontname}.sfd"
    f = fontforge.open(f"/home/viml/mg/zw8/pff/sfd/b/source15b/{sfdname}")
    print("####################")
    print(f"language is {l} and f path is {f.path}")    
    print("####################")    
    ########
    f.familyname = f"{thisfontname}"
    f.fullname = f"{thisfontname}"
    f.fontname = f"{thisfontname}"    
    f.uniqueid = create_uuid_from_string(f"{thisfontname} {unikname}")
    f.copyright = f"github.com/zawa8/font hscii4(4phinger maths) hscii5"
    f.version = f"w0.000"
    f.os2_vendor = "zawa"    
    # ########
    #f.appendSFNTName(language, strid, string)
    f.sfntRevision = 1.0000000
    ##############
    f.appendSFNTName('English (US)', 'UniqueID', f"FontForge 2.0 : {thisfontname} : 30-3-2025")
    f.appendSFNTName('English (US)', 'Fullname', f"{thisfontname}")
    f.appendSFNTName('English (US)', 'UniqueID', f"{unikname} 0.000;zawa;hscii5 {thisfontname}-regular")
    f.appendSFNTName('English (US)', 'PostScriptName', f"{thisfontname}")
    f.appendSFNTName('English (US)', 'Family', f"{thisfontname}")
    ##############  
    f.appendSFNTName('English (US)', 'Version', 'wersion 0.0000')
    f.appendSFNTName('English (US)', 'Copyright', 'github.com/zawa8/font hscii4(4phinger maths) hscii5')
    f.appendSFNTName('English (US)', 'SubFamily', 'Regular')
    f.appendSFNTName('English (US)', 'Version', 'wersion 0.0000')
    f.appendSFNTName('English (US)', 'Trademark', 'hscii5/4 fonts 5/4phingrmaths')
    f.appendSFNTName('English (US)', 'Manufacturer', 'simbAls hscii4 github zawa8')
    f.appendSFNTName('English (US)', 'Designer', 'wimxl kumar merged and changed fonts')
    f.appendSFNTName('English (US)', 'Descriptor', 'merged changed by zawa8 pff(python fontforge)')
    f.appendSFNTName('English (US)', 'Vendor URL', 'https://github.com/zawa8/font')
    f.appendSFNTName('English (US)', 'Designer URL', 'https://github.com/zawa8/pff')
    f.appendSFNTName('English (US)', 'License', 'please ask phur help/kuery at: https://github.com/zawa8/font/')
    f.appendSFNTName('English (US)', 'License URL', 'https://github.com/zawa8/font')
    # ########
    f.save(f"/home/viml/mg/zw8/pff/sfd/b/source15b/{sfdname}")
    ########
    print("####################")
    print(f"language is {l} and f family name is {f.familyname}")
    print(f"language is {l} and f fullname is {f.fullname}")
    print(f"language is {l} and f fontname is {f.fontname}")
    print(f"language is {l} and f copyright is {f.copyright}")
    print(f"language is {l} and f version is {f.version}")
    print(f"language is {l} and f uniqueid is {f.uniqueid}")
    print(f"language is {l} and f fondname is {f.fondname}")
    print(f"language is {l} and f os2_vendor is {f.os2_vendor}")
    print("####################")
    print(f"language is {l} and f f.sfntRevision is {f.sfntRevision}") 
    print(f"language is {l} and f sfnt_names is {f.sfnt_names}") 
    print("####################")
    ########
    f.close()
    ########