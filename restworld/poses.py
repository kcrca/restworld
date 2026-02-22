from pynecraft.base import as_facing, d, MIDNIGHT, NOON, r, WEST
from pynecraft.commands import Block, CREATIVE, data, e, effect, Entity, execute, fill, forceload, function, gamemode, \
    INFINITE, \
    n, p, \
    REPLACE, s, say, \
    schedule, \
    setblock, \
    summon, SURVIVAL, time, tp
from pynecraft.function import ENTITY
from pynecraft.values import BAD_OMEN
from restworld.rooms import kill_em, Room
from restworld.world import restworld


def room():
    room = Room('poses', restworld)

    def pose_funcs(mob, pose, facing, gap, create, remove):
        facing = as_facing(facing)
        placer = room.mob_placer(r(0, 2, 0), facing, adults=True, nbt={'NoAI': False})
        name = f'{mob}_{pose}'
        freeze = room.function(f'{name}_freeze', home=False).add(
            say(f'freeze {name}'),
            execute().as_(e().tag(name, room.name)).at(s()).run(remove),
            data().modify(n().tag(name, room.name), 'NoAI').set().value(True))
        room.function(f'{name}_init').add(
            kill_em(e().tag(name, room.name)),
            placer.summon(Entity(mob), tags=name),
            execute().as_(e().tag(name, room.name)).at(s()).run(create),
            schedule().function(freeze, gap, REPLACE)
        )

    def pose_target(mob, pose, facing, gap, target):
        name = f'{mob}_{pose}'
        pose_funcs(mob, pose, facing, gap, Entity(target).summon(d(0, 0, 5), {'Tags': [name, f'{name}_target']}),
                   kill_em(e().tag(f'{name}_target')))

    pose_target('cat', 'stalk', WEST, 15, 'rabbit')
    stop_water = room.function('wolf_shake_dry', home=False).add(
        say('stop water'),
        execute().at(e().tag('wolf_shake_home')).run(setblock(r(0, 2, 0), 'air')))
    pose_funcs('wolf', 'shake', WEST, 25,
               (setblock(d(0, 0, 0), Block('water')),
                schedule().function(stop_water, 5, REPLACE)
                ),
               ())
    pose_funcs('villager', 'sleep', WEST, 30,
               (setblock(d(0, 0, 1), Block('green_bed', {'part': 'foot', 'facing': WEST})),
                setblock(d(0, 0, 2), Block('green_bed', {'part': 'head', 'facing': WEST})),
                time().set(MIDNIGHT)),
               time().set(NOON))
    pose_funcs('camel', 'sit', WEST, 30,
               data().modify(n().tag('camel_sit'), 'LastPoseTick').set().value(0),
               ())

    restworld.tags(ENTITY)['raiders'] = {'values': ['pillager', 'vindicator', 'evoker', 'witch', 'ravager', 'vex']}
    villager_raid_run = room.function('villager_raid_run', home=False).add(
        # execute at @e[name=villager_arms_home] if entity @e[type=#restworld:raiders,distance=..96] run schedule clear restworld:poses/villager_celebrate_freeze
        execute().at(e().tag('pose_raid_home')).if_().entity(e().type('#restworld:raiders').distance(96))
    )
    raid_sz = 35
    villager_celebrate_raid = room.function('villager_celebrate_raid').add(
        setblock(r(-3, 2, -3),
                 Block('structure_block',
                       nbt={'mode': 'LOAD', 'name': 'restworld:pose_village', 'posX': 1, 'posY': 0, 'posZ': 1})),
        setblock(r(-3, 1, -3), 'redstone_block'),
        setblock(r(-3, 1, -3), 'air'),
        summon('villager', r(0, 3, 0)),
        fill(r(-raid_sz, 2, -raid_sz), r(raid_sz, 2, raid_sz), 'grass_block').replace('air'),

        gamemode(SURVIVAL, p()),
        effect().give(p(), BAD_OMEN, INFINITE, 1, False),
        tp(p(), r(0, 3, 0)),
    )
    villager_celebrate_clear = room.function('villager_celebrate_clear', home=False).add(
        execute().at(e().tag('pose_raid_home')).run(fill(r(-raid_sz, -2, -raid_sz), r(raid_sz, 5, raid_sz), 'air')),
        kill_em(e().tag('pose_raid_home')),
        kill_em(e().tag('poses_raid')),
        execute().at(e().tag('villager_celebrate_home')).run(tp(p(), r(0, 2, 0))),
        gamemode(CREATIVE, p()),
        effect().clear(p(), BAD_OMEN),
    )

    room.function('villager_celebrate_init').add(
        forceload().add(r(0, 0)),
        forceload().add(r(-100, 100)),
        execute().at(e().tag('poses_room_end_home')).run(
            summon('armor_stand', r(-100, 0, 100),
                   {'Tags': ['pose_raid_home', room.name, 'poses_raid'], 'NoGravity': True})),
        execute().as_(e().tag('pose_raid_home')).at(s()).run(function(villager_celebrate_raid)),
    )
