from __future__ import annotations

import io
import re
from enum import Enum, auto
from inspect import signature, getmembers, ismethod

from .enums import Advancement, ValueEnum


class PyEum(Enum):
    def __str__(self):
        return super().name.lower()


class Sort(ValueEnum):
    NEAREST = "nearest"
    FURTHEST = 'furthest'
    RANDOM = 'random'
    ARBITRARY = 'arbitrary'


class Gamemode(ValueEnum):
    SURVIVAL = 'survival'
    CREATIVE = 'creative'
    ADVENTURE = 'adventure'
    HARDCORE = 'hardcore'
    SPECTATOR = 'spectator'


class Action(Enum):
    GIVE = auto()
    GRANT = GIVE
    CLEAR = auto()
    REVOKE = CLEAR

    @classmethod
    def grant_names(cls, action):
        return action == 'grant' if action == cls.GIVE else 'revoke'


class Range:
    def __init__(self, start: int | float = None, end: int | float = None, at: int | float = None):
        if not start and not end and not at:
            raise ValueError("Must specify start or end or at")
        self.start = str(start) if start else ''
        self.end = str(end) if end else ''
        self.at = str(at) if at else ''

    def __str__(self):
        return self.at if self.at else '%s..%s' % (self.start, self.end)


class ScoreRange:
    def __init__(self, score: str, range: Range, inverse=False):
        self.score = score
        self.range = range
        self.inverse = inverse


class AdvancementCriteria:
    def __init__(self, advancement: Advancement, criteria: bool | tuple[str, bool]):
        self.advancement = advancement
        self.criteria = None if isinstance(criteria, bool) else criteria[0]
        self.done = criteria if isinstance(criteria, bool) else criteria[1]

    def __str__(self):
        if self.criteria:
            return '%s={%s=%s}' % (self.advancement, self.criteria, str(self.done).lower())
        else:
            return '%s=%s' % (self.advancement, str(self.done).lower())


class _NbtFormat:
    _needs_quotes = re.compile(r'[\s:"]')

    def __init__(self, nbt: dict):
        self.nbt = nbt
        self.sio = io.StringIO()

    def __str__(self):
        self._dict(self.nbt)
        return self.sio.getvalue()

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


def notify(value):
    s = str(value)
    if s[0] != '!':
        s = '!' + s
    return s


class Target:
    _create_key = object()

    # noinspection PyUnusedLocal
    def __init__(self, create_key, selector):
        assert (create_key == Target._create_key), "Private __init__, use creation methods"
        self._selector = selector
        self._args = {}

    @classmethod
    def player(cls):
        return Target(cls._create_key, "@p")

    @classmethod
    def random(cls):
        return Target(cls._create_key, "@r")

    @classmethod
    def all(cls):
        return Target(cls._create_key, "@a")

    @classmethod
    def entities(cls):
        return Target(cls._create_key, "@e")

    @classmethod
    def self(cls):
        return Target(cls._create_key, "@s")

    def __str__(self):
        if len(self._args) == 0:
            return self._selector
        return self._selector + '[' + ','.join(self._args.values()) + ']'

    def _add_arg(self, key: str, value: any):
        v = str(value)
        if v.find('=') < 0 or v[0] == '{':
            v = '%s=%s' % (key, v)
        if key in self._args:
            self._args[key] += ',' + v
        else:
            self._args[key] = v

    def _unique_arg(self, key: str, value: any):
        if key in self._args:
            raise KeyError("Already set in target: %s" % key)
        self._add_arg(key, value)
        return self

    def _multi_args(self, key: str, value: any, values: tuple[any]):
        self._add_arg(key, value)
        for v in values:
            self._add_arg(key, v)
        return self

    def _not_args(self, key: str, value, values):
        self._add_arg(key, notify(value))
        for v in values:
            self._add_arg(key, notify(v));
        result = self._args[key]
        value_count = result.count('=')
        neg_count = result.count('!')
        if value_count > 1 and neg_count != value_count:
            raise KeyError("Cannot repeat %s unless all are negated: %s" % (key, result))
        return self

    def pos(self, x, y, z):
        return self._unique_arg('pos', 'x=%s,y=%s,z=%s' % (str(x), str(y), str(z)))

    def distance(self, distance: Range):
        return self._unique_arg('distance', distance)

    def delta(self, dx, dy, dz):
        return self._unique_arg('delta', 'dx=%s,dy=%s,dz=%s' % (str(dx), str(dy), str(dz)))

    def scores(self, *scores):
        return self._unique_arg('scores', '{' + ','.join(scores) + '}')

    def tag(self, tag: str, *tags: str):
        return self._multi_args('tag', tag, tags)

    def team(self, team: str):
        return self._unique_arg('team', team)

    def not_team(self, team: str, *teams):
        return self._not_args('team', team, teams)

    def sort(self, sorting: Sort):
        return self._unique_arg('sort', sorting)

    def limit(self, limit: int):
        return self._unique_arg('limit', str(limit))

    def level(self, range: Range):
        return self._unique_arg('level', range)

    def gamemode(self, gamemode: Gamemode):
        return self._unique_arg('gamemode', gamemode)

    def not_gamemode(self, gamemode: Gamemode, *gamemodes: Gamemode):
        return self._not_args('gamemode', gamemode, gamemodes)

    def name(self, name: str):
        return self._unique_arg('name', name)

    def not_name(self, name: str, *names: str):
        return self._not_args('name', name, names)

    def x_rotation(self, range: Range):
        self._unique_arg('x_rotation', range)
        return self

    def y_rotation(self, range: Range):
        self._unique_arg('y_rotation', range)
        return self

    def type(self, type: type):
        return self._unique_arg('type', type)

    def not_types(self, type: str, *types: str):
        return self._not_args('type', type, types)

    def nbt(self, nbt: dict, *nbts: dict):
        return self._multi_args('nbt', _NbtFormat(nbt), tuple(_NbtFormat(x)
                                                              for x in nbts))

    def advancements(self, advancement: AdvancementCriteria, *advancements: AdvancementCriteria):
        adv = [advancement, ]
        for a in advancements:
            adv.append(a)
        return self._unique_arg('advancements', '{' + ','.join(str(x) for x in adv) + '}')

    def predicate(self, predicate: str, *predicates: str):
        return self._multi_args('predicate', predicate, predicates)


def _grant(action: Action):
    return 'grant' if action == Action.GRANT else 'revoke'


class Param(Enum):
    def __str__(self):
        return super().name.lower()


class AdvancementBehavior(Param):
    EVERYTHING = auto()
    ONLY = auto()
    FROM = auto()
    THROUGH = auto()
    UNTIL = auto()


class Command:
    def __int__(self):
        self.str = None

    def __str__(self):
        return self.str

    def advancement(self, action: Action, target: Target, behavior: AdvancementBehavior,
                    advancement: Advancement = None,
                    criterion: str = None):
        cmd = "advancement %s %s %s" % (_grant(action), target, behavior)
        if behavior != AdvancementBehavior.EVERYTHING:
            cmd += ' %s' % advancement
            if behavior == AdvancementBehavior.ONLY and criterion:
                cmd += ' %s' % criterion
        self.str = cmd

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
        """Starts or stops a debugging session."""

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

    def execute(self):
        """Executes another command."""

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
        """Starts or stops a JFR profiling."""

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

    def say(self):
        """Displays a message to multiple players."""

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
    sig = signature(m[1])
    old_sig = str(sig)
    added = 'out=sys.stdout)'
    if old_sig != '()':
        added = ', ' + added
    new_sig = str(sig)[:-1] + added
    pass_on = ', '.join(sig.parameters.keys())
    cmd = \
        """def %s%s:
            out.write(Command().%s(%s))
        """ % (m[0], new_sig, m[0], pass_on)
    cmds += '\n\n' + cmd

exec(cmds)
