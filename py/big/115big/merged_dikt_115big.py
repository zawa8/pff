#!/usr/bin/python3
# from eng2hin_dict_115_big import eng2hin_dict_115_big
eng2hin_dict_115_big={
    ":" : 2307, "X" : 2309,
    "k" : 2325,"K" : 2326, "g" : 2327, "G" : 2328, "N" : 2329,
    "c" : 2330, "C" : 2331, "z" : 2332, "Z" : 2333,
    "t" : 2335, "T" : 2336, "d" : 2337, "D" : 2338,
    ##### niyu jJqQ bilo
    "j" : 2340,"J" : 2341, "q" : 2342, "Q" : 2343,
    ##### niyu jJqQ up
    "n" : 2344,
    "p" : 2346, "f" : 2347, "b" : 2348, "B" : 2349, "m" : 2350,
    "y" : 2351, "r" : 2352, "l" : 2354, "w" : 2357,
    # "R" : 2353, "L" : 2355,
    # S(sh) is 2 before s wery important V=H
    "S" : 2358, "s" : 2360, "V" : 2361,
    "A" : 2366, "i" : 2368, "u" : 2369, "e" : 2375, "o" : 2379,
    "." : 2404, "`" : 2387, "'" : 2388,
    "0" : 2406, "1" : 2407, "2" : 2408, "3" : 2409, "4" : 2410,
    "5" : 2411, "6" : 2412, "7" : 2413, "8" : 2414, "9" : 2415,
    "-" : 2416, "?" : 2429,
}
simbl_src_dict={
"cbindu" : 2305, "nbindu" : 2306,
"aa" : 2310, "_i" : 2311, "_u" : 2313, "ri" : 2315, "_e" : 2319, "_o" : 2323,
"nukta" : 2364,
"om" : 2384,
"udatta" : 2385,
"anudtta" : 2386,
"hsdot" : 2417,
"ten" : 76,
# sinhala
"Ae" : 3463, "ae" : 3464, "mb" : 3513,
}
merged_dikt_115big = simbl_src_dict | eng2hin_dict_115_big
if __name__ == '__main__':
    print(merged_dikt_115big)
