from Domain import filmValidator, cardClientValidator, rezervareValidator
from Domain.cardClient import CardClient
from Domain.film import Film
from Domain.rezervare import Rezervare
from Repository.repository import Repository
from Repository.repositoryJson import RepositoryJson
from Service.UndoRedoService import UndoRedoService
from Service.cardClientService import CardClientService
from Service.filmService import FilmService
from Service.rezervareService import RezervareService
from utils import clear_file


def testFilmRepositoryJson():
    undoRedoSerivce = UndoRedoService()
    filename = "testfilm.json"
    clear_file(filename)
    filmRepository = RepositoryJson(filename)
    assert filmRepository.read() == []

    film = Film("1", "Dune", 2021, 30, "DA")
    filmRepository.adauga(film)
    assert filmRepository.read("1") == film

    filmService = FilmService
    assert len(filmService(filmRepository, filmValidator,
                           undoRedoSerivce).getAll()) == 1

    filmRepository.sterge("1")
    assert filmRepository.read() == []

    film1 = Film("1", "spiderman", 2021, 30, "DA")
    filmRepository.adauga(film1)
    assert filmRepository.read("1") == film1
    filmmod = Film("1", "spiderman", 2020, 15, "NU")
    filmRepository.modifica(filmmod)
    assert len(filmService(filmRepository, filmValidator,
                           undoRedoSerivce).getAll()) == 1
    assert filmRepository.read(("1")) == filmmod


def testCardClientRepositoryJson():
    undoRedoService = UndoRedoService()
    filename = "testcarduri.json"
    clear_file(filename)
    cardClientRepository = RepositoryJson(filename)
    assert cardClientRepository.read() == []

    card = CardClient("1",
                      "muresan",
                      "flaviu",
                      "1234567890123",
                      "12.12.1234",
                      "12.11.1234",
                      0)
    cardClientRepository.adauga(card)
    assert cardClientRepository.read("1") == card

    cardCleintService = CardClientService
    assert len(cardCleintService(cardClientRepository,
                                 cardClientValidator,
                                 undoRedoService).getAll()) == 1

    cardClientRepository.sterge("1")
    assert cardClientRepository.read() == []

    card = CardClient("1",
                      "muresan",
                      "flaviu",
                      "1234567890123",
                      "12.12.1234",
                      "12.11.1234",
                      0)
    cardClientRepository.adauga(card)
    assert cardClientRepository.read("1") == card
    cardmod = CardClient("1",
                         "muresan",
                         "alin",
                         "1234567890098",
                         "11.12.1234",
                         "12.01.1234",
                         0)
    cardClientRepository.modifica(cardmod)
    assert len(cardCleintService(cardClientRepository,
                                 cardClientValidator,
                                 undoRedoService).getAll()) == 1
    assert cardClientRepository.read("1") == cardmod


def testRezervareRepositoryJson():
    undoRedoService = UndoRedoService()
    filename = "testrezervare.json"
    clear_file(filename)
    rezervareRepository = RepositoryJson(filename)
    assert rezervareRepository.read() == []

    filmRepository = Repository
    cardClientRepository = Repository
    rezervare = Rezervare("1", "1", "1", "12.12.2021", "12:30")
    rezervareRepository.adauga(rezervare)
    assert rezervareRepository.read("1") == rezervare

    rezervareService = RezervareService
    assert len(rezervareService(rezervareRepository,
                                filmRepository,
                                cardClientRepository,
                                rezervareValidator,
                                undoRedoService).getAll()) == 1

    rezervareRepository.sterge("1")
    assert rezervareRepository.read() == []

    rezervare1 = Rezervare("1",
                           "1", "1", "12.12.2021", "12:30")
    rezervareRepository.adauga(rezervare1)
    assert rezervareRepository.read("1") == rezervare1
    rezervaremod = Rezervare("1", "1", "1", "11.10.2020", "10:11")
    rezervareRepository.modifica(rezervaremod)
    assert len(rezervareService(rezervareRepository,
                                filmRepository,
                                cardClientRepository,
                                rezervareValidator,
                                undoRedoService).getAll()) == 1
    assert rezervareRepository.read("1") == rezervaremod
