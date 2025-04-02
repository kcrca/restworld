from __future__ import annotations

from pynecraft.base import EAST, NE, NORTH, NW, Nbt, SE, SOUTH, SW, WEST, r
from pynecraft.commands import Entity, Score, Text, clone, e, execute, fill, function, kill, scoreboard, summon, tag
from pynecraft.info import Horse
from pynecraft.simpler import ItemFrame, Sign, WallSign
from restworld.materials import armor_for
from restworld.rooms import Room
from restworld.world import fast_clock, main_clock, restworld, slow_clock


def room():
    room = Room('center', restworld)

    room.function('example_painting_init').add(
        kill(e().tag('center_painting')),
        summon(Entity('painting', {'variant': 'prairie_ride', 'facing': 3, 'Tags': ['center_painting']}), r(0, 4, 0)))
    speed_fast = Score('SPEED_FAST', 'clocks')
    speed_main = Score('SPEED_MAIN', 'clocks')
    speed_slow = Score('SPEED_SLOW', 'clocks')
    room.function('faster_clocks', home=False).add(
        execute().if_().score(speed_fast).matches((13, None)).run(scoreboard().players().remove(speed_fast, 2)),
        execute().if_().score(speed_main).matches((13, None)).run(scoreboard().players().remove(speed_main, 6)),
        execute().if_().score(speed_slow).matches((13, None)).run(scoreboard().players().remove(speed_slow, 10)))
    room.function('slower_clocks', home=False).add(
        fast_clock.speed.add(2),
        main_clock.speed.add(6),
        slow_clock.speed.add(10))
    room.function('reset_clocks', home=False).add(
        list(c.speed.set(c.init_speed) for c in restworld.clocks()))

    # noinspection GrazieInspection
    step_sign = Sign(('Touch', 'the', 'Sign', 'Blow'), hanging=True, state={'attached': True})
    room.function('lights_init').add(
        WallSign(('This world lets', 'you test how', 'your resource', 'pack looks.')).place((r(1), 101, r(4)), NORTH),
        WallSign(('Almost everything', 'is here: blocks', 'mobs, particles,', 'UI, moon phases ...')).place(
            (r(-1), 101, r(4)), NORTH),

        WallSign(('Clocks switch', 'between variants,', 'which takes', 'less space.')).place((r(-4), 101, r(1)), EAST),
        WallSign(('You can also', 'compare things', 'that you may want', 'to make similar.')).place((r(-4), 101, r(-1)),
                                                                                                    EAST),

        WallSign(('Floor levers and', 'buttons control', 'modes, like floor', 'vs. wall torches.')).place(
            (r(-1), 101, r(-4)), SOUTH),
        WallSign(('Red or green', 'blocks below', 'buttons show if', 'clocks are on.')).place((r(1), 101, r(-4)),
                                                                                              SOUTH),

        WallSign(('The control book', 'lets you change', 'clock speeds', 'and step along.')).place((r(4), 101, r(-1)),
                                                                                                   WEST),
        WallSign(('Also, you might', 'like my "Clarity"', 'pack; a link is in', 'the control book!'),
                 (lambda txt: Text.text(txt).click_event().open_url('https://claritypack.com'),)).place(
            (r(4), 101, r(1)), WEST),

        step_sign.place(r(6, 5, 6), NW),
        Sign(('Go to', 'the', 'Optifine', 'Rooms'), (function('restworld:global/goto_optifine'),), hanging=True).place(r(6, 4, 6), NW),
        step_sign.place(r(6, 5, -6), SW),
        Sign(('Go to', 'the', 'Battle', 'Arena'), (function('restworld:global/goto_arena'),), hanging=True).place(r(6, 4, -6), SW),
        step_sign.place(r(-6, 5, -6), SE),
        Sign(('Go to', 'the', 'Biome', 'Sampler'), (function('restworld:global/goto_biomes'),), hanging=True).place(r(-6, 4, -6), SE),
        step_sign.place(r(-6, 5, 6), NE),
        Sign(('Go to', 'the', 'Photo', 'Area'), (function('restworld:global/goto_photo'),), hanging=True).place(r(-6, 4, 6), NE),

        tag(e().tag('lights_home')).add('fast_lights_home'),
        tag(e().tag('lights_home')).add('main_lights_home'),
        tag(e().tag('lights_home')).add('slow_lights_home'),
    )

    def lights_loop(y, block):
        yield fill(r(2, y, 2), r(-2, y, -2), 'redstone_block').replace(block)
        yield clone(r(2, y, 2), r(-2, y, -2), r(-2, 1, -2)).masked()
        yield fill(r(2, y, 2), r(-2, y, -2), block).replace('redstone_block')
        yield clone(r(2, y, 2), r(-2, y, -2), r(-2, 1, -2)).masked()

    # The "kill" here is to pick up the scutes the armadillo drops occasionally; could add a loop just for this
    room.loop('fast_lights', fast_clock).loop(lambda x: lights_loop(-3, 'stone'), range(0, 1)).add(
        kill(e().type('item').distance((None, 25))))
    room.loop('main_lights', main_clock).loop(lambda x: lights_loop(-4, 'diamond_block'), range(0, 1))
    room.loop('slow_lights', slow_clock).loop(lambda x: lights_loop(-5, 'emerald_block'), range(0, 1))

    all = {'Tags': ['center', 'mob_display'], 'PersistenceRequired': True}
    trim_stand = Entity('armor_stand', all).tag('center_stand')
    armor_for(trim_stand, 'iron', {'components': {'trim': {'pattern': 'flow', 'material': 'resin'}}})
    silent = Nbt({'Silent': True})
    room.function('mobs_display_init').add(
        summon(Entity('mooshroom', silent).tag('mob_display'), r(-6, 2.5, 0), all),
        summon(Entity('panda', {'MainGene': 'playful', 'Silent': True}).tag('mob_display'), r(-6, 2.5, 0), all),
        summon(Horse('horse', Horse.Color.CHESTNUT, Horse.Markings.WHITE, silent).tag('mob_display'), r(-6, 2.5, 0),
               all),
        summon(Entity('pig', silent.merge({'variant': 'cold'})).tag('mob_display'), r(-6, 2.5, 0), all),

        summon(Entity('llama', silent).tag('mob_display'), r(6, 2.5, 0), all),
        summon(Entity('cow', silent.merge({'variant': 'warm'})).tag('mob_display'), r(6, 2.5, 0), all),
        summon(Entity('piglin_brute', silent.merge({'IsImmuneToZombification': True})).tag('mob_display'), r(6, 2.5, 0),
               all),
        summon(Entity('armadillo', silent).tag('mob_display'), r(6, 2.5, 0), all),

        trim_stand.summon(r(10.51, 2, 0), facing=NORTH),

        kill(e().type('item')),
    )
    messages = (None, Text.text('F u cn rd ths').obfuscated(True),
                Text.text('u cd b hm by nw').obfuscated(True).extra(Text.text('‽').obfuscated(False)))
    room.function('plants_display_init').add(WallSign(messages).place(r(5, 3, -4), SOUTH))
    room.function('materials_display_init').add(ItemFrame(WEST).item('clock').tag('mob_display').summon(r(4, 4, 5)))
