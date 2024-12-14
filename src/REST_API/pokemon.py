from dataclasses import dataclass
from ORMSchema import Pokemon, GrowthRate
from typing import List
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