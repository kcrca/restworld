from __future__ import annotations

from restworld import ancient, aquatic, arena, banners, biomes, blocks, center, connect, containers, diy, effects, \
    enders, font, friendlies, global_, materials, monsters, nether, paintings, particles, photo, plants, redstone, tags, \
    the_end, time, wither
from restworld.world import restworld


def main():
    for f in (
            ancient.room, global_.room, aquatic.room, arena.room, banners.room, biomes.room, blocks.room, center.room,
            connect.room, containers.room, diy.room, effects.room, particles.room, enders.room, font.room,
            friendlies.room, materials.room, monsters.room, nether.room, paintings.room, photo.room, plants.room,
            redstone.room, the_end.room, time.room, wither.room):
        f()
    tags.tags()
    restworld.save()


if __name__ == '__main__':
    main()
