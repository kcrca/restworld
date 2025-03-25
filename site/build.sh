#!/bin/sh
std_size=750x483
cd $(dirname $0)
for f in src/*/; do
    if test "$(basename $f)" = "sample_pics"; then
	for img in "$f"/*.png; do
	    out="sample_pics/$(basename $img)"
	    if test "$img" -nt "$out"; then
		echo magick convert $img -scale $std_size $out
		magick convert $img -scale $std_size $out
	    fi
	done
    else
	name=$(dirname $f/.)
	out=$(basename $name)
	if test ! -f $out.gif || find $name -newer $out.gif | grep -q . > /dev/null ; then
	    case $out in
		download) size=32x32;;
		*) size=$std_size
	    esac
	    echo - magick convert -delay 200 $name/\*.png -loop 0 -resize $size $out.gif
	    ls $name/*.png
	    magick convert -delay 200 $name/*.png -loop 0 -scale $size $out.gif
	fi
    fi
done
