from __future__ import annotations

import random

from restworld import ancient, aquatic, arena, banners, biomes, blocks, center, connect, diy, effects, \
    enders, font, friendlies, global_, gui, hud, maps, materials, models, monsters, nether, paintings, particles, photo, \
    plants, redstone, tags, the_end, time, wither
from restworld.world import restworld


def main():
    # Use a constant seed so things appear random, but don't usually change from run to run (helps with diffs)
    random.seed(0xb00f)
    for m in (
            models, ancient, global_, aquatic, arena, banners, biomes, blocks, center, connect, gui, diy, effects,
            particles, enders, font, friendlies, hud, materials, monsters, nether, paintings, photo, plants, redstone,
            the_end, time, wither, maps):
        m.room()
    tags.tags()
    restworld.save('/Users/kcrca/clarity/home/saves/RestWorld_1.19.2')


if __name__ == '__main__':
    main()
