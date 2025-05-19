#!/usr/bin/python3
import os
import subprocess
import shutil
import fontforge

# Directory paths
thisdir = os.getcwd()
zw8dir = f"/home/viml/mg/zw8"
pffdir = f"{zw8dir}/pff/"
sfdroot = f"{pffdir}/sfd/"
fontroot = f"{zw8dir}/font/"
#######
encodings = ("englodotw8", "englosoftw8", "onlyw8")
ftypes = ("asc", "utf", "mono")
languages = (
    "inglish",  "korean", "russian",
    "hindi", "bangla","guzrati","gurmukhi","oriya",
    "telugu","tamil","kannada","malayalam","sinhala",
    "binaryw","heks",
)
# #######
for encoding in encodings:
    for ftype in ftypes:
        fontlogoname = "hscii"
        ttf_fontdir = f"{fontroot}/ttf/{fontlogoname}/{encoding}/{encoding}{ftype}/"
        woff2_fontdir = f"{fontroot}/woff2/{fontlogoname}/{encoding}/{encoding}{ftype}/"
        os.makedirs(f"{ttf_fontdir}", exist_ok=True)
        os.makedirs(f"{woff2_fontdir}", exist_ok=True)
        for lang in languages:
            sfd_file_path = f"{sfdroot}/{encoding}/{encoding}{ftype}/{lang}{encoding}{ftype}.sfd"
            if os.path.exists(sfd_file_path):
            ##########################
                with open(sfd_file_path, 'r') as f:
                    lines = f.readlines()        
                lines = [line for line in lines if 'lookup' not in line]        
                with open(sfd_file_path, 'w') as f:
                    f.writelines(lines)  
            ##########################
            # font.generate(filename,  flags=,  subfont_directory=, namelist=, layer=)
            ##########################
                ffobz = fontforge.open(f"{sfd_file_path}")
                ttf_font_path = f"{ttf_fontdir}/{lang}{encoding}{ftype}.ttf"
                woff2_font_path = f"{woff2_fontdir}/{lang}{encoding}{ftype}.woff2"
                ffobz.generate(f"{ttf_font_path}")
                ffobz.generate(f"{woff2_font_path}")
                ffobz.close()
            ##########################
##########################
# go to original directory
os.chdir(fontroot)
subprocess.run(["./fonts_linux_install.py"], check=True)
# Tree command equivalent again
# subprocess.run(["tree", fontdir], check=True)
# font install.
os.chdir(thisdir)
