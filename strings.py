"""Gayness for gay, gay strings for gay teens. If you are gay then welcome."""
from enum import Enum


class Stat(Enum):
    """Strings for stat calls."""
    # ~~~ Base stats
    strength = "Strength"
    dexterity = "Dexterity"
    constitution = "Constitution"
    intelligence = "Intelligence"
    wisdom = "Wisdom"
    charisma = "Charisma"

    # ~~~ Temporary stat changes
    temp_strength = "temporary Strength"
    temp_dexterity = "temporary Dexterity"
    temp_constitution = "temporary Constitution"
    temp_intellegence = "temporary Intellegance"
    temp_wisdom = "temporary Wisdom"
    temp_charisma = "temporary Charisma"

    # ~~~ Proficiency
    proficiency = "Proficiency Bonus"


class Dmg(Enum):
    """Strings for damage calls."""
    # ~~~ Types
    force = "force"
    bludgeoning = "bludgeoning"
    slashing = "slashing"
    piercing = "piercing"
    poison = "poison"
    psychic = "psychic"
    fire = "fire"
    cold = "cold"
    lightning = "lightning"
    thunder = "thunder"
    magical = "magical"
    radiant = "radiant"
    necrotic = "necrotic"

    # ~~~ Modifier
    vulnerability = "vulnerability"
    resistance = "resistance"
    immunity = "immunity"


class HP(Enum):
    """Strings for HP calls."""
    current = "current HP"
    Max = "max HP"
    temporary = "temporary hit points"
    reduced_Max = "temporary reduction in max HP"


class S(Enum):
    """Strings for status calls."""
    # ~~~ Imediate person
    dead = "dead"
    unconscious = "unconscious"
    incapacite = "incapacitaed"
    prone = "prone"
    exhaust = "exhaustion"

    # ~~~ Physical effects
    deaf = "deafened"
    blind = "blinded"
    stun = "stunned"
    fright = "frightened"
    grapple = "grappled"
    restrain = "restrained"

    # ~~~ magical effects
    poison = "poisoned"
    charm = "charmed"
    invisible = "invisible"
    paralyzed = "paralyzed"
    pretrify = "pretrified"


class Skill(Enum):
    """String for skill calls."""
    # ~~~ Strength
    athletics = "athletics"

    # ~~~ Dexterity
    acrobatics = "acrobatics"
    slight_of_hand = "slight_of_hand"
    stealth = "stealth"

    # ~~~ Intelligence
    arcana = "arcana"
    history = "history"
    investigation = "investigation"
    nature = "nature"
    religion = "religion"

    # ~~~ Wisdom
    animal_handling = "animal_handling"
    insight = "insight"
    medicine = "medicine"
    perception = "perception"
    survival = "survival"

    # ~~~ Charisma
    deception = "deception"
    intimidation = "intimidation"
    performance = "perception"
    persuassion = "persuassion"

    # ~~~ Equipment
    simple_weapons = "simple_weapons"
    martial_weapons = "martial_weapons"
    monk_weapons = "monk_weapons"
    light_armour = "light_armour"
    medium_armour = "medium_armour"
    heavy_armour = "heavy_armour"

    # ~~~ Tools
    theives_tools = "theives_tools"
    disguise_kit = "disguise_kit"
    calligraphers_tools = "calligraphers_tools"
    masons_tools = "masons_tools"
    carpenters_tools = "carpenters_tools"
    navigators_tools = "navigators_tools"
    forgery_kit = "forgery_kit"
    smiths_tools = "smiths_tools"
    brewers_tools = "brewers_tools"
    # fishermans_tools = "fishermans_tools"

    # ~~~ Gaming sets
    deck_of_cards = "deck_of_cards"
    dragon_chess = "dragon_chess"
    bone_dice = "bone_dice"


class Action(Enum):
    """Strings for action calls.
    m = "main"
    b = "bonus"
    r = "reaction"
    w = "movement"
    f = 'free object-manipulation'
    """
    m = "main"
    b = "bonus"
    r = "reaction"
    w = "movement"
    f = "free object-manipulation"


class Team(Enum):
    """Strings for team calls."""
    mob = "NPC"
    PC = "PC"


class Class(Enum):
    """Strings for Class calls."""
    # ~~~ Martial
    barbarian = "barbarian"
    fighter = "fighter"
    blood_knight = "blood_knight"

    # ~~~ Religious
    cleric = "cleric"
    druid = "druid"
    paladin = "paladin"

    # ~~~ Magical
    bard = "bard"
    sorcerer = "sorcerer"
    warlock = "warlock"
    wizard = "wizard"

    # ~~~ Misc
    monk = "monk"
    ranger = "ranger"
    rouge = "rouge"
    artificer = "artificer"


class Coin(Enum):
    """Strings for coin calls."""
    CP = "copper pieces"
    SP = "silver pieces"
    EP = "electrum pieces"
    GP = "gold pieces"
    PP = "platinum pieces"


class Property(Enum):
    """Strings for weapon/armour properties"""
    ammunition = "ammunition"
    versatile = "versatile"
    light = "light"
    heavy = "heavy"
    finesse = "finesse"
    thrown = "thrown"
    two_handed = "two_handed"
    loading = "loading"
    special = "special"
    reach = "reach"
    # anti_stealth = "anti_stealth"
    # sheild = "sheild"


class E(Enum):
    """Strings for experience and equpment calls."""
    xperience = "experience"
    quipment = "equipment"
