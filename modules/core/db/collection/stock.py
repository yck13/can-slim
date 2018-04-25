from mongoengine import Document, StringField, EmbeddedDocument, EmbeddedDocumentListField, DateTimeField, DecimalField


# note: embedded document, not a collection on its own
class HistoricPrice(EmbeddedDocument):
    date = DateTimeField(required=True)
    price = DecimalField(required=True)
    meta = {
        'ordering': ['date']
    }


# stock collection
class Stock(Document):
    ticker = StringField(primary_key=True)
    name = StringField()
    historicPrices = EmbeddedDocumentListField(HistoricPrice)
    meta = {
        'indexes': ['ticker', 'name']
    }
