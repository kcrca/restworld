from __future__ import annotations

import sys
from datetime import date

from pynecraft.base import DARK_GREEN, DARK_PURPLE, r
from pynecraft.commands import Commands, Entity, JsonText, data, e, execute, fill, function, give, p, tp
from pynecraft.function import Function, FunctionSet
from pynecraft.simpler import Book, Sign
from restworld.rooms import Clock, Room, RoomPack


def kill_em(target):
    return tp(target, e().tag('death').limit(1))


marker_tmpl = Entity('armor_stand', {'NoGravity': True, 'Small': True, })


class Restworld(RoomPack):
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
        gs = self.function_set.child('global')
        if gs is None:
            gs = FunctionSet('global', self.function_set)
        gs.add(self.control_book_func())
        self.function_set.add(*self.world_funcs())
        super().save(*args, **kwargs)

    # noinspection PyMethodMayBeStatic
    def clocks(self):
        return slow_clock, main_clock, fast_clock

    def control_book_func(self) -> Function:
        cb = Book()
        cb.sign_book('Control Book', 'RestWorld', 'Useful Commands')

        cb.add(r'Clock State:\n      ',
               self._action(r'|\u25c0\u25c0', 'Previous', '_decr'), r'  ',
               self._action(r'||', 'Play/Pause', 'global/clock_toggle').bold(),
               self._action(r'/\u25b6', 'Play/Pause', 'global/clock_toggle'), '  ',
               self._action(r'\u25b6\u25b6|', 'Next', '_incr'), r'\n', r'\nClock Speed:\n      ',
               self._action(r'<<', 'Slower Clock Speed', 'center/slower_clocks'), '   ',
               self._action(r'\u27f2', 'Reset Clock Speed', 'center/reset_clocks'), '   ',
               self._action(r'>>', 'Faster Clock Speed', 'center/faster_clocks'), r'\n', r'\nPlaces:\n   ',
               self._action('Home', 'Starting Point', 'global/goto_home'), r'\n   ',
               self._action('Photo Shoot', 'Scenic View', 'global/goto_photo'), r'\n   ',
               self._action('Battle Arena', 'Battle Arena', 'global/goto_arena'), r'\n   ',
               self._action('Biome Sampler', 'Biome Sampler', 'global/goto_biomes'), r'\n   ',
               self._action('Connected Textures', 'Connected Textures', 'global/goto_connected'), r'\n   ',
               self._action('Nether Home', 'Nether Starting Point', 'global/goto_nether'), r'\n   ',
               self._action('End Home', 'End Starting Point', 'global/goto_end_home'), r'\n   ',
               )

        cb.next_page()
        cb.add(r'Click on room name to go there: \n\n')
        rooms = filter(lambda x: isinstance(x, Room) and x.title is not None, self.function_set.children)
        rooms = sorted(rooms, key=lambda x: x.title)
        first = True
        for r in rooms:
            if first:
                first = False
            else:
                cb.add(', ')
            cb.add(self._action(r.title, r.title, r.name + '/_goto'))

        cb.next_page()
        cb.add(
            r'Credits:\n',
            JsonText.text(r'BlueMeanial:\n').bold(),
            r'  Command Blocks\n  Software Design\n  Programming\n',
            JsonText.text(r'JUMBOshrimp277:\n').bold(),
            r'  World Design\n  Testing\n  Rubber Duck\n\n',
            r'Minecraft Version:\n   1.19.1, ' + date.today().strftime('%-d %b %Y'),
            JsonText.text(r'\n\nTry the ').italic(),
            JsonText.text(r'Clarity Pack!').underlined().italic().color(DARK_PURPLE).click_event().open_url(
                'https://claritypack.com')
        )

        return Function('control_book').add(give(p(), cb.as_entity()))

    @staticmethod
    def _action(txt: str, tooltip: str, act: str) -> JsonText:
        return JsonText.text(txt).color(DARK_GREEN).underlined().click_event().run_command(
            function('restworld:' + act)).hover_event().show_text(tooltip)

    def _home_func_name(self, base):
        for f in self._suffixes:
            if base.endswith('_' + f):
                base = base[:-(len(f) + 1)]
                break
        return base + '_home'

    def world_funcs(self):
        for f in self._suffixes:
            fname = '_' + f
            func = Function(fname)
            for room in self.function_set.children:
                call = function(room.full_name + '/' + fname)
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
slow_clock = Clock('slow', 90)
main_clock = Clock('main', 60)
fast_clock = Clock('fast', 15)
tick_clock = Clock('clock')
restworld = Restworld()


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
