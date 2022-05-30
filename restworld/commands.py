from __future__ import annotations

import re
import textwrap
import typing
from abc import abstractmethod
from functools import wraps
from inspect import signature, getmembers, ismethod
from io import StringIO

from .enums import Advancement, Effects, Enchantments, GameRules


def fluent(method):
    @wraps(method)
    def inner(self, *args, **kwargs):
        obj = self.__class__.__new__(self.__class__)
        obj.__dict__ = self.__dict__.copy()
        method(obj, *args, **kwargs)
        return obj

    return inner


def _in_group(group: str, *names: str):
    group_list = globals()[group.upper()]
    missing = []
    for n in names:
        if n not in group_list:
            missing.append(n)
    if missing:
        raise ValueError('%s: Not in %s %s' % (missing, group, group_list))


_resource_re = re.compile(r'[\w.]+')
_name_re = re.compile(r'[\w+.-]+')
_user_re = re.compile(r'\w+')
_uuid_re = re.compile(r'(?:[a-fA-F0-9]+-){3}[a-fA-F0-9]+')


def _strip_namespace(path):
    parts = path.split(':', 1)
    if len(parts) > 1:
        good_resource(parts[0])
        path = parts[1]
    return path


def _strip_not(path):
    if path and path[0] == '!':
        return path[1:]
    return path


def good_resource(name: str, allow_namespace=True, allow_not=False) -> str:
    input = name
    if allow_not:
        name = _strip_not(name)
    if allow_namespace:
        name = _strip_namespace(name)
    if not _resource_re.match(name):
        raise ValueError('Invalid resource location: %s' % name)
    return input


def good_resources(*names: str, allow_not=False) -> tuple[str, ...]:
    for t in names:
        good_resource(t, allow_not=allow_not)
    return names


def good_resource_path(path: str, allow_not=False) -> str:
    input = path
    if allow_not:
        path = _strip_not(path)
    path = _strip_namespace(path)
    if path and path[0] == '/':
        # allow leading '/'
        path = path[1:]
    for r in path.split('/'):
        try:
            good_resource(r, allow_namespace=False)
        except ValueError:
            raise ValueError('Invalid resource location in path: %s (%s)' % (r, path))
    return input


def good_resource_paths(*paths: str, allow_not=False) -> tuple[str, ...]:
    for t in paths:
        good_resources(t, allow_not=allow_not)
    return paths


def good_name(name: str, allow_not=False) -> str:
    input = name
    if allow_not:
        name = _strip_not(name)
    if not _name_re.match(name):
        raise ValueError('Invalid name: %s' % name)
    return input


def good_names(*names: str, allow_not=False) -> tuple[str, ...]:
    for t in names:
        good_name(t, allow_not)
    return names


def good_user(name: str) -> str:
    if not _user_re.match(name):
        raise ValueError('Invalid user name: %s' % name)
    return name


def good_uuid(uuid: str) -> str:
    if not _uuid_re.match(uuid):
        raise ValueError('Invalid UUID string: %s' % uuid)
    return uuid


NEAREST = 'nearest'
FURTHEST = 'furthest'
RANDOM = 'random'
ARBITRARY = 'arbitrary'
SORT = [NEAREST, FURTHEST, RANDOM, ARBITRARY]

SURVIVAL = 'survival'
CREATIVE = 'creative'
ADVENTURE = 'adventure'
SPECTATOR = 'spectator'
GAMEMODE = [SURVIVAL, CREATIVE, ADVENTURE, SPECTATOR]

X = 'x'
XZ = 'xz'
ZYX = 'zyx'
YZ = 'yz'
AXES = [X, XZ, ZYX, YZ]

EYES = 'eyes'
FEET = 'feet'
ENTITY_ANCHOR = [EYES, FEET]

OVERWORLD = 'overworld'
THE_NETHER = 'the_nether'
THE_END = 'the_end'
DIMENSION = [OVERWORLD, THE_NETHER, THE_END]

ALL = 'all'
MASKED = 'masked'
SCAN_MODE = [ALL, MASKED]

FORCE = 'force'
MOVE = 'move'
NORMAL = 'normal'
CLONE_FLAGS = [FORCE, MOVE, NORMAL]

RESULT = 'result'
SUCCESS = 'success'
STORE = [RESULT, SUCCESS]

BYTE = 'byte'
SHORT = 'short'
INT = 'int'
LONG = 'long'
FLOAT = 'float'
DOUBLE = 'double'
DATA_TYPE = [BYTE, SHORT, INT, LONG, FLOAT, DOUBLE]

VALUE = 'value'
MAX = 'max'
BOSSBAR = [VALUE, MAX]

EVERYTHING = 'everything'
ONLY = 'only'
FROM = 'from'
THROUGH = 'through'
UNTIL = 'until'
ADVANCEMENT = [EVERYTHING, ONLY, FROM, THROUGH, UNTIL]

MAX = "max"
PLAYERS = 'players'
VALUE = 'value'
VISIBLE = 'visible'
BOSSBAR_GET = [MAX, PLAYERS, VALUE, VISIBLE]

BLUE = 'blue'
GREEN = 'green'
PINK = 'pink'
PURPLE = 'purple'
RED = 'red'
WHITE = 'white'
YELLOW = 'yellow'
BOSSBAR_COLORS = [BLUE, GREEN, PINK, PURPLE, RED, WHITE, YELLOW]

NOTCHED_6 = 'notched_6'
NOTCHED_10 = 'notched_10'
NOTCHED_12 = 'notched_12'
NOTCHED_20 = 'notched_20'
PROGRESS = 'progress'
BOSSBAR_STYLES = [NOTCHED_6, NOTCHED_10, NOTCHED_12, NOTCHED_20, PROGRESS]

ENABLE = 'enable'
DISABLE = 'disable'
DATAPACK_ACTIONS = [ENABLE, DISABLE]

FIRST = 'first'
LAST = 'last'
BEFORE = 'before'
AFTER = 'after'
ORDER = [FIRST, LAST, BEFORE, AFTER]

AVAILABLE = 'available'
ENABLED = 'enabled'
DATAPACK_FILTERS = [AVAILABLE, ENABLED]

EASY = 'easy'
HARD = 'hard'
NORMAL = 'normal'
PEACEFUL = 'peaceful'
DIFFICULTIES = [EASY, HARD, NORMAL, PEACEFUL]

LEVELS = 'levels'
POINTS = 'points'
EXPERIENCE_POINTS = [LEVELS, POINTS]

DESTROY = 'destroy'
HOLLOW = 'hollow'
KEEP = 'keep'
OUTLINE = 'outline'
REPLACE = 'replace'
FILL_ACTIONS = [DESTROY, HOLLOW, KEEP, OUTLINE, REPLACE]

GIVE = 'give'
CLEAR = 'clear'
GIVE_CLEAR = [GIVE, CLEAR]

GRANT = 'grant'
REVOKE = 'revoke'
GRANT_REVOKE = [GRANT, REVOKE]

GIVE_GRANT = GIVE_CLEAR + GRANT_REVOKE

MAX_EFFECT_SECONDS = 1000000


def _to_grant(action: str):
    if action == 'give':
        action = GRANT
    elif action == 'clear':
        action = REVOKE
    _in_group('GRANT_REVOKE', action)
    return action


LT = '<'
LE = '<='
EQ = '='
GE = '>='
GT = '>'
RELATION = [LT, LE, EQ, GE, GT]

ALL_SCORES = '*'


def _bool(value: bool | None) -> str | None:
    if value is None:
        return None
    return str(value).lower()


def not_ify(value) -> str:
    s = str(value)
    if s[0] != '!':
        s = '!' + s
    return s


class Chain:
    def __init__(self):
        self._rep = None

    def _add(self, *objs: any):
        s = ' '.join(str(x) for x in objs)
        if not self._rep:
            self._rep = ''
        self._rep += s

    def _add_if(self, s: str):
        if self._rep:
            self._rep += s

    def _add_opt(self, *objs: any):
        for o in objs:
            if o is not None:
                self._add('', o)

    def _start(self, start: T) -> T:
        start._rep = self._rep + ' '
        return start

    def __str__(self):
        return self._rep.strip()


T = typing.TypeVar("T", bound=Chain)


class Coord:
    def __init__(self, prefix: str, v: float):
        self._rep = prefix + str(v)

    @abstractmethod
    def __str__(self):
        return str(self._rep)


def r(v: float):
    return Coord('~', v)


def d(v: float):
    return Coord('^', v)


class Range(Chain):
    def __init__(self, start: float = None, end: float = None, at: float = None):
        super().__init__()
        if not start and not end and not at:
            raise ValueError("Must specify end, end or at")
        if at:
            self._add(str(at))
        else:
            b = str(start) if start else ''
            e = str(end) if end else ''
            self._add(b + '..' + e)


class ScoreRange:
    def __init__(self, score: str, range: Range, inverse=False):
        self.score = score
        self.range = range
        self.inverse = inverse


class Score(Chain):
    def __init__(self, target: Target | str, objective: str):
        super().__init__()
        if isinstance(target, str) and target != '*':
            raise ValueError('Target must be target or "*": %s' % target)
        self._add(target, good_name(objective))


class ScoreClause(Chain):
    def is_(self, relation: str, target: Target | str, objective: str) -> ExecuteMod:
        _in_group('RELATION', relation)
        self._add(relation, Score(target, objective))
        return self._start(ExecuteMod())

    def matches(self, range: Range) -> ExecuteMod:
        self._add('matches', range)
        return self._start(ExecuteMod())


class AdvancementCriteria(Chain):
    def __init__(self, advancement: Advancement, criteria: bool | tuple[str, bool]):
        super().__init__()
        if isinstance(criteria, bool):
            self._add('%s=%s' % (advancement, _bool(criteria)))
        else:
            self._add('%s={%s=%s}' % (advancement, good_resource_path(criteria[0]), _bool(criteria[1])))


# For future: https://github.com/vberlier/nbtlib/blob/main/docs/Usage.ipynb seems like a good
# NBT library, more focused on files, but that's OK, it seems to manage the NBT itself pretty
# well. Possibly a good base for the NBT work.
class _NbtFormat(Chain):
    _needs_quotes = re.compile(r'[\s:"]')

    def __init__(self, nbt: dict):
        super().__init__()
        self.sio = StringIO()
        self._dict(nbt)
        self._add(self.sio.getvalue())

    def _quote(self, s: str):
        s = s.replace('"', r'\"')
        quote = self._needs_quotes.search(s)
        if quote:
            self.sio.write('"')
        self.sio.write(s)
        if quote:
            self.sio.write('"')

    def _elem(self, elem):
        if isinstance(elem, str):
            self._quote(elem)
        elif isinstance(elem, bool):
            self._quote(str(elem).lower())
        elif isinstance(elem, dict):
            self._dict(elem)
        else:
            try:
                iter(elem)
                self._array(elem)
            except TypeError:
                self._quote(str(elem))

    def _dict(self, d: dict):
        self.sio.write('{')
        for k, v in d.items():
            self._quote(k)
            self.sio.write(':')
            self._elem(v)
        self.sio.write('}')

    def _array(self, array):
        self.sio.write('[')
        for i in range(0, len(array)):
            if i > 0:
                self.sio.write(',')
            self._elem(array[i])
        self.sio.write(']')


class Target(Chain):
    pass


class User(Target):
    def __init__(self, name: str):
        super().__init__()
        good_user(name)
        self._add(name)


class Uuid(Target):
    def __init__(self, u1: int, u2: int, u3: int, u4: int):
        super().__init__()
        self._add([u1, u2, u3, u4])


# noinspection PyProtectedMember
def player():
    return Selector(Selector._create_key, '@p')


# noinspection PyProtectedMember
def random():
    return Selector(Selector._create_key, '@r')


# noinspection PyProtectedMember
def all():
    return Selector(Selector._create_key, '@a')


# noinspection PyProtectedMember
def entities():
    return Selector(Selector._create_key, '@e')


# noinspection PyProtectedMember
def self():
    return Selector(Selector._create_key, '@s')


class Selector(Target):
    _create_key = object()

    def __init__(self, create_key, selector):
        super().__init__()
        assert (create_key == Selector._create_key), "Private __init__, use creation methods"
        self._selector = selector
        self._args = {}

    def __str__(self):
        if len(self._args) == 0:
            return self._selector
        return self._selector + '[' + super().__str__() + ']'

    def _add_arg(self, key: str, value: any):
        v = str(value)
        if v.find('=') < 0 or v[0] == '{':
            v = '%s=%s' % (key, v)
        if key in self._args:
            self._args[key] += ',' + v
        else:
            self._args[key] = v
        self._add_if(',')
        self._add(v)

    def _unique_arg(self, key: str, value: any):
        if key in self._args:
            raise KeyError("Already set in target: %s" % key)
        self._add_arg(key, value)
        return self

    def _multi_args(self, key: str, value: any, values: tuple[any, ...]):
        self._add_arg(key, value)
        for v in values:
            self._add_arg(key, v)
        return self

    def _not_args(self, key: str, value, values):
        self._add_arg(key, not_ify(value))
        for v in values:
            self._add_arg(key, not_ify(v))
        result = self._args[key]
        value_count = result.count('=')
        neg_count = result.count('!')
        if value_count > 1 and neg_count != value_count:
            raise KeyError("Cannot repeat %s unless all are negated: %s" % (key, result))
        return self

    @fluent
    def pos(self, x, y, z):
        self._unique_arg('pos', 'x=%s,y=%s,z=%s' % (str(x), str(y), str(z)))

    @fluent
    def distance(self, distance: Range):
        return self._unique_arg('distance', distance)

    @fluent
    def delta(self, dx, dy, dz):
        return self._unique_arg('delta', 'dx=%s,dy=%s,dz=%s' % (str(dx), str(dy), str(dz)))

    @fluent
    def scores(self, *scores):
        return self._unique_arg('scores', '{' + ','.join(scores) + '}')

    @fluent
    def tag(self, tag: str, *tags: str):
        return self._multi_args('tag', good_name(tag, allow_not=True), good_names(*tags, allow_not=True))

    @fluent
    def not_tag(self, tag: str, *tags: str):
        return self.tag(not_ify(good_name(tag, allow_not=True)), not_ify(good_names(*tags, allow_not=True)))

    @fluent
    def team(self, team: str):
        return self._unique_arg('team', good_name(team, allow_not=True))

    @fluent
    def not_team(self, team: str, *teams):
        return self._not_args('team', good_name(team, allow_not=True), good_names(*teams, allow_not=True))

    @fluent
    def sort(self, sorting: str):
        _in_group('SORT', sorting)
        return self._unique_arg('sort', sorting)

    @fluent
    def limit(self, limit: int):
        return self._unique_arg('limit', str(limit))

    @fluent
    def level(self, level_range: Range):
        return self._unique_arg('level', level_range)

    @fluent
    def gamemode(self, gamemode: str):
        _in_group('GAMEMODE', gamemode)
        return self._unique_arg('gamemode', gamemode)

    @fluent
    def not_gamemode(self, gamemode: str, *gamemodes: str):
        _in_group('GAMEMODE', gamemode, *gamemodes)
        return self._not_args('gamemode', gamemode, gamemodes)

    @fluent
    def name(self, name: str):
        return self._unique_arg('name', good_name(name, allow_not=True))

    @fluent
    def not_name(self, name: str, *names: str):
        return self._not_args('name', good_name(name, allow_not=True), good_names(*names, allow_not=True))

    @fluent
    def x_rotation(self, rot_range: Range):
        self._unique_arg('x_rotation', rot_range)
        return self

    @fluent
    def y_rotation(self, rot_range: Range):
        self._unique_arg('y_rotation', rot_range)
        return self

    @fluent
    def type(self, type_: str):
        return self._unique_arg('type', good_resource(type_, allow_not=True))

    @fluent
    def not_types(self, type_: str, *types: str):
        return self._not_args('type', good_resource(type_, allow_not=True), good_resources(*types, allow_not=True))

    @fluent
    def nbt(self, nbt: dict, *nbts: dict):
        return self._multi_args('nbt', _NbtFormat(nbt), tuple(_NbtFormat(x) for x in nbts))

    @fluent
    def advancements(self, advancement: AdvancementCriteria, *advancements: AdvancementCriteria):
        adv = [advancement, ]
        for a in advancements:
            adv.append(a)
        return self._unique_arg('advancements', '{' + ','.join(str(x) for x in adv) + '}')

    @fluent
    def predicate(self, predicate: str, *predicates: str):
        return self._multi_args('predicate', predicate, predicates)


def _grant(action: str):
    return 'grant' if action == GRANT else 'revoke'


class IfClause(Chain):
    def block(self, x: float | Coord, y: float | Coord, z: float | Coord, block_name: str) -> ExecuteMod:
        self._add('block', x, y, z, good_resource(block_name))
        return self._start(ExecuteMod())

    def blocks(self,
               start_x: float | Coord, start_y: float | Coord, start_z: float | Coord,
               end_x: float | Coord, end_y: float | Coord, end_z: float | Coord,
               dest_x: float | Coord, dest_y: float | Coord, dest_z: float | Coord,
               mode: str
               ) -> ExecuteMod:
        _in_group('SCAN_MODE', mode)
        self._add('blocks', start_x, start_y, start_z, end_x, end_y, end_z,
                  dest_x, dest_y, dest_z, mode)
        return self._start(ExecuteMod())

    def data_block(self, x: float | Coord, y: float | Coord, z: float | Coord, nbt_path: str) -> ExecuteMod:
        self._add('data', 'block', x, y, z, nbt_path)
        return self._start(ExecuteMod())

    def data_entity(self, target: Target, nbt_path: str) -> ExecuteMod:
        self._add('data', 'entity', target, nbt_path)
        return self._start(ExecuteMod())

    def data_storage(self, source: str, nbt_path: str) -> ExecuteMod:
        self._add('data', 'storage', source, nbt_path)
        return self._start(ExecuteMod())

    def predicate(self, predicate: str) -> ExecuteMod:
        self._add('predicate', predicate)
        return self._start(ExecuteMod())

    def score(self, target: Target | str, objective: str) -> ScoreClause:
        self._add('score', Score(target, objective))
        return self._start(ScoreClause())


class StoreClause(Chain):
    def block(self, x: float | Coord, y: float | Coord, z: float | Coord, nbt_patbh: str, data_type: str,
              scale: float) -> ExecuteMod:
        _in_group('DATA_TYPE', data_type)
        self._add('block', x, y, z, nbt_patbh, data_type, scale)
        return self._start(ExecuteMod())

    def bossbar(self, id: str, param: str) -> ExecuteMod:
        _in_group('BOSSBAR', param)
        self._add('bossbar', id, param)
        return self._start(ExecuteMod())

    def entity(self, target: Target, nbt_path: str, data_type: str, scale: float) -> ExecuteMod:
        _in_group('DATA_TYPE', data_type)
        self._add('entity', target, nbt_path, data_type, scale)
        return self._start(ExecuteMod())

    def score(self, target: Target | str, objective: str) -> ExecuteMod:
        self._add('score', Score(target, objective))
        return self._start(ExecuteMod())

    def storage(self, target: Target, nbt_path: str, data_type: str, scale: float) -> ExecuteMod:
        _in_group('DATA_TYPE', data_type)
        self._add('storage', target, nbt_path, data_type, scale)
        return self._start(ExecuteMod())


class ExecuteMod(Chain):
    @fluent
    def align(self, axes: str):
        _in_group('AXES', axes)
        self._add('align', axes)

    @fluent
    def anchored(self, anchor: str):
        _in_group('ENTITY_ANCHOR', anchor)
        self._add('anchored', anchor)

    @fluent
    def as_(self, target: Target):
        self._add('as', target)

    @fluent
    def at(self, target: Target):
        self._add('at', target)

    @fluent
    def facing(self, x: float | Coord, y: float | Coord, z: float | Coord):
        self._add('facing', x, y, z)

    @fluent
    def facing_entity(self, target: Target, anchor: str):
        _in_group('ENTITY_ANCHOR', anchor)
        self._add('facing entity', target, anchor)

    @fluent
    def in_(self, dimension: str):
        _in_group('DIMENSION', dimension)
        self._add('in', dimension)

    @fluent
    def positioned(self, x: float | Coord, y: float | Coord, z: float | Coord):
        self._add('positioned', x, y, z)

    @fluent
    def positioned_as(self, target: Target):
        self._add('positioned as', target)

    @fluent
    def rotated(self, yaw: float, pitch: float):
        self._add('rotated', yaw, pitch)

    @fluent
    def rotated_as(self, target: Target):
        self._add('rotated as', target)

    def if_(self) -> IfClause:
        self._add('if')
        return self._start(IfClause())

    def unless(self) -> IfClause:
        self._add('unless')
        return self._start(IfClause())

    def store(self) -> StoreClause:
        self._add('store')
        return self._start(StoreClause())

    def run(self) -> Command:
        self._add('run')
        return self._start(Command())


class AttributeBaseAct(Chain):
    def get(self, scale: float = None) -> str:
        self._add('get')
        if scale:
            self._add('', scale)
        return str(self)

    def set(self, value: float) -> str:
        self._add('set', value)
        return str(self)


class AttributeModifierAct(Chain):
    def add(self, uuid: str, name: str, value: float) -> str:
        self._add('add', good_uuid(uuid), '"%s"' % name, value)
        return str(self)

    def remove(self, uuid: str) -> str:
        self._add('remove', good_uuid(uuid))
        return str(self)

    def value(self, uuid: str, scale: float = None) -> str:
        self._add('value get', good_uuid(uuid))
        if scale:
            self._add('', scale)
        return str(self)


class AttributeAct(Chain):
    def get(self, scale: float = None) -> str:
        self._add('get')
        if scale:
            self._add('', scale)
        return str(self)

    def base(self) -> AttributeBaseAct:
        self._add('base')
        return self._start(AttributeBaseAct())

    def modifier(self) -> AttributeModifierAct:
        self._add('modifier')
        return self._start(AttributeModifierAct())


class BossbarSet(Chain):
    def color(self, color: str) -> str:
        _in_group('BOSSBAR_COLORS', color)
        self._add('color', color)
        return str(self)

    def max(self, value: int) -> str:
        self._add('max', value)
        return str(self)

    def name(self, name: str) -> str:
        self._add('name', name)
        return str(self)

    def players(self, *targets: Target) -> str:
        self._add('players', *targets)
        return str(self)

    def style(self, style: str) -> str:
        _in_group('BOSSBAR_STYLES', style)
        self._add('style', style)
        return str(self)

    def value(self, value: int) -> str:
        self._add('value', value)
        return str(self)

    def visible(self, visible: bool) -> str:
        self._add('visible', _bool(visible))
        return str(self)


class BossbarAct(Chain):
    def add(self, id: str, name: str) -> str:
        self._add('add', good_resource(id), name)
        return str(self)

    def get(self, id: str, which: str) -> str:
        _in_group('BOSSBAR_GET', which)
        self._add('get', good_resource(id), which)
        return str(self)

    def list(self) -> str:
        self._add('list')
        return str(self)

    def remove(self, id: str) -> str:
        self._add('remove', good_resource(id))
        return str(self)

    def set(self, id: str) -> BossbarSet:
        self._add('set', id)
        return self._start(BossbarSet())


class ClearClause(Chain):
    def item(self, item: str, max_count: int = None) -> str:
        self._add(item)
        if max_count:
            self._add('', max_count)
        return str(self)


class CloneClause(Chain):

    def _flag(self, flag):
        if flag:
            _in_group('CLONE_FLAGS', flag)
            self._add('', flag)

    def replace(self, flag: str = None) -> str:
        self._add('replace')
        self._flag(flag)
        return str(self)

    def masked(self, flag: str = None) -> str:
        self._add('masked')
        self._flag(flag)
        return str(self)

    def filtered(self, block_predicate: str, flag: str = None) -> str:
        self._add('filtered', block_predicate)
        self._flag(flag)
        return str(self)


class End(Chain):
    pass


class DataTarget(Chain):
    pass


class BlockData(DataTarget):
    def __init__(self, x: float | Coord, y: float | Coord, z: float | Coord):
        super().__init__()
        self._add('block', x, y, z)


class EntityData(DataTarget):
    def __init__(self, target: Target):
        super().__init__()
        self._add('entity', target)


class StorageData(DataTarget):
    def __init__(self, resource_path: str):
        super().__init__()
        self._add('storage', good_resource_path(resource_path))


class FromOrValue(Chain):
    def from_(self, data_target: DataTarget) -> str:
        self._add('from', data_target)
        return str(self)

    def value(self, nbt_tag: str) -> str:
        self._add('value', nbt_tag)
        return str(self)


class ModifyClause(Chain):
    def _keyword(self, keyword: str) -> FromOrValue:
        self._add(keyword)
        return self._start(FromOrValue())

    def append(self) -> FromOrValue:
        return self._keyword('append')

    def insert(self, index: int) -> FromOrValue:
        self._add('insert', index)
        return self._start(FromOrValue())

    def merge(self) -> FromOrValue:
        return self._keyword('merge')

    def prepend(self) -> FromOrValue:
        return self._keyword('prepend')

    def set(self) -> FromOrValue:
        return self._keyword('set')


class DataMod(Chain):
    def get(self, data_target: DataTarget, nbt_path: str = None, scale: float = None, /) -> str:
        self._add('get', data_target)
        if not nbt_path and scale is not None:
            raise ValueError('Must give path to use scale')
        self._add_opt(nbt_path, scale)
        return str(self)

    def merge(self, data_target: DataTarget, nbt: dict) -> str:
        self._add('merge', data_target, _NbtFormat(nbt))
        return str(self)

    def modify(self, data_target: DataTarget, nbt_path: str) -> ModifyClause:
        self._add('modify', data_target, nbt_path)
        return self._start(ModifyClause())

    def remove(self, data_target: DataTarget, nbt_path: str) -> str:
        self._add('remove', data_target, nbt_path)
        return str(self)


class DatapackAction(Chain):
    def disable(self, name: str) -> str:
        self._add('disable', good_name(name))
        return str(self)

    def enable(self, name, order: str = None, other_datapack: str = None) -> str:
        self._add('enable', name)
        if order:
            _in_group('ORDER', order)
            if order in (FIRST, LAST):
                self._add('', order)
            else:
                if not other_datapack:
                    raise ValueError('"%s" requires other_datapack value' % order)
                self._add('', order, other_datapack)
        return str(self)

    def list(self) -> str:
        self._add('list')
        return str(self)


class EffectAction(Chain):
    def give(self, target: Target, effect: Effects, seconds: int = None, amplifier: int = None,
             hide_particles: bool = None, /) -> str:
        if amplifier is not None and seconds is None:
            raise ValueError('must give seconds to use amplifier')
        if hide_particles is not None and amplifier is None:
            raise ValueError('must give amplifier to use hide_particles')
        seconds_range = range(0, MAX_EFFECT_SECONDS + 1)
        if seconds is not None and seconds not in seconds_range:
            raise ValueError('Not in range: %d (%s)' % (seconds, seconds_range))
        self._add('give', target, effect)
        self._add_opt(seconds, amplifier, _bool(hide_particles))
        return str(self)

    def clear(self, target: Target = None, effect: Effects = None, /) -> str:
        if effect is not None and target is None:
            raise ValueError('must give target to use effect')
        self._add('clear')
        self._add_opt(target, effect)
        return str(self)


class ExperienceMod(Chain):
    def add(self, target: Target, amount: int, which: str) -> str:
        _in_group('EXPERIENCE_POINTS', which)
        self._add('add', target, amount, which)
        return str(self)

    def set(self, target: Target, amount: int, which: str) -> str:
        _in_group('EXPERIENCE_POINTS', which)
        self._add('set', target, amount, which)
        return str(self)

    def query(self, target: Target, which: str) -> str:
        _in_group('EXPERIENCE_POINTS', which)
        self._add('query', target, which)
        return str(self)


class FilterClause(Chain):
    def filter(self, block_predicate: str) -> str:
        self._add('filter', block_predicate)
        return str(self)


def _good_col_coords(*coords):
    for c in coords:
        if '.' in str(c):
            raise ValueError('Only int values for column coordinates: %s' % c)


class ForceloadMod(Chain):
    def _to_from(self, action: str, from_x, from_z, to_x, to_z):
        if to_x is None != to_z is None:
            raise ValueError('Must specify both "to" coords or neither')
        _good_col_coords(from_x, from_z, to_x, to_z)
        self._add(action, from_x, from_z)
        self._add_opt(to_x, to_z)
        return str(self)

    def add(self, from_x: int | Coord, from_z: int | Coord, to_x: int | Coord = None, to_z: int | Coord = None,
            /) -> str:
        return self._to_from('add', from_x, from_z, to_x, to_z)

    def remove(self, from_x: int | Coord, from_z: int | Coord, to_x: int | Coord = None,
               to_z: int | Coord = None, /) -> str:
        return self._to_from('remove', from_x, from_z, to_x, to_z)

    def remove_all(self) -> str:
        self._add('remove', 'all')
        return str(self)

    def query(self, x: int | Coord = None, z: int | Coord = None) -> str:
        _good_col_coords(x, z)
        self._add('query')
        self._add_opt(x, z)
        return str(self)


class Command(Chain):
    def advancement(self, action: str, target: Selector, behavior: str,
                    advancement: Advancement = None,
                    criterion: str = None) -> str:
        action = _to_grant(action)
        _in_group('ADVANCEMENT', behavior)
        self._add('advancement', _grant(action), target, behavior)
        if behavior != EVERYTHING:
            self._add('', advancement)
            if behavior == ONLY and criterion:
                self._add('', criterion)
        return str(self)

    def attribute(self, target: Target, attribute: str) -> AttributeAct:
        """Queries, adds, removes or sets an entity attribute."""
        self._add('attribute', target, good_resource(attribute))
        return self._start(AttributeAct())

    def bossbar(self) -> BossbarAct:
        """Creates and modifies bossbars."""
        self._add('bossbar')
        return self._start(BossbarAct())

    def clear(self, target: Target, *targets: Target) -> ClearClause:
        """Clears items from player inventory."""
        self._add('clear', target, *targets)
        return self._start(ClearClause())

    def clone(self,
              start_x: float | Coord, start_y: float | Coord, start_z: float | Coord,
              end_x: float | Coord, end_y: float | Coord, end_z: float | Coord,
              dest_x: float | Coord, dest_y: float | Coord, dest_z: float | Coord) -> CloneClause:
        """Copies blocks from one place to another."""
        self._add('clone', start_x, start_y, start_z, end_x, end_y, end_z, dest_x, dest_y, dest_z)
        return self._start(CloneClause())

    def data(self) -> DataMod:
        """Gets, merges, modifies and removes block entity and entity NBT data."""
        self._add('data')
        return self._start(DataMod())

    def datapack(self) -> DatapackAction:
        """Controls loaded data packs."""
        self._add('datapack')
        return self._start(DatapackAction())

    def defaultgamemode(self, gamemode: str) -> str:
        """Sets the default game mode."""
        _in_group('GAMEMODE', gamemode)
        self._add('defaultgamemode', gamemode)
        return str(self)

    def deop(self, *targets: Selector | User) -> str:
        """Revokes operator status from a player."""
        self._add('deop', *targets)
        return str(self)

    def difficulty(self, difficulty: str) -> str:
        """Sets the difficulty level."""
        _in_group('DIFFICULTIES', difficulty)
        self._add('difficulty', difficulty)
        return str(self)

    def effect(self) -> EffectAction:
        """Adds or removes status effects."""
        self._add('effect')
        return self._start(EffectAction())

    def enchant(self, target: Target, enchantment: Enchantments | int, level: int = None) -> str:
        """Adds an enchantment to a player's selected item."""
        self._add('enchant', target)
        self._add('', enchantment)
        if level is not None:
            if type(enchantment) == Enchantments:
                max_level = Enchantments.max_level(enchantment)
                if level not in range(0, max_level + 1):
                    raise ValueError('Level not in range [0..%d]', max_level)
            self._add_opt(level)
        return str(self)

    def execute(self) -> ExecuteMod:
        """Executes another command."""
        self._add('execute')
        return self._start(ExecuteMod())

    def experience(self) -> ExperienceMod:
        """Adds or removes player experience."""
        self._add('experience')
        return self._start(ExperienceMod())

    xp = experience

    def fill(self,
             start_x: float | Coord, start_y: float | Coord, start_z: float | Coord,
             end_x: float | Coord, end_y: float | Coord, end_z: float | Coord,
             block: str, action: str) -> FilterClause | str:
        """Fills a region with a specific block."""
        _in_group('FILL_ACTIONS', action)
        self._add('fill', start_x, start_y, start_z, end_x, end_y, end_z, good_resource(block), action)
        if action == REPLACE:
            return self._start(FilterClause())
        return str(self)

    def forceload(self) -> ForceloaddMod:
        """Forces chunks to constantly be loaded or not."""
        self._add('forceload')
        return self._start(ForceloadMod())

    def function(self, path: str) -> str:
        """Runs a function."""
        self._add('function', good_resource_path(path))
        return str(self)

    def gamemode(self, gamemode: str, target: Target = None) -> str:
        _in_group('GAMEMODE', gamemode)
        self._add('gamemode', gamemode)
        self._add_opt(target)
        return str(self)

    def gamerule(self, rule: GameRules, value: bool | int = None) -> str:
        """Sets or queries a game rule value."""
        self._add('gamerule', rule)
        if value is not None:
            rule_type = GameRules.rule_type(rule)
            if rule_type == 'int':
                if type(value) != int:
                    raise ValueError('int value required for rule: %s' % rule)
                self._add('', int(value))
            else:
                self._add('', _bool(value))
        return str(self)

    def give(self):
        """Gives an item to a player."""

    def help(self):
        """An alias of /?. Provides help for commands."""

    def item(self):
        """Manipulates items in inventories."""

    def jfr(self):
        """ends or stops a JFR profiling."""

    def kick(self):
        """Kicks a player off a server."""

    def kill(self):
        """Kills entities (players, mobs, items, etc.)."""

    def list(self):
        """Lists players on the server."""

    def locate(self):
        """Locates closest structure."""

    def locatebiome(self):
        """Locates closest biome."""

    def loot(self):
        """Drops items from an inventory slot onto the ground."""

    def me(self):
        """Displays a message about the sender."""

    def msg(self):
        """An alias of /tell and /w. Displays a private message to other players."""

    def op(self):
        """Grants operator status to a player."""

    def pardon(self):
        """Removes entries from the banlist."""

    def pardon_ip(self):
        """Removes entries from the banlist."""

    def particle(self):
        """Creates particles."""

    def perf(self):
        """Captures info and metrics about the game for 10 seconds."""

    def place(self):
        """Used to place a configured feature, jigsaw, or structure at a given location."""

    def playsound(self):
        """Plays a sound."""

    def publish(self):
        """Opens single-player world to local network."""

    def recipe(self):
        """Gives or takes player recipes."""

    def reload(self):
        """Reloads loot tables, advancements, and functions from disk."""

    def save_all(self):
        """Saves the server to disk."""

    def save_off(self):
        """Disables automatic server saves."""

    def save_on(self):
        """Enables automatic server saves."""

    def say(self, *msg: str):
        """Displays a message to multiple players."""
        self._add('say', *msg)
        return str(self)

    def schedule(self):
        """Delays the execution of a function."""

    def scoreboard(self):
        """Manages scoreboard objectives and players."""

    def seed(self):
        """Displays the world seed."""

    def setblock(self):
        """Changes a block to another block."""

    def setidletimeout(self):
        """Sets the time before idle players are kicked."""

    def setworldspawn(self):
        """Sets the world spawn."""

    def spawnpoint(self):
        """Sets the spawn point for a player."""

    def spectate(self):
        """Make one player in spectator mode spectate an entity."""

    def spreadplayers(self):
        """Teleports entities to random locations."""

    def stop(self):
        """Stops a server."""

    def stopsound(self):
        """Stops a sound."""

    def summon(self):
        """Summons an entity."""

    def tag(self):
        """Controls entity tags."""

    def team(self):
        """Controls teams."""

    def teammsg(self):
        """An alias of /tm. Specifies the message to send to team."""

    def teleport(self):
        """An alias of /tp. Teleports entities."""

    def tell(self):
        """An alias of /msg and /w. Displays a private message to other players."""

    def tellraw(self):
        """Displays a JSON message to players."""

    def time(self):
        """Changes or queries the world's game time."""

    def title(self):
        """Manages screen titles."""

    def tm(self):
        """An alias of /teammsg. Specifies the message to send to team."""

    def tp(self):
        """An alias of /teleport. Teleports entities."""

    def trigger(self):
        """Sets a trigger to be activated."""

    def w(self):
        """An alias of /tell and /msg. Displays a private message to other players."""

    def warden_spawn_tracker(self):
        """Sets the spawn state of the Warden."""

    def weather(self):
        """Sets the weather."""

    def whitelist(self):
        """Manages server whitelist."""

    def worldborder(self):
        """Manages the world border."""

    def comment(self, text: str, wrap=False):
        """
        Inserts a comment.

        :param text: The text of the comment
        :param wrap: If False, the comment will be the text with each line prepended by a '# '. Otherwise, the text will
         be broken into paragraphs by blank lines, each paragraph will be formatted by textwrap.fill() (to 78 columns),
         and before each line is prepended by a '# '.
        """
        text = text.strip()
        if wrap:
            orig_paras = re.split(r'\n\s*\n', text)
            new_paras = (textwrap.fill(x, width=78) for x in orig_paras)
            text = '\n\n'.join(new_paras)
        text = text.replace('\n', '\n# ').replace('# \n', '#\n')
        return '# %s\n' % text

    def literal(self, text: str):
        """Puts the text in without modification."""
        return text


# Define stand-alone methods for each command that creates a command object, then prints it
top_level_defs = '\n\n'
command = Command()
for m in getmembers(command, ismethod):
    if m[0][0] == '_':
        continue
    sig = signature(m[1])
    to_pass = []
    for k in sig.parameters:
        p = sig.parameters[k]
        if p.kind == p.VAR_POSITIONAL:
            to_pass.append('*' + k)
        else:
            to_pass.append(k)
    pass_on = ', '.join(to_pass)
    top_level_def = \
        """def %s%s:
            return Command().%s(%s)
        """ % (m[0], (str(sig)), m[0], pass_on)
    top_level_defs += '\n\n' + top_level_def

exec(top_level_defs)
