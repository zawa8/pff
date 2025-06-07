#!/usr/bin/python3
import fontforge
############### "ing",
def ing_2_langs(sfdroot,encoding,ftype):
    sfddir=f"{sfdroot}/{encoding}/{encoding}{ftype}/"
    ingfullpath=f"{sfddir}/inglish{encoding}{ftype}.sfd"
    print(f"ingfullpath is {ingfullpath}")
    ffobz_ing = fontforge.open(ingfullpath)
    print(f"opened ffobz_ing file_path is {ffobz_ing.path} family name is {ffobz_ing.familyname}")
    print("================")
    languages = (
        "russian",
    )
    for lang in languages:
        ffobz_lang = fontforge.open(f"{sfddir}/{lang}{encoding}{ftype}.sfd")
        print(f"opened ffobz_lang file_path is {ffobz_lang.path} family name is {ffobz_lang.familyname}")
        ########
        ffobz_ing.selection.select(("ranges", None), " ", "G")
        ffobz_ing.copy()
        ffobz_lang.selection.select(("ranges", None), " ", "G")
        ffobz_lang.paste()
        ########
        ffobz_ing.selection.select(("ranges", None), "e", "~")
        ffobz_ing.copy()
        ffobz_lang.selection.select(("ranges", None), "e", "~")
        ffobz_lang.paste()
        ########
        ffobz_ing.selection.select(("ranges", None), "J", "M")
        ffobz_ing.copy()
        ffobz_lang.selection.select(("ranges", None), "J", "M")
        ffobz_lang.paste()
        ########
        ffobz_ing.selection.select(("ranges", None), "T", "W")
        ffobz_ing.copy()
        ffobz_lang.selection.select(("ranges", None), "T", "W")
        ffobz_lang.paste()
        ########
        ing_lang_common_tuple = (
            96,"b","P","Q",
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
    for encoding in ("hscii4w8",):
        for ftype in ("utf","asc","mono"):
            ing_2_langs(sfdroot,encoding,ftype)
    #########
