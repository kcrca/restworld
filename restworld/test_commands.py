import pytest

from restworld.commands import *
from restworld.commands import _NbtFormat


def test_command_advancement():
    assert str(advancement(GIVE, self(), EVERYTHING)) == 'advancement grant @s everything'
    assert str(advancement(GIVE, self(), ONLY, Advancement.A_BALANCED_DIET,
                           "pig")) == 'advancement grant @s only husbandry/balanced_diet pig'
    assert str(advancement(GIVE, self(), FROM,
                           Advancement.WAX_ON)) == 'advancement grant @s from husbandry/wax_on'
    assert str(advancement(GIVE, self(), THROUGH,
                           Advancement.WAX_ON)) == 'advancement grant @s through husbandry/wax_on'
    assert str(advancement(GIVE, self(), UNTIL,
                           Advancement.WAX_ON)) == 'advancement grant @s until husbandry/wax_on'

    assert str(advancement(REVOKE, self(), EVERYTHING)) == 'advancement revoke @s everything'
    assert str(advancement(REVOKE, self(), ONLY, Advancement.A_BALANCED_DIET,
                           "pig")) == 'advancement revoke @s only husbandry/balanced_diet pig'
    assert str(advancement(REVOKE, self(), FROM,
                           Advancement.WAX_ON)) == 'advancement revoke @s from husbandry/wax_on'
    assert str(advancement(REVOKE, self(), THROUGH,
                           Advancement.WAX_ON)) == 'advancement revoke @s through husbandry/wax_on'
    assert str(advancement(REVOKE, self(), UNTIL,
                           Advancement.WAX_ON)) == 'advancement revoke @s until husbandry/wax_on'

    with pytest.raises(ValueError):
        advancement('foo', self(), ONLY, Advancement.A_BALANCED_DIET, "pig")
        advancement(GIVE, self(), 'foo', Advancement.A_BALANCED_DIET, "pig")


def test_command_execute():
    assert str(execute().align(XZ)) == 'execute align xz'
    with pytest.raises(ValueError):
        execute().align('foo')


def test_execute_mod():
    assert str(ExecuteMod().align(XZ)) == 'align xz'
    assert str(ExecuteMod().anchored(EYES)) == 'anchored eyes'
    assert str(ExecuteMod().as_(self().tag('robin'))) == 'as @s[tag=robin]'
    assert str(ExecuteMod().at(Uuid(1, 3, 5, 7))) == 'at [1, 3, 5, 7]'
    assert str(ExecuteMod().facing(1, r(2), d(3))) == 'facing 1 ~2 ^3'
    assert str(ExecuteMod().facing_entity(User('robin'), FEET)) == 'facing entity robin feet'
    assert str(ExecuteMod().in_(THE_NETHER)) == 'in the_nether'
    assert str(ExecuteMod().if_().block(1, r(2), d(3), 'stone')) == 'if block 1 ~2 ^3 stone'
    assert str(ExecuteMod().unless().block(1, r(2), d(3), 'stone')) == 'unless block 1 ~2 ^3 stone'
    assert str(
        ExecuteMod().store().block(1, r(2), d(3), '{}', SHORT, 1.3)) == 'store block 1 ~2 ^3 {} short 1.3'
    assert str(ExecuteMod().run().say('hi')) == 'run say hi'
    with pytest.raises(ValueError):
        ExecuteMod().align('foo')
        ExecuteMod().anchored('foo')
        ExecuteMod().facing_entity(User('robin'), 'foo')
        ExecuteMod().in_('foo')
        ExecuteMod().store().block(1, r(2), d(3), '{}', 'foo', 1.3)


def test_if_clause():
    assert str(IfClause().blocks(1, 2, 3, 4, 5, 6, 7, 8, 9, MASKED)) == 'blocks 1 2 3 4 5 6 7 8 9 masked'
    assert str(IfClause().data_block(1, r(2), d(3), '{}')) == 'data block 1 ~2 ^3 {}'
    assert str(IfClause().data_entity(all(), '{}')) == 'data entity @a {}'
    assert str(IfClause().data_storage('stone', '{}')) == 'data storage stone {}'
    assert str(IfClause().predicate('foo')) == 'predicate foo'
    assert str(IfClause().score('*', 'bar').is_(LT, User('up'), 'down')) == 'score * bar < up down'
    assert str(IfClause().score('*', 'bar').matches(Range(end=10))) == 'score * bar matches ..10'
    with pytest.raises(ValueError):
        IfClause().score('foo', 'bar').matches(Range(end=10))
        IfClause().blocks(1, 2, 3, 4, 5, 6, 7, 8, 9, 'foo')
        IfClause().score('*', 'bar').is_('foo', User('up'), 'down')


def test_store_clause():
    assert str(StoreClause().block(1, r(2), d(3), '{}', SHORT, 1.3)) == 'block 1 ~2 ^3 {} short 1.3'
    assert str(StoreClause().bossbar('stud', MAX)) == 'bossbar stud max'
    assert str(StoreClause().entity(player(), '{}', FLOAT, 3.5)) == 'entity @p {} float 3.5'
    assert str(StoreClause().score(entities(), 'foo')) == 'score @e foo'
    assert str(StoreClause().storage(self(), '{}', DOUBLE, 1.9)) == 'storage @s {} double 1.9'
    with pytest.raises(ValueError):
        StoreClause().bossbar('stud', 'foo')
        StoreClause().entity(player(), '{}', 'foo', 3.5)
        StoreClause().storage(self(), '{}', 'foo', 1.9)


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
    assert str(player()) == '@p'


def test_target_random():
    assert str(random()) == '@r'


def test_target_all():
    assert str(all()) == '@a'


def test_target_entities():
    assert str(entities()) == '@e'


def test_score():
    assert str(Score('*', 'foo')) == '* foo'
    assert str(Score(all(), 'bar')) == '@a bar'
    with pytest.raises(ValueError):
        Score('bar', 'foo')


def test_target_pos():
    assert str(all().pos(1, 2, 3)) == '@a[x=1,y=2,z=3]'
    with pytest.raises(KeyError):
        all().pos(1, 2, 3).pos(4, 5, 6)


def test_target_distance():
    assert str(all().distance(Range(at=3))) == '@a[distance=3]'
    assert str(all().distance(Range(1, 3))) == '@a[distance=1..3]'
    assert str(all().distance(Range(None, 3))) == '@a[distance=..3]'
    assert str(all().distance(Range(1, None))) == '@a[distance=1..]'
    with pytest.raises(KeyError):
        all().distance(3).distance(4)


def test_target_delta():
    assert str(all().delta(1, 2, 3)) == '@a[dx=1,dy=2,dz=3]'
    with pytest.raises(KeyError):
        all().delta(1, 2, 3).delta(4, 5, 6)


def test_target_scores():
    assert str(all().scores('x=1', 'y=..3')) == '@a[scores={x=1,y=..3}]'
    with pytest.raises(KeyError):
        all().scores('x=1').scores('y=..3')


def test_target_tag():
    assert str(all().tag('foo')) == '@a[tag=foo]'
    assert str(all().tag('foo', 'bar')) == '@a[tag=foo,tag=bar]'
    assert str(all().tag('foo').tag('bar')) == '@a[tag=foo,tag=bar]'


def test_target_team():
    assert str(all().team('foo')) == '@a[team=foo]'
    with pytest.raises(KeyError):
        all().team('foo').team('bar')


def test_target_not_teams():
    assert str(all().not_team('foo')) == '@a[team=!foo]'
    assert str(all().not_team('foo', 'bar')) == '@a[team=!foo,team=!bar]'
    assert str(all().not_team('foo', '!bar')) == '@a[team=!foo,team=!bar]'
    assert str(all().not_team('foo').not_team('bar')) == '@a[team=!foo,team=!bar]'
    assert str(all().not_team('foo').not_team('!bar')) == '@a[team=!foo,team=!bar]'
    with pytest.raises(KeyError):
        all().team('foo').not_team('bar')


def test_target_sort():
    assert str(all().sort(NEAREST)) == '@a[sort=nearest]'
    with pytest.raises(KeyError):
        all().sort(NEAREST).sort(RANDOM)
        all().sort('foo')


def test_target_limit():
    assert str(all().limit(1)) == '@a[limit=1]'
    with pytest.raises(KeyError):
        all().limit(1).limit(2)


def test_target_level():
    assert str(all().level(Range(at=3))) == '@a[level=3]'
    assert str(all().level(Range(1, 3))) == '@a[level=1..3]'
    assert str(all().level(Range(None, 3))) == '@a[level=..3]'
    assert str(all().level(Range(1, None))) == '@a[level=1..]'
    with pytest.raises(KeyError):
        all().level(3).level(4)


def test_target_gamemode():
    assert str(all().gamemode(SURVIVAL)) == '@a[gamemode=survival]'
    with pytest.raises(KeyError):
        all().gamemode(CREATIVE).gamemode(ADVENTURE)
        all().gamemode('foo')


def test_target_not_gamemodes():
    assert str(all().not_gamemode(SURVIVAL)) == '@a[gamemode=!survival]'
    assert str(
        all().not_gamemode(SURVIVAL,
                           CREATIVE)) == '@a[gamemode=!survival,gamemode=!creative]'
    with pytest.raises(KeyError):
        all().gamemode(CREATIVE).not_gamemode(ADVENTURE)
        all().not_gamemode('foo')


def test_target_name():
    assert str(all().name('foo')) == '@a[name=foo]'
    with pytest.raises(KeyError):
        all().name('foo').name('bar')


def test_target_not_names():
    assert str(all().not_name('foo')) == '@a[name=!foo]'
    assert str(all().not_name('foo', 'bar')) == '@a[name=!foo,name=!bar]'
    assert str(all().not_name('foo', '!bar')) == '@a[name=!foo,name=!bar]'
    assert str(all().not_name('foo').not_name('bar')) == '@a[name=!foo,name=!bar]'
    assert str(all().not_name('foo').not_name('!bar')) == '@a[name=!foo,name=!bar]'
    with pytest.raises(KeyError):
        all().name('foo').not_name('bar')


def test_target_x_rotation():
    assert str(all().x_rotation(1.5)) == '@a[x_rotation=1.5]'
    with pytest.raises(KeyError):
        all().x_rotation(1.5).x_rotation(1.5)


def test_target_y_rotation():
    assert str(all().y_rotation(1.5)) == '@a[y_rotation=1.5]'
    with pytest.raises(KeyError):
        all().y_rotation(1.5).y_rotation(1.5)


def test_target_type():
    assert str(all().type('creeper')) == '@a[type=creeper]'
    with pytest.raises(KeyError):
        all().type('creeper').type('bat')


def test_target_not_types():
    assert str(all().not_types('foo')) == '@a[type=!foo]'
    assert str(all().not_types('foo', 'bar')) == '@a[type=!foo,type=!bar]'
    assert str(all().not_types('foo', '!bar')) == '@a[type=!foo,type=!bar]'
    assert str(all().not_types('foo').not_types('bar')) == '@a[type=!foo,type=!bar]'
    assert str(all().not_types('foo').not_types('!bar')) == '@a[type=!foo,type=!bar]'
    with pytest.raises(KeyError):
        all().type('foo').not_types('bar')


def test_target_nbt():
    assert str(all().nbt({'a': 17})) == '@a[nbt={a:17}]'
    assert str(all().nbt({'a': 17}, {'b': 'hi there'})) == '@a[nbt={a:17},nbt={b:"hi there"}]'
    assert str(all().nbt({'a': 17}).nbt({'b': 'hi there'})) == '@a[nbt={a:17},nbt={b:"hi there"}]'


def test_target_advancements():
    assert str(all().advancements(
        AdvancementCriteria(Advancement.WAX_ON, True))) == '@a[advancements={husbandry/wax_on=true}]'
    assert str(all().advancements(AdvancementCriteria(Advancement.WAX_ON,
                                                      ('stuff',
                                                       False)))) == '@a[advancements={husbandry/wax_on={stuff=false}}]'


def test_target_predicate():
    assert str(all().predicate('foo')) == '@a[predicate=foo]'
    assert str(all().predicate('foo', 'bar')) == '@a[predicate=foo,predicate=bar]'
    assert str(all().predicate('foo').predicate('bar')) == '@a[predicate=foo,predicate=bar]'


def test_target_chainability():
    assert str(all().pos(1, 2, 3).distance(Range(None, 15.5)).delta(4.4, 5.5, 6.6).scores().tag("one")
        .team('slug').sort(ARBITRARY).limit(15).level(Range(3, 15)).gamemode(SURVIVAL)
        .name('Robin').x_rotation(Range(at=9)).y_rotation(Range(None, 24)).type('cougar')
        .nbt({"hi": "there"}).advancements(AdvancementCriteria(Advancement.A_SEEDY_PLACE, True))
        .predicate(
        "nada")) == '@a[x=1,y=2,z=3,distance=..15.5,dx=4.4,dy=5.5,dz=6.6,scores={},tag=one,team=slug,sort=arbitrary,limit=15,level=3..15,gamemode=survival,name=Robin,x_rotation=9,y_rotation=..24,type=cougar,nbt={hi:there},advancements={husbandry/plant_seed=true},predicate=nada]'
    assert str(all().not_team('Raiders').not_name("GRBX").not_gamemode(CREATIVE)
               .not_types("worm")) == '@a[team=!Raiders,name=!GRBX,gamemode=!creative,type=!worm]'


def test_command_comment():
    long_line = 'This is a long line of text that would be wrapped if it were asked to be wrapped, and we use it to test if wrapping does or does not happen.'
    assert str(comment('hi')) == '# hi\n'
    assert str(comment(' hi ')) == '# hi\n'
    assert str(comment('hi\nthere')) == '# hi\n# there\n'
    assert str(comment('  hi\nthere  ')) == '# hi\n# there\n'
    assert str(comment(long_line)) == '# %s\n' % long_line
    assert str(comment(long_line + '\n\n\n' + long_line)) == '# %s\n#\n#\n# %s\n' % (long_line, long_line)

    assert str(comment('hi')) == '# hi\n'
    assert str(comment(' hi ')) == '# hi\n'
    assert str(comment('hi\nthere')) == '# hi\n# there\n'
    assert str(comment('  hi\nthere  ', wrap=True)) == '# hi there\n'
    assert str(comment(long_line, wrap=True)) == (
        '# This is a long line of text that would be wrapped if it were asked to be\n# wrapped, and we use it to test if wrapping does or does not happen.\n')
    assert str(comment(long_line + '\n\n\n' + long_line, wrap=True)) == (
        '# This is a long line of text that would be wrapped if it were asked to be\n'
        '# wrapped, and we use it to test if wrapping does or does not happen.\n'
        '#\n'
        '# This is a long line of text that would be wrapped if it were asked to be\n'
        '# wrapped, and we use it to test if wrapping does or does not happen.\n')


def test_command_literal():
    assert str(literal('xyzzy')) == 'xyzzy'


def test_command_attribute():
    assert str(attribute(self(), 'foo').get()) == 'attribute @s foo get'


def test_attribute_act():
    assert str(AttributeAct().get()) == 'get'
    assert str(AttributeAct().get(1.2)) == 'get 1.2'
    assert str(AttributeAct().base().get()) == 'base get'
    assert str(AttributeAct().base().get(1.2)) == 'base get 1.2'
    assert str(AttributeAct().base().set(1.2)) == 'base set 1.2'
    assert str(AttributeAct().modifier().add('1-2-3-f', 'robin', 1.3)) == 'modifier add 1-2-3-f "robin" 1.3'
    assert str(AttributeAct().modifier().remove('1-2-3-f')) == 'modifier remove 1-2-3-f'
    assert str(AttributeAct().modifier().value('1-2-3-f')) == 'modifier value get 1-2-3-f'
    assert str(AttributeAct().modifier().value('1-2-3-f', 1.3)) == 'modifier value get 1-2-3-f 1.3'


def test_command_bossbar():
    assert str(bossbar().add('foo', 'stud')) == 'bossbar add foo stud'
    assert str(bossbar().get('foo', 'max')) == 'bossbar get foo max'
    assert str(bossbar().list()) == 'bossbar list'
    assert str(bossbar().remove('foo')) == 'bossbar remove foo'
    assert str(bossbar().set('foo').color(BLUE)) == 'bossbar set foo color blue'
    assert str(bossbar().set('foo').max(17)) == 'bossbar set foo max 17'
    assert str(bossbar().set('foo').name('Freddy')) == 'bossbar set foo name Freddy'
    assert str(bossbar().set('foo').players(self(), entities())) == 'bossbar set foo players @s @e'
    assert str(bossbar().set('foo').style(NOTCHED_12)) == 'bossbar set foo style notched_12'
    assert str(bossbar().set('foo').value(17)) == 'bossbar set foo value 17'
    assert str(bossbar().set('foo').visible(False)) == 'bossbar set foo visible false'


def test_command_clear():
    assert str(clear(self(), User('robin')).item('foo{bar}')) == 'clear @s robin foo{bar}'
    assert str(clear(self(), User('robin')).item('foo{bar}', 4)) == 'clear @s robin foo{bar} 4'


def test_command_clone():
    assert str(clone(1, r(2), d(3), 4, 5, 6, 7, 8, 9).replace()) == 'clone 1 ~2 ^3 4 5 6 7 8 9 replace'
    assert str(clone(1, r(2), d(3), 4, 5, 6, 7, 8, 9).masked(FORCE)) == 'clone 1 ~2 ^3 4 5 6 7 8 9 masked force'
    assert str(clone(1, r(2), d(3), 4, 5, 6, 7, 8, 9).filtered('stone',
                                                               FORCE)) == 'clone 1 ~2 ^3 4 5 6 7 8 9 filtered stone force'


def test_data_target():
    assert str(BlockData(1, r(2), d(3))) == 'block 1 ~2 ^3'
    assert str(EntityData(self())) == 'entity @s'
    assert str(StorageData('m:/a/b')) == 'storage m:/a/b'


def test_command_data():
    assert str(data().get(EntityData(self()))) == 'data get entity @s'


def test_command_effect():
    assert str(effect().give(self(), Effects.SPEED)) == 'effect give @s speed'
    assert str(effect().give(self(), Effects.SPEED, 100)) == 'effect give @s speed 100'
    assert str(effect().give(self(), Effects.SPEED, 100, 2)) == 'effect give @s speed 100 2'
    assert str(effect().give(self(), Effects.SPEED, 100, 2, True)) == 'effect give @s speed 100 2 true'
    assert str(effect().clear()) == 'effect clear'
    assert str(effect().clear(self())) == 'effect clear @s'
    assert str(effect().clear(self(), Effects.SPEED)) == 'effect clear @s speed'
    with pytest.raises(ValueError):
        effect().give(self(), Effects.SPEED, -1)
        effect().give(self(), Effects.SPEED, MAX_EFFECT_SECONDS + 100)
        effect().give(self(), Effects.SPEED, None, 2)
        effect().give(self(), Effects.SPEED, None, None, True)
        effect().give(self(), Effects.SPEED, 100, None, True)
        effect().clear(None, Effects.SPEED)


def test_command_enchant():
    assert enchant(self(), Enchantments.LURE) == 'enchant @s lure'
    assert enchant(self(), Enchantments.LURE, 2) == 'enchant @s lure 2'
    assert enchant(self(), 12) == 'enchant @s 12'
    assert enchant(self(), 12, 2) == 'enchant @s 12 2'
    with pytest.raises(ValueError):
        enchant(self(), Enchantments.LURE, 17)


def test_command_experience():
    assert experience().add(self(), 3, LEVELS) == 'experience add @s 3 levels'
    assert experience().add(self(), 3, POINTS) == 'experience add @s 3 points'
    assert experience().set(self(), 3, LEVELS) == 'experience set @s 3 levels'
    assert experience().set(self(), 3, POINTS) == 'experience set @s 3 points'
    assert experience().query(self(), POINTS) == 'experience query @s points'
    assert xp().query(self(), POINTS) == 'experience query @s points'


def test_command_fill():
    assert str(fill(1, r(2), d(3), 4, 5, 6, 'stone', HOLLOW)) == 'fill 1 ~2 ^3 4 5 6 stone hollow'
    assert str(fill(1, r(2), d(3), 4, 5, 6, 'stone', REPLACE)) == 'fill 1 ~2 ^3 4 5 6 stone replace'
    assert str(
        fill(1, r(2), d(3), 4, 5, 6, 'stone', REPLACE).filter('air')) == 'fill 1 ~2 ^3 4 5 6 stone replace filter air'


def test_data_mod():
    assert str(DataMod().get(EntityData(all()))) == 'get entity @a'
    assert str(DataMod().merge(EntityData(all()), {})) == 'merge entity @a {}'
    assert str(DataMod().modify(EntityData(all()), 'a.b')) == 'modify entity @a a.b'
    assert str(DataMod().modify(EntityData(all()), 'a.b').append().from_(
        StorageData('m:b'))) == 'modify entity @a a.b append from storage m:b'
    assert str(
        DataMod().modify(EntityData(all()), 'a.b').insert(3).value(
            'Pos[0]')) == 'modify entity @a a.b insert 3 value Pos[0]'
    assert str(
        DataMod().modify(EntityData(all()), 'x').merge().value('Pos[0]')) == 'modify entity @a x merge value Pos[0]'
    assert str(
        DataMod().modify(EntityData(all()), 'x').prepend().value('Pos[0]')) == 'modify entity @a x prepend value Pos[0]'
    assert str(
        DataMod().modify(EntityData(all()), 'x').set().value('Pos[0]')) == 'modify entity @a x set value Pos[0]'
    assert str(DataMod().remove(EntityData(all()), 'x')) == 'remove entity @a x'
    with pytest.raises(ValueError):
        DataMod().get(BlockData(1, r(2), d(3)), None, 2.2)


def test_command_datapack():
    assert str(datapack().disable('robin')) == 'datapack disable robin'
    assert str(datapack().enable('robin')) == 'datapack enable robin'
    assert str(datapack().enable('robin', FIRST)) == 'datapack enable robin first'
    assert str(datapack().enable('robin', BEFORE, 'kelly')) == 'datapack enable robin before kelly'
    with pytest.raises(ValueError):
        datapack().enable('robin', BEFORE)


def test_command_forceload():
    assert forceload().add(1, r(2)) == 'forceload add 1 ~2'
    assert forceload().add(1, r(2), 3, 4) == 'forceload add 1 ~2 3 4'
    assert forceload().remove(1, r(2)) == 'forceload remove 1 ~2'
    assert forceload().remove(1, r(2), 3, 4) == 'forceload remove 1 ~2 3 4'
    assert forceload().remove_all() == 'forceload remove all'
    assert forceload().query() == 'forceload query'
    assert forceload().query(1, r(2)) == 'forceload query 1 ~2'
    with pytest.raises(ValueError):
        forceload().add(1, d(2))
        forceload().add(1, r(2.2))
        forceload().add(1, r(2), 3)
        forceload().query(d(2))
        forceload().query(r(2.2))
        forceload().query(1)


def test_command_gamemode():
    assert gamemode(SURVIVAL) == 'gamemode survival'
    assert gamemode(SURVIVAL, self()) == 'gamemode survival @s'


def test_command_gamerule():
    assert gamerule(GameRules.DISABLE_RAIDS) == 'gamerule disableRaids'
    assert gamerule(GameRules.DISABLE_RAIDS, True) == 'gamerule disableRaids true'
    assert gamerule(GameRules.MAX_COMMAND_CHAIN_LENGTH, 13) == 'gamerule maxCommandChainLength 13'
    with pytest.raises(ValueError):
        gamerule(GameRules.DISABLE_RAIDS, 17)
        gamerule(GameRules.MAX_COMMAND_CHAIN_LENGTH, True)


def test_command_give():
    assert give(self(), 'foo') == 'give @s foo'
    assert give(self(), 'foo', 17) == 'give @s foo 17'


def test_command_help():
    assert help() == 'help'
    assert help('foo') == 'help foo'


def test_command_item():
    assert str(item().modify().block(1, r(2), d(3), 17)) == 'item modify block 1 ~2 ^3 17'
    assert str(item().modify().block(1, r(2), d(3), 17, 'm:a')) == 'item modify block 1 ~2 ^3 17 m:a'
    assert str(item().modify().entity(self(), 17)) == 'item modify entity @s 17'
    assert str(item().modify().entity(self(), 17, 'm:a')) == 'item modify entity @s 17 m:a'
    assert str(item().replace().entity(self(), 17).with_('a{b}')) == 'item replace entity @s 17 with a{b}'
    assert str(item().replace().entity(self(), 17).with_('a{b}', 2)) == 'item replace entity @s 17 with a{b} 2'
    assert str(
        item().replace().entity(self(), 17).from_().block(1, r(2), d(3),
                                                          17)) == 'item replace entity @s 17 from block 1 ~2 ^3 17'
    assert str(
        item().replace().entity(self(), 17).from_().block(1, r(2), d(3), 17,
                                                          'm:a')) == 'item replace entity @s 17 from block 1 ~2 ^3 17 m:a'
    assert str(
        item().replace().entity(self(), 17).from_().entity(player(),
                                                           17)) == 'item replace entity @s 17 from entity @p 17'
    assert str(
        item().replace().entity(self(), 17).from_().entity(player(),
                                                           17,
                                                           'm:a')) == 'item replace entity @s 17 from entity @p 17 m:a'
    with pytest.raises(ValueError):
        item().replace().block(1, r(2), d(3), 17, 'm:a')
        item().replace().entity(self(), 17, 'm:a')


def test_simple_commands():
    assert (defaultgamemode(SURVIVAL)) == 'defaultgamemode survival'
    assert (deop(self(), all())) == 'deop @s @a'
    assert (difficulty(PEACEFUL)) == 'difficulty peaceful'
    assert (function('m:b/c')) == 'function m:b/c'


def test_resource_checks():
    assert good_resource('xyzzy') == 'xyzzy'
    assert good_resource('m:xyzzy') == 'm:xyzzy'
    assert good_resource_path('xyzzy') == 'xyzzy'
    assert good_resource_path('m:xyzzy') == 'm:xyzzy'
    assert good_resource_path('a/b/c') == 'a/b/c'
    assert good_resource_path('/a/b/c') == '/a/b/c'
    assert good_resource_path('m:a/b/c') == 'm:a/b/c'
    assert good_resource_path('m:/a/b/c') == 'm:/a/b/c'
    with pytest.raises(ValueError):
        good_resource('%')
        good_resource('m:xyzzy', allow_namespace=False)
        good_resource_path('/')
        good_resource_path('a//b')
        good_resource_path('/a/b:c')
        good_resource_path('//a/b/c')


def test_tag_checks():
    assert good_name('xyzzy') == 'xyzzy'
    assert good_name('a+b') == 'a+b'
    assert good_name('!a+b', allow_not=True) == '!a+b'
    assert good_names('_', 'b-3') == ('_', 'b-3')
    assert good_names('_', '!b-3', allow_not=True) == ('_', '!b-3')
    with pytest.raises(ValueError):
        good_name('x&y')
        good_name('!foo')
        good_names('_', '!b-3')
