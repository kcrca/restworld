#!/bin/sh
cd $(dirname $0)
world=${1:-RestWorld}
target="$HOME/clarity/home/saves/$world/datapacks/restworld/data/restworld/functions"
if [ ! -d "$target" ]; then
    echo No such directory: $target 1>&2
    exit 1
fi
rm */.f
for f in *; do
    if [ -d $f -a -d $target/$f ]; then
	echo + ln -s $target/$f $f/.f
	ln -s $target/$f $f/.f
    fi
done
