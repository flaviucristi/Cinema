from Domain.cardClient import CardClient
from Domain.film import Film
from Domain.rezervare import Rezervare


def testDomainFilm():
    film = Film("1", "Dune", 2021, 30, "DA")
    assert film.idEntitate == "1"
    assert film.titlu == "Dune"
    assert film.anAparitie == 2021
    assert film.pretBilet == 30
    assert film.inProgram == "DA"


def testDomainCardClient():
    cardClient = CardClient("1",
                            "Muresan",
                            "Flaviu",
                            "1234567890123",
                            "12.12.1234",
                            "12:30",
                            0)
    assert cardClient.idEntitate == "1"
    assert cardClient.nume == "Muresan"
    assert cardClient.prenume == "Flaviu"
    assert cardClient.dataNasterii == "12.12.1234"
    assert cardClient.dataInregistrarii == "12:30"
    assert cardClient.puncteAcumulate == 0


def testDomainRezervare():
    rezervare = Rezervare("1", "1", "2", "12.12.1234", "12:30")
    assert rezervare.idEntitate == "1"
    assert rezervare.idFilm == "1"
    assert rezervare.idCardClient == "2"
    assert rezervare.data == "12.12.1234"
    assert rezervare.ora == "12:30"
