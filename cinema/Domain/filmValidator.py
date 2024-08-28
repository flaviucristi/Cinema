from Domain.film import Film
from Domain.filmError import FilmError


class FilmValidator:
    def valideaza(self, film: Film):
        erori = []
        if film.inProgram not in ["DA", "NU"]:
            erori.append("Filmul trebuie sa fie sau nu in program:'DA','NU'!")
        if len(erori) > 0:
            raise FilmError(erori)
