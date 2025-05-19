#!/usr/bin/python3
import fontforge
# import sys
from uhin_dikt import uhin_dikt
print(uhin_dikt)
utftot = (
    ("cbindu", "cbindu", "nbindu", "colon",
     "_e", "x", "a", "_i", "_i", "_u", "_u", "ri", "l", "_e", "_e", "_e", "_e", "_o", "_o", "_o", "_o",
     "k", "K", "g", "G", "N", "c", "C", "z", "Z", "n", "t", "T", "d", "D", "n", "j", "J", "q", "Q", "n", "n",
     "p", "f", "b", "B", "m", "y", "r", "r", "l", "l", "l", "w", "S", "s", "s", "v",
     "e", "i", "nukta", "nukta", "a", "spesl", "i", "u", "u", "ri", "ri", "e", "e", "e", "e", "o", "o", "o", "o", "nukta",
     "null", "o", "om", "udatta", "anudtta", "`", "'", "e", "u", "u",
     "k", "K", "g", "z", "d", "D", "f", "y", "ri", "l", "l", "l", ".", ".",
     "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "hsdot",
     "x", "_e", "_o", "_o", "_u", "_u", "q", "Z", "y", "g", "z", "?", "d", "b",
    ),
    ("spesl", "cbindu", "nbindu", "colon",
     "_e", "x", "a", "_i", "_i", "_u", "_u", "ri", "l", "_e", "_e", "_e", "_e", "_o", "_o", "_o", "_o",
     "k", "K", "g", "G", "N", "c", "C", "z", "Z", "n", "t", "T", "d", "D", "n", "j", "J", "q", "Q", "n", "n",
     "p", "f", "b", "B", "m", "y", "r", "r", "l", "l", "l", "w", "S", "s", "s", "v",
     "null", "null", "nukta", "nukta",
     "a", "spesl", "i", "u", "u", "ri", "ri", "null", "null", "spesl", "spesl", "null", "null", "spesl", "spesl", "nukta", "j", "null", "null", "null", "null", "null", "null", "null", "null", "o", "null", "null", "null", "null", "d", "D", "null", "y", "ri", "l", "l", "l", ".", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "r", "w", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "nbindu", "-", "nukta", "null" ),
    ("cbindu", "cbindu", "nbindu", "colon",
     "_e", "x", "a", "_i", "_i", "_u", "_u", "ri", "l", "_e", "_e", "_e", "_e", "_o", "_o", "_o", "_o",
     "k", "K", "g", "G", "N", "c", "C", "z", "Z", "n", "t", "T", "d", "D", "n", "j", "J", "q", "Q", "n", "n",
     "p", "f", "b", "B", "m", "y", "r", "r", "l", "l", "l", "w", "S", "s", "s", "v",
     "null", "null", "nukta", "nukta", "a", "spesl", "i", "u", "u", "ri", "ri", "null", "null", "e", "e", "null", "null", "o", "o", "nukta",
     "null", "null", "null", "udatta", "null", "null", "null", "null", "null", "null", "null", "K", "g", "z", "d", "D", "f", "null", "ri", "l", "l", "l", ".", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "nbindu", "cbindu", "i", "u", "spesl", "y", "-", "null", "null", "null", "null", "null", "null", "null", "null", "null"),
    ("cbindu", "cbindu", "nbindu", "colon", "_e", "x", "a", "_i", "_i", "_u", "_u", "ri", "l", "_e", "_e", "_e", "_e", "_o", "_o", "_o", "_o", "k", "K", "g", "G", "N", "c", "C", "z", "Z", "n", "t", "T", "d", "D", "n", "j", "J", "q", "Q", "n", "n", "p", "f", "b", "B", "m", "y", "r", "r", "l", "l", "l", "w", "S", "s", "s", "v", "null", "null", "nukta", "nukta", "a", "spesl", "i", "u", "u", "ri", "ri", "e", "null", "e", "e", "o", "null", "o", "o", "nukta", "null", "null", "om", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "ri", "l", "l", "l", ".", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "r", "null", "null", "null", "null", "null", "null", "null", "Z", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl" ),
    ("cbindu", "cbindu", "nbindu", "colon", "_e", "x", "a", "_i", "_i", "_u", "_u", "ri", "l", "_e", "_e", "_e", "_e", "_o", "_o", "_o", "_o", "k", "K", "g", "G", "N", "c", "C", "z", "Z", "n", "t", "T", "d", "D", "n", "j", "J", "q", "Q", "n", "n", "p", "f", "b", "B", "m", "y", "r", "r", "l", "l", "l", "w", "S", "s", "s", "v", "null", "null", "nukta", "nukta", "a", "i", "i", "u", "u", "ri", "ri", "null", "null", "spesl", "spesl", "null", "null", "spesl", "spesl", "nukta", "null", "null", "null", "null", "null", "null", "null", "spesl", "e", "o", "null", "null", "null", "null", "r", "D", "null", "y", "ri", "l", "l", "l", ".", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "spesl", "w", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "null", "null", "null", "null", "null", "null", "null", "null"),
    ("null", "null", "nbindu", "colon", "_e", "x", "a", "_i", "_i", "_u", "_u", "ri", "l", "_e", "_e", "_e", "_e", "_o", "_o", "_o", "_o", "k", "K", "g", "G", "N", "c", "C", "z", "Z", "n", "t", "T", "d", "D", "n", "j", "J", "q", "Q", "n", "n", "p", "f", "b", "B", "m", "y", "r", "r", "l", "l", "l", "w", "S", "s", "s", "v", "null", "null", "nukta", "nukta", "a", "i", "i", "u", "u", "ri", "ri", "null", "spesl", "spesl", "spesl", "null", "spesl", "spesl", "spesl", "nukta", "null", "null", "om", "null", "null", "null", "null", "null", "null", "o", "null", "null", "null", "null", "null", "null", "null", "null", "ri", "l", "l", "l", ".", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "ten", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "null", "null", "null", "null", "null"),
    ("cbindu", "cbindu", "nbindu", "colon", "_e", "x", "a", "_i", "_i", "_u", "_u", "ri", "l", "_e", "_e", "_e", "_e", "_o", "_o", "_o", "_o", "k", "K", "g", "G", "N", "c", "C", "z", "Z", "n", "t", "T", "d", "D", "n", "j", "J", "q", "Q", "n", "n", "p", "f", "b", "B", "m", "y", "r", "r", "l", "l", "l", "w", "S", "s", "s", "v", "null", "null", "nukta", "nukta", "a", "i", "i", "u", "u", "ri", "ri", "null", "e", "e", "e", "null", "o", "o", "o", "nukta", "null", "null", "null", "null", "null", "null", "null", "o", "e", "null", "s", "z", "r", "null", "null", "n", "null", "null", "ri", "l", "l", "l", ".", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "null", "null", "null", "null", "null", "null", "null", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl"),
    ("cbindu", "cbindu", "nbindu", "colon", "_e", "x", "a", "_i", "_i", "_u", "_u", "ri", "l", "_e", "_e", "_e", "_e", "_o", "_o", "_o", "_o", "k", "K", "g", "G", "N", "c", "C", "z", "Z", "n", "t", "T", "d", "D", "n", "j", "J", "q", "Q", "n", "n", "p", "f", "b", "B", "m", "y", "r", "r", "l", "l", "l", "w", "S", "s", "s", "v", "null", "null", "nukta", "nukta", "a", "i", "i", "u", "u", "ri", "ri", "null", "e", "e", "e", "null", "o", "o", "o", "nukta", "null", "null", "null", "null", "null", "null", "null", "spesl", "spesl", "null", "null", "null", "null", "null", "null", "n", "l", "null", "ri", "l", "l", "l", ".", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "ten", "spesl", "spesl", "spesl", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null"),
    ("cbindu", "cbindu", "nbindu", "colon", "_e", "x", "a", "_i", "_i", "_u", "_u", "ri", "l", "_e", "_e", "_e", "_e", "_o", "_o", "_o", "_o", "k", "K", "g", "G", "N", "c", "C", "z", "Z", "n", "t", "T", "d", "D", "n", "j", "J", "q", "Q", "n", "n", "p", "f", "b", "B", "m", "y", "r", "r", "l", "l", "l", "w", "S", "s", "s", "v", "spesl", "cbindu", "nukta", "spesl", "a", "i", "i", "u", "u", "ri", "ri", "null", "spesl", "spesl", "spesl", "null", "spesl", "spesl", "spesl", "nukta", "cbindu", "o", "null", "null", "null", "null", "m", "y", "l", "o", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "ri", "l", "l", "l", ".", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "spesl", "n", "n", "r", "l", "l", "k"),
    ("null", "cbindu", "nbindu", "colon", "null", 
    "x", "a", "Ae", "ae", "_i", "_i", "_u", "_u", "r", "ri", "l", "l", "_e", "_e", "_e", "o", "o", "o", 
    "null", "null", "null", 
    "k", "K", "g", "G", "N", "N", 
    "c", "C", "z", "Z", "n", "n", "n", 
    "t", "T", "d", "D", "n", "n", "t", "T", "d", "D", "n",
    "null", "n", 
    "p", "f", "b", "B", "m", "mb", "y", "r", "null", "l", "null", "null",
    "w", "S", "s", "s", "v", "l", "f",
    "null", "null", "null", "nukta", "null", "null", "null", "null",
    "a", "e", "ae", "i", "i", "u", "null", "u", "null", "ri", "e", "e", "e", "o", "o", "o", "l",
    "null", "null", "null", "null", "null", "null",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "null", "null",
    "ri", "l", "spesl", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null")
)
# for langi in range(len(utftot)):
#     print(f"langi is {langi} . len(utftot[{langi}]) is {len(utftot[langi])}")
# exit()

################
def uhin_2_others(sfdroot,encoding):
    sfddir = f"{sfdroot}/{encoding}/{encoding}utf/"
    langscripts = (
        "inglish",
        "hindi",
        "bangla","guzrati","gurmukhi","oriya",
        "korean",
        "telugu","tamil","kannada","malayalam","sinhala"
        # "binaryw","binaryh","heks",
    )
    startpoint = 0x900
    for lscript in langscripts:
        ffobz_lscript_utf = fontforge.open(f"{sfddir}/{lscript}{encoding}utf.sfd")
        print(f"ffobz_lscript_utf path is {ffobz_lscript_utf.path} . ffobz_lscript_utf familyname is {ffobz_lscript_utf.familyname}")
        for langi in range(10): #(len(utftot)):
            for remainder_i in range(128): #(len(utftot[langi])):
                trglok = startpoint + 128*langi + remainder_i
                print(f"langi is {langi} . remainder_i is {remainder_i} and target_i is {trglok}")
                utf_glyph_name = utftot[langi][remainder_i]
                if utf_glyph_name in uhin_dikt:
                    srclok = uhin_dikt[utf_glyph_name]
                    print(f"utf_glyph_name is {utf_glyph_name} and srclok is {srclok} and trglok is {trglok}")
                    if srclok != trglok:
                        print(f"{srclok} not ekual to {trglok}")
                        ffobz_lscript_utf.selection.select(srclok)
                        ffobz_lscript_utf.copyReference()
                        ffobz_lscript_utf.selection.select(trglok)
                        ffobz_lscript_utf.clear()
                        ffobz_lscript_utf.paste()
        ffobz_lscript_utf.save()
        ffobz_lscript_utf.close()
##############
if __name__ == "__main__":
    sfdroot=f"/home/viml/mg/zw8/pff/sfd/"
    for encoding in ("englodotw8","englosoftw8","onlyw8"):
        uhin_2_others(sfdroot,encoding)
