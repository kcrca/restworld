from __future__ import annotations

import argparse
import random
from pathlib import Path

from pynecraft.simpler import Sign
from restworld import arena, banners, biomes, blocks, center, connect, diy, effects, enders, font, global_, gui, hud, \
    loot_tables, maps, materials, mobs, models, multimob, nether, paintings, particles, photo, plants, redstone, save, \
    tags, tester, the_end, time, wither
from restworld.world import restworld


def main():
    # Use a constant seed so things appear random, but don't usually change from run to run (helps with diffs)
    random.seed(0xb00f)

    cmdline = argparse.ArgumentParser()
    cmdline.add_argument('version', type=str, default='1.19.3')
    # noinspection SpellCheckingInspection
    cmdline.add_argument('--pynecraft_dev', action=argparse.BooleanOptionalAction)
    args = cmdline.parse_args()
    Sign.waxed = True
    Sign.default_wood = 'pale_oak'
    if args.pynecraft_dev:
        tester.room()
    for m in (
            connect,
            photo, blocks, save, multimob, models, global_, arena, banners, biomes, center, gui, diy, effects,
            particles, enders, font, mobs, hud, materials, nether, paintings, plants, redstone, the_end, time,
            wither, maps):
        m.room()
    tags.tags()
    loot_tables.loot_tables()
    dir = f'{Path.home()}/clarity/home/saves/RestWorld_{args.version}'
    print(dir)
    restworld.save(dir)


if __name__ == '__main__':
    main()
