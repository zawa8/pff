#!/usr/bin/python3
import fontforge
############### "ing",
def ingsoftutf_2_othering(sfdroot,encoding,ftype):
    ffobz_inglishenglosoftw8mono = fontforge.open(f"{sfdroot}/englosoftw8/englosoftw8mono/inglishenglosoftw8mono.sfd")
    sfddir=f"{sfdroot}/{encoding}/{encoding}{ftype}/"
    ffobz_ing = fontforge.open(f"{sfddir}/inglish{encoding}{ftype}.sfd")
    print(f"ffobz_ingenglosoftw8utf file_path is {ffobz_inglishenglosoftw8mono.path} family name is {ffobz_inglishenglosoftw8mono.familyname}")
    print(f"ffobz_ing file_path is {ffobz_ing.path} family name is {ffobz_ing.familyname}")
    ########
    ffobz_inglishenglosoftw8mono.selection.select(("ranges", None), "!", "~")
    ffobz_inglishenglosoftw8mono.copy()
    ffobz_ing.selection.select(("ranges", None), "!", "~")
    ffobz_ing.paste()
    ######## 
    ffobz_ing.save()
    ffobz_ing.close()
        ########        
    ffobz_inglishenglosoftw8mono.close()
##############
if __name__ == "__main__":
    sfdroot = "/home/viml/mg/zw8/pff/sfd/"
    for encoding in ("englodotw8","onlyw8"):
        ingsoftutf_2_othering(sfdroot,encoding,"mono")
