import unittest
from soup import html, geen_type
from bs4 import BeautifulSoup as soup
from process_soup import Process_soup

class mock_soup_element():
    def __init__(self, string):
        self.string = string

    def get_text(self):
        return self.string

class TestTicket(unittest.TestCase):
    def test_get_prices_and_transaction_stats(self):
        data = Process_soup(soup(html, "html.parser"))
        self.assertTrue(type(data.get_sold_ticket_prices()[0]) is int)
        self.assertTrue(type(data.get_transaction_stats()[0]) is int)

    def test_process_transaction_stats(self):
        data = Process_soup(soup(html, "html.parser"))
        self.assertTrue(data.process_sold_ticket_prices([mock_soup_element("$23,45")]) == [23])

    def test_process_transaction_stats_with_numeric_string(self):
        data = Process_soup(soup(html, "html.parser"))
        self.assertTrue(data.process_transaction_stats([mock_soup_element("15")]) == [15])

    def test_process_transaction_stats_with_non_numeric_string(self):
        data = Process_soup(soup(html, "html.parser"))
        self.assertTrue(data.process_transaction_stats([mock_soup_element("15l")]) == [])

    def test_get_average_price_without_noise(self):
        data = Process_soup(soup(geen_type, "html.parser"))
        self.assertTrue(data.ticket_type == "none")

