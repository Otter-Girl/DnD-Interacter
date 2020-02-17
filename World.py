""" A world simulating module
    Simulate a simplified world for use by a DM!
    Is like if someone cuts up some rope and uses it to tie someone up, most likely they're going to forget that. But I will also forget that, and slowing down the game to ask everyone all the time "Hey, do you pick back up X, and what about Y?" is really silly. Ideally I'll keep track of LITTERALLY everything, or the players will self-poliece, but even with the amount of good maners we have at our table that's not always followed. Computers however, they do not forget, the never forget. And instead of trawling through paper notes and writing everything down furiously myself: data and updating data is at a touch of the button, as long as I know the syntax."""

from random import randint
import datetime
import pickle
#eventually implement pathlib would be nice, esspecially for back-end stuff.


class World(object):
    """ This is the world for your world
        Contains the time and weather and allows action on them accordingly"""

    version = '0.1'

    def __init__(self, name, time=0, weather="fair", party={}, save_file_location=''):
        self.name = name # Required for comparison with combat encounters
        self.time = int(time)  # This is the time in your world.
        self.weather = str(weather)  # This is the weather in your world.
        self.party = {} # Create a set-type object for party memeber to attach onto.
        self.add_party = party # Required as it links the target party memebers to this world instance.
        self.combat = None # should be None by default
        self.save_file_location = save_file_location

    def __str__(self):
        return 'The time is ' + str(
            datetime.datetime.utcfromtimestamp(self.time)) + '\nThe weather is looking rather ' + self.weather

    # ~~~ World phenomena
    def time_skip(self, skip):
        """" progress time by any amount in seconds. Returns an update time and prints a converted time."""
        self.time += skip
        self.check_status()

    def change_weather(self, skip):
        # Will write a weather randomizer later
        pass

    def see(self, skip=0):
        """ see the target world, or skip time and run the world"""
        self.time_skip(skip)
        self.change_weather(skip)
        print(self)

    # ~~~ In-world objects
    def add_party(self, party_members):
        for PC in party_members: PC.world = self
        self.party.add(party_members)

    def move_party(self, party_members, target_world):
        """Programatically move party members from from world to another"""
        target_world.add_party(party_members)
        self.party.remove(party_members)

    def put_in(self, targets):
        for objects in targets: objects.world = self
        self.objects.add(targets)

    # ~~~ Administrative
    def save(self):
        """Save a world."""
        pickle_file = open(self.save_file_location + '.pickle','wb') # Consider using pathlib instead.
        pickle.dump(self, pickle_file)
        pickle_file.close()

    @staticmethod
    def world_load(name):
        """Load a world."""
        pickle_file = open(name, 'wb')
        world = pickle.load(pickle_file)
        pickle_file.close()
        return world


         

class Combat:
    """ Run an instance of combat in a world.
    Need to imput a list of Mob class objects, sorry I havn't figured this one out very well yet. :("""
       

    def __init__(self, world, mobs, chars=None):

        # ~~~ Set up the combat variables between the world and combat
        self.world, world.combat = world, self # combat and the world exchange variables
        self.name = world.name # Confirm idential names
        self.mobs = mobs

        # ~~~ Handle initiative (and exchange variables between combat and characters)
        if chars:   # Initiative given by party
            all_list = [char.initiative() for char in mobs] + [char for char in chars] 
        else:       # Initative generated
            self.party = world.party
            all_list = [char.initiative() for char in mobs + self.party] 
        self.initiative = all_list.sort(key = lambda Character: Character.initiative) # Find innitiative order
        self.who_turn = self.initiative[0] # Set the current who's turn it is
        for char in self.initiative:    # Main action is unique due to the existance of 'multiattack'
            char.combat = self          # Exchnge variables with combat
            char.actions = {Action.m: 1, Action.b: 0, Action.r: 0, Action.f: 0, Action.w: char.speed[Action.w]} # See help(Action)
        
        # ~~~ Finalisation
        self.round = 1 # Set the round; redundant but usefull if a player asks how many rounds it's been
        self.reward = {Coin.CP:0, Coin.SP:0, Coin.EP:0, Coin.GP:0, Coin.PP:0, E.xperience:0, E.quipment:{}}

    def new_round(self):
        """Initiates a new round in-world and resets variables accordingly"""

        self.world.time_skip(6)
        self.round += 1
        for char in self.initiative:
            if char == 0:                    # As characters die their place in initiative becomes 0, this prevents turn-order issues. 
                self.initiative.remove(char) # Handle redundant space, is only called if indeed the character has died.
                continue
            char.actions = {Action.m: 1, Action.b: 0, Action.r: 0, Action.f: 0, Action.w: char.speed[Action.w]} # See help(Action)
        self.who_turn = self.initiative[0]

    def new_turn(self):
        """Cycles through initiative order and handles exhausting the list as a new round."""

        try:
            self.who_turn = self.initiative[self.initiative.index[self.who_turn] + 1]
        except IndexError as e:
            self.new_round()
        else:
            if not self.who_turn: self.new_turn() # Handles character death as skipping the dead charachter's turn

    def add_loot(self,loot_to_add):
        """Add loot to the pile!"""

        try:
            for loot in loot_to_add: self.reward[loot] += loot
        except TypeError as e:
            if loot_to_add[E.quipment]: self.reward[E.quipment].add(loot_to_add[E.quipment])
            else: raise e

    def dead_char(self, character):
        """A character has died, adjust the combat variable and then check to see if combat is over."""

        self.initiative[self.initiative.index[character]] = 0

    def end_combat(self):
        """'End' combat, drop loot, clean-up states and dependancies and then kamakazi self. :'("""

        self.world.combat = None
        for char in self.party: self.party.combat = None
        print(self.reward)
        del self    



class Character:
    """The base character class, included also in this class are the PC and Mob sub-classes."""

    version = '0.1'

    def __init__(self, name, level=None, equipment=None, HP=None, stat_block=None, saving_throws={}, skills={}, speed=30):
        """Create the character, importing them if they are a Mob or creating a PC or so-called 'static' character, such as a door."""
        
        # ~~~ Checks
        if stat_block is None: stat_block = [10, 10, 10, 10, 10, 10]
        if level is None and not HP and not self.team == Team.mob: raise Exception("Please provide some basic info you fucking clout.")  # Falsy HP is used incase amount entered is 0
        if level is None: level = 0

        # ~~~ Getting
        if self.team == Team.mob:
            if True:    # Statement to check if mob is in data base
                pickle_file = open(name, 'wb')
                mob = pickle.load(pickle_file)
                pickle_file.close()
            else:
                import_mob(name)
        else:
            stat_block = parse_stats(stat_block)
        stat_block.proficiency = l_table(level, Skill.Proficiency, self.team)

        # ~~~ Setting
        self.name = name
        self.HP = {HP.Max: HP, HP.current: HP, HP.temporary: 0, HP.reduced_Max: 0}
        self.level = level
        self.stat = stat_block
        self.skills = skills
        self.speed = speed
        self.equipment = equipment
        self.experience = experience
        self.actions = '' # Perhaps actions and spells can be their own function domain? Makes the storing of data easier for charachters.
        self.spells = ''
        self.conditions = {} # Perhaps conditions are a class, allowing info such as release conditions, dc and time requirements. 
        # Seperate classes for each condition seems reasonable, they are all functional with considerable differences.
        # Counter-point, a 'status' class with condition-specific subclasses allows unversal functionaltiy between statuses (time, DC) while still
        # Maintaining an identity.


    @staticmethod   # Easily could be in init, is only called once per charachter creation. However this moves a load of BS out of 
                    # init making it more readable. Pick your posion.
    def parse_stats(stat_block):
        try:
            temporary_variable_name =   {
                                        Stat.strength: s_table(stat_block[0]), 
                                        Stat.dexterity: s_table(stat_block[1]),
                                        Stat.constitution: s_table(Stat_block[2]), 
                                        Stat.intelligence: s_table(stat_block[3]),
                                        Stat.wisdom: s_table(stat_block[4]), 
                                        Stat.charisma: s_table(stat_block[5]),
                                        Stat.proficiency: None
                                        "Values": stat_block
                                        }

        except IndexError as e:
            raise e

    def initiative(self):
        """Character initiative, called at the start of combat, indicated their 'readiness' for combat and turn order."""
        initiative = randint(1, 20) + self.stat[Stat.dexterity] #+ other modifiers I'm sure there's some out there stupid PHB being so dense
        return initiative

    def damage(self, amount=None, dmg_type=Dmg.bludgeoning):
        """Applies damage to the character, reducing their current HP. Calculated the amount to be applied based on the
        rolled damage and any immunities, reductions or vulnerabilities the character might have."""

        if amount is None: amount = self.stat[Stat.strength]

        # ~~~ Calculation
        if dmg_type == Dmg.immunity: # Needs to be handled differently
            amount = 0
            print(self.name, "is immune to", dmg_type, "damage!")
            pass
        if Stat.saving_throws: pass # perhaps handle ST seperately, how to handle ST with various outcomes?
        if dmg_type == Dmg.resistance: amount = amount / 2
        if dmg_type == Dmg.vulnerability: amount = amount * 2

        # ~~~ Application
        hp = self.HP[HP.current]
        temp = self.HP[HP.temporary]
        if temp:
            temp = temp - amount
            if temp < 0:
                amount = abs(temp)
                temp = 0
        hp = hp - amount

        # ~~~ Clean-up
        if hp <= 0:
            self.HP[HP.current] = 0
            self.down()
        else:
            print(self.name, "just took", amount, dmg_type, "damage and has", hp + temp, "HP remaining.")
            self.bloodied()
        self.HP[HP.current] = hp

    def bloodied(self):
        """Tell you how bloodied this character is (if at all)."""
        # Consider storing redundant data to raise a flag if 'bloodied' statement has already been made about character.
        # (should also consider when the function is being called directly.)

        if self.HP[HP.current] < 2 * self.HP[HP.Max] / 8 or self.HP[HP.current] < 2:
            print(self.name, "is on the brink of death!")
        elif self.HP[HP.current] < 2 * self.HP[HP.Max] / 4:
            print(self.name, "is VERY bloodied.")
        elif self.HP[HP.current] < 2 * self.HP[HP.Max] / 2:
            print(self.name, "is bloodied.")
        elif __name__ == "__main__" and self.HP[HP.current] > self.HP[HP.Max] / 2:
            print(self.name, "is not bloodied.")

    def attack(self, target, weapon):
        """Attack a fool."""

        # ~~~ Checkies
        try:
            AC = target.AC # Add to a temporary variable, unnecessary but conveniently raises NameError if target doesn't exist.
            if self.equiped.count(weapon): weapon = self.equipment[weapon] # Add an equipped weapon's statistics to a temporary variable
            elif self.equipment[weapon]: # Check is the character actually HAS the required item. Raises a KeyError if they don't.
                a = input("is not equipped, equip it? [y/n] ")
                if a =='y':
                    self.equip(weapon)
                    self.attack(target, weapon) # Equip the weapon, using free-om action, restart attack in a new instance and then pass the current one after resuloution.
                return
        except NameError: # I gotta ask other programmers, do you think this should be two different try blocks? Errors refer to entirely different lines of code in the try block.
            a = input("Target does not to exist, create one? [y/n] ")
            # recieve the input, either exit, create a new character, or attempt another input given a fault input.
            #   If a = "yes"
            #       target = Character("target")
            #       self.attack(target, weapon)
            #       return
        except KeyError:
            print("Doesn't have", weapon, ".")
            return
        #Perhaps something to check range later on, but that's complicated and requires a map. Also then disadvantage becomes a thing for ranged and it's just like :'(

        # ~~~ Str or Dex?
        if not (Used_stat := self.stat[Stat.temp_strength]): Used_stat = self.stat[stat.strength]
        if not (Dex := self.stat[Stat.temp_dexterity]): Dex = self.stat[stat.dexterity]
        if weapon.properties[Property.ammunition]:
            Used_stat = Dex
        if weapon.properties[Property.versatile]:
            if Dex > Used_stat: Used_stat = Dex

        # ~~~ Calculaties
        to_hit_mod = Used_stat + self.stat[Stat.proficiency] + weapon.enchantment["Bonus"] # + any_other_modifiers
        dmg_mod = Used_stat + weapon.enchantment["Bonus"] # + any_other_modifiers
        to_hit = randint(1, 20) + to_hit_mod

        # ~~~ Applicationies!
        if to_hit >= target.AC:
            damage = randint(1, weapon.die) + dmg_mod
            self.damage(target, damage)
        # Additional effects

    def stat_check(self, test):
        pass

    def move(self, whereto):
        pass

    def down(self, intent=''):
        if self.team == team.PC or intent:
            print(self.name, "is down!")
            self.status["Down"] = 1
        else:
            self.status["Dead"] = 1
            self.death()



class Mob(Character):

    team = Team.mob

    def death(self):
        # Hook line and sinker. Create the loot. Call the combat object currently attached to the mob. 
        # Pass the loot to that object and have the object handle adding the loot to itself.
        print(self.name, "is dead!")
        self.combat.reward[E.xperience] =+ self.EXP
        self.combat.reward[E.quipment] =+ self.equipment
        self.combat.reward[Coin.PP] =+ self.coins[Coin.PP]
        self.combat.reward[Coin.GP] =+ self.coins[Coin.GP]
        self.combat.reward[Coin.EP] =+ self.coins[Coin.EP]
        self.combat.reward[Coin.SP] =+ self.coins[Coin.SP]
        self.combat.reward[Coin.CP] =+ self.coins[Coin.CP]    


class PC(Character):

    team = Team.PC

    def dead(self):
        print("Oh noes!", self.name, "is dead!")


class Item(object):

    def __init__(self):
        print("gay")
        pass

    def __str__(self):
        return "It's a regular ol'"+self.name


class Weapon(Item):

    def __init__(self, name, dice, num_dice, dmg, properties=None, enchantment=None, additional_info=None ):
        self.name =name
        self.dice = dice
        self.num_dice = num_dice
        self.dmg = dmg
        self.enchantment = {"Bonus":0}

# ~~~ TO REMOVE LATER (Presant in this file to stop unresolved referances during debugging/writting)

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