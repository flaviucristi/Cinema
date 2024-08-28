from Domain.addOperantion import AddOperation
from Domain.deleteOperation import DeleteOperation
from Domain.film import Film
from Domain.filmValidator import FilmValidator
from Domain.modifyOperation import ModifyOperation
from Repository.repository import Repository
from Service.UndoRedoService import UndoRedoService


class FilmService:
    def __init__(self,
                 filmRepository: Repository,
                 filmValidator: FilmValidator,
                 undoRedoService: UndoRedoService):
        self.__filmRepository = filmRepository
        self.__filmValidator = filmValidator
        self.__undoRedoService = undoRedoService

    def getAll(self):
        return self.__filmRepository.read()

    def adauga(self, idFilm, titlu, anAparitie, pretBilet, inProgram):
        film = Film(idFilm, titlu, anAparitie, pretBilet, inProgram)
        self.__filmValidator.valideaza(film)
        self.__filmRepository.adauga(film)
        self.__undoRedoService.addUndoOperation(AddOperation(
            self.__filmRepository, film))

    def sterge(self, idFilm):
        filmSters = self.__filmRepository.read(idFilm)
        self.__filmRepository.sterge(idFilm)
        self.__undoRedoService.addUndoOperation(DeleteOperation(
            self.__filmRepository, filmSters))

    def modifica(self, idFilm, titlu, anAparitie, pretBilet, inProgram):
        filmVechi = self.__filmRepository.read(idFilm)
        film = Film(idFilm, titlu, anAparitie, pretBilet, inProgram)
        self.__filmValidator.valideaza(film)
        self.__filmRepository.modifica(film)
        self.__undoRedoService.addUndoOperation(ModifyOperation(
            self.__filmRepository, filmVechi, film))
