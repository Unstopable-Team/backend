import pandas as pd
from entsoe import EntsoePandasClient


class EntsoeClient:
    def __init__(self, token):
        self.client = EntsoePandasClient(api_key=token)

    def get_unavailability_production(self, country_code, start_date, end_date):
        """
        Get unavailability of production units (whatever that is)
        :param country_code: iso code of country
        :param start_date: epoch time of start in ms
        :param end_date: epoch time of end in ms
        :return: pandas dataframe with the requested data
        """
        start_date = pd.Timestamp(start_date, unit="ms", tz="CET")
        end_date = pd.Timestamp(end_date, unit="ms", tz="CET")

        return self.client.query_unavailability_of_production_units(country_code.upper(), start=start_date,
                                                                    end=end_date)

    def get_cross_border_flow(self, country_from, country_to, start_date, end_date):
        start_date = pd.Timestamp(start_date, unit="ms", tz="CET")
        end_date = pd.Timestamp(end_date, unit="ms", tz="CET")

        return self.client.query_crossborder_flows(country_code_from=country_from.upper(),
                                                   country_code_to=country_to.upper(),
                                                   start=start_date,
                                                   end=end_date)

    def get_forecasted_transfer(self, country_from, country_to, start_date, end_date):
        """
        Net capacity transfer for the day ahead between the 2 countries
        :param country_from:
        :param country_to:
        :param start_date:
        :param end_date:
        :return:
        """
        start_date = pd.Timestamp(start_date, unit="ms", tz="CET")
        end_date = pd.Timestamp(end_date, unit="ms", tz="CET")
        return self.client.query_net_transfer_capacity_dayahead(country_code_from=country_from.upper(),
                                                                country_code_to=country_to.upper(),
                                                                start=start_date,
                                                                end=end_date)
