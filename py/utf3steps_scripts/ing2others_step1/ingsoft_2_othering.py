#!/usr/bin/python3
import fontforge
############### "ing",
def ingsoftutf_2_othering(sfdroot,encoding,ftype):
    ffobz_ingenglosoftw8utf = fontforge.open(f"{sfdroot}/englosoftw8/englosoftw8utf/inglishenglosoftw8utf.sfd")
    sfddir=f"{sfdroot}/{encoding}/{encoding}{ftype}/"
    ffobz_ing = fontforge.open(f"{sfddir}/inglish{encoding}{ftype}.sfd")
    print(f"ffobz_ingenglosoftw8utf file_path is {ffobz_ingenglosoftw8utf.path} family name is {ffobz_ingenglosoftw8utf.familyname}")
    print(f"ffobz_ing file_path is {ffobz_ing.path} family name is {ffobz_ing.familyname}")
    ########
    ffobz_ingenglosoftw8utf.selection.select(("ranges", None), "!", "~")
    ffobz_ingenglosoftw8utf.copy()
    ffobz_ing.selection.select(("ranges", None), "!", "~")
    ffobz_ing.paste()
    ######## 
    ffobz_ing.save()
    ffobz_ing.close()
        ########        
    ffobz_ingenglosoftw8utf.close()
##############
if __name__ == "__main__":
    sfdroot = "/home/viml/mg/zw8/pff/sfd/"

    for encoding in ("englodotw8","onlyw8"):
        for ftype in ("utf","asc"):
            ingsoftutf_2_othering(sfdroot,encoding,ftype)
    #########
    encoding = "englosoftw8"
    for ftype in ("utf","asc","mono"):
        ingsoftutf_2_othering(sfdroot,encoding,"asc")
    #########
    # encoding = "onlyw8"
    # for ftype in ("utf","asc","mono"):
    #     ing_2_others(sfdroot,encoding,tpl_only)
    #########