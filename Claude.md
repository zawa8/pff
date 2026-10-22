hi claude please help to correct some python scripts
( https://github.com/zawa8/pff/blob/main/pysk/xi52py/glyph_copy/build_utf_fonts.py ) .
in 10 indic unicode ranges from 0x900-0x97F,0x980-0x9FF ,,,, 0xD00-0xD7F,0xD80-0xDFF
refence of glyphs are not getting pasted
as per https://github.com/zawa8/pff/blob/main/sfdsrc/asc-to-utf.json .
kindly find why build_utf_fonts.py---> _add_ref(utf_font, dst_unicode, src_ascii)
is unable to add(paste) copyref in destination locations as per sfdsrc/asc-to-utf.json file.