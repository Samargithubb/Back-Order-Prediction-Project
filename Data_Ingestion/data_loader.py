import pandas as pd
from Application_logging import logger


class DataGetter:
    """
        This class shall  be used for obtaining the data from the source for training.
        Version: 1.0
        Revisions: None

        """

    def __init__(self, file_object, logger_object):
        self.training_file = 'Training_FileFromDB/train_data.csv'
        self.test_file = "Test_FileFromDB/test.csv"
        self.file_object = file_object
        self.logger_object = logger_object

    def get_data(self):
        """
        This class shall  be used for obtaining the data from the source for training.
        Version: 1.0
        Revisions: None

        """
        self.logger_object.log(self.file_object, 'Entered the get_data method of the Data_Getter class')
        try:

            df_train = pd.read_csv(self.training_file)
            df_test = pd.read_csv(self.test_file)
            self.data = pd.concat([df_train, df_test])
            self.logger_object.log(self.file_object,
                                   'Data Load Successful.Exited the get_data method of the Data_Getter class')
            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in get_data method of the Data_Getter class. Exception message: '
                                   + str(e))
            self.logger_object.log(self.file_object,
                                   'Data Load Unsuccessful.Exited the get_data method of the Data_Getter class')
            raise Exception()
