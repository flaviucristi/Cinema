from Domain.cardClient import CardClient
from Domain.cardClientValidator import CardClientValidator
from Domain.film import Film
from Domain.filmValidator import FilmValidator
from Repository.repositoryInMemory import RepositoryInMemory
from Service.UndoRedoService import UndoRedoService
from Service.cardClientService import CardClientService
from Service.filmService import FilmService
from Service.functionalitati import Functionalitati


def testFunctionalitati():
    undoRedoService = UndoRedoService()
    filmRepository = RepositoryInMemory()
    filmValidator = FilmValidator()
    filmService = FilmService(filmRepository, filmValidator,
                              undoRedoService)
    cardCleintRepository = RepositoryInMemory()
    cardClientValidator = CardClientValidator()
    cardClientService = CardClientService(cardCleintRepository,
                                          cardClientValidator,
                                          undoRedoService)

    filmService.adauga("1", "Dune", 2021, 30, "DA")
    cardClientService.adauga("1",
                             "muresan",
                             "flaviu",
                             "1234567890123",
                             "12.12.1234",
                             "12.11.1234",
                             0)

    functionalitati = Functionalitati(filmService, cardClientService)

    assert functionalitati.cautare1("Dune") == [Film(idEntitate='1',
                                                     titlu='Dune',
                                                     anAparitie=2021,
                                                     pretBilet=30,
                                                     inProgram='DA')]
    # test UndoRedo

    filmRepository = RepositoryInMemory()
    filmValidator = FilmValidator()
    undoRedoService = UndoRedoService()
    rezervareRepository = RepositoryInMemory()
    filmService = FilmService(filmRepository,
                              filmValidator,
                              undoRedoService)
    film1 = Film('1', 'logan', 2019, 10, 'DA')
    film2 = Film('2', 'apex', 2020, 10, 'DA')
    film3 = Film('3', 'cars', 2012, 5, 'NU')

    filmService.adauga('1', 'Cars', 2010, 10, 'DA')
    undoRedoService.undo()

    assert len(filmRepository.read()) == 0

    filmService.adauga('2', 'apex', 2020, 10, 'DA')
    filmService.adauga('3', 'cars', 2012, 5, 'NU')
    undoRedoService.undo()

    assert filmRepository.read() == [film2]

    undoRedoService.undo()
    assert filmRepository.read() == []

    cardRepository = RepositoryInMemory()
    cardValidator = CardClientValidator()
    undoRedoService = UndoRedoService()
    cardService = CardClientService(cardRepository,
                                    cardValidator,
                                    undoRedoService)

    card1 = CardClient('1',
                       'muresan',
                       'flaviu',
                       '123456789012',
                       '28.09.2000',
                       '11.11.2020',
                       3)
    cardService.adauga('1',
                       'muresan',
                       'flaviu',
                       '123456789012',
                       '28.09.2000',
                       '11.11.2020',
                       3)

    undoRedoService.undo()
    assert cardRepository.read() == []
    undoRedoService.redo()
    assert cardRepository.read() == [card1]
