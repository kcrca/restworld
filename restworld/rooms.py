from __future__ import annotations

import copy
import re
from copy import deepcopy
from enum import Enum
from typing import Callable, Iterable, Tuple

from pynecraft.base import FacingDef, Nbt, ROTATION_180, ROTATION_270, ROTATION_90, UP, r, rotated_facing, to_name, \
    ORANGE, BLUE
from pynecraft.commands import Block, BlockDef, CLEAR, Command, Commands, Entity, EntityDef, JsonText, NEAREST, \
    Position, Score, SignMessages, a, comment, e, execute, function, good_block, good_entity, good_facing, good_score, \
    kill, p, schedule, scoreboard, setblock, summon, tag, tellraw, tp, weather
from pynecraft.enums import ScoreCriteria
from pynecraft.function import DataPack, Function, FunctionSet, LATEST_PACK_VERSION, Loop
from pynecraft.simpler import WallSign, TextDisplay


def named_frame_item(block: BlockDef = None, name=None, damage=None) -> Nbt:
    if not block and not name:
        return Nbt({'display': {}})
    block = good_block(block)
    tag_nbt = Nbt({'display': {'Name': str(JsonText.text(str(name if name else block.name))), }})
    if damage:
        tag_nbt.update(damage)
    nbt = Nbt({'Item': {'tag': tag_nbt}})
    if block:
        nbt = nbt.merge({'Item': {'id': block.id, 'Count': 1, }})
    return nbt


def ensure(pos: Position, block: BlockDef, nbt=None):
    block = good_block(block)
    to_place = block.clone()
    to_place.merge_nbt(nbt)
    return execute().unless().block(pos, block).run(setblock(pos, to_place))


def _to_iterable(tags):
    if tags is None:
        return tags
    if isinstance(tags, Iterable) and not isinstance(tags, str):
        return tags
    return tuple(tags)


def label(pos: Position, txt: str, facing=UP, invis=True, tags=(), block=Block('stone_button')) -> Commands:
    tags = list(tags)
    tags.append('label')
    return (
        execute().positioned(pos).run(
            kill(e().type('item_frame').tag('label').sort(NEAREST).distance((None, 1)).limit(1))),
        summon('item_frame', pos,
               named_frame_item(block, txt).merge(
                   {'Invisible': invis, 'Facing': good_facing(facing).number, 'Tags': tags, 'Fixed': True})),
    )


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

    def reset_at(self, xz: Tuple[int, int]) -> None:
        self._command_block(xz, 'Reset Room', ORANGE, f'restworld:{self.name}/_init')

    def change_height_at(self, xz: Tuple[int, int]) -> None:
        self._command_block(xz, 'Change Height', BLUE, 'restworld:global/toggle_raised')

    def _command_block(self, xz, label_text, color, command):
        func = self.functions[f'{self.name}_room_init']
        x = r(xz[0])
        z = r(xz[1])
        func.add(
            label((x, r(2), z), label_text),
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

    def _room_setup(self, facing, text, room_name):
        text = _to_list(text)
        self._record_room(text, room_name)
        text = tuple((JsonText.text(x).bold().italic() if x else x) for x in text)
        sign = WallSign(text)
        facing = good_facing(facing)
        x, z, rot = facing.dx, facing.dz, facing.yaw
        anchor = '%s_anchor' % self.name
        anchor_rot = rotated_facing(facing.name, ROTATION_180)
        marker = TextDisplay(None, {'Rotation': anchor_rot.rotation, 'shadow_radius': 0}).tag(anchor, 'anchor')
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

    def home_func(self, name):
        home_marker_comment = 'Default home function'
        marker_tag = '%s_home' % name
        if marker_tag in self.functions:
            f = self.functions[marker_tag]
            for c in f.commands():
                if home_marker_comment in c:
                    return
        marker = deepcopy(self._home_stand)
        marker.name = self.name
        marker.nbt.get_list('Tags').extend((marker_tag, self.name + '_home', 'homer'))
        return self.function(marker_tag, home=False, exists_ok=True).add(
            comment(home_marker_comment),
            kill(e().tag(marker_tag)),
            execute().positioned(r(-0.45, 0, -0.45)).run(kill(e().type('armor_stand').volume((0.3, 2, 0.3)))),
            marker.summon(r(0, 0.5, 0)),
        )

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

    def function(self, name: str, clock: Clock = None, /, home=True, exists_ok=False) -> Function:
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
            self.function(base_name + '_cur').add(loop.cur())
        self._scores.add(loop.score)
        self._scores.add(loop.to_incr)
        return loop

    def _add_func(self, func, name, clock, home):
        base_name, name = self._base_name(name, clock)
        if clock:
            self._clocks.setdefault(clock, []).append(func)
            clock.add(func)

        self.add(func)

        if home and base_name not in self._homes:
            self.home_func(base_name)
        return func

    def add(self, *functions: Function) -> FunctionSet:
        for f in functions:
            if f.name.endswith('_home'):
                self._homes.add(f.name[:-len('_home')])
        return super().add(*functions)

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
            'init': [scoreboard().objectives().add(self.name, ScoreCriteria.DUMMY),
                     scoreboard().objectives().add(self.name + '_max', ScoreCriteria.DUMMY),
                     (x.set(0) for x in sorted(self._scores, key=lambda x: str(x))),
                     to_incr.set(1)] + [tp(e().tag(self.name), e().tag('death').limit(1))]}
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
            facing = good_facing(facing)
            delta = delta if delta else 2
            kid_delta = kid_delta if kid_delta else 1.2
            try:
                if not isinstance(delta, (float, int)) or not isinstance(kid_delta, (float, int)):
                    raise ValueError('Deltas must be floats when using "facing" name')
                self.delta_x, _, self.delta_z = rotated_facing(facing, ROTATION_90).scale(delta)
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
               tags=None, nbt=None, auto_tag=None) -> Tuple[Command, ...]:
        if isinstance(mobs, (Entity, str)):
            mobs = (mobs,)
        if tags and isinstance(tags, str):
            tags = list(tags)
        for mob in mobs:
            mob = good_entity(mob)
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
        s = good_score(s)
        say.append(JsonText.text(str(s.target) + '='))
        say.append(JsonText.score(s))
    return tellraw(a(), *say)


class Wall:
    def __init__(self, width, facing, x, z, used):
        self.width = width
        self.facing = good_facing(facing)
        self.used = used
        self.x = x
        self.z = z

    def signs(self, desc_iter, get_sign):
        dx, _, dz = rotated_facing(self.facing, ROTATION_270).scale(1)
        for y in self.used.keys():
            for h in self.used[y]:
                sign = get_sign(next(desc_iter), self)
                x = self.x + h * dx
                z = self.z + h * dz
                yield sign.place(r(x, y, z), self.facing)


class ActionDesc:
    def __init__(self, enum: Enum, name=None, note=None, also=()):
        self.enum = enum
        if name is None:
            # noinspection PyUnresolvedReferences
            name = enum.display_name()
        self.name = name
        self.note = '(%s)' % note if note else None
        if isinstance(also, Iterable):
            self.also = also
        else:
            self.also = (also,)

    def __str__(self):
        return self.name + ' [' + self.enum + ']'

    def __lt__(self, other):
        assert self.__class__ == other.__class__
        assert self.enum.__class__ == other.enum.__class__
        return self.name < other.name

    def sign_text(self):
        block = Block(self.enum.value, name=self.name)
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
