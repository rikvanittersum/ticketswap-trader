from .document import Document

class Top_documents:
    def __init__(self, documents):
        self.documents = documents

        self.document_with_highest_price = None
        self.document_with_highest_sold_searched_ratio = None
        self.document_most_sold = None
        self.document_highest_increase_in_demand = None

        self.sales_increase = 0
        self.increase_in_demand = 0

        self.new_document = None
        self.last_document = None

        self.document_list = []

        self.process_documents()

        for event in self.document_list:
            self.get_best_documents()

    def process_documents(self):
        for document in self.documents:
            self.document_list.append(document)


    def get_best_documents(self):
        if self.document_list:
            self.new_document = Document(self.document_list.pop(0))
            return self.compare_prices_documents()

    def compare_prices_documents(self):
        if self.is_not_first_document():
            if self.document_with_highest_price.get_price() < self.new_document.get_price():
                self.document_with_highest_price = self.new_document
        else:
            self.document_with_highest_price = self.new_document

        return self.compare_sold_search_ratio()

    def compare_sold_search_ratio(self):
        if self.is_not_first_document():
            if self.document_with_highest_sold_searched_ratio.get_supply_demand_ratio() < self.new_document.get_supply_demand_ratio():
                self.document_with_highest_sold_searched_ratio = self.new_document
        else:
            self.document_with_highest_sold_searched_ratio = self.new_document

        return self.compare_most_sold_in_an_hour()

    def compare_most_sold_in_an_hour(self):
        if self.is_not_first_document():
            if self.sales_increase < self.new_document_increase_in_sales():
                self.document_most_sold = self.new_document
                self.sales_increase = self.new_document_increase_in_sales()

        return self.compare_document_highest_increase_in_demand()

    def compare_document_highest_increase_in_demand(self):
        if self.is_not_first_document():
            if self.increase_in_demand < self.new_document_increase_in_demand():
                self.document_highest_increase_in_demand = self.new_document
                self.increase_in_demand = self.new_document_increase_in_demand()

        self.last_document = self.new_document

    def get_best_time_to_sell(self):
        return self.document_with_highest_price.get_time()

    def get_time_highest_demand_to_supply_ratio(self):
        return self.document_with_highest_sold_searched_ratio.get_time()

    def get_time_highest_sold_ratio(self):
        return self.document_most_sold.get_time()

    def get_time_highest_increase_in_searched_tickets(self):
        return self.document_highest_increase_in_demand.get_time()

    def get_highest_price(self):
        return self.document_with_highest_price.get_price()


    def new_document_increase_in_demand(self):
        return self.new_document.get_searched() - self.last_document.get_searched()

    def new_document_increase_in_sales(self):
        return self.new_document.get_sold() - self.last_document.get_sold()

    def is_not_first_document(self):
        if self.last_document:
            return True
        return False

