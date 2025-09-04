from __future__ import annotations

import argparse
import random
from pathlib import Path

from pynecraft.simpler import Sign
from restworld import arena, banners, biomes, blocks, center, connect, dialogs, diy, effects, enders, font, global_, \
    gui, hud, maps, materials, mobs, models, multimob, nether, paintings, particles, photo, plants, \
    redstone, save, tags, test_blocks, tester, the_end, time, wither
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
    test_blocks.tests()
    for r in (tags, dialogs):
        r.create()
    for m in (
            materials, multimob, redstone, connect,
            photo, blocks, save, models, arena, banners, biomes, center, gui, diy, effects,
            particles, enders, font, mobs, hud, nether, paintings, plants, the_end, time,
            wither, maps):
        m.room()
    global_.room()  # This msut be last
    dir = f'{Path.home()}/clarity/home/saves/RestWorld_{args.version}'
    print(dir)
    restworld.save(dir)


if __name__ == '__main__':
    main()
