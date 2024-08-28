from dataclasses import dataclass
from Domain.entitate import Entitate


@dataclass
class Rezervare(Entitate):
    idFilm: str
    idCardClient: str
    data: str
    ora: str
