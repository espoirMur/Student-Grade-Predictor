import os
import pandas as pd
import sys
sys.path.insert(0, "/Users/espyMur/Desktop/Memory-WorkingDir/Memory-Working-Dir/GradePredictorApp/codes/")
from flask_api import FlaskAPI
from flask import render_template
from predictiveModelBuilding import PredictiveModelBuilding
from config import app_config
from sklearn.externals import joblib
from flask import request, abort, jsonify
from app.predictions import predictions
from flask_wtf.csrf import CSRFProtect,generate_csrf


csrf = CSRFProtect()
def create_app(config_name):
    """this method will initialise the flask API instance """

    if os.getenv('CIRCLECI'):
        app = FlaskAPI(__name__)
        app.config.update(
            SECRET_KEY=os.getenv('SECRET_KEY')
        )
    else:
        app = FlaskAPI(__name__, instance_relative_config=True)
        app.config.from_object(app_config[config_name])
        app.config.from_pyfile('config.py')
    csrf.init_app(app)
    from .predictions import predictions as predictions_blueprint
    app.register_blueprint(predictions_blueprint)
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    @app.route('/predictions/predict/', methods=['GET', 'POST'])
    @csrf.exempt
    def predict():
        """

        the main methode use to predict

        """

        predictives_models = []
        predicted_grades = {}
        model_names = ['FM', 'FSTA', 'FD', 'FSDC', 'FSEG', 'FPSE', 'FT']
        app_floder = predictions.root_path.replace('predictions', 'static/')
        for filename in model_names:
            model = joblib.load(app_floder+'/classes/'+filename+'.pkl')
            predictives_models.append(model)
        print "hello----------------------"
        print request.get_json(force=True)
        return "done "
    #new_student_data = pd.DataFrame(new_student, columns=new_student.keys(), index=range(1))
    #print new_student_data
    """
    for dept, name in zip(predictives_models, model_names):
        predicted_grade = dept.predict_new(new_student_data)
        final_grade = predicted_grade[0]
        predicted_grades[name] = final_grade
    response = jsonify(predicted_grades)
    response.status_code = 201

    """

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    @app.errorhandler(400)
    def internal_server_error(error):
        return render_template('errors/400.html', title='Server Error'), 400
    return app
