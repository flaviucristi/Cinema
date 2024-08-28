from Domain.entitate import Entitate
from Domain.undoRedoOperation import UndoRedoOperation
from Repository.repository import Repository


class MultipleModifyOperation(UndoRedoOperation):
    def __init__(self, repository: Repository,
                 obiecteVechi: list[Entitate],
                 obiecteNoi: list[Entitate]):
        self.__repository = repository
        self.__obiecteVechi = obiecteVechi
        self.__obiecteNoi = obiecteNoi

    def doUndo(self):
        for entitate in self.__obiecteVechi:
            self.__repository.modifica(entitate)

    def doRedo(self):
        for entitate in self.__obiecteNoi:
            self.__repository.modifica(entitate)
