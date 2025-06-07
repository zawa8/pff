#!/usr/bin/python3
import fontforge
############### "ing",
def ing_2_langs(sfdroot,encoding,ftype):
    sfddir=f"{sfdroot}/{encoding}/{encoding}{ftype}/"
    ffobz_inglish = fontforge.open(f"{sfddir}/inglish{encoding}{ftype}.sfd")
    print(f"opened ffobz_inglish file_path is {ffobz_inglish.path} family name is {ffobz_inglish.familyname}")
    print("================")
    languages = (
        "tamil",
    )
    for lang in languages:
        ffobz_lang = fontforge.open(f"{sfddir}/{lang}onlyw8{ftype}.sfd")
        print(f"opened ffobz_lang file_path is {ffobz_lang.path} family name is {ffobz_lang.familyname}")
        ########
        ffobz_inglish.selection.select(("ranges", None), " ", "I")
        ffobz_inglish.copy()
        ffobz_lang.selection.select(("ranges", None), " ", "I")
        ffobz_lang.paste()
        ########
        ffobz_inglish.selection.select(("ranges", None), "[", "i")
        ffobz_inglish.copy()
        ffobz_lang.selection.select(("ranges", None), "[", "i")
        ffobz_lang.paste()
        ########
        ffobz_inglish.selection.select(("ranges", None), "{", "~")
        ffobz_inglish.copy()
        ffobz_lang.selection.select(("ranges", None), "{", "~")
        ffobz_lang.paste()
        ########
        # ffobz_inglish.selection.select(("ranges", None), 0x80, 0x9F)
        # ffobz_inglish.copy()
        # ffobz_lang.selection.select(("ranges", None), 0x80, 0x9F)
        # ffobz_lang.paste()
        ########
        ing_lang_common_tuple = (
            "L","Y","V","W","P","F", ## hex
            "a","i","u","e","o","h","c","g",
            "A","I","U","E","O","H","C","G",
            "M","N","R","X",
            "w",
            "B","D","q","Q",
        )
        ########
        for loc in ing_lang_common_tuple:
            ffobz_inglish.selection.select(loc)
            ffobz_inglish.copy()
            ffobz_lang.selection.select(loc)
            #ffobzlang.clear()
            ffobz_lang.paste()
        ######## 
        ffobz_lang.save()
        ffobz_lang.close()
        ########        
    ffobz_inglish.close()
##############
if __name__ == "__main__":
    sfdroot = "/home/viml/mg/zw8/pff/sfd/"
    #########
    for encoding in ("onlyw8",):
        for ftype in ("utf","asc","mono"):
            ing_2_langs(sfdroot,encoding,ftype)
    #########
