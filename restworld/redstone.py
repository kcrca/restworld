from __future__ import annotations

import re

from pynecraft import info
from pynecraft.base import DOWN, EAST, NOON, SOUTH, UP, WEST, r
from pynecraft.commands import BYTE, Block, INT, RESULT, Score, data, e, execute, fill, function, item, kill, \
    random, return_, setblock, summon, tag, time
from pynecraft.info import instruments, stems
from pynecraft.simpler import Item, Region, Sign, WallSign
from restworld.rooms import Room, ensure, if_clause, kill_em
from restworld.world import fast_clock, main_clock, restworld


def room():
    room = Room('redstone', restworld, SOUTH, (None, 'Redstone'))

    room.function('dispenser_init').add(WallSign(()).place(r(0, 3, 0), WEST))

    def dispenser_loop(step):
        yield setblock(r(0, 2, 0), (step.elem, {'facing': UP}))
        yield setblock(r(1, 4, 0), (step.elem, {'facing': WEST}))
        yield setblock(r(0, 6, 0), (step.elem, {'facing': DOWN}))
        room.particle(step.elem, 'dispenser', r(1, 5, 0), step)
        yield Sign.change(r(0, 3, 0), (None, step.elem))

    room.loop('dispenser', main_clock).loop(dispenser_loop, ('Dispenser', 'Dropper'))
    room.function('hopper_init').add(WallSign((None, 'Which way are', 'they pointing?')).place(r(2, 3, 1), WEST))
    room.particle('hopper', 'hopper', r(1, 3, 1))

    def lever_loop(step):
        block = ('lever', {'powered': step.elem, 'face': 'floor'})
        yield setblock(r(0, 3, 0), block)
        room.particle(block, 'lever', r(0, 4, 0), step)

    room.loop('lever', main_clock).loop(lever_loop, (False, True))
    room.particle('tripwire', 'lever', r(0, 3, 2))

    def lightning_rod_loop(step):
        if step.elem:
            yield summon('lightning_bolt', r(0, 3, 0))
            yield Sign.change(r(1, 2, 0), ('Lightning &', None, '(Powered)'), start=1)
        else:
            yield Sign.change(r(1, 2, 0), ('', None, ''), start=1)
        yield setblock(r(0, 3, 0), Block('lightning_rod', {'powered': step.elem})),

    room.loop('lightning_rod', main_clock).loop(lightning_rod_loop, (True, False))
    room.function('lightning_rod_init').add(
        setblock(r(0, 3, 0), 'lightning_rod'),
        WallSign((None, 'Lightning &', 'Lightning Rod')).place(r(1, 2, 0), EAST))
    room.particle('lightning_rod', 'lightning_rod', r(0, 4, 0))

    minecart_types = list(Block(f'{t}Minecart') for t in
                          ('', 'Chest|', 'Furnace|', 'TNT|', 'Hopper|', 'Spawner|', 'Command Block|'))

    def minecart_loop(step):
        yield kill_em(e().tag('minecart_type'))
        yield summon(step.elem.merge_nbt({'Tags': ['minecart_type']}), r(0, 3, 0))
        yield data().merge(r(-1, 2, 0), step.elem.sign_nbt())

    room.loop('minecarts', main_clock).loop(minecart_loop, minecart_types)
    room.function('minecarts_init').add(room.label(r(-5, 2, 2), 'Reset Room', SOUTH))

    def observer_loop(step):
        block = ('observer', {'powered': step.elem, 'facing': WEST})
        yield setblock(r(0, 2, 0), block)
        if step.elem:
            yield setblock(r(-1, 2, 0), 'stone')
            yield setblock(r(-1, 2, 0), 'air')
        room.particle(block, 'observer', r(0, 3, 0), step)
        room.particle(Block('redstone_lamp', state={'lit': step.elem}), 'observer', r(2, 4, 0), step)

    room.loop('observer', main_clock).loop(observer_loop, (True, False))
    room.particle('trapped_chest', 'observer', r(0, 4, 3))
    room.function('piston_init').add(WallSign(()).place(r(-1, 2, 0), WEST))

    def piston_loop(step):
        extended = step.i in (1, 4)
        block = 'redstone_block' if extended else 'air'
        piston = 'Piston' if step.i < 3 else 'Sticky Piston'
        yield ensure(r(1, 3, 0), block)
        if step.i in (0, 3):
            yield ensure(r(0, 3, 0), f'{piston}[facing=west]')
            yield ensure(r(1, 4, 0), f'{piston}[facing=up,]')
        room.particle(piston, 'piston', r(0, 4, 0), step)
        yield WallSign((None, piston)).place(r(-1, 2, 0), WEST)

    room.loop('piston', main_clock).loop(piston_loop, range(6))

    def copper_bulb_loop(step):
        bulb = Block(step.elem)
        # We want "powered" to stay the same when switching oxidation level
        powered = (step.i + int(step.i / 4)) % 2 == 0
        lit = step.i % 4 < 2
        yield ensure(r(0, 3, 0), bulb)
        room.particle(bulb, 'copper_bulb', r(0, 4, 0), step)
        yield setblock(r(-1, 2, 0), 'air')
        yield setblock(r(0, 2, 0), ('redstone_wall_torch', {'facing': WEST}) if powered else 'air')
        state_names = []
        if powered:
            state_names.append('Powered')
        if lit:
            state_names.append('Lit')
        state = ', '.join(state_names)
        text = [''] + list(bulb.sign_text)
        text.extend([''] * (4 - len(text)))
        text[3] = f'({state})' if len(state) > 0 else ''
        yield WallSign(text).place(r(-1, 2, 0), WEST)

    bulbs = []
    for s in ('', 'Exposed', 'Weathered', 'Oxidized'):
        bulb = re.sub(r'^\|', '', f'{s}|Copper Bulb')
        bulbs.extend((bulb,) * 4)
    room.loop('copper_bulb', fast_clock).loop(copper_bulb_loop, bulbs)

    room.function('rail_init').add(WallSign(()).place(r(1, 2, -2), WEST))
    rails = (
        ('Rail', False),
        ('Powered Rail', False), ('Powered Rail', True),
        ('Detector Rail', False), ('Detector Rail', True),
        ('Activator Rail', False), ('Activator Rail', True),
    )
    room.function('rail_clean', home=False).add(kill_em(e().tag('tmp_minecart')))

    rube_locs = {r(0, 5, -1): '⬆', r(0, 6, 0): '⮕'}

    def rube_loop(step):
        for r, loc in enumerate(rube_locs):
            if r == step.i:
                ch = rube_locs[loc]
                yield WallSign(('', 'Start Here', f'{ch}{ch}')).place(loc, EAST)
            else:
                yield setblock(loc, 'air')

    room.loop('rube', fast_clock).loop(rube_loop, rube_locs.keys())
    room.function('rube_init').add(
        kill(e().type('minecart').volume((-10, 10, -10))),
        kill(e().type('furnace_minecart').volume((-10, 10, -10))),
        setblock(r(-6, 0, -8), 'redstone_block'),
        setblock(r(-6, 0, -8), 'air')
    )

    f_shapes = ['small_ball', 'large_ball', 'star', 'creeper', 'burst']
    f_colors = (
        0x815231,  # yellow
        # 0x0f1015  # black
        0x313497,  # blue
        0xfefefe,  # white
        0x992621,  # red
        0x8932b8,  # purple
        0xec80b5,  # pink
        0xec6d0b,  # orange
        0xb53cab,  # magenta
        0x7fc61e,  # lime
        # 0x9c9c96, # light grey
        0x4cc4e6,  # light blue
        # 0x815231, # brown
        0x5d7b16,  # green
        # 0x3b3f43, # grey
        0x3b3f43,  # cyan
    )
    f_range = 100_000
    f_odds = {
        'explosions': [41158, 67392, 83296, 92268, 96884, 98972, 99767, 99973, 100000],
        'colors': [76324, 96936, 100000], 'fade_colors': [76324, 96936, 100000], 'has_trail': [66667, 100000],
        'has_twinkle': [66667, 100000]
    }
    holder = room.score('holder')
    explosions_cnt = room.score('explosions_cnt')
    val_cnt = room.score('val_cnt')
    fade = room.score('fade')

    def raw_odds_value(name, store):
        yield execute().store(RESULT).storage(room.store, f'{store}.{name}', INT, 1).run(
            random().value((0, f_range - 1)))

    def val_odds_value(name: str, nbt_path_top: str, min: int = 0, score: Score = None):
        odds = f_odds[name]
        yield execute().store(RESULT).score(holder).run(data().get(room.store, f'{nbt_path_top}_raw.{name}'))
        prev = 0
        nbt_path = f'{nbt_path_top}_val.{name}'
        for i, v in enumerate(odds):
            end = v - 1
            if i == len(odds) - 1:
                end = None
            set_value = data().modify(room.store, nbt_path).set().value(i + min)
            if i > 0:
                set_value = execute().if_().score(holder).matches((prev, end)).run(set_value)
            yield set_value
            prev = v
        if score:
            yield execute().store(RESULT).score(score).run(data().get(room.store, nbt_path))

    def expand(name, nbt_path, score, func):
        singular = name[:-1]
        for i in range(len(f_odds[name])):
            cmds = (function(func),
                    data().modify(room.store, f'{nbt_path}.{name}').append().from_(room.store, f'{singular}_val'))
            if i > 0:
                cmds = execute().if_().score(score).matches((i + 1, None)).run(cmds)
            yield cmds

    explosion_raw = room.function('explosion_raw', home=False).add(
        execute().store(RESULT).storage(room.store, 'explosion_raw.shape', BYTE, 1).run(
            random().value((0, len(f_shapes) - 1))),
        raw_odds_value('has_trail', 'explosion_raw'),
        raw_odds_value('has_twinkle', 'explosion_raw'),
        raw_odds_value('colors', 'explosion_raw'),
        execute().store(RESULT).score(fade).run(random().value((0, 4))),
        execute().if_().score(fade).matches(0).run(raw_odds_value('fade_colors', 'explosion_raw')),
    )
    color_add = room.function('color_add', home=False).add(
        data().modify(room.store, 'explosion_val.$(which)').append().from_(room.store, 'fireworks.colors[$(color)]'))

    def colors_add():
        for name in 'colors', 'fade_colors':
            yield data().remove(room.store, f'{name}_raw')
            yield data().remove(room.store, f'{name}_val')
            yield data().modify(room.store, f'{name}_raw.which').set().value(name)
            yield data().modify(room.store, f'explosion_val.{name}').set().value([])
            for i in range(len(f_odds[name])):
                cmds = (
                    execute().store(RESULT).storage(room.store, f'{name}_raw.color', INT, 1).run(
                        random().value((0, len(f_colors) - 1))),
                    function(color_add).with_().storage(room.store, f'{name}_raw')
                )
                if i > 0:
                    cmds = execute().if_().score(val_cnt).matches((i, None)).run(cmds)
                if name == 'fade_colors':
                    cmds = execute().if_().score(fade).matches(0).run(cmds)
                yield cmds

    explosion_convert = room.function('explosion_convert', home=False).add(
        data().modify(room.store, 'explosion_val.shape').set().from_(room.store, 'fireworks.shapes[$(shape)]'),
        val_odds_value('has_trail', 'explosion'),
        val_odds_value('has_twinkle', 'explosion'),
        val_odds_value('colors', 'explosion', 1, val_cnt),
        execute().if_().score(fade).matches(0).run(val_odds_value('fade_colors', 'explosion', 1, val_cnt)),
        colors_add(),
    )
    explosion_add = room.function('explosion_add', home=False).add(
        data().remove(room.store, 'explosion_raw'),
        data().remove(room.store, 'explosion_val'),
        function(explosion_raw),
        function(explosion_convert).with_().storage(room.store, 'explosion_raw'),
    )
    new_firework_convert = room.function('new_firework_convert', home=False).add(
        data().modify(room.store, 'new_firework_val.explosions').set().value([]),
        expand('explosions', 'new_firework_val', explosions_cnt, explosion_add),
        execute().store(RESULT).storage(room.store, 'new_firework_val.flight_duration', BYTE, 1).run(
            random().value((1, 4))),
    )

    room.function('fireworks_init').add(
        data().remove(room.store, 'fireworks'),
        data().modify(room.store, 'fireworks').set().value({'shapes': f_shapes, 'colors': f_colors}),
    )
    room.loop('fireworks', main_clock).add(
        execute().if_().items(r(0, 2, 0), 'container.*', 'firework_rocket').run(return_()),
        data().remove(room.store, 'new_firework_raw'),
        data().remove(room.store, 'new_firework_val'),
        (raw_odds_value('explosions', 'new_firework_raw')),
        (val_odds_value('explosions', 'new_firework', 1, explosions_cnt)),
        function(new_firework_convert),
        function(new_firework_convert).with_().storage('new_firework_raw'),
        item().replace().block(r(0, 2, 0), 'container.0').with_(Item('firework_rocket')),
        data().modify(r(0, 2, 0), 'Items[0].components.fireworks').set().from_(room.store, 'new_firework_val')
    )

    def rail_loop(step):
        volume = Region(r(3, 3, -3), r(0, 0, 0))
        rail, on = step.elem
        added = dict(powered=True) if on else None
        yield volume.replace_straight_rails(rail, '#rails', added)
        room.particle(Block(rail, state=added), 'rail', r(0, 2, -2), step)
        if on:
            yield volume.replace('redstone_torch', 'glass')
        else:
            yield volume.replace('glass', 'redstone_torch')
        yield Sign.change(r(1, 2, -2), (None, rail, '(Powered)' if on else ''))

    room.loop('rail', main_clock).loop(rail_loop, rails)
    room.particle('rail', 'rail', r(0, 2, -1))

    room.function('redstone_lamp_init').add(WallSign((None, 'Redstone Lamp')).place(r(-1, 3, 0), EAST))
    room.loop('redstone_lamp', main_clock).loop(lambda step: setblock(r(0, 0, 0), step.elem),
                                                ('Redstone Torch', 'Air'))
    room.function('redstone_wire_init').add(WallSign((None, 'Redstone Wire')).place(r(0, 2, 0), WEST))
    room.particle('redstone_wire', 'redstone_wire', r(4, 3, 2))

    def redstone_wire_loop(step):
        volume = Region(r(0, 0, 0), r(7, 0, 7))
        if step.i == 0:
            yield volume.replace('redstone_torch', 'glass')
            yield Sign.change(r(0, 2, 0), (None, None, '(Powered)'))
        else:
            yield volume.replace('glass', 'redstone_torch')
            yield Sign.change(r(0, 2, 0), (None, None, ''))

    room.loop('redstone_wire', main_clock).loop(redstone_wire_loop, range(0, 2))

    def repeater_loop(step):
        on, locked, ticks = step.elem
        repeater = Block('repeater', {'facing': EAST, 'powered': on, 'locked': locked, 'delay': ticks})
        yield setblock(r(0, 2, 0), repeater)
        room.particle(repeater, 'repeater', r(0, 2.5, 0), step)
        yield setblock(r(1, 2, 0), 'redstone_block' if on else 'air')
        if locked:
            yield setblock(r(0, 2, 1), ('repeater', {'powered': True, 'facing': SOUTH}))
            yield setblock(r(0, 2, 2), 'redstone_block')
        else:
            yield fill(r(0, 2, 1), r(0, 2, 2), 'air')
        desc = 'Powered' if on else ''
        if locked:
            if desc:
                desc += ', '
            desc += 'Locked'
        yield WallSign.change(r(1, 3, 0), (None, None, desc, f'Delay: {ticks}'))

    room.loop('repeater', fast_clock).loop(
        repeater_loop,
        tuple((True, True, t) for t in range(1, 5)) +
        tuple((True, False, t) for t in range(4, 0, -1)) +
        tuple((False, False, t) for t in range(1, 5)) +
        tuple((False, True, t) for t in range(4, 0, -1))
    )
    room.function('repeater_init').add(
        WallSign((None, 'Repeater')).place(r(1, 3, 0), EAST),
        room.label(r(-5, 2, 1), 'Show Particles', SOUTH),
        # room.label(r(2, 2, 2), 'Change Daylight', WEST),
    )

    def comparator_loop(step):
        on, cmp = step.elem
        mode = 'compare' if cmp == 0 else 'subtract'
        comparator = Block('comparator', {'facing': EAST, 'powered': on, 'mode': mode})
        yield setblock(r(0, 2, 0), comparator)
        room.particle(comparator, 'comparator', r(0, 2.5, 0), step)
        yield setblock(r(1, 2, 0), 'redstone_block' if on else 'air')
        yield Sign.change(r(1, 3, 0), (None, None, f'Mode: {mode.title()}'))

    room.loop('comparator', main_clock).loop(comparator_loop,
                                             ((True, False), (True, True), (False, True), (False, False)))
    room.function('comparator_init').add(WallSign((None, 'Comparator')).place(r(1, 3, 0), EAST))

    def sculk_loop(step):
        if step.i == 0:
            block = 'Sculk Sensor'
            yield Sign.change(r(-1, 3, -0), (None, ''))
        else:
            # Shows up waterlogged by default; see https://bugs.mojang.com/browse/MC-261388
            block = Block('Calibrated|Sculk Sensor', {'waterlogged': False, 'facing': WEST})
            yield Sign.change(r(-1, 3, -0), (None, 'Calibrated'))
        yield setblock(r(0, 2, 0), block)
        room.particle(block, 'sculk', r(0, 3, 0), step)
        yield setblock(r(-4, 2, 0), 'air' if step.i < 2 else 'redstone_block')

    room.function('sculk_init').add(WallSign((None, None, 'Sculk Sensor')).place(r(-1, 3, 0), EAST))
    room.loop('sculk', main_clock).loop(sculk_loop, range(4))

    room.function('target_init').add(WallSign((None, 'Target', None, '(vanilla shows 1)')).place(r(1, 3, 0), WEST))
    room.particle('target', 'target', r(0, 3, 0))

    def target_loop(step):
        yield setblock(r(0, 2, 0), ('target', {'power': step.i}))
        yield Sign.change(r(1, 3, 0), (None, None, f'Power {step.i:d}'))

    room.loop('target', fast_clock).loop(target_loop, range(0, 16))
    room.function('wire_strength_init').add(
        fill(r(1, 2, -1), r(1, 2, -16),
             ('oak_wall_sign', {'facing': WEST}, {'front_text': Sign.lines_nbt((None, None, 'Powered'))})))

    def wire_strength_loop(step):
        block = 'redstone_block' if step.i == 0 else 'air'
        yield setblock(r(0, 2, 0), block)
        if block != 'air':
            room.particle(block, 'wire_strength', r(0, 3, 0), step)
        for i in range(0, 16):
            if step.i == 0:
                yield Sign.change(r(1, 2, -(16 - i)), (None, f'{i}'))
            else:
                yield Sign.change(r(1, 2, -(16 - i)), (None, 'Not'))

    room.loop('wire_strength', main_clock).loop(wire_strength_loop, (0, 1))

    def wood_power_loop(step):
        wood, powered = step.elem
        pressure_plate = (f'{wood.id}_pressure_plate', {'powered': powered})
        button = (f'{wood.id}_button', {'facing': EAST, 'powered': powered})
        room.particle(pressure_plate, 'wood_power', r(1, 2, -1), step)
        room.particle(button, 'wood_power', r(1, 3.5, 0), step)
        yield setblock(r(1, 2, -1), pressure_plate)
        yield setblock(r(1, 3, 0), button)
        yield setblock(r(0, 3, 0), ('redstone_lamp', {'lit': powered}))
        yield setblock(r(0, 2, -1), ('redstone_lamp', {'lit': powered}))
        yield setblock(r(1, 2, 0), ('pale_oak_wall_sign', {'facing': EAST}))
        yield data().merge(r(1, 2, 0), wood.sign_nbt())
        if powered:
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
    inv_times = [6000, 23959, 23780, 23600, 23400, 23200, 23100, 22900, 22800, 22600, 22400, 22300, 0, 1, 2, 3]
    inv_times = list(reversed(inv_times)) + inv_times[1: -1]

    daylight_inv = room.score('daylight_inv')
    daylight_detector = room.score('daylight_detector')

    def daylight_detector_loop(step):
        i = step.i
        inv = inv_times[i]
        yield execute().if_().score(daylight_inv).matches(0).run(time().set(day_times[i]))
        if inv > 1000:
            yield execute().if_().score(daylight_inv).matches(1).run(time().set(inv))
        else:
            yield execute().if_().score(daylight_inv).matches(1).run(time().set(22300))
            yield execute().if_().score(daylight_inv).matches(1).run(
                fill(r(inv, height, inv), r(-inv, height, -inv), 'stone'))

    room.loop('daylight_detector', main_clock).add(
        execute().at(e().tag('daylight_detector_setup_home')).run(
            function('restworld:redstone/daylight_detector_setup')),
        fill(r(3, height, 3), r(-3, height, -3), 'air')).loop(daylight_detector_loop, day_times)
    room.function('daylight_detector_reset').add(
        time().set(NOON), execute().at(e().tag('daylight_detector_home')).run(
            fill(r(3, 8, 3), r(-3, 8, -3), 'air')), daylight_detector.set(0), kill(e().tag('daylight_detector_home')))
    room.function('daylight_detector_setup').add(
        daylight_inv.set(0),
        execute().if_().block(r(0, 2, 1), ('daylight_detector', {'inverted': True})).run(daylight_inv.set(1)),
        execute().if_().score(daylight_inv).matches(0).run(Sign.change(r(0, 2, 0), (None, 'Daylight Detector', ''))),
        execute().if_().score(daylight_inv).matches(1).run(
            Sign.change(r(0, 2, 0), (None, 'Inverted', 'Daylight Detector'))))
    room.function('daylight_detector_setup_init').add(
        WallSign(()).place(r(0, 2, 0), EAST),
        execute().at(e().tag('daylight_detector_setup_home')).run(
            function('restworld:redstone/daylight_detector_setup')),
        room.label(r(2, 2, 2), 'Change Daylight', EAST),
        room.label(r(2, 2, 0), 'Invert', EAST))
    room.particle('daylight_detector', 'daylight_detector_setup', r(0, 2.75, 1), clause=if_clause(daylight_inv, 0))
    room.particle(('daylight_detector', {'inverted': True}), 'daylight_detector_setup', r(0, 2.5, 1),
                  clause=if_clause(daylight_inv, 1))


def note_block_funcs(room):
    instrument = room.score('instrument')
    note_powered = room.score('note_powered')

    start = room.function('start_note_blocks', home=False).add(
        tag(e().tag('note_home')).remove('instrument_home'), tag(e().tag('note_home')).add('note_block_home'))
    room.function('start_instruments', home=False).add(
        tag(e().tag('note_home')).remove('note_block_home'), tag(e().tag('note_home')).add('instrument_home'))

    sign_pos = r(0, 2, 1)
    note_display = WallSign((None, 'A')).glowing(True)
    note_block_init = room.function('note_init').add(
        note_display.place(sign_pos, SOUTH),
        function(start),
        function('restworld:redstone/instrument_cur'),
        function('restworld:redstone/note_block_cur'),
    )
    sign_locs = []
    for i, instr in enumerate(instruments):
        row_len = len(instruments) / 2
        x = i % row_len
        if x >= row_len / 2:
            x += 1
        x -= row_len / 2
        x = int(x)
        y = 3 - int(i / row_len)
        loc = r(x, y, 1)
        sign_locs.append(loc)
        note_block_init.add(
            WallSign(
                (None, instr.name, f'({instr.exemplar.name})'),
                (instrument.set(i),
                 execute().at(e().tag('note_home')).run(setblock(r(0, 2, 0), instr.exemplar)),
                 execute().at(e().tag('note_home')).run(function('restworld:redstone/instrument_cur')))
            ).place(loc, SOUTH),
            room.label(r(1, 2, 2), 'Play Notes', SOUTH),
            room.label(r(-1, 2, 2), 'Instruments', SOUTH))

    notes = (
        'Low F♯/G♭', 'Low G', 'Low G♯/A♭', 'Low A', 'Low A♯/B♭', 'Low B', 'Low C', 'Low C♯/D♭', 'Low D', 'Low D♯/E♭',
        'Low E', 'Low F', 'Mid F♯/G♭', 'Mid G', 'Mid G♯/A♭', 'Mid A', 'Mid A♯/B♭', 'Mid B', 'Mid C', 'Mid C♯/D♭',
        'Mid D', 'Mid D♯/E♭', 'Mid E', 'Mid F', 'High F♯/G♭')

    def note_block_loop(step):
        yield setblock(r(0, 3, 0), ('note_block', {'note': step.i}))
        yield Sign.change(sign_pos, (None, *step.elem.split(' ')))

    def instrument_loop(step):
        yield setblock(r(0, 2, 0), step.elem.exemplar)
        yield data().modify(sign_locs[step.i], 'front_text.has_glowing_text').set().value(True)
        yield data().modify(sign_locs[step.i], 'back_text.has_glowing_text').set().value(True)

    note_block_func = room.loop('note_block', home=False).loop(note_block_loop, notes)
    instrument_func = room.loop('instrument', home=False).add(
        (data().modify(x, 'front_text.has_glowing_text').set().value(False) for x in sign_locs),
        (data().modify(x, 'back_text.has_glowing_text').set().value(False) for x in sign_locs),
    ).loop(instrument_loop, instruments)

    room.loop('note', fast_clock).add(
        execute().at(e().tag('note_block_home')).run(function(note_block_func)),
        execute().at(e().tag('instrument_home')).run(function(instrument_func)),
        setblock(r(0, 3, -1), 'air'),
        execute().if_().score(note_powered).matches(1).run(
            setblock(r(0, 3, -1), ('redstone_wall_torch', {'facing': 'south'}))),
    )
    room.particle('note_block', 'note', r(0, 4, 0))


def pressure_plate_funcs(room):
    def one_item():
        return summon(('item', {'Item': Item.nbt_for('iron_pickaxe'), 'Age': -32768, 'PickupDelay': 2147483647,
                                'Tags': ['plate_items']}), r(0, 3, 0))

    plate_heavy = room.score('plate_heavy')
    pressure_plate = room.score('pressure_plate')
    room.function('pressure_plate_add', home=False).add(one_item(), (
        execute().if_().score(plate_heavy).matches((1, None)).run(one_item()) for _ in range(0, 9)))
    room.function('pressure_plate_init').add(room.label(r(2, 2, 0), 'Heavy', EAST))
    room.function('pressure_plate_cur').add(kill(e().tag('plate_items')),
                                            (execute().if_().score(pressure_plate).matches((i, None)).run(function(
                                                'restworld:redstone/pressure_plate_add')) for i in range(1, 16)))

    room.loop('pressure_plate', main_clock).add(
        execute().if_().score(pressure_plate).matches(0).run(kill(e().tag('plate_items'))),
        execute().unless().score(pressure_plate).matches(0).run(
            function('restworld:redstone/pressure_plate_add'))).loop(None, range(0, 16))

    plate_heavy = room.score('plate_heavy')

    def plate(heavy):
        which = 'Heavy' if heavy else 'Light'
        plate_id = f'{which.lower()}_weighted_pressure_plate'
        yield execute().at(e().tag('pressure_plate_home')).run(
            setblock(r(0, 3, 0), plate_id))
        yield execute().at(e().tag('pressure_plate_home')).run(Sign.change(r(1, 2, 0), (None, which, 'Pressure Plate')))
        yield plate_heavy.set(int(heavy))
        yield kill(e().tag('plate_items'))
        yield pressure_plate.set(0)
        room.particle(plate_id, 'pressure_plate', r(0, 3.1, 0), clause=if_clause(plate_heavy, int(heavy)))

    room.function('switch_to_heavy', home=False).add(plate(True))
    room.function('switch_to_light', home=False).add(plate(False))
