import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from imblearn.under_sampling import NearMiss
from sklearn.impute import SimpleImputer
import pickle


class Preprocessor:
    """
    This class shall  be used to clean and transform the data before training.
    Version: 1.0
    Revisions: None

    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def remove_columns(self, data, columns):
        """
        Method Name: remove_columns
        Description: This method removes the given columns from a pandas dataframe.
        Output: A pandas DataFrame after removing the specified columns.
        On Failure: Raise Exception
        Version: 1.0
        Revisions: None

        """
        self.logger_object.log(self.file_object, 'Entered the remove_columns method of the Preprocessor class')
        self.data = data
        self.columns = columns
        try:
            self.useful_data = self.data.drop(labels=self.columns, axis=1, errors='ignore')
            self.logger_object.log(self.file_object,
                                   'Column removal Successful.Exited the remove_columns method of the Preprocessor '
                                   'class')
            return self.useful_data
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in remove_columns method of the Preprocessor '
                                                     'class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'Column removal Unsuccessful. Exited the remove_columns method of '
                                                     'the Preprocessor class')
            raise Exception()

    def encode_categorical_columns(self, data):
        """
        Method Name: encode_categorical_columns
        Description: This method encodes the categorical values to numeric values.
        Output: only the columns with categorical values converted to numerical values
        On Failure: Raise Exception

        Version: 1.0
        Revisions: None
        """
        self.logger_object.log(self.file_object,
                               'Entered the encode_categorical_columns method of the Preprocessor class')
        try:
            # select only the categorical columns in the dataframe
            cat_columns = data.select_dtypes(include=['object']).columns
            if len(cat_columns) > 0:
                for col in cat_columns:
                    data[col] = data[col].replace({'No': 0, 'Yes': 1})
                    data[col] = data[col].astype(int)

            self.logger_object.log(self.file_object, 'encoding for categorical values successful. Exited the '
                                                     'encode_categorical_columns method of the Preprocessor class')
            return self.data

        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in encode_categorical_columns method of the '
                                                     'Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'encoding for categorical columns Failed. Exited the '
                                                     'encode_categorical_columns method of the Preprocessor class')
            raise Exception()

    def is_null_present(self, data):
        """
        Method Name: is_null_present
        Description: This method checks whether there are null values present in the pandas Dataframe or not.
        Output: Returns True if null values are present in the DataFrame, False if they are not present and
                returns the list of columns for which null values are present.
        On Failure: Raise Exception
        Version: 1.0
        Revisions: None

        """
        self.logger_object.log(self.file_object, 'Entered the is_null_present method of the Preprocessor class')
        self.null_present = False
        self.cols_with_missing_values = []
        self.cols = data.columns
        try:
            self.null_counts = data.isna().sum()  # check for the count of null values per column
            for i in range(len(self.null_counts)):
                if self.null_counts[i] > 0:
                    self.null_present = True
                    self.cols_with_missing_values.append(self.cols[i])
            if (self.null_present):
                self.dataframe_with_null = pd.DataFrame()
                self.dataframe_with_null['columns'] = data.columns
                self.dataframe_with_null['missing values count'] = np.asarray(data.isna().sum())
                self.dataframe_with_null.to_csv(
                    'preprocessing_data/null_values.csv')  # storing the null column information to file
            self.logger_object.log(self.file_object,
                                   'Finding missing values is a success.Data written to the null values file. Exited the is_null_present method of the Preprocessor class')
            return self.null_present, self.cols_with_missing_values
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in is_null_present method of the Preprocessor '
                                                     'class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'Finding missing values failed. Exited the is_null_present method '
                                                     'of the Preprocessor class')
            raise Exception()

    def impute_missing_values(self, data, cols_with_missing_values):
        """
                                        Method Name: impute_missing_values
                                        Description: This method replaces all the missing values in the Dataframe using KNNImputer.
                                        Output: A Dataframe which has all the missing values imputed.
                                        On Failure: Raise Exception

                                        Written By: iNeuron Intelligence
                                        Version: 1.0
                                        Revisions: None
                     """
        self.logger_object.log(self.file_object, 'Entered the impute_missing_values method of the Preprocessor class')
        self.data = data
        self.cols_with_missing_values = cols_with_missing_values
        try:
            self.imputer = SimpleImputer()
            for col in self.cols_with_missing_values:
                self.data[col] = self.imputer.fit_transform(self.data[[col]])
            self.logger_object.log(self.file_object,
                                   'Imputing missing values Successful. Exited the impute_missing_values method of the Preprocessor class')
            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in impute_missing_values method of the Preprocessor class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class')
            raise Exception()

    def separate_label_feature(self, data, label_column_name):
        """
        Method Name: separate_label_feature
        Description: This method separates the features and a Label Coulmns.
        Output: Returns two separate Dataframes, one containing features and the other containing Labels .
        On Failure: Raise Exception

        Version: 1.0
        Revisions: None

        """
        self.data = data
        self.column = label_column_name
        self.logger_object.log(self.file_object, 'Entered the separate_label_feature method of the Preprocessor class ')
        try:
            self.x = self.data.drop(labels=self.column, axis=1)
            self.y = self.data[self.column]
            self.logger_object.log(self.file_object,
                                   'Label Separation Successful. Exited the separate_label_feature method of the '
                                   'Preprocessor class')
            return self.x, self.y
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in separate_label_feature method of the Preprocessor class. '
                                   'Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Label Separation Unsuccessful. Exited the separate_label_feature method of the '
                                   'Preprocessor class')
            raise Exception()

    def scale_numerical_columns(self, data):
        """
        Method Name: scale_numerical_columns
        Description: This method transform the data into the scaled form Using RobustScaler which is robust to outliers.
        Output: Returns the scaled data .
        On Failure: Raise Exception

        Version: 1.0
        Revisions: None


        """
        self.logger_object.log(self.file_object, 'Entered the scale_numerical_columns method of the Preprocessor class')
        self.data = data

        try:
            path = 'scallingModel.pkl'
            self.df_scaled = self.data.copy()
            self.num_cols = self.data.select_dtypes(include=['int64', 'float64']).columns

            self.scaler = RobustScaler()
            self.df_scaled[self.num_cols] = self.scaler.fit_transform(self.df_scaled[self.num_cols])

            self.logger_object.log(self.file_object, 'Scale_numerical_columns name of the columns '
                                   + str(self.num_cols))

            with open('scale/scalingModel.pkl', 'wb') as f:
                pickle.dump(self.scaler, f)
            self.logger_object.log(self.file_object,
                                   'Scaling performed Successfully. Exited the Scale_numerical_columns'
                                   ' method of the Preprocessor class')
            return self.df_scaled

        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in Scale_numerical_columns method of'
                                                     ' the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'Finding missing values failed. Exited the Scale_numerical_columns'
                                                     ' method of the Preprocessor class')
            raise Exception()

    def handle_imbalanced_dataset(self, x, y):
        """
        Method Name: handle_imbalanced_dataset
        Description: This method handle the imbalanced data .
        Output: Returns the Balanced Dataset .
        On Failure: Raise Exception

        Version: 1.0
        Revisions: None

                """
        self.logger_object.log(self.file_object, 'Entered the handle_imbalanced_dataset method of the '
                                                 'Preprocessor class')
        try:
            self.NMSample = NearMiss()
            self.x_sampled, self.y_sampled = self.NMSample.fit_resample(x, y)
            self.logger_object.log(self.file_object, 'Balancing dataset Successful. Exited the '
                                                     'handle_imbalanced_dataset method of the Preprocessor class')
            return self.x_sampled, self.y_sampled

        except  Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in handle_imbalanced_dataset method of'
                                                     ' the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'Finding missing values failed. Exited the '
                                                     'handle_imbalanced_dataset method of the Preprocessor class')
            raise Exception()
