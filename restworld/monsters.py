from __future__ import annotations

import copy

from pynecraft.base import EAST, NORTH, WEST, r
from pynecraft.commands import Entity, data, e, execute, function, good_facing, s, tag
from pynecraft.simpler import Item
from restworld.rooms import MobPlacer, Room, label
from restworld.world import VERSION_1_20, kill_em, main_clock, restworld


def room():
    room = Room('monsters', restworld, NORTH, (None, 'Monsters,', 'Bosses'))

    def placer(*args, **kwargs):
        return room.mob_placer(*args, **kwargs)

    east_placer = list(r(-0.2, 2, 0)), EAST, 2, 2.2
    west_placer = list(r(0.2, 2, 0)), WEST, -2, 2.2

    room.function('creeper_init').add(placer(*west_placer, adults=True).summon('creeper'))
    room.loop('creeper', main_clock).loop(
        lambda step: execute().as_(e().tag('creeper').limit(1)).run(data().merge(s(), {'powered': step.elem})),
        (True, False))

    slime_placer = copy.deepcopy(west_placer)
    slime_placer[0][1] = r(3)
    room.function('slime_init').add(placer(*slime_placer, adults=True).summon('slime'))
    room.loop('slime', main_clock).loop(
        lambda step: data().modify(e().tag('slime').limit(1), 'Size').set().value(step.elem),
        range(0, 3), bounce=True)

    illagers = (Entity('Vindicator'), Entity('Evoker'), Entity('Pillager'),
                Entity('Pillager', nbt={'HandItems': [Item.nbt_for('crossbow')]}),
                Entity('illusioner', name='Illusioner (unused)'))
    tags = ('illager',)

    def illager_loop(step):
        place = list(copy.deepcopy(west_placer))
        dir = WEST if restworld.version < VERSION_1_20 else EAST
        if restworld.version >= VERSION_1_20:
            place[0][2] -= 0.5
            place[1] = dir
        yield placer(*place, adults=True, tags=tags).summon(step.elem)
        if step.elem.id == 'evoker':
            z = -1 if restworld.version < VERSION_1_20 else -1.5
            x = 0 if restworld.version < VERSION_1_20 else 1
            yield placer(r(x, 3.5, z), dir, adults=True, tags=tags).summon(
                Entity('vex', nbt={'HandItems': [Item.nbt_for('iron_sword')], 'LifeTicks': 2147483647}))
            yield placer(r(-1 + 2 * x, 2, 1), dir, adults=True, tags=tags).summon(
                Entity('Evoker Fangs', nbt={'Warmup': 0}))

    room.loop('illager', main_clock).add(kill_em(e().tag(*tags))).loop(illager_loop, illagers)

    dir = WEST if restworld.version < VERSION_1_20 else NORTH
    room.function('phantom_init').add(placer(r(-0.5, 4, 0), dir, adults=True).summon('phantom'))

    def ravager_loop(step):
        ravager = Entity('ravager')
        if step.elem is not None:
            ravager.passenger(Entity(step.elem, {'Rotation': good_facing(EAST).rotation}).merge_nbt(MobPlacer.base_nbt))
        yield placer(r(1, 2, 0), EAST, adults=True).summon(ravager)

    room.loop('ravager', main_clock).add(kill_em(e().tag('ravager'))).loop(
        ravager_loop, (None, 'Pillager', 'Vindicator', 'Evoker'))

    silverfish_dir = EAST if restworld.version < VERSION_1_20 else NORTH
    room.function('silverfish_init').add(placer(r(0.2, 2, 0), silverfish_dir, adults=True).summon('silverfish'))

    east = good_facing(EAST)
    east_rot = {'Rotation': east.rotation, 'Facing': east.name}

    def skeleton_horse_loop(step):
        horse = Entity('Skeleton Horse')
        if step.i == 1:
            helmet = {'id': 'iron_helmet', 'Count': 1, 'tag': {'RepairCost': 1, 'Enchantments': [
                {'lvl': 3, 'id': 'unbreaking'}]}}
            bow = {'id': 'bow', 'Count': 1,
                   'tag': {'RepairCost': 1, 'Enchantments': [{'lvl': 3, 'id': 'unbreaking'}]}}
            skel = Entity('Skeleton', nbt={'ArmorItems': [{}, {}, {}, helmet], 'HandItems': [bow, {}]})
            skel.merge_nbt(MobPlacer.base_nbt).merge_nbt(east_rot)
            skel.tag('monsters', 'passenger')
            horse.passenger(skel)
        yield placer(*east_placer, adults=True).summon(horse)

    room.loop('skeleton_horse').add(
        kill_em(e().tag('skeleton_horse', '!kid'))
    ).loop(skeleton_horse_loop, range(0, 2))

    rider_label_pos = r(3, 2, 0) if restworld.version < VERSION_1_20 else r(2, 2, -1)
    room.function('skeleton_horse_init').add(
        placer(*east_placer).summon('Skeleton Horse'),
        label(rider_label_pos, 'Rider'))

    bow = Item.nbt_for('bow')
    helmet = Item.nbt_for('iron_helmet')
    rider = Entity('Skeleton', nbt={'ArmorItems': [{}, {}, {}, helmet], 'HandItems': [bow, {}]}).merge_nbt(
        MobPlacer.base_nbt)

    room.loop('skeleton', main_clock).add(
        kill_em(e().tag('skeletal'))
    ).loop(lambda step: placer(*west_placer, adults=True).summon(
        Entity(step.elem, nbt={'HandItems': [bow]}).tag('skeletal')), ('Skeleton', 'Stray'))

    spider_dir = EAST if restworld.version < VERSION_1_20 else NORTH
    spider_facing = good_facing(spider_dir)
    spider_rot = {'Rotation': spider_facing.rotation, 'Facing': spider_facing.name}

    def spider_loop(step):
        p = placer(r(-0.2, 2.5, -0.2), spider_dir, -2.5, nbt={'Tags': ['spiders']}, adults=True)
        for s in ('Spider', 'Cave Spider'):
            spider = Entity(s)
            if step.i == 1:
                spider.passenger(rider.merge_nbt(spider_rot).merge_nbt(MobPlacer.base_nbt))
            yield p.summon(spider)

    room.loop('spiders').add(
        kill_em(e().tag('spiders'))
    ).loop(spider_loop, range(0, 2))
    jockey_label_pos = r(2, 2, -2) if restworld.version < VERSION_1_20 else r(-2, 2, -1)
    room.function('spiders_init').add(
        function('restworld:monsters/spiders_cur'),
        label(jockey_label_pos, 'Jockey'))
    place = list(copy.deepcopy(west_placer))
    if restworld.version >= VERSION_1_20:
        place[0][2] -= 0.5
    room.function('witch_init').add(placer(*place, adults=True).summon('witch'))
    place = list(copy.deepcopy(east_placer))
    if restworld.version >= VERSION_1_20:
        place[0][2] -= 0.5
    room.function('zombie_horse_init').add(
        placer(*place).summon(Entity('zombie_horse', name='Zombie Horse (Unused)')))
    zombie_jockey = room.score('zombie_jockey')
    zombie_jockey_label_pos = r(3, 2, 0) if restworld.version < VERSION_1_20 else r(2, 2, -1)
    room.function('zombie_init').add(
        zombie_jockey.set(0),
        execute().as_(e().tag('zombie_home')).run(tag(s()).add('zombie_home_selector')),
        execute().as_(e().tag('zombie_jockey_home')).run(tag(s()).add('zombie_home_selector')),
        label(zombie_jockey_label_pos, 'Jockey'))

    def zombie_loop(step):
        p = placer(r(0.2, 2, 0), EAST, 0, 1.8, tags=('zombieish',))
        yield execute().if_().score(zombie_jockey).matches(0).run(p.summon(Entity(step.elem)))

        p = placer(r(0.2, 2, 0), EAST, 0, 2.2, tags=('zombieish',), adults=True)
        yield execute().if_().score(zombie_jockey).matches(1).run(p.summon(Entity(step.elem)))
        chicken = Entity('Chicken').passenger(
            Entity(step.elem, {'Tags': ['kid', room.name], 'IsBaby': True, 'Age': -2147483648}).merge_nbt(
                east_rot).merge_nbt(MobPlacer.base_nbt))
        p = placer(r(2.0, 2, 0), EAST, 0, 2.2, tags=('zombieish',), kids=True)
        yield execute().if_().score(zombie_jockey).matches(1).run(p.summon(chicken))
        if step.elem == 'Drowned':
            yield execute().as_(e().tag('zombieish').tag('!kid')).run(
                data().merge(s(), {'HandItems': [Item.nbt_for('trident')]}))

    room.loop('zombie', main_clock).add(kill_em(e().tag('zombieish'))).loop(
        zombie_loop, ('Zombie', 'Husk', 'Drowned'))

    if restworld.version >= VERSION_1_20:
        placer = room.mob_placer(r(0, 2, 0), NORTH, adults=True)
        room.function('enderman_init').add(
            execute().unless().entity(e().type('enderman').distance((None, 5))).run(list(placer.summon('enderman'))[0]))

        # room.function('silverfish_init').add(placer(r(0.2, 2, 0), silverfish_dir, adults=True).summon('silverfish'))
        placer = room.mob_placer(r(0, 2, 0.2), NORTH, adults=True)
        room.function('endermite_init').add(placer.summon('endermite'))

        room.function('warden_init').add((room.mob_placer(r(0, 2, -0.5), NORTH, adults=True).summon('warden'),))
