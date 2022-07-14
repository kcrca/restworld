from __future__ import annotations

from pynecraft.base import EAST, NORTH, WEST, r
from pynecraft.commands import COLORS, LONG, MULT, PLUS, Score
from pynecraft.commands import EQ, MOD, scoreboard
from pynecraft.commands import Entity, RESULT, e, s
from pynecraft.commands import data, execute, function, kill
from pynecraft.commands import tp
from pynecraft.enums import ScoreCriteria
from pynecraft.simpler import WallSign
from restworld.rooms import Room, fishes
from restworld.world import fast_clock, kill_em, main_clock, restworld


def room():
    room = Room('aquatic', restworld, NORTH, (None, 'Aquatic'))
    clock_wall_sign = WallSign((None, 'Clock', 'On / Off'), (function('restworld:global/clock_toggle')))

    def n_fish_loop(count: int):
        def fish_loop(step):
            for f in [f for f in fishes if len(f[1]) == count]:
                tag, variants = f
                v = variants[step.i]
                yield data().merge(e().tag(tag).limit(1), {'Variant': v[0], 'CustomName': v[1]})

        return fish_loop

    room.loop('2_fish', main_clock).loop(n_fish_loop(2), range(0, 2))
    room.loop('3_fish', main_clock).loop(n_fish_loop(3), range(0, 3))
    all_fish_funcs(room, clock_wall_sign)
    t_fish = room.function('tropical_fish_init')
    for i in range(0, 12):
        tag, variants = fishes[i]
        fish = Entity('tropical_fish', nbt={'Variant': variants[0][0]}).tag(tag)
        fish.name = variants[0][1]
        t_fish.add(room.mob_placer(r(int(i / 6) + 0.5, 3.2, int(i % 6)), WEST, adults=True).summon(fish))
    t_fish.add(WallSign(('Naturally', 'Occurring', 'Tropical Fish', '<--------')).place(
        r(int((len(fishes) - 1) / 6) - 1, 2, (len(fishes) - 1) % 6), WEST, water=True))
    room.function('axolotl_init').add(room.mob_placer(r(1.3, 3.1, 0.6), 135, (0, 0), (-1.4, -1.4)).summon('axolotl'))

    axolotls = ('Lucy', 'Wild', 'Gold', 'Cyan', 'Blue')
    room.loop('axolotl', main_clock).loop(
        lambda step: execute().as_(e().tag('axolotl')).run(data().merge(
            s(), {'Variant': step.i, 'CustomName': step.elem + ' Axolotl'})), axolotls)
    room.function('guardian_init').add(room.mob_placer(r(-0.6, 3, -0.2), 180, adults=True).summon('guardian'))
    room.function('elder_guardian_init').add(room.mob_placer(r(2, 3, 0), 225, adults=True).summon('elder_guardian'))

    def squids_loop(step):
        placer = room.mob_placer(r(1.8, 4, 0.2), WEST, adults=True, tags=('squidy',), nbt={'NoGravity': True})
        return placer.summon('squid' if step.i == 0 else 'glow_squid')

    room.function('squid_init').add(clock_wall_sign.place(r(-1, 4, 3), EAST, water=True))
    room.loop('squid', main_clock).add(kill_em(e().tag('squidy'))).loop(squids_loop, range(0, 2))

    room.function('fishies_init').add(
        # For some reason, at 1.19 the kill-off in the _init function misses the pufferfish
        kill(e().tag('pufferfish')),
        room.mob_placer(r(1.8, 4, 0.8), EAST, adults=True).summon(Entity('dolphin', nbt={'Invulnerable': True})),
        room.mob_placer(r(1.8, 4, -4), EAST, -1, adults=True).summon(
            ('salmon', 'cod', 'pufferfish',
             Entity('tadpole', nbt={'Invulnerable': True, 'Age': -2147483648}).tag('kid', 'keeper'))),
    )

    def fishies_loop(step):
        yield data().merge(e().tag('pufferfish').limit(1), {'PuffState': step.elem})
        # Over time, the pufferfish creeps downward, so we have to put it back
        yield tp(e().tag('pufferfish'), r(1.8, 4, -6)).facing(r(5, 4, -6))

    room.loop('fishies', main_clock).loop(fishies_loop, range(0, 3), bounce=True)


def all_fish_funcs(room, clock_wall_sign):
    body = Score('body', 'fish')
    pattern = Score('pattern', 'fish')
    num_colors = Score('NUM_COLORS', 'fish')
    body_scale = Score('BODY_SCALE', 'fish')
    base_variant = Score('base_variant', 'fish')
    pattern_scale = Score('PATTERN_SCALE', 'fish')
    pattern_variant = Score('pattern_variant', 'fish')
    variant = Score('variant', 'fish')

    def all_fish_init():
        yield WallSign((None, 'All Possible', 'Tropical Fish', '-------->')).place(r(0, 2, 0), WEST, water=True)
        yield clock_wall_sign.place(r(3, 4, 2), WEST, water=True)
        placer = room.mob_placer(r(0.5, 3.2, 0), WEST, -1, adults=True)
        for i in range(0, 12):
            if i == 6:
                placer = room.mob_placer(r(1.5, 3.2, 0), WEST, -1, adults=True)
            yield placer.summon('tropical_fish', tags=(f'fish{i:d}',))
        yield (
            scoreboard().objectives().remove('fish'),
            scoreboard().objectives().add('fish', ScoreCriteria.DUMMY),
            num_colors.set(len(COLORS)),
            body.set(0),
            pattern.set(0),
            body_scale.set(0x10000),
            pattern_scale.set(0x1000000),
        )

    def all_fish():
        yield (
            pattern.add(1),
            pattern.operation(MOD, num_colors),
            execute().if_().score(pattern).matches(0).run(body.add(1)),
            body.operation(MOD, num_colors),
            base_variant.operation(EQ, body),
            base_variant.operation(MULT, body_scale),
            pattern_variant.operation(EQ, pattern),
            pattern_variant.operation(MULT, pattern_scale),
            base_variant.operation(PLUS, pattern_variant),
            variant.operation(EQ, base_variant),
        )
        for i in range(0, 6):
            yield execute().store(RESULT).entity(e().tag(f'fish{i:d}').limit(1), 'Variant', LONG, 1).run(
                variant.get())
            if i < 5:
                yield variant.add(256)
        yield variant.add(1)
        for i in range(6, 12):
            yield execute().store(RESULT).entity(e().tag(f'fish{i:d}').limit(1), 'Variant', LONG, 1).run(
                variant.get())
            if i < 11:
                yield variant.remove(256)

    room.function('all_fish_init').add(all_fish_init())
    room.loop('all_fish', fast_clock).add(all_fish())
