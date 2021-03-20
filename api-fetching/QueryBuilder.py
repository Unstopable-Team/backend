class QueryBuilder:
    def __init__(self):
        self.query = {}

    def add_area(self, area):
        """
        ISO names. Accepts only one, except if the exc (exchange) category is present, then it makes 2
        :param area:
        :return:
        """
        if ("category", "exc") in self.query.items() and "area" in self.query:
            self.query["area"] += "," + area
        else:
            self.query["area"] = area

    def add_category(self, category):
        if "category" in self.query:
            self.query["category"] += "," + category
        else:
            self.query["category"] = category

    def get_query(self):
        final_query = self.query.copy()
        self.query = {}
        return final_query
