#!/bin/bash
############################
zw8dir="/home/viml/mg/zw8"
pffdir="${zw8dir}/pff"
smallsfddir="${pffdir}/sfd/small/"
bigsfddir="${pffdir}/sfd/big/"
fontdir="${zw8dir}/font"
#### thisdir="${pffdir}/py" ######
thisdir="$(pwd)"
############################
bigttfdir="${fontdir}/bigttf"
bigwoffdir="${fontdir}/bigwoff"
smallttfdir="${fontdir}/smallttf"
smallwoffdir="${fontdir}/smallwoff"
hsciittfdir="${fontdir}/hsciittf"
hsciiwoffdir="${fontdir}/hsciiwoff"
mkdir -p ${bigttfdir} ${bigwoffdir} ${smallttfdir} ${smallwoffdir} ${hsciittfdir} ${hsciiwoffdir}
tree ${fontdir}
#exit
############################printf "pffdir is %s \n" ${pffdir}

############################
declare -a small15arr=("15ms" "15s" "115s")
for i in "${small15arr[@]}"
do
	currsmalldir="source${i}"
	printf "generating ttf/woff2 fonts in ${small15dir}\n"
	cd ${smallsfddir}/${currsmalldir}/ ; sed -E -i 's/.*lookup.*//' *[a-z]${i}.sfd ; ./convert.pe *[a-z]${i}.sfd ; 
	mkdir -p ${smallttfdir}/${i} ${smallwoffdir}/${i}
	mv *[a-z]${i}.ttf ${smallttfdir}/${i}/
	mv *[a-z]${i}.woff2 ${smallwoffdir}/${i}/
done
tree ${fontdir}
############################
############################
declare -a big15arr=("15mb" "15b" "115b")
for i in "${big15arr[@]}"
do
	currbigdir="source${i}"
	printf "generating ttf/woff2 fonts in ${big15dir}\n"
	cd ${bigsfddir}/${currbigdir}/ ; sed -E -i 's/.*lookup.*//' *[a-z]${i}.sfd ; ./convert.pe *[a-z]${i}.sfd ; 
	mkdir -p ${bigttfdir}/${i} ${bigwoffdir}/${i}
	mv *[a-z]${i}.ttf ${bigttfdir}/${i}/
	mv *[a-z]${i}.woff2 ${bigwoffdir}/${i}/
done
tree ${fontdir}
############################
cd ${thisdir}
############################
