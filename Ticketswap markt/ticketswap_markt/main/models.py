from __future__ import unicode_literals
from djongo import models
import pymongo

class Events:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://rik:Yanntiersen1970!@cluster0-ebw47.mongodb.net/test?retryWrites=true&w=majority")
        self.databases = self.client.list_database_names()
        self.databases = self.databases[:len(self.databases) - 2]

    def get_events(self):
        self.databases = [event.replace("_", " ") for event in self.databases]
        return self.databases

    def get_documents(self):
        db = self.client.get_database(self.name)
        collections = db.list_collection_names()
        records = db[collections[0]]
        return records.find()


class Most_wanted_event(Events):
    def __init__(self):
        super().__init__()
        self.name = None
        self.nr_of_wanted_tickets = 0
        self.process_dbs()

    def process_dbs(self):
        event = self.databases.pop()
        db = self.client.get_database(event)
        collections = db.list_collection_names()
        self.process_collections(collections, db, event)

    def process_collections(self, collections, db, event):
        records = db[collections[0]]
        document = records.find_one(sort=[( '_id', pymongo.DESCENDING)])
        self.update_most_wanted_event(document.get("searched_tickets"), event)

    def update_most_wanted_event(self, document, event):
        if self.nr_of_wanted_tickets < document:
            self.name = event
            self.nr_of_wanted_tickets = document

        if self.databases:
            self.process_dbs()

class chosen_event(Events):
    def __init__(self, name):
        super().__init__()
        self.name = name.replace(" ", "_")

def query_event(event=None):

    if not event:
        event = Most_wanted_event()
    else:
        event = chosen_event(event)

    prices, times, for_sale, searched, sold = ([] for i in range(5))

    for elem in event.get_documents():
        prices.append(elem.get("price"))
        for_sale.append(elem.get("for_sale"))
        times.append(int(elem.get("time").split(" ")[1][:2]))
        searched.append(elem.get("searched_tickets"))
        sold.append(elem.get("sold"))

    return {'name': event.name.replace("_", " "), 'times': times, 'prices':prices, 'for_sale': for_sale, 'sold': sold, 'searched': searched,
            'now_sold': sold[len(sold) - 1], 'now_searched': searched[len(searched) - 1], 'now_for_sale': for_sale[len(for_sale) - 1],
            'price_now': prices[len(prices) - 1]}

def query_events():
    events = Events()
    return events.get_events()


class Event(models.Model):
    user = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)
    nr_of_tickets_bought = models.IntegerField(null=True)
    price = models.IntegerField(null=True)

    def __str__(self):
        return self.name
