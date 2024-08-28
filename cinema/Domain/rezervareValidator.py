from datetime import datetime
from Domain.rezervare import Rezervare
from Domain.rezervareError import RezervareError


class RezervareValidator:
    def valideaza(self, rezervare: Rezervare):
        try:
            datetime.strptime(rezervare.data, '%d.%m.%Y')
            datetime.strptime(rezervare.data, '%d.%m.%Y')
        except ValueError:
            raise RezervareError("Formatul datei trebuie sa fie: DD.MM.YYYY!")
        try:
            datetime.strptime(rezervare.ora, '%H:%M')
        except ValueError:
            raise RezervareError("Formatul orei trebuie sa fie: hh:mm!")
