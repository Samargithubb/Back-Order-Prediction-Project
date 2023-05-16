from wsgiref import simple_server

import pandas as pd
from flask import Flask, request, render_template
import os
from flask import Response
from flask_cors import CORS, cross_origin
from Training.trainingModel import trainModel
from Prediction.prediction import Prediction

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        Input_data = request.get_json()
        sales_1_month = float(request.form['sales_1_month'])
        sales_3_month = float(request.form['sales_3_month'])
        sales_6_month = float(request.form['sales_6_month'])
        sales_9_month = float(request.form['sales_9_month'])
        forecast_3_month = float(request.form['forecast_3_month'])
        forecast_6_month = float(request.form['forecast_6_month'])
        forecast_9_month = float(request.form['forecast_9_month'])
        perf_6_month_avg = float(request.form['perf_6_month_avg'])
        perf_12_month_avg = float(request.form['perf_12_month_avg'])
        lead_time = float(request.form['lead_time'])

        input_df = pd.DataFrame({
            'lead_time': [lead_time],
            'forecast_3_month': [forecast_3_month],
            'forecast_6_month': [forecast_6_month],
            'forecast_9_month': [forecast_9_month],
            'sales_1_month': [sales_1_month],
            'sales_3_month': [sales_3_month],
            'sales_6_month': [sales_6_month],
            'sales_9_month': [sales_9_month],
            'perf_6_month_avg': [perf_6_month_avg],
            'perf_12_month_avg': [perf_12_month_avg]
        })

        input_df.to_csv("Prediction_FileFromDB/InputFile.csv", index=False)

        prediction = Prediction()
        path = prediction.predictionFromModel()

        predict = pd.read_csv('Prediction_Output_File/Predictions.csv')

        # showing the prediction results in a UI
        if list(predict["Prediction"])[0] == 'No':
            return render_template('predict.html', prediction="No")
        else:
            return render_template('predict.html', prediction="Yes")
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)


@app.route('/train', methods=['GET', 'POST'])
@cross_origin()
def training():
    try:

        train_obj = trainModel()
        train_obj.trainingModel()
        return render_template("index.html")

    except ValueError:
        return Response("Error Occurred! %s" % ValueError)

    except KeyError:
        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:
        return Response("Error Occurred! %s" % e)


if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s %d" % (host, port))
    httpd.serve_forever()
