from __future__ import annotations

import re
import typing
from abc import abstractmethod
from functools import wraps
from inspect import signature, getmembers, ismethod
from io import StringIO

from .enums import Advancement


def fluent(method):
    @wraps(method)
    def inner(self, *args, **kwargs):
        obj = self.__class__.__new__(self.__class__)
        obj.__dict__ = self.__dict__.copy()
        method(obj, *args, **kwargs)
        return obj

    return inner


def _in_group(group: str, *names: str):
    group = globals()[group.upper()]
    missing = []
    for n in names:
        if n not in group:
            missing.append(n)
    if missing:
        raise ValueError('Not in %s: %s' % (group, missing))


NEAREST = 'nearest'
FURTHEST = 'furthest'
RANDOM = 'random'
ARBITRARY = 'arbitrary'
SORT = [NEAREST, FURTHEST, RANDOM, ARBITRARY]

SURVIVAL = 'survival'
CREATIVE = 'creative'
ADVENTURE = 'adventure'
HARDCORE = 'hardcore'
SPECTATOR = 'spectator'
GAMEMODE = [SURVIVAL, CREATIVE, ADVENTURE, HARDCORE, SPECTATOR]

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

GIVE = 'give'
CLEAR = 'clear'
GIVE_CLEAR = [GIVE, CLEAR]

GRANT = 'grant'
REVOKE = 'revoke'
GRANT_REVOKE = [GRANT, REVOKE]

GIVE_GRANT = GIVE_CLEAR + GRANT_REVOKE


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


def _bool(criteria: bool) -> str:
    return str(criteria).lower()


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
        self._add(target, objective)


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
            self._add('%s={%s=%s}' % (advancement, criteria[0], _bool(criteria[1])))


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
    _name_re = re.compile(r'\w+')

    def __init__(self, name: str):
        super().__init__()
        if not User._name_re.match(name):
            raise ValueError('Invalid user name: %s' % name)
        self._add(name)


class Uuid(Target):
    def __init__(self, u1: int, u2: int, u3: int, u4: int):
        super().__init__()
        self._add([u1, u2, u3, u4])


class TargetSelector(Target):
    _create_key = object()

    @classmethod
    def player(cls):
        return TargetSelector(cls._create_key, '@p')

    @classmethod
    def random(cls):
        return TargetSelector(cls._create_key, '@r')

    @classmethod
    def all(cls):
        return TargetSelector(cls._create_key, '@a')

    @classmethod
    def entities(cls):
        return TargetSelector(cls._create_key, '@e')

    @classmethod
    def self(cls):
        return TargetSelector(cls._create_key, '@s')

    @classmethod
    def self_(cls):
        """Here so it can be imported as a shorthand."""
        return cls.self()

    def __init__(self, create_key, selector):
        super().__init__()
        assert (create_key == TargetSelector._create_key), "Private __init__, use creation methods"
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
        return self._multi_args('tag', tag, tags)

    @fluent
    def not_tag(self, tag: str, *tags: str):
        return self.tag(not_ify(tag), not_ify(tags))

    @fluent
    def team(self, team: str):
        return self._unique_arg('team', team)

    @fluent
    def not_team(self, team: str, *teams):
        return self._not_args('team', team, teams)

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
        return self._unique_arg('name', name)

    @fluent
    def not_name(self, name: str, *names: str):
        return self._not_args('name', name, names)

    @fluent
    def x_rotation(self, rot_range: Range):
        self._unique_arg('x_rotation', rot_range)
        return self

    @fluent
    def y_rotation(self, rot_range: Range):
        self._unique_arg('y_rotation', rot_range)
        return self

    @fluent
    def type(self, type_: type):
        return self._unique_arg('type', type_)

    @fluent
    def not_types(self, type_: str, *types: str):
        return self._not_args('type', type_, types)

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
        self._add('block', x, y, z, block_name)
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

    def data_block(self, x: float | Coord, y: float | Coord, z: float | Coord, path: str) -> ExecuteMod:
        self._add('data', 'block', x, y, z, path)
        return self._start(ExecuteMod())

    def data_entity(self, target: Target, path: str) -> ExecuteMod:
        self._add('data', 'entity', target, path)
        return self._start(ExecuteMod())

    def data_storage(self, source: str, path: str) -> ExecuteMod:
        self._add('data', 'storage', source, path)
        return self._start(ExecuteMod())

    def predicate(self, predicate: str) -> ExecuteMod:
        self._add('predicate', predicate)
        return self._start(ExecuteMod())

    def score(self, target: Target | str, objective: str) -> ScoreClause:
        self._add('score', Score(target, objective))
        return self._start(ScoreClause())


class StoreClause(Chain):
    def block(self, x: float | Coord, y: float | Coord, z: float | Coord, path: str, data_type: str,
              scale: float) -> ExecuteMod:
        _in_group('DATA_TYPE', data_type)
        self._add('block', x, y, z, path, data_type, scale)
        return self._start(ExecuteMod())

    def bossbar(self, id: str, param: str) -> ExecuteMod:
        _in_group('BOSSBAR', param)
        self._add('bossbar', id, param)
        return self._start(ExecuteMod())

    def entity(self, target: Target, path: str, data_type: str, scale: float) -> ExecuteMod:
        _in_group('DATA_TYPE', data_type)
        self._add('entity', target, path, data_type, scale)
        return self._start(ExecuteMod())

    def score(self, target: Target | str, objective: str) -> ExecuteMod:
        self._add('score', Score(target, objective))
        return self._start(ExecuteMod())

    def storage(self, target: Target, path: str, data_type: str, scale: float) -> ExecuteMod:
        _in_group('DATA_TYPE', data_type)
        self._add('storage', target, path, data_type, scale)
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


class Command(Chain):
    def advancement(self, action: str, target: TargetSelector, behavior: str,
                    advancement: Advancement = None,
                    criterion: str = None):
        action = _to_grant(action)
        _in_group('ADVANCEMENT', behavior)
        self._add('advancement', _grant(action), target, behavior)
        if behavior != EVERYTHING:
            self._add('', advancement)
            if behavior == ONLY and criterion:
                self._add('', criterion)
        return str(self)

    def attribute(self):
        """Queries, adds, removes or sets an entity attribute."""

    def ban(self):
        """Adds player to banlist."""

    def ban_ip(self):
        """Adds IP address to banlist."""

    def banlist(self):
        """Displays banlist."""

    def bossbar(self):
        """Creates and modifies bossbars."""

    def clear(self):
        """Clears items from player inventory."""

    def clone(self):
        """Copies blocks from one place to another."""

    def data(self):
        """Gets, merges, modifies and removes block entity and entity NBT data."""

    def datapack(self):
        """Controls loaded data packs."""

    def debug(self):
        """ends or stops a debugging session."""

    def defaultgamemode(self):
        """Sets the default game mode."""

    def deop(self):
        """Revokes operator status from a player."""

    def difficulty(self):
        """Sets the difficulty level."""

    def effect(self):
        """Adds or removes status effects."""

    def enchant(self):
        """Adds an enchantment to a player's selected item."""

    def execute(self) -> ExecuteMod:
        """Executes another command."""
        self._add('execute')
        return self._start(ExecuteMod())

    def experience(self):
        """An alias of /xp. Adds or removes player experience."""

    def fill(self):
        """Fills a region with a specific block."""

    def forceload(self):
        """Forces chunks to constantly be loaded or not."""

    def function(self):
        """Runs a function."""

    def gamemode(self):
        """Sets a player's game mode."""

    def gamerule(self):
        """Sets or queries a game rule value."""

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


# Define stand-alone methods for each command that creates a command object, then prints it
cmds = 'import sys\n\n'
command = Command()
for m in getmembers(command, ismethod):
    if m[0][0] == '_':
        continue
    sig = signature(m[1])
    old_sig = str(sig)
    added = 'out=sys.stdout'
    if old_sig[0:1] == '()':
        new_sig = '(' + added + ')' + old_sig[2:]
    else:
        new_sig = re.sub(r'\)( -> .*)?:$', ', ' + added + r'\1', old_sig)
    pass_on = ', '.join(sig.parameters.keys())
    cmd = \
        """def %s%s:
            out.write(Command().%s(%s))
        """ % (m[0], new_sig, m[0], pass_on)
    cmds += '\n\n' + cmd

exec(cmds)

# Add everything to 'import *'