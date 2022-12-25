from __future__ import annotations

from pynecraft.base import EAST, NORTH, SOUTH, WEST, r
from pynecraft.commands import COLORS, Entity, LONG, RESULT, Score, data, e, execute, function, \
    kill, s, scoreboard, tp
from pynecraft.enums import ScoreCriteria
from pynecraft.info import axolotls, tropical_fish
from pynecraft.simpler import WallSign
from restworld.rooms import Room
from restworld.world import VERSION_1_20, fast_clock, kill_em, main_clock, restworld


def room():
    room = Room('aquatic', restworld, NORTH, (None, 'Aquatic'))
    clock_sign = WallSign((None, 'Clock', 'On / Off'), (function('restworld:global/clock_toggle')))
    height_sign = WallSign((None, 'Change Height'), (function('restworld:global/mob_levitation')))
    reset_sign = WallSign((None, 'Reset Room'), (function('restworld:aquatic/_init')))

    def n_fish_loop(count: int):
        def fish_loop(step):
            for kind, breeds in tropical_fish.items():
                if len(breeds) == count:
                    fish = breeds[step.i]
                    fish.custom_name(True)
                    yield data().merge(e().tag(kind.lower()).limit(1), fish.nbt)

        return fish_loop

    room.loop('2_fish', main_clock).loop(n_fish_loop(2), range(2))
    room.loop('3_fish', main_clock).loop(n_fish_loop(3), range(3))
    room.loop('4_fish', main_clock).loop(n_fish_loop(4), range(4))
    all_fish_funcs(room, clock_sign, reset_sign)
    t_fish = room.function('tropical_fish_init')
    for i, (kind, breeds) in enumerate(tropical_fish.items()):
        fish = breeds[0]
        fish.custom_name(True)
        fish.tag(kind.lower())
        if restworld.version == VERSION_1_20:
            placer = room.mob_placer(r(-int(i / 4), 3.2, int(i % 4)), EAST, adults=True)
        else:
            placer = room.mob_placer(r(int(i / 6) + 0.5, 3.2, int(i % 6)), WEST, adults=True)
        t_fish.add(placer.summon(fish))
    if restworld.version < VERSION_1_20:
        t_fish.add(WallSign(('Naturally', 'Occurring', 'Tropical Fish', '<--------')).place(
            r(int((len(tropical_fish) - 1) / 6) - 1, 2, (len(tropical_fish) - 1) % 6), WEST, water=True))
    else:
        t_fish.add(WallSign(('Naturally', 'Occurring', u'Tropical Fish', u'→ → →')).place(
            r(1, 2, (len(tropical_fish) - 1) % 4), EAST, water=True))

    if restworld.version < VERSION_1_20:
        axolotl_placer = room.mob_placer(r(1.3, 3.1, 0.6), 135, (0, 0), (-1.4, -1.4))
    else:
        axolotl_placer = room.mob_placer(r(-0.4, 3, 0), WEST, None, 1.8)
    if restworld.version < VERSION_1_20:
        room.function('axolotl_init').add(axolotl_placer.summon('axolotl'))
    else:
        room.function('axolotl_init').add(
            axolotl_placer.summon('axolotl'),
            execute().at(e().tag('axolotl_dry_home')).run(
                room.mob_placer(r(0, 3, 0), EAST,kid_delta=2).summon('axolotl')))
        room.function('axolotl_dry')
    room.loop('axolotl', main_clock).loop(
        lambda step: execute().as_(e().tag('axolotl')).run(data().merge(
            s(), {'Variant': step.i, 'CustomName': step.elem + ' Axolotl'})), axolotls)
    guardian_pos = r(-0.6, 3, -0.2)
    guardian_rot = 180
    elder_guardian_pos = r(2, 3, 0)
    elder_guardian_rot = 225
    if restworld.version == VERSION_1_20:
        guardian_pos = elder_guardian_pos = r(0, 3, 0)
        guardian_rot = elder_guardian_rot = SOUTH
    room.function('guardian_init').add(room.mob_placer(guardian_pos, guardian_rot, adults=True).summon('guardian'))
    room.function('elder_guardian_init').add(
        room.mob_placer(elder_guardian_pos, elder_guardian_rot, adults=True).summon('elder_guardian'))

    def squids_loop(step):
        placer = room.mob_placer(r(1.8, 4, 0.2), WEST, adults=True, tags=('squidy',), nbt={'NoGravity': True})
        return placer.summon('squid' if step.i == 0 else 'glow_squid')

    if restworld.version < VERSION_1_20:
        room.function('squid_init').add(
            clock_sign.place(r(-1, 4, 3), EAST, water=True),
            height_sign.place(r(-1, 6, 3), EAST, water=True))
    room.loop('squid', main_clock).add(kill_em(e().tag('squidy'))).loop(squids_loop, range(0, 2))

    if restworld.version < VERSION_1_20:
        dolphin_placer = room.mob_placer(r(1.8, 4, 0.8), EAST, adults=True)
        fish_placer = room.mob_placer(r(1.8, 4, -4), EAST, -1, adults=True)
    else:
        dolphin_placer = room.mob_placer(r(1.35, 3, 1.1), NORTH, adults=True)
        fish_placer = room.mob_placer(r(0, 3, 1), NORTH, -1, adults=True)
    room.function('fishies_init').add(
        # For some reason, at 1.19 the kill-off in the _init function misses the pufferfish
        kill(e().tag('pufferfish')),
        dolphin_placer.summon(Entity('dolphin', nbt={'Invulnerable': True})),
        fish_placer.summon(
            ('salmon', 'cod', 'pufferfish',
             Entity('tadpole', nbt={'Invulnerable': True, 'Age': -2147483648}).tag('kid', 'keeper'))),
    )

    def fishies_loop(step):
        yield data().merge(e().tag('pufferfish').limit(1), {'PuffState': step.elem})
        # Over time, the pufferfish creeps downward, so we have to put it back
        if restworld.version < VERSION_1_20:
            puffer_pos = r(1.8, 4, -6)
            puffer_facing = r(5, 4, -6)
        else:
            puffer_pos = r(-2, 3, 1)
            puffer_facing = r(-2, 3, -5)
        yield tp(e().tag('pufferfish'), puffer_pos).facing(puffer_facing)

    room.loop('fishies', main_clock).loop(fishies_loop, range(0, 3), bounce=True)


def all_fish_funcs(room, clock_sign, reset_sign):
    pattern = Score('pattern', 'fish')
    num_colors = Score('NUM_COLORS', 'fish')
    body_scale = Score('BODY_SCALE', 'fish')
    overlay_scale = Score('OVERLAY_SCALE', 'fish')
    pattern_size = Score('PATTERN_SIZE', 'fish')
    variant = Score('variant', 'fish')

    kinds = tuple(tropical_fish.keys())

    def all_fish_init():
        if restworld.version < VERSION_1_20:
            yield WallSign((None, 'All Possible', 'Tropical Fish', '-------->')).place(r(0, 2, -1), WEST, water=True)
            yield clock_sign.place(r(3, 4, 2), WEST, water=True)
            yield reset_sign.place(r(3, 6, 2), WEST, water=True)
            start, facing, delta = r(0.5, 3.2, 0), WEST, -1
        else:
            yield WallSign((None, 'All Possible', 'Tropical Fish', '← ← ←')).place(r(0, 2, 0), EAST, water=True)
            start, facing, delta = r(0, 3.2, 0), EAST, 1
        placer = room.mob_placer(start, facing, delta, adults=True)
        for i in range(0, 12):
            if restworld.version < VERSION_1_20:
                if i == 6:
                    x, y, z = start
                    start = (x - delta, y, z)
                    placer = room.mob_placer(start, facing, delta, adults=True)
            else:
                if i % 4 == 0:
                    x, y, z = start
                    start = (x - delta, y, z)
                    placer = room.mob_placer(start, facing, delta, adults=True)
            fish = Entity('tropical_fish', name=kinds[i])
            summon = placer.summon(fish, tags=(f'fish{i}',))
            yield summon
        yield (
            scoreboard().objectives().remove('fish'),
            scoreboard().objectives().add('fish', ScoreCriteria.DUMMY),
            num_colors.set(len(COLORS)),
            pattern.set(0),
            pattern_size.set(len(COLORS) ** 2),
            body_scale.set(0x10000),
            overlay_scale.set(0x1000000),
        )

    def all_fish():
        yield (
            pattern.set((pattern + 1) % pattern_size),
            variant.set((pattern // num_colors) * body_scale + (pattern % num_colors) * overlay_scale))
        for i in range(0, 6):
            yield from fish_variant(i)
            if i < 5:
                yield variant.add(256)
        yield variant.add(1)
        for i in range(6, 12):
            yield from fish_variant(i)
            if i < 11:
                yield variant.remove(256)

    def fish_variant(i):
        yield execute().store(RESULT).entity(e().tag(f'fish{i:d}').limit(1), 'Variant', LONG, 1).run(variant.get())

    room.function('all_fish_init').add(all_fish_init())
    room.loop('all_fish', fast_clock).add(all_fish())
