class Ticket:

    def __init__(self, processed_soup):
        self.processed_soup = processed_soup

    def get_event_name(self):
        return self.processed_soup.get_event_name().replace(" ","_" )

    def get_ticket(self):
        return self.processed_soup.get_ticket_type()

    def get_tickets_for_sale(self):
        return self.processed_soup.get_transaction_stats()[0]

    def get_sold_tickets(self):
        return self.processed_soup.get_transaction_stats()[1]

    def get_searched_tickets(self):
        return self.processed_soup.get_transaction_stats()[2]

    def get_average_sold_price(self):
        len_sold_tickets_list = len(self.processed_soup.get_sold_ticket_prices())
        if len_sold_tickets_list > 0:
            clean_sold_tickets_list = []
            maximum = max(self.processed_soup.get_sold_ticket_prices())
            for ticket_price in self.processed_soup.get_sold_ticket_prices():
                if maximum / ticket_price < 3:
                    clean_sold_tickets_list.append(ticket_price)

            return round(sum(clean_sold_tickets_list) / len(clean_sold_tickets_list), 2)
        else:
            return len_sold_tickets_list




