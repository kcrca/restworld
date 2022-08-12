from pynecraft.base import NORTH, Nbt, r
from pynecraft.commands import Entity, LEVELS, POINTS, SUCCESS, data, e, effect, execute, function, item, p, xp
from pynecraft.enums import Effect
from restworld.rooms import Room
from restworld.world import kill_em, main_clock, restworld


def room():
    room = Room('hud', restworld, NORTH, ('GUI,', 'Containers,', 'Items'))

    def armor_loop(step):
        if step.elem == 5:
            yield item().replace().entity(p(), 'armor.chest').with_('chainmail_chestplate')
        elif step.elem == 10:
            yield item().replace().entity(p(), 'armor.chest').with_('chainmail_chestplate')
            yield item().replace().entity(p(), 'armor.legs').with_('chainmail_leggings')
            yield item().replace().entity(p(), 'armor.feet').with_('chainmail_boots')
        elif step.elem == 15:
            yield item().replace().entity(p(), 'armor.head').with_('iron_helmet')
            yield item().replace().entity(p(), 'armor.chest').with_('iron_chestplate')
            yield item().replace().entity(p(), 'armor.legs').with_('iron_leggings')
            yield item().replace().entity(p(), 'armor.feet').with_('iron_boots')
        elif step.elem == 20:
            yield item().replace().entity(p(), 'armor.head').with_('diamond_helmet')
            yield item().replace().entity(p(), 'armor.chest').with_('diamond_chestplate')
            yield item().replace().entity(p(), 'armor.legs').with_('diamond_leggings')
            yield item().replace().entity(p(), 'armor.feet').with_('diamond_boots')

    armor_places = tuple(f'armor.{x}' for x in ('feet', 'legs', 'chest', 'head'))
    saver_name = 'armor'
    room.function('armor_init', exists_ok=True).add(room.mob_placer(r(0, -2, 1), NORTH, adults=True).summon(
        Entity('armor_stand', Nbt(NoGravity=True), saver_name).tag(saver_name)))
    room.loop('armor', main_clock).add(
        tuple(item().replace().entity(p(), x).with_('air') for x in armor_places)
    ).loop(
        armor_loop, range(0, 21, 5), bounce=True)
    saver = e().tag(saver_name).limit(1)
    room.function('armor_enter', exists_ok=True).add(
        (item().replace().entity(saver, x).from_().entity(p(), x) for x in armor_places))
    room.function('armor_exit', exists_ok=True).add(
        (item().replace().entity(p(), x).from_().entity(saver, x) for x in armor_places))

    # Use for both the player and the horse. The horse will never have absorption or wither, but it isn't very expensive
    # to check for them, and keeps this code simpler.
    def health_funcs(prefix, entity, min_health, max_health):
        cur_health = room.score(f'{prefix}cur_health')
        health_up = room.score(f'{prefix}health_up')
        absorption = room.score(f'{prefix}absorption')
        healthing = room.score(f'{prefix}healthing')
        withering = room.score(f'{prefix}withering')
        effect_time = 100000
        absorption_value = data().get(entity, 'AbsorptionAmount')
        if 'horse' in prefix:
            # Horses don't get absorption, this makes nothing happen with absorption in the loop
            absorption_value = 1
        loop = room.loop(f'{prefix}health', main_clock).add(
            absorption.set(absorption_value),
            cur_health.set(data().get(entity, 'Health')),

            # If there is no effect currently going, act as if the health is too low.
            execute().store(SUCCESS).score(healthing).run(data().get(entity, 'ActiveEffects')),
            execute().if_().score(healthing).matches(0).run(cur_health.set(0)),

            execute().if_().score(cur_health).matches((None, min_health)).run(
                execute().if_().score(health_up).matches(0).run(
                    effect().clear(entity, Effect.POISON),
                    effect().clear(entity, Effect.WITHER),
                    effect().give(entity, Effect.REGENERATION, effect_time, 1, True)),
                health_up.set(1)),
            execute().if_().score(cur_health).matches(max_health).if_().score(health_up).matches(1).run(
                execute().if_().score(absorption).matches(0).run(
                    effect().give(entity, Effect.ABSORPTION, effect_time, 0, True)),
                execute().unless().score(absorption).matches(0).run(
                    effect().clear(entity, Effect.REGENERATION),
                    execute().if_().score(withering).matches(1).run(
                        effect().give(entity, Effect.WITHER, effect_time, 0, True)),
                    execute().unless().score(withering).matches(1).run(
                        effect().give(entity, Effect.POISON, effect_time, 0, True)),
                    health_up.set(0))))

    health_funcs('', p(), 15, 20)
    room.function('health_exit').add(effect().clear(p()))

    hud_horse = e().tag('hud_horse').limit(1)
    horse_init = room.function('horse_health_init').add(
        kill_em(e()),
        room.mob_placer(r(0, 2, 0), NORTH).summon('horse', auto_tag=False, tags=('hud_horse',)))
    room.function('horse_health_enter').add(function(horse_init.full_name))
    health_funcs('horse_', hud_horse, 45, 53)

    def xp_loop(step):
        yield xp().set(p(), step.elem[0], LEVELS)
        yield xp().set(p(), step.elem[1], POINTS)

    room.loop('xp', main_clock).loop(xp_loop, ((1, 0), (1, 3), (1, 6), (1, 8), (10, 0), (1, 10), (1, 20), (1, 26)))
