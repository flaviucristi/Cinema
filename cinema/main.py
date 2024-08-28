from Domain.cardClientValidator import CardClientValidator
from Domain.filmValidator import FilmValidator
from Domain.rezervareValidator import RezervareValidator
from Repository.repositoryJson import RepositoryJson
from Service.UndoRedoService import UndoRedoService
from Service.cardClientService import CardClientService
from Service.filmService import FilmService
from Service.functionalitati import Functionalitati
from Service.rezervareService import RezervareService
from Tests.testALL import runTests
from UI.console import Console


def main():
    runTests()
    undoRedoService = UndoRedoService()

    filmRepositoryJson = RepositoryJson("filme.json")
    filmValidator = FilmValidator()
    filmService = FilmService(filmRepositoryJson, filmValidator,
                              undoRedoService)

    cardClientRepositoryJson = RepositoryJson("carduriClienti.json")
    cardCleintValidator = CardClientValidator()
    cardClientService = CardClientService(cardClientRepositoryJson,
                                          cardCleintValidator,
                                          undoRedoService)

    rezervareRepositoryJson = RepositoryJson("rezervari.json")
    rezervareValidator = RezervareValidator()
    rezervareService = RezervareService(rezervareRepositoryJson,
                                        filmRepositoryJson,
                                        cardClientRepositoryJson,
                                        rezervareValidator,
                                        undoRedoService)

    functionalitati = Functionalitati(filmService, cardClientService)

    console = Console(filmService,
                      cardClientService,
                      rezervareService,
                      functionalitati,
                      undoRedoService)

    console.runMenu()


main()
