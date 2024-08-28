from typing import List
from Domain.entitate import Entitate
from Domain.undoRedoOperation import UndoRedoOperation
from Repository.repository import Repository


class MultipleDeleteOperation(UndoRedoOperation):
    def __init__(self,
                 repository: Repository,
                 obiecteSterse: list[Entitate],
                 obiecteSterse1: List = None,
                 repository1: Repository = None):
        self.__repository = repository
        self.__obiecteSterse = obiecteSterse
        self.__obiecteSterse1 = obiecteSterse1
        self.__repository1 = repository1

    def doUndo(self):
        for entitate in self.__obiecteSterse:
            self.__repository.adauga(entitate)
        if self.__obiecteSterse1:
            for entitate in self.__obiecteSterse1:
                self.__repository1.adauga(entitate)

    def doRedo(self):
        for entitate in self.__obiecteSterse:
            self.__repository.sterge(entitate.idEntitate)
        if self.__obiecteSterse1:
            for entitate in self.__obiecteSterse1:
                self.__repository1.sterge(entitate.idEntitate)
