import os
import sys
import app
import json
import pandas as pd
from sklearn.externals import joblib
sys.path.insert(0, "/Users/espyMur/Desktop/Memory-WorkingDir/Memory-Working-Dir/GradePredictorApp/codes/")
reload(sys)
sys.setdefaultencoding('utf8')
from predictiveModelBuilding import PredictiveModelBuilding
from flask import request, abort, jsonify, url_for
from . import predictions


@predictions.route('/predictions/predict/', methods=['GET', 'POST'])
def predict():
    """

    the main methode use to predict

    """

    predictives_models = []
    predicted_grades = {}
    model_names = ['FM.pkl', 'FSTA.pkl', 'FD.pkl', 'FSDC.pkl', 'FSEG.pkl', 'FPSE.pkl', 'FT.pkl']
    app_floder = predictions.root_path.replace('predictions', 'static/')
    for filename in model_names:
        model = joblib.load(app_floder+'/classes/'+filename)
        predictives_models.append(model)

    new_student = request.get_json()
    new_student_data = pd.DataFrame(new_student, columns=new_student.keys(), index=range(1))
    print new_student_data
    for dept in predictives_models:
        predicted_grade = dept.predict_new(new_student_data)
        final_grade = predicted_grade[0]
        predicted_grades[dept.__class__.__name__] = final_grade
    print predicted_grades
    response = jsonify(predicted_grades)
    response.status_code = 201
    return response
