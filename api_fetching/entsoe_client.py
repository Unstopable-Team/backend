import pandas as pd
from entsoe import EntsoePandasClient


class EntsoeClient:
    def __init__(self, token):
        self.client = EntsoePandasClient(api_key=token)

    def get_unavailability_production(self, country_code, start_date, end_date):
        start_date = pd.Timestamp(start_date, unit="ms", tz="CET")
        end_date = pd.Timestamp(end_date, unit="ms", tz="CET")

        return self.client.query_unavailability_of_production_units(country_code.upper(), start=start_date, end=end_date)

    def get_cross_border_flow(self, country_from, country_to, start_date, end_date):
        start_date = pd.Timestamp(start_date, unit="ms", tz="CET")
        end_date = pd.Timestamp(end_date, unit="ms", tz="CET")

        return self.client.query_crossborder_flows(country_code_from=country_from.upper(),
                                                   country_code_to=country_to.upper(),
                                                   start=start_date,
                                                   end=end_date)
