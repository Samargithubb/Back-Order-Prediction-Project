import csv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import BatchStatement
import os
import shutil
from os import listdir
from Application_logging.logger import App_Logger

class dBOperation:
    """
    This class shalle be used for handling all the DataStax Cassandra Operation.
    Version: 1.0
    Revisions: None
    """

    def __init(self):
        self.path = 'Prediction_Database/'
        self.logger = App_Logger()

    def dataBaseConnection(self,DatabaseName):
        """
        Method Name: dataBaseConnection Description: This method creates the database with the given name and if
                                                     Database already exists then opens the connection to the DB.
        Output: Connection to the DB On Failure: Raise ConnectionError

        Version: 1.0
        Revisions: None
        """
        try:
            cloud_config = {
                'secure_connect_bundle': 'C:\\Users\\samar\\PycharmProjects\\Back-Order-Prediction\\secure-connect-mydatabase (1).zip'
            }

            auth_provider = PlainTextAuthProvider('WoISKQTTnrPevtLwSIJbLSfr',
                                                  'crJ.wEE__N,8gWtuQiszS7YCivefjnN6oXyPUp1Ku.+mO3r.iAaU3tPQtXpt4K9ra22Zu,0UiFgSnQYa8NtJK1UYyMoDdQnucCXdyW_2a_b5JZC6PCL7Dggf_xNMniBi')
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session = cluster.connect('backorderprediction')
            file = open("Prediction_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Opened %s database successfully")
            file.close()
            session.execute("""
                CREATE TABLE IF NOT EXISTS train_data1 (
                    sku int PRIMARY KEY,
                    national_inv float,
                    lead_time float,
                    in_transit_qty float,
                    forecast_3_month float,
                    forecast_6_month float,
                    forecast_9_month float,
                    sales_1_month float,
                    sales_3_month float,
                    sales_6_month float,
                    sales_9_month float,
                    min_bank float,
                    potential_issue text,
                    pieces_past_due float,
                    perf_6_month_avg float,
                    perf_12_month_avg float,
                    local_bo_qty float,
                    deck_risk text,
                    oe_constraint text,
                    ppap_risk text,
                    stop_auto_buy text,
                    rev_stop text,
                    went_on_backorder text
                );
            """)

            # Prepare the insert statement
            insert_statement = session.prepare("""
                INSERT INTO train_data1 (
                    sku, national_inv, lead_time, in_transit_qty,
                    forecast_3_month, forecast_6_month, forecast_9_month, sales_1_month,
                    sales_3_month, sales_6_month, sales_9_month, min_bank, potential_issue,
                    pieces_past_due, perf_6_month_avg, perf_12_month_avg, local_bo_qty,
                    deck_risk, oe_constraint, ppap_risk, stop_auto_buy, rev_stop,
                    went_on_backorder
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                );
            """)

            # Create a BatchStatement
            batch = BatchStatement()

            with open('Data/Kaggle_Training_Dataset_v2.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    sku_str = row['sku']
                    if not sku_str.isdigit():
                        continue  # skip this row if sku value is not a valid integer
                    params = (
                        int(row['sku']),
                        float(row.get('national_inv')),
                        float(row['lead_time']) if row['lead_time'] != '' else None,
                        float(row.get('in_transit_qty')),
                        float(row.get('forecast_3_month')),
                        float(row.get('forecast_6_month')),
                        float(row.get('forecast_9_month')),
                        float(row.get('sales_1_month')),
                        float(row.get('sales_3_month')),
                        float(row.get('sales_6_month')),
                        float(row.get('sales_9_month')),
                        float(row.get('min_bank')),
                        row.get('potential_issue'),
                        float(row.get('pieces_past_due')),
                        float(row.get('perf_6_month_avg')),
                        float(row.get('perf_12_month_avg')),
                        float(row.get('local_bo_qty')),
                        row.get('deck_risk'),
                        row.get('oe_constraint'),
                        row.get('ppap_risk'),
                        row.get('stop_auto_buy'),
                        row.get('rev_stop'),
                        row.get('went_on_backorder')
                    )
                    bound_statement = insert_statement.bind(params)

                    # Add the bound statement to the batch
                    batch.add(bound_statement)

                    # Execute the batch every 1000 rows
                    if len(batch) == 1000:
                        session.execute(batch)
                        batch.clear()

            # Execute any remaining statements in the batch
            if batch:
                session.execute(batch)
        except ConnectionError:
            raise ConnectionError

