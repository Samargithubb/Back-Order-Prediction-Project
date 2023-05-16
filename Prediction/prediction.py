import pandas as pd
import pickle
import os
from File_Operations import file_methods
from Data_Preprocessing import preprocessing
from Data_Ingestion import data_loader_prediction
from Application_logging import logger


class Prediction:
    def __init__(self):
        self.file_object = open("Prediction_Logs/Prediction_log.txt", 'a+')
        self.log_writer = logger.App_Logger()

    def predictionFromModel(self):

        try:
            self.log_writer.log(self.file_object, 'Start of the Prediction')
            data_getter = data_loader_prediction.Data_Getter_Pred(self.file_object, self.log_writer)
            data = data_getter.get_data()

            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)
            # removing these columns as it doesn't contribute to prediction.
            data = preprocessor.remove_columns(data,
                                               ["sku", "national_inv", "in_transit_qty", "min_bank",
                                                "potential_issue",
                                                "pieces_past_due", "local_bo_qty", "deck_risk", "oe_constraint",
                                                "ppap_risk", "stop_auto_buy", "rev_stop","went_on_backorder"])
            # Check if missing values are present in the dataset
            is_null_present, cols_with_missing_values = preprocessor.is_null_present(data)
            self.log_writer.log(self.file_object, 'Is Null Values Present :' + str(is_null_present))

            # # if missing values are there, replace them appropriately.
            if (is_null_present):
                data = preprocessor.impute_missing_values(
                    data, cols_with_missing_values)

            # Scale the numerical data
            with open('scale/scalingModel.pkl', 'rb') as f:
                scaler = pickle.load(f)
            # Convert DataFrame to numpy ndarray
            data_array = data.to_numpy()

            # Scale the data using the loaded scaler
            scaled_data = scaler.transform(data_array)

            # Convert the scaled data back to a pandas DataFrame
            self.data = pd.DataFrame(scaled_data, columns=data.columns)

            # Convert categorical values to numeric values
            self.data = preprocessor.encode_categorical_columns(self.data)

            file_loader = file_methods.File_Operation(self.file_object, self.log_writer)
            model_name = file_loader.find_correct_model_file()
            model = file_loader.load_model(model_name)
            result = list(model.predict(data))

            result = pd.DataFrame(result, columns=['Prediction'])
            result['Prediction'] = result['Prediction'].map(
                {0: 'No', 1: "Yes"})

            path = "Prediction_Output_File"
            os.makedirs(path, exist_ok=True)
            result.to_csv("Prediction_Output_File/Predictions.csv",
                          header=True)
            self.log_writer.log(self.file_object, 'End of Prediction')

        except Exception as e:
            self.log_writer.log(self.file_object, 'Error occured while running the prediction!! Error:: %s' % e)
            raise e
        return path
