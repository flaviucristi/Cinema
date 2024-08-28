from typing import List
from Domain.entitate import Entitate
from Domain.undoRedoOperation import UndoRedoOperation
from Repository.repository import Repository


class MultipleAddOperation(UndoRedoOperation):
    def __init__(self,
                 repository: Repository,
                 obiecteAdaugate):
        self.__repository = repository
        self.__obiecteAdaugate = obiecteAdaugate

    def doUndo(self):
        for entitate in self.__obiecteAdaugate:
            self.__repository.sterge(entitate.idEntitate)

    def doRedo(self):
        for entitate in self.__obiecteAdaugate:
            self.__repository.adauga(entitate)
