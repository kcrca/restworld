#!/bin/sh
cd $(dirname $0)
for f in src/*/; do
    name=$(dirname $f/.)
    out=$(basename $name)
    if test ! -f $out.gif || find $name -newer $out.gif | grep -q . > /dev/null ; then
	case $out in
	    download) size=32x32;;
	    *) size=750x483
	esac
	echo - convert -delay 200 $name/\*.png -loop 0 -resize $size $out.gif
	ls $name/*.png
	convert -delay 200 $name/*.png -loop 0 -scale $size $out.gif
    fi
done
