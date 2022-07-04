from __future__ import annotations

from pyker.commands import r, mc, entity, Entity, Score, NORTH, EAST, SOUTH, WEST
from pyker.simpler import WallSign
from restworld.rooms import Room
from restworld.world import restworld, fast_clock, slow_clock, main_clock


def room():
    room = Room('center', restworld)

    room.function('example_painting_init').add(
        mc.kill(entity().tag('center_painting')),
        mc.summon(Entity('painting', {'variant': 'skeleton', 'Facing': 3, 'Tags': ['center_painting']}), r(0, 3, 0)))
    speed_fast = Score('SPEED_FAST', 'clocks')
    speed_main = Score('SPEED_MAIN', 'clocks')
    speed_slow = Score('SPEED_SLOW', 'clocks')
    room.function('faster_clocks', home=False).add(
        mc.execute().if_().score(speed_fast).matches((13, None)).run().scoreboard().players().remove(speed_fast, 2),
        mc.execute().if_().score(speed_main).matches((13, None)).run().scoreboard().players().remove(speed_main, 6),
        mc.execute().if_().score(speed_slow).matches((13, None)).run().scoreboard().players().remove(speed_main, 10))
    room.function('slower_clocks', home=False).add(
        fast_clock.speed.add(2),
        main_clock.speed.add(6),
        slow_clock.speed.add(10))
    room.function('reset_clocks', home=False).add(
        list(c.speed.set(c.init_speed) for c in restworld.clocks()))

    room.function('lights_init').add(
        WallSign(('This world lets', 'you test how', 'your resource', 'pack looks.')).place((r(1), 101, r(4)), NORTH),
        WallSign(('Everything', 'is here:', 'blocks, mobs,', 'particles, UI, ...')).place((r(-1), 101, r(4)), NORTH),

        WallSign(('Much of it runs', 'on clocks that', 'switch the', 'variant shown.')).place(
            (r(-4), 101, r(1)), EAST),
        WallSign(('This uses', 'less space', 'so things can', 'be closer together.')).place(
            (r(-4), 101, r(-1)), EAST),

        WallSign(('You can also', 'compare things', 'that you may want', 'to make similar.')).place(
            (r(-1), 101, r(-4)), SOUTH),
        WallSign(('For example,', 'wools may be the', 'same pattern with', 'different colors.')).place(
            (r(1), 101, r(-4)), SOUTH),

        WallSign(('The control book', 'lets you change', 'clock speeds', 'and step it.')).place(
            (r(4), 101, r(-1)), WEST),
        WallSign(('The color of the', 'floor blocks under', 'buttons show if', 'clocks are on.')).place(
            (r(4), 101, r(1)), WEST),

        mc.tag(entity().tag('lights_home')).add('fast_lights_home'),
        mc.tag(entity().tag('lights_home')).add('main_lights_home'),
        mc.tag(entity().tag('lights_home')).add('slow_lights_home'),
    )

    def lights_loop(y, block):
        yield mc.fill(r(2, y, 2), r(-2, y, -2), 'redstone_block').replace(block)
        yield mc.clone(r(2, y, 2), r(-2, y, -2), r(-2, 1, -2)).masked()
        yield mc.fill(r(2, y, 2), r(-2, y, -2), block).replace('redstone_block')
        yield mc.clone(r(2, y, 2), r(-2, y, -2), r(-2, 1, -2)).masked()

    room.loop('fast_lights', fast_clock).loop(lambda x: lights_loop(-3, 'stone'), range(0, 1))
    room.loop('main_lights', main_clock).loop(lambda x: lights_loop(-4, 'diamond_block'), range(0, 1))
    room.loop('slow_lights', slow_clock).loop(lambda x: lights_loop(-5, 'emerald_block'), range(0, 1))

    all = {'Tags': ['center', 'mob_display'], 'PersistenceRequired': True}
    room.function('mobs_display_init').add(
        mc.kill(entity().tag('mob_display')),

        mc.summon('cow', r(-6, 2.5, 0), all),
        mc.summon('polar_bear', r(-6, 2.5, 0), all),
        mc.summon('panda', r(-6, 2.5, 0), all),
        mc.summon('horse', r(-6, 2.5, 0), all),

        mc.summon('turtle', r(6, 2.5, 0), all),
        mc.summon('llama', r(6, 2.5, 0), all),
        mc.summon('mooshroom', r(6, 2.5, 0), all),
        mc.summon('pig', r(6, 2.5, 0), all),

        mc.kill(entity().type('item')),
    )
