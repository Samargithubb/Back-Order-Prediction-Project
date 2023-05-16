"""
This is the Entry point for Training the Machine Learning Model.

Version: 1.0
Revisions: None

"""
# Doing the necessary imports

from sklearn.model_selection import train_test_split
from Data_Ingestion import data_loader
from Data_Preprocessing import preprocessing
from Model_Finder import tuner
from File_Operations import file_methods
from Application_logging import logger
import numpy as np
import pandas as pd
import os


class trainModel:

    def __init__(self):
        self.file_object = open("Training_Logs/ModelTrainingLog.txt", 'a+')
        self.log_writer = logger.App_Logger()

    def trainingModel(self):
        # Logging the start of Training
        self.log_writer.log(self.file_object, 'Start of Training')
        try:
            # Getting the data from the source
            data_getter = data_loader.DataGetter(self.file_object, self.log_writer)
            data = data_getter.get_data()

            """ Doing Data Preprocessing"""
            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)
            # Remove the unnamed column as it doesn't contribute to prediction
            data = preprocessor.remove_columns(data,
                                               ["sku", "national_inv", "in_transit_qty", "min_bank",
                                                "potential_issue",
                                                "pieces_past_due", "local_bo_qty", "deck_risk", "oe_constraint",
                                                "ppap_risk", "stop_auto_buy", "rev_stop"])

            # Check if missing values are present in the dataset
            is_null_present, cols_with_missing_values = preprocessor.is_null_present(data)
            self.log_writer.log(self.file_object, 'Is Null Values Present :' + str(is_null_present))

            # if missing values are there, replace them appropriately.
            if (is_null_present):
                data = preprocessor.impute_missing_values(
                    data, cols_with_missing_values)

            # create separate features and labels
            X, Y = preprocessor.separate_label_feature(
                data, label_column_name='went_on_backorder')

            # encoding the label column
            Y = Y.map({'No': 0, 'Yes': 1})

            # Scale the numerical data
            X = preprocessor.scale_numerical_columns(X)

            # Convert categorical values to numeric values
            X = preprocessor.encode_categorical_columns(X)

            # Imba lanced dataset to make it a balanced one
            X, Y = preprocessor.handle_imbalanced_dataset(X, Y)

            # Splitting the data into train and test
            x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=1 / 3, random_state=2)

            # Finding the best model
            model_finder = tuner.Model_Finder(self.file_object, self.log_writer)
            best_model_name, best_model = model_finder.get_best_model(x_train, y_train, x_test, y_test)

            # saving the best model to the directory.
            file_op = file_methods.File_Operation(self.file_object, self.log_writer)
            save_model = file_op.save_model(best_model, best_model_name)

            # logging the successful Training
            self.log_writer.log(self.file_object, 'Successful End of Training')
            self.file_object.close()

        except Exception as e:
            # logging the unsuccessful Training
            self.log_writer.log(self.file_object, 'Unsuccessful End of Training')
            self.file_object.close()
            raise Exception
