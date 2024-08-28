from dataclasses import dataclass


@dataclass
class RezervareError(Exception):
    mesaj: str

    def __str__(self):
        return f'RezervareError: {self.mesaj}'
