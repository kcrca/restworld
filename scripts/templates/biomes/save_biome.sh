#!/bin/zsh
set -x
if [[ -z "${1}" ]]; then
    echo usage: $0 biome
    exit 0
fi
files=(~/clarity/home/saves/Biomes1.15.2/generated/minecraft/structures/${1}_[1-9].nbt)
if [[ $#files < 4 ]]; then
    echo Missing some files, we have only:
    ls $files
    exit 1
fi
cp $files ~/clarity/home/saves/RestWorld/generated/minecraft/structures/
