from __future__ import annotations

import copy
import math
import re
from copy import deepcopy
from typing import Callable, Iterable, Tuple

from pynecraft.base import BLUE, EAST, FacingDef, NE, NORTH, NW, Nbt, ORANGE, ROTATION_180, ROTATION_270, ROTATION_90, \
    RelCoord, \
    SE, SOUTH, \
    SW, WEST, r, \
    rotate_facing, \
    to_name
from pynecraft.commands import Block, BlockDef, CLEAR, Command, Commands, Entity, EntityDef, INT, JsonText, MINUS, \
    Position, RESULT, Score, SignMessages, a, as_block, as_entity, as_facing, as_score, comment, data, e, \
    execute, function, kill, p, say, schedule, scoreboard, setblock, summon, tag, tellraw, tp, weather
from pynecraft.function import DataPack, Function, FunctionSet, LATEST_PACK_VERSION, Loop
from pynecraft.simpler import TextDisplay, WallSign
from pynecraft.values import DUMMY


def named_frame_item(block: BlockDef = None, name=None, damage=None) -> Nbt:
    if not block and not name:
        return Nbt({'custom_name': {}})
    block = as_block(block)
    tag_nbt = Nbt({'custom_name': str(JsonText.text(str(name if name else block.name)))})
    if damage:
        tag_nbt.update(damage)
    nbt = Nbt({'Item': {'components': tag_nbt}})
    if block:
        nbt = nbt.merge({'Item': {'id': block.id}})
    return nbt


def ensure(pos: Position, block: BlockDef, nbt=None):
    block = as_block(block)
    to_place = block.clone()
    to_place.merge_nbt(nbt)
    return execute().unless().block(pos, block).run(setblock(pos, to_place))


def _to_iterable(tags):
    if tags is None:
        return tags
    if isinstance(tags, Iterable) and not isinstance(tags, str):
        return tags
    return tuple(tags)


class Clock:
    def __init__(self, name: str, init_speed: int = None):
        self.name = name
        self.time = Score(name, 'clocks')
        self.speed = Score('SPEED_' + name.upper(), 'clocks')
        self.init_speed = init_speed
        self._funcs = []

    @classmethod
    def stop_all_clocks(cls) -> Command:
        return setblock((0, 1, 0), 'redstone_block')

    def add(self, function: Function):
        self._funcs.append(function)

    def tick_cmds(self, other_funcs=()):
        # execute at @e[tag=cage_home] run function restworld:enders/cage_main
        for f in self._funcs:
            yield execute().at(e().tag(self._tag(f))).run(function(f.name))
        yield '\n'
        for f in self._funcs:
            loop_finish = f.name[-len(self.name):] + 'finish'
            if loop_finish in other_funcs:
                yield execute().at(e().tag(self._tag(f))).run(schedule().function(loop_finish, 1))

    @staticmethod
    def _tag(f):
        return f.name.split(':')[-1]


def _to_list(obj):
    if not isinstance(obj, list):
        if isinstance(obj, str):
            return [obj]
        return list(obj)
    return obj


class RoomPack(DataPack):
    base_suffixes = ('tick', 'init', 'enter', 'incr', 'decr', 'cur', 'exit', 'finish')
    base_suffixes_re = re.compile(r'(\w+)_(' + '|'.join(base_suffixes) + ')')

    def __init__(self, name: str, suffixes: Iterable[str, ...] = None,
                 format_version: int = LATEST_PACK_VERSION, /):
        super().__init__(name, format_version)
        if suffixes is None:
            suffixes = RoomPack.base_suffixes
        self._suffixes = suffixes

    @property
    def suffixes(self):
        return self._suffixes


class Room(FunctionSet):
    def __init__(self, name: str, dp: RoomPack, facing: str = None, text: SignMessages = None, room_name: str = None):
        super().__init__(name, dp.function_set)
        self.pack = dp
        self._clocks = {}
        self._scores = set()
        self._homes = set()
        self._home_stand = Entity('armor_stand', {
            'Tags': ['homer', '%s_home' % self.name], 'NoGravity': True, 'Small': True})
        self.title = None
        self._player_in_room_setup()
        self.facing = facing
        if facing:
            self._room_setup(facing, text, room_name)

    def reset_at(self, xz: Tuple[int, int], facing=None, note=None) -> None:
        self.function('_init').add(function('restworld:global/reset_raised'))
        text = 'Reset Room'
        if note:
            text += fr'\n{note}'
        self._command_block(xz, text, ORANGE, f'restworld:{self.name}/_init', facing=facing)

    def change_height_at(self, xz: Tuple[int, int]) -> None:
        self._command_block(xz, 'Change Height', BLUE, 'restworld:global/toggle_raised')

    def _command_block(self, xz, label_text, color, command, facing=None):
        func = self.functions[f'{self.name}_room_init']
        x = r(xz[0])
        z = r(xz[1])
        if facing:
            facing = as_facing(facing)
        else:
            facing = rotate_facing(self.facing, 180)
        func.add(
            self.label((x, r(2), z), label_text, facing.name),
            setblock((x, r(2), z), ('stone_button', {'facing': self.facing, 'face': 'floor'})),
            setblock((x, r(1), z), f'{color}_concrete'),
            setblock((x, r(0), z), 'air'),
            setblock((x, r(0), z), Block('command_block', nbt={'Command': f'function {str(command)}'})),
        )

    def _player_in_room_setup(self):
        player_home = self.home_func(f'{self.name}_player')
        player_home.add(tag(e().tag(f'{self.name}_player_home')).add('no_expansion'))
        self.function('_enter', exists_ok=True).add(
            execute().positioned(r(1, -1, 1)).run(function(player_home.full_name)))
        self.function('_exit', exists_ok=True).add(kill(e().tag(f'{self.name}_player_home')))
        self.function(f'{self.name}_room_end')
        dx = self.score('dx')
        dz = self.score('dz')
        dx_beg = self.score('dx_beg')
        dz_beg = self.score('dz_beg')
        dx.set(0)
        self.store = f'{self.pack.name}:{self.name}'
        store = self.pos_store = f'{self.store}_pos'
        beg_tag = e().tag(f'{self.name}_room_beg_home').limit(1)
        end_tag = e().tag(f'{self.name}_room_end_home').limit(1)
        self.function(f'{self.name}_room_beg_init').add(
            execute().unless().entity(beg_tag).run(say(f'WARNING: no entity {self.name} beg')),
            dx.set(data().get(end_tag, 'Pos[0]')),
            dz.set(data().get(end_tag, 'Pos[2]')),
            execute().unless().entity(end_tag).run(say(f'WARNING: no entity {self.name} end')),
            dx_beg.set(data().get(beg_tag, 'Pos[0]')),
            dz_beg.set(data().get(beg_tag, 'Pos[2]')),
            dx.operation(MINUS, dx_beg),
            dz.operation(MINUS, dz_beg),
            execute().store(RESULT).storage(store, 'dx', INT).run(dx.get()),
            execute().store(RESULT).storage(store, 'dz', INT).run(dz.get()),
            data().modify(store, 'room').set().value(f'{self.name}'),
            execute().at(e().tag(f'{self.name}_room_beg_home')).run(
                function('restworld:global/room_bounds').with_().storage(store)),
        )

    def _room_setup(self, facing, text, room_name):
        text = _to_list(text)
        self._record_room(text, room_name)
        text = tuple((JsonText.text(x).bold().italic() if x else x) for x in text)
        sign = WallSign(text)
        facing = as_facing(facing)
        x, z, rot = facing.dx, facing.dz, facing.yaw
        anchor = '%s_anchor' % self.name
        anchor_rot = rotate_facing(facing.name, ROTATION_180)
        marker = Entity('marker', {'Rotation': anchor_rot.rotation, 'shadow_radius': 0}).tag(anchor, 'anchor')
        self.add(Function('%s_room_init' % self.name).add(
            sign.place(r(x, 6, z), facing),
            kill(e().tag(anchor)),
            summon(marker, r(0, 2, 0))
        ))
        self.function('_goto').add(
            tp(p(), e().tag(anchor).limit(1))
        )
        self.home_func(self.name + '_room')

    def _record_room(self, text, room_name):
        while len(text) > 0 and text[0] is None:
            text = text[1:]
        if not room_name:
            room_name = text[0]
            if text[0][-1] == '&':
                room_name += ' ' + text[1]
            room_name = room_name.replace(',', '').replace(':', '')
        self.title = room_name

    def home_func(self, name, home=None):
        home_marker_comment = 'Default home function'
        marker_tag = '%s_home' % name
        if marker_tag in self.functions:
            f = self.functions[marker_tag]
            for c in f.commands():
                if home_marker_comment in c:
                    return
        stand = deepcopy(self._home_stand)
        stand.name = self.name
        stand.nbt.get_list('Tags').extend((marker_tag, self.name + '_home', 'homer'))
        func = self.function(marker_tag, home=False, exists_ok=True).add(
            comment(home_marker_comment),
            kill(e().tag(marker_tag)),
            execute().positioned(r(-0.45, 0, -0.45)).run(kill(e().type('armor_stand').volume((0.3, 2, 0.3)))),
            stand.summon(r(0, 0.5, 0)),
        )
        if not isinstance(home, bool):
            func.add(execute().as_(e().tag(marker_tag)).run(home))
        return func

    def mob_placer(self, *args, **kwargs):
        tag_list = kwargs.setdefault('tags', [])
        if not isinstance(tag_list, list):
            if isinstance(tag_list, str):
                tag_list = [tag_list]
            else:
                tag_list = list(tag_list)
        tag_list.append(self.name)
        kwargs['tags'] = tag_list
        return MobPlacer(*args, **kwargs)

    def function(self, name: str, clock: Clock = None, /, home: bool | Command | Commands = True,
                 exists_ok=False) -> Function:
        """If home is more than a bool, it is commands to add to the home function."""
        base_name, name = self._base_name(name, clock)
        if exists_ok and name in self.functions:
            return self.functions[name]
        if home:
            if base_name[0] == '_' or base_name in self._homes or name.endswith('_home'):
                home = False
        return self._add_func(Function(name, base_name), name, clock, home)

    def loop(self, name: str, clock: Clock = None, /, home=True, score=None, exists_ok=False) -> Loop:
        base_name, name = self._base_name(name, clock)
        if exists_ok and name in self.functions:
            func = self.functions[name]
            if not isinstance(func, Loop):
                raise ValueError(f'{name}: Exists but is not a loop')
            return func
        if not score:
            score = Score(base_name, self.name)
        loop = self._add_func(Loop(score, name=name, base_name=base_name), name, clock, home)
        if not base_name + '_cur' in self.functions:
            self.function(base_name + '_cur', home=home).add(loop.cur())
        self._scores.add(loop.score)
        self._scores.add(loop.to_incr)
        return loop

    def _add_func(self, func, name, clock, home=None):
        base_name, name = self._base_name(name, clock)
        if clock:
            self._clocks.setdefault(clock, []).append(func)
            clock.add(func)

        self.add(func)

        if home and base_name not in self._homes:
            self.home_func(base_name, home)
        return func

    def add(self, function: Function) -> Function:
        if function.name.endswith('_home'):
            self._homes.add(function.name[:-len('_home')])
        return super().add(function)

    def _base_name(self, name, clock):
        if not clock:
            base_name = name
        else:
            if not name.endswith('_' + clock.name):
                base_name = name
                name += '_' + clock.name
            else:
                base_name = name[:-len(clock.name) - 1]
            return base_name, name
        if name[0] != '_':
            for s in self.pack.suffixes:
                tail = '_' + s
                if name.endswith(tail):
                    base_name = name[:-len(tail)]
                    break
        return base_name, name

    def finalize(self):
        self.add_room_funcs()

    def add_room_funcs(self):
        self._add_clock_funcs()
        self._add_loop_funcs()
        self._add_other_funcs()

    def _add_clock_funcs(self):
        tick_func = self.function('_tick')
        for clock, loops in self._clocks.items():
            name = '_%s' % clock.name
            clock_func = self.function(name).add((
                execute().at(e().tag(x.base_name + '_home')).run(function(x.full_name)) for x in loops))
            tick_func.add(execute().if_().score(clock.time).matches(0).run(function(clock_func.full_name)))
        tick_func.add(function(x.full_name) for x in filter(
            lambda x: self._is_func_type(x, '_tick'), self.functions.values()))

        finish_funcs = {}
        clock_re = str('(' + '|'.join(x.name for x in self._clocks.keys()) + ')')
        finish_funcs_re = re.compile('(.*)_finish_%s$' % clock_re)
        for f in self.functions.values():
            m = finish_funcs_re.match(f.name)
            if m:
                finish_funcs.setdefault('_finish_' + m.group(2), []).append(f)
        self.function('_finish').add((function(self._path(x)) for x in finish_funcs.keys()))
        for cf in finish_funcs.keys():
            self.function(cf).add((function(x.full_name) for x in finish_funcs[cf]))

    def _path(self, name):
        return self.full_name + '/' + name

    def _add_loop_funcs(self):
        incr_f = self.function('_incr')
        decr_f = self.function('_decr')
        for loop in self.functions.values():
            if isinstance(loop, Loop):
                home_f = loop.base_name + '_home'
                at_home = execute().at(e().tag(home_f))
                incr_f.add(at_home.run(loop.score.add(1)))
                decr_f.add(at_home.run(loop.score.remove(1)))
        cur_f = self.full_name + '/_cur'
        incr_f.add(function(cur_f))
        decr_f.add(function(cur_f))

    def _add_other_funcs(self):
        to_incr = self.score('_to_incr')
        before_commands = {
            'init': [kill(e().tag(self.name, 'label')),
                     scoreboard().objectives().add(self.name, DUMMY),
                     scoreboard().objectives().add(self.name + '_max', DUMMY),
                     (x.set(0) for x in sorted(self._scores, key=lambda x: str(x))),
                     to_incr.set(1)] + [tp(e().tag(self.name), e().tag('death').limit(1)), kill(e().tag(self.name))]
        }
        after_commands = {
            'enter': [weather(CLEAR)],
            'init': [function('%s/_cur' % self.full_name)],
        }
        clock_suffixes = set(x.name for x in self._clocks)
        clock_suffixes.add('tick')
        for f in self.pack.suffixes:
            if f in clock_suffixes:
                continue
            f_name = '_' + f
            relevant = filter(lambda x: self._is_func_type(x, f_name), self.functions.values())
            # Sorting means that we can force something to be first or last (rarely needed, but useful)
            relevant = list(relevant)
            relevant.sort(key=lambda f: f.name)
            commands = []
            commands.extend(before_commands.setdefault(f, []))
            commands.extend(
                (execute().at(e().tag(self._home_func_name(x.name))).run(function(x.full_name)) for x in
                 relevant))
            commands.extend(after_commands.setdefault(f, []))
            if len(commands) > 0:
                self.function(f_name, exists_ok=True).add(*commands)

    @staticmethod
    def _is_func_type(x, f_name):
        return x.name.endswith(f_name) and len(x.name) > len(f_name)

    def score(self, name):
        score = Score(name, self.name)
        self._scores.add(score)
        return score

    def score_max(self, name):
        score = Score(name, '%s_max' % self.name)
        return score

    def _home_func_name(self, base):
        # noinspection PyProtectedMember
        return self.pack._home_func_name(base)

    _ADJ = 0.45
    _DIAG_ADJ = _ADJ * math.sin(45)

    _transform = {
        False: {
            SOUTH: ((0, 1, 0), 1, {'right_rotation': [0.7, 0.0, 0.0, -0.7], 'left_rotation': [0.0, 1.0, 0.0, 0.0],
                                   'translation': [0.0, 0.0, -_ADJ]}),
            NORTH: ((0, 1, 0), 1, {'right_rotation': [0.7, 0.0, 0.0, -0.7], 'left_rotation': [0.0, 0.0, 0.0, 1.0],
                                   'translation': [0.0, 0.0, _ADJ]}),
            EAST: ((0, 1, 0), 1, {'right_rotation': [0.7, 0.0, 0.0, -0.7], 'left_rotation': [0.0, 0.7, 0.0, -0.7],
                                  'translation': [-_ADJ, 0.0, 0.0]}),
            WEST: ((0, 1, 0), 1, {'right_rotation': [0.7, 0.0, 0.0, -0.7], 'left_rotation': [0.0, 0.7, 0.0, 0.7],
                                  'translation': [_ADJ, 0.0, 0.0]}),
            NW: ((0, 1, 0), 1, {'right_rotation': [0.7, 0.0, 0.0, -0.7], 'left_rotation': [0.0, 0.39, 0.0, 1.0],
                                'translation': [_DIAG_ADJ, 0.0, _DIAG_ADJ]}),
            NE: ((0, 1, 0), 1, {'right_rotation': [0.7, 0.0, 0.0, -0.7], 'left_rotation': [0.0, -0.39, 0.0, 1.0],
                                'translation': [-_DIAG_ADJ, 0.0, _DIAG_ADJ]}),
            SE: ((0, 1, 0), 1, {'right_rotation': [0.7, 0.0, 0.0, -0.7], 'left_rotation': [0.0, 0.9, 0.0, -0.4],
                                'translation': [-_DIAG_ADJ, 0.0, -_DIAG_ADJ]}),
            SW: ((0, 1, 0), 1, {'right_rotation': [0.7, 0.0, 0.0, -0.7], 'left_rotation': [0.0, - 0.9, 0.0, -0.4],
                                'translation': [_DIAG_ADJ, 0.0, -_DIAG_ADJ]}),
        },
        True: {
            NORTH: ((0, 0, 1), 1, {'right_rotation': [0.0, 0.0, 0.0, 1.0], 'left_rotation': [0.0, 0.0, 0.0, 1.0],
                                   'translation': [0.0, 0.0, 0.0]}),
            SOUTH: ((0, 0, 0), -1, {'right_rotation': [0.0, 1.0, 0.0, 0.0], 'left_rotation': [0.0, 0.0, 0.0, 1.0],
                                    'translation': [0.0, 0.0, 0.0]}),
            WEST: ((-_ADJ, 0, 0), 1, {'right_rotation': [0.0, 0.7, 0.0, 0.7], 'left_rotation': [0.0, 0.0, 0.0, 1.0],
                                      'translation': [0.0, 0.0, 0.0]}),
            EAST: ((_ADJ, 0, 0), -1, {'right_rotation': [0.0, 0.7, 0.0, -0.7], 'left_rotation': [0.0, 0.0, 0.0, 1.0],
                                      'translation': [0.0, 0.0, 0.0]}),
        },
    }

    def label(self, pos: Position, txt: str, looking=EAST, *, vertical=False, bump=0.02, tags=()) -> str:
        if isinstance(tags, str):
            tags = (tags,)
        t = ['label', self.name]
        t.extend(tags)
        offset_tmpl, bump_sign, xform = self._transform[vertical][looking]
        offset = []
        for v in offset_tmpl:
            if v == 0:
                offset.append(0)
            else:
                if vertical:
                    offset.append(0 if v == 0 else v + bump * bump_sign)
                else:
                    offset.append(bump)
        pos = RelCoord.add(pos, offset)
        scale = 0.45
        return TextDisplay(txt, nbt={'Tags': t, 'line_width': int(200 * scale), 'transformation': xform,
                                     'background': 0}).scale(scale).summon(pos)


def _name_for(mob):
    if mob.name:
        return mob.name
    return to_name(mob.id)


class MobPlacer:
    _armor_stand_tmpl = Entity('armor_stand').merge_nbt({'Invisible': True, 'Small': True, 'NoGravity': True})

    base_nbt = {'NoAI': True, 'PersistenceRequired': True, 'Silent': True}

    def __init__(self, start: Position, facing: FacingDef | float,
                 delta: float | tuple[float, float] = None, kid_delta: float | tuple[float, float] = None, *,
                 tags: str | Tuple[str, ...] = None,
                 nbt=None, kids=None, adults=None, auto_tag=True):
        self.start = start
        self.nbt = nbt if nbt else Nbt()
        self.tags = _to_iterable(tags)
        if (kids, adults) == (None, None):
            kids, adults = True, True
        elif kids is None:
            kids = False
        elif adults is None:
            adults = False
        self.kids = kids
        self.adults = adults
        self.auto_tag = auto_tag
        if not isinstance(facing, (float, int)):
            facing = as_facing(facing)
            delta = delta if delta else 2
            kid_delta = kid_delta if kid_delta else 1.2
            try:
                if not isinstance(delta, (float, int)) or not isinstance(kid_delta, (float, int)):
                    raise ValueError('Deltas must be floats when using "facing" name')
                self.delta_x, _, self.delta_z = rotate_facing(facing, ROTATION_90).scale(delta)
                self.kid_x, _, self.kid_z = facing.scale(kid_delta)
                self.rotation = facing.yaw
            except KeyError:
                raise ValueError('%s: Unknown "facing" with no "rotation"' % facing.name)
        else:
            delta = delta if delta else (0, 0)
            kid_delta = kid_delta if kid_delta else (0, 0)
            self.rotation = facing
            self.delta_x, self.delta_z = delta
            self.kid_x, self.kid_z = kid_delta
        self._cur = list(self.start)

    def clone(self) -> MobPlacer:
        return copy.deepcopy(self)

    def summon(self, mobs: Iterable[EntityDef] | EntityDef, *, on_stand: bool | Callable[[Entity], bool] = False,
               tags: str | tuple[str] | list[str] = None, nbt=None, auto_tag=None) -> Tuple[Command, ...]:
        if isinstance(mobs, (Entity, str)):
            mobs = (mobs,)
        if tags and isinstance(tags, str):
            tags = list(tags)
        for mob in mobs:
            mob = as_entity(mob)
            tmpl = mob.clone()
            if self.nbt:
                tmpl.merge_nbt(self.nbt)
            if nbt:
                tmpl.merge_nbt(nbt)
            tmpl.merge_nbt(MobPlacer.base_nbt)
            tmpl.custom_name(True)
            tmpl.merge_nbt({'Rotation': [self.rotation, 0]})
            tmpl.name = _name_for(mob)
            if self.tags:
                tmpl.tag(*self.tags)
            if tags:
                tmpl.tag(*tags)
            if auto_tag is None:
                auto_tag = self.auto_tag
            if auto_tag:
                tmpl.tag(tmpl.id)

            if self.adults:
                adult = tmpl.clone()
                adult.tag('adult')
                yield self._do_summoning(adult, on_stand, self._cur)
            if self.kids:
                kid = tmpl.clone()
                kid.tag('kid')
                kid.merge_nbt({'IsBaby': True, 'Age': -2147483648})
                pos = self._cur
                if self.adults:
                    pos = pos[0] + self.kid_x, pos[1], pos[2] + self.kid_z
                yield self._do_summoning(kid, on_stand, pos)

            self._cur[0] += self.delta_x
            self._cur[2] += self.delta_z

    @staticmethod
    def _do_summoning(tmpl, on_stand, pos):
        if on_stand:
            stand = MobPlacer._armor_stand_tmpl.clone()
            stand.tag(*tmpl.nbt.get('Tags'))
            tmpl.merge_nbt({'id': tmpl.full_id()})
            stand.nbt.get_list('Passengers').append(tmpl.nbt)
            tmpl = stand
        return tmpl.summon(pos)

    @classmethod
    def adult(cls, which: EntityDef, pos, facing: str | float, **kwargs):
        if isinstance(facing, (float, int)):
            delta = kid_delta = (0, 0)
        else:
            delta = kid_delta = 0
        return MobPlacer(pos, facing, delta, kid_delta, adults=True, **kwargs).summon([which])


def say_score(*scores):
    say = [JsonText.text('scores:')]
    for s in scores:
        s = as_score(s)
        say.append(JsonText.text(str(s.target) + '='))
        say.append(JsonText.score(s))
    return tellraw(a(), *say)


class Wall:
    def __init__(self, width, facing, x, z, used):
        self.width = width
        self.facing = as_facing(facing)
        self.used = used
        self.x = x
        self.z = z

    def signs(self, desc_iter, get_sign):
        dx, _, dz = rotate_facing(self.facing, ROTATION_270).scale(1)
        for y in self.used.keys():
            for h in self.used[y]:
                sign = get_sign(next(desc_iter), self)
                x = self.x + h * dx
                z = self.z + h * dz
                yield sign.place(r(x, y, z), self.facing)


class ActionDesc:
    def __init__(self, which: str, name=None, note=None, also=()):
        self.enum = None
        self.which = which
        self.name = to_name(which)
        if name is not None:
            self.name = name
        self.note = '(%s)' % note if note else None
        if isinstance(also, Iterable):
            self.also = also
        else:
            self.also = (also,)

    def __str__(self):
        return self.name

    def __lt__(self, other):
        assert self.__class__ == other.__class__
        return self.name < other.name

    def sort_key(self):
        return self.name

    def func(self):
        return self.which

    def sign_text(self):
        block = Block(self.which, name=self.name)
        sign_text = list(block.sign_text)
        if self.note:
            sign_text.append(self.note)
        if len(sign_text) < 4:
            sign_text.insert(0, None)
        while len(sign_text) > 4:
            if sign_text[0]:
                raise ValueError('%s: Too much sign text for action' % sign_text)
            sign_text = sign_text[1:]
        return sign_text


class SignedRoom(Room):
    def __init__(self, name: str, dp: RoomPack, facing, sign_txt, get_sign, signs: Iterable[ActionDesc],
                 walls: Iterable[Wall]):
        super().__init__(name, dp, facing, sign_txt)
        self.get_sign = get_sign
        self.walls = walls
        self.function('signs').add(self.init(signs))

    def init(self, descriptions):
        i = iter(descriptions)
        try:
            for w in self.walls:
                yield from w.signs(i, self.get_sign)
        except StopIteration:
            return None
        try:
            desc = next(i)
            raise ValueError('%s...: Remaining descriptions after all signs are placed' % desc.name)
        except StopIteration:
            return


def span(start, end):
    return range(start, end + 1)
