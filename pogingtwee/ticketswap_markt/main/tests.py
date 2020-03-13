from django.test import TestCase
from .models import query_top_event

# Create your tests here.

class test_queries(TestCase):

    #def test_int_times(self):
        #data_top_event = query_top_event()
        #self.assertTrue(type(data_top_event.get('times')[0]) == int)

    def test_get_top_event(self):
        data_top_event = query_top_event([{'name': 'naam1', 'price': 120, 'searched_tickets': 1000, 'time': "gg 12:00"},
                                          {'name': 'naam2', 'price': 10, 'searched_tickets': 10, 'time':"gg 12:00"}])
        self.assertTrue(data_top_event.get('name') == "naam1")





