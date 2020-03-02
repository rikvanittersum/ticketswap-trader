import unittest
from ticket import Ticket
import urllib3
from soup import html, geen_type
from bs4 import BeautifulSoup as soup
from process_soup import Process_soup

def make_processed_soup(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    return Process_soup(soup(response.data, "html.parser"))

class mock_ticket():
    def __init__(self):
        pass

    def get_avarage_sold_price(self, sold_tickets_list):
        if len(sold_tickets_list) > 0:
            return round(200 / len(sold_tickets_list), 2)
        else:
            return 0

class TestTicket(unittest.TestCase):
    def test_name_ticket(self):
        lowlands = Ticket(make_processed_soup('https://www.ticketswap.nl/event/lowlands-festival-2020/weekend-tickets/03156ec9-7774-4c70-88aa-0716cb30438c/1588534'))
        self.assertTrue(lowlands.get_event_name() == "Lowlands_Festival_2020")
        self.assertTrue(lowlands.get_ticket() == "Weekend")

    def test_sold_tickets_divide_by_zero(self):
        ticket = mock_ticket()
        self.assertTrue(ticket.get_avarage_sold_price([]) == 0)

    def test_sold_tickets_divide_by_non_zero(self):
        ticket = mock_ticket()

        self.assertTrue(ticket.get_avarage_sold_price([200]) == 200 / len([200]))

    def test_fog_in_average(self):
        test = Process_soup(soup(html, "html.parser"))
        test.sold_ticket_prices = [14, 16, 18, 20, 20, 200, 200, 200, 200, 200]
        test = Ticket(test)
        self.assertTrue(test.get_average_sold_price() == 200)






if __name__ == '__main__':
    unittest.main()
