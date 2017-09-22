import os
import sys
import app
import json
import pandas as pd
from sklearn.externals import joblib
reload(sys)
sys.setdefaultencoding('utf8')
from predictiveModelBuilding import PredictiveModelBuilding
from flask import request, abort, jsonify, url_for, render_template,redirect
from . import predictions


@predictions.route('/predictions/predict_form/', methods=['GET'])
def predict_form():
    """ this is the main route to handle the predict form"""
    return render_template('predictions/forms.html')

@predictions.route('/predictions/predict/', methods=['GET', 'POST'])
def predict():
    """

    the main method use to predict

    """
    if request.method == 'GET':
        abort(403)
    else :
        predictives_models = []
        predicted_grades = {}
        model_names = ['FM', 'FSTA', 'FD', 'FSDC', 'FSEG', 'FPSE', 'FT']
        app_floder = predictions.root_path.replace('predictions', 'static/')
        for filename in model_names:
            model = joblib.load(app_floder+'/classes/'+filename+'.pkl')
            predictives_models.append(model)

        new_student = request.data
        new_student_data = pd.DataFrame(new_student, columns=new_student.keys(), index=range(1))
        for dept, name in zip(predictives_models, model_names):
            predicted_grade = dept.predict_new(new_student_data)
            final_grade = predicted_grade[0]
            predicted_grades[name] = final_grade*100
        response = jsonify(predicted_grades)
        response.status_code = 200
        return response


@predictions.route('/predictions/results/<results>', methods=['GET'])
def view_results(results):
    """ display the predicted results """
    results = json.loads(results)
    return render_template('predictions/results.html', results=results)
