from __future__ import annotations

from pynecraft.base import NORTH, Nbt, r
from pynecraft.commands import CREATIVE, Entity, LEVELS, POINTS, SUCCESS, SURVIVAL, data, e, effect, execute, \
    function, \
    gamemode, item, p, xp
from pynecraft.simpler import WallSign
from pynecraft.values import ABSORPTION, POISON, REGENERATION, WITHER
from restworld.rooms import Room, label
from restworld.world import kill_em, main_clock, restworld


def room():
    room = Room('hud', restworld)

    # noinspection GrazieInspection
    room.function('hud_room_init').add(
        WallSign(('The HUD', '(your armor will', 'be restored when', 'you leave)')).place(r(0, 2, -1), NORTH),
        label(r(-1, 2, 4), 'Wither')
    )
    room.function('hud_room_enter').add(gamemode(SURVIVAL, p()))
    room.function('hud_room_exit').add(gamemode(CREATIVE, p()))

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
    room.function('armor_init', exists_ok=True).add(
        room.mob_placer(r(0, -2, 1), NORTH, adults=True, auto_tag=False).summon(
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
        def give_effect(ef: str):
            return effect().give(entity, ef, effect_time, 0, True)

        def clear_effect(ef: str | None):
            return effect().clear(entity, ef)

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
        room.loop(f'{prefix}health', main_clock).add(
            absorption.set(absorption_value),
            cur_health.set(data().get(entity, 'Health')),

            # If there is no effect currently going, act as if the health is too low.
            execute().store(SUCCESS).score(healthing).run(data().get(entity, 'active_effects')),
            execute().if_().score(healthing).matches(0).run(
                cur_health.set(0),
                health_up.set(0)),

            execute().if_().score(cur_health).matches((None, min_health)).run(
                execute().if_().score(health_up).matches(0).run(
                    clear_effect(POISON),
                    clear_effect(WITHER),
                    give_effect(REGENERATION)),
                health_up.set(1)),
            execute().if_().score(cur_health).matches(max_health).if_().score(health_up).matches(1).run(
                execute().if_().score(absorption).matches(0).run(
                    give_effect(ABSORPTION)),
                execute().unless().score(absorption).matches(0).run(
                    clear_effect(REGENERATION),
                    execute().if_().score(withering).matches(1).run(give_effect(WITHER)),
                    execute().unless().score(withering).matches(1).run(give_effect(POISON)),
                    health_up.set(0))))
        room.function(f'{prefix}health_exit').add(clear_effect(None))
        if 'horse' in prefix:
            return
        switch_effect = room.score('switch_effect')
        room.function('switch_to_wither', home=False).add(
            execute().if_().score(withering).matches(0).run(
                execute().store(SUCCESS).score(switch_effect).run(
                    data().get(entity, f'active_effects[{{id:"minecraft:poison"}}]')),
                execute().if_().score(switch_effect).matches(1).run(
                    clear_effect(POISON),
                    give_effect(WITHER)
                )),
            withering.set(1))
        room.function('switch_to_poison', home=False).add(
            execute().if_().score(withering).matches(1).run(
                execute().store(SUCCESS).score(switch_effect).run(
                    data().get(entity, f'active_effects[{{id:"minecraft:wither"}}]')),
                execute().if_().score(switch_effect).matches(1).run(
                    clear_effect(WITHER),
                    give_effect(POISON)
                )),
            withering.set(0))

    health_funcs('', p(), 15, 20)

    hud_horse = e().tag('hud_horse').limit(1)
    horse_init = room.function('horse_health_init').add(
        kill_em(hud_horse),
        room.mob_placer(r(0, 2, 0), NORTH, adults=True).summon(
            Entity('horse', name='Climb on', nbt=Nbt(Tame=True, Variant=514)), auto_tag=False, tags=('hud_horse',)))
    room.function('horse_health_enter').add(function(horse_init.full_name))
    health_funcs('horse_', hud_horse, 45, 53)

    def xp_loop(step):
        yield xp().set(p(), step.elem[0], LEVELS)
        yield xp().set(p(), step.elem[1], POINTS)

    room.loop('xp', main_clock).loop(xp_loop, ((1, 0), (1, 3), (1, 6), (1, 8), (10, 0), (1, 10), (1, 20), (1, 26)))
