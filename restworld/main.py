from __future__ import annotations

import argparse
import random

from pynecraft.base import parameters
from restworld import ancient, aquatic, arena, banners, biomes, blocks, center, connect, diy, effects, \
    enders, font, friendlies, global_, gui, hud, maps, materials, models, monsters, multimob, nether, paintings, \
    particles, photo, plants, redstone, save, tags, the_end, time, wither
from restworld.world import restworld


def main():
    global experimental

    # Use a constant seed so things appear random, but don't usually change from run to run (helps with diffs)
    random.seed(0xb00f)

    cmdline = argparse.ArgumentParser()
    cmdline.add_argument('version', type=str, default='1.19.3')
    cmdline.add_argument('--mcversion', type=str)
    args = cmdline.parse_args()
    version = args.version
    restworld.experimental = '+x' in version
    mc_version = args.mcversion
    if not mc_version:
        mc_version = version
    parameters.version = mc_version
    for m in (
            blocks, save, multimob, models, ancient, global_, aquatic, arena, banners, biomes, center, connect, gui,
            diy, effects, particles, enders, font, friendlies, hud, materials, monsters, nether, paintings, photo,
            plants, redstone, the_end, time, wither, maps):
        m.room()
    tags.tags()
    dir = f'/Users/kcrca/clarity/home/saves/RestWorld_{version}'
    print(dir)
    restworld.save(dir)


if __name__ == '__main__':
    main()
