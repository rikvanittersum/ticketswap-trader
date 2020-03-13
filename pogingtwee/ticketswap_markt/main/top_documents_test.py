import unittest
from ticketswap_markt.main.top_documents import Top_documents


class MyTestCase(unittest.TestCase):
    def test_best_time_to_sell_with_with_unequal_price(self):
        self.assertTrue(Top_documents([{'searched_tickets': 200, 'for_sale': 0, 'price': 100, 'time': '12:00', 'sold': 100},
                                    {'searched_tickets': 300, 'for_sale': 0, 'price': 80, 'time': '13:00', 'sold': 100}]).get_best_time_to_sell() == "12:00")

    def test_best_time_to_sell_with_with_equal_price(self):
        self.assertTrue(Top_documents([{'searched_tickets': 200, 'for_sale': 0, 'price': 100, 'time': '12:00', 'sold': 100},
                                    {'searched_tickets': 300, 'for_sale': 0, 'price': 100, 'time': '13:00', 'sold': 100}]).get_best_time_to_sell() == "12:00")

    def test_get_profit_on_ticket_sold_at_best_time(self):
        self.assertTrue(Top_documents([{'searched_tickets': 200, 'for_sale': 0, 'price': 100, 'time': '12:00', 'sold': 100},
                                    {'searched_tickets': 300, 'for_sale': 0, 'price': 20, 'time': '13:00', 'sold': 100}], 90).get_profit_on_ticket_sold_at_best_time() == 5)

    def test_highest_demand_to_supply_ratio(self):
        self.assertTrue(Top_documents([{'searched_tickets': 200, 'for_sale': 0, 'price': 100, 'time': '12:00', 'sold': 100},
                                    {'searched_tickets': 200, 'for_sale': 1, 'price': 20, 'time': '13:00', 'sold': 100}]).get_time_highest_demand_to_supply_ratio() == "12:00")

    def test_time_highest_sell_ratio(self):
        self.assertTrue(Top_documents([{'searched_tickets': 200, 'for_sale': 0, 'price': 100, 'time': '12:00', 'sold': 0},
                                    {'searched_tickets': 200, 'for_sale': 0, 'price': 100, 'time': '13:00', 'sold': 100},
                                    {'searched_tickets': 200, 'for_sale': 1, 'price': 100, 'time': '14:00', 'sold': 201}]).get_time_highest_sold_ratio() == "14:00")

    def test_time_highest_increase_in_searched_tickets(self):
        self.assertTrue(Top_documents([{'searched_tickets': 0, 'for_sale': 0, 'price': 100, 'time': '12:00', 'sold': 0},
                                    {'searched_tickets': 200, 'for_sale': 0, 'price': 100, 'time': '13:00', 'sold': 100},
                                    {'searched_tickets': 399, 'for_sale': 1, 'price': 100, 'time': '14:00', 'sold': 201}]).get_time_highest_increase_in_searched_tickets() == "13:00")

if __name__ == '__main__':
    unittest.main()
