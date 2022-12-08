from __future__ import annotations

import random
import sys

from pynecraft import info
from pynecraft.base import parameters
from restworld import ancient, aquatic, arena, banners, biomes, blocks, center, connect, diy, effects, \
    enders, font, friendlies, global_, gui, hud, maps, materials, models, monsters, multimob, nether, paintings, \
    particles, photo, plants, redstone, save, tags, the_end, time, wither
from restworld.world import restworld


def main():
    global experimental
    # Use a constant seed so things appear random, but don't usually change from run to run (helps with diffs)
    random.seed(0xb00f)
    if len(sys.argv) > 1:
        restworld.experimental = True
    version = '1.19.3'
    if restworld.experimental:
        info.woods = info.woods + ('Bamboo',)
        version += '+x'
    parameters.version = version
    for m in (
            blocks, save, multimob, models, ancient, global_, aquatic, arena, banners, biomes, center, connect, gui,
            diy, effects, particles, enders, font, friendlies, hud, materials, monsters, nether, paintings, photo,
            plants, redstone, the_end, time, wither, maps):
        m.room()
    tags.tags()
    dir = '/Users/kcrca/clarity/home/saves/Restworld_1.19.3'
    if restworld.experimental:
        dir += '+x'
    restworld.save(dir)


if __name__ == '__main__':
    main()
