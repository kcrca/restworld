from __future__ import annotations

from pyker.commands import Score, mc, entity, r, WEST, COLORS, MOD, EQ, MULT, PLUS, RESULT, LONG, NORTH, Entity, self, \
    EAST
from pyker.enums import ScoreCriteria
from pyker.simpler import WallSign
from restworld.rooms import fishes, Room
from restworld.world import fast_clock, restworld, main_clock, kill_em


def room():
    def loop_n_fish(count: int):
        def fish_loop(step):
            for f in [f for f in fishes if len(f[1]) == count]:
                tag, variants = f
                v = variants[step.i]
                yield mc.data().merge(entity().tag(tag).limit(1), {'Variant': v[0], 'CustomName': v[1]})

        return fish_loop

    def all_fish_funcs(room):
        body = Score('body', 'fish')
        pattern = Score('pattern', 'fish')
        num_colors = Score('NUM_COLORS', 'fish')
        body_scale = Score('BODY_SCALE', 'fish')
        pattern_scale = Score('PATTERN_SCALE', 'fish')
        pattern_variant = Score('pattern_variant', 'fish')
        variant = Score('variant', 'fish')

        def all_fish_init():
            yield WallSign((None, 'All Possible', 'Tropical Fish', '-------->')).place(r(0, 2, 0), WEST, water=True)
            # , nbt={'Invulnerable': True}
            placer = room.mob_placer(r(0.5, 3.2, 0), WEST, -1, adults=True)
            for i in range(0, 12):
                if i == 6:
                    placer = room.mob_placer(r(1.5, 3.2, 0), WEST, -1, adults=True)
                yield placer.summon('tropical_fish', tags=('fish%d' % i,))
            yield (
                mc.scoreboard().objectives().remove('fish'),
                mc.scoreboard().objectives().add('fish', ScoreCriteria.DUMMY),
                num_colors.set(len(COLORS)),
                body_scale.set(0x10000),
                pattern_scale.set(0x1000000),
                body.set(0),
                pattern.set(0),
            )

        def all_fish():
            yield (
                pattern.add(1),
                pattern.operation(MOD, num_colors),
                mc.execute().if_().score(pattern).matches(0).run(body.add(1)),
                body.operation(MOD, num_colors),
                pattern_variant.operation(EQ, pattern),
                pattern_variant.operation(MULT, pattern_scale),
                variant.operation(EQ, body),
                variant.operation(MULT, body_scale),
                variant.operation(PLUS, pattern_variant),
            )
            for i in range(0, 12):
                yield mc.execute().store(RESULT).entity(entity().tag('fish%d' % i).limit(1), 'Variant', LONG, 1).run(
                    variant.get())
                if i == 6:
                    yield variant.add(1)
                yield variant.add(256)

        room.function('all_fish_init').add(all_fish_init())
        room.loop('all_fish', fast_clock).add(all_fish())

    def squids(_, i, _2):
        placer = room.mob_placer(r(1.8, 4, 0), WEST, adults=True, tags=('squidy',), nbt={'NoGravity': True})
        return placer.summon('squid' if i == 0 else 'glow_squid')

    room = Room('aquatic', restworld, NORTH, (None, 'Aquatic'))

    room.loop('2_fish', main_clock).loop(loop_n_fish(2), range(0, 2))
    room.loop('3_fish', main_clock).loop(loop_n_fish(3), range(0, 3))
    all_fish_funcs(room)
    t_fish = room.function('tropical_fish_init')
    for i in range(0, 12):
        tag, variants = fishes[i]
        fish = Entity('tropical_fish', nbt={'Variant': variants[0][0]}).tag(tag).set_name(variants[0][1])
        t_fish.add(room.mob_placer(r(int(i / 6) + 0.5, 3.2, int(i % 6)), WEST, adults=True).summon(fish))
    t_fish.add(WallSign(("Naturally", "Occurring", "Tropical Fish", "<--------")).place(
        r(int((len(fishes) - 1) / 6) - 1, 2, (len(fishes) - 1) % 6), WEST, water=True))
    room.function('axolotl_init').add(room.mob_placer(r(1.3, 4, 1.3), 135, (0, 0), (-1.4, -1.4)).summon('axolotl'))
    axolotls = ('Lucy', 'Wild', 'Gold', 'Cyan', 'Blue')
    room.loop('axolotl', main_clock).loop(
        lambda step: mc.execute().as_(entity().tag('axoltol')).run().data().merge(
            self(), {'Variant': step.i, 'CustomName': step.item + ' Axolotl'}), axolotls)
    room.function('elder_guardian_init').add(room.mob_placer(r(2, 3, 0), 225, adults=True).summon('elder_guardian'))
    room.function('guardian_init').add(room.mob_placer(r(-0.6, 3, 0), 180, adults=True).summon('guardian'))
    room.function('fishies_init').add(
        room.mob_placer(r(1.8, 4, 0), EAST, adults=True).summon(Entity('dolphin', nbt={'Invulnerable': True})),
        room.mob_placer(r(1.8, 4, -4), EAST, -1, adults=True).summon(
            ('salmon', 'cod', 'pufferfish', Entity('tadpole', nbt={'Invulnerable': True, 'Age': -2147483648}))),
    )
    room.loop('fishies', main_clock).loop(
        lambda step: mc.data().merge(entity().tag('pufferfish').limit(1), {'PuffState': step.item}),
        range(0, 3), bounce=True)
    room.loop('squid', main_clock).add(kill_em(entity().tag('squidy'))).loop(squids, range(0, 2))
