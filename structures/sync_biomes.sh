#!/bin/sh
src=$(dirname $0)/
rwd=$HOME/clarity/home/saves/RestWorld/generated/minecraft/structures/
bio=$HOME/clarity/home/saves/RestWorld_old/generated/minecraft/structures/
args="$@"
test ${#args} = 0

sync() {
    echo $1 '->' $2
    rsync -v -ruW --exclude='tmp*.nbt' --exclude='?[0-9]*.nbt' --include='*.nbt' "$@" | grep nbt
}

sync $rwd $bio
sync $bio $rwd
sync $rwd $src
