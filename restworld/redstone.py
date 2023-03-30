from __future__ import annotations

from pynecraft import info
from pynecraft.base import DOWN, EAST, NOON, SOUTH, UP, WEST, r
from pynecraft.commands import Block, data, e, execute, fill, function, kill, say, setblock, summon, time
from pynecraft.info import instruments, stems
from pynecraft.simpler import Item, Region, Sign, WallSign
from restworld.rooms import Room, ensure, label
from restworld.world import fast_clock, kill_em, main_clock, restworld


def room():
    room = Room('redstone', restworld, SOUTH, (None, 'Redstone'))

    room.function('dispenser_init').add(WallSign(()).place(r(0, 3, 0), WEST))

    def dispenser_loop(step):
        yield setblock(r(0, 2, 0), (step.elem, {'facing': UP}))
        yield setblock(r(0, 4, 0), (step.elem, {'facing': WEST}))
        yield setblock(r(0, 6, 0), (step.elem, {'facing': DOWN}))
        yield Sign.change(r(0, 3, 0), (None, step.elem))

    room.loop('dispenser', main_clock).loop(dispenser_loop, ('Dispenser', 'Dropper'))
    room.function('hopper_init').add(WallSign((None, 'Which way are', 'they pointing?')).place(r(2, 3, 1), WEST))
    room.loop('lever', main_clock).loop(
        lambda step: setblock(r(0, 3, 0), ('lever', {'powered': step.elem, 'face': 'floor'})), (False, True))

    def lightning_rod_loop(step):
        yield setblock(r(0, 3, 0), step.elem)
        yield Sign.change(r(1, 2, 0), (None, None, '(Powered)' if 'powered' in str(step.elem) else ''))

    room.loop('lightning_rod', main_clock).loop(
        lightning_rod_loop, (Block('Lightning Rod'), Block('Lightning Rod', {'powered': True})))

    minecart_types = list(Block(f'{t}Minecart') for t in
                          ('', 'Chest|', 'Furnace|', 'TNT|', 'Hopper|', 'Spawner|', 'Command Block|'))

    def minecart_loop(step):
        yield kill_em(e().tag('minecart_type'))
        yield summon(step.elem.merge_nbt({'Tags': ['minecart_type']}), r(0, 3, 0))
        yield data().merge(r(-1, 2, 0), step.elem.sign_nbt)

    room.loop('minecarts', main_clock).loop(minecart_loop, minecart_types)
    room.loop('observer', main_clock).loop(
        lambda step: setblock(r(0, 2, 0), ('observer', {'powered': step.elem, 'facing': EAST})), (True, False))
    room.function('piston_init').add(WallSign(()).place(r(-1, 2, 0), WEST))

    def piston_loop(step):
        extended = step.i in (1, 4)
        block = 'redstone_block' if extended else 'air'
        piston = 'Piston' if step.i < 3 else 'Sticky Piston'
        if block == 'air':
            yield setblock(r(-1, 2, 0), 'air')
        yield ensure(r(0, 2, 0), block)
        if step.i in (0, 3):
            yield ensure(r(0, 2, -1), f'{piston}[facing=north]')
            yield ensure(r(0, 2, 1), f'{piston}[facing=west]')
            yield ensure(r(0, 3, 0), f'{piston}[facing=up,]')
        yield WallSign((None, piston)).place(r(-1, 2, 0), WEST)

    room.loop('piston', main_clock).loop(piston_loop, range(6))
    room.function('rail_init').add(WallSign(()).place(r(1, 2, -2), WEST))
    rails = (
        ('Rail', False),
        ('Powered Rail', False), ('Powered Rail', True),
        ('Detector Rail', False), ('Detector Rail', True),
        ('Activator Rail', False), ('Activator Rail', True),
    )
    room.function('rail_clean', home=False).add(say('clean'), kill_em(e().tag('tmp_minecart')))

    def rail_loop(step):
        volume = Region(r(3, 3, -3), r(0, 0, 0))
        rail, on = step.elem
        # 'powered=true' only seems to work for detector rail, but it's harmless for the others and maybe someday it
        # will work for all, and we can get rid of the torches.
        added = dict(powered=True) if on else None
        yield volume.replace_straight_rails(rail, '#rails', added)
        if on:
            yield volume.replace('redstone_torch', 'glass')
        else:
            yield volume.replace('glass', 'redstone_torch')
        yield Sign.change(r(1, 2, -2), (None, rail, '(Powered)' if on else ''))

    room.loop('rail', main_clock).loop(rail_loop, rails)

    room.function('redstone_lamp_init').add(WallSign((None, 'Redstone Lamp')).place(r(-1, 3, 0), EAST))
    room.loop('redstone_lamp', main_clock).loop(lambda step: setblock(r(0, 0, 0), step.elem),
                                                ('Redstone Torch', 'Air'))
    room.function('redstone_wire_init').add(WallSign((None, 'Redstone Wire')).place(r(0, 2, 0), WEST))

    def redstone_wire_loop(step):
        volume = Region(r(0, 0, 0), r(7, 0, 7))
        if step.i == 0:
            yield volume.replace('redstone_torch', 'glass')
            yield Sign.change(r(0, 2, 0), (None, None, '(Powered)'))
        else:
            yield volume.replace('glass', 'redstone_torch')
            yield Sign.change(r(0, 2, 0), (None, None, ''))

    room.loop('redstone_wire', main_clock).loop(redstone_wire_loop, range(0, 2))
    room.function('repeater_init').add(
        WallSign((None, 'Comparator', 'and Repeater')).place(r(0, 3, 0), WEST),
        WallSign(()).place(r(-1, 2, -2), WEST))

    def repeater_loop(step):
        mode = 'compare' if step.i < 2 else 'subtract'
        yield setblock(r(-1, 2, -1),
                       ('comparator', {'facing': 'east', 'mode': mode}))
        yield data().merge(r(-1, 2, -2), Sign.lines_nbt((None, 'Comparator Mode:', mode.title())))
        if step.i > 0:
            yield fill(r(0, 2, -1), r(0, 2, 1), 'redstone_block').replace('air')
        else:
            yield fill(r(0, 2, -1), r(0, 2, 1), 'air').replace('redstone_block')
        if step.i == 2:
            yield fill(r(0, 2, 2), r(-1, 2, 3), 'redstone_wire')
            yield setblock(r(-1, 2, 2), ('repeater', {'facing': 'south'}))
        else:
            yield fill(r(0, 2, 2), r(-1, 2, 3), 'air')

    room.loop('repeater', main_clock).loop(repeater_loop, range(0, 3))

    def sculk_loop(step):
        if step.i % 2 == 0:
            if step.i == 0:
                block = 'Sculk Sensor'
                yield Sign.change(r(-1, 3, -0), (None, ''))
            else:
                # Shows up waterlogged by default; see https://bugs.mojang.com/browse/MC-261388
                block = Block('Calibrated|Sculk Sensor', {'waterlogged': False, 'facing': WEST})
                yield Sign.change(r(-1, 3, -0), (None, 'Calibrated'))
            yield setblock(r(0, 2, 0), block)
        yield setblock(r(-4, 2, 0), 'air' if step.i < 2 else 'redstone_block')

    room.function('sculk_init').add(WallSign((None, None, 'Sculk Sensor')).place(r(-1, 3, 0), EAST))
    room.loop('sculk', main_clock).loop(sculk_loop, range(4))

    room.function('target_init').add(WallSign((None, 'Target', None, '(vanilla shows 1)')).place(r(1, 3, 0), WEST))

    def target_loop(step):
        yield setblock(r(0, 2, 0), ('target', {'power': step.i}))
        yield Sign.change(r(1, 3, 0), (None, None, f'Power {step.i:d}'))

    room.loop('target', fast_clock).loop(target_loop, range(0, 16))
    room.function('wire_strength_init').add(
        fill(r(1, 2, -1), r(1, 2, -16),
             ('oak_wall_sign', {'facing': WEST}, {'front_text': Sign.lines_nbt((None, None, 'Powered'))})))

    def wire_strength_loop(step):
        yield setblock(r(0, 2, 0), 'redstone_block' if step.i == 0 else 'air')
        for i in range(0, 16):
            if step.i == 0:
                yield Sign.change(r(1, 2, -(16 - i)), (None, f'{i}'))
            else:
                yield Sign.change(r(1, 2, -(16 - i)), (None, 'Not'))

    room.loop('wire_strength', main_clock).loop(wire_strength_loop, (0, 1))

    def wood_power_loop(step):
        wood, powered = step.elem
        yield setblock(r(1, 2, -1), (f'{wood.id}_pressure_plate', {'powered': powered}))
        yield setblock(r(1, 3, 0), (f'{wood.id}_button', {'facing': EAST, 'powered': powered}))
        yield setblock(r(0, 3, 0), ('redstone_lamp', {'lit': powered}))
        yield setblock(r(0, 2, -1), ('redstone_lamp', {'lit': powered}))
        yield setblock(r(1, 2, 0), ('oak_wall_sign', {'facing': EAST}))
        yield data().merge(r(1, 2, 0), wood.sign_nbt)
        if powered == 'True':
            yield Sign.change(r(1, 2, 0), (None, None, None, '(Powered)'))

    powerings = []
    for t in ('Stone', 'Polished|Blackstone') + info.woods + stems:
        powerings.append((Block(t), False))
        powerings.append((Block(t), True))
    room.loop('wood_power', main_clock).loop(wood_power_loop, powerings)

    light_detector_funcs(room)
    note_block_funcs(room)
    pressure_plate_funcs(room)


def light_detector_funcs(room):
    height = 8
    day_times = (
        8000, 9200, 10000, 10400, 10800, 11100, 11600, 11900, 12100, 12300, 12600, 12800, 13100, 13400, 19000, 22500,
        23000, 23100, 23400, 23600, 23800, 0, 300, 700, 1000, 1500, 2000, 2700, 3500, 4400,)
    inv_times = [23960, 23959, 23780, 23600, 23400, 23200, 23100, 22900, 22800, 22600, 22400, 22300, 0, 1, 2, 3]
    inv_times = list(reversed(inv_times)) + inv_times[1: -1]

    daylight_inv = room.score('daylight_inv')
    daylight_detector = room.score('daylight_detector')

    def daylight_detector_loop(step):
        i = step.i
        inv = inv_times[i]
        yield execute().if_().score(daylight_inv).matches(0).run(time().set(day_times[i]))
        if inv > .22200:
            yield execute().if_().score(daylight_inv).matches(1).run(time().set(inv))
        else:
            yield execute().if_().score(daylight_inv).matches(1).run(time().set(22300))
            yield execute().if_().score(daylight_inv).matches(1).run(
                fill(r(inv, height, inv), r(-inv, height, -inv), 'stone'))

    room.loop('daylight_detector', main_clock).add(
        execute().at(e().tag('daylight_detector_setup_home')).run(
            function('restworld:redstone/daylight_detector_setup')),
        fill(r(3, height, 3), r(-3, height, -3), 'air')
    ).loop(daylight_detector_loop, day_times)
    room.function('daylight_detector_reset').add(
        time().set(NOON),
        execute().at(e().tag('daylight_detector_home')).run(fill(r(3, 8, 3), r(-3, 8, -3), 'air')),
        daylight_detector.set(0),
        kill(e().tag('daylight_detector_home'))
    )
    room.function('daylight_detector_setup').add(
        daylight_inv.set(0),
        execute().if_().block(r(0, 2, 1), ('daylight_detector', {'inverted': True})).run(daylight_inv.set(1)),
        execute().if_().score(daylight_inv).matches(0).run(Sign.change(r(0, 2, 0), (None, 'Daylight Detector', ''))),
        execute().if_().score(daylight_inv).matches(1).run(
            Sign.change(r(0, 2, 0), (None, 'Inverted', 'Daylight Detector')))
    )
    room.function('daylight_detector_setup_init').add(
        WallSign(()).place(r(0, 2, 0), EAST),
        execute().at(e().tag('daylight_detector_setup_home')).run(
            function('restworld:redstone/daylight_detector_setup')),
        label(r(2, 2, 2), 'Daylight Changing'),
        label(r(2, 2, 0), 'Invert Detector'))


def note_block_funcs(room):
    instrument = room.score('instrument')
    note_powered = room.score('note_powered')

    def note_block_loop(step):
        for i, inst in enumerate(instruments):
            yield execute().if_().score(instrument).matches(i).run(
                setblock(r(0, 3, 0), ('note_block', {'note': step.elem, 'instrument': inst.id})))

    room.loop('note_block', fast_clock).loop(note_block_loop, range(0, 25)).add(
        execute().if_().score(note_powered).matches(1).run(setblock(r(0, 3, -1), 'redstone_torch')),
        execute().if_().score(note_powered).matches(1).run(setblock(r(0, 3, -1), 'air')))

    note_block_init = room.function('note_block_init').add(instrument.set(0), setblock(r(0, 2, 0), 'grass_block'))
    for i, instr in enumerate(instruments):
        row_len = len(instruments) / 2
        x = i % row_len
        if x >= row_len / 2:
            x += 1
        x -= row_len / 2
        x = int(x)
        y = 3 - int(i / row_len)
        note_block_init.add(
            WallSign(
                (None, instr.name, f'({instr.exemplar.name})'),
                (instrument.set(i),
                 execute().at(e().tag('note_block_home')).run(setblock(r(0, 2, 0), instr.exemplar)))
            ).place(r(x, y, 1), SOUTH),
            label(r(0, 2, 1), 'Powered')
        )


def pressure_plate_funcs(room):
    def one_item():
        return summon(('item', {'Item': Item.nbt_for('iron_pickaxe'), 'Age': -32768, 'PickupDelay': 2147483647,
                                'Tags': ['plate_items']}), r(0, 3, 0))

    plate_heavy = room.score('plate_heavy')
    pressure_plate = room.score('pressure_plate')
    room.function('pressure_plate_add', home=False).add(
        one_item(),
        (execute().if_().score(plate_heavy).matches((1, None)).run(one_item()) for _ in range(0, 9)))
    room.function('pressure_plate_init').add(label(r(2, 2, 0), 'Pressure Plate Type'))

    room.function('pressure_plate_cur').add(
        kill(e().tag('plate_items')),
        (execute().if_().score(pressure_plate).matches((i, None)).run(function(
            'restworld:redstone/pressure_plate_add')) for i in range(1, 16)))

    room.loop('pressure_plate', main_clock).add(
        execute().if_().score(pressure_plate).matches(0).run(kill(e().tag('plate_items'))),
        execute().unless().score(pressure_plate).matches(0).run(function('restworld:redstone/pressure_plate_add'))
    ).loop(None, range(0, 16))

    def plate(heavy):
        which = 'Heavy' if heavy else 'Light'
        plate_heavy = room.score('plate_heavy')
        yield execute().at(e().tag('pressure_plate_home')).run(
            setblock(r(0, 3, 0), f'{which.lower()}_weighted_pressure_plate'))
        yield execute().at(e().tag('pressure_plate_home')).run(Sign.change(r(1, 2, 0), (None, which, 'Pressure Plate')))
        yield plate_heavy.set(int(heavy))
        yield kill(e().tag('plate_items'))
        yield pressure_plate.set(0)

    room.function('switch_to_heavy', home=False).add(plate(True))
    room.function('switch_to_light', home=False).add(plate(False))
