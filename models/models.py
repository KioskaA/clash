from pydantic import BaseModel
from datetime import date, datetime

class Achievement(BaseModel):
    name: str
    stars: int
    value: int
    target: int

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

class BaseAttack(BaseModel):
    stars: int
    duration: int
    destruction: float

class RaidAttack(BaseAttack):
    pass

class Attack(BaseAttack):
    attacker_tag: str
    defender_tag: str

class CWLAttack(Attack):
    attack_day: int

class GameEventSummary(BaseModel):
    end_date: date
    is_ongoing: bool

class RaidsSummary(GameEventSummary):
    attacks: list[RaidAttack]
    available_attacks: int
    gold_looted: int

class CWSummary(GameEventSummary):
    attacks: list[Attack]
    stars: int

class CWLSummary(GameEventSummary):
    season: str
    attacks: list[CWLAttack]
    stars: int

class CGSummary(GameEventSummary):
    points: int
    season: str

class Player(BaseModel):
    tag: str
    name: str
    role: str
    exp_level: int
    town_hall: int
    builder_hall: int

    join_date: date
    is_new: bool
    is_returned:bool
    leave_date: date | None

    builder_base_league: str
    trophies: int
    builder_base_trophies: int

    donations: int
    received: int

    war_opted_in: bool
    cw: list[CWSummary]
    cwl: list[CWLSummary]
    clan_games_points: list[CGSummary]
    raids: list[RaidsSummary]
    clan_capital_contributions: int

    achievements: list[Achievement]
    builder_troops: list[Troop]
    equipment: list[Equipment]
    heroes: list[Hero]
    home_troops: list[Troop]
    pets: list[Pet]
    spells: list[Spell]
    siege_machines: list[SiegeMachine]

class Clan(BaseModel):
    ...

class GameEvent(BaseModel):
    id: int
    home_clan: Clan
    state: str
    end_date: datetime
    overlooked: list[str] # Игроки, которые проигнорировали ивент полностью

class RaidWeekend(GameEvent):
    attack_count: int
    offensive_reward: int
    defensive_reward: int
    total_loot: int
    completed_raid_count: int
    attackers: list[str] # Атаковавшие в рейдах

class CGPlayerPoints(BaseModel):
    player_tag: str
    points: int

class ClanGames(GameEvent):
    season: str
    total_points: int
    players_points: list[CGPlayerPoints]

class ClanWar(GameEvent):
    opponent: str
    team_size: int
    status: str
    attackers: list[str]

class CWLWar(BaseModel):
    day: int
    attackers: list[str]

class CWLOverlooked(BaseModel):
    day: int
    overlooked: list[str]

class CWL(GameEvent):
    season: str
    rounds_count: int
    wars: list[CWLWar]
    overlooked_detailed: list[CWLOverlooked]
