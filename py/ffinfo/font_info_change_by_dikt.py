#!/usr/bin/python3
from datetime import datetime
import fontforge
# import uuid
import hashlib

def create_uuid_from_string(val: str):
    hex_string = hashlib.md5(val.encode("UTF-8")).hexdigest()
    return int(hex_string, 16) % 10**16
##############    
def font_info_change_by_dikt(sfddir,old_new_name_dikt):
    for oldname, newname in old_new_name_dikt.items():
        oldfontname = f"{oldname}"
        oldsfdname = f"{oldfontname}.sfd"
        newfontname = f"{newname}"
        newsfdname = f"{newfontname}.sfd"
        fontfileobzekt = fontforge.open(f"{sfddir}/{oldsfdname}")
        print("####################")
        print(f"oldsfdname is {oldsfdname}. newsfdname is {newsfdname}.fontfileobzekt file_path is {fontfileobzekt.path}")    
        print("####################")    
        ########
        todayd = datetime.today().strftime('%Y-%m-%d')
        unikname = f"{newfontname} hscii 4finger1thumb 4f1t maths {todayd}"
        fontfileobzekt.familyname = f"{newfontname}"
        fontfileobzekt.fullname = f"{newfontname}"
        fontfileobzekt.fontname = f"{newfontname}"    
        fontfileobzekt.uniqueid = create_uuid_from_string(f"{newfontname} {unikname}")
        fontfileobzekt.copyright = f"github.com/zawa8/font hscii 4finger1thumb 4f1t maths"
        fontfileobzekt.version = f"w0.000"
        fontfileobzekt.os2_vendor = "zawa"    
        # ########
        #f.appendSFNTName(language, strid, string)
        fontfileobzekt.sfntRevision = 1.0000000
        ##############
        fontfileobzekt.appendSFNTName('English (US)', 'UniqueID', f"FontForge 2.0 : {newfontname} : 30-3-2025")
        fontfileobzekt.appendSFNTName('English (US)', 'Fullname', f"{newfontname}")
        fontfileobzekt.appendSFNTName('English (US)', 'UniqueID', f"{unikname} 0.000;zawa;hscii5 {newfontname}-regular")
        fontfileobzekt.appendSFNTName('English (US)', 'PostScriptName', f"{newfontname}")
        fontfileobzekt.appendSFNTName('English (US)', 'Family', f"{newfontname}")
        ##############  
        fontfileobzekt.appendSFNTName('English (US)', 'Version', 'wersion 0.0000')
        fontfileobzekt.appendSFNTName('English (US)', 'Copyright', 'github.com/zawa8/font hscii4(4phinger maths) hscii5')
        fontfileobzekt.appendSFNTName('English (US)', 'SubFamily', 'regular')
        fontfileobzekt.appendSFNTName('English (US)', 'Version', 'wersion 0.0000')
        fontfileobzekt.appendSFNTName('English (US)', 'Trademark', 'hscii5/4 fonts 5/4phingrmaths')
        fontfileobzekt.appendSFNTName('English (US)', 'Manufacturer', 'simbxls hscii github zawa8')
        fontfileobzekt.appendSFNTName('English (US)', 'Designer', 'wimxl kumar merged and changed fonts')
        fontfileobzekt.appendSFNTName('English (US)', 'Descriptor', 'merged changed by zawa8 pff(python fontforge)')
        fontfileobzekt.appendSFNTName('English (US)', 'Vendor URL', 'https://github.com/zawa8/font')
        fontfileobzekt.appendSFNTName('English (US)', 'Designer URL', 'https://github.com/zawa8/pff')
        fontfileobzekt.appendSFNTName('English (US)', 'License', 'license file present in : https://github.com/zawa8/font/')
        fontfileobzekt.appendSFNTName('English (US)', 'License URL', 'https://github.com/zawa8/font')
        # ########
        fontfileobzekt.save(f"{sfddir}/{newsfdname}")
        ########
        print("####  language is {lang}  ####")
        print(f"newsfdname is {newsfdname}.fontfileobzekt file_path is {fontfileobzekt.path}")    
        print(f"ffo family name is {fontfileobzekt.familyname}")
        print(f"ffo fullname is {fontfileobzekt.fullname}")
        print(f"ffo fontname is {fontfileobzekt.fontname}")
        print(f"ffo copyright is {fontfileobzekt.copyright}")
        print(f"ffo version is {fontfileobzekt.version}")
        print(f"ffo uniqueid is {fontfileobzekt.uniqueid}")
        print(f"ffo fondname is {fontfileobzekt.fondname}")
        print(f"ffo os2_vendor is {fontfileobzekt.os2_vendor}")
        print("####################")
        print(f"ffo f.sfntRevision is {fontfileobzekt.sfntRevision}") 
        print(f"ffo sfnt_names is {fontfileobzekt.sfnt_names}") 
        print("####################")
        ########
        fontfileobzekt.close()
##############
if __name__ == "__main__":
    sfddir = "/home/viml/mg/zw8/pff/sfd/englosoftw8/englosoftw8mono/"
    old_new_name_dikt = {
        "inglishw8mono":"inglishenglosoftw8mono",
        "hindiw8mono":"hindienglosoftw8mono", "banglaw8mono":"banglaenglosoftw8mono",
        "guzratiw8mono":"guzratienglosoftw8mono", "gurmukhiw8mono":"gurmukhienglosoftw8mono", "oriyaw8mono":"oriyaenglosoftw8mono",
        "tamilw8mono":"tamilenglosoftw8mono", "teluguw8mono":"teluguenglosoftw8mono", "kannadaw8mono":"kannadaenglosoftw8mono",
        "malayalamw8mono":"malayalamenglosoftw8mono", "sinhalaw8mono":"sinhalaenglosoftw8mono", "koreanw8mono":"koreanenglosoftw8mono",
        "binaryww8mono":"binarywenglosoftw8mono",
        "heksw8mono":"heksenglosoftw8mono",
    }
    font_info_change_by_dikt(sfddir,old_new_name_dikt)
