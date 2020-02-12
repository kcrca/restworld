#!/bin/sh
cd $(dirname $0)
world=${1:-RestWorld}
target="$HOME/clarity/home/saves/$world/datapacks/restworld/data/v3/functions"
rm */.f
for f in *; do
    if [ -d $f -a -d $target/$f ]; then
	echo + ln -s $target/$f $f/.f
	ln -s $target/$f $f/.f
    fi
done
