import random
from datetime import datetime
from Domain.cardClientError import CardClientError
from Domain.film import Film
from Domain.filmError import FilmError
from Domain.rezervareError import RezervareError
from Service.UndoRedoService import UndoRedoService
from Service.cardClientService import CardClientService
from Service.filmService import FilmService
from Service.functionalitati import Functionalitati
from Service.rezervareService import RezervareService


class Console:
    def __init__(self, filmService: FilmService,
                 cardClientService: CardClientService,
                 rezervareService: RezervareService,
                 functionalitati: Functionalitati,
                 undoRedoService: UndoRedoService):
        self.__filmService = filmService
        self.__cardClientService = cardClientService
        self.__rezervareService = rezervareService
        self.__functionalitati = functionalitati
        self.__undoRedoSerivce = undoRedoService

    def runMenu(self):
        if True:
            print("1. CRUD  film")
            print("2. CRUD card client")
            print("3. CRUD rezervare")
            print("4. Căutare filme și clienți. Căutare full text")
            print("5. Afișarea tuturor rezervărilor dintr-un"
                  " interval de ore dat, indiferent de zi.")
            print("6. Afișarea filmelor ordonate descrescător"
                  " după numărul de rezervări.")
            print("7. Afișarea cardurilor client ordonate descrescător"
                  " după numărul de puncte de pe card.")
            print("8. Ștergerea tuturor rezervărilor dintr-un"
                  " anumit interval de zile.")
            print("9. Incrementarea cu o valoare dată a punctelor"
                  " de pe toate cardurile"
                  " a căror zi de naștere se află într-un interval dat.")
            print("10. Delete in cascada.")
            print("u. Undo")
            print("r. Redo")
            print("g. Generare automata x filme")
            print("x. Iesire")

            optiune = input("Dati optiune: ")

            if optiune == "1":
                self.runCRUDFilmMenu()
            elif optiune == "2":
                self.runCRUDCardClienMenu()
            elif optiune == "3":
                self.runCRUDRezervareMenu()
            elif optiune == "4":
                self.uiCautareString()
            elif optiune == "5":
                self.uiRezervariIntervalOre()
            elif optiune == "6":
                self.uiFilmeDescDupaNrRezervari()
            elif optiune == "7":
                self.uiCarduriClientiDescDupaPuncteAcumulate()
            elif optiune == "8":
                self.uiStergereRezervariInterval()
            elif optiune == "9":
                self.uiIncrementarePuncte()
            elif optiune == "10":
                self.uiDeleteCascada()
            elif optiune == "u":
                self.__undoRedoSerivce.undo()
            elif optiune == "r":
                self.__undoRedoSerivce.redo()
            elif optiune == "g":
                self.uiGenerareRandom()
            elif optiune == "x":
                return
            else:
                print("Optiune gresita! Reincercati!")
        self.runMenu()

    def runCRUDFilmMenu(self):
        while True:
            print("1. Adauga filme")
            print("2. Sterge film")
            print("3. Modifica film")
            print("a. Afiseaza toate filmere")
            print("x. Iesire")

            optiune = input("Dati optiune: ")

            if optiune == "1":
                self.uiAdaugaFilm()
            elif optiune == "2":
                self.uiStergeFilm()
            elif optiune == "3":
                self.uiModificaFilm()
            elif optiune == "a":
                self.showAllFilme()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati!")

    def runCRUDCardClienMenu(self):
        while True:
            print("1. Adauga card client")
            print("2. Sterge card client")
            print("3. Modifica card client")
            print("a. Afiseaza toate cardurile clientiilor")
            print("x. Iesire")

            optiune = input("Dati optiune: ")

            if optiune == "1":
                self.uiAdaugaCardClient()
            elif optiune == "2":
                self.uiStergeCardClient()
            elif optiune == "3":
                self.uiModificaCardClient()
            elif optiune == "a":
                self.showAllCarduriClienti()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati!")

    def runCRUDRezervareMenu(self):
        while True:
            print("1. Adauga rezervare")
            print("2. Sterge rezervare")
            print("3. Modifica rezervare")
            print("a. Afiseaza rezervarile")
            print("x. Iesire")

            optiune = input("Dati optiune: ")

            if optiune == "1":
                self.uiAdaugaRezervare()
            elif optiune == "2":
                self.uiStergeRezervare()
            elif optiune == "3":
                self.uiModificaRezervare()
            elif optiune == "a":
                self.showAllRezervari()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati!")

    def uiAdaugaFilm(self):
        try:
            idFilm = input("Dati id-ul filmului: ")
            titlu = input("Dati titlul filmului: ")
            anAparitie = int(input("Dati anul aparitiei filmului: "))
            pretBilet = float(input("Dati pretul biletului: "))
            inProgram = input("DA/NU daca filmul este sau nu in program: ")

            self.__filmService.adauga(idFilm,
                                      titlu,
                                      anAparitie,
                                      pretBilet,
                                      inProgram)
        except ValueError as ve:
            print(ve)
        except FilmError as fe:
            print(fe)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiStergeFilm(self):
        try:
            idFilm = input("Dati id-ul filmului de sters: ")
            self.__filmService.sterge(idFilm)

        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiModificaFilm(self):
        try:
            idFilm = input("Dati id-ul filmului d emodificat: ")
            titlu = input("Dati noul titlu al filmului: ")
            anAparitie = int(input("Dati noul an al aparitiei noului film: "))
            pretBilet = float(input("Dati noul pret al biletului: "))
            inProgram = input("DA/NU daca noul film este sau nu in program: ")

            self.__filmService.modifica(idFilm,
                                        titlu,
                                        anAparitie,
                                        pretBilet,
                                        inProgram)
        except ValueError as ve:
            print(ve)
        except FilmError as fe:
            print(fe)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def showAllFilme(self):
        for entitate in self.__filmService.getAll():
            print(entitate)

    def uiAdaugaCardClient(self):
        try:
            idCardClient = input("Dati id-ul cardului clientului: ")
            nume = input("Dati numele clientului: ")
            prenume = input("Dati prenumele clientului: ")
            CNP = input("Dati CNP-ul clientului: ")
            if len(CNP) > 13 or len(CNP) < 13 or\
                    (len(CNP) == 13 and CNP.isdecimal() is False):
                raise ValueError("CNP-ul trebuie sa aiba exact 4 cifre!")
            with open("carduriClienti.json", 'r') as read:
                for line in read:
                    if CNP in line:
                        raise ValueError("CNP-ul exista deja!")

            dataNasterii = input("Dati data nasterii cleintului(dd.mm.yyyy): ")
            dataInregistrarii = input("Dati data inregitrarii cardului "
                                      "clientului(dd.mm.yyyy): ")

            puncteAcumulate = 0
            self.__cardClientService.adauga(idCardClient,
                                            nume,
                                            prenume,
                                            CNP,
                                            dataNasterii,
                                            dataInregistrarii,
                                            puncteAcumulate)
            print("Numar puncte acumulate: ")
            print(puncteAcumulate)
        except ValueError as ve:
            print(ve)
        except CardClientError as cce:
            print(cce)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiStergeCardClient(self):
        try:
            idCardClient = input("Dati id-ul cardului clientului de sters: ")
            self.__cardClientService.sterge(idCardClient)

        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiModificaCardClient(self):
        try:
            idCardClient = input("Dati id-ul cardului "
                                 "clientului de modificat: ")
            nume = input("Dati noul nume al clientului: ")
            prenume = input("Dati noul prenume al clientului: ")
            CNP = input("Dati noul CNP al clientului: ")
            if len(CNP) > 13 or len(CNP) < 13 or\
                    (len(CNP) == 13 and CNP.isdecimal() is False):
                raise ValueError("CNP-ul trebuie sa aiba exact 4 cifre!")
            with open("carduriClienti.json", 'r') as read:
                for line in read:
                    if CNP in line:
                        raise ValueError("CNP-ul exista deja!")

            dataNasterii = input("Dati noua data de nastere a clientului: ")

            dataInregistrarii = input("Dati noua data de "
                                      "inregitrare a cardului clientului: ")

            puncteAcumulate = 0

            self.__cardClientService.modifica(idCardClient,
                                              nume,
                                              prenume,
                                              CNP,
                                              dataNasterii,
                                              dataInregistrarii,
                                              puncteAcumulate)
            print(puncteAcumulate)
        except ValueError as ve:
            print(ve)
        except CardClientError as cce:
            print(cce)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def showAllCarduriClienti(self):
        for entitate in self.__cardClientService.getAll():
            print(entitate)

    def uiAdaugaRezervare(self):
        try:
            idRezervare = input("Dati id-ul revervarii: ")
            idFilm = input("Dati id-ul filmului: ")
            idCardClient = input("Dati id-ul cardului: ")
            data = input("Dati data: ")
            ora = input("Dati ora la care incepe filmul(hh:mm): ")
            self.__rezervareService.adauga(idRezervare,
                                           idFilm,
                                           idCardClient,
                                           data,
                                           ora)
        except ValueError as ve:
            print(ve)
        except RezervareError as re:
            print(re)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiStergeRezervare(self):
        try:
            idRezervare = input("Dati id-ul rezervarii de sters: ")

            self.__rezervareService.sterge(idRezervare)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiModificaRezervare(self):
        try:
            idRezervare = input("Dati id-ul revervarii de modificat: ")
            idFilm = input("Dati id-ul noului film: ")
            idCardClient = input("Dati id-ul noului card: ")
            data = input("Dati noua data: ")
            ora = input("Dati noua ora la care incepe filmul: ")
            self.__rezervareService.modifica(idRezervare, idFilm,
                                             idCardClient, data, ora)

        except ValueError as ve:
            print(ve)
        except RezervareError as re:
            print(re)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def showAllRezervari(self):
        print(list(
            rezervare for rezervare in self.__rezervareService.getAll()))

    def uiCautareString(self):
        string = input("Dati stringul pe care doriti sa il cautati: ")

        list1 = self.__functionalitati.cautare1(string)
        list2 = self.__functionalitati.cautare2(string)

        print(list1)
        print(list2)

    def uiGenerareRandom(self):
        try:
            x = int(input("Dati numarul de filme pe care"
                          " doriti sa le generati: "))
            filme = ["Dune", "Spiderman", "Ironman", "Batman", "Apex", "007"]
            inprogram = ["DA", "NU"]
            listFilmAdd = []
            for i in range(x):
                idFilm = random.randint(1, 2000)
                titlu = random.choice(filme)
                anAparitie = random.randint(1990, 2021)
                pretBielt = random.randint(1, 60)
                inProgram = random.choice(inprogram)
                film = Film(str(idFilm), titlu, anAparitie, pretBielt,
                            inProgram)
                self.__filmService.adauga(film.idEntitate,
                                          film.titlu,
                                          film.anAparitie,
                                          film.pretBilet,
                                          film.inProgram)
                listFilmAdd.append(film)

        except ValueError as ve:
            print("Eroare: {}".format(ve))
        except Exception as e:
            print(e)

    def uiRezervariIntervalOre(self):
        try:
            ora1 = input("Dati ora de la care doriti sa"
                         " incepa intervalul(%H:%M): ")
            if datetime.strptime(ora1, '%H:%M') is False:
                raise ValueError
            ora2 = input("Dati ora de la care doriti sa"
                         " incepa intervalul(%H:%M): ")
            if datetime.strptime(ora2, '%H:%M') is False:
                raise ValueError
            rezultat = self.__rezervareService.afisRezervariIntervalOre(ora1,
                                                                        ora2)
            for rezervari in rezultat:
                print(rezervari)
        except ValueError as ve:
            print("Eroare: {}".format(ve))
        except Exception as e:
            print(e)

    def uiFilmeDescDupaNrRezervari(self):
        for film in self.__rezervareService.ordoneazaFilmeDupaNrDeRezervari():
            print(film)

    def uiCarduriClientiDescDupaPuncteAcumulate(self):
        for card in self.__cardClientService.ordoneazaCardDupaPctAcum():
            print(card)

    def uiStergereRezervariInterval(self):
        try:
            data1 = input("Dati data de la care doriti sa"
                          " incepa intervalul(%d.%m.%Y): ")
            if datetime.strptime(data1, '%d.%m.%Y') is False:
                raise ValueError
            data2 = input("Dati data la care doriti sa se"
                          " sfarseasca intervalul(%d.%m.%Y): ")
            if datetime.strptime(data2, '%d.%m.%Y') is False:
                raise ValueError
            self.__rezervareService.stergereRezervariInterval(data1, data2)
        except ValueError as ve:
            print("Eroare: {}".format(ve))
        except Exception as e:
            print(e)

    def uiIncrementarePuncte(self):
        try:
            puncte = float(input("Dati numarul de puncte"
                                 " e care doriti sa il adaugati: "))
            data1 = input("Dati data de la care doriti"
                          " sa incepa intervalul(%d.%m): ")
            if datetime.strptime(data1, '%d.%m') is False:
                raise ValueError
            data2 = input("Dati data la care doriti sa se"
                          " sfarseasca intervalul(%d.%m): ")
            if datetime.strptime(data2, '%d.%m') is False:
                raise ValueError
            self.__cardClientService.incrementare(puncte, data1, data2)
        except ValueError as ve:
            print("Eroare: {}".format(ve))
        except Exception as e:
            print(e)

    def uiDeleteCascada(self):
        idfilm = input("Dati id-ul  filmului pe care doriti sa il stergeti"
                       "impreuna cu rezervarile legate de filmul care "
                       "contine id-ul: ")
        self.__rezervareService.deleteInCascada(idfilm)
