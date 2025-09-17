from __future__ import annotations

import sys

from pynecraft.base import r
from pynecraft.commands import CREATIVE, Commands, Entity, SIDEBAR, clear, data, e, \
    execute, fill, function, gamemode, kill, p, scoreboard, setblock, tp
from pynecraft.function import Function
from pynecraft.simpler import Sign, TextDisplay
from restworld.rooms import Clock, Room, RoomPack

marker_tmpl = Entity('armor_stand', {'NoGravity': True, 'Small': True, })


class RestWorld(RoomPack):
    def __init__(self):
        suffixes = list(RoomPack.base_suffixes)
        suffixes.extend(list(x.name for x in self.clocks()))
        super().__init__('restworld', suffixes, 4)

    def finalize(self):
        for kid in self.function_set.children:
            if isinstance(kid, Room):
                kid.finalize()

    def save(self, *args, **kwargs):
        self.finalize()
        for f in self.world_funcs():
            self.function_set.add(f)
        self.function_set.add(Function('ready').add(
            clear(p()),
            gamemode(CREATIVE, p()),
            function('restworld:global/control_book'),
            tp(p(), (0, 101, 0)).facing((0, 99, 7)),
            scoreboard().objectives().setdisplay(SIDEBAR),
            function('restworld:center/reset_clocks'),
            function('restworld:global/clock_on'),
            function("restworld:_exit"),  # Leave any room we were in by leaving them all
            execute().at(e().tag('particles_action_home')).run(setblock(r(0, 2, -3), 'air')),
            execute().at(e().tag('font_run_home')).run(fill(r(-3, 2, 2), r(3, 2, 2), 'air')),
            execute().at(e().tag('maps_room_home')).run(setblock(r(8, 2, -2), 'air')),
            execute().at(e().tag('paintings_home')).run(function('restworld:paintings/_init')),
            function('restworld:global/power_off'),
            kill(e().type('item')),
        ))
        super().save(*args, **kwargs)

    # noinspection PyMethodMayBeStatic
    def clocks(self):
        return slow_clock, main_clock, fast_clock


    def _home_func_name(self, base):
        for f in self._suffixes:
            if base.endswith('_' + f):
                base = base[:-(len(f) + 1)]
                break
        return base + '_home'

    def world_funcs(self):
        for f in self._suffixes:
            func_name = '_' + f
            func = Function(func_name)
            for room in self.function_set.children:
                call = function(room.full_name + '/' + func_name)
                if f in ('incr', 'decr'):
                    call = execute().at(e().tag(f'{room.name}_player_home')).run(call)
                func.add(call)
            yield func


class Fencelike:
    @classmethod
    def update(cls, id, text2, text3='') -> Commands:
        return (
            fill(r(8, 3, 6), r(0, 2, 0), id).replace('#restworld:fencelike'),
            data().merge(r(5, 2, 0), Sign.lines_nbt(('', text2, text3, '')))
        )


clock = Clock('clock')
slow_clock = Clock('slow', 60)
main_clock = Clock('main', 30)
fast_clock = Clock('fast', 15)
tick_clock = Clock('clock')
restworld = RestWorld()


def die(*msg: str):
    sys.stderr.write(*msg)
    sys.exit(1)


class Wall:
    def __init__(self, width, used, facing, block_at, y_first=3, y_last=1, used_widths=None, start=None, skip=None):
        self.width = width
        self.provided_start = start
        self.facing = facing
        self.block_at = block_at
        self.y_first = y_first
        self.y_last = y_last
        if used_widths is None:
            used_widths = (used,) * 10
        self.used_widths = used_widths
        self.skip = skip if skip else {}
        self.line = 0
        self.start = None
        self.end = None
        self.set_line_range()

    def set_line_range(self):
        self.start = self.provided_start
        if not self.start:
            self.start = int((self.width - self.used_widths[self.line]) / 2)
        self.end = self.start + self.used_widths[self.line]

    def to_next_wall(self, tag):
        return f'execute as @e[tag={tag}] run execute at @s run teleport @s ^-{self.width - 1:d} ^0 ^0 ~90 ~'

    def start_pos(self):
        return self.start, self.y_first

    def next_pos(self, x, y):
        # The top row is sparse
        x += 1
        try:
            skip = self.skip[y]
            while skip and x - self.start in range(skip[0], skip[1] + 1):
                x += 1
        except KeyError:
            pass
        if y == 4 and x == 3:
            # Skip the middle position
            x += 1
        if x >= self.end:
            self.line += 1
            if self.line >= len(self.used_widths):
                return None, None
            self.set_line_range()
            y -= 1
            x = self.start
            if y < self.y_last:
                return None, None
        return x, y


def text_display(text: str, shown: bool = True) -> TextDisplay:
    return TextDisplay(text, nbt={'Rotation': [180.0, 0.0], 'text_opacity': 255 if shown else 25, 'background': 0,
                                  'billboard': 'vertical', 'shadow_radius': 0}).scale(0.6)
