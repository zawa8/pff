#!/usr/bin/python3
import fontforge
############### "ing",
def ing_2_langs(sfdroot,encoding,ftype):
    sfddir=f"{sfdroot}/{encoding}/{encoding}{ftype}/"
    ffobz_inglish = fontforge.open(f"{sfddir}/inglish{encoding}{ftype}.sfd")
    print(f"opened ffobz_inglish file_path is {ffobz_inglish.path} family name is {ffobz_inglish.familyname}")
    print("================")
    languages = (
        "russian",
    )
    for lang in languages:
        ffobz_lang = fontforge.open(f"{sfddir}/{lang}{encoding}{ftype}.sfd")
        print(f"opened ffobz_lang file_path is {ffobz_lang.path} family name is {ffobz_lang.familyname}")
        ########
        ffobz_inglish.selection.select(("ranges", None), " ", "A")
        ffobz_inglish.copy()
        ffobz_lang.selection.select(("ranges", None), " ", "A")
        ffobz_lang.paste()
        ########
        ffobz_inglish.selection.select(("ranges", None), "[", "a")
        ffobz_inglish.copy()
        ffobz_lang.selection.select(("ranges", None), "[", "a")
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
            "j","J","q","Q",
            "t","T",
            "w",
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
    for encoding in ("englosoftw8","englodotw8"):
        for ftype in ("utf","asc","mono"):
            ing_2_langs(sfdroot,encoding,ftype)
    #########
