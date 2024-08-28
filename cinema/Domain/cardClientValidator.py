from datetime import datetime
from Domain.cardClient import CardClient
from Domain.cardClientError import CardClientError


class CardClientValidator:
    def valideaza(self, cardClient: CardClient):
        try:
            datetime.strptime(cardClient.dataNasterii, '%d.%m.%Y')
            datetime.strptime(cardClient.dataInregistrarii, '%d.%m.%Y')
        except ValueError:
            raise CardClientError("Formatul datei trebuie sa fie: DD.MM.YYYY")
