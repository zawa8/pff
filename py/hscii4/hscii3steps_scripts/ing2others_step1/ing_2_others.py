#!/usr/bin/python3
import fontforge
############### "ing",
def ing_2_others(sfdroot,encoding,ftype,tpl):
    sfddir=f"{sfdroot}/{encoding}/{encoding}{ftype}/"
    ffobz_ing = fontforge.open(f"{sfddir}/inglish{encoding}{ftype}.sfd")
    languages = (
        "hindi",
        "bangla","guzrati","gurmukhi","oriya",
        "korean",
        "telugu","tamil","kannada","malayalam","sinhala",
        #"binaryw",
    )
    for lang in languages:
        ffobz_lang = fontforge.open(f"{sfddir}/{lang}{encoding}{ftype}.sfd")
        print(f"ffobz_lang file_path is {ffobz_lang.path} family name is {ffobz_lang.familyname}")
        ########
        for loc in tpl:
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
    tpl_englodot = (
        "v", "w", "x", "j", "J", "q", "Q", ##uncomment for dot fonts
    )
    tpl_englosoft = (
        "v", "w", "x", "j", "J", "q", "Q", ##uncomment for dot fonts
    )
    tpl_only = (
        # "v", "w", "x", "j", "J", "q", "Q", ##uncomment for dot fonts        
    )
    #########
    encoding = "englodotw8"
    for ftype in ("utf","asc","mono"):
        ing_2_others(sfdroot,encoding,ftype,tpl_englodot)
    #########
    encoding = "englosoftw8"
    for ftype in ("utf","asc","mono"):
        ing_2_others(sfdroot,encoding,ftype,tpl_englosoft)
    #########
    # encoding = "onlyw8"
    # for ftype in ("utf","asc","mono"):
    #     ing_2_others(sfdroot,encoding,tpl_only)
    #########