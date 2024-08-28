from datetime import datetime
from functools import reduce
from Domain.addOperantion import AddOperation
from Domain.deleteOperation import DeleteOperation
from Domain.modifyOperation import ModifyOperation
from Domain.multipleDeleteOperation import MultipleDeleteOperation
from Domain.rezervare import Rezervare
from Domain.rezervareValidator import RezervareValidator
from Repository.repository import Repository
from Service.UndoRedoService import UndoRedoService


class RezervareService:
    def __init__(self, rezervareRepository: Repository,
                 filmRepository: Repository,
                 cardClientRepository: Repository,
                 rezervareValidator: RezervareValidator,
                 undoRedoService: UndoRedoService):
        self.__rezervareRepository = rezervareRepository
        self.__rezervareValidator = rezervareValidator
        self.__filmRepository = filmRepository
        self.__cardClientRepository = cardClientRepository
        self.__undoRedoService = undoRedoService

    def getAll(self):
        return self.__rezervareRepository.read()

    def adauga(self, idRezervare, idFilm, idCardClient, data, ora):
        if self.__filmRepository.read(idFilm) is None:
            raise KeyError("Nu exista un film cu id-ul dat!")
        if self.__cardClientRepository.read(idCardClient) is None:
            raise KeyError("Nu exista un card cu id-ul dat!")

        film = self.__filmRepository.read(idFilm)
        cardClient = self.__cardClientRepository.read(idCardClient)

        if film.inProgram == "NU":
            raise ValueError("Filmul nu este in program!")
        else:
            rezervare = Rezervare(idRezervare, idFilm, idCardClient, data, ora)
            self.__rezervareValidator.valideaza(rezervare)

            puncte = 10/100 * film.pretBilet
            puncteacum = cardClient.puncteAcumulate
            cardClient.puncteAcumulate = puncteacum + int(puncte)

            self.__cardClientRepository.modifica(cardClient)
            self.__rezervareRepository.adauga(rezervare)
            self.__undoRedoService.addUndoOperation(AddOperation(
                self.__rezervareRepository, rezervare))

    def sterge(self, idRezervare):
        rezervare = self.__rezervareRepository.read(idRezervare)
        film = self.__filmRepository.read(rezervare.idFilm)
        cardClient = self.__cardClientRepository.read(rezervare.idCardClient)

        puncte = 10 / 100 * film.pretBilet
        puncteacum = cardClient.puncteAcumulate
        cardClient.puncteAcumulate = puncteacum - int(puncte)
        if cardClient.puncteAcumulate < 0:
            cardClient.puncteAcumulate = 0
        self.__cardClientRepository.modifica(cardClient)

        rezervareStearsa = self.__rezervareRepository.read(idRezervare)
        self.__rezervareRepository.sterge(idRezervare)
        self.__undoRedoService.addUndoOperation(DeleteOperation(
            self.__rezervareRepository, rezervareStearsa))

    def modifica(self, idRezervare, idFilm, idCardClient, data, ora):
        if self.__filmRepository.read(idFilm) is None:
            raise KeyError("Nu exista un film cu id-ul dat!")
        if self.__cardClientRepository.read(idCardClient) is None:
            raise KeyError("Nu exista un card cu id-ul dat!")

        rezervare1 = self.__rezervareRepository.read(idRezervare)
        film = self.__filmRepository.read(rezervare1.idFilm)
        cardClient = self.__cardClientRepository.read(rezervare1.idCardClient)

        puncte = 10 / 100 * film.pretBilet
        puncteacum = cardClient.puncteAcumulate
        cardClient.puncteAcumulate = puncteacum - int(puncte)
        self.__cardClientRepository.modifica(cardClient)

        rezervare = Rezervare(idRezervare, idFilm, idCardClient, data, ora)
        self.__rezervareValidator.valideaza(rezervare)

        film = self.__filmRepository.read(idFilm)
        cardClient = self.__cardClientRepository.read(idCardClient)

        puncte = 10 / 100 * film.pretBilet
        puncteacum = cardClient.puncteAcumulate
        cardClient.puncteAcumulate = puncteacum + int(puncte)

        rezervareVeche = rezervare1
        self.__cardClientRepository.modifica(cardClient)
        self.__rezervareRepository.modifica(rezervare)
        self.__undoRedoService.addUndoOperation(ModifyOperation(
            self.__rezervareRepository, rezervareVeche, rezervare))

    def afisRezervariIntervalOre(self, ora1, ora2):
        list = []
        for rezervare in self.__rezervareRepository.read():
            if datetime.strptime(ora1,
                                 '%H:%M') <= datetime.strptime(rezervare.ora,
                                                               '%H:%M') and\
                    datetime.strptime(rezervare.ora,
                                      '%H:%M') <= datetime.strptime(ora2,
                                                                    '%H:%M'):
                list.append(rezervare)

        return list

    def mySort(self, list, key, reverse: bool):
        n = len(list)
        if reverse is False:
            for i in range(n):
                for j in range(1, n):
                    if key(list[j-1]) > key(list[j]):
                        list[j-1], list[j] = list[j], list[j-1]
        elif reverse is True:
            for i in range(n):
                for j in range(1, n):
                    if key(list[j-1]) < key(list[j]):
                        list[j-1], list[j] = list[j], list[j-1]
        return list

    def ordoneazaFilmeDupaNrDeRezervari(self):
        nrRezervari = {}
        rezultat = []

        for film in self.__filmRepository.read():
            nrRezervari[film.idEntitate] = []
        for rezervare in self.__rezervareRepository.read():
            nrRezervari[rezervare.idFilm].append(1)

        for idFilm in nrRezervari:
            if len(nrRezervari[idFilm]) != 0:
                nr = reduce(lambda x, y: x+y, nrRezervari[idFilm])
            else:
                nr = 0
            rezultat.append({
                "film": self.__filmRepository.read(idFilm),
                "nrRezervari": nr
            })

        return self.mySort(rezultat,
                           key=lambda nrRezervare: nrRezervare["nrRezervari"],
                           reverse=True)

    def stergereRezervariInterval(self, data1, data2):
        list = []
        for rezervare in self.__rezervareRepository.read():
            if datetime.strptime(
                    data1, '%d.%m.%Y') <= datetime.strptime(
                rezervare.data, '%d.%m.%Y') and\
                    datetime.strptime(
                        rezervare.data, '%d.%m.%Y') <=\
                    datetime.strptime(data2, '%d.%m.%Y'):

                idrez = rezervare.idEntitate
                rezervari = self.__rezervareRepository.read(idrez)
                film = self.__filmRepository.read(rezervari.idFilm)
                idrezClient = rezervari.idCardClient
                cardClient = self.__cardClientRepository.read(idrezClient)

                puncte = 10 / 100 * film.pretBilet
                puncteacum = cardClient.puncteAcumulate
                cardClient.puncteAcumulate = puncteacum - int(puncte)
                if cardClient.puncteAcumulate < 0:
                    cardClient.puncteAcumulate = 0

                self.__cardClientRepository.modifica(cardClient)
                self.__rezervareRepository.sterge(rezervare.idEntitate)
                list.append(rezervare)
        if list:
            self.__undoRedoService.addUndoOperation((MultipleDeleteOperation(
                self.__rezervareRepository, list)))

    def deleteInCascada(self, idfilm):
        listFilmeSterse = []
        listRezSterse = []
        for film in self.__filmRepository.read():
            if str(film.idEntitate) == str(idfilm):
                listFilmeSterse.append(self.__filmRepository.read(
                    film.idEntitate))
                self.__filmRepository.sterge(idfilm)
                for rezervare in self.__rezervareRepository.read():
                    if str(rezervare.idFilm) == str(idfilm):
                        listRezSterse.append(self.__rezervareRepository.read(
                            rezervare.idEntitate))
                        self.__rezervareRepository.sterge(rezervare.idEntitate)
        if listFilmeSterse:
            self.__undoRedoService.addUndoOperation(MultipleDeleteOperation(
                self.__filmRepository,
                listFilmeSterse, listRezSterse, self.__rezervareRepository))
