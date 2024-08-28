from Tests.testDomain import testDomainCardClient,\
    testDomainFilm,\
    testDomainRezervare
from Tests.testRepositoryJson import testFilmRepositoryJson,\
    testCardClientRepositoryJson,\
    testRezervareRepositoryJson
from Tests.testService import testFilmService,\
    testCardClientService, testRezervareService
from Tests.testfunctionalitati import testFunctionalitati


def runTests():
    testDomainFilm()
    testDomainCardClient()
    testDomainRezervare()
    testFilmRepositoryJson()
    testCardClientRepositoryJson()
    testRezervareRepositoryJson()
    testFilmService()
    testCardClientService()
    testRezervareService()
    testFunctionalitati()
