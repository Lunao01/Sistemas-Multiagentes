from dataclasses import dataclass
from ORMSchema import Pokemon, GrowthRate, Habitat
from typing import List

from ORMSchema._orm_pokemon import Ability, Move, Type

@dataclass
class PokemonResponse():
    id: int
    name: str
    base_experience: int
    height: int
    weight: int
    is_default: bool
    order: int
    habitat: List[str]
    growth_rate: GrowthRate
    is_legendary: bool
    is_mythical: bool
    gender_rate: int

    capture_rate: int
    base_happiness: int
    abilities: List[str]
    forms: List[str]
    held_items: bool
    moves: List[str]
    types: List[str]
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int
    evolution: str
    evolution_level: int
    def __init__(self, p: "Pokemon"):
        self.id: int = p.id
        self.name: str = p.name
        self.base_experience: int = p.base_experience
        self.height: int = p.height
        self.weight: int = p.weight
        self.is_default: bool = p.is_default
        self.order: int = p.order
        self.habitat: List[str] = [i.habitat for i in p.habitat]
        self.growth_rate: GrowthRate = p.growth_rate
        self.is_legendary: bool = p.is_legendary
        self.is_mythical: bool = p.is_mythical
        self.gender_rate: int = p.gender_rate

        self.capture_rate: int = p.capture_rate
        self.base_happiness: int = p.base_happiness
        self.abilities: List[str] = [i.ability for i in p.abilities]
        self.forms: List[str] = [i.form for i in p.forms]
        self.held_items: bool = p.held_items
        self.moves: List[str] = [i.move for i in p.moves]
        self.types: List[str] = [i.type for i in p.types]
        self.hp: int = p.hp
        self.attack: int = p.attack
        self.defense: int = p.defense
        self.special_attack: int = p.special_attack
        self.special_defense: int = p.special_defense
        self.speed: int = p.speed
        self.evolution: str = p.evolution
        self.evolution_level: int = p.evolution_level
    
    def to_pokemon(self):
        return Pokemon(
            name = self.name,
            base_experience = self.base_experience,
            height = self.height,
            weight = self.weight,
            is_default = self.is_default,
            order = self.order,
            habitat = list(map(lambda x:Habitat(habitat=x),self.habitat)),
            growth_rate = self.growth_rate,
            is_legendary = self.is_legendary,
            is_mythical = self.is_mythical,
            gender_rate = self.gender_rate,

            capture_rate = self.capture_rate,
            base_happiness = self.base_happiness,
            abilities = list(map(lambda x:Ability(ability=x),self.abilities)),
            forms = list(map(lambda x:x.form, self.forms)),
            held_items = self.held_items,
            moves = list(map(lambda x:Move(move=x),self.moves)),
            types = list(map(lambda x:Type(type=x),self.types)),
            hp = self.hp,
            attack = self.attack,
            defense = self.defense,
            special_attack = self.special_attack,
            special_defense = self.special_defense,
            speed = self.speed,
            evolution = self.evolution,
            evolution_level = self.evolution_level,
        )