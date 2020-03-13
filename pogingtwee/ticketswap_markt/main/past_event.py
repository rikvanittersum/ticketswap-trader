class Past_event:
    def __init__(self, documents, original_price=None):
        self.documents = documents

        self.best_selling_document = None
        self.document_with_best_price = None
        self.document_highest_sold_increase = None
        self.document_with_best_ratio = None
        self.document_highest_searched_increase = None

        if original_price:
            self.original_price = original_price

        ratio = 0
        highest_searched_increase = 0
        last_searched_stat = 0
        highest_price = 0
        demand = 0
        highest_sold_increase = 0
        last_sold_stat = 0

        for document in self.documents:
            document_price = document.get("price")
            document_demand = document.get("searched_tickets")
            searched_tickets_this_hour = document.get("searched_tickets")
            tickets_for_sale = document.get("for_sale")
            sold_this_hour = document.get("sold")

            sold_increase_now = sold_this_hour - last_sold_stat

            if document_price > highest_price:
                self.document_with_best_price = document
                highest_price = document_price
                demand = document_demand

            if document_price == highest_price and document_demand > demand:
                self.document_with_best_price = document
                demand = document_demand

            if tickets_for_sale == 0:
                this_ratio = searched_tickets_this_hour + 1
            else:
                this_ratio = searched_tickets_this_hour / tickets_for_sale

            if this_ratio > ratio:
                self.document_with_best_ratio = document
                ratio = this_ratio

            if sold_increase_now > highest_sold_increase:
                highest_sold_increase = sold_increase_now
                self.document_highest_sold_increase = document

            searched_increase_now = searched_tickets_this_hour - last_searched_stat
            if searched_increase_now > highest_searched_increase:
                highest_searched_increase = searched_increase_now
                self.document_highest_searched_increase = document

            last_sold_stat = sold_this_hour
            last_searched_stat = searched_tickets_this_hour


    def get_time_highest_price(self):
        return self.document_with_best_price

    def get_price_of_ticket_sold_at_best_time(self):
        return self.document_with_best_price.get('price') * .95

    def get_time_highest_demand_to_supply_ratio(self):

        return self.document_with_best_ratio.get('time')

    def get_time_highest_sold_ratio(self):

        return self.document_highest_sold_increase.get("time")

    def get_time_highest_increase_in_searched_tickets(self):

        return self.document_highest_searched_increase.get("time")






