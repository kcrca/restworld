import pytest

from restworld.commands import *
from restworld.commands import _NbtFormat


def test_command_advancement():
    for give in Action.GIVE, Action.GRANT:
        assert str(Command().advancement(give, TargetSelector.self(),
                                         AdvancementBehavior.EVERYTHING)) == 'advancement grant @s everything'
        assert str(Command().advancement(give, TargetSelector.self(),
                                         AdvancementBehavior.ONLY,
                                         Advancement.A_BALANCED_DIET,
                                         "pig")) == 'advancement grant @s only husbandry/balanced_diet pig'
        assert str(Command().advancement(give, TargetSelector.self(),
                                         AdvancementBehavior.FROM,
                                         Advancement.WAX_ON)) == 'advancement grant @s from husbandry/wax_on'
        assert str(Command().advancement(give, TargetSelector.self(),
                                         AdvancementBehavior.THROUGH,
                                         Advancement.WAX_ON)) == 'advancement grant @s through husbandry/wax_on'
        assert str(Command().advancement(give, TargetSelector.self(),
                                         AdvancementBehavior.UNTIL,
                                         Advancement.WAX_ON)) == 'advancement grant @s until husbandry/wax_on'

    for give in Action.REVOKE, Action.CLEAR:
        assert str(Command().advancement(give, TargetSelector.self(),
                                         AdvancementBehavior.EVERYTHING)) == 'advancement revoke @s everything'
        assert str(Command().advancement(give, TargetSelector.self(),
                                         AdvancementBehavior.ONLY,
                                         Advancement.A_BALANCED_DIET,
                                         "pig")) == 'advancement revoke @s only husbandry/balanced_diet pig'
        assert str(Command().advancement(give, TargetSelector.self(),
                                         AdvancementBehavior.FROM,
                                         Advancement.WAX_ON)) == 'advancement revoke @s from husbandry/wax_on'
        assert str(Command().advancement(give, TargetSelector.self(),
                                         AdvancementBehavior.THROUGH,
                                         Advancement.WAX_ON)) == 'advancement revoke @s through husbandry/wax_on'
        assert str(Command().advancement(give, TargetSelector.self(),
                                         AdvancementBehavior.UNTIL,
                                         Advancement.WAX_ON)) == 'advancement revoke @s until husbandry/wax_on'


def test_command_execute():
    assert str(Command().execute().align(Axes.XZ)) == 'execute align xz'
    assert str(Command().execute().anchored(EntityAnchor.EYES)) == 'execute anchored eyes'
    assert str(Command().execute().as_(TargetSelector.self().tag('fred'))) == 'execute as @s[tag=fred]'
    assert str(Command().execute().at(Uuid(1, 3, 5, 7))) == 'execute at [1, 3, 5, 7]'
    assert str(Command().execute().facing(1, r(2), d(3))) == 'execute facing 1 ~2 ^3'
    assert str(Command().execute().facing_entity(User('Fred'), EntityAnchor.FEET)) == 'execute facing entity Fred feet'
    assert str(Command().execute().in_(Dimension.THE_NETHER)) == 'execute in the_nether'
    assert str(Command().execute().if_().block(1, r(2), d(3), 'stone')) == 'execute if block 1 ~2 ^3 stone'


def test_range():
    assert str(Range(at=3)) == '3'
    assert str(Range(1, 3)) == '1..3'
    assert str(Range(None, 3)) == '..3'
    assert str(Range(1, None)) == '1..'
    with pytest.raises(ValueError):
        Range()


def test_coords():
    assert str(r(1)) == '~1'
    assert str(r(-1.5)) == '~-1.5'
    assert str(d(1)) == '^1'
    assert str(d(-1.5)) == '^-1.5'


def test_nbt_format():
    assert str(_NbtFormat({})) == '{}'
    assert str(_NbtFormat({'q': 17})) == '{q:17}'
    assert str(_NbtFormat({'q': [1, 2, 3.5]})) == '{q:[1,2,3.5]}'
    assert str(_NbtFormat({'q': [1, 2, {'t': True}]})) == '{q:[1,2,{t:true}]}'
    assert str(_NbtFormat({'q': [1, 2, {'t': True}]})) == '{q:[1,2,{t:true}]}'
    assert str(_NbtFormat({"name": '"Hi there"'})) == r'{name:"\"Hi there\""}'
    assert str(_NbtFormat({"id": "minecraft:air"})) == '{id:"minecraft:air"}'


def test_target_player():
    assert str(TargetSelector.player()) == '@p'


def test_target_random():
    assert str(TargetSelector.random()) == '@r'


def test_target_all():
    assert str(TargetSelector.all()) == '@a'


def test_target_entities():
    assert str(TargetSelector.entities()) == '@e'


def test_target_pos():
    assert str(TargetSelector.all().pos(1, 2, 3)) == '@a[x=1,y=2,z=3]'
    with pytest.raises(KeyError):
        TargetSelector.all().pos(1, 2, 3).pos(4, 5, 6)


def test_target_distance():
    assert str(TargetSelector.all().distance(Range(at=3))) == '@a[distance=3]'
    assert str(TargetSelector.all().distance(Range(1, 3))) == '@a[distance=1..3]'
    assert str(TargetSelector.all().distance(Range(None, 3))) == '@a[distance=..3]'
    assert str(TargetSelector.all().distance(Range(1, None))) == '@a[distance=1..]'
    with pytest.raises(KeyError):
        TargetSelector.all().distance(3).distance(4)


def test_target_delta():
    assert str(TargetSelector.all().delta(1, 2, 3)) == '@a[dx=1,dy=2,dz=3]'
    with pytest.raises(KeyError):
        TargetSelector.all().delta(1, 2, 3).delta(4, 5, 6)


def test_target_scores():
    assert str(TargetSelector.all().scores('x=1', 'y=..3')) == '@a[scores={x=1,y=..3}]'
    with pytest.raises(KeyError):
        TargetSelector.all().scores('x=1').scores('y=..3')


def test_target_tag():
    assert str(TargetSelector.all().tag('foo')) == '@a[tag=foo]'
    assert str(TargetSelector.all().tag('foo', 'bar')) == '@a[tag=foo,tag=bar]'
    assert str(TargetSelector.all().tag('foo').tag('bar')) == '@a[tag=foo,tag=bar]'


def test_target_team():
    assert str(TargetSelector.all().team('foo')) == '@a[team=foo]'
    with pytest.raises(KeyError):
        TargetSelector.all().team('foo').team('bar')


def test_target_not_teams():
    assert str(TargetSelector.all().not_team('foo')) == '@a[team=!foo]'
    assert str(TargetSelector.all().not_team('foo', 'bar')) == '@a[team=!foo,team=!bar]'
    assert str(TargetSelector.all().not_team('foo', '!bar')) == '@a[team=!foo,team=!bar]'
    assert str(TargetSelector.all().not_team('foo').not_team('bar')) == '@a[team=!foo,team=!bar]'
    assert str(TargetSelector.all().not_team('foo').not_team('!bar')) == '@a[team=!foo,team=!bar]'
    with pytest.raises(KeyError):
        TargetSelector.all().team('foo').not_team('bar')


def test_target_sort():
    assert str(TargetSelector.all().sort(Sort.NEAREST)) == '@a[sort=nearest]'
    with pytest.raises(KeyError):
        TargetSelector.all().sort(Sort.NEAREST).sort(Sort.RANDOM)


def test_target_limit():
    assert str(TargetSelector.all().limit(1)) == '@a[limit=1]'
    with pytest.raises(KeyError):
        TargetSelector.all().limit(1).limit(2)


def test_target_level():
    assert str(TargetSelector.all().level(Range(at=3))) == '@a[level=3]'
    assert str(TargetSelector.all().level(Range(1, 3))) == '@a[level=1..3]'
    assert str(TargetSelector.all().level(Range(None, 3))) == '@a[level=..3]'
    assert str(TargetSelector.all().level(Range(1, None))) == '@a[level=1..]'
    with pytest.raises(KeyError):
        TargetSelector.all().level(3).level(4)


def test_target_gamemode():
    assert str(TargetSelector.all().gamemode(Gamemode.SURVIVAL)) == '@a[gamemode=survival]'
    with pytest.raises(KeyError):
        TargetSelector.all().gamemode(Gamemode.CREATIVE).gamemode(Gamemode.ADVENTURE)


def test_target_not_gamemodes():
    assert str(TargetSelector.all().not_gamemode(Gamemode.SURVIVAL)) == '@a[gamemode=!survival]'
    assert str(
        TargetSelector.all().not_gamemode(Gamemode.SURVIVAL,
                                          Gamemode.CREATIVE)) == '@a[gamemode=!survival,gamemode=!creative]'
    with pytest.raises(KeyError):
        TargetSelector.all().gamemode(Gamemode.CREATIVE).not_gamemode(Gamemode.ADVENTURE)


def test_target_name():
    assert str(TargetSelector.all().name('foo')) == '@a[name=foo]'
    with pytest.raises(KeyError):
        TargetSelector.all().name('foo').name('bar')


def test_target_not_names():
    assert str(TargetSelector.all().not_name('foo')) == '@a[name=!foo]'
    assert str(TargetSelector.all().not_name('foo', 'bar')) == '@a[name=!foo,name=!bar]'
    assert str(TargetSelector.all().not_name('foo', '!bar')) == '@a[name=!foo,name=!bar]'
    assert str(TargetSelector.all().not_name('foo').not_name('bar')) == '@a[name=!foo,name=!bar]'
    assert str(TargetSelector.all().not_name('foo').not_name('!bar')) == '@a[name=!foo,name=!bar]'
    with pytest.raises(KeyError):
        TargetSelector.all().name('foo').not_name('bar')


def test_target_x_rotation():
    assert str(TargetSelector.all().x_rotation(1.5)) == '@a[x_rotation=1.5]'
    with pytest.raises(KeyError):
        TargetSelector.all().x_rotation(1.5).x_rotation(1.5)


def test_target_y_rotation():
    assert str(TargetSelector.all().y_rotation(1.5)) == '@a[y_rotation=1.5]'
    with pytest.raises(KeyError):
        TargetSelector.all().y_rotation(1.5).y_rotation(1.5)


def test_target_type():
    assert str(TargetSelector.all().type('creeper')) == '@a[type=creeper]'
    with pytest.raises(KeyError):
        TargetSelector.all().type('creeper').type('bat')


def test_target_not_types():
    assert str(TargetSelector.all().not_types('foo')) == '@a[type=!foo]'
    assert str(TargetSelector.all().not_types('foo', 'bar')) == '@a[type=!foo,type=!bar]'
    assert str(TargetSelector.all().not_types('foo', '!bar')) == '@a[type=!foo,type=!bar]'
    assert str(TargetSelector.all().not_types('foo').not_types('bar')) == '@a[type=!foo,type=!bar]'
    assert str(TargetSelector.all().not_types('foo').not_types('!bar')) == '@a[type=!foo,type=!bar]'
    with pytest.raises(KeyError):
        TargetSelector.all().type('foo').not_types('bar')


def test_target_nbt():
    assert str(TargetSelector.all().nbt({'a': 17})) == '@a[nbt={a:17}]'
    assert str(TargetSelector.all().nbt({'a': 17}, {'b': 'hi there'})) == '@a[nbt={a:17},nbt={b:"hi there"}]'
    assert str(TargetSelector.all().nbt({'a': 17}).nbt({'b': 'hi there'})) == '@a[nbt={a:17},nbt={b:"hi there"}]'


def test_target_advancements():
    assert str(TargetSelector.all().advancements(
        AdvancementCriteria(Advancement.WAX_ON, True))) == '@a[advancements={husbandry/wax_on=true}]'
    assert str(TargetSelector.all().advancements(AdvancementCriteria(Advancement.WAX_ON,
                                                                     ('stuff',
                                                                      False)))) == '@a[advancements={husbandry/wax_on={stuff=false}}]'


def test_target_predicate():
    assert str(TargetSelector.all().predicate('foo')) == '@a[predicate=foo]'
    assert str(TargetSelector.all().predicate('foo', 'bar')) == '@a[predicate=foo,predicate=bar]'
    assert str(TargetSelector.all().predicate('foo').predicate('bar')) == '@a[predicate=foo,predicate=bar]'


def test_target_chainability():
    assert str(TargetSelector.all().pos(1, 2, 3).distance(Range(None, 15.5)).delta(4.4, 5.5, 6.6).scores().tag("one")
        .team('slug').sort(Sort.ARBITRARY).limit(15).level(Range(3, 15)).gamemode(Gamemode.HARDCORE)
        .name('Robin').x_rotation(Range(at=9)).y_rotation(Range(None, 24)).type('cougar')
        .nbt({"hi": "there"}).advancements(AdvancementCriteria(Advancement.A_SEEDY_PLACE, True))
        .predicate(
        "nada")) == '@a[x=1,y=2,z=3,distance=..15.5,dx=4.4,dy=5.5,dz=6.6,scores={},tag=one,team=slug,sort=arbitrary,limit=15,level=3..15,gamemode=hardcore,name=Robin,x_rotation=9,y_rotation=..24,type=cougar,nbt={hi:there},advancements={husbandry/plant_seed=true},predicate=nada]'
    assert str(TargetSelector.all().not_team('Raiders').not_name("GRBX").not_gamemode(Gamemode.CREATIVE)
               .not_types("worm")) == '@a[team=!Raiders,name=!GRBX,gamemode=!creative,type=!worm]'
