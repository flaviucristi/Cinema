from Domain.cardClient import CardClient
from Domain.cardClientValidator import CardClientValidator
from Domain.film import Film
from Domain.filmValidator import FilmValidator
from Domain.rezervareValidator import RezervareValidator
from Repository.repositoryInMemory import RepositoryInMemory
from Service.UndoRedoService import UndoRedoService
from Service.cardClientService import CardClientService
from Service.filmService import FilmService
from Service.rezervareService import RezervareService


def testFilmService():
    undoRedoService = UndoRedoService()
    filmRepository = RepositoryInMemory()
    filmValidator = FilmValidator()
    filmService = FilmService(filmRepository, filmValidator,
                              undoRedoService)
    filmService.adauga("1", "Dune", 2021, 30, "DA")
    assert len(filmService.getAll()) == 1

    filmService.adauga("2", "spiderman", 2020, 15, "DA")
    filmService.adauga("3", "007", 2021, 45, "NU")
    filmService.adauga("4", "logan", 2019, 10, "DA")

    assert len(filmService.getAll()) == 4
    assert filmService.getAll()[0].titlu == "Dune"

    filmService.sterge("4")
    assert len(filmService.getAll()) == 3

    filmService.modifica("3", "007", 2018, 5, "DA")
    assert filmService.getAll()[2].anAparitie == 2018


def testCardClientService():
    undoRedoService = UndoRedoService()
    cardClientRepository = RepositoryInMemory()
    cardClientValidator = CardClientValidator()
    cardClientService = CardClientService(cardClientRepository,
                                          cardClientValidator,
                                          undoRedoService)
    cardClientService.adauga("1", "muresan", "flaviu", "1234567890123",
                             "12.12.1234", "23.12.2018", 0)
    assert len(cardClientService.getAll()) == 1

    assert cardClientService.getAll()[0].nume == "muresan"
    assert cardClientService.getAll()[0].prenume == "flaviu"

    cardClientService.adauga("2",
                             "popescu",
                             "marius",
                             "1234567890123",
                             "12.11.2001",
                             "12.05.2020",
                             12)
    cardClientService.adauga("3", "ionescu", "alin", "1234567890456",
                             "12.12.2000", "12.03.2021", 0)
    cardClientService.adauga("4", "adrian", "marian", "1234567890789",
                             "03.08.1999", "12.10.2018", 0)

    assert len(cardClientService.getAll()) == 4

    cardClientService.sterge("4")
    assert len(cardClientService.getAll()) == 3

    cardClientService.modifica("3",
                               "maxim",
                               "laurentiu",
                               "1234567890456",
                               "12.12.2000",
                               "12.03.2021",
                               6)
    assert cardClientService.getAll()[2].prenume == "laurentiu"

    assert cardClientService.ordoneazaCardDupaPctAcum()[0].puncteAcumulate ==\
           12
    assert cardClientService.ordoneazaCardDupaPctAcum()[1].puncteAcumulate == 6
    assert cardClientService.ordoneazaCardDupaPctAcum()[2].puncteAcumulate == 0

    cardClientService.incrementare(10, "12.07", "11.12")
    assert cardClientService.getAll()[0].puncteAcumulate == 0
    assert cardClientService.getAll()[1].puncteAcumulate == 22
    assert cardClientService.getAll()[2].puncteAcumulate == 6


def testRezervareService():
    undoRedoService = UndoRedoService()
    rezervareRepository = RepositoryInMemory()
    rezervareValidator = RezervareValidator()
    filmRepository = RepositoryInMemory()
    cardClientRepository = RepositoryInMemory()

    film = Film("1", "Dune", 2021, 30, "DA")
    filmRepository.adauga(film)
    film1 = Film("2", "spiderman", 2020, 15, "DA")
    filmRepository.adauga(film1)
    film2 = Film("3", "007", 2021, 45, "DA")
    filmRepository.adauga(film2)
    film3 = Film("4", "logan", 2019, 10, "DA")
    filmRepository.adauga(film3)

    card = CardClient("1",
                      "muresan",
                      "flaviu",
                      "1234567890123",
                      "12.12.1234",
                      "12.11.1234",
                      0)
    cardClientRepository.adauga(card)
    card1 = CardClient("2",
                       "popescu",
                       "marius",
                       "1234567890123",
                       "12.11.2001",
                       "12.05.2020",
                       0)
    cardClientRepository.adauga(card1)
    card2 = CardClient("3",
                       "ionescu",
                       "alin",
                       "1234567890456",
                       "12.12.2000",
                       "12.03.2021",
                       0)
    cardClientRepository.adauga(card2)
    card3 = CardClient("4",
                       "adrian",
                       "marian",
                       "1234567890789",
                       "03.08.1999",
                       "12.10.2018",
                       0)
    cardClientRepository.adauga(card3)

    assert len(filmRepository.read()) == 4
    assert len(cardClientRepository.read()) == 4

    rezervareService = RezervareService(rezervareRepository,
                                        filmRepository,
                                        cardClientRepository,
                                        rezervareValidator,
                                        undoRedoService)

    rezervareService.adauga("1", "1", "1", "12.12.2021", "12:30")
    assert len(rezervareService.getAll()) == 1

    rezervareService.adauga("2", "1", "2", "12.11.2021", "11:30")
    rezervareService.adauga("3", "1", "3", "12.02.2019", "13:30")
    rezervareService.adauga("4", "3", "1", "24.09.2020", "14:30")
    rezervareService.adauga("5", "3", "2", "28.11.2021", "14:30")
    rezervareService.adauga("6", "4", "2", "12.12.2019", "18:30")
    rezervareService.adauga("7", "1", "2", "12.12.2019", "18:30")

    assert len(rezervareService.getAll()) == 7

    rezervareService.sterge("3")
    assert len(rezervareService.getAll()) == 6

    rezervareService.adauga("3", "2", "2", "12.02.2019", "13:30")
    rezervareService.modifica("2", "1", "3", "12.02.2018", "14:30")
    assert rezervareService.getAll()[2].ora == "14:30"

    list = rezervareService.afisRezervariIntervalOre("13:30", "14:40")
    assert len(list) == 4
    assert list[0].idEntitate == "2"
    assert list[1].idEntitate == "4"
    assert list[2].idEntitate == "5"
    assert list[3].idEntitate == "3"

    list1 = rezervareService.ordoneazaFilmeDupaNrDeRezervari()
    assert list1[0] == {'film': Film(idEntitate='1',
                                     titlu='Dune',
                                     anAparitie=2021,
                                     pretBilet=30,
                                     inProgram='DA'),
                        'nrRezervari': 3}
    assert list1[1] == {'film': Film(idEntitate='3',
                                     titlu='007',
                                     anAparitie=2021,
                                     pretBilet=45,
                                     inProgram='DA'),
                        'nrRezervari': 2}
    assert list1[2] == {'film': Film(idEntitate='2',
                                     titlu='spiderman',
                                     anAparitie=2020, pretBilet=15,
                                     inProgram='DA'),
                        'nrRezervari': 1}
    assert list1[3] == {'film': Film(idEntitate='4',
                                     titlu='logan',
                                     anAparitie=2019,
                                     pretBilet=10,
                                     inProgram='DA'),
                        'nrRezervari': 1}

    rezervareService.stergereRezervariInterval("12.10.2020", "12.12.2021")
    assert len(rezervareService.getAll()) == 5
    assert rezervareService.getAll()[0].idEntitate == "2"
    assert rezervareService.getAll()[1].idEntitate == "4"
    assert rezervareService.getAll()[2].idEntitate == "6"
    assert rezervareService.getAll()[3].idEntitate == "7"
    assert rezervareService.getAll()[4].idEntitate == "3"
