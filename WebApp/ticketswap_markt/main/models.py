from __future__ import unicode_literals
from djongo import models
import pymongo
from datetime import datetime
import pytz


class Events:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://rik:Yanntiersen1970!@cluster1.rondo.mongodb.net/Lowlands_Festival_2020?retryWrites=true&w=majority")
        self.databases = self.client.list_database_names()
        self.databases = self.databases[:len(self.databases) - 2]
        self.most_wanted_event = {'name': None, 'wanted_tickets': 0}
        self.future_events = []
        self.passed_events = []
        self.process_dbs()

    def get_events(self):
        return sorted([event.replace("_", " ") for event in self.future_events])

    def get_passed_events(self):
        return self.passed_events

    def get_documents(self, event=None):
        if event:
            db = self.client.get_database(event.get_event_name())
        else:
            db = self.client.get_database(self.get_name_most_wanted_event())
        collections = db.list_collection_names()
        records = db[collections[0]]
        return records.find()

    def process_dbs(self):
        event = self.databases.pop()
        db = self.client.get_database(event)
        collections = db.list_collection_names()
        self.process_collections(collections, db, event)

    def process_collections(self, collections, db, event):
        records = db[collections[0]]
        document = records.find_one(sort=[('_id', pymongo.DESCENDING)])

        tz = pytz.timezone('Europe/Berlin')
        now = datetime(2020, 3,3)
        dt_string = now.strftime("%d/%m/%Y %H:%M")

        scrape_time_event = datetime.strptime(document.get("time"), "%d/%m/%Y %H:%M")
        now = datetime.strptime(dt_string, "%d/%m/%Y %H:%M")

        difference = now - scrape_time_event
        if difference.total_seconds()/3600 > 2:
            self.passed_events.append(event)
        else:
            self.future_events.append(event)
        self.update_most_wanted_event(document.get("searched_tickets"), event)

    def update_most_wanted_event(self, this_event_nr_of_wanted_tickets, event_name):
        if self.nr_of_wanted_tickets_most_wanted_event() < this_event_nr_of_wanted_tickets:
            self.set_new_most_wanted_event(event_name, this_event_nr_of_wanted_tickets)
        if self.databases:
            self.process_dbs()

    def nr_of_wanted_tickets_most_wanted_event(self):
        return self.most_wanted_event.get("wanted_tickets")

    def get_name_most_wanted_event(self):
        return self.most_wanted_event.get("name")

    def set_new_most_wanted_event(self, name, wanted_tickets):
        self.most_wanted_event["name"] = name
        self.most_wanted_event["wanted_tickets"] = wanted_tickets

    def get_event_name(self):
        return self.get_name_most_wanted_event()


class Chosen_event(Events):
    def __init__(self, name):
        super().__init__()
        self.name = name.replace(" ", "_")

    def get_event_name(self):
        return self.name


def advice(event):
    event = Chosen_event(event)
    documents = event.get_documents()

    return documents


def query_event(event=None):

    if not event:
        event = Events()
        documents = event.get_documents()
    else:
        event = Chosen_event(event)
        documents = event.get_documents(event)

    prices, times, for_sale, searched, sold, full_times = ([] for i in range(6))

    for elem in documents:
        prices.append(elem.get("price"))
        for_sale.append(elem.get("for_sale"))
        times.append(int(elem.get("time").split(" ")[1][:2]))
        searched.append(elem.get("searched_tickets"))
        sold.append(elem.get("sold"))

    return {'name': event.get_event_name().replace("_", " "), 'times': times, 'prices': prices, 'for_sale': for_sale, 'sold': sold, 'searched': searched,
            'now_sold': sold[len(sold) - 1], 'now_searched': searched[len(searched) - 1], 'now_for_sale': for_sale[len(for_sale) - 1],
            'price_now': prices[len(prices) - 1]}


def query_events():
    events = Events()

    return events.get_events()


def query_last_price_event(event):
    client = pymongo.MongoClient(
        "mongodb+srv://rik:Yanntiersen1970!@cluster1.rondo.mongodb.net/Cluster1?retryWrites=true&w=majority")
    db = client.get_database(event)
    collections = db.list_collection_names()
    records = db[collections[0]]
    documents = records.find(sort=[('_id', pymongo.DESCENDING)])

    return documents[0].get('price')

class Event(models.Model):
    user = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)
    nr_of_tickets_bought = models.IntegerField(null=True)
    price = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    user = models.CharField(max_length=50, null=True)
    event = models.CharField(max_length=50, null=True)
    nr_of_tickets_bought = models.IntegerField(null=True)
    original_price = models.IntegerField(null=True)
    current_price = models.IntegerField(null=True)
    profit = models.IntegerField(null=True)

    def __str__(self):
        return self.event
