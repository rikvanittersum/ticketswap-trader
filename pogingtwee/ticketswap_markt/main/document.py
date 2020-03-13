class Document:
    def __init__(self, document):
        self.document = document

    def get_time(self):
        return self.document.get('time')

    def get_price(self):
        return self.document.get('price')

    def get_searched(self):
        return self.document.get('searched_tickets')

    def get_for_sale(self):
        return self.document.get('for_sale')

    def get_supply_demand_ratio(self):
        for_sale = self.get_for_sale()

        if (for_sale) == 0:
            return self.get_searched() + 1

        return self.get_searched() / for_sale

    def get_sold(self):
        return self.document.get('sold')
