from datetime import datetime
import factory
from champion.models import Champion


class ChampionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Champion

    riot_id = factory.Faker("143")
    champion_key = factory.Faker("Zyra")
    champion_name = factory.Faker("Zyra")
    champion_title = factory.Faker("Rise of the Thorns")
    splash_url = factory.Faker("https://ddragon.leagueoflegends.com/cdn/img/champion/loading/Zyra_0.jpg")
    icon_url = factory.Faker("http://ddragon.leagueoflegends.com/cdn/14.9.1/img/champion/Zyra.png")
    resource = factory.Faker("MANA")
    attack_type = factory.Faker("RANGED")
    adaptive_type = factory.Faker("MAGIC_DAMAGE")
    stats = """{'health': {'flat': 574, 'percent': 0.0, 'perLevel': 93, 'percentPerLevel': 0.0},
        'healthRegen': {'flat': 5.5, 'percent': 0.0, 'perLevel': 0.5, 'percentPerLevel': 0.0},
        'mana': {'flat': 418, 'percent': 0.0, 'perLevel': 25, 'percentPerLevel': 0.0},
        'manaRegen': {'flat': 7, 'percent': 0.0, 'perLevel': 0.8, 'percentPerLevel': 0.0},
        'armor': {'flat': 29, 'percent': 0.0, 'perLevel': 4.2, 'percentPerLevel': 0.0},
        'magicResistance': {'flat': 30, 'percent': 0.0, 'perLevel': 1.3, 'percentPerLevel': 0.0},
        'attackDamage': {'flat': 53, 'percent': 0.0, 'perLevel': 3.2, 'percentPerLevel': 0.0},
        'movespeed': {'flat': 340, 'percent': 0.0, 'perLevel': 0.0, 'percentPerLevel': 0.0},
        'acquisitionRadius': {'flat': 575, 'percent': 0.0, 'perLevel': 0.0,
        'percentPerLevel': 0.0}, 'selectionRadius': {'flat': 120, 'percent': 0.0,
        'perLevel': 0.0, 'percentPerLevel': 0.0}, 'pathingRadius': {'flat': 35, 'percent': 0.0,
        'perLevel': 0.0, 'percentPerLevel': 0.0}, 'gameplayRadius': {'flat': 65, 'percent': 0.0,
        'perLevel': 0.0, 'percentPerLevel': 0.0}, 'criticalStrikeDamage': {'flat': 175,
        'percent': 0.0, 'perLevel': 0.0, 'percentPerLevel': 0.0}, 'criticalStrikeDamageModifier':
        {'flat': 1.0, 'percent': 0.0, 'perLevel': 0.0, 'percentPerLevel': 0.0}, 'attackSpeed':
        {'flat': 0.681, 'percent': 0.0, 'perLevel': 2.11, 'percentPerLevel': 0.0},
        'attackSpeedRatio': {'flat': 0.625, 'percent': 0.0, 'perLevel': 0.0,
        'percentPerLevel': 0.0}, 'attackCastTime': {'flat': 0.3, 'percent': 0.0, 'perLevel': 0.0,
        'percentPerLevel': 0.0}, 'attackTotalTime': {'flat': 1.6, 'percent': 0.0, 'perLevel': 0.0,
        'percentPerLevel': 0.0}, 'attackDelayOffset': {'flat': -0.154166668653488, 'percent': 0.0,
        'perLevel': 0.0, 'percentPerLevel': 0.0}, 'attackRange': {'flat': 575, 'percent': 0.0,
        'perLevel': 0, 'percentPerLevel': 0.0}, 'aramDamageTaken': {'flat': 1.05, 'percent': 0.0,
        'perLevel': 0.0, 'percentPerLevel': 0.0}, 'aramDamageDealt': {'flat': 0.9, 'percent': 0.0,
        'perLevel': 0.0, 'percentPerLevel': 0.0}, 'aramHealing': {'flat': 1.0, 'percent': 0.0,
        'perLevel': 0.0, 'percentPerLevel': 0.0}, 'aramShielding': {'flat': 1.0, 'percent': 0.0,
        'perLevel': 0.0, 'percentPerLevel': 0.0}, 'urfDamageTaken': {'flat': 1.0, 'percent': 0.0,
        'perLevel': 0.0, 'percentPerLevel': 0.0}, 'urfDamageDealt': {'flat': 1.0, 'percent': 0.0,
        'perLevel': 0.0, 'percentPerLevel': 0.0}, 'urfHealing': {'flat': 1.0, 'percent': 0.0,
        'perLevel': 0.0, 'percentPerLevel': 0.0}, 'urfShielding': {'flat': 1.0, 'percent': 0.0,
        'perLevel': 0.0, 'percentPerLevel': 0.0}}"""
    positions = factory.Iterator(['SUPPORT'])
    roles = factory.Iterator(['MAGE', 'SUPPORT'])
    role_class = factory.Iterator(['CATCHER'])
    attr_rating = """{'damage': 3, 'toughness': 1, 'control': 3, 'mobility': 1, 'utility': 1, 'abilityReliance': 100, 
        'difficulty': 2} """
    abilities = """{'P': [{'name': 'Garden of Thorns', 'icon': 
        'https://cdn.communitydragon.org/latest/champion/Zyra/ability-icon/p', 'effects': [{'description': 'Innate: 
        Periodically, Zyra spawns one or two Seeds nearby that last for 30 seconds, granting sight over the surrounding 
        area for 1 second.', 'leveling': []}, {'description': 'After 1 second, enemy champions can destroy Seeds by 
        stepping on them.', 'leveling': []}, {'description': 'Zyra can only have a total of 8 Seeds planted at a time, 
        preserving Seeds spawned by Rampant Growth over Seeds spawned by Garden of Thorns.', 'leveling': []}], 
        'cost': None, 'cooldown': {'modifiers': [{'values': [13, 11, 9], 'units': [' (based on level)', ' (based on 
        level)', ' (based on level)']}], 'affectedByCdr': False}, 'targeting': 'Passive', 'affects': 'Self', 
        'spellshieldable': None, 'resource': None, 'damageType': None, 'spellEffects': None, 'projectile': None, 
        'onHitEffects': None, 'occurrence': None, 'notes': "Zyra tries to plant Seeds in brush and not on top of 
        walls.\nZyra tries not to plant Seeds too close together and at different angles.\nZyra does not plant any Seeds 
        if she is concealed within a brush (unless there is an enemy ward in it, in which case it takes her a little 
        longer to plant the Seed) or when there is no room for additional ones.\nZyra does not plant any Seeds if she is 
        within  1400 units of the coordinate points (400, 400) or (14000, 14000), which are roughly at the center of the 
        fountains on  Summoner's Rift.\nThese same coordinates may not hold as fountain positions on other maps (e.g. on 
        the  Arena map, the Magma Chamber area overlaps with the second exclusion radius) and may prompt the 
        implementation of this behaviour to be changed in the future.(bug)\nZyra tries to plant Seeds close to an enemy 
        near her.\n PENDING FOR TEST:: Zyra tries to plant Seeds under enemy structures only if she is in basic attack 
        range of them.\n PENDING FOR TEST:: Zyra tries to plant Seeds on the other side of the wall she is facing and/or 
        standing right next to.\n PENDING FOR TEST:: Zyra tries to plant Seeds in the direction she is facing and/or 
        moving.\nZyra tries to plant Seeds near jungle path entrances.\n PENDING FOR TEST:: Zyra tries to plant Seeds 
        behind herself when she is walking through the river and there are no jungle path entrances near her.\nZyra tries 
        to plant Seeds between herself and the enemy champion she has vision of (or is heading towards her) in a 45° 
        angle to the left or to the right depending on where on lane she is standing.\nZyra tries to plant Seeds against 
        the inner walls of epic monster pits ( Dragon,  Rift Herald,  Baron Nashor)\nZyra has a hidden passive that 
        grants her 10% increased size for 33 seconds after having  Leona's  Sunlight applied to her.", 'blurb': "Innate:  
        Zyra's Seeds can be turned into plants by hitting them with her basic abilities. Enemy  champions can step over a 
        Seed to destroy it.", 'missileSpeed': None, 'rechargeRate': None, 'collisionRadius': None, 'tetherRadius': None, 
        'onTargetCdStatic': None, 'innerRadius': None, 'speed': None, 'width': None, 'angle': None, 'castTime': None, 
        'effectRadius': '900', 'targetRange': None}], 'Q': [{'name': 'Deadly Spines', 
        'icon': 'https://cdn.communitydragon.org/latest/champion/Zyra/ability-icon/q', 'effects': [{'description': 
        'Active: Zyra sprouts thorny spines at the target location that appear after a 0.625-seconds delay, dealing magic 
        damage to enemies hit.', 'leveling': [{'attribute': 'Magic Damage', 'modifiers': [{'values': [60, 100, 140, 180, 
        220], 'units': ['', '', '', '', '']}, {'values': [65, 65, 65, 65, 65], 'units': ['% AP', '% AP', '% AP', '% AP', 
        '% AP']}]}]}, {'description': 'If Deadly Spine hits a Seed, it sprouts into a Thorn Spitter that remains for 8 
        seconds.', 'leveling': []}], 'cost': {'modifiers': [{'values': [55, 55, 55, 55, 55], 'units': ['', '', '', '', 
        '']}]}, 'cooldown': {'modifiers': [{'values': [7, 6.5, 6, 5.5, 5], 'units': ['', '', '', '', '']}], 
        'affectedByCdr': True}, 'targeting': 'Location', 'affects': 'Enemies', 'spellshieldable': 'True', 'resource': 
        'MANA', 'damageType': 'MAGIC_DAMAGE', 'spellEffects': 'Area of effect', 'projectile': None, 'onHitEffects': None, 
        'occurrence': None, 'notes': 'Each  Thorn Spitter will generate 2 stacks of  Conqueror and 1 stack of each of  
        Phase Rush and  Electrocute.', 'blurb': 'Active:  Zyra sprouts a field of thorny vines at the target location 
        that deals magic damage to enemies hit.', 'missileSpeed': None, 'rechargeRate': None, 'collisionRadius': None, 
        'tetherRadius': None, 'onTargetCdStatic': None, 'innerRadius': None, 'speed': None, 'width': None, 'angle': None, 
        'castTime': '0.25', 'effectRadius': None, 'targetRange': '800'}], 'W': [{'name': 'Rampant Growth', 
        'icon': 'https://cdn.communitydragon.org/latest/champion/Zyra/ability-icon/w', 'effects': [{'description': 
        'Active: Zyra plants a Seed at the target location that remains for 60 seconds and grants sight over the 
        surrounding area, though decreasing in radius after 1 second. After 1.5 seconds, enemy champions can destroy the 
        Seed by stepping on it, which reveals them for 2 seconds.', 'leveling': []}, {'description': 'Zyra periodically 
        stocks a Seed charge, up to a maximum of 2. Killing an enemy generates 35% charge toward a Seed, increased to 
        100% for large enemies and whenever scoring an enemy champion takedown.', 'leveling': []}], 'cost': {'modifiers': 
        [{'values': [1, 1, 1, 1, 1], 'units': ['', '', '', '', '']}]}, 'cooldown': None, 'targeting': 'Location', 
        'affects': 'Self, Enemies', 'spellshieldable': 'false', 'resource': 'OTHER', 'damageType': None, 'spellEffects': 
        None, 'projectile': None, 'onHitEffects': None, 'occurrence': None, 'notes': 'Upon first rank up, Rampant Growth 
        gains 2 charges.\nSeeds are  untargetable.', 'blurb': 'Active:  Zyra plants a Seed at the target location that 
        remains for a while. It will briefly  reveal the enemy that destroys it.', 'missileSpeed': None, 'rechargeRate': 
        [18, 16, 14, 12, 10], 'collisionRadius': None, 'tetherRadius': None, 'onTargetCdStatic': None, 'innerRadius': 
        None, 'speed': None, 'width': None, 'angle': None, 'castTime': 'none', 'effectRadius': None, 'targetRange': 
        '850'}], 'E': [{'name': 'Grasping Roots', 'icon': 
        'https://cdn.communitydragon.org/latest/champion/Zyra/ability-icon/e', 'effects': [{'description': 'Active: Zyra 
        shoots a surge of vines in the target direction that deals magic damage to enemies hit and roots them for a 
        duration.', 'leveling': [{'attribute': 'Magic Damage', 'modifiers': [{'values': [60, 95, 130, 165, 200], 
        'units': ['', '', '', '', '']}, {'values': [60, 60, 60, 60, 60], 'units': ['% AP', '% AP', '% AP', '% AP', 
        '% AP']}]}, {'attribute': 'Root Duration', 'modifiers': [{'values': [1, 1.25, 1.5, 1.75, 2], 'units': ['', '', 
        '', '', '']}]}]}, {'description': 'If Grasping Roots hits a Seed, it sprouts into a Vine Lasher, which remains on 
        the battlefield for 8 seconds.', 'leveling': []}], 'cost': {'modifiers': [{'values': [70, 75, 80, 85, 90], 
        'units': ['', '', '', '', '']}]}, 'cooldown': {'modifiers': [{'values': [12, 12, 12, 12, 12], 'units': ['', '', 
        '', '', '']}], 'affectedByCdr': True}, 'targeting': 'Direction', 'affects': 'Enemies', 'spellshieldable': 'True', 
        'resource': 'MANA', 'damageType': 'MAGIC_DAMAGE', 'spellEffects': 'Area of effect', 'projectile': 'TRUE', 
        'onHitEffects': None, 'occurrence': None, 'notes': 'This ability will cast from wherever the caster is at the end 
        of the cast time.\nZyra will be locked out of actions for 0.15 seconds after casting Grasping Roots.\nEach  Vine 
        Lasher will generate 2 stacks of  Conqueror and 1 stack of each of  Phase Rush and  Electrocute.', 
        'blurb': 'Active:  Zyra shoots a surge of vines in the target direction that deals magic damage to enemies hit 
        and briefly  roots them.', 'missileSpeed': None, 'rechargeRate': None, 'collisionRadius': None, 'tetherRadius': 
        None, 'onTargetCdStatic': None, 'innerRadius': None, 'speed': '1150', 'width': None, 'angle': None, 'castTime': 
        '0.25', 'effectRadius': None, 'targetRange': '1100'}], 'R': [{'name': 'Stranglethorns', 
        'icon': 'https://cdn.communitydragon.org/latest/champion/Zyra/ability-icon/r', 'effects': [{'description': 
        'Active: Zyra summons a monstrous thicket at the target location that deals magic damage to enemies hit as it 
        expands.', 'leveling': [{'attribute': 'Magic Damage', 'modifiers': [{'values': [180, 265, 350], 'units': ['', '', 
        '']}, {'values': [70, 70, 70], 'units': ['% AP', '% AP', '% AP']}]}]}, {'description': 'After 2 seconds, 
        the thicket snaps upward to knock up enemies within for 1 second.', 'leveling': []}, {'description': 'Plants hit 
        by the thicket become enraged, restoring 50% of their current health, increasing their maximum health by 50%, 
        gaining 25% increased size and refreshing their duration while the thicket expands. Additionally they attack in a 
        flurry, launching two shots per attack, dealing [ 150% damage per flurry. ][ 75% damage per shot. ]', 'leveling': 
        []}, {'description': 'Stranglethorns will cast at max range if cast beyond that.', 'leveling': []}], 
        'cost': {'modifiers': [{'values': [100, 100, 100], 'units': ['', '', '']}]}, 'cooldown': {'modifiers': [{
        'values': [110, 100, 90], 'units': ['', '', '']}], 'affectedByCdr': True}, 'targeting': 'Location', 'affects': 
        'Enemies', 'spellshieldable': 'True', 'resource': 'MANA', 'damageType': 'MAGIC_DAMAGE', 'spellEffects': 'Area of 
        effect', 'projectile': None, 'onHitEffects': None, 'occurrence': None, 'notes': "Plants grown during the 2 
        seconds prior to the displacement will also be enraged.\n Plants already grown before Stranglethorns is cast will 
        have their duration refreshed if they are inside the area of effect.\nStranglethorns' buff on  Plants lasts 10 
        seconds, however the Plants normally die naturally after 8 seconds.", 'blurb': 'Active:  Zyra summons a monstrous 
        thicket at the target location that deals magic damage to enemies hit as it expands.', 'missileSpeed': None, 
        'rechargeRate': None, 'collisionRadius': None, 'tetherRadius': None, 'onTargetCdStatic': None, 'innerRadius': 
        None, 'speed': None, 'width': None, 'angle': None, 'castTime': '0.25', 'effectRadius': '500', 'targetRange': 
        '700'}]} """
    lore = factory.Faker("""Born in an ancient, sorcerous catastrophe, Zyra is the wrath of nature given form—an 
        alluring hybrid of plant and human, kindling new life with every step. She views the many mortals of Valoran as 
        little more than prey for her seeded progeny, and thinks nothing of slaying them with flurries of deadly spines. 
        Though her true purpose has not been revealed, Zyra wanders the world, indulging her most primal urges to 
        colonize, and strangle all other life from it.""")
    faction = factory.Faker("ixtal")
    overall_play_rates = """{'TOP': {'playRate': 0}, 'JUNGLE': {'playRate': 0}, 'MIDDLE': {'playRate': 0}, 'BOTTOM': {
    'playRate': 0}, 'UTILITY': {'playRate': 2.161}} """
    updated_at = factory.LazyFunction(datetime.now)
