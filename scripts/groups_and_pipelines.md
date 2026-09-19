we will cenz *xv* to *xh* (xNglohinDi)
g1(aiueohNRLYVWPF) : xe52->xe38->xh52->xh38
g2(EIOUMX) : xe52->xh52 , notomath->xe38->xh38
g3(cCgGDqQTjJ) : xe52->xe38->xh52 , notohindi -> xh38
g4(bdfklmnprstwyzKSZ) : xe52->xe38 , notohindi->xh38->xh52
g5(vHxA) : xe52->xe38 , notohindi->xh38->open xlang*38asc.sfd in fontforge and wait till all fontforge window gets sawed and closed->copy in xlang*52asc.sfd
at last generate fonts from *asc.sfd.

in g5 for dizain open x*38.sfd in fontforge 
3 pipelines :
1) asc: using g1-g5 create *asc.sfd for 52 and 38 series. generate asc fonts.
2) *asc.sfd --copy 128-> *utf.sfd -> copy ref start 128 glyph to 10 unicode ranges. generate utf fonts.
3) create *ascmono.sfd from *asc.sfd and *utfmono.sfd with .sfd name changes for mono.
4) make width ekual in mono from maksimum width in 65-128 glyphs.
5) center align glyphs in all mono.
6) generate mono fonts.
7) ask  for git commit and push or git restore *.sfd.