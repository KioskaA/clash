from pydantic import BaseModel, field_validator

class Achievement(BaseModel):
    ...

class BaseTroop(BaseModel):
    name: str
    level: int
    is_troop: bool = False
    is_siege_machine: bool = False
    is_pet: bool = False
    is_spell: bool = False
    is_hero: bool = False

class Troop(BaseTroop):
    is_troop: bool = True

class SiegeMachine(BaseTroop):
    is_siege_machine: bool = True

class Pet(BaseTroop):
    is_pet: bool = True

class Spell(BaseTroop):
    is_spell: bool = True

class Hero(BaseTroop):
    is_hero: bool = True

class Equipment(BaseModel):
    name: str
    level: int
    hero: Hero

class Player(BaseModel):
    tag: str
    name: str
    role: str
    clan_capital_contributions: int
    exp_level: int
    builder_base_league: str
    trophies: int
    builder_base_trophies: int
    town_hall: int
    donations: int
    received: int
    builder_hall: int
    war_opted_in: bool
    achievements: list[Achievement]
    builder_troops: list[Troop]
    equipment: list[Equipment]
    heroes: list[Hero]
    home_troops: list[Troop]
    pets: list[Pet]
    spells: list[Spell]
    siege_machines: list[SiegeMachine]