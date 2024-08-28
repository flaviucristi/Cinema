from datetime import datetime
from Domain.addOperantion import AddOperation
from Domain.cardClient import CardClient
from Domain.cardClientValidator import CardClientValidator
from Domain.deleteOperation import DeleteOperation
from Domain.modifyOperation import ModifyOperation
from Domain.multipleModifyOperation import MultipleModifyOperation
from Repository.repository import Repository
from Service.UndoRedoService import UndoRedoService


class CardClientService:
    def __init__(self, cardClientRepository: Repository,
                 cardClientValidator: CardClientValidator,
                 undoRedoService: UndoRedoService):
        self.__cardClientRepository = cardClientRepository
        self.__cardCleintValidator = cardClientValidator
        self.__undoRedoService = undoRedoService

    def getAll(self):
        return self.__cardClientRepository.read()

    def adauga(self, idCardClient, nume, prenume, CNP,
               dataNasterii, dataInregistrarii, puncteAcumulate):
        cardClient = CardClient(idCardClient,
                                nume,
                                prenume,
                                CNP,
                                dataNasterii,
                                dataInregistrarii,
                                puncteAcumulate)
        self.__cardCleintValidator.valideaza(cardClient)
        self.__cardClientRepository.adauga(cardClient)
        self.__undoRedoService.addUndoOperation(AddOperation(
            self.__cardClientRepository, cardClient
        ))

    def sterge(self, idCardClient):
        cardClientSters = self.__cardClientRepository.read(idCardClient)
        self.__cardClientRepository.sterge(idCardClient)
        self.__undoRedoService.addUndoOperation(DeleteOperation(
            self.__cardClientRepository, cardClientSters))

    def modifica(self, idCardClient, nume, prenume,
                 CNP, dataNasterii, dataInregistrarii, puncteAcumulate):
        cardClientVechi = self.__cardClientRepository.read(idCardClient)
        cardClient = CardClient(idCardClient,
                                nume,
                                prenume,
                                CNP,
                                dataNasterii,
                                dataInregistrarii,
                                puncteAcumulate)
        self.__cardCleintValidator.valideaza(cardClient)
        self.__cardClientRepository.modifica(cardClient)
        self.__undoRedoService.addUndoOperation(ModifyOperation(
            self.__cardClientRepository, cardClientVechi, cardClient))

    def Sortare(self, carduriCleinti, lungime) -> None:
        if lungime == 1:
            return
        else:
            for i in range(lungime - 1):
                if carduriCleinti[i].puncteAcumulate < \
                        carduriCleinti[i+1].puncteAcumulate:
                    aux = carduriCleinti[i]
                    carduriCleinti[i] = carduriCleinti[i+1]
                    carduriCleinti[i+1] = aux
            self.Sortare(carduriCleinti, lungime-1)

    def ordoneazaCardDupaPctAcum(self):
        carduriClienti = self.__cardClientRepository.read()
        lungime = len(carduriClienti)
        self.Sortare(carduriClienti, lungime)
        return carduriClienti

    def incrementare(self, puncte, data1, data2):
        clientiVechi = []
        clientiNoi = []
        for card1 in self.__cardClientRepository.read():
            nastere = card1.dataNasterii[:5]
            if datetime.strptime(data1,
                                 '%d.%m') <= datetime.strptime(nastere,
                                                               '%d.%m') \
                    and\
                    datetime.strptime(nastere,
                                      '%d.%m') <= datetime.strptime(data2,
                                                                    '%d.%m'):
                clientiVechi.append(card1)

        for card in self.__cardClientRepository.read():
            nastere = card.dataNasterii[:5]
            if datetime.strptime(data1,
                                 '%d.%m') <= datetime.strptime(nastere,
                                                               '%d.%m') \
                    and\
                    datetime.strptime(nastere,
                                      '%d.%m') <= datetime.strptime(data2,
                                                                    '%d.%m'):
                pctacumulate = card.puncteAcumulate
                card.puncteAcumulate = pctacumulate + puncte
                self.__cardClientRepository.modifica(card)
                clientiNoi.append(card)
        self.__undoRedoService.addUndoOperation(MultipleModifyOperation(
            self.__cardClientRepository, clientiVechi,
            clientiNoi))
