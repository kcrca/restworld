import shutil
import sys

import amulet_nbt
from amulet_nbt import ListTag, StringTag


def main():
    version = '1.19.3'
    dir = f'/Users/kcrca/clarity/home/saves/Restworld_{version}'
    dir_x = dir + '+x'

    shutil.rmtree(dir_x, ignore_errors=True)
    shutil.copytree(dir, dir_x)

    nbt(dir, dir_x)


def nbt(dir, dir_x):
    top = amulet_nbt.load(dir + '/level.dat')
    data = top.compound.get('Data')
    packs = data.get_compound('DataPacks')
    enabled = packs.get_list('Enabled')
    disabled = packs.get_list('Disabled')
    for s in disabled:
        enabled.append(s)
    disabled.clear()
    enabled_features = ListTag((StringTag(f'minecraft:{x}') for x in ('vanilla', 'update_1_20')))
    data['enabled_features'] = enabled_features
    top.save_to(dir_x + '/level.dat')


if __name__ == '__main__':
    # Only run this if any argument is given
    if len(sys.argv) !=1:
       main()
