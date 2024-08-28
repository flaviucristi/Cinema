from Service.cardClientService import CardClientService
from Service.filmService import FilmService


class Functionalitati:
    def __init__(self, filmService: FilmService,
                 cardClientService: CardClientService):
        self.__filmService = filmService
        self.__cardClientService = cardClientService

    def cautare1(self, string):
        filme = self.__filmService.getAll()
        return list(filter(lambda x: string in str(x.titlu) or
                    string in str(x.anAparitie) or
                    string in str(x.idEntitate) or
                    string in str(x.pretBilet) or
                    string in str(x.inProgram), filme))

    def cautare2(self, string):
        carduriClienti = self.__cardClientService.getAll()
        return list(filter(lambda x: string in str(x.idEntitate) or
                    string in str(x.nume) or
                    string in str(x.prenume) or
                    string in str(x.dataNasterii) or
                    string in str(x.dataInregistrarii) or
                    string in str(x.puncteAcumulate),
                           carduriClienti))
