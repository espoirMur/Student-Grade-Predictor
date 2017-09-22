import os
import sys
reload(sys)
sys.setdefaultencoding('utf8') #for ascii decoder in notes
import json
import unittest
import pandas as pd
from codes.predictiveModelBuilding import PredictiveModelBuilding
from app import create_app
from testfixtures import TempDirectory
from flask import jsonify
from sklearn.externals import joblib


class GradePredictorTestCase(unittest.TestCase):
    """

    this class represent all the test cases we will use to test
    our API

    """

    def setUp(self):
        """this method will make all initialisation for ours tests"""

        if os.getenv('CIRCLECI'): #if we are in CIRCLECI environement
            self.app = create_app(config_name="CIRCLECI")
        else:
            self.app = create_app(config_name="testing")
        self.app_floder = self.app.root_path
        self.client = self.app.test_client
        self.directory = TempDirectory(
            path=self.app_floder+'/static',
            create=False)        #initialisation of temporary directory
        self.predictives_models = []
        self.new_student = {'DIPPERC':0.60, 'SCHOOL_RIGHT':'itfm/bukavu', 'OPTION_RIGHT':'elec indust'}

    def test_model_exist(self):
        """

        the following testcase will vertify if predictives models
        exist in the floder classes

        """
        self.directory.compare(sorted([
            'FM.pkl',
            'FSTA.pkl',
            'FD.pkl',
            'FSDC.pkl',
            'FSEG.pkl',
            'FPSE.pkl',
            'FT.pkl'
            ], reverse=True), path='classes/')



    def step_1_can_connect_post(self):
        """

        Test API can create a  (POST request)

        """


        res = self.client().post('predictions/predict/', data=json.dumps(self.new_student), content_type='application/json')

        self.assertEqual(res.status_code, 200)
        #self.assertIn('welcome to grade ', str(res.data))


    def step_2_can_load_models(self):
        """

        test that the app can read the model from saved floders
        here we will try to read all the modeles
        and check if there are instances of preictives models class

        """
        path = self.app_floder+'/static/classes/'
        for filename in os.listdir(path):
            model = joblib.load(path+filename)
            self.predictives_models.append(model)
            self.assertTrue(model.__class__, 'PredictiveModelBuilding' and model.__module__ == 'predictiveModelBuilding')

    def step_3_can_predict(self):
        """

        this method will test if the app can predict good values
        of students grades by goods values I mean grades betweens 30-100
        percents .

        """
        #check if the model can handle unknow schools
        new_student_data = pd.DataFrame(self.new_student, columns=self.new_student.keys(), index=range(1))
        for dept in self.predictives_models:
            predicted_grades = dept.predict_new(new_student_data)
            final_grade = predicted_grades[0]
            self.assertTrue((final_grade >= .3 or final_grade < .10) and (new_student_data['DIPPERC'][0] >= 0.50))


    def _steps(self):
        for name in sorted(dir(self)): #attributes of a object
            if name.startswith("step"):
                yield name, getattr(self, name)

    def test_steps(self):
        """for now I don't know who this works"""
        for name, step in self._steps():
            try:
                step()
            except Exception as exception:
                self.fail("{} {} failed ({}: {})".format(step, name, type(exception), exception))

    def tearDown(self):

        """
        the method will remove all variables
        used for the tests
        """


if __name__ == "__main__":
    unittest.main()
