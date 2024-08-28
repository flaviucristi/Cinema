from dataclasses import dataclass
from Domain.entitate import Entitate


@dataclass
class Film(Entitate):
    titlu: str
    anAparitie: int
    pretBilet: float
    inProgram: str
