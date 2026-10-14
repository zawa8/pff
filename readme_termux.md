# Termux Setup for pff (FontForge Project)

## Environment
- Android + Termux + proot-distro + Ubuntu
- FontForge: fontforge-nox version 20230101
- Project path: /data/data/com.termux/files/home/pff/

## How to Enter Ubuntu
proot-distro login ubuntu

## How to Exit Ubuntu
exit

## Alias
alias ffz='PYTHONIOENCODING=utf-8 /usr/bin/timeout 3600 /usr/bin/fontforge -lang=py -script'

Load alias:
source ~/.bashrc

## Run Main Script
proot-distro login ubuntu
cd /data/data/com.termux/files/home/pff
ffz pysk/xi52py/main.py

## Script Structure
- main.py runs 18 steps (step 1/18 to 18/18)
- Each step calls a separate .py file
- Logs saved in logs/ folder
- Output fonts in sfd/, sfdsrc/, xnglofonts/

## Progress
- Step 2: 78 glyphs copied from English
- Step 3: xi38asc -> xi38utf (copy 128 + unicode refs)
- Step 4: xi52asc -> xi52utf (copy + refs)
- Step 5: xi52utf unicode-range refs added (slow but completed)

## Problems Solved
1. FontForge hang -> pkill -9 fontforge fixes it
2. Unicode error -> PYTHONIOENCODING=utf-8 fixes it
3. timeout was Rust coreutils -> use full path /usr/bin/timeout
4. -c mode open() failed -> use -script mode instead
5. --list-phases argument caused hang -> do not pass extra arguments

## Useful Commands
pkill -9 fontforge; pkill -9 python3
ffz -version
tail -20 /data/data/com.termux/files/home/pff/logs/*.log
ls -la /data/data/com.termux/files/home/pff/pysk/xi52py/
ffz pysk/xi52py/main.py 2>&1 | tee /tmp/full_run.log

## Important Paths
- Termux home: /data/data/com.termux/files/home/
- Ubuntu root: /root/
- Project: /data/data/com.termux/files/home/pff/
- Main script: pysk/xi52py/main.py
- Logs: logs/
- Phone storage: /sdcard/

## Notes
- Step 5 is slow (not hang), may take several minutes
- Do NOT pass extra arguments like --list-phases to ffz
- If script hangs, press Ctrl+C then run pkill -9 fontforge
- Timeout is set to 3600 seconds (1 hour) for long runs
