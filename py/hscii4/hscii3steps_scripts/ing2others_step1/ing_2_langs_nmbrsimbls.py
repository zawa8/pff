#!/usr/bin/python3
import fontforge
############### "ing",
def ing_2_langs_nmbrsimbls(sfdroot,encoding,ftype):
    sfddir=f"{sfdroot}/{encoding}/{encoding}{ftype}/"
    ffobz_ing = fontforge.open(f"{sfddir}/inglish{encoding}{ftype}.sfd")
    print(f"opened ffobz_ing file_path is {ffobz_ing.path} family name is {ffobz_ing.familyname}")
    print("================")
    languages = (
        "hindi",
        "bangla","guzrati","gurmukhi","oriya",
        "korean",
        "telugu","tamil","kannada","malayalam","sinhala",
    )
    for lang in languages:
        ffobz_lang = fontforge.open(f"{sfddir}/{lang}{encoding}{ftype}.sfd")
        print(f"opened ffobz_lang file_path is {ffobz_lang.path} family name is {ffobz_lang.familyname}")
        ########
        ffobz_ing.selection.select(("ranges", None), " ", "@")
        ffobz_ing.copy()
        ffobz_lang.selection.select(("ranges", None), " ", "@")
        ffobz_lang.paste()
        ########
        ffobz_ing.selection.select(("ranges", None), "[", "`")
        ffobz_ing.copy()
        ffobz_lang.selection.select(("ranges", None), "[", "`")
        ffobz_lang.paste()
        ########
        ffobz_ing.selection.select(("ranges", None), "{", "~")
        ffobz_ing.copy()
        ffobz_lang.selection.select(("ranges", None), "{", "~")
        ffobz_lang.paste()
        ########
        ffobz_ing.selection.select(("ranges", None), 0x80, 0x9F)
        ffobz_ing.copy()
        ffobz_lang.selection.select(("ranges", None), 0x80, 0x9F)
        ffobz_lang.paste()
        ########
        ing_lang_common_tuple = (
            "L","Y","V","W","P","F", ## hex
            "a","i","u","e","o","h","c","g",
            "A","I","U","E","O","H","C","G",
            "M","N","R","X",
        )
        ########
        for loc in ing_lang_common_tuple:
            ffobz_ing.selection.select(loc)
            ffobz_ing.copy()
            ffobz_lang.selection.select(loc)
            #ffobzlang.clear()
            ffobz_lang.paste()
        ######## 
        ffobz_lang.save()
        ffobz_lang.close()
        ########        
    ffobz_ing.close()
##############
if __name__ == "__main__":
    sfdroot = "/home/viml/mg/zw8/pff/sfd/"
    #########
    for encoding in ("englodotw8","englosoftw8","onlyw8"):
        for ftype in ("utf","asc","mono"):
            ing_2_langs_nmbrsimbls(sfdroot,encoding,ftype)
    #########
