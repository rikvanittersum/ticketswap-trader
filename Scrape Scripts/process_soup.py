# encoding: utf-8

class Process_soup:
    def __init__(self, soup):
        self.soup = soup
        self.event_name = self.soup.find("h1", {"class": "css-54iqnz e149jiyc0"}).get_text()

        ticket_type = self.soup.find("h2", {"class": "css-7kic73 e1hbno2b0"})
        if ticket_type:
            self.ticket_type = ticket_type.get_text()
        else:
            self.ticket_type = "none"

        self.transaction_stats = self.process_transaction_stats(self.soup.findAll("span", {"class": "css-v0hcsa e7cn512"}))
        self.sold_ticket_prices = self.process_sold_ticket_prices(self.soup.findAll("strong", {"class": "css-wc0tnl e1pkfxq10"}))

    def process_transaction_stats(self, list):
        numbers = []
        for transaction_stat in list:
            if transaction_stat.get_text().split()[0].isnumeric():
                numbers.append(int(transaction_stat.get_text().split()[0]))
        return numbers

    def process_sold_ticket_prices(self, list):
        numbers = []

        for price_stat in list:
            price_stat = price_stat.get_text()
            numbers.append(int(price_stat[1:].split(',', 1)[0]))
        return numbers

    def get_event_name(self):
        return self.event_name

    def get_ticket_type(self):
        return self.ticket_type

    def get_sold_ticket_prices(self):
        return self.sold_ticket_prices

    def get_transaction_stats(self):
        return self.transaction_stats
